# Datacube dev environment

``` docker
docker-compose up -d
```

## STAC indexer

Index a sample dataset using the `stac-to-dc` tool
``` docker
docker exec -it stac-indexer stac-to-dc stac-to-dc https://s3-uk-1.sa-catapult.co.uk/public-eo-data/stac_catalogs/cs_stac/catalog.json
```


## Datacube explorer

After all the environment is started and the database ready to receive requests, 
it is needed to initialise and generate the product summaries.

``` docker
docker exec -it datacube-explorer cubedash-gen --init --all
```

*NOTE*: Run this every time a new dataset is indexed
``` docker
docker exec -it datacube-explorer cubedash-gen --force-refresh
```

Open http://localhost/products to see the indexed dataset or http://localhost/stac to access the STAC API.

## Datacube Jupyter Notebook

Get the access link from the logs

``` docker
docker logs datacube-notebook
```

*NOTE*: The link should look like:

http://127.0.0.1:8888/?token=1f3b399aef1e98f11fc919b10602ed8cf8b1f3d69311440d