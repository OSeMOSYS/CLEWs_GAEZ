Introduction
=====================================

GeoCLEWs offers an extensive set of beneficial features for developers and users to process high-resolution land and water data for Climate, Land, Energy, and Water systems modelling (CLEWs). This script automatically collects data from  GAEZ v4 (Global Agro-Ecological Zones version 4) and FAOSTAT (Food and Agriculture Organization of the United Nations). GeoCLEWs performs processing and calibration of agro-climatic potential yield, crop water deficit, crop evapotranspiration, precipitation, and land cover. Outputs can be efficiently combined with additional data for CLEWs modelling, such as electricity information, to create a detailed CLEWs model without implementing complicated and time-consuming spatial processing. Jupiter Notebook code provides a comprehensive and detailed explanation of the processing steps involved.



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
-	Download the shapefile admin level 0 containing the administrative boundary from the [GADM](https://gadm.org/download_country.html) or any other sources. The file should be placed inside the 'Data/input' directory and renamed to "..._ adm0" where "..." represents the 3-letter ISO [country code]( https://www.nationsonline.org/oneworld/country_code_list.htm). For instance, "KEN_adm0.shp" indicates the shapefile of the administrative boundary for the country of Kenya.
-	The second required shapefile for clustering can also be obtained from [GADM](https://gadm.org/download_country.html). Depending on the project specifications, the user can download either the admin level 0 or admin level 1 shapefile. The GAEZ data will be processed based on the admin level selected by the user. Please store the shapefile in the 'Data/input' folder and adhere to the “…_data” naming convention. Rename the files to match the 3-letter ISO [country code]( https://www.nationsonline.org/oneworld/country_code_list.htm) of your case study, such as naming the shapefile for Kenya as “KEN_data.shp”.


Note: Two shapefiles corresponding to the selected country need to be downloaded and placed inside the 'Data/input' folder.

Outputs
---------------------------------------------------
GeoCLEWs code produces tabular results in a CSV format which is compatible with clewsy for CLEWs modelling, along with interactive graphs. The GAEZ portal provides continuous raster data representing crop yields in kg DW/ha and crop water deficit, precipitation, and crop evapotranspiration in millimeter. Units presented in this analysis are recalculated based on the CLEWs framework, and therefore, the million tonnes per 1000 km² unit of measurement is used to quantify agro-climatic potential yield. Crop water deficit, crop evapotranspiration, and precipitation are calculated in BCM (billion cubic meters) per 1000 km². These units have been chosen to ensure consistency with the CLEWs methodology and facilitate comparability with other studies. The output of categorical land cover raster data is summarized in units of square kilometers. 


