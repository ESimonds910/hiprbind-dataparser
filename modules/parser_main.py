import json
import pandas as pd
from tkinter import Tk
import import_od as od
from tkinter.messagebox import showinfo
from modules.enspire_formatter import DataFormatter
from modules.import_csv import FileFinder
from modules.enspire_od_concat import DataConcat
from modules.calculations import Calculator

# TODO Import JSON file to use data


class DataParser:
    def __init__(self):
        try:
            with open("../proj_data.json") as self.proj_file:
                self.contents = json.load(self.proj_file)
        except FileNotFoundError:
            print("Did not work")
        else:
            # TODO Eventually add for loop to parse multiple projects
            proj_names = [key for key in self.contents.keys()]
            for proj_name in proj_names:
                self.proj_name = proj_name.split("-")[0]
                self.plate_ids = self.contents[proj_name]["Plate IDs"]
                self.dilutions = self.contents[proj_name]["Dilution volumes"]
                self.raw_file_path = self.contents[proj_name]["raw_file_path"]
                # self.raw_file_path = self.raw_file_path.replace("/mnt/lab", "L:")
                self.od_file_path = self.contents[proj_name]["OD path"]
                # self.od_file_path = self.od_file_path.replace("/mnt/lab", "L:")
                self.out_file_path = self.contents[proj_name]["Output path"]
                # self.out_file_path = self.out_file_path.replace("/mnt/lab", "L:")
                self.standard_row = "H"
                self.standard_conc = [24, 8.0, 2.7, 0.9, 0.3, 0.1] * 2
                self.parse_data()

    def parse_data(self):

        raw_od_df = od.import_od(self.od_file_path, self.standard_row)

        raw_enspire_df, all_rep_enspire_df = FileFinder().data_finder(self.plate_ids, self.raw_file_path, self.standard_row)
        formatted_enspire_df, display_ready_df = DataFormatter().formatter(
            raw_enspire_df,
            all_rep_enspire_df,
            self.plate_ids,
            self.dilutions,
            self.proj_name,
            self.standard_row,
            self.standard_conc
        )
        all_concat_df = DataConcat().data_concat(formatted_enspire_df, raw_od_df, self.standard_row)
        display_concat_df = DataConcat().display_data_concat(display_ready_df, raw_od_df, self.standard_row)
        clean_df = Calculator().make_calculations(all_concat_df, self.dilutions)
        print(clean_df)

        with pd.ExcelWriter(f"{self.proj_name}.xlsx") as writer:
            clean_df.to_excel(writer, sheet_name="Main_Data")
            display_concat_df.to_excel(writer, sheet_name="Display_Ready")


if __name__ == "__main__":
    DataParser()
    window = Tk()
    window.withdraw()
    showinfo("Way to go!", "Data has been output!")
    window.destroy()
