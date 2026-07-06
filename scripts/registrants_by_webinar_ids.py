from typing import List
import json
import logging

from config.GlobalConfig import GlobalConfig
from config.RegistrantsByWebinarConfig import RegistrantsByWebinarConfig

logging.basicConfig(level=logging.INFO)

def registrants_by_webinar_ids(webinar_ids: List[str]):
    registrants_by_webinar = []

    logging.info(
        f"attempting to parse the registrants of {len(webinar_ids)} webinars"
    )

    for id in webinar_ids:
        filename = f"{id}.json"
        file_path = (
            GlobalConfig.OUTPUT_DIRECTORY_PATH
            / RegistrantsByWebinarConfig.OUTPUT_SUBDIRECTORY / filename
        )

        logging.debug(f"attempting to read from {file_path}")

        with open(file_path) as file:
            logging.debug(
                f"attempting to parse the contents of {file_path} as JSON"
            )

            registrants_of_current_webinar = json.load(file)

        for registrant in registrants_of_current_webinar:
            registrant["webinar_id"] = id

        # concatenate the previous registrants and the current registrants
        registrants_by_webinar.extend(registrants_of_current_webinar)

    logging.info(
        f"loaded {len(registrants_by_webinar)} registrants "
        f"from {len(webinar_ids)} webinars"
        "\n"
    )

    return registrants_by_webinar
