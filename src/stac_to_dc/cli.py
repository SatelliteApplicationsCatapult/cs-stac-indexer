from typing import Tuple

from datacube import Datacube
from datacube import model, index

import click as click
from datacube.index.hl import Doc2Dataset
from odc.index.stac import stac_transform, stac_transform_absolute
from stac_to_dc.domain.operations import get_item


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


@click.command("stac-to-dc")
@click.argument("stac-item", type=str, nargs=1)
@click.argument("product", type=str, nargs=1)
def main(stac_item, product):

    dc = Datacube()

    # Get (stac, uri, relative_uri) tuples
    item = get_item(stac_item)

    # Get dataset
    dataset = stac_item_to_dataset(
        dc_index=dc.index,
        product_name=product,
        stac_item=item
    )

    # Do the indexing
    dc.index.datasets.add(dataset)

    print(f"http://localhost/products/{product}/datasets/{dataset.id}")


if __name__ == '__main__':
    main()
