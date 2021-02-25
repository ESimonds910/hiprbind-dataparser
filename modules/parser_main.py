import json
from tkinter import Tk
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
                self.plate_ids = self.contents[proj_name]["Plate IDs"]
                self.dilutions = self.contents[proj_name]["Dilution volumes"]
                self.raw_file_path = self.contents[proj_name]["raw_file_path"]
                self.raw_file_path = self.raw_file_path.replace("/mnt/lab", "L:")
                self.od_file_path = self.contents[proj_name]["OD path"]
                self.od_file_path = self.od_file_path.replace("/mnt/lab", "L:")
                self.out_file_path = self.contents[proj_name]["Output path"]
                self.out_file_path = self.out_file_path.replace("/mnt/lab", "L:")
                self.parse_data()

    def parse_data(self):

        raw_enspire_df, all_rep_enspire_df, raw_od_df = FileFinder().data_finder(self.plate_ids, self.raw_file_path, self.od_file_path)
        formatted_enspire_df = DataFormatter().formatter(raw_enspire_df, all_rep_enspire_df, self.plate_ids)
        all_concat_df = DataConcat().data_concat(formatted_enspire_df, raw_od_df)
        Calculator(all_concat_df, self.dilutions, self.out_file_path)


if __name__ == "__main__":
    DataParser()
    window = Tk()
    window.withdraw()
    showinfo("Way to go!", "Data has been output!")
    window.destroy()
