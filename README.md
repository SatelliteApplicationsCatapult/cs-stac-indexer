# CS Indexing tools

## Introduction

This repo contains different CLI tools to facilitate data indexing into different platforms.

## Usage
### stac-to-dc

Indexes the `STAC_URL` catalog/s contained under the given s3 path as a parameter into datacube. It automatically 
resolves and indexes the *collections* as a **product definition** and *items* as a **dataset**.


```
> stac-to-dc --help
Usage: stac-to-dc [OPTIONS] STAC_URL

Options:
  --help  Show this message and exit.
```

Example of use
```
> stac-to-dc https://s3-uk-1.sa-catapult.co.uk/public-eo-data/stac_catalogs/cs_stac/catalog.json
```

One criteria to bear in mind is the `product_definition` stac_extension included in the collection, it
is where the tool will look at in order to create the product. This `product_definition` extension looks like this:

```json
{
    ...
    "stac_extensions": [
        "product_definition"
    ],
    ...
    "properties": {
        "product_definition:metadata_type": "eo3",
        "product_definition:metadata": {
            "product": {
                "name": "sentinel_2"
            }
        },
        "product_definition:measurements": [
            {
              "name": "B01",
              "aliases": [
                "band_01",
                "coastal_aerosol"
              ],
              "units": "1",
              "dtype": "uint16",
              "nodata": 0
            },
            ...
        ]
    }
    ...
}
```

## Environment Variables
| Var name| Used for |
| --- | --- |
|DB_HOSTNAME| The hostname of the database |
|DB_USERNAME| The username of the database user |
|DB_PASSWORD| The password of the database user |
|DB_DATABASE| The name of the database |
|DB_PORT| The port of the database |
|NATS_HOST | The hostname of the NATS server |
|NATS_PORT | The port of the NATS server |
|AWS_ACCESS_KEY_ID | AWS access key |
|AWS_SECRET_ACCESS_KEY | AWS secret key |
|AWS_DEFAULT_REGION | AWS region |
|S3_ENDPOINT_URL | S3 endpoint url |
|S3_BUCKET | S3 bucket name |


#### Test Environment

The following make command will remove if exists any deployment, build the docker image, deploy the environment and run
all the tests.
```
make all
```

See [Makefile](./Makefile) for more instructions.

#### Configuration

This tool allows some configuration via the [config.json](./src/stac_to_es/config.json) file:
- _es_index_settings_: elasticsearch [indices put mapping](https://www.elastic.co/guide/en/elasticsearch/reference/master/indices-put-mapping.html).
- _stac_excluded_keys_: STAC keys that aren't going to be included into the properties.
