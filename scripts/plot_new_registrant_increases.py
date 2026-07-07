from datetime import datetime
import re
import logging

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from config.GlobalConfig import GlobalConfig
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

new_registrants_dict = {}
encountered_emails = []

for (_webinar_id, webinar_df) in grouped:
    registrant_count_with_duplicates = webinar_df.shape[0]

    # remove duplicate emails
    webinar_df = webinar_df.drop_duplicates(subset="email")

    webinar_name = webinar_df.loc[:, "webinar"].iloc[0].strip()

    webinar_datetime = datetime.strptime(
        webinar_df.loc[:, "schedule"].iloc[0],
        PlotNewRegistrantIncreasesConfig.STRPTIME_FORMAT
    ).strftime(PlotNewRegistrantIncreasesConfig.STRFTIME_FORMAT)

    # remove text inside the first occurence of brackets (between "(" and ")")
    webinar_name = re.sub("^\\(.*?\\)", "", webinar_name)
    webinar_name = f"[{webinar_datetime}] {webinar_name}"

    new_emails = []

    for email in webinar_df.loc[:, "email"]:
        if email not in encountered_emails:
            if webinar_name not in new_registrants_dict:
                new_registrants_dict[webinar_name] = 0
            new_registrants_dict[webinar_name] += 1
            new_emails.append(email)

    logger.debug(
        "\n"
        f"there are {webinar_df.shape[0]} registrants "
        f"(with {registrant_count_with_duplicates - webinar_df.shape[0]} "
        "duplicates having been removed)"
        "\n"
        f"for webinar '{webinar_name}',"
        "\n"
        f"with {len(new_emails)} of them being new"
    )

    encountered_emails.extend(new_emails)

# render Chinese characters properly
matplotlib.rc("font", family="Noto Sans CJK SC")

fig, ax = plt.subplots()

new_registrant_counts = list(new_registrants_dict.values())
webinar_names = list(new_registrants_dict.keys())

webinar_count = len(webinar_names)

ax.set_xlabel("Number of new unique registrants")
ax.set_ylabel("Webinar")

ax.plot(new_registrant_counts, np.arange(webinar_count))

ax.set_yticks(
    list(n for n in range(webinar_count)),
    labels=webinar_names
)

OUTPUT_PATH = (
    GlobalConfig.OUTPUT_DIRECTORY_PATH
    / PlotNewRegistrantIncreasesConfig.OUTPUT_SUBDIRECTORY
)

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# `bbox_inches="tight"` prevents the axis labels from overflowing the screen
# and being hidden
plt.savefig(OUTPUT_PATH / "plot.pdf", bbox_inches="tight")
