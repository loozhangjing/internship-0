import re
import json

from config.GlobalConfig import GlobalConfig
from config.WebinarListConfig import WebinarListConfig

WEBINAR_LIST_PATH = (
    GlobalConfig.OUTPUT_DIRECTORY_PATH
    / WebinarListConfig.OUTPUT_FILENAME
)

with open(WEBINAR_LIST_PATH) as file:
    webinar_list = json.load(file)

    # create a mapping of numeric webinar IDs to the webinar names, based on
    # the data in the file specified in `WebinarListConfig.OUTPUT_FILENAME`
    webinar_ids_to_names =  {
        str(webinar["webinar_id"]): webinar["name"] for webinar in webinar_list
    }

class WebinarsByRegistrantConfig:
    OUTPUT_FILENAME = "webinars_by_registrant.csv"

    # characters used in each cell in the output CSV file to represent
    # the status of a registrant for a particular webinar
    PAID_CHARACTER = "RM ?"
    ATTENDED_FREE_CHARACTER = "✔"
    REGISTERED_FREE_CHARACTER = "O"

    # should be passed to the `.apply()` method of a `pandas.DataFrame`
    @staticmethod
    def format_row(row):
        row.first_name = row.first_name.title()
        row.last_name = row.last_name.title()

        # this is a new column
        row["phone_number_formatted"] = format_phone_number(row.phone_number)

        row.phone_number = f"{row.phone_country_code} {row.phone_number}"

        return row

    COLUMN_LABEL_RENAME_MAPPINGS = {
        "first_name": "First name",
        "last_name": "Last name",
        "phone_number": "Phone number (as entered)",
        "phone_number_formatted": "Phone number (automatically formatted)",
        "total_paid": "Total PAID webinars registered/attended",
        "total_free_attended": "Total FREE webinars attended",
        "total_free_registered": "Total FREE webinars registered/attended",
    }

    webinar_ids_to_names = webinar_ids_to_names

    # labels of the columns to keep (all other columns will be deleted) for
    # the 'registrants by webinar' data loaded from the `.json` files
    RELEVANT_COLUMNS_BEFORE_GROUPING = [
        "email",
        "first_name",
        "last_name",
        "phone_country_code",
        "phone_number",
        "webinar_id",
        "attended_live"
    ]

    # labels of the columns to remove after every row with the same email has
    # been combined, i.e. the 'registrants by webinar' data has been
    # converted to a 'webinars by registrant' format
    COLUMNS_TO_DROP_AFTER_GROUPING = [
        "phone_country_code",
        "webinar_id",
        "attended_live"
    ]

def format_phone_number(phone_number):
    """
    Examples:
    format_phone_number("012 345678")
    # -> "012 345 678"
    format_phone_number("+60123456789")
    # -> "012 345 6789"
    format_phone_number("03123456")
    # -> "03 123456"
    """

    # make the phone number numeric-only
    # i.e. remove extraneous characters like '-'
    # ('\D' in a regular expression means any digit)
    phone_number_digits_only = re.sub(r"\D", "", str(phone_number))

    # convert the phone number to an integer, then back to a string
    # to remove any trailing/leading zeroes
    formatted_phone_number = str(int(phone_number_digits_only))

    # if the phone number begins with a '60',
    # and its length is that of a home phone number,
    # (60 xx xxx xxxx) or (60 xx xxxx xxxx)
    # remove the '60'
    if formatted_phone_number[:2] == "60"\
    and len(formatted_phone_number) == 11 or len(formatted_phone_number) == 12:
        formatted_phone_number = formatted_phone_number[2:]

    formatted_phone_number = "0" + formatted_phone_number

    if formatted_phone_number[1] == "1":
        # if a phone number is 10 digits long, format it as 01x xxx xxxx
        # if it's 11 digits long: 01x xxxx xxxx
        second_section_length = 3
        if len(formatted_phone_number) == 11:
            second_section_length = 4

        formatted_phone_number = (
            f"{formatted_phone_number[:3]} "
            f"{formatted_phone_number[3:second_section_length + 3]} "
            f"{formatted_phone_number[second_section_length + 3:]}"
        )
    else:
        # for phone numbers that don't begin with "01" (e.g. 03 xxxxxxx)
        formatted_phone_number = (
            f"{formatted_phone_number[:2]} "
            f"{formatted_phone_number[2:]}"
        )

    return formatted_phone_number
