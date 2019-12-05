# Seed++

## Requirements:
- Python 3 with pip
- PostgreSQL

## Installation
- Clone the repository into a directory
- Run `pip install -r requirements.txt`
- Make sure your Postgres server is accessible via internet connection or hosted locally
- In ./seedplusplus/settings.py, change the DATABASES dictionary to point to a new database on your Postgres server, with all necessary credentials.
- Run `python manage.py migrate` to create all necessary database tables and schemas
- Run `python manage.py runserver` to start the server 