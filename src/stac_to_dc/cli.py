from typing import Tuple

from datacube import Datacube
from datacube import model, index

import click as click
from datacube.index.hl import Doc2Dataset
from odc.index.stac import stac_transform, stac_transform_absolute
from stac_to_dc.domain.operations import get_item, create_product, \
    get_product_definition, get_collection_url


def stac_item_to_dataset(
        dc_index: index.Index,
        product_name: str,
        stac_item: Tuple[dict, str, bool]
) -> model.Dataset:

    doc2ds = Doc2Dataset(index=dc_index, products=[product_name])
    metadata, uri, relative = stac_item

    if relative:
        metadata = stac_transform(metadata)
    else:
        metadata = stac_transform_absolute(metadata)

    ds, err = doc2ds(metadata, uri)

    if ds is not None:
        return ds


def collection_to_product(
        dc_index: index.Index,
        collection_url: str
) -> model.DatasetType:
    product_definition = get_product_definition(collection_url)
    return create_product(dc_index, product_definition)


@click.command("stac-to-dc")
@click.argument("stac-item", type=str, nargs=1)
def main(stac_item):

    dc = Datacube()

    # Get (stac, uri, relative_uri) tuples
    item = get_item(stac_item)

    # Get collection link from item
    collection_url = get_collection_url(stac_item)

    # Convert collection to product definition
    product = collection_to_product(
        dc_index=dc.index,
        collection_url=collection_url
    )

    # Add product to datacube
    dc.index.products.add(product)

    # Get dataset
    dataset = stac_item_to_dataset(
        dc_index=dc.index,
        product_name=product.name,
        stac_item=item
    )

    # Do the indexing
    dc.index.datasets.add(dataset)

    print(f"http://localhost/products/{product.name}/datasets/{dataset.id}")


if __name__ == '__main__':
    main()
