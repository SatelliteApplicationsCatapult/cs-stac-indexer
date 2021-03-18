from stac_to_dc.entrypoints.cli import main
from click.testing import CliRunner


def test_main():
    runner = CliRunner()
    result = runner.invoke(main, ['https://s3-uk-1.sa-catapult.co.uk/'
                                  'public-eo-data/stac_catalogs/cs_stac/catalog.json'])
    assert result.exit_code == 0
