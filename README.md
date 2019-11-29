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

- Create and activate virtual environment
```
virtualenv venv
source venv/bin/activate
```

- Install requirements
```
pip install -r requirements.txt
```

- Create .env file in StorageOfKnowledge/storageofknowledge (use example.env)

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

- Run a new container, with `.env` file and logging configuration, use `host`
network to connect host database or Elasticsearch.
```
docker run --rm --network="host" \
    --env-file $(pwd)/storageofknowledge/.env \
    -v $(pwd)/storageofknowledge/logging/develop.json:/app/storageofknowledge/logging/develop.json \
    artyomsliusar/storage-of-knowledge-be:01
```

You can check https://github.com/ArtyomSliusar/storage-of-knowledge if you want
to run this application with all dependencies from scratch.

### Configuration

Environment variables for configuration:

- DJANGO_ANYMAIL - 
- DJANGO_ACCESS_TOKEN_LIFETIME_MINUTES - 
- DJANGO_ADMINS - 
- DJANGO_ADMIN_HEADER_COLOR - 
- DJANGO_ADMIN_HEADER_TITLE - 
- DJANGO_ALLOWED_HOSTS - 
- DJANGO_CORS_ORIGIN_WHITELIST -
- DJANGO_DATABASE_ENGINE -
- DJANGO_DATABASE_NAME -
- DJANGO_DATABASE_USER -
- DJANGO_DATABASE_PASSWORD -
- DJANGO_DATABASE_HOST -
- DJANGO_DATABASE_PORT -
- DJANGO_DEBUG -
- DJANGO_DEFAULT_FROM_EMAIL -
- DJANGO_ELASTICSEARCH_HOST -
- DJANGO_ELASTICSEARCH_PORT -
- DJANGO_EMAIL_BACKEND -
- DJANGO_ENVIRONMENT -
- DJANGO_LOGGING_CONFIG_FILE -
- DJANGO_RECAPTCHA_PRIVATE_KEY -
- DJANGO_RECAPTCHA_URL -
- DJANGO_SECRET_KEY -
- DJANGO_SERVER_EMAIL -
- DJANGO_STATIC_ROOT -
- DJANGO_USER_CONFIRMATION_LIFETIME_HOURS -

### How to

- Build a new docker image
```
docker build -f Dockerfile ./ -t artyomsliusar/storage-of-knowledge-be:01
```

- Run `bash` inside a new docker container
```
docker run -ti --rm --entrypoint=/bin/bash artyomsliusar/storage-of-knowledge-be:01
```

### TODO:
- clear tokens/confirmations cron
- correct notes body
- aws ecs
- fix cert renew
- tests
- use ssr
- api documentation
- multiplex requests to get note, its comments and likes
- flatten data in store
- add client-side encryption
- fix `history.goBack()` goes out of the website
- use UUID for user
- add language field
- make mobile header fixed
- use FE badges for private/public info
- add site monitoring and statistics solution
- email user, if somebody has commented his/her note
- social networks integration
- private cabinet with delete account option
- add popup for not logged in users (describe functionality)
