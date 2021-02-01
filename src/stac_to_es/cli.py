import json
from pathlib import Path

import click as click
from elasticsearch import Elasticsearch, helpers

from stac_to_es.load_config import es_index_settings, stac_excluded_keys


def data_generator(geojson, id_field, index_name):
    print(f"Inserting {id_field} in {index_name}...")
    yield {
        "_index": index_name,
        "_id": geojson['properties'][id_field],
        "_source": json.dumps(geojson)
    }


def stac_to_geojson(stac_data):
    geojson = {
        'type': stac_data['type'],
        'geometry': stac_data['geometry'],
        'properties': stac_data['properties']
    }

    for key in stac_data.keys():
        if key not in list(geojson.keys()) + stac_excluded_keys:
            geojson['properties'][key] = stac_data[key]

    return geojson


@click.command("stac-to-es")
@click.argument("collection-folder", type=click.Path(exists=True), nargs=1)
@click.argument("id-field", type=str, nargs=1)
def main(collection_folder, id_field):

    es = Elasticsearch()
    index_name = Path(collection_folder).name

    if es.indices.exists(index_name):
        es.indices.delete(index_name)

    es.indices.create(index=index_name, body=es_index_settings, request_timeout=90)

    for file in Path(collection_folder).glob('**/*.json'):
        if 'collection' not in file.name:
            with open(file) as fh:
                d = json.load(fh)
                geojson = stac_to_geojson(d)
                # call generator function to yield features into ES build API
                helpers.bulk(es, data_generator(geojson, id_field, index_name))


if __name__ == '__main__':
    main()


