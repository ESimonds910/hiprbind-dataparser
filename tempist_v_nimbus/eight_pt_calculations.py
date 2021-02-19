import pandas as pd
import numpy as np


def make_calculations(df):

    alpha_slopes = [[(df.iloc[row + x]["Alpha"] - df.iloc[row + x -1]["Alpha"]) /
               (df.iloc[row + x]["Volumes"] - df.iloc[row + x - 1]["Volumes"])
              for row in range(7)] for x in range(1, df.shape[0], 8)]

    dna_slopes = [[(df.iloc[row + x]["DNA"] - df.iloc[row + x -1]["DNA"]) /
               (df.iloc[row + x]["Volumes"] - df.iloc[row + x - 1]["Volumes"])
              for row in range(7)] for x in range(1, df.shape[0], 8)]

    slope_df = pd.DataFrame(alpha_slopes, columns=[f"Alpha_Slope_{x}" for x in range(1, 8)])
    slope_df = pd.concat([slope_df, pd.DataFrame(dna_slopes, columns=[f"DNA_Slope_{x}" for x in range(1, 8)])], axis=1)

    slope_df["Alpha_Max"] = slope_df.iloc[:, 0:7].max(axis=1)
    slope_df["DNA_Max"] = slope_df.iloc[:, 7:14].max(axis=1)
    slope_df["Alpha_Max/DNA_Max"] = slope_df["Alpha_Max"] / slope_df["DNA_Max"]

    return slope_df
