import pandas as pd
from tkinter import messagebox


def import_eln_od(input_od_path):
    try:
        od_data = pd.read_excel(input_od_path, sheet_name="Growth Details")
    except FileNotFoundError:
        messagebox.showinfo(title="Uh oh...", message="Something's wrong. The OD file wasn't found.")
    else:
        return od_data

def import_od(input_od_path, standard_row):
    try:
        od_data = pd.read_excel(input_od_path)
    except FileNotFoundError:
        messagebox.showinfo(title="Uh oh...", message="Something's wrong. The OD file wasn't found.")
        pass
    else:
        try:
            for column in od_data.columns:
                od_data.rename(columns={column: column.lower().title().strip()}, inplace=True)
            od_data.dropna(thresh=3, subset=od_data.columns[:-1], inplace=True)
            od_data.dropna(axis=1, how="all", inplace=True)
            od_data["Od600"] = od_data["Od600"].replace(" ", "0.0")
            od_data.set_index("Harvest Sample Id", drop=False, inplace=True)
            od_data.loc[(od_data["Harvest Well"].apply(lambda x: x[:1]) == standard_row), "Sample Type"] = "Standard"
        except KeyError:
            od_data = import_eln_od(input_od_path)
            for column in od_data.columns:
                od_data.rename(columns={column: column.lower().title().strip()}, inplace=True)
            od_data.dropna(thresh=3, subset=od_data.columns[:-1], inplace=True)
            od_data.dropna(axis=1, how="all", inplace=True)
            od_data["Od600"] = od_data["Od600"].replace(" ", "0.0")
            od_data.set_index("Harvest_Sample_Id", drop=False, inplace=True)

        finally:
            return od_data


if __name__ == "__main__":
    standard_row = "H"
    od_file_path = "L:/Molecular Sciences/Small Scale Runs/SSF00603 DSS Xolo reference sequence into 3 hosts/SSF00603 "\
                   "Xolo Discrete Strain Screening (DSS) ELN v1.xlsx"
    # od_file_path = "L:/Molecular Sciences/Small Scale Runs/SSF00607 Discrete Strain Screening (DSS) akita Compare " \
    #                "Chap hits side-by-side/Assays/OD/Processed/SSF00607 24DW OD.xlsx "
    import_od(od_file_path, standard_row)
