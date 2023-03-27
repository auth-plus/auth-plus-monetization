# Auth+ Monetization

This project it's a sample for monetization system. It use a hexagonal architeture with layer for dependency manager.

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

# Running HTTP server
poetry run flask --app src/presentation/server run --port $PORT

# Running formatter
poetry run black src/ -v

# Running lint
poetry run flake8 src/ -v
```
