# from python3.8
FROM python:3.8
# COPY requirements.txt /
# RUN env-build-tool new /requirements.txt /env
# FROM opendatacube/geobase:runner
# COPY --from=env_builder /env /env
# ENV LC_ALL=C.UTF-8
# ENV PATH="/env/bin:${PATH}"
# RUN mkdir -p /src
# COPY src/ /src/
# RUN pip install --upgrade pip
# RUN apt-get update && apt-get install -y build-essential git
COPY . .
RUN pip install --extra-index-url="https://packages.dea.ga.gov.au" odc-index
# RUN python /src/setup.py install
# ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
# RUN chmod +x /wait
WORKDIR /src
RUN python3 setup.py install
CMD datacube system init && python3 -m stac_to_dc.entrypoints.nats_consumer

