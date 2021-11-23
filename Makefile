# This Makefile requires the following commands to be available:
# * python3.9
# * pip
# * docker
# * poetry
MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
MAKEFILE_DIR := $(shell dirname $(MAKEFILE_PATH))

IMAGE=bday-reminder-api
PYTHON=python3.9
export PYTHONPATH=$(shell echo $(MAKEFILE_DIR))/src
RUN_WITH_PYTHON_PATH=


# When we are not in Docker we assume poetry usage
ifneq ($(IN_DOCKER), 1)
  RUN_WITH_PYTHON_PATH=poetry run
endif


run:
	$(RUN_WITH_PYTHON_PATH) $(PYTHON) src/manage.py runserver


# migrate on dev environment
.PHONY: migrate
migrate:
	$(RUN_WITH_PYTHON_PATH) $(PYTHON) src/manage.py migrate --noinput
	@echo 'migrate done!'


# ********** Static files **********

collectstatic:
	$(RUN_WITH_PYTHON_PATH) $(PYTHON) src/manage.py collectstatic --noinput
	@echo 'collectstatic done!'


# ********** Docker **********

docker/build/%:
	docker build --no-cache -t $(IMAGE):$* .

docker/run: requirements.txt docker/build/dev
	docker run --rm -p 8000:8000 -e DEBUG=true $(IMAGE):dev


# ****** Tests ******

.PHONY: prepare_dev_packages
test_local: prepare_dev_packages lint pytest
	@echo 'Tests are done!'

ifneq ($(IN_DOCKER), 1)
prepare_dev_packages:
	@poetry install
else
prepare_dev_packages:
	# install globally since we are in docker
	pip install -r requirements.dev.txt
endif

pytest:
	$(RUN_WITH_PYTHON_PATH) py.test src/tests -svv --cov-report=term-missing --cov-report=html --cov-report=xml --cov=src --tb=short


# ********** Code style **********
.PHONY: lint lint/isort lint/flake8 lint/black format format/isort format/black
lint: lint/flake8 lint/isort lint/black

lint/isort:
	$(RUN_WITH_PYTHON_PATH) isort -c src

lint/flake8:
	$(RUN_WITH_PYTHON_PATH) flake8 src

lint/black:
	$(RUN_WITH_PYTHON_PATH) black --check src

format: format/isort format/black

format/isort:
	$(RUN_WITH_PYTHON_PATH) isort src

format/black:
	$(RUN_WITH_PYTHON_PATH) black --verbose src


# ********** Requirements **********
.PHONY: requirements.txt requirements.dev.txt
requirements: requirements.dev.txt requirements.txt

requirements.txt: poetry.lock
	@poetry export -f requirements.txt --output requirements.txt

requirements.dev.txt: poetry.lock
	poetry export --dev -f requirements.txt --output requirements.dev.txt

# Helper for docker build
install_requirements_txt:
	pip install -r requirements.txt
