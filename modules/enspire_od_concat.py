import pandas as pd


class DataConcat:

    def __init__(self):

        self.concat_data = pd.DataFrame()

    def data_concat(self, enspire_df, od_df):

        self.concat_data = pd.concat([od_df, enspire_df], axis=1)
        # self.concat_data = pd.merge(od_df, enspire_df, on="ID")
        print(self.concat_data)
        # pd.DataFrame.to_csv(self.concat_data, "merged_data.csv")
        return self.concat_data
