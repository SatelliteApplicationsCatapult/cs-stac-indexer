from stac_to_dc.domain.operations import get_item, guess_location
from stac_to_dc.util import load_json


def test_get_item():
    item = get_item('test/data/sentinel-s2-l2a-cogs/S2A_30VXL_20210203_0_L2A.json')
    assert len(item) == 3


def test_guess_location_absolute():
    metadata = load_json('test/data/sentinel-s2-l2a-cogs/S2A_30VXL_20210203_0_L2A.json')
    uri, relative = guess_location(metadata)
    assert not relative


def test_guess_location_relative():
    metadata = load_json('test/data/uksa-ssgp/uksa-ssgp-spot/'
                         'UKSA_SPOT155_SO18034609-55-01_DS_SPOT6_201810101058095_FR1_FR1_FR1_FR1_W001N52_01140/'
                         'UKSA_SPOT155_SO18034609-55-01_DS_SPOT6_201810101058095_FR1_FR1_FR1_FR1_W001N52_01140.json')
    uri, relative = guess_location(metadata)
    assert relative
