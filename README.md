# Lazy Baker

[lazybaker.juliaebert.com](http://lazybaker.juliaebert.com)

---

## Setup

Install system dependencies: `sudo apt install libpq-dev python3-venv python3-pip postgresql postgresql-contrib`

Create virtual environment: `python3 -m venv venv`

Activate virtual environment: `source venv/bin/activate`

Install dependencies: `pip3 install -r requirements.txt`

Create a `.env` file with the following:
```shell
DJANGO_SETTINGS_MODULE=recipe_box.settings.production
SECRET_KEY='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXxx'
AWS_ACCESS_KEY_ID='XXXXXXXXXXXXXXXX'
AWS_SECRET_ACCESS_KEY='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
```
and switching between `recipe_box.settings.production` and `recipe_box.settings.dev` as needed.

Create/update the database: `python3 manage.py migrate`

- If you get the error `role "USERNAME" does not exist`, create the user with `sudo -u postgres createuser USERNAME`
- If you get the error `database "recipe_box_db" does not exist`, create it:
  - Run as postgres user: `sudo -i -u postgres`
  - Create database: `createdb recipe_box_db`
  - Get out: `exit`
- If you want to copy the existing database from Heroku as a starting place, [follow these instructions](https://docs.juliaebert.com/programming/web#copy-heroku-database-locally-for-django-project)

Run the server: `python3 manage.py runserver`
