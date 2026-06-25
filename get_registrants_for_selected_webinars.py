import os
from pathlib import Path
import json
import time

from dotenv import load_dotenv
import tomllib
import requests

# adds all key-value pairs in the `.env` file to `os.environ`
load_dotenv()

API_KEY = os.environ["WEBINARJAM_API_KEY"]

with open("config.toml", "rb") as file:
    config = tomllib.load(file)

OUTPUT_DIRECTORY_PATH = Path(config["output_folder_path"])

WEBINARS_LIST_FILENAME = config["get_all_webinars"]["output_filename"]
WEBINARS_LIST_FILE_PATH = OUTPUT_DIRECTORY_PATH / WEBINARS_LIST_FILENAME

with open(WEBINARS_LIST_FILE_PATH) as file:
    webinars = json.load(file)["webinars"]

print(f"Loaded the list of all webinars from {WEBINARS_LIST_FILE_PATH}.")
print()

ENDPOINT = config["get_registrants_for_selected_webinars"]["api_endpoint"]

INCLUDE_YEAR = config["get_registrants_for_selected_webinars"]["include_year"]
EXCLUDE_YEAR = config["get_registrants_for_selected_webinars"]["exclude_year"]

registrants = {}

for webinar in webinars:
    webinar_name = webinar["name"]
    webinar_id = webinar["webinar_id"]

    if (INCLUDE_YEAR in webinar_name or INCLUDE_YEAR in webinar["schedules"][0]) and (EXCLUDE_YEAR not in webinar_name and EXCLUDE_YEAR not in webinar["schedules"][0]):
        current_page = 1
        registrants_of_current_webinar = []

        # the WebinarJam API does not return all registrants at once, but instead splits them into pages
        # which means that a new POST request has to be sent for each page
        while True:
            print(f"[page {current_page}] Fetching registrants for webinar '{webinar_name}' (ID: {webinar_id}) ...")

            request_data = {
                "api_key": API_KEY,
                "webinar_id": webinar_id,
                "page": current_page
            }

            response = requests.post(ENDPOINT, request_data)

            response_json = response.json()
            registrants_of_current_webinar += response_json["registrants"]["data"]

            # prevent exceeding the WebinarJam API's limit of 20 API calls per second
            time.sleep(0.06)

            if (response_json["registrants"]["next_page_url"] is None):
                break

            current_page += 1

        registrants[webinar_id] = registrants_of_current_webinar
        print()

output_filename = config["get_registrants_for_selected_webinars"]["output_filename"]
output_file_path = OUTPUT_DIRECTORY_PATH / output_filename

with open(output_file_path, "w") as file:
    formatted_registrants = json.dumps(registrants, indent=4)
    file.write(formatted_registrants)

print(f"Successfully written the registrant data of {len(registrants)} webinars to {output_file_path}.")
