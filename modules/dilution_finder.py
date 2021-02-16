import pandas as pd
import json
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import showinfo

FILE_PATH = "L:/High Throughput Screening/HiPrBind/parser_helper/modules/proj_data.json"


def dilution_folder():
    """
    Allows user to search and open file containing dilution values
    needed for SLIMS
    """
    dilution_path = askopenfilename(title='Open protocol with dilutions',
                                    initialdir="L:/Molecular Sciences/Small Scale Runs")
    try:
        dilution_data = pd.read_excel(dilution_path, usecols="L", skiprows=40, nrows=4)
        volumes = dilution_data['sample used (uL)'].to_list()
        str_volumes = ", ".join([str(volume) for volume in volumes])
        return str_volumes
    except ValueError:
        showinfo(title="Warning", message="Perhaps the dilution data was moved to another column")
        return False
    except KeyError:
        showinfo(title="Warning", message="Perhaps the dilution data was moved to another column")
        return False


def dilution_folder_multiple():
    """
    Allows user to search and open file containing dilution values
    needed for SLIMS
    """
    try:
        with open(FILE_PATH, "r") as proj_data_file:
            contents = json.load(proj_data_file)
    except FileNotFoundError:
        showinfo(title="Warning!", message="File not found or doesn't exist!")
    else:
        for entry, value in contents.items():
            dilution_path = askopenfilename(title=f'Open {entry} protocol with dilutions',
                                            initialdir="L:/Molecular Sciences/Small Scale Runs")
            try:
                dilution_data = pd.read_excel(dilution_path, usecols="L", skiprows=40, nrows=4)
                volumes = dilution_data['sample used (uL)'].to_list()
                str_volumes = ", ".join([str(volume) for volume in volumes])

            except ValueError:
                showinfo(title="Warning", message="Perhaps the dilution data was moved to another column")
                return False
            except KeyError:
                showinfo(title="Warning", message="Perhaps the dilution data was moved to another column")
                return False
            else:
                value["Dilution volumes"] = str_volumes
                with open(FILE_PATH, "w") as proj_data_file:
                    json.dump(contents, proj_data_file, indent=4)
                showinfo(title="Success!", message="Dilution volumes found and copied!")