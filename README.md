# pydo

**DESCRIPTION:** A tasks management solution

created from: <https://github.com/tiagoprn/celery-db-flask-cookiecutter>

## Overview

This project provides a RESTful API for a simple task management system  using Flask.

The API allow users to:

- Create, read, update, and delete tasks.
- Assign tasks to users.
- Mark tasks as completed.
- Filter tasks based on status and due date.

## Architecture

See [this](ARCHITECTURE.md)

## Technologies

- `Python` 3.13 and `Flask` (3.1) as the web API framework.

- `uv` for packaging (requirements, additional tooling)

- JWT authentication.

- `bcrypt` for password hashing

- CRUD endpoints for managing tasks, with:
    - Pagination for listing tasks.
    - Filtering tasks by status and due date.

- Uses `PostgreSQL` as the database (containerized - `docker` or `podman`), with `SQLAlchemy` as the abstraction layer

- `pytest` for unit tests, with some plugins to ease presentation.

- tests coverage report (80% test coverage minimum)

- Provides a `Dockerfile` and `docker-compose.yml` to set up the app and database locally:
    - docker/podman image generation (properly tagged)
    - docker-compose configured with the app required infrastructure (rabbitmq as celery broker, postgresql as the database)

- API documentation using `Flasgger` (`Swagger` wrapper) as documentation for the API, using doctrings on the API endpoints to write the documentation.

- Rate limiting to prevent API abuse.

- Background task processing using `Celery` with `RabbitMQ` as the broker

- `Makefile` to wrap the most common operations and ease project management, with commands to run the development server, shell, etc...

- `gunicorn` configured to run the project in the production environment.

- code style and quality: `ruff` as the linter and formatter (customized with `pyproject.toml`)

- environment variables for configuration (`.env` file)

## Potential enhancements

- `PATCH /user`: implement current password confirmation and new password confirmation (2nd time to check their are equal)

- implement user removal

- RBAC implementation (an admin user could create new users, update other users information, etc...)

- Audit trail for changes on user/task tables

- Use "git-secret": migrate `.env.JWT_SECRET_KEY` to there

- CI pipeline (github actions):
    - ruff lint/format check
    - tests (with coverage report)

- Apply Clean/Hexagonal Architecture

## How to run this project locally (development environment)

### OPTION 1 - USING AN UV VIRTUALENV:

- This requires the installation of python's uv package manager. To install it:

``` bash

$ curl -LsSf https://astral.sh/uv/install.sh | sh

```

- Create a virtualenv to the project. If you want to use the default provided using uv on the Makefile:

``` bash
$ make dev-setup-uv
```

- Install the development requirements (also using uv):

`$ make requirements`

- Run the make command to create the sample configuration file:

``` bash
$ make init-env
```

- Now, the development infrastructure containers (postgressql, rabbitmq) must be started:

``` bash

$ make dev-infra-start

```

- Generate the db migrations and run them:

``` bash
$ make migrations
$ make migrate
```

- Run the formatter and linter:

NOTE: We use "ruff" as a python linter and formatter, due to its' speed.

If you do not have it installed, you can run this command first:

``` bash

$ make dev-setup-ruff

```

This will install ruff globally, but do not worry. It needs to be explicitly called and you can customize its' behavior per project if you need.

``` bash
$ make style; make style-autofix && make style
$ make lint; make lint-autofix && make lint
```

- Run the test suite:

``` bash
$ make test
```

- Start the development server:

`$ make dev-runserver`

... or start the production server (gunicorn):

`$ make runserver`

Then, check the api documentation URL:

`$ make dev-api-docs`

- Start the development worker:

`$ make dev-runworker`

... or start the production worker (gunicorn):

`$ make runworker`

### OPTION 2 - BUILD AND RUN FROM DOCKER/PODMAN

(TODO: this needs to be tested)

``` bash
$ make docker-build-local-app-container && make docker-run-local-app-container

or...

$ make podman-build-local-app-container && make podman-run-local-app-container
```

Then, check the api documentation:

`$ make dev-api-docs`

## etc

### run a specific test with pytest

``` bash

$ pytest -s -k 'test_models' -vvv  --disable-warnings

```

### pgcli

You can interact with the postgresql database (making queries) using a cli util called 'pgcli'. It provides some features like autocomplete and others.

To install it (uses uv):

``` bash

$ make dev-setup-pgcli

```

To connect to the database (using pgcli):

``` bash

$ make dev-pgcli

```
