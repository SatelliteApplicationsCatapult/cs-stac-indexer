import logging
import os
from typing import Tuple

from datacube import index, model
from datacube.index.hl import Doc2Dataset
from odc.index.stac import stac_transform, stac_transform_absolute
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
        product_name = collection.get("properties").get("product_definition:metadata").get("product").get("name")
        product_definition = {
            "name": product_name,
            "description": collection.get("description"),
        }
        for k, v in collection.get("properties").items():
            if "product_definition:" in k:
                product_definition[k.split(':')[1]] = v
                
    return product_definition

def add_custom_metadata(metadata: dict) -> dict:
    try:
        metadata['eo:platform'] = {'name': metadata['properties']['eo:platform']}
    except KeyError as e:
        logger.warning(f"Missing property: {e}")
    
    return metadata

def item_to_dataset(
        dc_index: index.Index,
        product_name: str,
        item: dict
) -> model.Dataset:

    doc2ds = Doc2Dataset(index=dc_index, products=[product_name])
    uri, relative = guess_location(item)

    if relative:
        metadata = stac_transform(item)
    else:
        metadata = stac_transform_absolute(item)
    logger.info("got metadata?")
    ds, err = doc2ds(metadata, uri)
    logger.info(f"ds: {ds} err: {err}")
    if err is not None:
        logger.error(f"could not create dataset {err}")

    if ds is not None:
        return ds

