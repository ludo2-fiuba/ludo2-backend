# Python implementation of Libreta Universitaria Digital Oficial

## Run Locally

### Requirements
- Python3
- PostgreSQL

### Setup dependencies
```
1. Get Python 3.7+
2. Install pip
3. pip3 install -r requirements.txt
```

### Setup DB
Create role and database 'ludo' with password 'ludo' locally.
```
sudo -u postgres psql;
create database ludo;
```

### Setup initial data
Run the following every time the database is created from scratch:
- python3 manage.py migrate
- python3 manage.py initdata

## Migrate
For each change in your models that implicates a change in the data stored in the database, you will
have to run the following
- `python3 manage.py makemigrations` to create migrations for those changes
- `python3 manage.py migrate` to apply those changes to the database.

## Run Server
Run
```
python3 manage.py runserver
```
The server will start by default on the port 8000

## Run with Docker

### Requirements
- Docker

### Run server
Run
```
docker-compose up --build
```
The server will start by default on the port 8007

## API Specification
The endpoints of the API are exemplified in Postman in the following collection: https://www.getpostman.com/collections/d34849a7f0ccdae5831f


## Deployed application
The application is running at `https://ludo-backend.herokuapp.com`

## License
This source code is property of er-inc and cannot be publicly distributed without explicit consent.

This project is maintained by **Federico Esteban** (fede.est@gmail.comn) and **Daniela Riesgo** (daniealp.riesgo@gmail.com)
