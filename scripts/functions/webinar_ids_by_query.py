import logging
import json
from datetime import datetime
from typing import List

from config.GlobalConfig import GlobalConfig
from config.WebinarListConfig import WebinarListConfig

logging.basicConfig(level=logging.INFO)

def webinar_ids_by_query(
        included_years: List[int],
        names_must_include_one_of: List[str]
):
    WEBINAR_LIST_FILE_PATH = (
        GlobalConfig.OUTPUT_DIRECTORY_PATH
        / WebinarListConfig.OUTPUT_FILENAME
    )

    with open(WEBINAR_LIST_FILE_PATH) as file:
        webinar_list = json.load(file)

    matching_webinar_ids = []

    for webinar in webinar_list:
        id = webinar["webinar_id"]
        name = webinar["name"]
        date_str = webinar["schedules"][0]

        try:
            webinar_datetime = datetime.strptime(
                date_str,
                WebinarListConfig.STRPTIME_FORMAT
            )
        except ValueError:
            logging.debug(
                f"date '{date_str}' for the webinar '{name}' "
                f"could not be parsed, skipping webinar '{name}'"
            )
            continue

        for year in included_years:
            if webinar_datetime.year == year:
                for string in names_must_include_one_of:
                    string = string.lower()
                    if string in name.lower():
                        logging.debug(
                            f"webinar '{name}' was held in the year {year} "
                            f"and has '{string}' in its name, "
                            f"adding webinar {id} to the list"
                        )
                        matching_webinar_ids.append(id)

    return matching_webinar_ids
