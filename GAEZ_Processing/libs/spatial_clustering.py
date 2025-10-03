import geopandas as gpd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
import os
import warnings
import pandas as pd

from libs.constants import OUTPUT_DATA_PATH


def prepare_data_for_clustering(input_data):
    scenario = input_data['scenario']
    country_name = input_data['country_name']
    admin_level = input_data['admin_level']
    n_clusters = input_data['number_of_clusters']
    os.environ["OMP_NUM_THREADS"] = "1"

    # Generating Dendrogram
    def generate_dendrogram(df, name):
        linkage_matrix_normalized = linkage(df.values, method='ward', metric='euclidean')
        dendrogram(linkage_matrix_normalized)
        plt.title('Dendrogram ' + name)
        out_path = f"{OUTPUT_DATA_PATH}/{scenario}/dendrogram_graph"
        file_path = os.path.join(out_path, name + "_" + "{}_Dendrogram_Yield".format(country_name))
        plt.savefig(file_path)
        plt.close()

    # Elbow Method
    def generate_elbow_graph(df, name):
        wcss = []  # Initialize a list to store the within-cluster sum of squares
        out_path = f"{OUTPUT_DATA_PATH}/{scenario}/elbow_graph"
        for k in range(1, 10):  # Initial numbers of clusters to calculate WCSS
            kmeans = KMeans(n_clusters=k, random_state=0, n_init='auto')
            kmeans.fit(df)
            wcss.append(kmeans.inertia_)  # Calculate WCSS for each k

        # Plot the elbow graph values to identify the elbow point (optimum number of clusters)
        plt.figure(figsize=(8, 10))
        plt.plot(range(1, 10), wcss, marker='o', linestyle='-', color='b')
        plt.title('Elbow Graph for Optimal Number of Clusters ' + name)
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('WCSS')
        plt.grid()

        file_path = os.path.join(out_path, name + "_" + "{}_elbow_Yield".format(country_name))
        plt.savefig(file_path)
        plt.close()

    def agglomerative_clustering(gdf, df, n_clusters, name):
        agglo_clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
        gdf['clusters_yield'] = agglo_clustering.fit_predict(df)
        # Adjust cluster numbers to start from 1
        gdf['clusters_yield'] += 1

        out_path = f"{OUTPUT_DATA_PATH}/{scenario}/spatial_clustering"
        gdf.plot(column='clusters_yield', cmap='viridis', legend=True)
        plt.title('Clustered yield ' + name)
        file_path_new = os.path.join(out_path, name + "_" + "{}_Clustered_Yield.png".format(country_name))
        plt.savefig(file_path_new)
        plt.close()

        gdf.to_file(os.path.join(out_path, name + "_" + "{}_clustered_data.gpkg".format(country_name)),
                    driver="GPKG")
        gdf.to_csv(os.path.join(out_path, name + "_" + "{}_clustered_data.csv".format(country_name)))


    land_cells = gpd.read_file(
        f"{OUTPUT_DATA_PATH}/{scenario}/{country_name}_vector_admin{admin_level}_land_cells_with_attributes.gpkg")
    regions = list(land_cells['cluster'].unique())
    print(f'List of regions:{regions}')
    # For every regional cluster, create an individual gdf according to the administrative border level.

    regions_gdf = {}
    regions_list = []

    for i in regions:
        region_name = 'region_' + i
        regions_list.append(region_name)
        regions_gdf[region_name] = land_cells.loc[land_cells['cluster'] == i]

    # Normalizing GeoDataFrame
    clusters = land_cells
    columns_yld = [col for col in clusters.columns if "yld" in col]
    regions_normalized_list = []
    regions_normalized_gdf = {}

    for i in regions_list:
        region_normalized_name = 'normalized_' + i
        regions_normalized_list.append(region_normalized_name)
        regions_normalized_gdf[region_normalized_name] = regions_gdf[i][columns_yld]

    for i in regions_normalized_list:
        for col in regions_normalized_gdf[i].columns:
            min_value = min(regions_normalized_gdf[i].loc[:, col])
            max_value = max(regions_normalized_gdf[i].loc[:, col])
            regions_normalized_gdf[i].loc[:, col] = (regions_normalized_gdf[i].loc[:, col] - min_value) / (
                        max_value - min_value)

    for i in regions_normalized_list:
        regions_normalized_gdf[i].fillna(0, inplace=True)

    # Generate dendrogram
    for i in regions_normalized_list:
        generate_dendrogram(regions_normalized_gdf[i], i)

    # generate elbow graph for each region
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)

        for i in regions_normalized_list:
            generate_elbow_graph(regions_normalized_gdf[i], i)

    for i in regions_normalized_list:
        region = i.split('_')[-1]
        # Use the user shapefile or the default value
        number_cluster = n_clusters[region]

        for j in regions_list:
            if j in i:
                # Perform agglomerative hierarchical clustering
                agglomerative_clustering(regions_gdf[j], regions_normalized_gdf[i], number_cluster, j)
    regions_info = {
        'regions_list': regions_list,
        'regions_gdf': regions_gdf
    }
    return land_cells, regions_info
