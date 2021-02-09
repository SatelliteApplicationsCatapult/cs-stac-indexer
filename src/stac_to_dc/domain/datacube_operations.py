from datacube import index, model


def create_product(dc_index: index.Index, product_definition: dict) -> model.DatasetType:
    return dc_index.products.from_doc(product_definition)
