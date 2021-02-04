from stac_to_dc.util import get_files_from_dir


def test_get_files_from_dir():
    files = get_files_from_dir('test/data/uksa-ssgp', 'json')
    assert files
