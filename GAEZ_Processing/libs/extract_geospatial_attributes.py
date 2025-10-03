import rasterio
from rasterstats import zonal_stats
from rasterio.mask import mask
import datetime
import geopandas as gpd
import json
import os

from libs.constants import GLOBAL_RASTER_PATH, CROPPED_RASTER_PATH, OUTPUT_DATA_PATH, INPUT_DATA_PATH


# Processing Continuous/Numerical Rasters
def processing_raster_con(path, raster, prefix, method, land_cells):
    """
    This function calculates stats for numerical rasters and attributes them to the given vector features.

    INPUT:
    name: string used as prefix when assigning features to the vectors
    method: statistical method to be used (check documentation)
    land_cells: the vector layer containing the land cells

    OUTPUT:
    geojson file of the vector features including the new attributes
    """

    raster = rasterio.open(path + '/' + raster)

    land_cells = zonal_stats(
        land_cells,
        raster.name,
        stats=[method],
        prefix=prefix, geojson_out=True, all_touched=True)

    print("{} processing completed at".format(prefix), datetime.datetime.now())
    return land_cells


# Processing Categorical/Discrete Rasters
def processing_raster_cat(path, raster, prefix, land_cells):
    """
    This function calculates stats for categorical rasters and attributes them to the given vector features.

    INPUT:
    path: the directory where the raster layer is stored
    raster: the name and extention of the raster layer
    prefix: string used as prefix when assigning features to the vectors
    land_cells: the vector layer containing the land cells

    OUTPUT:
    geojson file of the vector features including the new attributes
    """
    raster = rasterio.open(path + '/' + raster)

    land_cells = zonal_stats(
        land_cells,
        raster.name,
        categorical=True,
        prefix=prefix, geojson_out=True, all_touched=True)

    print("{} processing completed at".format(prefix), datetime.datetime.now())
    return land_cells


## Converting geojson to GeoDataFrame
def geojson_to_gdf(workspace, geojson_file):
    """
    This function returns a GeoDataFrame for a given geojson file

    INPUT:
    workplace: working directory
    geojson_file: geojson layer to be convertes
    crs: projection system in epsg format (e.g. 'EPSG:21037')

    OUTPUT:
    GeoDataFrame
    """
    output = workspace + r'/placeholder.geojson'
    with open(output, "w") as dst:
        collection = {
            "type": "FeatureCollection",
            "features": list(geojson_file)}
        dst.write(json.dumps(collection))

    land_cells = gpd.read_file(output)
    os.remove(output)

    print("cluster created a new at", datetime.datetime.now())
    return land_cells


def clip_raster_file(admin, input_data):
    crs_wgs = input_data['crs_WGS84']
    admin = admin.to_crs(crs_wgs)
    for i in os.listdir(GLOBAL_RASTER_PATH):
        with rasterio.open(os.path.join(GLOBAL_RASTER_PATH, i)) as src:
            # Get the admin's CRS
            admin_crs = admin.crs

            # Get the geometry of the admin
            admin_geom = admin.geometry.values[0]

            # Crop the raster based on the admin's geometry
            out_image, out_transform = mask(src, [admin_geom], crop=True)

            # Update the metadata of the cropped raster
            out_meta = src.meta.copy()
            out_meta.update({
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform,
                "crs": admin_crs
            })

            # Write the cropped raster to the output directory
            out_path_tif_crop = os.path.join(CROPPED_RASTER_PATH, i)
            with rasterio.open(out_path_tif_crop, "w", **out_meta) as dest:
                dest.write(out_image)


def collect_raster_files():
    # Read files with tif extension and assign their name into two list for discrete and continuous datasets
    raster_files_dis = []
    raster_files_con = []
    total_raster_files = os.listdir(CROPPED_RASTER_PATH)
    for i in total_raster_files:
        if ("ncb" in i) and i.endswith('.tif'):
            with rasterio.open(CROPPED_RASTER_PATH + '/' + i) as src:
                raster_files_dis.append(i)
        elif i.endswith('.tif'):
            with rasterio.open(CROPPED_RASTER_PATH + '/' + i) as src:
                data = src.read()
                raster_files_con.append(i)

    # keep only unique values -- Not needed but just in case there are dublicates
    raster_files_con = list(set(raster_files_con))
    raster_files_dis = list(set(raster_files_dis))

    print(f"We have identified {len(raster_files_con)} continuous raster(s):")
    for raster in raster_files_con:
        print("*", raster)

    print(f"We have identified {len(raster_files_dis)} discrete raster(s):")
    for raster in raster_files_dis:
        print("*", raster)

    return raster_files_con, raster_files_dis


def extract_raster_values(input_data, raster_files_con, raster_files_dis):
    scenario = input_data['scenario']
    country_name = input_data['country_name']
    admin_level = input_data['admin_level']
    land_cells = gpd.read_file(f"{OUTPUT_DATA_PATH}/{scenario}/{country_name}_vector_admin{admin_level}_land_cells.gpkg")

    for raster in raster_files_con:
        prefix = raster.rstrip(".tif")
        prefix = prefix + "_"

        # Calling the extraction function for continuous layers
        land_cells = processing_raster_con(CROPPED_RASTER_PATH, raster, prefix, "mean", land_cells)

    for raster in raster_files_dis:
        prefix = raster.rstrip(".tif")
        prefix = prefix.rstrip('_ncb')

        # Calling the extraction function for discrete layers
        land_cells = processing_raster_cat(CROPPED_RASTER_PATH, raster, prefix, land_cells)

    land_cells = geojson_to_gdf(f"{OUTPUT_DATA_PATH}/{scenario}", land_cells)
    # Export as csv
    land_cells.to_csv(
        f"{OUTPUT_DATA_PATH}/{scenario}/{country_name}_vector_admin{admin_level}_land_cells_with_attributes.csv")
    land_cells.to_file(
        f"{OUTPUT_DATA_PATH}/{scenario}/{country_name}_vector_admin{admin_level}_land_cells_with_attributes.gpkg",
        driver="GPKG")
