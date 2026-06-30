from pathlib import Path
import json
import re

import tomllib
import pandas as pd

with open("config.toml", "rb") as file:
    config = tomllib.load(file)

OUTPUT_DIRECTORY_PATH = Path(config["output_folder"])

WEBINAR_LIST_FILE_PATH = OUTPUT_DIRECTORY_PATH / config["fetch_webinar_list"]["output_filename"]

WEBINARS_BY_REGISTRANT_FILE_PATH = OUTPUT_DIRECTORY_PATH / config["transform_into_webinars_by_registrant"]["output_filename"]

OUTPUT_FILE_PATH = OUTPUT_DIRECTORY_PATH / Path(config["convert_webinars_by_registrant_to_csv"]["output_filename"])

with open(WEBINAR_LIST_FILE_PATH) as file:
    webinar_list = json.load(file)

with open(WEBINARS_BY_REGISTRANT_FILE_PATH) as file:
    registrants_df = pd.read_json(file, orient="index")

# iterate over lists of webinars each registrant has registered for
for email, webinars in registrants_df["webinars"].items():
    # iterate over each webinar the current registrant has registered for
    for webinar_id, stats in webinars.items():
        # `webinar_id` is a string because JSON keys must be strings
        webinar_id_int = int(str(webinar_id))

        # find basic information for the current webinar from `webinar_list` using its ID
        webinar_info = next(webinar for webinar in webinar_list if webinar["webinar_id"] == webinar_id_int)
        # .strip() removes leading and trailing whitespace
        webinar_name = webinar_info["name"].strip()

        if stats["attended"] is True:
            registrants_df.loc[email, webinar_name] = "✔"
            continue

        registrants_df.loc[email, webinar_name] = "O"

# remove the "webinars" column because all its JSON data has already been added as new columns
# remove the "phone_country_code" column because it seems like all phone numbers are local
registrants_df.drop(
    columns = ["webinars", "phone_country_code"],
    inplace = True
)

def capitalize_each_word(string):
    return string.title()

registrants_df["first_name"] = registrants_df["first_name"].map(capitalize_each_word)
registrants_df["last_name"] = registrants_df["last_name"].map(capitalize_each_word)

for email, phone_number in registrants_df["phone_number"].items():
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

    registrants_df.loc[email, "phone_number"] = formatted_phone_number


registrants_df.sort_values(
    by = "total_attended",
    ascending = False,
    inplace = True
)

registrants_df.rename(
    columns = {
        "first_name": "First name",
        "last_name": "Last name",
        "phone_number": "Phone number",
        "total_registered": "Total registered webinars",
        "total_attended": "Total attended webinars",
    },
    inplace = True
)

with open(OUTPUT_FILE_PATH, "w") as file:
    file.write(registrants_df.to_csv())
