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

output_directory_path = Path(config["output_folder_path"])

webinar_list_filename = config["get_all_webinars"]["output_filename"]
webinar_list_file_path = output_directory_path / webinar_list_filename

output_filename = config["get_registrants_for_selected_webinars"]["output_filename"]
output_file_path = output_directory_path / output_filename

print(f"reading the list of all webinars from {webinar_list_file_path}...\n")

with open(webinar_list_file_path) as file:
    webinars = json.load(file)["webinars"]

endpoint = config["get_registrants_for_selected_webinars"]["api_endpoint"]

year = "2026"
registrants = {}

for webinar in webinars:
    if year in webinar["name"] or year in webinar["schedules"][0]:
        webinar_id = webinar["webinar_id"]

        request_data = {
            "api_key": API_KEY,
            "webinar_id": webinar_id
        }
        print(f"getting registrants for webinar '{webinar["name"]}' with id {webinar_id}...")

        response = requests.post(endpoint, request_data)

        response_json = response.json()
        registrants[webinar_id] = response_json["registrants"]["data"]

        # prevent exceeding the WebinarJam API's limit of 20 API calls per second
        time.sleep(0.1)

with open(output_file_path, "w") as file:
    formatted_registrants = json.dumps(registrants, indent=4)
    file.write(formatted_registrants)

print("\nsuccessfully written the registrant data of", len(registrants), "webinars to", output_file_path)
