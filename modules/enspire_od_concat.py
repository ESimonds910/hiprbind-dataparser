import pandas as pd


class DataConcat:

    def __init__(self):

        self.concat_data = pd.DataFrame()

    def data_concat(self, enspire_df, od_df):
        self.concat_data = od_df.join(enspire_df, how="right", lsuffix="_od", rsuffix="_enspire")
        print(self.concat_data)
        # pd.DataFrame.to_csv(self.concat_data, "merged_data.csv")
        return self.concat_data
