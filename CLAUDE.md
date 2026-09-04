# Lazy Baker / Reckless Ham

A Wagtail-powered recipe website ("Reckless Ham") running on Django + PostgreSQL with AWS S3 for media/static storage.

## Stack

- **Python:** 3.12
- **Django:** 5.2
- **Wagtail:** 7.x
- **Database:** PostgreSQL 17 (via Docker)
- **Storage:** AWS S3 (static + media via `custom_storages.py`, using `django-storages`' `S3Boto3Storage`)
- **Web server:** Gunicorn
- **Dependency management:** `uv` (deps declared in `pyproject.toml`)
- **Config:** `python-decouple` reads from `.env`
- **Reverse proxy (production):** Caddy

## Project Layout

```
recipe_box/      Django project (settings, urls, wsgi, templates, static)
home/            Wagtail app — homepage and general site settings
recipes/         Wagtail app — recipe pages and template tags
images/          Custom Wagtail image model (CustomImage)
search/          Search and random recipe views
assets/          SCSS source files
custom_storages.py  S3 storage backends (StaticStorage, MediaStorage)
Dockerfile           App image (python:3.12-slim + uv)
docker-compose.yml   Local dev (web + db)
docker-compose.prod.yml  Production (web + db + caddy)
Caddyfile            Production reverse proxy config
```

## Environment Variables

Required in `.env` (see `.env.example`):

```
DEBUG=True
PRODUCTION=False
SECRET_KEY=...
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=lazy_baker
DB_HOST=db

# Production only:
DB_USER=...
DB_PASSWORD=...
AWS_STORAGE_BUCKET_NAME=...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

## Key Settings Behavior

- `PRODUCTION=False` → local DB (no user/password), static files served locally
- `PRODUCTION=True` → DB with user/password, static/media served from S3, `SECURE_PROXY_SSL_HEADER` enabled for HTTPS behind Caddy
- Media files always point to S3 (`DEFAULT_FILE_STORAGE` is always S3-backed)

## Running Locally

```bash
cp .env.example .env   # fill in values
docker compose up
docker compose exec web python manage.py migrate
docker compose exec web python manage.py update_index
docker compose exec web python manage.py createsuperuser
```

See `Makefile` for shortcuts (`make up`, `make migrate`, `make shell`, `make logs`) and `README.md` for full local dev / production instructions.

## Deployment

Push to `main` triggers `.github/workflows/deploy.yml`: builds and pushes the image to GHCR, copies `docker-compose.prod.yml` + `Caddyfile` to the Digital Ocean droplet, runs migrations/collectstatic/renditions/search-index update, health-checks `/health/`, and rolls back to the previous image on failure. A pre-deploy DB backup is taken automatically (last 5 kept).

## Wagtail Admin

- URL: `/admin/`
- Django admin: `/django-admin/`
- Custom image model: `images.CustomImage`
