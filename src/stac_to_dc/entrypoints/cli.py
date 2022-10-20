import logging

from datacube import Datacube
from datacube import model, index

import urllib3

from stac_to_dc.domain import operations

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import click as click
from datacube.index.hl import Doc2Dataset
from datacube.model import DatasetType
from odc.index.stac import stac_transform, stac_transform_absolute
from stac_to_dc.adapters import repository
from stac_to_dc.config import get_s3_configuration, LOG_LEVEL, LOG_FORMAT
from stac_to_dc.domain.operations import get_product_metadata_from_collection, guess_location, add_custom_metadata
from stac_to_dc.domain.s3 import S3
from stac_to_dc.util import parse_s3_url

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

logger = logging.getLogger(__name__)

S3_ACCESS_KEY_ID = get_s3_configuration()["key_id"]
S3_SECRET_ACCESS_KEY = get_s3_configuration()["access_key"]
S3_ENDPOINT = get_s3_configuration()["endpoint"]
S3_REGION = get_s3_configuration()["region"]



def collection_to_product(dc_index: index.Index, collection: dict) -> DatasetType:
    product_metadata = get_product_metadata_from_collection(collection)
    return dc_index.products.from_doc(product_metadata)


@click.command("stac-to-dc")
@click.argument("stac-url", type=str, nargs=1)
def main(stac_url):
    try:
        s3 = S3(key=S3_ACCESS_KEY_ID, secret=S3_SECRET_ACCESS_KEY,
                s3_endpoint=S3_ENDPOINT, region_name=S3_REGION)
        s3_repo = repository.S3Repository(s3)

        bucket, path = parse_s3_url(url=stac_url)
        catalog = s3_repo.get_catalog(bucket=bucket, path=path)
        collections = s3_repo.get_collections_from_catalog(catalog)
        for collection in collections:
            dc = Datacube()
            odc_products = dc.index.products.get_all()
            product = collection_to_product(
                dc_index=dc.index,
                collection=collection
            )
            if product not in odc_products:
                logger.info(f"[-- Indexing Product definition: {product.name} --]")
                dc.index.products.add(product)

            items = s3_repo.get_items_from_collection(collection)
            for item in items:
                dataset = operations.item_to_dataset(
                    dc_index=dc.index,
                    product_name=product.name,
                    item=item
                )                
                dc.index.datasets.add(dataset)

    except Exception as err:
        logger.exception(err)


if __name__ == '__main__':
    main()
