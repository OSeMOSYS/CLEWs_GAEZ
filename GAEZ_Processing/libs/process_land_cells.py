# Numerical
import numpy as np

# Spatial
import geopandas as gpd

#Plotting
import matplotlib.pyplot as plt

from libs.constants import USER_INPUTS_PATH, OUTPUT_DATA_PATH, SHAPEFILE_PATH


def read_shapefiles(input_data):
    country_name = input_data['country_name']
    admin_level = input_data['admin_level']
    crs_w = input_data['crs_WGS84']
    shp_file_path = f"{SHAPEFILE_PATH}/gadm41_{country_name}"
    shapefile = gpd.read_file(shp_file_path + f"_{admin_level}.shp")
    shapefile.to_crs(crs_w, inplace=True)
    admin = gpd.read_file(shp_file_path + "_0.shp")
    admin.to_crs(crs_w, inplace=True)
    return shapefile, admin


def generate_georeference(shapefile, input_data):
    scenario = input_data['scenario']
    country_name = input_data['country_name']
    # Create point grid
    spacing = 0.09
    xmin, ymin, xmax, ymax = shapefile.total_bounds
    xcoords = [i for i in np.arange(xmin, xmax, spacing)]
    ycoords = [i for i in np.arange(ymin, ymax, spacing)]

    pointcoords = np.array(np.meshgrid(xcoords, ycoords)).T.reshape(-1, 2)
    points = gpd.points_from_xy(x=pointcoords[:, 0], y=pointcoords[:, 1])
    grid = gpd.GeoSeries(points, crs=shapefile.crs)
    grid.name = 'geometry'

    # only points inside administrative boundary:
    gridinside = gpd.sjoin(gpd.GeoDataFrame(grid), shapefile[['geometry']], how="inner")

    # Plot georeferenced point grid
    fig, ax = plt.subplots(figsize=(20, 20))
    shapefile.plot(ax=ax, alpha=0.7, color="pink", edgecolor='red', linewidth=3)
    grid.plot(ax=ax, markersize=30, color="blue")
    gridinside.plot(ax=ax, markersize=15, color="yellow")
    # file_path = os.path.join(out_path, "{}_PointGrid.png".format(country_name))
    file_path = f"{OUTPUT_DATA_PATH}/{scenario}/{country_name}_PointGrid.png"
    plt.savefig(file_path)
    return gridinside


def convert_points_to_polygons(shapefile, clustered_gdf, input_data):
    crs_w = input_data['crs_WGS84']
    admin_level = input_data['admin_level']
    aggregate = input_data['aggregate']
    aggregate_region = input_data['aggregate_region']
    # Calculate the centroids
    clustered_gdf = clustered_gdf.to_crs(crs_w)

    # Rename the columns to cluster
    clustered_gdf.rename(columns={'index_right': 'cluster'}, inplace=True)

    # Convert cluster column to string
    clustered_gdf.cluster = clustered_gdf.cluster.astype(str).replace('0', 'NaN')

    # Reset the index of the left dataframe
    clustered_gdf = clustered_gdf.reset_index(drop=True)
    admin_name = "NAME_" + str(admin_level)

    if admin_level == 0:
        # Perform the spatial join
        clustered_gdf = gpd.sjoin(clustered_gdf, shapefile[["geometry", "GID_0"]], predicate='within').drop(['cluster'],
                                                                                                     axis=1)

        # Rename the 'GID_0' column to 'cluster'
        clustered_gdf.rename(columns={'GID_0': 'cluster'}, inplace=True)
    else:
        # Perform the spatial join
        clustered_gdf = gpd.sjoin(clustered_gdf, shapefile[["geometry", admin_name]], predicate='within').drop(['cluster'],
                                                                                                        axis=1)

        # Rename the 'NAME_1' column to 'cluster'
        clustered_gdf.rename(columns={admin_name: 'cluster'}, inplace=True)

    # Print the first 5 rows of the joined GeoDataFrame
    print(clustered_gdf.head(3))

    # create a new column based on first 3 letters of the 'cluster' column
    clustered_gdf['new_cluster'] = clustered_gdf['cluster'].apply(lambda x: x[:3]).str.upper()
    clustered_gdf = clustered_gdf.rename(columns={'cluster': 'old_cluster'})
    clustered_gdf = clustered_gdf.rename(columns={'new_cluster': 'cluster'})
    clustered_gdf = clustered_gdf.drop(columns=['old_cluster'])
    print(clustered_gdf.head(3))

    # Aggregating subnational regions based on user-defined aggregation list. The aggregated land cells of regions are represented by the Grouped Region Cluster (GRC).
    if aggregate:
        clustered_gdf['cluster'] = clustered_gdf['cluster'].apply(lambda x: 'GRC' if x in aggregate_region else x)

    print(clustered_gdf.head(3))
    # Buffer value used should be half the distance between two adjacent points, which in turn is dependent on the location of the Area of Interest (AoI) on Earth and the projection system being used.
    buffer_value = 0.045
    # cap_style refers to the type of geometry generated; 3=square (see shapely documectation for more info -- https://shapely.readthedocs.io/en/stable/manual.html)

    clustered_gdf['geometry'] = clustered_gdf.apply(lambda x:
                                                    x.geometry.buffer(buffer_value, cap_style=3), axis=1)

    print(clustered_gdf.head(3))
    return clustered_gdf


def get_multiplier(estimated, official):
    if official == estimated:
        return 1
    try:
        return  official / estimated
    except ZeroDivisionError:
        return 0


def calibrate_area(admin, clustered_gdf, input_data):
    admin_level = input_data['admin_level']
    country_name = input_data['country_name']
    scenario = input_data['scenario']
    crs_w = input_data['crs_WGS84']
    crs_p = input_data['crs_proj']
    print(clustered_gdf.head(3))
    clustered_gdf_prj = clustered_gdf.to_crs(crs_p)
    clustered_gdf_prj["sqkm"] = clustered_gdf_prj["geometry"].area / 10 ** 6

    estimated_area = clustered_gdf_prj.sqkm.sum()
    admin.to_crs(crs_p, inplace=True)
    official_area = admin.geometry.area.sum() / 10 ** 6

    # Estimate column multipler
    multiplier = get_multiplier(estimated_area, official_area)

    clustered_gdf_prj.sqkm = clustered_gdf_prj.sqkm * multiplier

    print("Our modelling exercise yields a total area of {0:.1f} sqkm for the country".format(estimated_area))
    print("The admin layer indicates {0:.1f} sqkm".format(official_area))
    print("After calibration the total area is set at {0:.1f} sqkm".format(clustered_gdf_prj.sqkm.sum()))

    # Revert to original crs
    final_clustered_gdf = clustered_gdf_prj.to_crs(crs_w)
    print(final_clustered_gdf.head(3))

    final_clustered_gdf.to_file(f"{OUTPUT_DATA_PATH}/{scenario}/{country_name}_vector_admin{admin_level}_land_cells.gpkg",
                                driver="GPKG")
