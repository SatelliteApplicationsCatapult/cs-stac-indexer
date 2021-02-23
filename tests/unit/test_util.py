from stac_to_dc.util import get_files_from_dir, parse_s3_url, load_json, get_rel_links


def test_get_files_from_dir():
    files = get_files_from_dir('tests/data/uksa-ssgp', 'json')
    assert files


def test_parse_s3_url():
    url = "https://s3-uk-1.sa-catapult.co.uk/public-eo-data/cs_stac/sentinel-2/collection.json"
    bucket, key = parse_s3_url(url=url)
    assert (bucket, key) == ('public-eo-data', 'cs_stac/sentinel-2/collection.json')


def test_rel_links_child():
    metadata = load_json('tests/data/catalog.json')
    child_links = get_rel_links(metadata, 'child')
    assert child_links == ["https://s3-uk-1.sa-catapult.co.uk/public-eo-data/stac_catalogs/cs_stac/sentinel-2"
                           "/collection.json"]


def test_rel_links_item():
    metadata = load_json('tests/data/sentinel-2/collection.json')
    child_links = get_rel_links(metadata, 'item')
    assert child_links == ['https://s3-uk-1.sa-catapult.co.uk/public-eo-data/stac_catalogs/cs_stac/sentinel-2'
                           '/S2A_MSIL2A_20151002T222056_T01KAU/S2A_MSIL2A_20151002T222056_T01KAU.json',
                           'https://s3-uk-1.sa-catapult.co.uk/public-eo-data/stac_catalogs/cs_stac/sentinel-2'
                           '/S2A_MSIL2A_20151002T222056_T01KBU/S2A_MSIL2A_20151002T222056_T01KBU.json',
                           'https://s3-uk-1.sa-catapult.co.uk/public-eo-data/stac_catalogs/cs_stac/sentinel-2'
                           '/S2A_MSIL2A_20151022T222102_T01KAU/S2A_MSIL2A_20151022T222102_T01KAU.json',
                           'https://s3-uk-1.sa-catapult.co.uk/public-eo-data/stac_catalogs/cs_stac/sentinel-2'
                           '/S2A_MSIL2A_20151022T222102_T01KBU/S2A_MSIL2A_20151022T222102_T01KBU.json',
                           'https://s3-uk-1.sa-catapult.co.uk/public-eo-data/stac_catalogs/cs_stac/sentinel-2'
                           '/S2A_MSIL2A_20151114T223002_T60KWD/S2A_MSIL2A_20151114T223002_T60KWD.json',
                           'https://s3-uk-1.sa-catapult.co.uk/public-eo-data/stac_catalogs/cs_stac/sentinel-2'
                           '/S2A_MSIL2A_20151114T223002_T60KWE/S2A_MSIL2A_20151114T223002_T60KWE.json',
                           'https://s3-uk-1.sa-catapult.co.uk/public-eo-data/stac_catalogs/cs_stac/sentinel-2'
                           '/S2A_MSIL2A_20151114T223002_T60KWF/S2A_MSIL2A_20151114T223002_T60KWF.json',
                           'https://s3-uk-1.sa-catapult.co.uk/public-eo-data/stac_catalogs/cs_stac/sentinel-2'
                           '/S2A_MSIL2A_20151114T223002_T60KWG/S2A_MSIL2A_20151114T223002_T60KWG.json',
                           'https://s3-uk-1.sa-catapult.co.uk/public-eo-data/stac_catalogs/cs_stac/sentinel-2'
                           '/S2A_MSIL2A_20151114T223002_T60KXD/S2A_MSIL2A_20151114T223002_T60KXD.json',
                           'https://s3-uk-1.sa-catapult.co.uk/public-eo-data/stac_catalogs/cs_stac/sentinel-2'
                           '/S2A_MSIL2A_20151114T223002_T60KXE/S2A_MSIL2A_20151114T223002_T60KXE.json']


def test_rel_links_no_exists():
    metadata = load_json('tests/data/catalog.json')
    child_links = get_rel_links(metadata, 'foo')
    assert child_links == []
