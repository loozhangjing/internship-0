import logging

import pandas as pd

from config.GlobalConfig import GlobalConfig
from config.WebinarListConfig import WebinarListConfig

from config.WebinarsByRegistrantConfig import webinar_ids_to_names

from functions.get_registrants_by_webinar_ids\
    import get_registrants_by_webinar_ids
from functions.webinar_mapping_utils\
    import get_paid_webinar_ids_from_free_id

logging.basicConfig(level = logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


free_webinar_ids = WebinarListConfig.get_free_webinar_ids()

df = pd.DataFrame(index=free_webinar_ids)

for free_webinar_id in free_webinar_ids:
    free_registrants_df = pd.DataFrame(
        get_registrants_by_webinar_ids([free_webinar_id])
    )

    # remove duplicate free registrants
    free_registrants_df = free_registrants_df.groupby("email").first()


    paid_webinar_ids = get_paid_webinar_ids_from_free_id(free_webinar_id)

    if paid_webinar_ids is None:
        raise Exception(
            f"no paid webinar IDs found for free webinar ID {free_webinar_id}"
        )

    paid_registrants_df = pd.DataFrame()

    for paid_webinar_id in paid_webinar_ids:
        paid_registrants = get_registrants_by_webinar_ids([paid_webinar_id])
        new_df = pd.DataFrame(paid_registrants)

        paid_registrants_df = pd.concat([paid_registrants_df, new_df])

    count_including_duplicates = paid_registrants_df.shape[0]

    # remove duplicate registrants, some due to the previous concatenation
    paid_registrants_df = paid_registrants_df.groupby("email").first()

    count_without_duplicates = paid_registrants_df.shape[0]

    logger.debug(
        f"for paid webinars {paid_webinar_ids}:"
        "\n"
        f"{count_including_duplicates} registrants in total, "
        f"{count_without_duplicates} unique"
        "\n"
    )

    paid_webinar_ids = [str(id) for id in paid_webinar_ids]
    paid_webinar_names = [webinar_ids_to_names[id] for id in paid_webinar_ids]

    free_registrant_count = free_registrants_df.shape[0]
    paid_registrant_count = paid_registrants_df.shape[0]

    df.loc[free_webinar_id, "Conversion rate (%)"] = paid_registrant_count / free_registrant_count * 100
    df.loc[free_webinar_id, "Number of unique free registrants"] = free_registrant_count
    df.loc[free_webinar_id, "Number of unique paid registrants"] = paid_registrant_count
    df.loc[free_webinar_id, "Paid webinar name(s)"] = "\n".join(paid_webinar_names)

GlobalConfig.pretty_print_df(df)
