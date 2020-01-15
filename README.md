# Python implementation of Libreta Universitaria Digital Oficial

## Requirements
- Python3
- Django
- PostgreSQL

## Setup dependencies
```
1. Get Python 3.7+
2. Install pip
3. pip3 install -m requirements.txt
```

## Setup DB
Create role and database 'ludo' with password 'ludo' locally.
```
sudo -u postgres psql;
create database ludo;
create user ludo with encrypted password 'ludo';
grant all privileges on database ludo to ludo;
```

## Migrate
- Change your models (in models.py).
- Run python3 manage.py makemigrations to create migrations for those changes
- Run python3 manage.py migrate to apply those changes to the database.

## Things to check up eventually
- https://django-localflavor.readthedocs.io/en/latest/
