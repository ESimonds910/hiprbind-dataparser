from tkinter import Tk
from tkinter.filedialog import askopenfilename
from modules.import_csv import FileFinder
import data_formatter
import eight_pt_calculations

import pandas as pd

file_finder = FileFinder()

window = Tk()
window.withdraw()
proj_name = input("Enter project name: ")
plate_num = int(input("Enter number of plates: "))
plates = [f"P{x}" for x in range(1, plate_num+1)]
volumes = input("Enter the volumes used for experiment: ").split(",")
volumes = [float(x) for x in volumes]
raw_enpsire_path = askopenfilename(title="Choose raw file")

# This data will be used for testing
# plates = "P1 P2 P3 P4 P5 P6".split()
# volumes = [0.5, 0.25, 0.125, 0.0625, 0.03125, 0.02, 0.01, 0.001]
# raw_enpsire_path = r"L:/High Throughput Screening/HiPrBind/Data_Parser_Helper_Tool/Training Helper tool/TestEnpireFile.csv"

# window.destroy()


source_df, rep_df, od = file_finder.data_finder(plates, raw_enpsire_path, "")

clean_df = data_formatter.data_format(source_df, plates, volumes)

complete_df = eight_pt_calculations.make_calculations(clean_df)

with pd.ExcelWriter(f"{proj_name}.xlsx") as writer:
    clean_df.to_excel(writer, sheet_name="Sorted_Raw_Data")
    complete_df.to_excel(writer, sheet_name="Calculations")
