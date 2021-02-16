import json
from tkinter import *
from tkinter import messagebox

BACKGROUND = "steel blue"
FONT = ("Arial", 12, "bold")

FILE_PATH = "L:/High Throughput Screening/HiPrBind/parser_helper/modules/proj_data.json"


class DisplayData:
    def __init__(self):
        pass
        with open(FILE_PATH, "r") as self.proj_data:
            self.contents = json.load(self.proj_data)
        self.proj_ids = [key for key in self.contents.keys()]

        self.window = Tk()
        self.window.title("Project Display")
        self.window.config(padx=50, pady=20, bg=BACKGROUND)
        self.proj_id_selected = StringVar(self.window)
        self.proj_id_selected.set("")

        self.cmbx_label = Label(text="Choose project to display: ", bg=BACKGROUND, font=FONT)
        self.cmbx_label.grid(row=0, column=0)

        self.proj_cmbx = OptionMenu(self.window, self.proj_id_selected, *self.proj_ids)
        self.proj_cmbx.config(width=15, highlightthickness=0)
        self.proj_cmbx.grid(row=0, column=1, sticky=W)

        self.select_proj_id = Button(text="Select", width=15, command=self.select_proj)
        self.select_proj_id.grid(row=1, column=0, pady=20, sticky=W)

        # All labels for display window

        self.proj_id_label = Label(text="Project ID: ", bg=BACKGROUND, font=FONT)
        self.proj_id_label.grid(row=2, column=0, pady=20, sticky=E)
        self.raw_label = Label(text="Raw File Location: ", bg=BACKGROUND, font=FONT)
        self.raw_label.grid(row=3, column=0, pady=20, sticky=E)
        self.plate_ids_label = Label(text="Plate IDs: ", bg=BACKGROUND, font=FONT)
        self.plate_ids_label.grid(row=4, column=0, pady=20, sticky=E)
        self.dilutions_label = Label(text="Dilution Volumes: ", bg=BACKGROUND, font=FONT)
        self.dilutions_label.grid(row=5, column=0, pady=20, sticky=E)
        self.od_file_label = Label(text="OD File Location: ", bg=BACKGROUND, font=FONT)
        self.od_file_label.grid(row=6, column=0, pady=20, sticky=E)
        self.output_label = Label(text="Output File Location: ", bg=BACKGROUND, font=FONT)
        self.output_label.grid(row=7, column=0, pady=20, sticky=E)

        # All boxes that will display data

        self.proj_id_display = Entry()
        self.proj_id_display.grid(row=2, column=1, pady=20, sticky=W)
        self.raw_display = Text(height=3, width=50)
        self.raw_display.insert(END, "")
        self.raw_display.grid(row=3, column=1, pady=20, sticky=W)
        self.plate_ids_display = Entry(width=60)
        self.plate_ids_display.grid(row=4, column=1, pady=20, sticky=W)
        self.dilutions_display = Entry(width=60)
        self.dilutions_display.grid(row=5, column=1, pady=20, sticky=W)
        self.od_file_display = Text(height=3, width=50)
        self.od_file_display.insert(END, "")
        self.od_file_display.grid(row=6, column=1, pady=20, sticky=W)
        self.output_display = Text(height=3, width=50)
        self.output_display.insert(END, "")
        self.output_display.grid(row=7, column=1, pady=20, sticky=W)

        self.close_window = Button(text="Close", width=15, command=self.window.destroy)
        self.close_window.grid(row=8, column=0, pady=20, sticky=W)

        self.window.mainloop()

    def select_proj(self):
        selected_proj = self.proj_id_selected.get()
        display_data = self.contents[selected_proj]
        display_keys = ["raw_file_path", "Plate IDs", "Dilution volumes", "OD path", "Output path"]
        for key in display_keys:
            if key not in display_data.keys():
                display_data[key] = " "

        self.clear_data()

        self.proj_id_display.insert(END, selected_proj)
        self.raw_display.insert(END, display_data["raw_file_path"])
        self.plate_ids_display.insert(END, ", ".join(display_data['Plate IDs']))
        self.dilutions_display.insert(END, display_data["Dilution volumes"])
        self.od_file_display.insert(END, display_data["OD path"])
        self.output_display.insert(END, display_data["Output path"])

    def clear_data(self):
        self.proj_id_display.delete(0, END)
        self.raw_display.delete("1.0", END)
        self.plate_ids_display.delete(0, END)
        self.dilutions_display.delete(0, END)
        self.od_file_display.delete("1.0", END)
        self.output_display.delete("1.0", END)
