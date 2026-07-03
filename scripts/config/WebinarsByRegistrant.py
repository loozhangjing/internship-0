import re

class WebinarsByRegistrantConfig:
    # in order
    WEBINAR_IDS = [
        1201, 1204,
        1202, 1203,
        1181, 1189,
        1176, 1177,
    ]

    # should be passed to the `.apply()` method of a `DataFrame`
    @staticmethod
    def format_row(row):
        row.first_name = row.first_name.title()
        row.last_name = row.last_name.title()

        row.phone_number = format_phone_number(row.phone_number)

        return row

    COLUMN_LABEL_RENAME_MAPPINGS = {
        "first_name": "First name",
        "last_name": "Last name",
        "phone_number": "Phone number"
    }

    # labels of the columns to keep (all other columns will be deleted) for the data loaded from the `.json` files, i.e. the registrants by webinar
    RELEVANT_COLUMNS_BEFORE_GROUPING = [
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "webinar_id",
        "attended_live"
    ]

    # labels of the columns to remove after every row with the same email has been combined, i.e. the data in webinars by registrant form
    COLUMNS_TO_DROP_AFTER_GROUPING = [
        "webinar_id",
        "attended_live"
    ]

    # labels of the columns to rearrange in front of the columns representing webinars
    COLUMNS_THAT_COME_FIRST = [
        "first_name",
        "last_name",
        "phone_number"
    ]

def format_phone_number(phone_number):
    # make phone numbers numeric-only (remove extraneous characters like '-')
    # \D in a regular expression means any digit
    phone_number_digits_only = re.sub(r"\D", "", str(phone_number))

    # convert them to integers (to remove any trailing/leading zeroes)
    phone_number_int = int(phone_number_digits_only)

    formatted_phone_number = str(phone_number_int)

    # a phone number beginning with "60" will not have been truncated by turning it into an int
    if formatted_phone_number[:2] == "60" and len(formatted_phone_number) > 11:
        formatted_phone_number = formatted_phone_number[2:]

    formatted_phone_number = "0" + formatted_phone_number

    if formatted_phone_number[1] == "1":
        # if a phone number is 10 digits long, format it as 01x xxx xxxx
        # if it's 11 digits long: 01x xxxx xxxx
        second_section_length = 3
        if len(formatted_phone_number) == 11:
            second_section_length = 4

        formatted_phone_number = formatted_phone_number[:3] + " " + formatted_phone_number[3:second_section_length + 3] + " " + formatted_phone_number[second_section_length + 3:]
    else:
        # for phone numbers that don't begin with "01" (e.g. 03 xxxxxxx)
        formatted_phone_number = formatted_phone_number[:2] + " " + formatted_phone_number[2:]

    return formatted_phone_number
