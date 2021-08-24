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

build: ## Build the project ready for deployment to pypi
build: dist

dist: setup.py
	python3 setup.py sdist bdist_wheel

deploy-test: ## Build and upload the project to TestPyPI (sandbox)
deploy-test: dist
	@echo You will need to manually run:
	@echo 'twine upload -r testpypi dist/*'

deploy: ## Build and upload the project to PyPI
deploy: dist
	@echo You will need to manually run:
	@echo 'twine upload dist/*'



# Help
help-display:
	@awk '/^[\-[:alnum:]]*: ##/ { split($$0, x, "##"); printf "%20s%s\n", x[1], x[2]; }' $(MAKEFILE_LIST)
