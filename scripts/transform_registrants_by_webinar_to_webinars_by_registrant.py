import pandas as pd

from registrants_by_webinar_ids import registrants_by_webinar_ids

registrants_for_selected_webinars = registrants_by_webinar_ids([1228, 1229])

df = pd.DataFrame(registrants_for_selected_webinars)

# pretty-print the `DataFrame` (pipe the output to less -S for scrolling)
with pd.option_context({ "display.max_rows": None, "display.max_columns": None, "display.width": None }):
    print(df)
