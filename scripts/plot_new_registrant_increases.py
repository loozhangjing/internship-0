import logging

import pandas as pd

from config.PlotNewRegistrantIncreasesConfig\
    import PlotNewRegistrantIncreasesConfig

from functions.webinar_ids_by_query import webinar_ids_by_query
from registrants_by_webinar_ids import registrants_by_webinar_ids

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

desired_webinar_ids = webinar_ids_by_query(
    PlotNewRegistrantIncreasesConfig.WEBINAR_MUSTVE_BEEN_HELD_IN_THE_YEARS,
    PlotNewRegistrantIncreasesConfig.WEBINAR_NAMES_MUST_INCLUDE_ONE_OF
)

registrants = registrants_by_webinar_ids(desired_webinar_ids)

df = pd.DataFrame(registrants)

# reverse the the order of rows so the earlier webinars appear first
df = df.iloc[:, ::-1]

grouped = df.groupby("webinar_id")

new_registrants = {}
encountered_emails = []

for (webinar_id, webinar_df) in grouped:
    new_emails = []

    for email in webinar_df.loc[:, "email"]:
        if email not in encountered_emails:
            if webinar_id not in new_registrants:
                new_registrants[webinar_id] = 0
            new_registrants[webinar_id] += 1
            new_emails.append(email)

    logger.debug(
        f"there are {webinar_df.shape[0]} registrants "
        f"for webinar {webinar_id}, "
        f"with {len(new_emails)} of them being new"
    )

    encountered_emails.extend(new_emails)

logging.info(
    "number of new registrants per webinar: "
    "\n"
    f"{new_registrants}"
)
