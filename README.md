# Auth+ Monetization Service

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=auth-plus_auth-plus-monetization&metric=coverage)](https://sonarcloud.io/summary/new_code?id=auth-plus_auth-plus-monetization)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/c4ceb5e2b57948b7af282f3f58f87ab9)](https://app.codacy.com/gh/auth-plus/auth-plus-monetization/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![Known Vulnerabilities](https://snyk.io/test/github/auth-plus/auth-plus-monetization/badge.svg)](https://snyk.io/test/github/auth-plus/auth-plus-monetization)

The `auth-plus-monetization` service is the core monetization and metering engine for the Auth+ ecosystem. It handles usage-based event pricing, financial credit ledgers, multi-model billing subscriptions (pre-paid and post-paid), plan conversions, and billing orchestration with the `auth-plus-billing` service.

Built with **Python 3.14+**, **FastAPI**, **SQLAlchemy**, and **PostgreSQL 17**, following strict **Hexagonal Architecture (Ports & Adapters)** principles.

---

## Table of Contents

- [Overview & Architecture](#overview--architecture)
- [Monetization Models & Business Rules](#monetization-models--business-rules)
  - [Subscription Types](#subscription-types)
  - [Immutable Credit & Debit Ledger](#immutable-credit--debit-ledger)
  - [Event Metering & Pricing Catalog](#event-metering--pricing-catalog)
  - [Plan Conversions](#plan-conversions)
- [Database Schema (Entity-Relationship)](#database-schema-entity-relationship)
- [REST API Reference](#rest-api-reference)
- [Kafka Event-Driven Architecture](#kafka-event-driven-architecture)
- [Background Workers & Automation](#background-workers--automation)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [1. Environment Setup](#1-environment-setup)
  - [2. Infrastructure with Docker](#2-infrastructure-with-docker)
  - [3. Running the Application](#3-running-the-application)
- [Development, Testing & Code Quality](#development-testing--code-quality)
- [Troubleshooting & Dev Tips](#troubleshooting--dev-tips)

---

## Overview & Architecture

The application adopts **Hexagonal Architecture (Ports & Adapters)** to decouple core business logic from database engines, message queues, and HTTP frameworks:

```text
auth-plus-monetization/
├── db/                        # Database migrations (dbmate) and ER diagrams
│   ├── migrations/            # Versioned SQL migration files
│   └── MER.png                # Database diagram
├── src/
│   ├── config/                # Environment variables, database connection, observability
│   │   ├── database.py        # SQLAlchemy engine & session maker
│   │   ├── envvar.py          # Environment settings
│   │   ├── logger.py          # Structured logging
│   │   └── observability.py   # OpenTelemetry / Uptrace initialization
│   ├── core/                  # Core Business Domain (Framework-agnostic)
│   │   ├── entity/            # Domain Entities (Account, Transaction, Event, Discount, etc.)
│   │   ├── helpers.py         # Domain errors and utility functions
│   │   ├── repository/        # Driven Adapters (SQLAlchemy repositories & HTTP Billing client)
│   │   └── usecase/           # Business Use Cases & Driving Logic
│   │       └── driven/        # Driven Ports (Abstract interfaces for repositories & services)
│   └── presentation/          # Driving Adapters (Entrypoints)
│       ├── server.py          # FastAPI REST HTTP server
│       ├── worker.py          # Scheduled background worker (daily automated charges)
│       └── kafka.py           # Kafka event consumer
└── tests/                     # Unit and integration test suite
```

---

## Monetization Models & Business Rules

### Subscription Types

The platform supports multiple subscription models defined in `AccountType`:

1. **`PRE_PAID`**:
   - Customers purchase credits in advance via `POST /ledger/credit`.
   - The credit balance is credited only after the payment invoice is settled in `auth-plus-billing`.
   - Each billable event (e.g. 2FA SMS, email verification) deducts from the customer's balance.
   - Customers cannot purchase specific events directly; they purchase general credit amount.
2. **`POST_PAID_MONTH`**:
   - Customers consume events throughout the billing cycle.
   - Each event deducts locally on the ledger for real-time auditability and immediately adds an `InvoiceItem` to an open `Draft` invoice on `auth-plus-billing`.
   - Invoices are automatically settled and charged monthly (or on demand).
3. **`POST_PAID_SEMESTER`** & **`POST_PAID_ANNUAL`**:
   - Extended billing windows charged on recurring semester or annual anniversary dates.

### Immutable Credit & Debit Ledger

- **Append-Only Accounting:** The `ledger` table records every financial mutation. Rows are **never updated** (except for linking a `charge_id` upon post-paid settlement) and **never deleted**.
- **Auditability:** Total balance (`GET /ledger/{external_id}`) is dynamically derived from the sum of all positive credits (`amount > 0`) and negative event debits (`amount < 0`).

### Event Metering & Pricing Catalog

The platform charges for system events using the `price` table:

| Event Type (`price.event`) | Description | Default Unit Price |
| :--- | :--- | :--- |
| `EMAIL_AUTH_FACTOR_CREATED` | Creation of email authentication factor | R$ 1.01 |
| `PHONE_AUTH_FACTOR_CREATED` | Creation of SMS/Phone authentication factor | R$ 1.02 |
| `EMAIL_AUTH_FACTOR_SENT` | Dispatch of 2FA verification email | R$ 1.03 |
| `PHONE_AUTH_FACTOR_SENT` | Dispatch of 2FA verification SMS | R$ 1.04 |
| `USER_CREATED` | User registration event | R$ 1.05 |
| `ORGANIZATION_CREATED` | Organization tenant creation event | R$ 1.06 |

### Plan Conversions

Users can seamlessly migrate between billing models:

- **Pre-Paid $\rightarrow$ Post-Paid (`PATCH /account/to_post_paid`):**
  - The remaining credit balance is computed.
  - If positive balance exists, an `ABSOLUTE` discount record is created in the `discount` table.
  - The subscription is converted to `POST_PAID_MONTH`, allowing the user to enjoy a discount on their upcoming post-paid invoice.
- **Post-Paid $\rightarrow$ Pre-Paid (`PATCH /account/to_pre_paid`):**
  - Unbilled debits accumulated in the current cycle are calculated.
  - Existing discounts (absolute or percentage) are applied.
  - Any remaining debit is billed and charged immediately via `auth-plus-billing`.
  - The subscription is converted back to `PRE_PAID`.

---

## Database Schema (Entity-Relationship)

![Database ER Diagram](./db/MER.png "Database Diagram")

### Primary Tables

- **`account`**: Stores the root account associated with the platform's `external_id`.
- **`subscription`**: Tracks active and historic subscription plan types (`PRE_PAID`, `POST_PAID_MONTH`, etc.) and effective dates.
- **`ledger`**: Immutable audit log of financial transactions (`amount`, `description`, `price_id`, `charge_id`).
- **`price`**: Catalog defining prices for each billable event type.
- **`discount`**: Stores absolute or percentage discounts applied to accounts.

---

## REST API Reference

The HTTP server exposes the following endpoints (default port: `5004`):

| Method | Endpoint | Description | Request Body Example |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Healthcheck and service readiness | _None_ |
| `POST` | `/account` | Initialize a monetization account | `{"external_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}` |
| `GET` | `/ledger/{external_id}` | Retrieve total current credit balance | _None_ (path parameter `external_id`) |
| `POST` | `/ledger/credit` | Buy pre-paid credits (triggers billing charge) | `{"external_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "amount": 50.0}` |
| `POST` | `/ledger/debit` | Meter and debit a billable event | `{"external_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "event": "PHONE_AUTH_FACTOR_SENT"}` |
| `POST` | `/charge` | Trigger billing settlement for post-paid accounts | `{"external_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "date_start": "2026-01-01T00:00:00"}` |
| `PATCH` | `/account/to_post_paid` | Migrate account from Pre-Paid to Post-Paid | `{"external_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}` |
| `PATCH` | `/account/to_pre_paid` | Migrate account from Post-Paid to Pre-Paid | `{"external_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}` |

---

## Kafka Event-Driven Architecture

The Kafka consumer (`src.presentation.kafka`) subscribes to internal event topics and automatically processes them:

| Topic | Triggered Action | Result |
| :--- | :--- | :--- |
| `USER_CREATED` | `core.account_create.create(external_id)` | Creates initial Pre-Paid account |
| `ORGANIZATION_CREATED` | `core.account_create.create(external_id)` | Creates initial Pre-Paid account |
| `2FA_EMAIL_CREATED` | `core.receive_event.receive_event(external_id, topic)` | Meters and debits email factor creation |
| `2FA_PHONE_CREATED` | `core.receive_event.receive_event(external_id, topic)` | Meters and debits phone factor creation |
| `2FA_EMAIL_SENT` | `core.receive_event.receive_event(external_id, topic)` | Meters and debits email 2FA dispatch |
| `2FA_PHONE_SENT` | `core.receive_event.receive_event(external_id, topic)` | Meters and debits SMS 2FA dispatch |

---

## Background Workers & Automation

The scheduled worker (`src.presentation.worker`) executes periodically using the `schedule` library:

- **Daily Billing Automation (`02:00 UTC`):**
  - Queries all active post-paid accounts due for billing on the current date (`by_subscription_period`).
  - Fetches the active `Draft` invoice from `auth-plus-billing`.
  - Executes immediate payment capture (`POST /charge`).
  - Associates the generated `charge_id` with all unbilled entries in the `ledger`.

---

## Prerequisites

- **Python:** `v3.14+`
- **Poetry:** `v2.0+`
- **Docker & Docker Compose:** `v23.0+`
- **dbmate:** `v1.16+` (for managing schema migrations)

---

## Getting Started

### 1. Environment Setup

Copy or define your local environment variables (`.env`):

```bash
APP_NAME=auth-plus-monetization
PORT=5004
PYTHON_ENV=development
DATABASE_URL=postgresql+psycopg2://root:db_password@localhost:5432/monetization
KAFKA_URL=localhost:9092
UPTRACE_DSN=http://localhost:4317
BILLING_HOST=http://localhost:5002
```

Install Python dependencies:

```bash
poetry install
```

### 2. Infrastructure with Docker

Start database and supporting containers:

```bash
# Start PostgreSQL container and run dbmate migrations automatically
make infra/up

# Tear down infrastructure
make infra/down
```

### 3. Running the Application

```bash
# 1. Start the HTTP API Server (port 5004 with hot-reload)
poetry run uvicorn src.presentation.server:app --host 0.0.0.0 --port 5004 --reload

# 2. Start the Scheduled Background Worker
poetry run python -m src.presentation.worker

# 3. Start the Kafka Event Consumer
poetry run python -m src.presentation.kafka
```

---

## Development, Testing & Code Quality

### Code Formatting & Linting

```bash
# Run full CI suite (black, flake8, isort, mypy)
make ci

# Or run individual tools
poetry run black src/ tests/
poetry run isort src/ tests/
poetry run flake8 src/ tests/
poetry run mypy src/ --check-untyped-defs
```

### Automated Tests

```bash
# Run unit & integration tests with coverage
poetry run coverage run -m pytest
poetry run coverage report -m

# Run specific test file
poetry run pytest tests/presentation/test_server.py

# Run specific test case
poetry run pytest tests/presentation/test_worker.py -k "test_worker_post_paid_automation_charge"

# Run tests in Docker container environment (mimics CI)
make test
```

### Database Migrations (dbmate)

Create a new migration:

```bash
dbmate new <migration_name>
```

Apply migrations manually:

```bash
make migration/up
```

---

## Troubleshooting & Dev Tips

### VS Code Python Interpreter

If VS Code fails to locate imported dependencies:

```bash
poetry config virtualenvs.in-project true
poetry env list
poetry env remove <env-name>
poetry install
```

Then in VS Code press `Ctrl+Shift+P` $\rightarrow$ `Python: Select Interpreter` $\rightarrow$ Select `.venv/bin/python`.

### Clean Python Caches

```bash
make clean/python
# or
find . | grep -E "(/__pycache__$|\.mypy_cache$|\.pytest_cache$|\.pyc$|\.pyo|\.venv$\)" | xargs sudo rm -rf
```

### Missing PostgreSQL System Libraries (psycopg2)

If building `psycopg2` from source on Debian/Ubuntu:

```bash
sudo apt update && sudo apt install -y python3-dev libpq-dev gcc
```

### Check Outdated Dependencies

```bash
poetry show -o
```
