SHELL=/bin/bash
.DEFAULT_GOAL := help


# ---------------------------------
# Project specific targets
# ---------------------------------
#
# Add any targets specific to the current project in here.



# -------------------------------
# Common targets for DEV projects
# -------------------------------
#
# Edit these targets so they work as expected on the current project.
#
# Remember there may be other tools which use these targets, so if a target is not suitable for
# the current project, then keep the target and simply make it do nothing.

help: ## This help dialog.
help: help-display

clean: ## Remove unneeded files generated from the various build tasks.
clean: build-clean

reset: ## Reset your local environment. Useful after switching branches, etc.
reset: venv-check venv-wipe install-local

check: ## Check for any obvious errors in the project's setup.
check: pipdeptree-check

format: ## Run this project's code formatters.
format: ruff-format

lint: ## Lint the project.
lint: ruff-lint

test: ## Run unit and integration tests.
test: django-test

test-report: ## Run and report on unit and integration tests.
test-report: coverage-clean test coverage-report

test-lowest: ## Run tox with lowest (oldest) package dependencies.
test-lowest: tox-test-lowest

package: ## Builds source and wheel packages
package: clean build-package


# ---------------
# Utility targets
# ---------------
#
# Targets which are used by the common targets. You likely want to customise these per project,
# to ensure they're pointing at the correct directories, etc.

# Build
build-clean:
	rm -rf build
	rm -rf dist
	rm -rf .eggs
	find . -maxdepth 1 -name '*.egg-info' -exec rm -rf {} +

build-package:
	python -m build
	twine check --strict dist/*
	check-wheel-contents dist/*.whl


# Virtual Environments
venv-check:
ifndef VIRTUAL_ENV
	$(error Must be in a virtualenv)
endif

venv-wipe: venv-check
	if ! pip list --format=freeze | grep -v "^pip=\|^setuptools=\|^wheel=" | xargs pip uninstall -y; then \
	    echo "Nothing to remove"; \
	fi


# Installs
install-local: pip-install-local


# Pip
pip-install-local: venv-check
	pip install -r requirements/local.txt


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


# ruff
ruff-lint:
	ruff check
	ruff format --check

ruff-format:
	ruff check --fix-only
	ruff format


# pipdeptree
pipdeptree-check:
	pipdeptree --warn fail >/dev/null


# Project testing
django-test:
	PYTHONWARNINGS=all coverage run $$(which django-admin) test --pythonpath $$(pwd) --settings tests.settings tests

tox-test-lowest:
	tox --recreate --override testenv.uv_resolution=lowest


# Help
help-display:
	@awk '/^[\-[:alnum:]]*: ##/ { split($$0, x, "##"); printf "%20s%s\n", x[1], x[2]; }' $(MAKEFILE_LIST)
