build:
	docker-compose build

up:
	docker-compose up -d app

unit-tests:
	docker-compose run --rm --no-deps --entrypoint=pytest app /tests/unit

integration-tests: up
	docker-compose run --rm --no-deps --entrypoint=pytest app /tests/integration

tests: up unit-tests integration-tests

logs:
	docker-compose logs app | tail -100

down:
	docker-compose down --remove-orphans

all: down build tests