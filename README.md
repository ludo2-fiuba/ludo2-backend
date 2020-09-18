# Python implementation of Libreta Universitaria Digital Oficial

## Requirements
- Python3
- Django
- PostgreSQL

## Setup dependencies
```
1. Get Python 3.7+
2. Install pip
3. pip3 install -r requirements.txt
```

## Setup DB
Create role and database 'ludo' with password 'ludo' locally.
```
sudo -u postgres psql;
create database ludo;
create user ludo with encrypted password 'ludo';
grant all privileges on database ludo to ludo;
```

## Start Server
Just run
```
python3 manage.py runserver
```
The server will start by default on the port 8000

## Migrate
For each change in your models that implicates a change in the data stored in the databse, you will
have to run the following
- `python3 manage.py makemigrations` to create migrations for those changes
- `python3 manage.py migrate` to apply those changes to the database.

## API Specification
The endpoints of the API are documented using Swagger 2.0 (pending OpenApi 3.0 availability) and are 
described in the following paths:
```
A JSON view of the API specification at /swagger.json
A YAML view of the API specification at /swagger.yaml
A swagger-ui view of the API specification at /swagger/
A ReDoc view of the API specification at /redoc/
```

## Deployed application
The application is running at `https://ludo-backend.herokuapp.com`

## License
This source code is property of er-inc and cannot be publicly distributed without explicit consent.

This project is maintained by **Federico Esteban** (fede.est@gmail.comn) and **Daniela Riesgo** (daniealp.riesgo@gmail.com)
