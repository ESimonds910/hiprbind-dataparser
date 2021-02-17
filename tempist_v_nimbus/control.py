from tkinter import Tk
from tkinter.filedialog import askopenfilename
from modules.import_csv import FileFinder

file_finder = FileFinder()

# window = Tk()
# window.withdraw()
plate_num = int(input("Enter number of plates: "))
plates = [f"P-{x}" for x in range(1, plate_num+1)]
volumes = input("Enter the volumes used for experiment: ")
raw_enpsire_path = askopenfilename(title="Choose raw mile")
# window.destroy()


source_df, rep_df, od = file_finder.data_finder(plates, raw_enpsire_path, "")
print(alpha_df)