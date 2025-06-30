import geopandas as gpd
import pandas as pd
import os
from libs.constants import OUTPUT_DATA_PATH


def calculate(land_cells, other_crop_name, regions_info, input_data):
    scenario = input_data['scenario']
    admin_level = input_data['admin_level']
    country_name = input_data['country_name']
    regions_list = regions_info["regions_list"]
    regions_gdf = regions_info["regions_gdf"]
    origin_list_of_cols = gpd.read_file(
        f"{OUTPUT_DATA_PATH}/{scenario}/{country_name}_vector_admin{admin_level}_land_cells.gpkg")
    final_list_of_cols = list(land_cells.columns)

    # Land cover area estimator
    def calc_lc_sqkm(df, col_list):
        """
        This function takes the df where the LC type for different classes is provided per location (row).
        It adds all pixels per location; then is calculates the ratio of LC class in each location (% of total).
        Finally is estimates the area per LC type in each location by multiplying with the total area each row represents.

        INPUT:
        df -> Pandas dataframe with LC type classification
        col_list -> list of columns to include in the summary (e.g. LC1-LC11)

        OUTPUT: Updated dataframe with estimated area (sqkm) of LC types per row
        """
        df["LC_sum"] = df[col_list].sum(axis=1)
        for col in col_list:
            df[col] = df[col] / df["LC_sum"] * df["sqkm"]

        return df

    # Add new column contain average value of five to ten in the top 10 crops
    def additional_stat_group(parameter):
        selected_group = [col for col in additional_stat_table_group.columns if parameter in col]

        selected_group = additional_stat_table_group.loc[:, selected_group]

        Irrigation_Low_group = selected_group.loc[:, [a for a in selected_group.columns if 'Irrigation Low' in a]]
        Low_group = round(Irrigation_Low_group.mean(axis=1), 4)
        clusters_stat['OTH' + ' ' + parameter + ' ' + 'Irrigation Low_mean'] = Low_group

        Irrigation_High_group = selected_group.loc[:, [a for a in selected_group.columns if 'Irrigation High' in a]]
        High_group = round(Irrigation_High_group.mean(axis=1), 4)
        clusters_stat['OTH' + ' ' + parameter + ' ' + 'Irrigation High_mean'] = High_group

        Rain_fed_Low_group = selected_group.loc[:, [a for a in selected_group.columns if 'Rain-fed Low' in a]]
        Rain_Low = round(Rain_fed_Low_group.mean(axis=1), 4)
        clusters_stat['OTH' + ' ' + parameter + ' ' + 'Rain-fed Low_mean'] = Rain_Low

        Rain_fed_High_group = selected_group.loc[:, [a for a in selected_group.columns if 'Rain-fed High' in a]]
        Rain_High = round(Rain_fed_High_group.mean(axis=1), 4)
        clusters_stat['OTH' + ' ' + parameter + ' ' + 'Rain-fed High_mean'] = Rain_High

        # Identify land cover related columns
    land_cover_cols = []
    for col in final_list_of_cols:
        if "LCType" in col:
            land_cover_cols.append(col)
    if not land_cover_cols:
        print("There is not any Land Cover associated column in the dataframe; please revise")
    else:
        pass

    data_gdf_lc_sqkm_list = []
    data_gdf_lc_sqkm = {}

    for i in regions_list:
        data_gdf_lc_sqkm_name = 'data_gdf_LCsqkm_' + i
        data_gdf_lc_sqkm_list.append(data_gdf_lc_sqkm_name)
        data_gdf_lc_sqkm[data_gdf_lc_sqkm_name] = calc_lc_sqkm(regions_gdf[i], land_cover_cols)

    # new
    # Calculate summary statistics for other than land cover attribute columns
    data_gdf_stat = data_gdf_lc_sqkm

    # Define the conversion factor for CLEWs modelling
    # Potential yield unit conversion from kg DW/ha to million tonnes per 1000 sqkm
    factor1 = 0.0001

    # Other parameter unit conversion from millimeter to BCM per 1000 sqkm
    factor2 = 0.001

    for i in data_gdf_lc_sqkm_list:
        for col in data_gdf_stat[i].columns:

            if "yld" in col:
                data_gdf_stat[i].loc[:, col] *= factor1
            elif "evt" in col:
                data_gdf_stat[i].loc[:, col] *= factor2
            elif "prc" in col:
                data_gdf_stat[i].loc[:, col] *= factor2
            elif "cwd" in col:
                data_gdf_stat[i].loc[:, col] *= factor2
        final_list_of_cols = list(data_gdf_stat[i].columns)

    sum_cols = [x for x in final_list_of_cols if x not in origin_list_of_cols]
    sum_cols = [x for x in sum_cols if x not in land_cover_cols]
    sum_cols.remove("id")
    sum_cols.remove("LC_sum")

    group_lc = {}

    summary_stats_path = f"{OUTPUT_DATA_PATH}/{scenario}/summary_stats"
    for key, gdf in data_gdf_stat.items():
        # Group by 'clusters_yield'
        clusters = gdf.groupby(['clusters_yield'])
        clusters_lc = clusters[land_cover_cols].sum().merge(clusters["sqkm"].sum().reset_index(name="sqkm"),
                                                           on="clusters_yield").round(decimals=1)
        clusters_lc = clusters_lc.sort_values(ascending=True, by='clusters_yield').reset_index(drop=True)
        name = key[-3:]

        # Export land cover stats to csv
        clusters_lc.to_csv(os.path.join(summary_stats_path, "{}_LandCover_byCluster_summary.csv".format(name)),
                           index_label='cluster')

        # Display summary statistics
        print('#### Cluster summary statistics for area and land cover in {}'.format(name))
        print(' **Total area:** {:0.1f} sq.km'.format(clusters_lc.sqkm.sum()))
        print(clusters_lc)

        # Store the result in the group_dic dictionary
        group_lc[key] = clusters_lc

    group_stat = {}
    for key, gdf in data_gdf_stat.items():
        # Group by 'clusters_yield'
        clusters = gdf.groupby(['clusters_yield'])

        clusters_stat = clusters[sum_cols].mean().round(decimals=4)

        additional_crop_stat_group = [col for col in clusters_stat.columns if any(a in col for a in other_crop_name)]
        additional_stat_table_group = clusters_stat.loc[:, additional_crop_stat_group].copy()
        clusters_stat = clusters_stat.drop(additional_stat_table_group, axis=1)

        additional_stat_group('yld')
        additional_stat_group('cwd')
        additional_stat_group('evt')

        name = key[-3:]

        print('#### Cluster summary statistics for other variables in {}'.format(name))
        print(clusters_stat)

        group_stat[key] = clusters_stat

    for key, gdf in group_stat.items():
        clusters_other = gdf

        name = key[-3:]

        # generating the crop potential yeild csv files
        yld_columns = [col for col in clusters_other.columns if 'yld' in col]
        yld_df = clusters_other[yld_columns]

        # Name correction according clewsy format
        yld_rename = {col: col.replace(' yld', '').replace('_mean', '') for col in yld_df.columns}
        yld_df = yld_df.rename(columns=yld_rename)
        empty_yld = pd.DataFrame(columns=['', '', '', '', '', '', '', '', ''], index=yld_df.index)
        combined_yld = pd.concat([empty_yld, yld_df], axis=1)

        # Store as CSV file
        combined_yld.to_csv(os.path.join(summary_stats_path, "clustering_results_{}.csv".format(name)), index=True,
                            index_label='cluster')

        # generating crop evapotranspiration csv files
        evt_columns = [col for col in clusters_other.columns if 'evt' in col]
        evt_df = clusters_other[evt_columns]

        # Name correction
        evt_rename = {col: col.replace(' evt', '').replace('_mean', '') for col in evt_df.columns}
        evt_df = evt_df.rename(columns=evt_rename)
        empty_evt = pd.DataFrame(columns=['', '', '', '', '', '', '', '', ''], index=evt_df.index)
        combined_evt = pd.concat([empty_evt, evt_df], axis=1)

        combined_evt.to_csv(os.path.join(summary_stats_path, "clustering_results_evt_{}.csv".format(name)), index=True,
                            index_label='cluster')

        # generating crop water deficit csv files
        cwd_columns = [col for col in clusters_other.columns if 'cwd' in col]
        cwd_df = clusters_other[cwd_columns]

        # Name correction
        cwd_rename = {col: col.replace(' cwd', '').replace('_mean', '') for col in cwd_df.columns}
        cwd_df = cwd_df.rename(columns=cwd_rename)
        empty_cwd = pd.DataFrame(columns=['', '', '', '', '', '', '', '', ''], index=cwd_df.index)
        combined_cwd = pd.concat([empty_cwd, cwd_df], axis=1)

        combined_cwd.to_csv(os.path.join(summary_stats_path, "clustering_results_cwd_{}.csv".format(name)), index=True,
                            index_label='cluster')

        # generating precipitation csv files
        prc_columns = [col for col in clusters_other.columns if 'prc' in col]
        prc_df = clusters_other[prc_columns]

        prc_rename = {col: col.replace(' prc', '').replace('_mean', '') for col in prc_df.columns}
        prc_df = prc_df.rename(columns=prc_rename)

        prc_df.to_csv(os.path.join(summary_stats_path, "clustering_results_prc_{}.csv".format(name)), index=True,
                      index_label='cluster')

        # Export summary stats to csv
        clusters_other.to_csv(os.path.join(summary_stats_path, "{}_Parameter_byCluster_summary.csv".format(name)))

        print("Part 6 - and with that the analysis - completed!")
