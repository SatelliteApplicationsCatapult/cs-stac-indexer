import os
from logging import INFO

LOG_FORMAT = '%(asctime)s - %(levelname)6s - %(message)s'
LOG_LEVEL = INFO


def get_nats_uri():
    nats_host = os.environ.get("NATS_HOST", "localhost")
    nats_port = int(os.environ.get("NATS_PORT", "30001"))
    return f"nats://{nats_host}:{nats_port}"


def get_s3_configuration():
    key_id = os.environ.get("AWS_ACCESS_KEY_ID", None)
    access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", None)
    region = os.environ.get("AWS_DEFAULT_REGION", None)
    endpoint = os.environ.get("AWS_ENDPOINT_URL", 'https://s3.eu-west-2.amazonaws.com')
    bucket = os.environ.get("S3_BUCKET", None)

    return dict(key_id=key_id, access_key=access_key, region=region,
                endpoint=endpoint, bucket=bucket)
