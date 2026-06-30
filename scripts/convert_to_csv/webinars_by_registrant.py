from pathlib import Path
import json

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
            registrants_df.loc[email, webinar_name] = "ATTENDED"
            continue

        registrants_df.loc[email, webinar_name] = "registered"

# remove the "webinars" column
registrants_df.drop(
    columns = ["webinars"],
    inplace = True
)

registrants_df.rename(
    columns = {
        "first_name": "First name",
        "last_name": "Last name",
        "phone_country_code": "Phone country code",
        "phone_number": "Phone number",
        "total_registered": "Total registered webinars",
        "total_attended": "Total attended webinars",
    },
    inplace = True
)

with open(OUTPUT_FILE_PATH, "w") as file:
    file.write(registrants_df.to_csv())
