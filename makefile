.PHONY: infra/up
infra/up:
	docker compose up -d

.PHONY: infra/down
infra/down:
	docker compose down

.PHONY: dev
dev:
	make infra/up
	docker compose exec api sh

.PHONY: test
test:
	make infra/up
	docker compose exec -T api poetry install
	docker compose exec -T api npm test
	make clean/docker

.PHONY: clean/node
clean/node:
	rm -rf node_modules
	rm package-lock.json

.PHONY: clean/docker
clean/docker:
	make infra/down
	docker container prune -f
	docker volume prune -f
	docker image prune -f
	docker network prune -f
	rm -rf db/schema.sql
	rm -f db/schema.sql