import os
from pathlib import Path
from typing import Tuple

from datacube import index, model

from stac_to_dc.util import load_json


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
            return str((Path(stac_item).parent / link.get("href")).absolute())


def get_product_definition(collection_url: str) -> dict:
    collection = load_json(collection_url)
    if collection.get("product_definition"):
        product_definition = {
            "name": collection.get("id"),
            "description": collection.get("description"),
            "metadata_type": collection.get("product_definition").get("metadata_type"),
            "metadata": collection.get("product_definition").get("metadata"),
            "measurements": collection.get("product_definition").get("measurements")
        }

        return product_definition


def create_product(dc_index: index.Index, product_definition: dict) -> model.DatasetType:
    return dc_index.products.from_doc(product_definition)
