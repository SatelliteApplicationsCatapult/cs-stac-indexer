import responses
from pathlib import Path

from stac_to_dc.domain.operations import get_item, guess_location, get_product_definition, \
    get_collection_url
from stac_to_dc.util import load_json


def valid_collection_url():
    url = 'https://s3-uk-1.sa-catapult.co.uk/public-eo-data/stac_catalogs/cs_stac/sentinel-2/collection.json'
    with open("tests/data/sentinel-2/collection.json", "rb") as enso_file:
        responses.add(
            responses.GET,
            url,
            status=200,
            stream=True,
            body=enso_file.read(),
            headers={'Content-Type': 'text/plain; charset=UTF-8'}
        )
    return url


def invalid_collection_url():
    url = 'https://s3-uk-1.sa-catapult.co.uk/public-eo-data/stac_catalogs/cs_stac/sentinel-2/collection.json'
    responses.add(
        responses.GET,
        url,
        status=503,
    )
    return url


def test_get_item():
    item = get_item('tests/data/sentinel-s2-l2a-cogs/S2A_30VXL_20210203_0_L2A.json')
    assert len(item) == 3


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


def test_get_collection_url_same_level():
    collection_url = get_collection_url('tests/data/sentinel-s2-l2a-cogs/S2A_30VXL_20210203_0_L2A.json')
    assert Path(collection_url) == Path('./tests/data/sentinel-s2-l2a-cogs/sentinel-s2-l2a-cogs.json').absolute()


def test_get_collection_url_parent_level():
    collection_url = get_collection_url('tests/data/uksa-ssgp/uksa-ssgp-pleiades/'
                                        'Pleiades_UKSA7_SO18034613-7-01_DS_PHR1A_201802241127550_FR1_PX_W002N51_0711_'
                                        '024843613631101/'
                                        'Pleiades_UKSA7_SO18034613-7-01_DS_PHR1A_201802241127550_FR1_PX_W002N51_0711_'
                                        '024843613631101.json')

    assert Path(collection_url) == Path('./tests/data/uksa-ssgp/uksa-ssgp-pleiades/collection.json').absolute()


def test_get_product_definition():
    product_definition = get_product_definition('tests/data/sentinel-2/collection.json')
    assert product_definition


@responses.activate
def test_get_product_definition_remote():
    product_definition = get_product_definition(valid_collection_url())
    assert product_definition


@responses.activate
def test_get_product_definition_remote_invalid():
    product_definition = get_product_definition(invalid_collection_url())
    assert not product_definition
