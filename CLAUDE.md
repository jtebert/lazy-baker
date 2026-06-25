# Lazy Baker / Reckless Ham

A Wagtail-powered recipe website ("Reckless Ham") running on Django + PostgreSQL with AWS S3 for media/static storage.

## Stack

- **Python:** 3.7.3 (target: 3.12)
- **Django:** 2.2.10 (target: 4.2 LTS)
- **Wagtail:** 2.8 (target: 5.2 LTS)
- **Database:** PostgreSQL
- **Storage:** AWS S3 (static + media via `custom_storages.py`)
- **Web server:** Gunicorn
- **Config:** `python-decouple` reads from `.env` or `settings.ini`

## Project Layout

```
recipe_box/      Django project (settings, urls, wsgi, templates, static)
home/            Wagtail app — homepage and general site settings
recipes/         Wagtail app — recipe pages and template tags
images/          Custom Wagtail image model (CustomImage)
search/          Search and random recipe views
assets/          SCSS source files
custom_storages.py  S3 storage backends (StaticStorage, MediaStorage)
```

## Environment Variables

Required in `.env` or `settings.ini`:

```
DEBUG=True
PRODUCTION=False
SECRET_KEY=...
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=lazy_baker
AWS_STORAGE_BUCKET_NAME=...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...

# Production only:
DB_USER=...
DB_PASSWORD=...
```

## Key Settings Behavior

- `PRODUCTION=False` → local DB (no user/password), static files served locally
- `PRODUCTION=True` → DB with user/password, static/media served from S3
- Media files always point to S3 (`DEFAULT_FILE_STORAGE` is always S3-backed)

## Running Locally (current, pre-Docker)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Upgrade Plan (in progress)

See project conversation for the full phased plan. Broad steps:

1. **Containerize** at current versions (Python 3.7, Django 2.2, Wagtail 2.8)
2. **Update S3 layer** — replace `boto` with `boto3`, update `django-storages`, rewrite `custom_storages.py`
3. **Step through Django + Wagtail LTS versions** — 2.8→2.16→3.0→5.2, Django 2.2→3.2→4.2
4. **Update Python** to 3.12 (via Docker base image change)
5. **Deploy** updated container to Digital Ocean

### Breaking changes to handle:
- Wagtail 3.0: `wagtail.core` → `wagtail`; `SiteMiddleware` removed
- Django 3.x: `url()` → `path()`/`re_path()`; `ugettext_lazy` → `gettext_lazy`
- S3: `S3BotoStorage` → `S3Boto3Storage`
- `dj-static`, `static3` — Heroku-era, remove when containerized
- `libsass`, `django-compressor` — may need replacement (libsass unmaintained)

## Wagtail Admin

- URL: `/admin/`
- Django admin: `/django-admin/`
- Custom image model: `images.CustomImage`
