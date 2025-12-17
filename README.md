# Auth+ Monetization

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=auth-plus_auth-plus-monetization&metric=coverage)](https://sonarcloud.io/summary/new_code?id=auth-plus_auth-plus-monetization)

[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/c4ceb5e2b57948b7af282f3f58f87ab9)](https://app.codacy.com/gh/auth-plus/auth-plus-monetization/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)

[![Known Vulnerabilities](https://snyk.io/test/github/auth-plus/auth-plus-monetization/badge.svg)](https://snyk.io/test/github/auth-plus/auth-plus-monetization)

This project it's a sample for monetization system. It use a hexagonal architeture with layer for dependency manager.

## Documentation

### Table Event-Price

- The table event-price should be public
- This table contains all information regard event and cost of it
- Price can be different between plan's type for the same event

### Types of plan

There will be two types of subscription plans: Pre-Paid and Post-Paid.

#### Pre-Paid

Pre paid organizations will paid before usage, which means that each event will be disconted on the credit. They can not buy events, they can only buy credit.

#### Post-Paid

Post paid organizations will be charged after usage, which means that each month will be calculated all events used and will be charged. All clients must choose a day to be charged except 29, 30, 31

#### Change plan type

In ocasion of changing, only exist 2 possibility

- Pre->Post: everything goes normal, except that on the first charge will contain a discount on the value of credit
- Post->Pre: a charge will be created at the time containing all event. Then from this client will follow the flow of Pre-Paid

### Model Entity Relation

![diagram made by DBeaver](/db/MER.png "Database Diagram")

## Pré-requisite

- Docker v23.0.1
- Python v3.10.6

## Commands

```bash
# rise/destroy all dependency
make infra/up # already create tables based on ./db/migration folder
make infra/down # does not remove volume

# make test on the same condition where it's executed on CI
make test

# developer and test enviroment
make dev

# Installing dependency
poetry install

# Running HTTP server
poetry run uvicorn src.presentation.server:app --host 0.0.0.0 --reload
poetry run uvicorn src.presentation.server:app --host 0.0.0.0 --port 5004
poetry run python3 -m src.presentation.worker

# Running formatter
poetry run black src/

# Running lint
poetry run flake8 src/
poetry run isort src/
poetry run mypy src/ --check-untyped-defs

# Running test
poetry run coverage run -m pytest  # all tests
poetry run coverage run -m pytest tests/presentation/test_server.py # specific file
poetry run coverage run -m pytest tests/presentation/test_worker.py -k 'test_should_select_by_account_id' # specific test
```

## Dev Hints

### Setup for those who want develop on local machine

poetry: <https://python-poetry.org/docs/#installation>
python: <https://github.com/pyenv/pyenv>

### Creating new migrations with dbmate

Install dbmate (<https://github.com/amacneil/dbmate#installation>)
execute `dbmate new <name-of-migration>`

### VSCode does not resolve libs

First execute this commands

```bash
poetry config virtualenvs.in-project true
poetry env list
poetry env remove <name-of-enviroment> # remove the only listed env
poetry install
```

On VSCode select the interpreter with poetry

### Python not updating because cache folders

```bash
find . | grep -E "(/__pycache__$|.mypy_cache$|.pytest_cache$|.pyc$|.pyo$)" | xargs sudo rm -rf
```

### Psycopg2 problem when installing

```bash
sudo apt install python3-dev libpq-dev
```
