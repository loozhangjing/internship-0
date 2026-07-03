import logging

import pandas as pd

from registrants_by_webinar_ids import registrants_by_webinar_ids
from config.WebinarsByRegistrant import WebinarsByRegistrantConfig

logging.basicConfig(level=logging.INFO)

registrants_for_selected_webinars = registrants_by_webinar_ids([1228, 1229])

df = pd.DataFrame(registrants_for_selected_webinars)

# select only relevant columns so the other columns are dropped (removed)
df = df[WebinarsByRegistrantConfig.RELEVANT_COLUMNS]

unique_email_count = len(df.email.unique())
webinar_count = len(df.webinar_id.unique())

logging.info(f"there are {unique_email_count} unique registrants (identified by their emails) across {webinar_count} webinars")
