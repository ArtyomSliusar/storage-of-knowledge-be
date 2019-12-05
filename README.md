# Storage of knowledge

This repository contains a web application for keeping your study notes and 
useful links in one place.
Your notes and links are always available, can be easily filtered and found.
Application doesn't have its own UI (except of admin UI), it just provides
an API for web (https://github.com/ArtyomSliusar/storage-of-knowledge-fe) or 
mobile clients.

## Technology

* Python 3.6
* Django 2.1

### Installing

#### on-premise

- Install build dependencies for mysql client
```
sudo apt-get install default-libmysqlclient-dev gcc
```

- Create and activate virtual environment
```
python3.6 -m venv stofkn-venv
source stofkn-venv/bin/activate
```

- Install requirements
```
pip install -r requirements.txt
```

- Create .env file in storageofknowledge folder (use example.env)

- Create logging configuration file (use storageofknowledge/logging templates)

- Run migrations
```
python manage.py migrate
```

- Create superuser
```
python manage.py createsuperuser
```

- Run server
```
python manage.py runserver
```

#### docker

- Run a new container, with `.env` file and `develop.json` logging configuration, 
use `host` network to connect to host database or Elasticsearch.
```
docker run --rm --network="host" \
    --env-file $(pwd)/storageofknowledge/.env \
    -v $(pwd)/storageofknowledge/logging/develop.json:/app/storageofknowledge/logging/develop.json \
    artyomsliusar/storage-of-knowledge-be:0.1
```

You can check https://github.com/ArtyomSliusar/storage-of-knowledge if you want
to run this application with all dependencies included.

### Configuration

Environment variables for configuration:

- DJANGO_ANYMAIL - anymail configuration settings (https://github.com/anymail/django-anymail)
- DJANGO_ACCESS_TOKEN_LIFETIME_MINUTES - JWT access token lifetime in minutes 
- DJANGO_ADMINS - application admins
- DJANGO_ADMIN_HEADER_COLOR - admin page header color
- DJANGO_ADMIN_HEADER_TITLE - admin page header title
- DJANGO_ALLOWED_HOSTS - https://docs.djangoproject.com/en/2.1/ref/settings/#allowed-hosts
- DJANGO_CORS_ORIGIN_WHITELIST - https://github.com/adamchainz/django-cors-headers#cors_origin_whitelist
- DJANGO_DATABASE_ENGINE - https://docs.djangoproject.com/en/2.1/ref/settings/#databases
- DJANGO_DATABASE_NAME - database name
- DJANGO_DATABASE_USER - database user
- DJANGO_DATABASE_PASSWORD - database password
- DJANGO_DATABASE_HOST - database host
- DJANGO_DATABASE_PORT - database port
- DJANGO_DEBUG - https://docs.djangoproject.com/en/2.1/ref/settings/#debug
- DJANGO_DEFAULT_FROM_EMAIL - https://docs.djangoproject.com/en/2.1/ref/settings/#default-from-email
- DJANGO_ELASTICSEARCH_HOST - elasticsearch host
- DJANGO_ELASTICSEARCH_PORT - elasticsearch port
- DJANGO_EMAIL_BACKEND - https://docs.djangoproject.com/en/2.1/ref/settings/#email-backend
- DJANGO_ENVIRONMENT - environment name (will be displayed in admin page header)
- DJANGO_LOGGING_CONFIG_FILE - relative path to logging configuration file
- DJANGO_RECAPTCHA_PRIVATE_KEY - google recaptcha private key
- DJANGO_RECAPTCHA_URL - google recaptcha url
- DJANGO_SECRET_KEY - site secret key
- DJANGO_SERVER_EMAIL - https://docs.djangoproject.com/en/2.1/ref/settings/#server-email
- DJANGO_STATIC_ROOT - relative path for static files
- DJANGO_USER_CONFIRMATION_LIFETIME_HOURS - confirmation token lifetime in hours

### How to

- Build a new docker image manually
```
docker build -f Dockerfile ./ -t artyomsliusar/storage-of-knowledge-be:0.1
```

- Run `bash` inside a new docker container
```
docker run -ti --rm --entrypoint=/bin/bash artyomsliusar/storage-of-knowledge-be:0.1
```

### TODO:
- tests
- api documentation
- use UUID for user
- add language field
- email user, if somebody has commented his/her note
- social networks integration
