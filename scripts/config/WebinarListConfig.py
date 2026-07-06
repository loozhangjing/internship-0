class WebinarListConfig:
    API_ENDPOINT = "https://api.webinarjam.com/webinarjam/webinars"
    OUTPUT_FILENAME = "webinar_list.json"
    # format of the string dates in `schedule` property of the webinar list
    STRPTIME_FORMAT = "%A, %d %b %Y, %I:%M %p"
