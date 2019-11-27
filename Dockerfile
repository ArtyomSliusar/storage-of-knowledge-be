# docker build -f Dockerfile ./ -t artyomsliusar/storage-of-knowledge-be:01
# docker run -ti --rm --entrypoint=/bin/bash artyomsliusar/storage-of-knowledge-be:01
# docker run --rm --network="host" \
#	--env-file $(pwd)/storageofknowledge/.env \
#	-v $(pwd)/storageofknowledge/logging/develop.json:/app/storageofknowledge/logging/develop.json \
# 	artyomsliusar/storage-of-knowledge-be:01

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
COPY docker-entrypoint.sh wait-for-it.sh ./
RUN chmod +x wait-for-it.sh docker-entrypoint.sh

RUN chown -R service-user:service-user /app
USER service-user

EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]
