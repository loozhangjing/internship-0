class WebinarListConfig:
    API_ENDPOINT = "https://api.webinarjam.com/webinarjam/webinars"
    OUTPUT_FILENAME = "webinar_list.json"
    # format of the string dates in the `schedule` property of the webinar list
    STRPTIME_FORMAT = "%A, %d %b %Y, %I:%M %p"

    # dict keys are the IDs of the free webinar(s)
    # dict values are the IDs of the corresponding paid webinar(s)
    FREE_TO_PAID_WEBINAR_IDS = {
        (1218, ): (1228, 1229),
        (1202, 1205): (1203, ),
        (1178, ): (1193, 1194, 1200),
        (1201, ): (1204, ),
        (1206, 1226): (1227, ),
        (1176, ): (1177, )
    }
    # (dangling commas ensure Python interprets brackets with only one number
    # within them as a tuple)

    # flatten the dictionary view objects
    # (returned by `.keys() and `.values()`)
    # containing tuples into a flat tuple
    _FREE_WEBINAR_IDS = sum(FREE_TO_PAID_WEBINAR_IDS.keys(), ())
    _PAID_WEBINAR_IDS = sum(FREE_TO_PAID_WEBINAR_IDS.values(), ())

    @staticmethod
    def is_free_webinar_id(id):
        return(id in WebinarListConfig._FREE_WEBINAR_IDS)

    @staticmethod
    def is_paid_webinar_id(id):
        return(id in WebinarListConfig._PAID_WEBINAR_IDS)
