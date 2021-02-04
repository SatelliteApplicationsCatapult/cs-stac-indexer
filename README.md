# CS Indexing tools

## Introduction

This repo contains different CLI tools to facilitate data indexing into different platforms.

## Installation
Create a virtual environment (recommended)
```
> python -m venv venv
> source venv/bin/activate
```

Install dependencies
```
> pip install -r requirements.txt
> pip install --extra-index-url="https://packages.dea.ga.gov.au" odc-index
> pip install .
```

## Usage
### stac-to-es

Indexes STAC item files contained in the given `COLLECTION_FOLDER` path into Elasticsearch (ES). A new ES index is created
using the same collection folder's name and uses the given `ID_FIELD` as unique identifier.

```
> stac-to-es --help
Usage: stac-to-es [OPTIONS] COLLECTION_FOLDER ID_FIELD

Options:
  --help  Show this message and exit.
```

Example of use

```
> stac-to-es ./test/data/uksa-ssgp/uksa-ssgp-pleiades id
```

#### Configuration

This tool allows some configuration via the [config.json](./src/stac_to_es/config.json) file:
- _es_index_settings_: elasticsearch [indices put mapping](https://www.elastic.co/guide/en/elasticsearch/reference/master/indices-put-mapping.html).
- _stac_excluded_keys_: STAC keys that aren't going to be included into the properties.

### stac-to-dc

Indexes the `STAC_ITEM` file given as a parameter into datacube in the given `PRODUCT`.

```
> stac-to-dc --help
Usage: stac-to-dc [OPTIONS] STAC_ITEM PRODUCT

Options:
  --help  Show this message and exit.
```

Example of use
```
> stac-to-dc ./test/data/sentinel-s2-l2a-cogs/S2A_30VXL_20210203_0_L2A.json s2_l2a
```

#### Test Environment
Spin the test environment up
```
docker-compose up -d
```

(wait for the database to be populated)

Add sentinel 2 product
``` docker
docker exec -it cs-stac-indexer_explorer_1 datacube product add https://raw.githubusercontent.com/digitalearthafrica/config/master/products/esa_s2_l2a.yaml
```

Generate product summaries (for datacube explorer)
``` docker
docker exec -it cs-stac-indexer_explorer_1 cubedash-gen --init --all
```

Index the s2 example dataset
``` bash
stac-to-dc ./test/data/sentinel-s2-l2a-cogs/S2A_30VXL_20210203_0_L2A.json s2_l2a
```

Refresh the collection (for datacube explorer)
``` docker
docker exec -it cs-stac-indexer_explorer_1 cubedash-gen --force-refresh s2_l2a
```