FROM opendatacube/geobase:wheels as env_builder
COPY requirements.txt /
RUN env-build-tool new /requirements.txt /env

FROM opendatacube/geobase:runner
COPY --from=env_builder /env /env
ENV LC_ALL=C.UTF-8
ENV PATH="/env/bin:${PATH}"

RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src
RUN pip install --extra-index-url="https://packages.dea.ga.gov.au" odc-index

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

CMD /wait && datacube system init && tail -f /dev/null
