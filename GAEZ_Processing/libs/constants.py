import yaml
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
USER_INPUTS_PATH = f"{ROOT_DIR}/user_input"
with open(f"{USER_INPUTS_PATH}/config.yaml", "r") as input_file:
    all_input_data = yaml.load(input_file, Loader=yaml.FullLoader)
scenario_name = all_input_data["scenario"]
GLOBAL_RASTER_PATH = f"{ROOT_DIR}/Data/interim_output/{scenario_name}/global_raster_input"
CROPPED_RASTER_PATH = f"{ROOT_DIR}/Data/interim_output/{scenario_name}/cropped_raster_input"
INPUT_DATA_PATH = f"{ROOT_DIR}/Data/input"
OUTPUT_DATA_PATH = f"{ROOT_DIR}/Data/output"
INTERIM_DATA_PATH = f"{ROOT_DIR}/Data/interim_output/{scenario_name}"
SHAPEFILE_PATH = f"{ROOT_DIR}/user_input/shapefile"
