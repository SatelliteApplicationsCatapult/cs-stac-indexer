from setuptools import setup

setup(
    name='stac_to_dc',
    version='0.1',
    packages=['stac_to_dc'],
    entry_points={
        'console_scripts': [
            'stac-to-dc=stac_to_dc.cli:main',
        ],
    }
)
