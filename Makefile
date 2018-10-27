DOCKER_COMPOSE = docker-compose -p app
TOOLS = @$(DOCKER_COMPOSE) run --rm api

build:
	@$(DOCKER_COMPOSE) build --force-rm

up:
	@$(DOCKER_COMPOSE) up -d --no-recreate

start:
	@$(DOCKER_COMPOSE) up --build

down:
	@$(DOCKER_COMPOSE) down

sh:
	@$(DOCKER_COMPOSE) exec api sh

logs:
	@$(DOCKER_COMPOSE) logs -f

psql:
	@$(DOCKER_COMPOSE) exec database psql postgresql://app:app@localhost:5432/app

migrate:
	@$(TOOLS) python manage.py migrate

makemigrations:
	@$(TOOLS) python manage.py makemigrations

showmigrations:
	@$(TOOLS) python manage.py showmigrations

shell:
	@$(TOOLS) python manage.py shell
