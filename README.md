# Sample project with Django + DRF

[![GitHub tag](https://img.shields.io/github/tag/rodgomes/drf-quickstart?include_prereleases=&sort=semver&color=blue)](https://github.com/rodgomes/drf-quickstart/releases/)
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![code style - black](https://img.shields.io/badge/code_style-black-blue)](https://black.readthedocs.io/ "Go to Black homepage")

This project contains a simple API that is used to store people's birthdays. 

## Structure
Main folders are: 
- `src/api`: where the main code lives, including views (controllers), models (active records) and any other modules you would like.
- `src/config`: Djago settings, urls wsgi and asgi files (and any other configuration file you would like to put)
- `tests`: Where your tests will live

The project also includes some boilerplate utility files such as: Dockerfile and respective entrypoint.sh, Makefile with some utilities commands and setup.cfg for configuring linting, etc.

## Basic installation and usage

You need poetry in order to run this project locally. 
To install the dependencies
```
poetry install
```

Then execute the commands below to run locally with sqlite Database.
```
make migrate
make run
```

You should see the message below and can start calling the existing endpoints (see tests folder for details)
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```


## License

Released under [MIT](/LICENSE) by [@rodgomes](https://github.com/rodgomes).
