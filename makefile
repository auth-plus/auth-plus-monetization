.PHONY: infra/up
infra/up:
	docker compose up -d
	HOST=localhost make migration/up

.PHONY: infra/down
infra/down:
	docker compose down -v

.PHONY: dev
dev:
	make infra/up
	docker compose exec api sh

.PHONY: test
test:
	make infra/up
	docker compose exec -T api coverage run -m pytest
	make clean/docker

.PHONY: ci
ci:
	uv run black src/
	uv run flake8 src/
	uv run isort src/
	uv run mypy src/ --check-untyped-defs
	uv run black tests/
	uv run flake8 tests/
	uv run isort tests/

.PHONY: ci_test
ci_test:
	uv run black tests/
	uv run flake8 tests/
	uv run isort tests/
	uv run mypy tests/ --check-untyped-defs

.PHONY: clean/docker
clean/docker:
	make infra/down
	docker container prune -f
	docker volume prune -f
	docker image prune -f
	docker network prune -f
	rm -rf db/schema.sql
	rm -f db/schema.sql

.PHONY: clean/python
clean/python:
	find . | grep -E "(/__pycache__$|\.mypy_cache$|\.pytest_cache$|\.pyc$|\.pyo|\.venv$\)" | xargs sudo rm -rf

.PHONY: migration/up
migration/up:
	docker run -t --network=host -v "$(shell pwd)/db:/db" ghcr.io/amacneil/dbmate:1.16 --url postgres://root:db_password@$(HOST):5432/monetization?sslmode=disable --wait --wait-timeout 60s --no-dump-schema up