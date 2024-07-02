Introduction
=====================================

GeoCLEWs offers an extensive set of beneficial features for developers and users to process high-resolution land and water data for Climate, Land, Energy, and Water systems (CLEWs) modelling. This tool provides:
- Detailed representation of land and water systems using high-resolution Global Agro-Ecological Zones ([GAEZ v4](https://gaez.fao.org/)) datasets and Food and Agriculture Organization of the United Nations (FAOSTAT), facilitating the development of CLEWs models in a clewsy-compatible format.
- Implementation of customized geographical aggregation and Agglomerative Hierarchical clustering to capture cross-regional interdependencies and streamline computational complexity.
- Automation of data collection, preparation, processing, and result generation across arbitrary geographical regions, reducing manual effort and minimizing errors in WEF assessments.
- Integration of agro-climatic data for additional crops and scalability in aggregating administrative regions.
- Promotion of sustainable collaboration through the use of open-source tools and datasets. GeoCLEWs is openly licensed under the MIT License, providing transparent, self-descriptive, and reproducible scripts and essential supplementary documents to encourage user contributions.

GeoCLEWs performs processing and calibration of agro-climatic potential yield, crop water deficit, crop evapotranspiration, precipitation, and land cover. Outputs can be efficiently combined with additional data for CLEWs modelling, such as electricity information, to create a detailed CLEWs model without implementing complicated and time-consuming spatial processing. Jupiter Notebook code provides a comprehensive and detailed explanation of the processing steps involved.

Note: GeoCLEWs has been successfully tested and verified on Windows machines. However, there may be incompatibility issues with other operating systems due to differences in Python packages or their versions. 

Contributors:
------------------------------------------------
**[Yalda Saedi](https://github.com/Ysaedi)** - Developer<br />
**[Taco Niet](https://github.com/tniet)** - Supervisor<br />


Release Notes
------------------------------------------------
### Version 2.0.0 (July 2024):

- **Spatial Clustering**: Implements spatial clustering to capture cross-regional interdependencies and reduce computational complexity.
- **Optimal Clusters Identification**: Generates dendrograms and elbow graphs to identify the optimal number of spatial clusters.
- **Cluster Classification**: Classifies regions into clusters based on agro-climatic potential yield patterns and soil suitability.
- **CLEWs-Compatible Outputs**: Generates CSV files for individual clusters in each region, providing statistics on land cover, precipitation, crop potential yield, water deficit, and evapotranspiration.


### Version 1.0.0 (December 2023):
- **Crop Identification**: Identifies primary crops using FAOSTAT data, including agro-ecological stats for five additional crops.
- **GAEZ Data Collection**: Automates data extraction and preprocessing from GAEZ datasets.
- **Land Cell Generation**: Generates georeferenced land cells adaptable to any geographical boundary.
- **Spatial Attributes Extraction**: Integrates high resolution agro-ecological attributes into land cells.
- **Geographical Aggregation**: Aggregates administrative regions to reduce CLEWs modelling computation.
- **CLEWs-Compatible Outputs**: Provides tabular outputs and interactive graphs.

Creating and Activating the Environment
------------------------------------------------
Please ensure that you install all the necessary Python packages and their dependencies for the smooth functioning of the script. An environment YAML file, 'environment.yml', is provided to facilitate reproducing of the Python environment and avoid any potential version conflicts. 
To set up the environment, run the following command:


    conda env create -f environment.yml
    conda activate GeoCLEWs

Download Files and Data
--------------------------------------------------
GeoCLEWs with its adaptable design allows for running with any arbitrary shape and incorporating the geospatial characteristics of any geographical region. Additionally, users have the option to utilize the open-source [GADM](https://gadm.org/download_country.html) dataset , which provides various levels of administrative boundaries for all countries. With this flexibility, users can seamlessly tailor the analysis to their specific needs and explore a wide range of geospatial data. It is essential to make sure to follow the same naming format as provided in the examples.
-	The 'GAEZ_Processing' folder includes the Jupyter Notebook code (GeoCLEWs.ipynb), required GAEZ and FAOSTAT resources in CSV format, and the 'Data' folder corresponding to the input and output data. Please ensure that all files within the 'GAEZ_Processing' folder are placed in the same directory in your local machine for seamless execution of the GeoCLEWs code.
-	Download the shapefile for administrative boundary at level 0 from the [GADM](https://gadm.org/download_country.html) or any other sources. Place the file inside the 'Data/input' directory and rename it to "..._ adm0" where "..." represents the 3-letter ISO [country code]( https://www.nationsonline.org/oneworld/country_code_list.htm). For instance, "KEN_adm0.shp" indicates the shapefile for the administrative boundary of Kenya. Admin level 0 is essential to include in all projects as it provides the outer boundary of the region.

Please note: Ensure that all necessary files, such as .shx, .shp, etc., are included. For example, for Kenya, you’ll need to input the following files: KEN_adm0.gpkg, KEN_adm0.prj, KEN_adm0.shp, KEN_adm0.shx, and so on.	
-	The second required shapefile for clustering can also be obtained from [GADM](https://gadm.org/download_country.html). Depending on the project specifications, users can download either the administrative level 0 or higher. The GAEZ data will be processed based on the admin level selected by the user in this step. Please store the shapefile in the 'Data/input' folder and adhere to the “…_data” naming convention. Rename the files to match the 3-letter ISO [country code]( https://www.nationsonline.org/oneworld/country_code_list.htm) of your case study, such as naming the shapefile for Kenya as “KEN_data.shp”.

Please make sure that all required files, such as .shx, .shp, and others, are included. For instance, for Kenya, you'll need to input files like KEN_data.gpkg, KEN_data.prj, KEN_data.shp, KEN_data.shx, and so forth.


Note: Two datasets (two collections of shapefiles including "..._ adm0" and “…_data”) corresponding to the selected country need to be downloaded and placed inside the 'Data/input' folder. If processing at administrative level 0, the same dataset with different naming formats should be used and placed together in the same directory.

Outputs
---------------------------------------------------
GeoCLEWs code produces tabular results in a CSV format which is compatible with clewsy for CLEWs modelling, along with interactive graphs. The GAEZ portal provides continuous raster data representing crop yields in kg DW/ha and crop water deficit, precipitation, and crop evapotranspiration in millimeter. Units presented in this analysis are recalculated based on the CLEWs framework, and therefore, the million tonnes per 1000 km² unit of measurement is used to quantify agro-climatic potential yield. Crop water deficit, crop evapotranspiration, and precipitation are calculated in BCM (billion cubic meters) per 1000 km². These units have been chosen to ensure consistency with the CLEWs methodology and facilitate comparability with other studies. The output of categorical land cover raster data is summarized in units of square kilometers. 

Contact
-----------------------------------------
For any inquiries, please contact [Yalda Saedi](https://www.linkedin.com/in/yalda-saedi/).

