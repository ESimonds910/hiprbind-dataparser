from tkinter import Tk
from tkinter.filedialog import askopenfilename
from modules.import_csv import FileFinder
import data_formatter
import pandas as pd

file_finder = FileFinder()

# window = Tk()
# window.withdraw()
# plate_num = int(input("Enter number of plates: "))
# plates = [f"P{x}" for x in range(1, plate_num+1)]
# volumes = input("Enter the volumes used for experiment: ")
# raw_enpsire_path = askopenfilename(title="Choose raw mile")

# This data will be used for testing
plates = "P1 P2 P3 P4 P5 P6".split()
raw_enpsire_path = r"L:/High Throughput Screening/HiPrBind/Data_Parser_Helper_Tool/Training Helper tool/TestEnpireFile.csv"

# window.destroy()


source_df, rep_df, od = file_finder.data_finder(plates, raw_enpsire_path, "")

data_formatter.data_format(source_df)