import logging

import pandas as pd

from config.GlobalConfig import GlobalConfig
from config.WebinarListConfig import WebinarListConfig

from functions.get_registrants_by_webinar_ids\
    import get_registrants_by_webinar_ids
from functions.webinar_mapping_utils\
    import get_paid_webinar_ids_from_free_id

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


free_webinar_ids = WebinarListConfig.get_free_webinar_ids()

df = pd.DataFrame(index=free_webinar_ids)

for free_webinar_id in free_webinar_ids:
    registrants = get_registrants_by_webinar_ids([free_webinar_id])

    df.loc[free_webinar_id, "free_registrant_count"] = len(registrants)

    paid_webinar_ids = get_paid_webinar_ids_from_free_id(free_webinar_id)

    if paid_webinar_ids is None:
        raise Exception(
            f"no paid webinar IDs found for free webinar ID {free_webinar_id}"
        )

    paid_webinar_ids = [str(id) for id in paid_webinar_ids]

    df.loc[free_webinar_id, "paid_webinar_id"] = " & ".join(paid_webinar_ids)

GlobalConfig.pretty_print_df(df)
