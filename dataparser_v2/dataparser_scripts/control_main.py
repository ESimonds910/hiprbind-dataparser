import pandas as pd
import json
import numpy as np
from time import time
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename
from string import ascii_uppercase as upstr
import file_split as fs
from import_csv import FileFinder
import data_formatter as formatter
import enspire_od_join as enspire_od_join
import pt_calculations as pt_calculations
from import_od import import_od

# TODO just create separate inputs module

def concat_projs(df):
    all_projs_df = pd.DataFrame()
    pass

def run_main(proj_dict):
    proj_concat = False
    file_finder = FileFinder()

    proj_dict = fs.split_projects(proj_dict)

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

        df_list = formatter.data_format(source_df, proj_data)

        if proj_data["od_file"]:
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

        with pd.ExcelWriter(f"../test_files/test_outputs/{project_title}_output_test.xlsx") as writer:
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
    try:
        with open(r"C:\Users\esimonds\parser_data.json", "r") as parser_file:
            proj_data_dict = json.load(parser_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Warning!", message="There's no file, did you complete the parser form?")
    # proj_names = [
    #     "SSF00626",
    # ]
    # proj_data_dict = {
    #     proj: {"plates": "",
    #            "raw_file": "",
    #            "od_file": r"L:\Molecular Sciences\Small Scale Runs\SSF00626 DSS Spaniel_discrete chaperone set\SSF00626 Spaniel (96DW) ELN v2.xlsm",
    #            "std_row": "",
    #            "std_pos": "",
    #            "std_conc": "",
    #            "volumes": vol_sp,
    #            "points": 4
    #            }
    #     for proj in proj_names
    # }
    # for proj, inner in proj_data_dict.items():
    #     add_std = input("Use standard? y/n    ")
    #     if add_std == 'y':
    #         more_ids = True
    #         std_conc = input("Enter standard concentration, e.g. '100, 50, 25, 12, 6, 3': ").split(",")
    #         std_conc_len = len(std_conc)
    #
    #         std_ids = []
    #         count = 1
    #         while more_ids == True:
    #             z = input("Enter 'column', 'row', 'none: ").lower()
    #             y = input("Enter staring well id, e.g. 'A11' or 'G1'").capitalize()
    #
    #             if z == "column":
    #                 col_letter = y[:1]
    #                 letter_idx = upstr.index(col_letter)
    #                 col_num = y[1:]
    #                 std_ids += [f"{upstr[letter]}{str(col_num).zfill(2)}" for letter in range(letter_idx, std_conc_len)]
    #
    #             elif z == 'row':
    #                 row_letter = y[:1]
    #                 row_num = int(y[1:])
    #                 std_ids += [f"{row_letter}{str(num).zfill(2)}" for num in range(row_num, row_num + std_conc_len)]
    #
    #             elif z == 'none':
    #                 break
    #
    #             else:
    #                 print("Sorry, you may not have typed 'column' or 'row'.")
    #
    #             add_more = input("Hit 'enter' to add replicates, or 'n' to continue: ").lower()
    #             if add_more == "n":
    #                 std_conc *= count
    #                 more_ids = False
    #             else:
    #                 count += 1
    #
    #         std_dict = dict(zip(std_ids, std_conc))
    #         inner["std_conc"] = std_dict
    #
    #
    #     if proj == "SSF00626":
    #         inner["plates"] = plate_ids_1
            # inner["volumes"] = vol_ak
            # inner["od_file"] = r"L:\Molecular Sciences\Small Scale Runs\SSF00627 DSS Spaniel003_discrete host screening\Copy of SSF00627 DSS Spaniel ELN_v2 copy.xlsm"
    run_main(proj_data_dict)
    window.destroy()
    end_time = time()
    split = round(end_time - start_time, 2)
    print(f"Program runtime: {split}s")
