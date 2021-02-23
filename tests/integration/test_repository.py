from moto import mock_s3
from stac_to_dc.adapters import repository
from stac_to_dc.domain.s3 import S3
from pathlib import Path

from stac_to_dc.util import load_json, get_files_from_dir

BUCKET = 'public-eo-data'


def initialise_stac_bucket(s3_resource, bucket_name):
    s3_resource.create_bucket(Bucket=bucket_name)
    s3_resource.Bucket(bucket_name).upload_file(
        Filename='tests/data/catalog.json',
        Key='stac_catalogs/cs_stac/catalog.json'
    )
    s3_resource.Bucket(bucket_name).upload_file(
        Filename='tests/data/sentinel-2/collection.json',
        Key=f"stac_catalogs/cs_stac/sentinel-2/collection.json"
    )
    for file in Path('tests/data/sentinel-2').glob('**/*.json'):
        s3_resource.Bucket(bucket_name).upload_file(
            Filename=str(file),
            Key=f"stac_catalogs/cs_stac/sentinel-2/{file.stem}/{file.name}"
        )


@mock_s3
def test_repository_can_get_catalogs_from_s3_path():
    s3 = S3(key=None, secret=None, s3_endpoint=None, region_name='us-east-1')
    initialise_stac_bucket(s3_resource=s3.s3_resource, bucket_name=BUCKET)

    repo = repository.S3Repository(s3)
    catalogs = repo.get_catalogs_from_path(bucket=BUCKET, path='stac_catalogs/cs_stac')

    assert catalogs == [load_json('tests/data/catalog.json')]


@mock_s3
def test_repository_can_get_collections_from_catalog():
    s3 = S3(key=None, secret=None, s3_endpoint=None, region_name='us-east-1')
    initialise_stac_bucket(s3_resource=s3.s3_resource, bucket_name=BUCKET)
    catalog_test = load_json('tests/data/catalog.json')
    collection_test = load_json('tests/data/sentinel-2/collection.json')

    repo = repository.S3Repository(s3)
    collections = repo.get_collections_from_catalog(catalog_test)

    assert collections == [collection_test]


@mock_s3
def test_repository_get_items_from_collection():
    s3 = S3(key=None, secret=None, s3_endpoint=None, region_name='us-east-1')
    initialise_stac_bucket(s3_resource=s3.s3_resource, bucket_name=BUCKET)
    collection_test = load_json('tests/data/sentinel-2/collection.json')
    items_test = [load_json(item) for item in get_files_from_dir('tests/data/sentinel-2', 'json')
                  if not item.endswith('collection.json')]

    repo = repository.S3Repository(s3)
    items = repo.get_items_from_collection(collection_test)

    assert any(x != y for x, y in zip(items, items_test))

