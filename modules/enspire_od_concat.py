import pandas as pd


class DataConcat:

    def __init__(self):

        self.concat_data = pd.DataFrame()
        self.concat_display = pd.DataFrame()

    def data_concat(self, enspire_df, od_df, standard_row, ab_name):
        self.concat_data = od_df.join(enspire_df, how="right", lsuffix="_od", rsuffix="_enspire")
        self.concat_data.loc[
            (self.concat_data["Well_Id"].apply(lambda x: x[:1]) == standard_row), "Sample_type"
        ] = "Standard"
        if ab_name != "":
            self.concat_data.insert(loc=1, column="HPB_scheme", value=ab_name)
        # pd.DataFrame.to_csv(self.concat_data, "merged_data.csv")
        return self.concat_data

    def display_data_concat(self, display_data, od_df, standard_row, ab_name):
        try:
            od_cols = od_df[["Sample_type", "Harvest_sample_id", "Strain_id", "Induction_temp"]]
            od_cols.set_index("Harvest_sample_id", inplace=True)
        except KeyError:
            print("Unexpected error with od file column header name.")
            pass
        else:
            display_data.set_index("Unique_Id", inplace=True)
            self.concat_display = od_cols.join(display_data, how="right")
            self.concat_display.loc[
                (self.concat_display["Well_Id"].apply(lambda x: x[:1]) == standard_row), "Sample_type"
            ] = "Standard"
            if ab_name != "":
                self.concat_display.insert(loc=1, column="HPB_scheme", value=ab_name)
            return self.concat_display


