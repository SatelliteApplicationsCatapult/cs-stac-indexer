FROM opendatacube/geobase:wheels as env_builder
COPY requirements.txt /
RUN env-build-tool new /requirements.txt /env

FROM opendatacube/geobase:runner
COPY --from=env_builder /env /env
ENV LC_ALL=C.UTF-8
ENV PATH="/env/bin:${PATH}"

RUN mkdir -p /src
COPY src/ /src/
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y build-essential git

RUN pip install --extra-index-url="https://packages.dea.ga.gov.au" odc-index sqlalchemy==1.3.20
RUN pip install -e /src


# ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
# RUN chmod +x /wait

CMD datacube system init && python /src/stac_to_dc/entrypoints/nats_consumer.py