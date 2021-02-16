import pandas as pd


class Calculator:

    def __init__(self, main_df, dilution_volumes, output_path):
        self.clean_df = main_df
        self.output_file_path = output_path
        # dilution_volumes = [0.357, 0.056, 0.006, 0.0004]
        self.dilution_volumes = [float(x) for x in dilution_volumes.split(",")]
        main_df["Od600"] = main_df["Od600"].apply(lambda x: round(float(x), 2) if x != "" else "0.0")
        main_df[["Alpha_1", "Alpha_2", "Alpha_3", "Alpha_4"]] = main_df[
            ["Alpha_1", "Alpha_2", "Alpha_3", "Alpha_4"]
        ].astype(float)
        self.make_calculations()

    def make_calculations(self):

        for n in range(1, 4):
            self.clean_df[f"alpha_slope_{n}"] = round((self.clean_df[f"Alpha_{n + 1}"] - self.clean_df[f"Alpha_{n}"]) /
                                                      (self.dilution_volumes[n] - self.dilution_volumes[n - 1]), 2)
        self.clean_df["max_alpha_slope"] = self.clean_df[
            ["alpha_slope_1", "alpha_slope_2", "alpha_slope_3"]
        ].max(axis=1)

        for n in range(1, 4):
            self.clean_df[f"dna_slope_{n}"] = round((self.clean_df[f"DNA_{n + 1}"] - self.clean_df[f"DNA_{n}"]) /
                                                    (self.dilution_volumes[n] - self.dilution_volumes[n - 1]), 2)
        self.clean_df["max_dna_slope"] = self.clean_df[
            ["dna_slope_1", "dna_slope_2", "dna_slope_3"]
        ].max(axis=1)

        self.clean_df["max_alpha_slope/max_dna_slope"] = round(self.clean_df["max_alpha_slope"] /
                                                               self.clean_df["max_dna_slope"], 2)

        self.clean_df["max_alpha_slope/OD"] = round(self.clean_df["max_alpha_slope"] / self.clean_df["Od600"], 2)

        self.file_cleanup()

    def file_cleanup(self):
        col_list = set(list(self.clean_df.columns))
        drop_cols = ["Source", "Ssf Exp", "Induction Plate", "Induction Well", "Seed Plate", "Seed Well",
                     "Harvest Plate", "Harvest Well", "Well ID"]
        print(col_list)
        for col in drop_cols:
            if col in col_list:
                self.clean_df.drop(columns=col, inplace=True)
        print(self.output_file_path)
        pd.DataFrame.to_excel(self.clean_df, self.output_file_path)

        return self.clean_df
