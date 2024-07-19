.DEFAULT_GOAL := help
PROJECT_DIR=wagtail_link_block

help: ## Display this help dialog
help: help-display

format: ## Run this project's code formatters.
format: black-format isort-format

lint: ## Lint the project.
lint: black-lint isort-lint flake8-lint

check: ## Check for any obvious errors in the project's setup.
check: pipdeptree-check

test: ## Run unit and integration tests.
test: django-test

# ISort
isort-lint:
	isort --check-only --diff ${PROJECT_DIR}

isort-format:
	isort ${PROJECT_DIR}

# Flake8
flake8-lint:
	flake8 ${PROJECT_DIR}

# Black
black-lint:
	black --check ${PROJECT_DIR}

black-format:
	black ${PROJECT_DIR}

build: ## Build the project ready for deployment to pypi
build: dist

dist: pyproject.toml
	poetry build

deploy-test: ## Build and upload the project to TestPyPI (sandbox)
deploy-test: dist
	poetry publish -r test-pypi

deploy: ## Build and upload the project to PyPI
deploy: dist
	poetry publish


# pipdeptree
pipdeptree-check:
	pipdeptree --warn fail >/dev/null


# Coverage
coverage-report: coverage-combine coverage-html
	coverage report --show-missing

coverage-combine:
	coverage combine

coverage-html:
	coverage html

coverage-clean:
	rm -rf htmlcov
	rm -f .coverage


# Project testing
django-test:
	PYTHONWARNINGS=all coverage run $$(which django-admin) test --pythonpath $$(pwd) --settings tests.settings tests

tox-test-lowest:
	tox --recreate --override testenv.uv_resolution=lowest


# Help
help-display:
	@awk '/^[\-[:alnum:]]*: ##/ { split($$0, x, "##"); printf "%20s%s\n", x[1], x[2]; }' $(MAKEFILE_LIST)
