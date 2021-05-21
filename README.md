## Akvelon python course study project.
[![codecov](https://codecov.io/gh/unbrokenguy/python-course/branch/main/graph/badge.svg?token=FWZ7B3PNCF)](https://codecov.io/gh/unbrokenguy/python-course)
* [Installation](#installation)
* [About](#about)
* [Setup](#setup)
## About  

Service for shortening links and file sharing, with the ability to register to track the statistics of created links and files. 

####Latest deployed version.
[https://python-course.sadmadsoul.dev](https://python-course.sadmadsoul.dev)

## Installation
Use python version 3.7 or higher 
### Install poetry
```shell
pip install poetry
```

### Install the project dependencies
```shell
poetry install 
```

## Setup

### Spawn a shell within the virtual environment
```shell
cd src && poetry shell
```
### Start current server
#### Add environments
* SECRET_KEY: Your secret key for django application.
* ALLOWED_HOST: Optional, standard value = 127.0.0.1
#### Start server
```shell
python manage.py runserver
```
Server will be available at this url  `http://localhost:8000/` or `http://127.0.0.1:8000/`
