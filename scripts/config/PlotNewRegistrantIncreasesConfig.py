class PlotNewRegistrantIncreasesConfig:
    WEBINAR_MUSTVE_BEEN_HELD_IN_THE_YEARS = [2026]
    WEBINAR_NAMES_MUST_INCLUDE_ONE_OF = ["free", "免费"]

    STRPTIME_FORMAT = "%a, %d %b %Y, %I:%M %p"
    STRFTIME_FORMAT = "%d/%m/%Y"
    OUTPUT_SUBDIRECTORY = "plots/"
