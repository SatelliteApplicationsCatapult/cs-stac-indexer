from setuptools import setup

extras_require = {
    # These are all optional but nice to have on a real deployment
    "deployment": [
        # Performance
        "ciso8601",
        "bottleneck",
        # The default run.sh and docs use gunicorn+meinheld
        "gunicorn",
        "setproctitle",
        "meinheld",
        "gevent",
        # Monitoring
        "raven",
        "blinker",
        "prometheus-flask-exporter",
    ],
}

setup(
    name='stac_to_dc',
    version='0.1',
    packages=['stac_to_dc', 'cubedash'],
    setup_requires=["setuptools_scm"],
    install_requires=[
        "cachetools",
        "click",
        "dataclasses>=0.6;python_version<'3.7'",
        "datacube>=1.8",
        "eodatasets3 >= 0.17.0",
        "fiona",
        "flask",
        "Flask-Caching",
        "flask_themes @ git+https://git@github.com/opendatacube/flask-themes@master",
        "geoalchemy2",
        "geographiclib",
        "jinja2",
        "pyorbital",
        "pyproj",
        "python-dateutil",
        "python-rapidjson",
        "shapely",
        "simplekml",
        "sqlalchemy",
        "structlog",
    ],
    extras_require=extras_require,
    entry_points={
        'console_scripts': [
            'stac-to-dc=stac_to_dc.cli:main',
            'cubedash-gen=cubedash.generate:cli'
        ],
    }
)
