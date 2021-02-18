import json
from typing import List, Tuple
from pathlib import Path
from urllib.parse import urlparse


def load_json(file: str) -> dict:
    with open(file) as json_file:
        return json.load(json_file)


def get_files_from_dir(directory: str, extension: str) -> List[str]:
    return [str(x.absolute()) for x in Path(directory).glob(f'**/*.{extension}')]


def parse_s3_link(link: str) -> Tuple[str, str]:
    return urlparse(link).path.split('/')[1], '/'.join(urlparse(link).path.split('/')[2:])


def get_rel_links(metadata: dict, rel: str) -> List[str]:
    return [link.get('href') for link in metadata.get('links') if link.get('rel') == rel]
