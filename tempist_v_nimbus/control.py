import pandas as pd
from time import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from import_csv_test import FileFinder
import data_formatter
import eight_pt_calculations
from eight_point_concat import DataConcat
from modules.import_od import import_od




def run_main(proj_names):
    file_finder = FileFinder()
    # proj_name = input("Enter project name: ")
    # plate_num = int(input("Enter number of plates: "))
    for proj in proj_names:
        project_title = proj
        if "-" in proj:
            proj_name = proj.split("-")[0]
            ab_name = proj.split("-")[-1]
        else:
            ab_name = ""
            proj_name = proj
        plate_num = 11
        # plates = [f"P{x}" for x in range(1, plate_num+1)]
        plates = ["P1-1", "P1-2", "P2", "P3", "P4-1", "P4-2"]
        # volumes = input("Enter the volumes used for experiment: ").split(",")
        # volumes = [float(x) for x in volumes]
        raw_enpsire_path = askopenfilename(title="Choose raw file")
        od_file_path = askopenfilename(title="Choose ELN file")

        # This data will be used for testing
        std_row = "D"
        std_pos = "half"
        std_conc = [100, 50, 16.7, 5.6, 1.9, 0.6] * 2
        # plates = "P1 P2 P3 P4 P5 P6".split()
        volumes = [0.21428571, 0.03061224, 0.00437318, 0.00062474, 0.00008925, 0.00001275, 0.00000182, 0.00000026]
        # raw_enpsire_path = r"L:/High Throughput Screening/HiPrBind/Data_Parser_Helper_Tool/Training Helper tool/TestEnpireFile.csv"

        # window.destroy()

        raw_od = import_od(od_file_path)

        source_df, rep_df = file_finder.data_finder(
            plates,
            raw_enpsire_path,
            std_row
        )

        clean_df, main_df, clean_rep_df, main_rep_df = data_formatter.data_format(
            source_df,
            proj_name,
            plates,
            volumes,
            std_row,
            std_conc,
            std_pos
        )

        clean_df.set_index("Unique_Id", inplace=True)
        raw_od.set_index("Harvest_id", drop=False, inplace=True)
        clean_concat_df = raw_od.join(clean_df, how="right")
        if std_pos == 'half':
            clean_concat_df.loc[
                (clean_concat_df["Well_Id"].apply(lambda x: x[:1]) == std_row) &
                (clean_concat_df["Well_Id"].apply(lambda x: int(x[1:]) > 6)), "Abs_id"
            ] = "Standard"
        else:
            clean_concat_df.loc[
                (clean_concat_df["Well_Id"].apply(lambda x: x[:1]) == std_row), "Abs_id"
            ] = "Standard"
        if ab_name != "":
            clean_concat_df.insert(loc=1, column="HPB_scheme", value=ab_name)

        main_df.set_index("Unique_Id", drop=False, inplace=True)
        main_concat_df = raw_od.join(main_df, how="right")
        if std_pos == 'half':
            main_concat_df.loc[
                (main_concat_df["Well_Id"].apply(lambda x: x[:1]) == std_row) &
                (main_concat_df["Well_Id"].apply(lambda x: int(x[1:]) > 6)), "Abs_id"
            ] = "Standard"
        else:
            main_concat_df.loc[
                (main_concat_df["Well_Id"].apply(lambda x: x[:1]) == std_row), "Abs_id"
            ] = "Standard"
        if ab_name != "":
            main_concat_df.insert(loc=1, column="HPB_scheme", value=ab_name)
        # clean_concat_df = concat_data.concat_display(clean_df, raw_od)
        # main_concat_df = concat_data.concat_data(main_df, raw_od)
        # main_concat_df.to_csv("test_df_precalc.csv")
        complete_df = eight_pt_calculations.make_calculations(main_concat_df, volumes)

        with pd.ExcelWriter(f"{proj_name}.xlsx") as writer:
            complete_df.to_excel(writer, sheet_name="Calculations")
            clean_concat_df.to_excel(writer, sheet_name="Display_Ready")
        print(f"Project {project_title} has been output.")


if __name__ == "__main__":
    start_time = time()
    window = Tk()
    window.withdraw()
    proj_names = ["SOM00001-CD19", "SOM00001-ULBP2"]
    run_main(proj_names)
    window.destroy()
    end_time = time()
    split = round(end_time - start_time, 2)
    print(f"Program runtime: {split}s")
