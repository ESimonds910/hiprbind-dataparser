import pandas as pd
import numpy as np

def find_max(row, clean_df):

    max_found = False
    max_slope = 0
    original_max = 0
    max_cols = [f"alpha_slope_{n}" for n in range(1, 8)]
    alpha_cols = [f"Alpha_{n}" for n in range(1, 9)]
    search_cols = alpha_cols + max_cols
    selected_row = clean_df[clean_df["Alpha_avg_raw"] == row].loc[:, search_cols]
    # new_avg = selected_row.loc[:, ["Alpha_5", "Alpha_6", "Alpha_7", "Alpha_8"]].std(axis=1).item()
    # row_minus_std = row - std
    while not max_found:

        # print(max_cols)
        max_slope = float(selected_row.loc[:, max_cols].max(axis=1))

        # print(f"max_slope: {max_slope}")
        col_idx = selected_row.loc[:, max_cols].idxmax(axis=1).item()
        # print(f"col_idx 1: {col_idx}")
        try:
            col_num = int(col_idx.split("_")[2])
        except IndexError:
            print(f"col_idx 2: {col_idx}")
        alpha_raw_max = int(selected_row[f"Alpha_{col_num}"])
        # print(f"alpha_raw_max: {alpha_raw_max} vs alpha_mean: {row}")
        if alpha_raw_max < row:
            max_cols.remove(col_idx)
            if max_slope > original_max:
                original_max = max_slope
            if max_cols == []:
                return original_max
        else:
            max_found = True
            return max_slope




def make_calculations(main_df, dilution_volumes):
    clean_df = main_df
    main_df["Od600"] = main_df["Od600"].apply(lambda x: round(float(x), 2) if x != "" else "0.0")
    # main_df[["Alpha_1", "Alpha_2", "Alpha_3", "Alpha_4", "Alpha_5", "Alpha_6", "Alpha_7", "Alpha_8"]] = main_df[
    #     ["Alpha_1", "Alpha_2", "Alpha_3", "Alpha_4", "Alpha_5", "Alpha_6", "Alpha_7", "Alpha_8"]
    # ].astype(float)

    clean_df["Alpha_avg_raw"] = clean_df.loc[:, "Alpha_1":"Alpha_8"].mean(axis=1)

    for n in range(1, 8):
        clean_df[f"alpha_slope_{n}"] = round((clean_df[f"Alpha_{n + 1}"] - clean_df[f"Alpha_{n}"]) /
                                                  (dilution_volumes[n] - dilution_volumes[n - 1]), 2)

    # clean_df["Value"] = clean_df["Alpha_avg_raw"].apply(find_max, args=(clean_df, ))
    # clean_df["4pt_selection"] = clean_df.loc[:, "alpha_slope_1":"alpha_slope_4"].max(axis=1)
    clean_df["Alpha.Max.Slope"] = clean_df.loc[:, "alpha_slope_1":"alpha_slope_4"].max(axis=1)

    for n in range(1, 8):
        clean_df[f"dna_slope_{n}"] = round((clean_df[f"DNA_{n + 1}"] - clean_df[f"DNA_{n}"]) /
                                                (dilution_volumes[n] - dilution_volumes[n - 1]), 2)

    clean_df["DNA.Max.Slope"] = clean_df.loc[:, "dna_slope_1":"dna_slope_4"].max(axis=1)

    clean_df["HPB_DNA"] = round(clean_df["Alpha.Max.Slope"] / clean_df["DNA.Max.Slope"], 2)

    clean_df["HPB_OD"] = round(clean_df["Alpha.Max.Slope"] / clean_df["Od600"], 2)

    return clean_df


if __name__ == "__main__":
    test_df = pd.read_csv("test_df_precalc.csv")
    volumes = [0.21428571, 0.03061224, 0.00437318, 0.00062474, 0.00008925, 0.00001275, 0.00000182, 0.00000026]
    output_df = make_calculations(test_df, volumes)
    print(output_df.iloc[0])
    output_df.to_csv("Test_output.csv")
