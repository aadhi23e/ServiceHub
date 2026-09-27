# COMPOSE = docker compose -f docker-compose.local.yml
COMPOSE = docker compose

.PHONY: setup up down restart ps logs build test lint format-check typecheck check db-upgrade db-downgrade

setup:
	@echo "ServiceHub development environment initialized."

up:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) restart

ps:
	$(COMPOSE) ps

logs:
	$(COMPOSE) logs -f

build:
	$(COMPOSE) build

test:
	$(COMPOSE) run --rm backend pytest

lint:
	$(COMPOSE) run --rm backend ruff check app tests

format-check:
	$(COMPOSE) run --rm backend ruff format --check app tests

typecheck:
	$(COMPOSE) run --rm backend mypy app

check: lint format-check typecheck test

db-upgrade:
	$(COMPOSE) run --rm backend alembic upgrade head

db-downgrade:
	$(COMPOSE) run --rm backend alembic downgrade -1