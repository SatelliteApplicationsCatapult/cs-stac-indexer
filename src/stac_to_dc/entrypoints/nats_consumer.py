import asyncio
import logging
import signal

from datacube import Datacube
from nats.aio.client import Client as NATS
from stac_to_dc.adapters import repository
from stac_to_dc.config import get_s3_configuration, LOG_LEVEL, LOG_FORMAT, get_nats_uri
from stac_to_dc.domain.s3 import S3
from stac_to_dc.service_layer.services import index_product_definition, index_dataset

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

logger = logging.getLogger(__name__)

S3_ACCESS_KEY_ID = get_s3_configuration()["key_id"]
S3_SECRET_ACCESS_KEY = get_s3_configuration()["access_key"]
S3_REGION = get_s3_configuration()["region"]
S3_ENDPOINT = get_s3_configuration()["endpoint"]


async def run(loop):
    nc = NATS()

    async def closed_cb():
        logger.info("Connection to NATS is closed.")
        await asyncio.sleep(0.1, loop=loop)
        loop.stop()

    options = {
        "servers": [get_nats_uri()],
        "loop": loop,
        "closed_cb": closed_cb
    }

    await nc.connect(**options)
    logger.info(f"Connected to NATS at {nc.connected_url.netloc}...")

    async def message_handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        logger.info(f"Received a message on '{subject}': {data}")
        r = {
            'collection': index_product_definition,
            'item': index_dataset
        }
        message_type = subject.split('.')[1]
        if message_type in r.keys():
            s3 = S3(key=S3_ACCESS_KEY_ID, secret=S3_SECRET_ACCESS_KEY,
                    s3_endpoint=S3_ENDPOINT, region_name=S3_REGION)
            repo = repository.S3Repository(s3)
            dc = Datacube()

            for k, v in r.items():
                if k in subject:
                    v(dc.index, repo, data)

    await nc.subscribe("stac_indexer.*", cb=message_handler)

    def signal_handler():
        if nc.is_closed:
            return
        logger.info("Disconnecting...")
        loop.create_task(nc.close())

    for sig in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sig), signal_handler)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()
