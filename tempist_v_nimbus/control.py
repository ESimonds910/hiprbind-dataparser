import pandas as pd
from time import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from import_csv_test import FileFinder
import data_formatter
import eight_pt_calculations
from eight_point_concat import DataConcat
from modules.import_od import import_od


def join_dfs(df_list, raw_od, std_pos, std_row, ab_name):
    join_df_list = []
    for df in df_list:
        df.set_index("Unique_Id", inplace=True)
        raw_od.set_index("Harvest_sample_id", drop=False, inplace=True)
        join_df = raw_od.join(df, how="right")
        if std_pos == 'half':
            join_df.loc[
                (join_df["Well_Id"].apply(lambda x: x[:1]) == std_row) &
                (join_df["Well_Id"].apply(lambda x: int(x[1:]) > 6)), "Sample_type"
            ] = "Standard"
        else:
            join_df.loc[
                (join_df["Well_Id"].apply(lambda x: x[:1]) == std_row), "Sample_type"
            ] = "Standard"
        if ab_name != "":
            join_df.insert(loc=1, column="HPB_scheme", value=ab_name)
        join_df_list.append(join_df)
    return join_df_list


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
        # plate_num = 11
        # plates = [f"P{x}" for x in range(1, plate_num+1)]
        plates = ["P2-1", "P2-2"]
        # volumes = input("Enter the volumes used for experiment: ").split(",")
        # volumes = [float(x) for x in volumes]
        raw_enpsire_path = askopenfilename(title="Choose raw file")
        # od_file_path = askopenfilename(title="Choose ELN file")
        od_file_path = r"L:\Molecular Sciences\Small Scale Runs\SSF00613 DSS (96DW) Xolo 40 variant screening\SSF00613 Discrete Strain Screening (DSS) 96DW ELN v1.5.xlsm".replace("\\", "/")
        # This data will be used for testing
        std_row = "D"
        std_pos = ""
        std_conc = [24, 8, 2.7, 0.9, 0.3, 0.1] * 2
        # plates = "P1 P2 P3 P4 P5 P6".split()
        volumes = [2.000, 0.667, 0.222, 0.074, 0.025, 0.008, 0.003, 0.001]
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

        df_list = [clean_df, main_df, clean_rep_df, main_rep_df]
        dfs_return = join_dfs(df_list, raw_od, std_pos, std_row, ab_name)
        # clean_df.set_index("Unique_Id", inplace=True)
        # raw_od.set_index("Harvest_id", drop=False, inplace=True)
        # clean_join_df = raw_od.join(clean_df, how="right")
        # if std_pos == 'half':
        #     clean_join_df.loc[
        #         (clean_join_df["Well_Id"].apply(lambda x: x[:1]) == std_row) &
        #         (clean_join_df["Well_Id"].apply(lambda x: int(x[1:]) > 6)), "Abs_id"
        #     ] = "Standard"
        # else:
        #     clean_join_df.loc[
        #         (clean_join_df["Well_Id"].apply(lambda x: x[:1]) == std_row), "Abs_id"
        #     ] = "Standard"
        # if ab_name != "":
        #     clean_join_df.insert(loc=1, column="HPB_scheme", value=ab_name)
        #
        # main_df.set_index("Unique_Id", drop=False, inplace=True)
        # main_join_df = raw_od.join(main_df, how="right")
        # if std_pos == 'half':
        #     main_join_df.loc[
        #         (main_join_df["Well_Id"].apply(lambda x: x[:1]) == std_row) &
        #         (main_join_df["Well_Id"].apply(lambda x: int(x[1:]) > 6)), "Abs_id"
        #     ] = "Standard"
        # else:
        #     main_join_df.loc[
        #         (main_join_df["Well_Id"].apply(lambda x: x[:1]) == std_row), "Abs_id"
        #     ] = "Standard"
        # if ab_name != "":
        #     main_join_df.insert(loc=1, column="HPB_scheme", value=ab_name)
        # # clean_join_df = concat_data.concat_display(clean_df, raw_od)
        # # main_join_df = concat_data.concat_data(main_df, raw_od)
        # # main_join_df.to_csv("test_df_precalc.csv")
        clean_join_df = dfs_return[0]
        main_join_df = dfs_return[1]
        clean_rep_join_df = dfs_return[2]
        main_rep_join_df = dfs_return[3]

        complete_df = eight_pt_calculations.make_calculations(main_join_df, volumes)
        complete_rep_df = eight_pt_calculations.make_calculations(main_rep_join_df, volumes)

        with pd.ExcelWriter(f"{project_title}_output.xlsx") as writer:
            complete_df.to_excel(writer, sheet_name="Calculations")
            clean_join_df.to_excel(writer, sheet_name="Display_Ready")
            complete_rep_df.to_excel(writer, sheet_name="Rep_Calculations")
            clean_rep_join_df.to_excel(writer, sheet_name="Rep_Display_Ready")
        print(f"Project {project_title} has been output.")


if __name__ == "__main__":
    start_time = time()
    window = Tk()
    window.withdraw()
    proj_names = [
        "SSF00613-p1-CD19",
        "SSF00613-p1-ULBP2",
        "SSF00613-p2-CD19",
        "SSF00613-p2-ULBP2",
        "SSF00613-p3-CD19",
        "SSF00613-p3-ULBP2"
    ]
    run_main(proj_names)
    window.destroy()
    end_time = time()
    split = round(end_time - start_time, 2)
    print(f"Program runtime: {split}s")
