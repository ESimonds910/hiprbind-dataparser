import json
import tkinter as tk
from tkinter import messagebox

FILE_PATH = "L:/High Throughput Screening/HiPrBind/parser_helper/modules/proj_data.json"
ARCHIVE_FILE_PATH = "L:/High Throughput Screening/HiPrBind/parser_helper/modules/archive_json_test.json"


class ArchiveData:
    def __init__(self):
        window = tk.Tk()
        window.withdraw()
        try:
            with open(FILE_PATH, "r") as self.proj_data_file:
                self.contents = json.load(self.proj_data_file)
        except FileNotFoundError:
            messagebox.showerror(title="Warning!", message="Project file not found or doesn't exist!")
        try:
            with open(ARCHIVE_FILE_PATH, "r") as self.arch_data_file:
                self.arch_contents = json.load(self.arch_data_file)
        except FileNotFoundError:
            with open(ARCHIVE_FILE_PATH, "w") as self.arch_data_file:
                json.dump(self.contents, self.arch_data_file, indent=4)
            # messagebox.showerror(title="Warning!", message="Archived file not found or doesn't exist!")
        else:
            self.arch_contents.update(self.contents)
            with open(ARCHIVE_FILE_PATH, "w") as self.arch_data_file:
                json.dump(self.arch_contents, self.arch_data_file, indent=4)

        messagebox.showinfo(title="Success!", message="Data has been archived!")
        window.destroy()
