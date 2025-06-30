"""Module for reading in data sources"""

# Numerical
import pandas as pd
import requests
import os
import shutil as sh
from libs.constants import GLOBAL_RASTER_PATH, INPUT_DATA_PATH, INTERIM_DATA_PATH


def retrieve_top_10_crops(input_data):
    country_full_name = input_data["geographic_scope"]
    # Read the FAOSTAT file
    data = pd.read_csv('./Data/FAOSTAT_2020.csv')
    filtered_data = data[data['Area'] == country_full_name]

    # Sorting based on the harvested area in descending order and get top 10 rows
    # Retrieve data according to the user-defined country
    top_10_values = filtered_data.nlargest(10, 'Value')
    all_crops = top_10_values['Item'].tolist()

    main_crops = all_crops[:5]
    other_crops = all_crops[5:]

    print(f"Top 5 crops considering harvested area are: {main_crops}")
    print(f"Crops ranked from six to ten in the top 10 FAO dataset are: {other_crops}")
    return main_crops, other_crops


def standardize_faostat(main_crops, other_crops):
    crop_code = pd.read_csv('./Data/Crop_code.csv')
    # FAO correction: 3 letter naming convention per crop considering CLEWs naming format
    crop_name = []
    for item in main_crops:
        matching_rows = crop_code[crop_code['Name'] == item]

        if not matching_rows.empty:
            crop_name.extend(matching_rows['Code'].tolist())

    other_crop_name = []

    for item in other_crops:
        matching_rows = crop_code[crop_code['Name'] == item]

        if not matching_rows.empty:
            other_crop_name.extend(matching_rows['Code'].tolist())

    # Adding "prc" refering to annual precipitation
    crop_name.append('prc')
    print(f"Based on 3-letter names, the main crops list from the FAOSTAT is: {crop_name}")
    print(f"Based on 3-letter names, the additional crops list from the FAOSTAT is: {other_crop_name}")
    return crop_name, other_crop_name, crop_code


def gaez_naming(dataset, filename, crop_code):
    dataset['New Crop'] = dataset['Crop'].apply(
        lambda x: crop_code.loc[crop_code['GAEZ_name'] == x, 'Code'].values[0] if x in crop_code[
            'GAEZ_name'].values else 'Nan')
    dataset.to_csv(f"{INTERIM_DATA_PATH}/{filename}", index=False)


def gaez_listing(dataframe, crop_list, column):
    result = pd.DataFrame()
    for crop in crop_list:
        if dataframe[column].str.contains(crop).any():
            result = pd.concat([result, dataframe[dataframe[column].str.contains(crop)]])
    return result


def download_url(dataframe, column, folder_name):
    for index, row in dataframe.iterrows():
        url = str(row[column])
        filename = str(row['New Crop']) + ' ' + ('cwd' if str(row['Name'].split('_')[-1]) == "wde" else 'evt' if str(
            row['Name'].split('_')[-1]) == "eta" else str(row['Name'].split('_')[-1])) + ' ' + str(
            row['New Water Supply']) + ' ' + str(row['Input Level'])
        file_path = os.path.join(folder_name, filename + '.tif')

        response = requests.get(url)

        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(f"Downloaded: {filename}")


def process_gaez_data(crop_name, other_crop_name, crop_code, input_data):
    rcp = input_data["rcp"]
    # GAEZ data list - potential yield, water deficit, evapotranspiration
    gaez_data = ['yld', 'cwd', 'evt']
    gaez_df = {}
    for item in gaez_data:
        high_input = pd.read_csv(f'{INPUT_DATA_PATH}/GAEZ_{item}_High_Input.csv')
        low_input = pd.read_csv(f'{INPUT_DATA_PATH}/GAEZ_{item}_Low_Input.csv')

        # Add a new column for water supply for each datum
        high_input['New Water Supply'] = high_input['Water Supply'].apply(
            lambda x: 'Irrigation' if 'irrigation' in x else 'Rain-fed')
        low_input['New Water Supply'] = low_input['Water Supply'].apply(
            lambda x: 'Irrigation' if 'irrigation' in x else 'Rain-fed')

        # Change namings
        gaez_naming(high_input, f'New_{item}_High_input.csv', crop_code)
        gaez_naming(low_input, f'New_{item}_Low_input.csv', crop_code)

        # Filter in accordance with user-defined RCP
        filtered_high_input = high_input[high_input["RCP"] == rcp]

        main_high = gaez_listing(filtered_high_input, crop_name, "New Crop")
        other_high = gaez_listing(filtered_high_input, other_crop_name, "New Crop")
        main_low = gaez_listing(low_input, crop_name, "New Crop")
        other_low = gaez_listing(low_input, other_crop_name, "New Crop")
        gaez_df[item] = [main_high, other_high, main_low, other_low]
        download_url(main_high, "Download URL", GLOBAL_RASTER_PATH)
        download_url(other_high, "Download URL", GLOBAL_RASTER_PATH)
        download_url(main_low, "Download URL", GLOBAL_RASTER_PATH)
        download_url(other_low, "Download URL", GLOBAL_RASTER_PATH)
    sh.copyfile(f'{INPUT_DATA_PATH}/precipitation prc.tif', f'{GLOBAL_RASTER_PATH}/precipitation prc.tif')
    sh.copyfile(f'{INPUT_DATA_PATH}/LCType_ncb.tif', f'{GLOBAL_RASTER_PATH}/LCType_ncb.tif')

