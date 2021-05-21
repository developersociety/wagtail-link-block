.DEFAULT_GOAL := help
PROJECT_DIR=wagtail_link_block

help: ## Display this help dialog
help: help-display

format: ## Run this project's code formatters.
format: black-format isort-format

lint: ## Lint the project.
lint: black-lint isort-lint flake8-lint

# ISort
isort-lint:
	isort --check-only --diff ${PROJECT_DIR} setup.py

isort-format:
	isort ${PROJECT_DIR} setup.py

# Flake8
flake8-lint:
	flake8 ${PROJECT_DIR} setup.py

# Black
black-lint:
	black --check ${PROJECT_DIR} setup.py

black-format:
	black ${PROJECT_DIR} setup.py

# Help
help-display:
	@awk '/^[\-[:alnum:]]*: ##/ { split($$0, x, "##"); printf "%20s%s\n", x[1], x[2]; }' $(MAKEFILE_LIST)
