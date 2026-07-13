from config.GlobalConfig import GlobalConfig

from functions.get_aggregated_revenue import get_aggregated_revenue

df = get_aggregated_revenue()

GlobalConfig.pretty_print_df(df)
