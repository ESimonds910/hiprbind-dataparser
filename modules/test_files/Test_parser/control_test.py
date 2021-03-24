import pandas as pd
from time import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from modules.test_files.Test_parser.import_csv_test import FileFinder
import modules.test_files.Test_parser.test_formatter as test_formatter
import modules.test_files.Test_parser.enspire_od_join_test as enspire_od_join
import modules.test_files.Test_parser.pt_calculations_test as pt_calculations
from modules.test_files.Test_parser.import_od_test import import_od


def run_main(proj_dict):
    file_finder = FileFinder()

    for proj, inner_dict in proj_dict.items():
        project_title = proj
        if "-" in proj:
            inner_dict["proj_name"] = proj.split("-")[0]
            inner_dict["ab_name"] = proj.split("-")[-1]
        else:
            inner_dict["ab_name"] = ""
            inner_dict["proj_name"] = proj

        proj_data = proj_dict[proj]

        source_df = file_finder.data_finder(proj_data)

        df_list = test_formatter.data_format(source_df, proj_data)

        if proj_data["od_file"] != "":
            raw_od = import_od(proj_data)
            joined_df_list = enspire_od_join.join_dfs(df_list, raw_od, proj_data)
            main_join_dfs = joined_df_list[:2]
            final_display_df = joined_df_list[2]
            final_display_rep_df = joined_df_list[3]
            completed_main_dfs = pt_calculations.make_calculations(main_join_dfs, proj_data)
        else:
            main_dfs = df_list[:2]
            final_display_df = df_list[2]
            final_display_rep_df = df_list[3]
            completed_main_dfs = pt_calculations.make_calculations(main_dfs, proj_data)

        final_main_df = completed_main_dfs[0]
        final_main_rep_df = completed_main_dfs[1]

        with pd.ExcelWriter(f"../test_outputs/{project_title}_output_test.xlsx") as writer:
            final_main_df.to_excel(writer, sheet_name="Calculations")
            final_display_df.to_excel(writer, sheet_name="Display_Ready")
            final_main_rep_df.to_excel(writer, sheet_name="Rep_Calculations")
            final_display_rep_df.to_excel(writer, sheet_name="Rep_Display_Ready")
        print(f"Project {project_title} has been output.")

        # Also return these four dataframes into list?
        # clean_df, main_df, clean_rep_df, main_rep_df = test_formatter.data_format(source_df, proj_data)
        # df_list = [clean_df, main_df, clean_rep_df, main_rep_df]
        # dfs_return = join_dfs(df_list, raw_od, proj_data)
        #
        # clean_join_df = dfs_return[0]
        # main_join_df = dfs_return[1]
        # clean_rep_join_df = dfs_return[2]
        # main_rep_join_df = dfs_return[3]
        #
        # complete_df = eight_pt_calculations.make_calculations(main_join_df, proj_data)
        # complete_rep_df = eight_pt_calculations.make_calculations(main_rep_join_df, proj_data)
        #



if __name__ == "__main__":
    start_time = time()
    window = Tk()
    window.withdraw()
    proj_names = [
        "SSF00622-CD19",
        "SSF00622-ULBP2",
    ]
    u_volumes = [2.40000, 0.48000, 0.09600, 0.01920, 0.00384, 0.00077, 0.00015, 0.00003]
    c_volumes = [4.286, 1.531, 0.547, 0.195, 0.070, 0.025, 0.009, 0.003]
    # plates = input("Plate ids: ").split(" ")
    # raw_enpsire_path = askopenfilename(title="Choose raw file")
    # # od_file_path = askopenfilename(title="Choose ELN file")
    # od_file_path = r"L:\Molecular Sciences\Small Scale Runs\SSF00613 DSS (96DW) Xolo 40 variant screening\SSF00613 Discrete Strain Screening (DSS) 96DW ELN v1.5.xlsm".replace(
    #     "\\", "/")
    #
    # std_row = "D"
    # std_pos = "half"
    # std_conc = [24, 8, 2.7, 0.9, 0.3, 0.1] * 2
    # volumes = [2.000, 0.667, 0.222, 0.074, 0.025, 0.008, 0.003, 0.001]

    proj_data_dict = {
        proj: {"plates": input("Plate ids: ").split(" "),
               "raw_file": askopenfilename(title="Choose raw file"),
               "od_file": r"L:\Molecular Sciences\Small Scale Runs\SSF00622 DSS (96DW) XOLO 40 variant screening Repeat of SSF00613\SSF00622 Xolo DSS ELN v2.xlsm",
               "std_row": "D",
               "std_pos": "half",
               "std_conc": [24, 8.0, 2.7, 0.9, 0.3, 0.1] * 2,
               "volumes": "",
               "points": 8
               }
        for proj in proj_names
    }
    for proj, inner in proj_data_dict.items():
        if proj == "SSF00622-CD19":
            inner["volumes"] = c_volumes
        else:
            inner["volumes"] = u_volumes

    run_main(proj_data_dict)
    window.destroy()
    end_time = time()
    split = round(end_time - start_time, 2)
    print(f"Program runtime: {split}s")
