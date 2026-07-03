import logging

import pandas as pd

from registrants_by_webinar_ids import registrants_by_webinar_ids
from config.WebinarsByRegistrant import WebinarsByRegistrantConfig

logging.basicConfig(level=logging.INFO)

registrants_for_selected_webinars = registrants_by_webinar_ids(WebinarsByRegistrantConfig.WEBINAR_IDS)

registrants_by_webinar = pd.DataFrame(registrants_for_selected_webinars)

# select only relevant columns so the other columns are dropped (removed)
registrants_by_webinar = registrants_by_webinar[WebinarsByRegistrantConfig.RELEVANT_COLUMNS_BEFORE_GROUPING]

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

# remove irrelevant columns
webinars_by_registrant = registrants_by_webinar.drop(
    labels = WebinarsByRegistrantConfig.COLUMNS_TO_DROP_AFTER_GROUPING,
    axis = "columns"
)

# move the columns representing webinars to the end
webinar_column_labels = [e for e in webinars_by_registrant.columns.tolist() if e not in WebinarsByRegistrantConfig.COLUMNS_THAT_COME_FIRST]
webinars_by_registrant = pd.concat(
    [
        webinars_by_registrant.loc[:, WebinarsByRegistrantConfig.COLUMNS_THAT_COME_FIRST],
        webinars_by_registrant.loc[:, webinar_column_labels]
    ],
    axis = "columns"
)

# format the values of every cell
webinars_by_registrant = webinars_by_registrant.apply(
    WebinarsByRegistrantConfig.format_row,
    axis = "columns"
)

# make all emails (which are the row labels) lowercase
webinars_by_registrant.rename(str.lower, inplace = True)

webinars_by_registrant.rename(
    WebinarsByRegistrantConfig.COLUMN_LABEL_RENAME_MAPPINGS,
    axis = "columns",
    inplace = True
)

# rename column labels of numeric webinar IDs into the corresponding webinar names
webinars_by_registrant.rename(
    WebinarsByRegistrantConfig.webinar_ids_to_names,
    axis = "columns",
    inplace = True
)

with pd.option_context({ "display.max_rows": None, "display.max_columns": None, "display.width": None }):
    print(webinars_by_registrant)
