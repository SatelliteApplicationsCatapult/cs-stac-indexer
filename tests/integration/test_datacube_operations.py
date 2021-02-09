from datacube import Datacube
from stac_to_dc.domain.datacube_operations import create_product
from stac_to_dc.domain.operations import get_product_definition


def test_create_product():
    dc = Datacube()
    product_definition = get_product_definition('tests/data/sentinel-s2-l2a-cogs/sentinel-s2-l2a-cogs.json')
    product = create_product(dc.index, product_definition)
    assert product


def test_add_product():
    dc = Datacube()
    product_definition = get_product_definition('tests/data/sentinel-s2-l2a-cogs/sentinel-s2-l2a-cogs.json')
    product = create_product(dc.index, product_definition)
    dc.index.products.add(product)
