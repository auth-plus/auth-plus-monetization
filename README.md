# Auth+ Monetization

This project it's a sample for monetization system. It use a hexagonal architeture with layer for dependency manager.

## Documentation

### Flow for monetization events

1. Event listened
2. Add invoice-item

### Flow for monetization schedule

1. Once a month create a draft invoice
2. Add invoice-item

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
