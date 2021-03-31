import json
from tkinter import *
from tkinter import messagebox

BACKGROUND = "steel blue"
FONT = ("Arial", 12, "bold")
FILE_PATH = "L:/High Throughput Screening/HiPrBind/parser_helper/modules/proj_data.json"


class InputWindow:

    def __init__(self):
        self.entries = []
        self.project_data = open(FILE_PATH, "w")
        self.project_data.close()

        self.window = Tk()
        self.window.title("Input Data")
        self.window.config(padx=20, pady=20, bg=BACKGROUND)

        self.check_input_first = IntVar()
        self.check_input_last = IntVar()
        self.check_input_all = IntVar()

        self.proj_data_file = ""

        # self.text = Text(width=35, height=10)
        # self.text.grid(row=6, column=0, columnspan=4, pady=10)

        self.proj_id_label = Label(text="Enter Project ID: ", bg=BACKGROUND, fg="black", font=FONT)
        self.proj_id_label.grid(row=0, column=0, pady=10)

        self.plate_num_label = Label(text="Enter Plate Num: ", bg=BACKGROUND, fg="black", font=FONT)
        self.plate_num_label.grid(row=1, column=0)

        self.proj_id_entry = Entry()
        self.proj_id_entry.grid(row=0, column=1, pady=10)

        self.plate_num_entry = Entry()
        self.plate_num_entry.grid(row=1, column=1)

        self.checkbox_first = Checkbutton(text="First plate in replicate",
                                          font=("Arial", 11, "bold"),
                                          variable=self.check_input_first,
                                          bg=BACKGROUND,
                                          )

        self.checkbox_first.grid(row=2, column=0, columnspan=2)

        self.checkbox_last = Checkbutton(text="Last plate in replicate",
                                         bg=BACKGROUND,
                                         fg="black",
                                         variable=self.check_input_last,
                                         font=("Arial", 11, "bold"))

        self.checkbox_last.grid(row=3, column=0, columnspan=2)

        self.checkbox_all = Checkbutton(text="All plates in replicate",
                                        bg=BACKGROUND,
                                        variable=self.check_input_all,
                                        font=("Arial", 11, "bold"))

        self.checkbox_all.grid(row=4, column=0, columnspan=2)

        self.enter_button = Button(text="Add Data", width=10, height=1, command=self.save_data)
        self.enter_button.grid(row=5, column=0, pady=10, padx=5)

        self.close_button = Button(text="Continue", width=10, height=1, command=self.window.destroy)
        self.close_button.grid(row=5, column=1, pady=10, padx=5)

        self.update_text()

        self.window.mainloop()

    def save_data(self):
        try:
            entry = self.proj_id_entry.get()
            plate_num = int(self.plate_num_entry.get())
            first_plate_rep = int(self.check_input_first.get())
            last_plate_rep = int(self.check_input_last.get())
            all_plate_rep = int(self.check_input_all.get())

        except ValueError:
            messagebox.showerror(title="Wait!", message="Plate number is not an integer!")
        else:
            if entry == "":
                messagebox.showerror(title="Wait!", message="You left an entry blank!")
            elif plate_num <= 0:
                messagebox.showerror(title="Wait!", message="Plate number is not an integer or more than 0")
            else:
                project_data = {
                    entry: {
                        "plate num": plate_num,
                        "first rep": first_plate_rep,
                        "last rep": last_plate_rep,
                        "all rep": all_plate_rep,
                    },
                }
                try:
                    with open(FILE_PATH, "r") as self.proj_data_file:
                        contents = json.load(self.proj_data_file)
                        contents.update(project_data)
                except json.decoder.JSONDecodeError:
                    # messagebox.showerror(title="Warning!", message="File is empty")
                    with open(FILE_PATH, "w") as self.proj_data_file:
                        json.dump(project_data, self.proj_data_file, indent=4)
                    messagebox.showinfo(title="Success!", message="Data Added!")
                    self.update_text()

                # except FileNotFoundError:
                #     self.proj_data_file = open("proj_data.json", "w")
                #     self.proj_data_file.close()
                #     with open("proj_data.json", "w") as self.proj_data_file:
                #         json.dump(self.project_data, self.proj_data_file, indent=4)
                else:
                    with open(FILE_PATH, "w") as self.proj_data_file:
                        json.dump(contents, self.proj_data_file, indent=4)
                    messagebox.showinfo(title="Success!", message="Data Added!")
                    self.update_text()

    def update_text(self):
        # print(self.project_data)
        # try:
        #     with open("proj_data.json", "r") as self.proj_data_file:
        #         contents = json.load(self.proj_data_file)
        #         contents.update(self.project_data)
        # except json.decoder.JSONDecodeError:
        #     messagebox.showerror(title="Warning!", message="File is empty")
        # except FileNotFoundError:
        #     self.proj_data_file = open("proj_data.json", "w")
        #     self.proj_data_file.close()
        #     with open("proj_data.json", "w") as self.proj_data_file:
        #         json.dump(self.project_data, self.proj_data_file, indent=4)
        # else:
        #     with open("proj_data.json", "w") as self.proj_data_file:
        #         json.dump(contents, self.proj_data_file, indent=4)
        # finally:
        # self.text.delete("1.0", END)
        # self.text.insert(END, contents)
        self.proj_id_entry.delete(0, END)
        self.plate_num_entry.delete(0, END)
        self.checkbox_first.deselect()
        self.checkbox_last.deselect()
        self.checkbox_all.deselect()
