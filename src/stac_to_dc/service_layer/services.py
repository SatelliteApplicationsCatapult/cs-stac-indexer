import logging

from datacube.index import Index
from stac_to_dc.adapters.repository import S3Repository
from stac_to_dc.config import LOG_LEVEL, LOG_FORMAT, get_s3_configuration
from stac_to_dc.domain.operations import get_product_metadata_from_collection, item_to_dataset
from stac_to_dc.domain.s3 import NoObjectError
from stac_to_dc.util import get_rel_links, parse_s3_url

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

S3_BUCKET = get_s3_configuration()["bucket"]


def index_product_definition(dc_index: Index, repo: S3Repository, collection_key: str):
    try:
        collection_dict = repo.get_dict(bucket=S3_BUCKET, key=collection_key)
        product_metadata = get_product_metadata_from_collection(collection_dict)

        product = dc_index.products.from_doc(product_metadata)
        dc_index.products.add(product)

        item_links = get_rel_links(collection_dict, 'item')
        for item_href in item_links:
            bucket, item_key = parse_s3_url(item_href)
            index_dataset(dc_index, repo, item_key)

    except NoObjectError:
        logger.error(f"Could not index product definition from {collection_key}")


def index_dataset(dc_index: Index, repo: S3Repository, item_key: str):
    try:
        item_dict = repo.get_dict(bucket=S3_BUCKET, key=item_key)
        product_name = item_key.split('/')[-3]

        dataset = item_to_dataset(
            dc_index=dc_index,
            product_name=product_name,
            item=item_dict
        )
        logger.info(f"adding dataset {item_key}")
        dc_index.datasets.add(dataset)

    except NoObjectError:
        logger.error(f"Could not index dataset from {item_key}")

