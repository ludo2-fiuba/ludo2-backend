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
docker compose up --build
```
The server will start by default on the port 8007. Admin dashboard URL is http://localhost:8007/admin

#### Populate the Database

For the first time, you'll need to run a migration and seed the DB. For this run:
```bash
docker exec -it ludo2-backend-web-1 python3 manage.py migrate
docker exec -it ludo2-backend-web-1 python3 manage.py initdata
```

Debug: in case you want to explore the DB using PSQL, you can run:
```bash
docker exec -it ludo2-backend-db-1 psql --user ludo --db ludo_dev
```

And explore present tables with `\d [TABLE]`:
```
PS C:\Users\PC\Documents\repos\ludo2\ludo2-backend> docker exec -it ludo2-backend-db-1 psql --user ludo --db ludo_dev
psql (12.0)
Type "help" for help.

ludo_dev=# \d
                          List of relations
 Schema |                  Name                   |   Type   | Owner
--------+-----------------------------------------+----------+-------
 public | auth_group                              | table    | ludo
 public | auth_group_id_seq                       | sequence | ludo
 public | auth_group_permissions                  | table    | ludo
 public | auth_group_permissions_id_seq           | sequence | ludo
 public | auth_permission                         | table    | ludo
 public | auth_permission_id_seq                  | sequence | ludo
 public | authtoken_token                         | table    | ludo
 public | backend_final                           | table    | ludo
 public | backend_final_id_seq                    | sequence | ludo
 public | backend_finalexam                       | table    | ludo
 public | backend_finalexam_id_seq                | sequence | ludo
 public | backend_staff                           | table    | ludo
 public | backend_student                         | table    | ludo
 public | backend_teacher                         | table    | ludo
 public | backend_user                            | table    | ludo
 public | backend_user_groups                     | table    | ludo
 public | backend_user_groups_id_seq              | sequence | ludo
 public | backend_user_id_seq                     | sequence | ludo
 public | backend_user_user_permissions           | table    | ludo
 public | backend_user_user_permissions_id_seq    | sequence | ludo
 public | django_admin_log                        | table    | ludo
 public | django_admin_log_id_seq                 | sequence | ludo
 public | django_content_type                     | table    | ludo
 public | django_content_type_id_seq              | sequence | ludo
 public | django_migrations                       | table    | ludo
 public | django_migrations_id_seq                | sequence | ludo
 public | django_session                          | table    | ludo
 public | push_notifications_apnsdevice           | table    | ludo
 public | push_notifications_apnsdevice_id_seq    | sequence | ludo
 public | push_notifications_gcmdevice            | table    | ludo
 public | push_notifications_gcmdevice_id_seq     | sequence | ludo
 public | push_notifications_webpushdevice        | table    | ludo
 public | push_notifications_webpushdevice_id_seq | sequence | ludo
 public | push_notifications_wnsdevice            | table    | ludo
 public | push_notifications_wnsdevice_id_seq     | sequence | ludo
(35 rows)

ludo_dev=# \d backend_user
                                        Table "public.backend_user"
    Column    |           Type           | Collation | Nullable |                 Default
--------------+--------------------------+-----------+----------+------------------------------------------
 id           | integer                  |           | not null | nextval('backend_user_id_seq'::regclass)
 password     | character varying(128)   |           | not null |
 last_login   | timestamp with time zone |           |          |
 is_superuser | boolean                  |           | not null |
 email        | character varying(254)   |           | not null |
 is_staff     | boolean                  |           | not null |
 is_active    | boolean                  |           | not null |
 date_joined  | timestamp with time zone |           | not null |
 is_student   | boolean                  |           | not null |
 is_teacher   | boolean                  |           | not null |
 first_name   | character varying(50)    |           | not null |
 last_name    | character varying(50)    |           | not null |
 username     | character varying(30)    |           | not null |
 dni          | character varying(9)     |           | not null |
 created_at   | timestamp with time zone |           | not null |
 updated_at   | timestamp with time zone |           | not null |
```

## API Specification
The endpoints of the API are exemplified in Postman in the following collection: https://www.getpostman.com/collections/d34849a7f0ccdae5831f


## Deployed application
The application is running at `https://ludo-backend.herokuapp.com`

## License
This source code is property of er-inc and cannot be publicly distributed without explicit consent.

This project is maintained by **Federico Esteban** (fede.est@gmail.comn) and **Daniela Riesgo** (daniealp.riesgo@gmail.com)
