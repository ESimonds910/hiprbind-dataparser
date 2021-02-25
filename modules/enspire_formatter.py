import pandas as pd


class DataFormatter:

    def __init__(self):
        self.all_data_signals = pd.DataFrame()
        self.well_ids = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12',
                         'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11', 'B12',
                         'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10', 'C11', 'C12',
                         'D01', 'D02', 'D03', 'D04', 'D05', 'D06', 'D07', 'D08', 'D09', 'D10', 'D11', 'D12',
                         'E01', 'E02', 'E03', 'E04', 'E05', 'E06', 'E07', 'E08', 'E09', 'E10', 'E11', 'E12',
                         'F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F07', 'F08', 'F09', 'F10', 'F11', 'F12',
                         'G01', 'G02', 'G03', 'G04', 'G05', 'G06', 'G07', 'G08', 'G09', 'G10', 'G11', 'G12',
                         'H01', 'H02', 'H03', 'H04', 'H05', 'H06', 'H07', 'H08', 'H09', 'H10', 'H11', 'H12',
                         ]

    def formatter(self, all_enspire_data, all_rep_data, plate_ids):
        for plate in plate_ids:
            try:
                main_data_bloc = all_enspire_data[all_enspire_data["Plate"] == plate]
                rep_data_bloc = all_rep_data[all_rep_data["Plate"] == plate]
            except KeyError:
                main_data_bloc = all_enspire_data[all_enspire_data["Plate"] == plate]
            finally:
                data_signals_list = []
                rep_data_signals_list = []
                for r in range(0, 16, 2):
                    for c in range(1, 25, 2):
                        try:
                            sub_data_bloc = main_data_bloc.iloc[[r, r + 1]][[c, c + 1]]
                            sub_dna_data_bloc = main_data_bloc.iloc[[r, r + 1]][[c + 24, c + 25]]
                        except IndexError:
                            sub_data_bloc = rep_data_bloc.iloc[[r, r + 1]][[c, c + 1]]
                            sub_dna_data_bloc = rep_data_bloc.iloc[[r, r + 1]][[c + 24, c + 25]]

                            new_list = list(sub_data_bloc.iloc[0]) + \
                                       list(sub_data_bloc.iloc[1]) + \
                                       list(sub_dna_data_bloc.iloc[0]) + \
                                       list(sub_dna_data_bloc.iloc[1])
                            rep_data_signals_list.append(new_list)
                        else:
                            new_list = list(sub_data_bloc.iloc[0]) + \
                                       list(sub_data_bloc.iloc[1]) + \
                                       list(sub_dna_data_bloc.iloc[0]) + \
                                       list(sub_dna_data_bloc.iloc[1])
                            data_signals_list.append(new_list)

                if data_signals_list:
                    data_signals_df = pd.DataFrame(
                        data_signals_list,
                        index=[x + 1 for x in range(len(data_signals_list))],
                        columns="Alpha_1 Alpha_2 Alpha_3 Alpha_4 DNA_1 DNA_2 DNA_3 DNA_4".split()
                    )
                    data_signals_df.insert(0, "Well ID", self.well_ids, True)
                    data_signals_df.insert(1, "Source", plate[:2], True)
                    data_signals_df.insert(2, "Plate", plate, True)
                    data_signals_df.insert(0, "ID", data_signals_df["Source"] + "-" + data_signals_df["Well ID"], True)
                    data_signals_df.set_index("ID", inplace=True)
                    self.all_data_signals = pd.concat([self.all_data_signals, data_signals_df])
                    # pd.DataFrame.to_csv(self.all_data_signals, "all_data_df.csv")
                else:
                    rep_data_signals_df = pd.DataFrame(
                        rep_data_signals_list,
                        index=[x + 1 for x in range(len(rep_data_signals_list))],
                        columns="Alpha_1 Alpha_2 Alpha_3 Alpha_4 DNA_1 DNA_2 DNA_3 DNA_4".split()
                    )

                    rep_data_signals_df.insert(0, "Well ID", self.well_ids, True)
                    rep_data_signals_df.insert(1, "Source", plate[:2], True)
                    rep_data_signals_df.insert(2, "Plate", plate, True)
                    rep_data_signals_df.insert(0, "ID", rep_data_signals_df["Source"] +
                                               "-" + rep_data_signals_df["Well ID"], True)

                # TODO Need to create rep dataframes

        # pd.DataFrame.to_csv(self.all_data_signals, "data_output.csv")
        # return self.all_data_signals, self.all_rep_data_signals
        print(self.all_data_signals)
        return self.all_data_signals
