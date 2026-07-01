import os
import sys
import pathlib
import json
import logging

from dotenv import load_dotenv
import requests

from config.GlobalConfig import GlobalConfig
from config.WebinarListConfig import WebinarListConfig

logging.basicConfig(level=logging.INFO)

load_dotenv()
request_data = {
    "api_key": os.environ["WEBINARJAM_API_KEY"]
}

logging.info(f"fetching the list of webinars from {WebinarListConfig.API_ENDPOINT}...")

response = requests.post(WebinarListConfig.API_ENDPOINT, request_data)
logging.info("response received")

response_json = response.json()
logging.info("response converted to JSON")

webinars = response_json["webinars"]
logging.info(f"there are {len(webinars)} webinars")

OUTPUT_DIRECTORY_PATH = pathlib.Path(GlobalConfig.OUTPUT_DIRECTORY)

# create the output directory if it doesn't yet exist
OUTPUT_DIRECTORY_PATH.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE_PATH = OUTPUT_DIRECTORY_PATH / WebinarListConfig.OUTPUT_FILENAME

if os.path.isfile(OUTPUT_FILE_PATH) is True:
    print()
    overwrite = input(f"{OUTPUT_FILE_PATH} already exists. overwrite? ")
    print()

    overwrite = overwrite.lower().strip()

    if overwrite != "y" and overwrite != "yes":
        logging.info(f"{OUTPUT_FILE_PATH} remains unchanged")
        sys.exit()

    logging.info(f"overwriting {OUTPUT_FILE_PATH}")

with open(OUTPUT_FILE_PATH, "w") as file:
    formatted_response = json.dumps(webinars, indent=4)
    file.write(formatted_response)

logging.info(f"wrote {len(formatted_response)} characters to {OUTPUT_FILE_PATH}")
