# Reckless Ham (formerly Lazy Baker)

[recklessham.com](http://recklessham.com)

---

## Stack

- **Python 3.12**, **Django 5.2**, **Wagtail 7**
- **PostgreSQL 17** (via Docker)
- **AWS S3** for static and media files in production
- **Gunicorn** as the application server
- **uv** for dependency management

## Local Development

### Setup

1. Copy the example env and fill in values:

```shell
cp .env.example .env
```

Required variables:

```shell
DEBUG=True
PRODUCTION=False
SECRET_KEY=<a-long-random-string>
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=lazy_baker
DB_HOST=db
```

AWS credentials are only needed when `PRODUCTION=True`. Leave them out for local development.

2. Start the containers:

```shell
docker compose up
```

3. On first run (or after restoring a database dump), run migrations and populate the search index:

```shell
docker compose exec web python manage.py migrate
docker compose exec web python manage.py update_index
```

4. Create a superuser to access the Wagtail admin:

```shell
docker compose exec web python manage.py createsuperuser
```

### Useful commands

```shell
# Run tests
docker compose exec web python manage.py test

# Open a Django shell
docker compose exec web python manage.py shell

# Rebuild containers after dependency changes
docker compose build
```

### Admin URLs

- Wagtail admin: http://localhost:8000/admin/
- Django admin: http://localhost:8000/django-admin/

## Production

Set `PRODUCTION=True` in the environment. This enables:

- Static and media files served from AWS S3
- Database authentication via `DB_USER` / `DB_PASSWORD`
- `SECURE_PROXY_SSL_HEADER` for HTTPS behind a proxy

Additional env variables required in production:

```shell
PRODUCTION=True
DEBUG=False
DB_USER=...
DB_PASSWORD=...
AWS_STORAGE_BUCKET_NAME=...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

After deploying, run:

```shell
python manage.py migrate
python manage.py update_index
python manage.py collectstatic --noinput
```
