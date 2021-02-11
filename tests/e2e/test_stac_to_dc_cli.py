from stac_to_dc.cli import main
from click.testing import CliRunner


def test_main():
    runner = CliRunner()
    result = runner.invoke(main, ['tests/data/sentinel-s2-l2a-cogs/S2A_30VXL_20210203_0_L2A.json'])
    assert result.exit_code == 0
