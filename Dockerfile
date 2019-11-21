# docker build -f Dockerfile ./ -t storage-of-knowledge-be:01
# docker run -ti --rm storage-of-knowledge-be:01 bash
# docker run --rm --network="host" -v $(pwd)/.env:/app/storageofknowledge/.env -v $(pwd)/logging/develop.json:/app/storageofknowledge/logging/develop.json storage-of-knowledge-be:01

FROM python:3.6-slim
ENV PYTHONUNBUFFERED 1
MAINTAINER artyomsliusar@gmail.com

RUN useradd -ms /bin/bash service-user
COPY ./requirements.txt /app/requirements.txt
RUN apt-get update \
	&& apt-get install -y --no-install-recommends default-libmysqlclient-dev gcc \
	&& pip install --upgrade pip setuptools \
	&& pip install -r /app/requirements.txt \
	&& rm -rf /var/lib/apt/lists/* \
	&& apt-get purge -y --auto-remove gcc

COPY ./ /app/
RUN mkdir /static_root

WORKDIR /app/storageofknowledge

RUN DJANGO_STATIC_ROOT=/static_root/static DJANGO_SECRET_KEY=x DJANGO_RECAPTCHA_PRIVATE_KEY=x DJANGO_ACCESS_TOKEN_LIFETIME_MINUTES=0 python -W 'ignore:Not reading .env' manage.py collectstatic --noinput

RUN chown -R service-user:service-user /app
EXPOSE 8000
USER service-user

CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
