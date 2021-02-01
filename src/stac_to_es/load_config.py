import json
from pathlib import Path


with open(Path(__file__).parent / "config.json") as json_data_file:
    config = json.load(json_data_file)

es_index_settings = config['es_index_settings']
stac_excluded_keys = list(config['stac_excluded_keys'])
