import logging
import os
from typing import Tuple

from stac_to_dc.config import LOG_LEVEL, LOG_FORMAT

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


def get_product_metadata_from_collection(collection: dict) -> dict:
    product_definition = None

    if collection and "product_definition" in collection.get("stac_extensions"):
        product_definition = {
            "name": collection.get("properties").get("product_definition:metadata").get("product").get("name"),
            "description": collection.get("description"),
        }
        for k, v in collection.get("properties").items():
            if "product_definition:" in k:
                product_definition[k.split(':')[1]] = v

    return product_definition
