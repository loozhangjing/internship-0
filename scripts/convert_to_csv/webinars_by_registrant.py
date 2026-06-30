from pathlib import Path
import json

import tomllib
import pandas as pd

with open("config.toml", "rb") as file:
    config = tomllib.load(file)

OUTPUT_DIRECTORY_PATH = Path(config["output_folder"])

WEBINARS_BY_REGISTRANT_FILE_PATH = OUTPUT_DIRECTORY_PATH / config["transform_into_webinars_by_registrant"]["output_filename"]

OUTPUT_FILE_PATH = OUTPUT_DIRECTORY_PATH / Path(config["convert_webinars_by_registrant_to_csv"]["output_filename"])

with open(WEBINARS_BY_REGISTRANT_FILE_PATH) as file:
    registrants_df = pd.read_json(file).transpose()

registrants_df = registrants_df.rename(columns = {
    "first_name": "First name",
    "last_name": "Last name",
    "phone_country_code": "Phone country code",
    "phone_number": "Phone number",
    "total_registered": "Total registered webinars",
    "total_attended": "Total attended webinars",
})

with open(OUTPUT_FILE_PATH, "w") as file:
    file.write(registrants_df.to_csv())
