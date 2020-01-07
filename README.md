# Lazy Baker

[lazybaker.juliaebert.com](http://lazybaker.juliaebert.com)

---

## Setup

Install system dependencies: `sudo apt install libpq-dev python3-venv python3-pip postgresql postgresql-contrib`

Create virtual environment: `python3 -m venv venv`

Activate virtual environment: `source venv/bin/activate`

Install dependencies: `pip3 install -r requirements.txt`

Create a `.env` or `settings.ini` file with the following:
```shell
[settings]
DEBUG=True
PRODUCTION=False
SECRET_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
ALLOWED_HOSTS=*
DB_NAME=recipe_box_db
```

- `DEBUG` (True or False) sets the Django debug variable. Do not use `DEBUG=True` in production.
- `PROUDCTION` determines whether the production static/media content (AWS vs local) is used, and whether to use production database settings.
- `SECRET_KEY` is the Django secret key
- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are the credentials for hosting static/media data on AWS S3
- `ALLOWED_HOSTS` is the allowed host for the site to appear on. It shouldn't *really* be `*` (any host).
- `DB_NAME` is the database name in Postgres.

The following parameters are required if you are in a production setting (otherwise, they'll be ignored):
```shell
DB_USER=XXXXXXXXXXX
DB_PASSWORD=XXXXXXXXXX
```

Create/update the database: `python3 manage.py migrate`

- If you get the error `role "USERNAME" does not exist`, create the user with `sudo -u postgres createuser USERNAME`
- If you get the error `database "recipe_box_db" does not exist`, create it:
  - Run as postgres user: `sudo -i -u postgres`
  - Create database: `createdb recipe_box_db`
  - Get out: `exit`
- If you want to copy the existing database from Heroku as a starting place, [follow these instructions](https://docs.juliaebert.com/programming/web#copy-heroku-database-locally-for-django-project)

Run the server: `python3 manage.py runserver`
