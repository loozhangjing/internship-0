import logging

import pandas as pd

from functions.get_registrants_by_webinar_ids\
    import get_registrants_by_webinar_ids
from functions.webinar_mapping_utils import get_paid_webinar_ids_from_learnabee_name
from config.GlobalConfig import GlobalConfig
from config.WebinarListConfig import WebinarListConfig
from config.WebinarsByRegistrantConfig import WebinarsByRegistrantConfig
from config.AggregateRevenueConfig import AggregateRevenueConfig

logging.basicConfig(level=logging.INFO)

webinar_ids = []
for (key, value) in WebinarListConfig.FREE_TO_PAID_WEBINAR_IDS.items():
    webinar_ids.extend(list(key))
    webinar_ids.extend(list(value))

# convert integer IDs into strings
webinar_ids = [str(id) for id in webinar_ids]

registrants_for_selected_webinars = get_registrants_by_webinar_ids(webinar_ids)

registrants_by_webinar = pd.DataFrame(registrants_for_selected_webinars)

# select only relevant columns so the other columns are dropped (removed)
registrants_by_webinar = registrants_by_webinar[
    WebinarsByRegistrantConfig.RELEVANT_COLUMNS_BEFORE_GROUPING
]

logging.info(
    f"there are {len(registrants_by_webinar.email.unique())} "
    f"unique registrants (as identified by their emails) "
    f"across {len(webinar_ids)} webinars"
    "\n"
)

def add_a_column_for_every_unique_webinar(row):
    if WebinarListConfig.is_paid_webinar_id(int(row.webinar_id)) is True:
        value = WebinarsByRegistrantConfig.PAID_CHARACTER
    elif row.attended_live == "Yes":
        value = WebinarsByRegistrantConfig.ATTENDED_FREE_CHARACTER
    else:
        value = WebinarsByRegistrantConfig.REGISTERED_FREE_CHARACTER

    row[str(row.webinar_id)] = value
    return row

registrants_by_webinar = registrants_by_webinar.apply(
    add_a_column_for_every_unique_webinar,
    axis="columns"
)

# combines all rows with the same email
# for every column's value, take the first value that's not NaN
webinars_by_registrant = registrants_by_webinar.groupby("email").first()

# format the values of every cell of the relevant columns
webinars_by_registrant = webinars_by_registrant.apply(
    WebinarsByRegistrantConfig.format_row,
    axis = "columns"
)

# remove irrelevant columns
webinars_by_registrant = webinars_by_registrant.drop(
    labels = WebinarsByRegistrantConfig.COLUMNS_TO_DROP_AFTER_GROUPING,
    axis = "columns"
)

def add_columns_for_total_webinars_joined(row):
    row["total_paid"] = sum(
        1 for value in row[webinar_ids]
        if value == WebinarsByRegistrantConfig.PAID_CHARACTER
    )
    row["total_free_attended"] = sum(
        1 for value in row[webinar_ids]
        if value == WebinarsByRegistrantConfig.ATTENDED_FREE_CHARACTER
    )
    row["total_free_registered"] = sum(
        1 for value in row[webinar_ids]
        if value == WebinarsByRegistrantConfig.REGISTERED_FREE_CHARACTER
        or value == WebinarsByRegistrantConfig.ATTENDED_FREE_CHARACTER
    )

    return row

webinars_by_registrant = webinars_by_registrant.apply(
    add_columns_for_total_webinars_joined,
    axis="columns"
)

# make all emails (which are the row labels) lowercase
webinars_by_registrant.rename(str.lower, inplace = True)

webinars_by_registrant.rename(
    WebinarsByRegistrantConfig.COLUMN_LABEL_RENAME_MAPPINGS,
    axis = "columns",
    inplace = True
)

# move the columns representing webinars to the end
columns_that_come_first = [
    label for label in webinars_by_registrant.columns.tolist()
    if label not in webinar_ids
] # non-webinar-ID column labels
webinars_by_registrant = pd.concat(
    [
        webinars_by_registrant.loc[:, columns_that_come_first],
        webinars_by_registrant.loc[:, webinar_ids]
    ],
    axis = "columns"
)


REVENUE_BY_REGISTRATION_FILE_PATH = (
    GlobalConfig.OUTPUT_DIRECTORY_PATH
    / AggregateRevenueConfig.CSV_INPUT_FILENAME
)

logging.info(
    f"attempting to load CSV data from {REVENUE_BY_REGISTRATION_FILE_PATH}..."
)

revenue_by_registration = pd.read_csv(REVENUE_BY_REGISTRATION_FILE_PATH)

def add_revenue(row):
    email = row[AggregateRevenueConfig.CSV_COLUMN_NAMES.EMAIL]
    if type(email) is not str:
        logging.error(f"email '{email}' is not a string")
        return row

    email = email.lower()

    # remember that this is the name in Learnabee, not in WebinarJam
    learnabee_webinar_name = row[
        AggregateRevenueConfig.CSV_COLUMN_NAMES.WEBINAR_NAME
    ]

    learnabee_webinar_name = str(learnabee_webinar_name)

    # remove all zero-width spaces because some webinar names contain it
    # for some reason
    learnabee_webinar_name = learnabee_webinar_name.replace("\u200b", "")

    try:
        webinar_ids = get_paid_webinar_ids_from_learnabee_name(
            learnabee_webinar_name
        )
        # to be continued
    except StopIteration:
        logging.error(
            "could not find corresponding paid webinar ID(s) for "
            f"'{learnabee_webinar_name}'"
        )

    return row

revenue_by_registration.apply(
    add_revenue,
    axis="columns"
)


# rename the column labels that are numeric webinar IDs
# into their corresponding webinar names
webinars_by_registrant.rename(
    WebinarsByRegistrantConfig.webinar_ids_to_names,
    axis = "columns",
    inplace = True
)

OUTPUT_FILE_PATH = (
    GlobalConfig.OUTPUT_DIRECTORY_PATH
    / WebinarsByRegistrantConfig.OUTPUT_FILENAME
)
with open(OUTPUT_FILE_PATH, "w") as file:
    csv = webinars_by_registrant.to_csv()
    file.write(csv)

    logging.info(f"wrote {len(csv)} characters to {OUTPUT_FILE_PATH}")
