.PHONY: up down build test migrate shell logs

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose up -d --build

migrate:
	docker compose exec web python manage.py migrate

shell:
	docker compose exec web python manage.py shell

logs:
	docker compose logs -f web

test:
	python smoke_test.py
