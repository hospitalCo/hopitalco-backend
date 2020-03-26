# hopitalco-backend

[![Build Status](https://travis-ci.org/hospitalCo/hopitalco-backend.svg?branch=master)](https://travis-ci.org/hospitalCo/hopitalco-backend)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Providing a simple, focussed marketplace for healthcare.. Check out the
project's [documentation](http://hospitalCo.github.io/hopitalco-backend/).

## Getting started
You'll need Docker and ideally a recent python installation. Choose your poison :snake:

+ [Only Postgres in Docker](#1-local-development-with-postgres-in-docker-recommended)
+ [Nothing inside Docker](#2-local-development-on-your-machine-no-docker-recommended)
+ [Everything inside Docker](#3-local-development-using-docker-not-recommended)

> #### A kind request
> After you choose one of the two recommended ways to set up, we suggest that you
> mount the `pre-commit` hooks:
> 
> ``` bash
> pre-commit install
> ```
> 
> Be a bit patient, this downloads some python packages -- trust us, this will
> supercharge :zap: :zap: your development experience!

## (1) Local development with Postgres in Docker (recommended)
Like most people, you'd like to keep the code on your machine and maybe just the
DB inside docker. That works best.

### Set up python env
1. Set up a vitual environment using any manager of your choice (or simply
   `python -m venv .pyenv`) -- and activate it.
2. Install the deps:\
   `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` (and _ideally_ don't edit it).

### Up the services
```bash
docker-compose up -d postgres documentation

# to see logs/stdout attach a shell
docker logs -f <postgres-container-name> # or <documentation-container-name>
```
This will launch only the Postgres and documentation services inside docker.

### Edit and hot-reload
The django app will load your `.env` to pick the Postgres configuration. Run the
app:

``` bash
python manage.py runserver
```

or generate and run migrations as usual :tada:
``` bash
python manage.py migrate
```
### Inspecting the DB
Want to inspect the shell using `psql`?

``` bash
psql -U postgres -d development -h localhost -p 8002
```

## (2) Local development on your machine (no Docker, recommended)
1. Set up a vitual environment using any manager of your choice (or simply
   `python -m venv .pyenv`).
2. `pip install -r requirements.txt`
3. Install Postgres 12 on your machine (lower versions may work absolutely fine
   and are untested).
4. Copy the `.env.example` to `.env` and edit it to suit your installation of
   Postgres.
5. Do your thing :tada:

## (3) Local Development using Docker (not recommended)
You can do most development without setting up any python packages/environments
on your local machine -- keeping the code and the DB inside docker.

### Up the services
```bash
docker-compose up -d

# to see logs/stdout attach a shell
docker logs -f web # or <postgres-container-name> or <documentation-container-name>
```

### Edit and hot-reload
By default the docker container will watch for local changes you make using your
editor and reload the server (typical django).

### Cons
The only problem is running migrations, you'll have to resort to
```bash
docker-compose run --rm web "python migrate.py migrate"
```
