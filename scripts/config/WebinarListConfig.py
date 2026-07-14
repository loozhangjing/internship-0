from functions.webinar_mapping_utils import get_free_to_paid_webinar_id_mappings

class WebinarListConfig:
    API_ENDPOINT = "https://api.webinarjam.com/webinarjam/webinars"
    OUTPUT_FILENAME = "webinar_list.json"
    # format of the string dates in the `schedule` property of the webinar list
    STRPTIME_FORMAT = "%A, %d %b %Y, %I:%M %p"

    FREE_TO_PAID_WEBINAR_IDS = get_free_to_paid_webinar_id_mappings()

    # flatten the dictionary view objects
    # (returned by `.keys() and `.values()`)
    # containing tuples into a flat tuple
    _FREE_WEBINAR_IDS = sum(FREE_TO_PAID_WEBINAR_IDS.keys(), ())
    _PAID_WEBINAR_IDS = sum(FREE_TO_PAID_WEBINAR_IDS.values(), ())

    @staticmethod
    def get_free_webinar_ids():
        return WebinarListConfig._FREE_WEBINAR_IDS

    @staticmethod
    def get_paid_webinar_ids():
        return WebinarListConfig._PAID_WEBINAR_IDS

    @staticmethod
    def is_free_webinar_id(id):
        return(id in WebinarListConfig._FREE_WEBINAR_IDS)

    @staticmethod
    def is_paid_webinar_id(id):
        return(id in WebinarListConfig._PAID_WEBINAR_IDS)
