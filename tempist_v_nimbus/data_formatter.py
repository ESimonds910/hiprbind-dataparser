import pandas as pd


def data_format(source):

    # Picking bloc
    cols = ["Plate"] + [f"Alpha_{x}" for x in range(1,5)] + [f"DNA_{x}" for x in range(1,5)]
    print(cols)
    df_bloc = pd.DataFrame()

    x = pd.DataFrame([list(source.iloc[0][[1, 2]]) + list(source.iloc[1][[1, 2]]),
                      list(source.iloc[0][[25, 26]]) + list(source.iloc[1][[25, 26]])],
                     index=["Alpha", "DNA"]).transpose()
    df_bloc = pd.concat([df_bloc, x])
    print(df_bloc)

