import pandas as pd
import numpy as np


def make_calculations(main_df, dilution_volumes):
#     unique_id = df["Id"] + "_" + df["Sample"]
#     unique_id_list = list(unique_id.unique())
#     sample_id = [x.split("_")[0] for x in unique_id_list]
#     sample_type = [x.split("_")[1] for x in unique_id_list]
#     alpha_slopes = [[(df.iloc[row + x]["Alpha"] - df.iloc[row + x - 1]["Alpha"]) /
#                (df.iloc[row + x]["Volumes"] - df.iloc[row + x - 1]["Volumes"])
#               for row in range(7)] for x in range(1, df.shape[0], 8)]
#
#     dna_slopes = [[(df.iloc[row + x]["DNA"] - df.iloc[row + x - 1]["DNA"]) /
#                (df.iloc[row + x]["Volumes"] - df.iloc[row + x - 1]["Volumes"])
#               for row in range(7)] for x in range(1, df.shape[0], 8)]
#
#     slope_df = pd.DataFrame(alpha_slopes, columns=[f"Alpha_Slope_{x}" for x in range(1, 8)])
#     slope_df = pd.concat([slope_df, pd.DataFrame(dna_slopes, columns=[f"DNA_Slope_{x}" for x in range(1, 8)])], axis=1)
#
#     slope_df["Alpha_Max"] = slope_df.iloc[:, 0:7].max(axis=1)
#     slope_df["DNA_Max"] = slope_df.iloc[:, 7:14].max(axis=1)
#     slope_df["Alpha_Max/DNA_Max"] = slope_df["Alpha_Max"] / slope_df["DNA_Max"]
#     slope_df.insert(0, "Id", unique_id_list)
#     slope_df.insert(1, "Sample", sample_id)
#     slope_df.insert(2, "Sample_Type", sample_type)
#
#     return slope_df


    clean_df = main_df
    # dilution_volumes = [0.357, 0.056, 0.006, 0.0004]
    # dilution_volumes = [float(x) for x in dilution_volumes.split(",")]
    main_df["Raw_od"] = main_df["Raw_od"].apply(lambda x: round(float(x), 2) if x != "" else "0.0")
    # main_df[["Alpha_1", "Alpha_2", "Alpha_3", "Alpha_4", "Alpha_5", "Alpha_6", "Alpha_7", "Alpha_8"]] = main_df[
    #     ["Alpha_1", "Alpha_2", "Alpha_3", "Alpha_4", "Alpha_5", "Alpha_6", "Alpha_7", "Alpha_8"]
    # ].astype(float)
    for n in range(1, 8):
        clean_df[f"alpha_slope_{n}"] = round((clean_df[f"Alpha_{n + 1}"] - clean_df[f"Alpha_{n}"]) /
                                                  (dilution_volumes[n] - dilution_volumes[n - 1]), 2)
    clean_df["Alpha.Max.Slope"] = clean_df[
        ["alpha_slope_1", "alpha_slope_2", "alpha_slope_3", "alpha_slope_4", "alpha_slope_5", "alpha_slope_6", "alpha_slope_7"]
    ].max(axis=1)

    for n in range(1, 8):
        clean_df[f"dna_slope_{n}"] = round((clean_df[f"DNA_{n + 1}"] - clean_df[f"DNA_{n}"]) /
                                                (dilution_volumes[n] - dilution_volumes[n - 1]), 2)
    clean_df["DNA.Max.Slope"] = clean_df[
        ["dna_slope_1", "dna_slope_2", "dna_slope_3", "dna_slope_4", "dna_slope_5", "dna_slope_6", "dna_slope_7"]
    ].max(axis=1)

    clean_df["HPB_DNA"] = round(clean_df["Alpha.Max.Slope"] /
                                     clean_df["DNA.Max.Slope"], 2)

    clean_df["HPB_OD"] = round(clean_df["Alpha.Max.Slope"] / clean_df["Raw_od"], 2)


    return clean_df