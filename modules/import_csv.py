import pandas as pd
import numpy as np
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename

PLATE_IDX = [x for x in range(25)]
DNA_PLATE_IDX = [x for x in range(24, 49)]


class FileFinder:

    def __init__(self):
        self.window = Tk()
        self.window.withdraw()
        # File paths will eventually be take from json file
        # self.enspire_file_path = askopenfilename(title="Choose EnSpire file to import")
        # self.od_file_path = askopenfilename(title="Choose OD File to import")
        self.window.destroy()
        self.all_data = pd.DataFrame()
        self.all_rep_data = pd.DataFrame()

    def data_finder(self, plates, input_raw_path):

        all_alpha_data = pd.DataFrame()
        all_dna_data = pd.DataFrame()
        replicate_alpha_data = pd.DataFrame()
        replicate_dna_data = pd.DataFrame()

        try:
            count = 0
            for plate in plates:
                new_alpha_data = pd.read_csv(
                    input_raw_path,
                    header=None,
                    names=PLATE_IDX,
                    usecols=np.arange(0, 25),
                    skiprows=7 + count * 48,
                    nrows=16,
                    encoding='unicode_escape'
                )
                new_dna_data = pd.read_csv(
                    input_raw_path,
                    header=None,
                    names=DNA_PLATE_IDX,
                    usecols=np.arange(0, 25),
                    skiprows=31 + count * 48,
                    nrows=16,
                    encoding='unicode_escape'
                )

                new_alpha_data.insert(1, "Plate", plate)
                new_alpha_data.insert(2, "Source", plate[:2])
                new_alpha_data.rename(columns={0: "row"}, inplace=True)
                new_dna_data.rename(columns={24: "row"}, inplace=True)
                new_alpha_data.set_index(["row"], inplace=True)
                new_dna_data.set_index(["row"], inplace=True)

                if "-" in plate and plate.split("-")[1] == "2":
                    replicate_alpha_data = pd.concat([replicate_alpha_data, new_alpha_data])
                    replicate_dna_data = pd.concat([replicate_dna_data, new_dna_data])
                    count += 1
                else:
                    all_alpha_data = pd.concat([all_alpha_data, new_alpha_data])
                    all_dna_data = pd.concat([all_dna_data, new_dna_data])
                    count += 1
        except FileNotFoundError:
            pass
        else:
            self.all_data = pd.concat([all_alpha_data, all_dna_data], axis=1)
            self.all_rep_data = pd.concat([replicate_alpha_data, replicate_dna_data], axis=1)
            print(self.all_data)
            return self.all_data, self.all_rep_data


if __name__ == "__main__":
    FileFinder()
