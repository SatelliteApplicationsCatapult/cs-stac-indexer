import json
from typing import List
from pathlib import Path


def load_json(file: str) -> dict:
    with open(file) as json_file:
        return json.load(json_file)


def get_files_from_dir(directory: str, extension: str) -> List[str]:
    return [str(x.absolute()) for x in Path(directory).glob(f'**/*.{extension}')]
