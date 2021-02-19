import pandas as pd


def data_format(source, plates, volumes):

    # Picking bloc
    # 4 pt dataframe
    clean_df = pd.DataFrame()

    end_row = int(source.shape[0] - 1)
    for row in range(0, end_row, 2):
        end_col = int(source.shape[1] / 2)
        for col in range(1, end_col, 2):
            dna_col_id = col + 24
            bloc_df = pd.DataFrame([list(source.iloc[row][[col, col + 1]])
                            + list(source.iloc[row + 1][[col, col + 1]]),
                            list(source.iloc[row][[dna_col_id, dna_col_id + 1]])
                            + list(source.iloc[row + 1][[dna_col_id, dna_col_id + 1]])],
                            index=["Alpha", "DNA"]).transpose()
            bloc_df.insert(0, "Plate", source.iloc[row]["Plate"])
            clean_df = pd.concat([clean_df, bloc_df])
    print(f"shape: {clean_df.shape}")
    print(clean_df.tail())
    clean_df.to_csv("Output.csv")


    clean_df = pd.DataFrame()
    start_row = 0
    end_row = 8
    for plate in range(len(plates)):
        for row in range(start_row, end_row, 2):
            end_col = int(source.shape[1] / 2)
            for col in range(1, end_col, 2):
                dna_col_id = col + 24
                bloc_df = pd.DataFrame([list(source.iloc[row][[col, col + 1]])
                                        + list(source.iloc[row + 1][[col, col + 1]])
                                       + list(source.iloc[row + 8][[col, col + 1]])
                                       + list(source.iloc[row + 9][[col, col + 1]]),
                                        list(source.iloc[row][[dna_col_id, dna_col_id + 1]])
                                       + list(source.iloc[row + 1][[dna_col_id, dna_col_id + 1]])
                                       + list(source.iloc[row + 8][[dna_col_id, dna_col_id + 1]])
                                       + list(source.iloc[row + 9][[dna_col_id, dna_col_id + 1]])],
                                       index=["Alpha", "DNA"]).transpose()
                bloc_df.insert(0, "Plate", f"P{plate + 1}")
                bloc_df.insert(1, "Volumes", volumes)
                if plate + 1 < 4:
                    bloc_df.insert(2, "Method", "Nimbus")
                else:
                    bloc_df.insert(2, "Method", "Tempist")
                clean_df = pd.concat([clean_df, bloc_df])
        start_row += 16
        end_row += 16
        print(f"shape: {clean_df.shape}")
        print(clean_df.tail())
        clean_df.to_csv("Output8pt.csv")
        return clean_df
