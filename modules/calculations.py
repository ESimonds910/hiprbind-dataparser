import pandas as pd


class Calculator:

    def __init__(self):
        self.clean_df = pd.DataFrame()

    def make_calculations(self, main_df, dilution_volumes):
        self.clean_df = main_df
        # dilution_volumes = [0.357, 0.056, 0.006, 0.0004]
        dilution_volumes = [float(x) for x in dilution_volumes.split(" ")]
        main_df["Od600"] = main_df["Od600"].apply(lambda x: round(float(x), 2) if x != "" else "0.0")
        main_df[["Alpha_1", "Alpha_2", "Alpha_3", "Alpha_4"]] = main_df[
            ["Alpha_1", "Alpha_2", "Alpha_3", "Alpha_4"]
        ].astype(float)
        for n in range(1, 4):
            self.clean_df[f"alpha_slope_{n}"] = round((self.clean_df[f"Alpha_{n + 1}"] - self.clean_df[f"Alpha_{n}"]) /
                                                      (dilution_volumes[n] - dilution_volumes[n - 1]), 2)
        self.clean_df["Alpha.Max.Slope"] = self.clean_df[
            ["alpha_slope_1", "alpha_slope_2", "alpha_slope_3"]
        ].max(axis=1)

        for n in range(1, 4):
            self.clean_df[f"dna_slope_{n}"] = round((self.clean_df[f"DNA_{n + 1}"] - self.clean_df[f"DNA_{n}"]) /
                                                    (dilution_volumes[n] - dilution_volumes[n - 1]), 2)
        self.clean_df["DNA.Max.Slope"] = self.clean_df[
            ["dna_slope_1", "dna_slope_2", "dna_slope_3"]
        ].max(axis=1)

        self.clean_df["HPB_DNA"] = round(self.clean_df["Alpha.Max.Slope"] /
                                                               self.clean_df["DNA.Max.Slope"], 2)

        self.clean_df["HPB_OD"] = round(self.clean_df["Alpha.Max.Slope"] / self.clean_df["Od600"], 2)

        self.file_cleanup()
        return self.clean_df

    def file_cleanup(self):
        col_list = set(list(self.clean_df.columns))
        drop_cols = ["Source", "Ssf Exp", "Induction Plate", "Induction Well", "Seed Plate", "Seed Well",
                     "Harvest Plate", "Harvest Well", "Well ID"]
        for col in drop_cols:
            if col in col_list:
                self.clean_df.drop(columns=col, inplace=True)

        return self.clean_df
