# Auth+ Monetization

This project it's a sample for monetization system. It use a hexagonal architeture with layer for dependency manager.

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=auth-plus_auth-plus-monetization&metric=coverage)](https://sonarcloud.io/summary/new_code?id=auth-plus_auth-plus-monetization)

[![Test Coverage](https://api.codeclimate.com/v1/badges/61f1c963ee5c1420d31b/test_coverage)](https://codeclimate.com/github/auth-plus/auth-plus-monetization/test_coverage)

[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/c4ceb5e2b57948b7af282f3f58f87ab9)](https://app.codacy.com/gh/auth-plus/auth-plus-monetization/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)

## Documentation

### Table Event-Price

- The table event-price should be public
- This table contains all information regard event and cost of it
- Price can be different between plan's type for the same event

### Types of plan

There will be two types of monetization: Pre-Paid and Post-Paid.

#### Pre-Paid

Pre paid organizations will paid before usage, which means that each event will be disconted on the credit. They can not buy events, they can only buy credit.

#### Post-Paid

Post paid organizations will be charged after usage, which means that each month will be calculated all events used and will be charged. All clients must choose a day to be charged except 29, 30, 31

#### Change plan type

In ocasion of changing, only exist 2 possibility

- Pre->Post: everything goes normal, except that on the first charge will contain a discount on the value of credit
- Post->Pre: a charge will be created at the time containing all event. Then from this client will follow the flow of Pre-Paid

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
poetry run flask --app src/presentation/server run --port $PORT

# Running formatter
poetry run black src/ -v

# Running lint
poetry run flake8 src/ -v
```
