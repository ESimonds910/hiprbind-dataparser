import pandas as pd


def join_dfs(df_list, raw_od, proj_data):
    std_pos = proj_data["std_pos"]
    std_row = proj_data["std_row"]
    std_conc = proj_data["std_conc"]
    ab_name = proj_data["ab_name"]
    join_df_list = []
    for df in df_list:
        df.set_index("Unique_Id", inplace=True)
        raw_od.set_index("Harvest_sample_id", drop=False, inplace=True)
        join_df = raw_od.join(df, how="right")

        try:
            join_df.loc[(join_df["std_conc"].apply(lambda x: x) != ""), "Sample_type"] = "Standard"
        except KeyError:
            pass
        # if std_pos == 'half':
        #     join_df.loc[
        #         (join_df["Well_Id"].apply(lambda x: x[:1]) == std_row) &
        #         (join_df["Well_Id"].apply(lambda x: int(x[1:]) > 6)), "Sample_type"
        #     ] = "Standard"
        # elif type(std_conc) == dict:
        #     join_df.loc[
        #         (join_df["Well_Id"].apply(lambda x: x in std_conc)), "Sample_type"
        #     ] = "Standard"
        # else:
        #     join_df.loc[
        #         (join_df["Well_Id"].apply(lambda x: x[:1]) == std_row), "Sample_type"
        #     ] = "Standard"
        if ab_name != "":
            join_df.insert(loc=1, column="HPB_scheme", value=ab_name)
        join_df_list.append(join_df)
    return join_df_list
