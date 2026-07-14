import logging

import pandas as pd

from config.GlobalConfig import GlobalConfig
from config.CalculateConversionRatesConfig\
    import CSVColumnNames, CalculateConversionRatesConfig
from config.WebinarListConfig import WebinarListConfig
from config.WebinarsByRegistrantConfig import WebinarsByRegistrantConfig

from functions.get_registrants_by_webinar_ids\
    import get_registrants_by_webinar_ids
from functions.webinar_mapping_utils\
    import get_paid_webinar_ids_from_free_id

logging.basicConfig(level = logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

COLUMN_NAMES = CalculateConversionRatesConfig.CSV_COLUMN_NAMES

def remove_rows_with_duplicate_emails(df: pd.DataFrame):
    return df.groupby("email").first()

def get_unique_paid_registrants(paid_webinar_ids: list[str]) -> pd.DataFrame:
    # initialise an empty `DataFrame`
    paid_registrants_df = pd.DataFrame()

    for paid_webinar_id in paid_webinar_ids:
        paid_registrants = get_registrants_by_webinar_ids([paid_webinar_id])
        new_df = pd.DataFrame(paid_registrants)

        # note that many registrants who have joined the paid webinar(s) of the
        # previous loop iteration(s) will have joined this webinar too, so,
        # at this point, there will be lots of rows with duplicate emails
        paid_registrants_df = pd.concat([paid_registrants_df, new_df])

    count_including_duplicates = paid_registrants_df.shape[0]

    paid_registrants_df = remove_rows_with_duplicate_emails(
        paid_registrants_df
    )

    count_without_duplicates = paid_registrants_df.shape[0]

    logger.debug(
        f"for paid webinar(s) {",".join(paid_webinar_ids)}:"
        "\n"
        f"{count_including_duplicates} registrants in total, "
        f"{count_without_duplicates} unique"
        "\n"
    )

    return paid_registrants_df


free_webinar_ids = WebinarListConfig.get_free_webinar_ids()

df = pd.DataFrame(index=free_webinar_ids)

for free_webinar_id in free_webinar_ids:
    total_free_registrants_df = pd.DataFrame(
        get_registrants_by_webinar_ids([free_webinar_id])
    )

    attended_free_registrants_df = total_free_registrants_df.loc[
        total_free_registrants_df.attended_live == "Yes"
    ]

    total_free_registrants_df = remove_rows_with_duplicate_emails(
        total_free_registrants_df
    )
    attended_free_registrants_df = remove_rows_with_duplicate_emails(
        attended_free_registrants_df
    )

    paid_webinar_ids = [
        str(id) for id in get_paid_webinar_ids_from_free_id(free_webinar_id)
    ]

    paid_registrants_df = get_unique_paid_registrants(paid_webinar_ids)

    paid_webinar_names = [
        WebinarsByRegistrantConfig.webinar_ids_to_names[id]
        for id in paid_webinar_ids
    ]

    total_free_registrant_count = total_free_registrants_df.shape[0]
    attended_free_registrant_count = attended_free_registrants_df.shape[0]
    paid_registrant_count = paid_registrants_df.shape[0]

    if attended_free_registrant_count == 0:
        attended_paid_conversion_rate = 0
    else:
        attended_paid_conversion_rate = (
            paid_registrant_count / attended_free_registrant_count * 100
        )

    df.loc[free_webinar_id, CSVColumnNames.ATTENDED_PAID_CONVERSION_RATE]\
        = attended_paid_conversion_rate
    df.loc[free_webinar_id, CSVColumnNames.TOTAL_PAID_CONVERSION_RATE]\
        = paid_registrant_count / total_free_registrant_count * 100

    df.loc[free_webinar_id, CSVColumnNames.ATTENDED_FREE_REGISTRANT_COUNT]\
        = attended_free_registrant_count
    df.loc[free_webinar_id, CSVColumnNames.TOTAL_FREE_REGISTRANT_COUNT]\
        = total_free_registrant_count

    df.loc[free_webinar_id, CSVColumnNames.PAID_REGISTRANT_COUNT]\
        = paid_registrant_count
    df.loc[free_webinar_id, CSVColumnNames.PAID_WEBINAR_NAMES]\
        = "\n".join(paid_webinar_names)

# convert row indices (which are free webinar IDs) into strings)
df = df.rename(lambda id: str(id), axis="rows")

# rename the row indices (which are free webinar IDs) to webinar names
df = df.rename(WebinarsByRegistrantConfig.webinar_ids_to_names, axis="rows")

OUTPUT_FILE_PATH = (
    GlobalConfig.OUTPUT_DIRECTORY_PATH
    / CalculateConversionRatesConfig.OUTPUT_FILENAME
)
with open(OUTPUT_FILE_PATH, "w") as file:
    csv = df.to_csv()
    file.write(csv)

    logging.info(f"wrote {len(csv)} characters to {OUTPUT_FILE_PATH}")
