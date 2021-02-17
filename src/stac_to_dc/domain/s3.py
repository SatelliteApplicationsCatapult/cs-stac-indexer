import json
import logging

import boto3
from botocore.exceptions import ClientError
from stac_to_dc.config import LOG_LEVEL, LOG_FORMAT

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

logger = logging.getLogger(__name__)


class S3:
    """Class to handle S3 operations."""

    def __init__(self, key, secret, s3_endpoint, region_name):
        """
        Initialize s3 class.
        Params:
            key           (str): AWS_ACCESS_KEY_ID
            secret        (str): AWS_SECRET_ACCESS_KEY
            s3_endpoint   (str): S3 endpoint URL
            region_name   (str): Region Name
        """
        self.s3_resource = boto3.resource(
            "s3",
            endpoint_url=s3_endpoint,
            verify=False,
            region_name=region_name,
            aws_access_key_id=key,
            aws_secret_access_key=secret,
        )
        self.buckets_exist = []

    def check_bucket_exist(self, bucket_name):
        """
        Verify if a bucket exists.
        Params:
            bucket_name           (str): Bucket name
        Return:
            True  : bucket exists
            False : bucket does not exist
        """
        # If bucket was already checked, return it exists
        if bucket_name in self.buckets_exist:
            logger.debug("bucket %s was already checked, do not check again", bucket_name)
            return True

        try:
            logger.debug("Checking if bucket exist: %s", bucket_name)
            self.s3_resource.meta.client.head_bucket(Bucket=bucket_name)
            self.buckets_exist.append(bucket_name)
            return True
        except ClientError as error:
            if error.response["Error"]["Code"] == "404":
                return False
            else:
                raise

    def list_objects(self, bucket_name, *, prefix=None, suffix=None, limit=None):
        """
        List objects stored in a bucket.
        Params:
            bucket_name      (str): Bucket name
        Keyword arguments (opt):
            prefix           (str): Filter only objects with specific prefix
                                    default None
            suffix           (str): Filter only objects with specific suffix
                                    default None
            limit            (int): Limit the number of objects returned
                                    default None
        Returns:
            An iterable of ObjectSummary resources
        """
        if prefix:
            objects = list(self.s3_resource.Bucket(bucket_name).objects.filter(Prefix=prefix).limit(limit))
        else:
            objects = list(self.s3_resource.Bucket(bucket_name).objects.all().limit(limit))

        if suffix:
            return [obj for obj in objects if obj.key.endswith(suffix)]
        else:
            return objects

    def get_json_object(self, bucket_name, object_name) -> dict:
        """
        Download an object from S3 and return its body as a dictionary.
        Params:
            bucket_name            (str): Bucket name
            object_name            (str): Object name
        """
        try:
            obj = self.s3_resource.Object(bucket_name=bucket_name, key=object_name).get()
            return json.loads(obj.get('Body').read().decode('utf-8'))
        except ClientError as ex:
            if ex.response['Error']['Code'] == 'NoSuchKey':
                logger.warning(f"No object found for {object_name} in {bucket_name} bucket")
                return dict()
            else:
                raise
        except UnicodeDecodeError:
            logger.error(f"Could not obtain JSON from {object_name}")
            return dict()
