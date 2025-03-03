# pydo

This project was bootstrapped from this cookiecutter template of mine: <https://github.com/tiagoprn/celery-db-flask-cookiecutter>.


## Overview

This project provides a RESTful API for a simple task management system using Flask.

The API allow users to:

- Create, read, update, and delete tasks.
- Assign tasks to users.
- Mark tasks as completed.
- Filter tasks based on status and due date.


## Test coverage

``` bash

---------- coverage: platform linux, python 3.13.1-final-0 -----------
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
pydo/__init__.py         3      0   100%
pydo/api.py            162      9    94%   21-23, 72-74, 151-152, 190, 470
pydo/commons.py         47      8    83%   23-27, 40-41, 91, 93
pydo/exceptions.py       5      3    40%   3-5
pydo/extensions.py      49      0   100%
pydo/factory.py         14      0   100%
pydo/models.py         122      5    96%   69, 131, 135-136, 170
pydo/settings.py        34      2    94%   15, 52
pydo/tasks.py           15      3    80%   21-28
--------------------------------------------------
TOTAL                  451     30    93%


Results (17.11s):
      32 passed

```


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

- `pytest` for unit tests, with some plugins to ease presentation.

- `Makefile` to wrap the most common operations and ease project management, with commands to run the development server, shell, etc...

- code style and quality: `ruff` as the linter and formatter (customized with `pyproject.toml`)

- environment variables for configuration (`.env` file)

- Provides a `docker-compose.yml` to set up the development environment:
    - configured with the app required infrastructure (postgresql, rabbitmq)
    - `PostgreSQL` as the database , with `SQLAlchemy` as the abstraction layer
    - Background task processing using `Celery` with `RabbitMQ` as the broker


## How to run this project locally (development environment)

- This requires the installation of python's `uv` package manager. To install it:

``` bash

$ curl -LsSf https://astral.sh/uv/install.sh | sh

```

- Create a virtualenv to the project. If you want to use the default provided using uv on the Makefile:

``` bash

$ make dev-setup-uv

```

- Install the development requirements (also using uv):

``` bash

$ make requirements

```


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

``` bash

$ make dev-runserver

```


Then, check the api documentation URL:

``` bash

$ make dev-api-docs

```


- Start the development worker:

``` bash

$ make dev-runworker

```


## etc

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

### run a specific test with pytest

``` bash

$ pytest -s -k 'test_models' -vvv  --disable-warnings

```


## Potential enhancements

- `PATCH /user`: implement current password confirmation and new password confirmation (2nd time to check their are equal)

- implement user removal

- RBAC implementation (an admin user could create new users, update other users information, etc...)

- Audit trail for changes on user/task tables

- implement rate limiting

- populate the database with some tasks - using a `flask shell` script; add command to the Makefile

- Provides a `Dockerfile`
    - docker/podman image generation (properly tagged)

- API documentation using `Flasgger` (`Swagger` wrapper) as documentation for the API, using doctrings on the API endpoints to write the documentation.

- `gunicorn` configured to run the project in the production environment.

- pre-commit hook (install `pre-commit` through `uv` and put command on the `Makefile` to do that)

- Use "git-secret": migrate `.env.JWT_SECRET_KEY` to there

- CI pipeline (github actions):
    - ruff lint/format check
    - tests (with coverage report)

- Apply Clean/Hexagonal Architecture
