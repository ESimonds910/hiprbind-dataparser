import json
from tkinter import *
import dataparser_v1.modules.dilution_finder as dilutions
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import messagebox

BACKGROUND = "steel blue"
FILE_PATH = "L:/High Throughput Screening/HiPrBind/parser_helper/modules/proj_data.json"


class PathFinder:

    def __init__(self):
        self.window = Tk()
        self.window.title("Find your path in life")
        self.window.config(pady=20, padx=20, bg=BACKGROUND)

        self.check_od = IntVar()
        self.check_output = IntVar()

        self.checkbox_od = Checkbutton(text="OD file path",
                                            bg=BACKGROUND,
                                            width=20,
                                            fg="black",
                                            variable=self.check_od,
                                            font=("Arial", 11, "bold"))

        self.checkbox_od.grid(row=0, column=0)

        self.checkbox_output = Checkbutton(text="Output file path",
                                                bg=BACKGROUND,
                                                width=20,
                                                variable=self.check_output,
                                                font=("Arial", 11, "bold"))

        self.checkbox_output.grid(row=1, column=0)

        self.find_path_button = Button(text="Find file path", command=self.find_path)
        self.find_path_button.grid(row=2, column=0, pady=10)

        self.find_dilution_button = Button(text="Find dilutions", command=self.find_dilutions)
        self.find_dilution_button.grid(row=3, column=0, pady=10)

        self.close_button = Button(text="Close", command=self.window.destroy)
        self.close_button.grid(row=4, column=0, pady=10)

        self.window.mainloop()

    def find_path(self):
        try:
            with open(FILE_PATH, "r") as proj_data_file:
                contents = json.load(proj_data_file)
        except FileNotFoundError:
            messagebox.showerror(title="Warning!", message="File has not been created or no data exists!")
        else:
            for entry, value in contents.items():
                if self.check_od.get() == 1:
                    # Insert initial directory
                    od_path = askopenfilename(title=f"Find {entry} OD file:")
                    od_path = '/mnt/lab' + od_path.split(':')[1]
                    value["OD path"] = od_path

                if self.check_output.get() == 1:

                    output_path = askdirectory(title=f"Find {entry} processed folder for output:")
                    output_path = f"/mnt/lab{output_path.split(':')[1]}/{entry}_output.xlsx"
                    value["Output path"] = output_path

        with open(FILE_PATH, "w") as proj_data_file:
            json.dump(contents, proj_data_file, indent=4)

        messagebox.showinfo(title="Success!", message="File paths copied and formatted!")

    def find_dilutions(self):
        dilutions.dilution_folder_multiple()

# Remember to remove


