from moto import mock_s3
from schema import Schema
from stac_to_dc.domain.s3 import S3


BUCKET = 'test'


def initialise_bucket(s3_resource, bucket_name):
    s3_resource.create_bucket(Bucket=bucket_name)
    s3_resource.Bucket(bucket_name).upload_file(
        Filename='tests/data/catalog.json',
        Key='/path1/catalog.json'
    )
    s3_resource.Bucket(bucket_name).upload_file(
        Filename='tests/data/catalog.json',
        Key='/path2/catalog.json'
    )
    s3_resource.Bucket(bucket_name).upload_file(
        Filename='tests/data/catalog.jpg',
        Key='/path2/catalog.jpg'
    )


@mock_s3
def test_check_bucket_exists():
    s3 = S3(key=None, secret=None, s3_endpoint=None, region_name='us-east-1')
    initialise_bucket(s3_resource=s3.s3_resource, bucket_name=BUCKET)
    assert s3.check_bucket_exist(BUCKET)


@mock_s3
def test_check_bucket_does_not_exist():
    s3 = S3(key=None, secret=None, s3_endpoint=None, region_name='us-east-1')
    assert not s3.check_bucket_exist(BUCKET)


@mock_s3
def test_list_objects_with_suffix():
    s3 = S3(key=None, secret=None, s3_endpoint=None, region_name='us-east-1')
    initialise_bucket(s3_resource=s3.s3_resource, bucket_name=BUCKET)

    objects = s3.list_objects(BUCKET, suffix='catalog.json')

    object_names = [obj.key for obj in objects]
    assert object_names == ['/path1/catalog.json', '/path2/catalog.json']


@mock_s3
def test_list_objects_with_prefix():
    s3 = S3(key=None, secret=None, s3_endpoint=None, region_name='us-east-1')
    initialise_bucket(s3_resource=s3.s3_resource, bucket_name=BUCKET)

    objects = s3.list_objects(BUCKET, prefix='/path2')

    object_names = [obj.key for obj in objects]
    assert object_names == ['/path2/catalog.jpg', '/path2/catalog.json']


@mock_s3
def test_list_objects_with_suffix_and_prefix():
    s3 = S3(key=None, secret=None, s3_endpoint=None, region_name='us-east-1')
    initialise_bucket(s3_resource=s3.s3_resource, bucket_name=BUCKET)

    objects = s3.list_objects(BUCKET, prefix='/path2', suffix='catalog.json')

    object_names = [obj.key for obj in objects]
    assert object_names == ['/path2/catalog.json']


@mock_s3
def test_get_json_object():
    s3 = S3(key=None, secret=None, s3_endpoint=None, region_name='us-east-1')
    initialise_bucket(s3_resource=s3.s3_resource, bucket_name=BUCKET)

    catalog = s3.get_json_object(bucket_name=BUCKET, object_name='/path2/catalog.json')

    schema = Schema({'id': str,
                     'stac_version': str,
                     'description': str,
                     'links': list,
                     'stac_extensions': list,
                     'title': str}
                    )
    assert schema.validate(catalog)


@mock_s3
def test_get_json_object_key_does_not_exist():
    s3 = S3(key=None, secret=None, s3_endpoint=None, region_name='us-east-1')
    initialise_bucket(s3_resource=s3.s3_resource, bucket_name=BUCKET)

    catalog = s3.get_json_object(bucket_name=BUCKET, object_name='/path2/fake_catalog.json')
    assert not catalog


@mock_s3
def test_get_json_object_json_does_not_exist():
    s3 = S3(key=None, secret=None, s3_endpoint=None, region_name='us-east-1')
    initialise_bucket(s3_resource=s3.s3_resource, bucket_name=BUCKET)

    catalog = s3.get_json_object(bucket_name=BUCKET, object_name='/path2/catalog.jpg')
    assert not catalog
