import pathlib

import pandas as pd

class GlobalConfig:
    OUTPUT_DIRECTORY_PATH = pathlib.Path("data/")

    @staticmethod
    def pretty_print_df(df: pd.DataFrame):
        """if using this function, pipe the output of the script to less -S"""
        with pd.option_context(
            {
                "display.max_colwidth": None,
                "display.max_rows": None,
                "display.max_columns": None,
                "display.width": None,
            }
        ):
            print(df)
