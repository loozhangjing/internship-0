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
