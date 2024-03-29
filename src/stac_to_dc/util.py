import json
from typing import List, Tuple
from pathlib import Path
from urllib.parse import urlparse
from stac_to_dc.config import get_s3_configuration



def load_json(file: str) -> dict:
    with open(file) as json_file:
        return json.load(json_file)


def get_files_from_dir(directory: str, extension: str) -> List[str]:
    return [str(x.absolute()) for x in Path(directory).glob(f'**/*.{extension}')]


def parse_s3_url(url: str) -> Tuple[str, str]:
    return urlparse(url).path.split('/')[1], '/'.join(urlparse(url).path.split('/')[2:])


def get_rel_links(metadata: dict, rel: str) -> List[str]:
    return [link.get('href') for link in metadata.get('links') if link.get('rel') == rel]


def get_key_from_url(url: str) -> str:
    x = url.split('/')[3:]
    return '/'.join(x)