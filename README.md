# Storage of knowledge

This repository contains a web application for comfortable work with your study notes, links and tests.
Your notes and links are always available, can be easily filtered and found.

## Technology

* Python 3.6
* Django 1.11.5

### Installing

A step by step series of examples that tell you how to get a development env running

- Create and activate virtual environment
```
virtualenv storageofknowledge_venv
source storageofknowledge_venv/bin/activate
```

- Install requirements (dev)
```
pip install -r StorageOfKnowledge/requirements/development.txt
```

- Create .env file in StorageOfKnowledge/storageofknowledge (use example.env)

- Run migrations
```
python manage.py migrate
```

- Initialize subjects
```
python manage.py initsubjects
```

- Initialize types
```
python manage.py inittypes
```

- Create superuser
```
python manage.py createsuperuser
```

- Run server
```
python manage.py runserver
```

### Production deploy

- External link
```
http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/
```

ENVIRONMENTS:
...

TODO:
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
