FROM satapps/dask-datacube:v3.2.22
ENV LC_ALL=C.UTF-8

RUN mkdir -p /src
COPY src/ /src/
COPY requirements.txt /src/requirements.txt

RUN pip install --upgrade pip
RUN pip install asyncio-nats-client==0.11.4 boto3~=1.17.8 botocore~=1.20.8
RUN apt-get --allow-releaseinfo-change update && apt-get install -y build-essential git
RUN pip install -e /src
RUN pip install --extra-index-url="https://packages.dea.ga.gov.au" odc-index sqlalchemy==1.3.20

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

CMD /wait && datacube system init && python /src/stac_to_dc/entrypoints/nats_consumer.py
