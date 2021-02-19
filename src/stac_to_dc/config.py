import os
from logging import INFO
from typing import Tuple

LOG_FORMAT = '%(asctime)s - %(levelname)6s - %(message)s'
LOG_LEVEL = INFO


def get_aws_config() -> Tuple[str, str, str]:
    s3_key_id = os.getenv('AWS_ACCESS_KEY_ID', 'foobar_id')
    s3_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'foobar_key')
    s3_endpoint_url = os.getenv('AWS_ENDPOINT_URL', 'http://s3-uk-1.sa-catapult.co.uk')
    return s3_key_id, s3_access_key, s3_endpoint_url
