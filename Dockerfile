# pull official base image
# FROM python:3.8-alpine
FROM fedest/face_recognition:latest

# set work directory
WORKDIR /usr/src/ludo

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV SIU_URL $SIU_URL

# install psycopg2 dependencies
# https://stackoverflow.com/a/52655008/3663124
RUN apt-get update --allow-releaseinfo-change \
    && mkdir -p /usr/share/man/man1 \
    && mkdir -p /usr/share/man/man7 \
    && apt-get install -y --fix-missing build-essential postgresql musl libpq-dev

# install dependencies
RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel
RUN pip install --upgrade Pillow
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

CMD gunicorn ludo.wsgi:application --bind 0.0.0.0:$PORT
