import logging

from config.GlobalConfig import GlobalConfig
from config.AggregateRevenueConfig import AggregateRevenueConfig
from config.WebinarsByRegistrantConfig import WebinarsByRegistrantConfig

from functions.get_aggregated_revenue import get_aggregated_revenue
from functions.webinar_mapping_utils\
    import get_paid_webinar_ids_from_learnabee_name,\
    get_free_webinar_ids_from_learnabee_name

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


df = get_aggregated_revenue()

def add_webinarjam_webinar_names(row):
    learnabee_course_name = row.name

    try:
        webinarjam_free_webinar_names = [
            WebinarsByRegistrantConfig.webinar_ids_to_names[str(id)]
                for id in get_free_webinar_ids_from_learnabee_name(
                    learnabee_course_name
                )
        ]
        webinarjam_paid_webinar_names = [
            WebinarsByRegistrantConfig.webinar_ids_to_names[str(id)]
                for id in get_paid_webinar_ids_from_learnabee_name(
                    learnabee_course_name
                )
        ]

        print(webinarjam_free_webinar_names, webinarjam_paid_webinar_names)

    except StopIteration:
        logger.debug(
            "no WebinarJam IDs found for "
            f"'{learnabee_course_name}'"
        )
        return row

    return row

df = df.apply(add_webinarjam_webinar_names, axis = "columns")

GlobalConfig.pretty_print_df(df)
