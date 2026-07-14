class CSVColumnNames:
    ATTENDED_PAID_CONVERSION_RATE = (
        "Conversion rate (%) "
        "[for registrants that registered & ATTENDED the free webinar]"
    )
    TOTAL_PAID_CONVERSION_RATE = (
        "Conversion rate (%) "
        "[for all registrants that registered for the free webinar]"
    )
    ATTENDED_FREE_REGISTRANT_COUNT = (
        "Number of unique free registrants "
        "[that registered & ATTENDED]"
    )
    TOTAL_FREE_REGISTRANT_COUNT = (
        "Total number of unique free registrants "
        "[that registered]"
    )
    PAID_REGISTRANT_COUNT = "Number of unique paid registrants"
    PAID_WEBINAR_NAMES = "Paid webinar name(s)"

class CalculateConversionRatesConfig:
    OUTPUT_FILENAME = "conversion_rates.csv"

    CSV_COLUMN_NAMES = CSVColumnNames
