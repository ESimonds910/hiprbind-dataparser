import pandas as pd
import numpy as np


def data_format(source, proj_name, plates, volumes, std_row, std_conc, std_pos):

    # Picking bloc
    # 4 pt dataframe
    # clean_df = pd.DataFrame()
    # main_formatted_df = pd.DataFrame()
    #
    # end_row = int(source.shape[0] - 1)
    # for row in range(0, end_row, 2):
    #     end_col = int(source.shape[1] / 2)
    #     for col in range(1, end_col, 2):
    #         dna_col_id = col + 24
    #         bloc_df = pd.DataFrame([list(source.iloc[row][[col, col + 1]])
    #                         + list(source.iloc[row + 1][[col, col + 1]]),
    #                         list(source.iloc[row][[dna_col_id, dna_col_id + 1]])
    #                         + list(source.iloc[row + 1][[dna_col_id, dna_col_id + 1]])],
    #                         index=["Alpha", "DNA"]).transpose()
    #         bloc_df.insert(0, "Plate", source.iloc[row]["Plate"])
    #         clean_df = pd.concat([clean_df, bloc_df])
    # clean_df.to_csv("Output.csv")
    # 8pt dataframe
    well_id = [f"A{str(y).zfill(2)}" for y in range(1, 13)] \
              + [f"B{str(y).zfill(2)}" for y in range(1, 13)] \
              + [f"C{str(y).zfill(2)}" for y in range(1, 13)] \
              + [f"D{str(y).zfill(2)}" for y in range(1, 13)]
    # well_id = [f"A{y}" for y in range(1, 13)] \
    #           + [f"B{y}" for y in range(1, 13)] \
    #           + [f"C{y}" for y in range(1, 13)] \
    #           + [f"D{y}" for y in range(1, 13)]

    clean_df = pd.DataFrame()
    main_formatted_df = pd.DataFrame()
    start_row = 0
    end_row = 8
    for plate in plates:
        print(plate)
        well_index = 0
        for row in range(start_row, end_row, 2):
            end_col = int(source.shape[1] / 2)
            for col in range(1, end_col, 2):
                dna_col_id = col + 24

                main_df = pd.DataFrame([[plate] + [well_id[well_index]] +
                                        list(source.iloc[row][[col, col + 1]])
                                        + list(source.iloc[row + 1][[col, col + 1]])
                                        + list(source.iloc[row + 8][[col, col + 1]])
                                       + list(source.iloc[row + 9][[col, col + 1]]) +
                                        list(source.iloc[row][[dna_col_id, dna_col_id + 1]])
                                        + list(source.iloc[row + 1][[dna_col_id, dna_col_id + 1]])
                                        + list(source.iloc[row + 8][[dna_col_id, dna_col_id + 1]])
                                        + list(source.iloc[row + 9][[dna_col_id, dna_col_id + 1]])
                                        ],
                                       columns="Plate Well_Id Alpha_1 Alpha_2 Alpha_3 Alpha_4 "
                                               "Alpha_5 Alpha_6 Alpha_7 Alpha_8 "
                                               "DNA_1 DNA_2 DNA_3 DNA_4 "
                                               "DNA_5 DNA_6 DNA_7 DNA_8".split())

                bloc_df = pd.DataFrame([list(source.iloc[row][[col, col + 1]])
                                        + list(source.iloc[row + 1][[col, col + 1]])
                                       + list(source.iloc[row + 8][[col, col + 1]])
                                       + list(source.iloc[row + 9][[col, col + 1]]),
                                        list(source.iloc[row][[dna_col_id, dna_col_id + 1]])
                                       + list(source.iloc[row + 1][[dna_col_id, dna_col_id + 1]])
                                       + list(source.iloc[row + 8][[dna_col_id, dna_col_id + 1]])
                                       + list(source.iloc[row + 9][[dna_col_id, dna_col_id + 1]])],
                                       index=["Alpha", "DNA"]).transpose()
                bloc_df.insert(0, "Plate", plate)
                # if plate + 1 < 4:
                #     bloc_df.insert(1, "Method", "Nimbus")
                # else:
                #     bloc_df.insert(1, "Method", "Tempist")
                # if int((row - 16 * plate) / 2) == 3:
                #     bloc_df.insert(2, "Sample", "Standard")
                # else:
                #     bloc_df.insert(2, "Sample", "Experimental")
                bloc_df.insert(1, "Well_Id", well_id[well_index])
                if std_row != "" and std_pos == "half":
                    bloc_df.insert(
                        2,
                        "std_conc",
                        bloc_df["Well_Id"].apply(
                            lambda x: std_conc[int(x[1:]) - 1] if x[:1] == std_row and int(x[1:]) > 6 else ""
                        )
                    )
                elif std_row != "":
                    bloc_df.insert(
                        2,
                        "std_conc",
                        bloc_df["Well_Id"].apply(
                            lambda x: std_conc[int(x[1:]) - 1] if x[:1] == std_row else ""
                        )
                    )
                bloc_df.insert(3, "Volumes", volumes)
                bloc_df.insert(2, "Row", bloc_df["Well_Id"].apply(lambda x: x[:1]))
                bloc_df.insert(3, "Col", bloc_df["Well_Id"].apply(lambda x: x[1:]))
                bloc_df.insert(0, "Id", plate[:2] + "-" + bloc_df["Well_Id"])
                bloc_df.insert(0, "Unique_Id", proj_name + "-" + bloc_df["Id"])
                main_df.insert(0, "Unique_Id", proj_name + "-" + plate[:2] + "-" + main_df["Well_Id"])
                main_formatted_df = pd.concat([main_formatted_df, main_df])
                clean_df = pd.concat([clean_df, bloc_df])
                well_index += 1
        start_row += 16
        end_row += 16

    clean_df["Replicate"] = np.where(
        clean_df["Plate"].apply(lambda x: x[2:]) == "-2",
        "replicate", ""
    )
    main_formatted_df["Replicate"] = np.where(
        main_formatted_df["Plate"].apply(lambda x: x[2:]) == "-2",
        "replicate", ""
    )

    clean_rep_df = clean_df[clean_df["Replicate"] == "replicate"]
    clean_df = clean_df[clean_df["Replicate"] == ""]
    print(clean_df)
    main_formatted_rep_df = main_formatted_df[main_formatted_df["Replicate"] == "replicate"]
    main_formatted_df = main_formatted_df[main_formatted_df["Replicate"] == ""]
    #     print(f"shape: {clean_df.shape}")
    #     print(clean_df.tail())
    clean_df.to_csv("Output8pt.csv")


    return clean_df, main_formatted_df, clean_rep_df, main_formatted_rep_df
