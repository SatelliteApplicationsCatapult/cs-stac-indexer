import logging
import os
from pathlib import Path
from typing import Tuple

import requests
from requests import HTTPError
from stac_to_dc.config import LOG_LEVEL, LOG_FORMAT
from stac_to_dc.util import load_json

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

logger = logging.getLogger(__name__)


def guess_location(metadata: dict) -> Tuple[str, bool]:
    self_link = None
    asset_link = None
    relative = True

    for link in metadata.get("links"):
        rel = link.get("rel")
        if rel and rel == "self":
            self_link = link.get("href")

    if metadata.get("assets"):
        for asset in metadata["assets"].values():
            if asset.get("type") in [
                "image/tiff; application=geotiff; profile=cloud-optimized",
                "image/tiff; application=geotiff",
            ]:
                asset_link = os.path.dirname(asset["href"])

    # If the metadata and the document are not on the same path,
    # we need to use absolute links and not relative ones.
    if (self_link and asset_link) and os.path.dirname(self_link) != os.path.dirname(
            asset_link
    ):
        relative = False

    return self_link, relative


def get_item(stac_item: str) -> Tuple[dict, str, bool]:
    metadata = load_json(stac_item)
    uri, relative = guess_location(metadata)
    return metadata, uri, relative


def get_collection_url(stac_item: str) -> str:
    metadata = load_json(stac_item)
    for link in metadata.get("links"):
        rel = link.get("rel")
        if rel and rel == "collection":
            return str((Path(stac_item).parent / link.get("href")).resolve())


def get_product_definition(collection_url: str) -> dict:
    collection = None
    product_definition = None

    if 'http' in collection_url:
        try:
            response = requests.get(collection_url)
            response.raise_for_status()
        except HTTPError as http_err:
            logger.error(f'HTTP error occurred: {http_err}')
        except Exception as err:
            logger.error(f'Other error occurred: {err}')
        else:
            collection = response.json()
    else:
        collection = load_json(collection_url)

    if collection and "product_definition" in collection.get("stac_extensions"):
        product_definition = {
            "name": collection.get("properties").get("product_definition:metadata").get("product").get("name"),
            "description": collection.get("description"),
        }
        for k, v in collection.get("properties").items():
            if "product_definition:" in k:
                product_definition[k.split(':')[1]] = v

    return product_definition
