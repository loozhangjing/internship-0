class CSVColumnNames:
    EMAIL = "Email Address"
    WEBINAR_NAME = "Course Name"
    REVENUE = "Amount Paid (RM)"

class AggregateRevenueConfig:
    CSV_INPUT_FILENAME = "revenue_by_registration.csv"
    CSV_COLUMN_NAMES = CSVColumnNames

    ONLY_DIGITS_REGULAR_EXPRESSION = "^[0-9]*$"

    @staticmethod
    def row_revenue_to_int(row):
        revenue = row[AggregateRevenueConfig.CSV_COLUMN_NAMES.REVENUE]

        row[AggregateRevenueConfig.CSV_COLUMN_NAMES.REVENUE] = int(revenue)

        return row

