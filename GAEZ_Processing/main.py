"""Main file to execute GeoCLEWs"""

import pandas as pd
import errno
import os

import yaml

from libs.collect import process_gaez_data, retrieve_top_10_crops, standardize_faostat
from libs.process_land_cells import read_shapefiles, generate_georeference, convert_points_to_polygons, calibrate_area
from libs.extract_geospatial_attributes import clip_raster_file, extract_raster_values, collect_raster_files
from libs.spatial_clustering import prepare_data_for_clustering
from libs.calculation_cluster import calculate
from libs.constants import GLOBAL_RASTER_PATH, CROPPED_RASTER_PATH, OUTPUT_DATA_PATH, INTERIM_DATA_PATH, USER_INPUTS_PATH


def initialize_directories(input_data):
    scenario = input_data["scenario"]
    do = f"{OUTPUT_DATA_PATH}/{scenario}/"
    paths = ['Data/interim_output', GLOBAL_RASTER_PATH, CROPPED_RASTER_PATH, do, f'{do}summary_stats',
             f"{do}dendrogram_graph", f'{do}elbow_graph', f'{do}spatial_clustering']
    # Initialize output paths for data
    for output_path_raw in paths:
        output_path = f"{output_path_raw}"
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise


def main():
    # Read yaml file and prepare for the inputs
    with open(f"{USER_INPUTS_PATH}/config.yaml", "r") as f:
        input_data = yaml.load(f, Loader=yaml.FullLoader)
    # 3-letter ISO code of the selected country
    code = pd.read_csv(
        'Data/Country_code.csv')  # More info: https://www.nationsonline.org/oneworld/country_code_list.htm
    code_name = code[code['Full_name'] == input_data['geographic_scope']]
    input_data['country_name'] = code_name.iloc[0]['country_code']

    # execute functions
    initialize_directories(input_data)

    main_crops, other_crops = retrieve_top_10_crops(input_data)
    crop_name, other_crop_name, crop_code = standardize_faostat(main_crops, other_crops)
    process_gaez_data(crop_name, other_crop_name, crop_code, input_data)
    shapefile, admin = read_shapefiles(input_data)
    grid_points = generate_georeference(shapefile, input_data)
    gdf_clustered = convert_points_to_polygons(shapefile, grid_points, input_data)
    calibrate_area(admin, gdf_clustered, input_data)
    clip_raster_file(admin, input_data)
    raster_files_con, raster_files_dis = collect_raster_files()
    extract_raster_values(input_data, raster_files_con, raster_files_dis)
    land_cells, regions_info = prepare_data_for_clustering(input_data)
    calculate(land_cells, other_crop_name, regions_info, input_data)


if __name__ == "__main__":
    main()
