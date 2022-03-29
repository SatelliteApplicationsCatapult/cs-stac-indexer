import json
from typing import List

from stac_to_dc.domain.s3 import S3, NoObjectError
from stac_to_dc.util import parse_s3_url, get_rel_links


class S3Repository:

    def __init__(self, s3: S3):
        self.s3 = s3

    def get_catalogs_from_path(self, bucket: str, path: str) -> List[dict]:
        catalog_objs = self.s3.list_objects(bucket, prefix=path, suffix='catalog.json')
        return [self.s3.get_json_object(c.bucket_name, c.key) for c in catalog_objs]
    
    def get_catalog(self, bucket: str, path: str) -> dict:
        return self.s3.get_json_object(bucket, path)
    
    def get_collections_from_catalog(self, catalog: dict) -> List[dict]:
        collection_links = get_rel_links(catalog, 'child')
        return [self.s3.get_json_object(bucket, key) for bucket, key in map(parse_s3_url, collection_links)]

    def get_items_from_collection(self, collection: dict) -> List[dict]:
        item_links = get_rel_links(collection, 'item')
        return [self.s3.get_json_object(bucket, key) for bucket, key in map(parse_s3_url, item_links)]

    def get_dict(self, bucket: str, key: str) -> dict:
        try:
            catalog_body = self.s3.get_object_body(bucket_name=bucket, object_name=key)
            return json.loads(catalog_body.decode('utf-8'))
        except NoObjectError:
            raise
