from schema import Schema
from stac_to_dc.domain.operations import guess_location, get_product_metadata_from_collection
from stac_to_dc.util import load_json


def test_guess_location_absolute():
    metadata = load_json('tests/data/sentinel-s2-l2a-cogs/S2A_30VXL_20210203_0_L2A.json')
    uri, relative = guess_location(metadata)
    assert not relative


def test_guess_location_relative():
    metadata = load_json('tests/data/uksa-ssgp/uksa-ssgp-spot/'
                         'UKSA_SPOT155_SO18034609-55-01_DS_SPOT6_201810101058095_FR1_FR1_FR1_FR1_W001N52_01140/'
                         'UKSA_SPOT155_SO18034609-55-01_DS_SPOT6_201810101058095_FR1_FR1_FR1_FR1_W001N52_01140.json')
    uri, relative = guess_location(metadata)
    assert relative


def test_get_product_metadata_from_collection():
    collection = load_json('tests/data/sentinel-2/collection.json')
    product = get_product_metadata_from_collection(collection)

    schema = Schema({'name': str,
                     'description': str,
                     'metadata_type': str,
                     'metadata': dict,
                     'measurements': list}
                    )
    assert schema.validate(product)
