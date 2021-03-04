import pandas as pd


class DataFormatter:

    def __init__(self):
        self.all_data_signals = pd.DataFrame()
        self.display_ready_df = pd.DataFrame()
        self.well_ids = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12',
                         'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11', 'B12',
                         'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12',
                         'D01', 'D02', 'D03', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09', 'D10', 'D11', 'D12',
                         'E01', 'E02', 'E03', 'E04', 'E05', 'E06', 'E07', 'E08', 'E09', 'E10', 'E11', 'E12',
                         'F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F07', 'F08', 'F09', 'F10', 'F11', 'F12',
                         'G01', 'G02', 'G03', 'G04', 'G05', 'G06', 'G07', 'G08', 'G09', 'G10', 'G11', 'G12',
                         'H01', 'H02', 'H03', 'H04', 'H05', 'H06', 'H07', 'H08', 'H09', 'H10', 'H11', 'H12',
                         ]

    # TODO edit replicate data to same table
    def formatter(self, all_enspire_data, all_rep_data, plate_ids, dilutions, proj_name, std_row, std_conc):
        for plate in plate_ids:
            if len(plate) == 2 or plate.split("-")[1] == "1":
                wl = 0
                end_row = 16
                for row in range(0, end_row, 2):
                    end_col = int(all_enspire_data.shape[1] / 2)
                    for col in range(1, end_col, 2):
                        dna_col_id = col + 24
                        bloc_df = pd.DataFrame([[plate[:2]] + [self.well_ids[wl]] +
                                                list(all_enspire_data.iloc[row][[col, col + 1]])
                                                + list(all_enspire_data.iloc[row + 1][[col, col + 1]]) +
                                                list(all_enspire_data.iloc[row][[dna_col_id, dna_col_id + 1]])
                                                + list(all_enspire_data.iloc[row + 1][[dna_col_id, dna_col_id + 1]])],
                                               columns="plate Well_Id Alpha_1 Alpha_2 Alpha_3 Alpha_4 DNA_1 DNA_2 DNA_3 DNA_4".split())

                        display_bloc = pd.DataFrame([[self.well_ids[wl] for n in range(4)],
                                                     dilutions.split(","),
                                                     list(bloc_df.iloc[0, 2:6]),
                                                     list(bloc_df.iloc[0, 6:])],
                                                    index="Well_Id Volumes Alpha DNA".split()).transpose()
                        display_bloc.insert(0, "plate", plate[:2])
                        display_bloc.insert(0, "Plate_Well_Id", display_bloc["plate"] + "-" + display_bloc["Well_Id"])
                        display_bloc.insert(0, "Unique_Id", proj_name + "-" + display_bloc["Plate_Well_Id"])
                        display_bloc.insert(3, "row", display_bloc["Well_Id"].apply(lambda x: x[:1]))
                        display_bloc.insert(4, "col", display_bloc["Well_Id"].apply(lambda x: x[1:]))

                        if std_row != "":
                            display_bloc.insert(5, "std_conc", display_bloc["Well_Id"].apply(lambda x: std_conc[int(x[1:]) - 1] if x[:1] == std_row else ""))

                        display_bloc[["Volumes", "col"]] = display_bloc[["Volumes", "col"]].apply(pd.to_numeric)
                        bloc_df.insert(0, "Plate_Well_Id", bloc_df["plate"] + "-" + bloc_df["Well_Id"])
                        bloc_df.insert(0, "Unique_Id", proj_name + "-" + bloc_df["Plate_Well_Id"])
                        wl += 1
                        self.all_data_signals = pd.concat([self.all_data_signals, bloc_df])
                        self.display_ready_df = pd.concat([self.display_ready_df, display_bloc])

        self.all_data_signals.set_index("Unique_Id", inplace=True)
            # if data_signals_list:
            #     data_signals_df = pd.DataFrame(
            #         data_signals_list,
            #         index=[x + 1 for x in range(len(data_signals_list))],
            #         columns="Alpha_1 Alpha_2 Alpha_3 Alpha_4 DNA_1 DNA_2 DNA_3 DNA_4".split()
            #     )
            #
            #     pd.DataFrame.to_csv(display_bloc, "Display_Ready.csv")
            #     data_signals_df.insert(0, "Well ID", self.well_ids, True)
            #     data_signals_df.insert(1, "Source", plate[:2], True)
            #     data_signals_df.insert(2, "Plate", plate, True)
            #     data_signals_df.insert(0, "ID", data_signals_df["Source"] + "-" + data_signals_df["Well ID"], True)
            #     data_signals_df.set_index("ID", inplace=True)
            #     self.all_data_signals = pd.concat([self.all_data_signals, data_signals_df])
            #     # pd.DataFrame.to_csv(self.all_data_signals, "all_data_df.csv")
            # else:
            #     rep_data_signals_df = pd.DataFrame(
            #         rep_data_signals_list,
            #         index=[x + 1 for x in range(len(rep_data_signals_list))],
            #         columns="Alpha_1 Alpha_2 Alpha_3 Alpha_4 DNA_1 DNA_2 DNA_3 DNA_4".split()
            #     )
            #
            #     rep_data_signals_df.insert(0, "Well ID", self.well_ids, True)
            #     rep_data_signals_df.insert(1, "Source", plate[:2], True)
            #     rep_data_signals_df.insert(2, "Plate", plate, True)
            #     rep_data_signals_df.insert(0, "ID", rep_data_signals_df["Source"] +
            #                                "-" + rep_data_signals_df["Well ID"], True)

                # TODO Need to create rep dataframes

        # pd.DataFrame.to_csv(self.all_data_signals, "data_output.csv")
        # return self.all_data_signals, self.all_rep_data_signals
        return self.all_data_signals, self.display_ready_df
