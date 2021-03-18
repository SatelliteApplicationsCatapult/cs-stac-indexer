import os
from logging import INFO

LOG_FORMAT = '%(asctime)s - %(levelname)6s - %(message)s'
LOG_LEVEL = INFO


def get_s3_configuration():
    key_id = os.environ.get("S3_ACCESS_KEY_ID", None)
    access_key = os.environ.get("S3_SECRET_ACCESS_KEY", None)
    region = os.environ.get("S3_REGION", 'us-east-1')
    endpoint = os.environ.get("S3_ENDPOINT", 'https://s3-uk-1.sa-catapult.co.uk')
    bucket = os.environ.get("S3_BUCKET", 'public-eo-data')

    return dict(key_id=key_id, access_key=access_key, region=region,
                endpoint=endpoint, bucket=bucket)
