## Akvelon python course study project.
[![codecov](https://codecov.io/gh/unbrokenguy/python-course/branch/main/graph/badge.svg?token=FWZ7B3PNCF)](https://codecov.io/gh/unbrokenguy/python-course)
* [Installation](#installation)
* [About](#about)
* [Setup](#setup)
## About  

Service for shortening links and file sharing, with the ability to register to track the statistics of created links and files. 

#### Latest deployed version.
[https://python-course.sadmadsoul.dev](https://python-course.sadmadsoul.dev)

## Installation

### Install python version 3.7 or higher 
### Install docker and docker-compose

## Setup

### Start current server
#### Add environments
* SECRET_KEY: Your secret key for django application.
* ALLOWED_HOST: Optional, standard value = 127.0.0.1
* EMAIL_HOST: Email from which the server will send confirmation emails.
* EMAIL_HOST_PASSWORD: Email password.
#### Run tests
```shell
export CELERY_BROKER_URL="redis://127.0.0.1:6379"
docker-compose -f docker-compose.test.yml -d --build
cd src
coverage run -m pytest
coverage report --rcfile=.coveragerc
docker-compose -f docker-compose.test.yml down
```
#### Start server
```shell
docker-compose -f docker-compose.yml -d --build
```
Server will be available at this url  `http://localhost:8282/` or `http://127.0.0.1:8282/`
