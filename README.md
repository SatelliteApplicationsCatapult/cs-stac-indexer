# CS Indexing tools

## Introduction

This repo contains different CLI tools to facilitate data indexing into different platforms.

## Installation
```
pip install .
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
