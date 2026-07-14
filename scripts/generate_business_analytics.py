import logging

from config.GlobalConfig import GlobalConfig
from config.AggregateRevenueConfig import AggregateRevenueConfig
from config.WebinarsByRegistrantConfig import WebinarsByRegistrantConfig

from functions.get_aggregated_revenue import get_aggregated_revenue
from functions.webinar_mapping_utils\
    import learnabee_webinar_name_exists,\
    get_paid_webinar_ids_from_learnabee_name,\
    get_free_webinar_ids_from_learnabee_name

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


df = get_aggregated_revenue()

mask = df.index.map(learnabee_webinar_name_exists)

df = df[mask]

GlobalConfig.pretty_print_df(df)

def add_webinarjam_webinar_names(row):
    learnabee_course_name = row.name

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

    return row

df = df.apply(add_webinarjam_webinar_names, axis = "columns")

# GlobalConfig.pretty_print_df(df)
