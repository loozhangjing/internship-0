import logging

import pandas as pd

from registrants_by_webinar_ids import registrants_by_webinar_ids
from config.WebinarsByRegistrant import WebinarsByRegistrantConfig

logging.basicConfig(level=logging.INFO)

registrants_for_selected_webinars = registrants_by_webinar_ids([1228, 1229])

registrants_by_webinar = pd.DataFrame(registrants_for_selected_webinars)

# select only relevant columns so the other columns are dropped (removed)
registrants_by_webinar = registrants_by_webinar[WebinarsByRegistrantConfig.RELEVANT_COLUMNS]

unique_emails = registrants_by_webinar.email.unique()
webinar_ids = registrants_by_webinar.webinar_id.unique()

logging.info(f"there are {len(unique_emails)} unique registrants (identified by their emails) across {len(webinar_ids)} webinars")

def add_a_column_for_every_unique_webinar(row):
    new_column_name = str(row.webinar_id)

    if row.attended_live == "Yes":
        row[new_column_name] = "attended"
    else:
        row[new_column_name] = "registered"
    return row

registrants_by_webinar = registrants_by_webinar.apply(add_a_column_for_every_unique_webinar, axis="columns")

# combines all rows with the same email
# for every column's value, take the first value that's not NaN
registrants_by_webinar = registrants_by_webinar.groupby("email").first()

with pd.option_context({ "display.max_rows": None, "display.max_columns": None, "display.width": None }):
    print(registrants_by_webinar)
