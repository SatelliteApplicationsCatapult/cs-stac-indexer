from stac_to_dc.cli import main
from click.testing import CliRunner


def test_main():
    runner = CliRunner()
    result = runner.invoke(main, ['tests/data/sentinel-2/'
                                  'S2A_MSIL2A_20151002T222056_T01KAU/'
                                  'S2A_MSIL2A_20151002T222056_T01KAU.json'])
    assert result.exit_code == 0
