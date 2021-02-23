import logging

from datacube import Datacube
from datacube import model, index

import click as click
from datacube.index.hl import Doc2Dataset
from datacube.model import DatasetType
from odc.index.stac import stac_transform, stac_transform_absolute
from stac_to_dc.adapters import repository
from stac_to_dc.config import get_aws_config, LOG_LEVEL, LOG_FORMAT
from stac_to_dc.domain.operations import get_product_metadata_from_collection, guess_location
from stac_to_dc.domain.s3 import S3
from stac_to_dc.util import parse_s3_url

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

logger = logging.getLogger(__name__)


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

    ds, err = doc2ds(metadata, uri)

    if ds is not None:
        return ds


def collection_to_product(dc_index: index.Index, collection: dict) -> DatasetType:
    product_metadata = get_product_metadata_from_collection(collection)
    return dc_index.products.from_doc(product_metadata)


@click.command("stac-to-dc")
@click.argument("stac-url", type=str, nargs=1)
def main(stac_url):
    try:
        s3_key, s3_secret, s3_endpoint_url = get_aws_config()
        s3 = S3(key=s3_key, secret=s3_secret, s3_endpoint=s3_endpoint_url, region_name=None)
        s3_repo = repository.S3Repository(s3)

        bucket, path = parse_s3_url(url=stac_url)
        catalogs = s3_repo.get_catalogs_from_path(bucket=bucket, path=path)
        for catalog in catalogs:
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
                    dataset = item_to_dataset(
                        dc_index=dc.index,
                        product_name=product.name,
                        item=item
                    )
                    logger.info(f"[-- Indexing Dataset: {dataset.metadata.label} --]")
                    dc.index.datasets.add(dataset)

    except Exception as err:
        logger.error(err)


if __name__ == '__main__':
    main()
