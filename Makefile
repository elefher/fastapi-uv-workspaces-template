SHELL := /bin/bash

# Variables
SYSTEM_PYTHON = $(or $(shell which python3), $(shell which python))
VIRTUAL_ENV = $(PWD)/.venv
DOCKER_COMPOSE_DEV_FILES := -f ./docker/docker-compose.yml
SERVICE_NAME := app
PYTEST_CMD := uv run pytest --cov=. --cov-report=term-missing

help: ## Display this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	@uv sync

build: ## Build the Docker container for the application
	@echo "Building application..."
	@docker compose $(DOCKER_COMPOSE_DEV_FILES) build --no-cache

up: ## Start the Docker container for the application
	@docker compose $(DOCKER_COMPOSE_DEV_FILES) up

logs: ## Display logs from the running Docker container
	@docker compose $(DOCKER_COMPOSE_DEV_FILES) logs

down: ## Stop and remove Docker containers and networks
	@docker compose $(DOCKER_COMPOSE_DEV_FILES) down

run-tests: ## Run tests inside the Docker container
	@docker compose $(DOCKER_COMPOSE_TEST_FILES) run --rm $(SERVICE_NAME) $(PYTEST_CMD)

shell: ## Open a bash shell inside the running Docker container
	@docker compose $(DOCKER_COMPOSE_DEV_FILES) run --rm $(SERVICE_NAME) bash

format: ## Format Python code using ruff
	@uv run ruff format app packages
	@uv run ruff check --extend-select I --fix app packages

type-check: ## Perform type checking using mypy
	@uv run mypy app packages

update-lock: ## Update uv.lock file with the latest dependencies
	@uv lock --upgrade
