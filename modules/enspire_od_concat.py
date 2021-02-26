import pandas as pd


class DataConcat:

    def __init__(self):

        self.concat_data = pd.DataFrame()
        self.concat_display = pd.DataFrame()

    def data_concat(self, enspire_df, od_df):
        self.concat_data = od_df.join(enspire_df, how="right", lsuffix="_od", rsuffix="_enspire")
        print(self.concat_data)
        # pd.DataFrame.to_csv(self.concat_data, "merged_data.csv")
        return self.concat_data

    def display_data_concat(self, display_data, od_df):
        od_cols = od_df[["Sample Type", "Harvest Sample Id", "Strain"]]
        od_cols.set_index("Harvest Sample Id", inplace=True)
        display_data.set_index("Unique_Id", inplace=True)
        self.concat_display = od_cols.join(display_data, how="right")
        return self.concat_display


