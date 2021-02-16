import json
from tkinter import messagebox

FILE_PATH = "L:/High Throughput Screening/HiPrBind/parser_helper/modules/proj_data.json"


class PlateIDGenerator:

    def __init__(self):
        try:
            with open(FILE_PATH, "r") as self.proj_data_file:
                self.contents = json.load(self.proj_data_file)
        except FileNotFoundError:
            messagebox.showerror(title="Warning!", message="File does not exist or no data was created!")
        else:
            for entry, value in self.contents.items():
                if value["all rep"] == 1:
                    plate_ids = []
                    for x in range(int(value["plate num"] / 2)):
                        plate_ids.append(f"P{x + 1}-1")
                        plate_ids.append(f"P{x + 1}-2")
                else:
                    plate_ids = [f"P{num + 1}" for num in range(value["plate num"] - 1)]
                    first_ids = ["P1-1", "P1-2"]
                    last_ids = [f"P{value['plate num'] - 1}-1", f"P{value['plate num'] - 1}-2"]

                    if value["first rep"] == 1 and value["last rep"] == 1:
                        plate_ids = first_ids + plate_ids[1:value["plate num"] - 3] + \
                                    [f"P{value['plate num'] - 2}-1", f"P{value['plate num'] - 2}-2"]
                    elif value["first rep"] == 1:
                        plate_ids = first_ids + plate_ids[1:]
                    elif value["last rep"] == 1:
                        plate_ids = plate_ids[:value["plate num"] - 2] + last_ids

                value["Plate IDs"] = plate_ids

            with open(FILE_PATH, "w") as self.proj_data_file:
                json.dump(self.contents, self.proj_data_file, indent=4)



