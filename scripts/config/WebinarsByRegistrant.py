class WebinarsByRegistrantConfig:
    # labels of the columns to keep (all other columns will be deleted) for the data loaded from the `.json` files, i.e. the registrants by webinar
    RELEVANT_COLUMNS_BEFORE_GROUPING = [
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "webinar_id",
        "attended_live"
    ]

    # labels of the columns to remove after every row with the same email has been combined, i.e. the data in webinars by registrant form
    COLUMNS_TO_DROP_AFTER_GROUPING = [
        "webinar_id",
        "attended_live"
    ]

    # labels of the columns to rearrange in front of the columns representing webinars
    COLUMNS_THAT_COME_FIRST = [
        "first_name",
        "last_name",
        "phone_number"
    ]
