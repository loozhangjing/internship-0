import logging

import pandas as pd

from config.GlobalConfig import GlobalConfig
from config.AggregateRevenueConfig import AggregateRevenueConfig

logging.basicConfig(level=logging.INFO)

COLUMN_NAMES = AggregateRevenueConfig.CSV_COLUMN_NAMES
INPUT_PATH = (
    GlobalConfig.OUTPUT_DIRECTORY_PATH
    / AggregateRevenueConfig.CSV_INPUT_FILENAME
)

logging.info(f"attempting to load CSV data from {INPUT_PATH}...")

df = pd.read_csv(INPUT_PATH)

logging.info(
    f"loaded {df.shape[0]} registrations "
    f"across {len(df[COLUMN_NAMES.REVENUE].unique())} unique webinars"
)

# a `Series` of booleans each corresponding to whether
# a row's revenue value is parseable as an `int` (i.e. only numeric digits)
rows_with_integer_revenues = df[COLUMN_NAMES.REVENUE].str.contains(
    AggregateRevenueConfig.ONLY_DIGITS_REGULAR_EXPRESSION
)


rows_without_integer_revenues = ~rows_with_integer_revenues
dropped_rows = df.loc[
    rows_without_integer_revenues,
    [COLUMN_NAMES.EMAIL, COLUMN_NAMES.REVENUE, COLUMN_NAMES.WEBINAR_NAME],
]

logging.info(
    "\n"
    f"removed {dropped_rows.shape[0]} registrations because "
    f"their values in '{COLUMN_NAMES.REVENUE}' cannot be parsed as integers:"
    "\n\n"
    f"{dropped_rows}"
    "\n"
)


# remove the rows with revenues that cannot be parsed as an `int`
# so that converting the `str` revenue values to `int` doesn't throw errors
df = df.loc[rows_with_integer_revenues]
df = df.apply(AggregateRevenueConfig.row_revenue_to_int, axis="columns")

df = (
    df.groupby(COLUMN_NAMES.WEBINAR_NAME)[COLUMN_NAMES.REVENUE]
        .aggregate(["sum", "size", "mean", "median", "min", "max", "std"])
        .rename(
            columns = {
                "sum": "Total revenue (RM)",
                "size": "Number of registratations",
                "mean": "Mean (average) revenue per registration (RM)",
                "median": "Median revenue per registration (RM)",
                "min": "Minimum amount paid (RM)",
                "max": "Maximum amount paid (RM)",
                "std": "Standard deviation of the amount paid (RM)",
            }
        )
)

OUTPUT_PATH = (
    GlobalConfig.OUTPUT_DIRECTORY_PATH / AggregateRevenueConfig.OUTPUT_FILENAME
)

with open(OUTPUT_PATH, "w") as file:
    csv = df.to_csv()

    file.write(csv)

    logging.info(f"wrote {len(csv)} characters to {OUTPUT_PATH}")


"""
with pd.option_context(
    {
        "display.max_rows": None,
        "display.max_columns": None,
        "display.width": None,
    }
):
    # pipe the output of this script to less -S for a pretty-printed
    # `DataFrame` without any rows containing non-integer revenue values
    print(df)
"""
