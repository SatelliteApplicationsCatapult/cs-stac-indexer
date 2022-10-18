import logging
import math
from typing import List

import datacube.model
from datacube.index import Index
from datacube.utils import geometry
from datacube.utils.geometry import CoordList

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
        logger.info(f"adding {item_key} to dataset")
        dc_index.datasets.add(dataset)

    except NoObjectError:
        logger.error(f"Could not index dataset from {item_key}")


def split_geometry_anti_meridian(dataset: datacube.model.Dataset) -> datacube.model.Dataset:
    geom = geometry.Geometry(dataset["geometry"])

    # TODO: handle crs not being 4326

    # if the bounding box is wider than 180 degrees we will assume its meant to cross the anti meridian.
    # NOTE: this will break if we ever try to load a single global image.
    # Hay look, that tin can flies down the road really well.
    if geom.boundingbox().width() > 180:
        # Now split the geom into two parts around the anti meridian
        new_geom = geometry.multipolygon(_split_am(geom), geom.crs)
        dataset.metadata_doc["geometry"] = new_geom.json

    return dataset


def _split_am(geom: geometry.Geometry):
    left = []
    right = []

    for i in range(1, len(geom.exterior.points)):

        point = geom.exterior.points[i]
        prev = geom.exterior.points[i - 1]
        left, right = pair(left, right, prev, point)

    # handle the end of the loop back to the start.
    first = geom.exterior.points[0]
    last = geom.exterior.points[len(geom.exterior.points)-1]
    # are we crossing the anti meridian?
    if diff(last, first) > 180:
        # calculate the crossing point
        y = crossing_y(first, last)
        left.append((180.0, y))
        right.append((-180.0, y))

    # put in the last point to both lists.
    if left_side(first):
        left.append(first)
        right.append(right[0])
    else:
        right.append(first)
        left.append(left[0])

    return [[left, right]]


def pair(left, right, prev, point):
    # are we crossing the anti meridian?
    if diff(prev, point) > 180:
        # calculate the crossing point
        y = crossing_y(point, prev)
        left.append((180.0, y))
        right.append((-180.0, y))

    # normal point so just add to current.
    if left_side(point):
        left.append(point)
    else:
        right.append(point)

    return left, right


def diff(a, b):
    return max(a[0], b[0]) - min(a[0], b[0])


def left_side(p):
    return p[0] > 0


def crossing_y(a, b) -> float:
    """
    Use trig to calculate where on the y-axis the line crosses the anti-meridian.
    Note: This does not treat the earth as a sphere, in theory we should be dealing with small enough regions this
    should be ok.
    """
    angle_a = angle_from_y(a, b)
    angle_b = 180 - 90 - angle_a  # work out the other angle of the right angle triangle

    len_a = from_am(a[0])

    # sin rule
    len_b = (len_a / math.sin(math.radians(angle_a))) * math.sin(math.radians(angle_b))

    if a[1] > 0:
        return min(a[1], b[1]) + len_b
    return max(a[1], b[1]) - len_b


def angle_from_y(a, b) -> float:

    # normalise the points so -175 becomes 185
    a = normalise_am(a)
    b = normalise_am(b)

    # Now we can work out the angle from the x-axis
    angle = math.atan2(a[1] - b[1], a[0] - b[0]) * 180.0 / math.pi

    # now swap to the y-axis
    if a[0] > b[0]:
        if a[1] > b[1]:
            # below left
            return 90.0 - angle
        else:
            # above left
            return 90 + angle
    else:
        if a[1] > b[1]:
            # below right
            return angle - 90.0
        else:
            # above right
            return (90 + angle) * -1


def from_am(x):
    if x < 0:
        return 180.0 + x
    else:
        return 180 - x


def normalise_am(point):
    if point[0] < -150:  # -150 picked so its somewhere out the way of our aoi, but we can still test at 0,0
        return point[0] + 360.0, point[1]
    return point
