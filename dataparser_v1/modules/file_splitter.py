import csv
import json
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
import tkinter.messagebox as messagebox

FILE_PATH = "L:/High Throughput Screening/HiPrBind/parser_helper/modules/proj_data.json"


class FileFinder:
    """
    For one project: file found, copied, and moved to specified location
    for multiple: file found, split according to entry details, and moved
                to specified location
    """
    def __init__(self):
        try:
            with open(FILE_PATH, "r") as self.project_data_file:
                self.contents = json.load(self.project_data_file)
        except FileNotFoundError:
            messagebox.showerror(title="Warning!", message="File has had been deleted, or never existed.")
        else:
            self.split_projects()

    # def split_projects(self, proj_num, proj_ids):
    #     if proj_num == 1:
    #         name = entries[0][0].get()
    #
    #         folder_path_raw = askdirectory(title='Choose Raw folder from Project folder to place file for ' + name,
    #                                        initialdir='L:/Molecular Sciences/Small Scale Runs')
    #         # Set path for file move location and rename file with proj id
    #         raw_output = folder_path_raw + '/' + name + '.csv'
    #         # Move file to new location
    #         new_location = shutil.copy(file_path_raw, raw_output)
    #
    #         path_text.insert(END, '/mnt/lab' + raw_output.split(':')[1] + '\n')
    #
    #     if proj_num > 1:
    #         file_path = askopenfilename(title='Open HiPrBind Plate Data', initialdir="L:/Assay Development/Enspire")
    #
    #
    def split_projects(self):
        start = 0
        end = 0
        window = Tk()
        window.withdraw()

        file_path_raw = askopenfilename(title='Select file to copy', initialdir="L:/Assay Development/Enspire")
        for entry, plates in self.contents.items():
            name = entry
            plate_num = plates["plate num"]
            try:
                folder_path_raw = askdirectory(title="Choose Raw folder from Project folder to place file for " + name,
                                               initialdir='L:/Molecular Sciences/Small Scale Runs')
            except FileNotFoundError:
                pass
            else:
                print('%s and %s' % (name, plate_num))
                with open(file_path_raw) as csv_file:
                    reader = csv.reader(csv_file)
                    end += int(plate_num) * 48
                    plate_rows = [row for idx, row in enumerate(reader) if idx in range(start, end)]
                    start = end

                    raw_output = folder_path_raw + '/' + name + '.csv'
                    with open(raw_output, 'w', newline="") as newFile:
                        csv_writer = csv.writer(newFile)
                        for row in plate_rows:
                            csv_writer.writerow(row)

                    path_text = '/mnt/lab' + raw_output.split(':')[1]
                    plates["raw_file_path"] = path_text
# Update json contents
        with open(FILE_PATH, "w") as self.project_data_file:
            json.dump(self.contents, self.project_data_file, indent=4)

        messagebox.showinfo(title="Congrats!", message="File has been moved! Copy and Paste raw input file for SLIMS!")
        window.destroy()