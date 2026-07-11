from config.env import WEBINAR_MAPPINGS

"""
`WEBINAR_MAPPINGS` is a list of tuples of three elements, where each element
in a specific position in the tuple represents a specific value:

```
WEBINAR_MAPPINGS = [
    (
        "name of this webinar in the Learnabee system",
        (1218, ), # IDs of the free webinars in the WebinarJam API
        (1228, 1229) # IDs of the paid webinars in the WebinarJam API
    ),
    # and so on...
]
```
"""

def get_free_to_paid_webinar_id_mappings():
    return {
        tup[1]: tup[2]
            for tup in WEBINAR_MAPPINGS
    }

def get_free_webinar_ids_from_learnabee_name(learnabee_webinar_name):
    return next(
        list(tup[1])
            for tup in WEBINAR_MAPPINGS
            if tup[0] in learnabee_webinar_name
    )

def get_paid_webinar_ids_from_learnabee_name(learnabee_webinar_name):
    return next(
        list(tup[2])
            for tup in WEBINAR_MAPPINGS
            if tup[0] in learnabee_webinar_name
    )

