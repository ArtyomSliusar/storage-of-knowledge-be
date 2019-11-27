#!/usr/bin/env bash

if ./wait-for-it.sh $DJANGO_DATABASE_HOST:$DJANGO_DATABASE_PORT --strict; then
  python manage.py migrate && python manage.py collectstatic --noinput
else
  exit 1
fi

if ./wait-for-it.sh $DJANGO_ELASTICSEARCH_HOST:$DJANGO_ELASTICSEARCH_PORT --strict; then
  yes | python manage.py search_index --rebuild
else
  exit 1
fi

# Prepare log files and start outputting logs to stdout
touch /app/log/gunicorn.log
touch /app/log/access.log
tail -n 0 -f /app/log/*.log &

# Start Gunicorn processes
echo Starting Gunicorn
exec gunicorn storageofknowledge.wsgi:application \
    --name storageofknowledge \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level=info \
    --log-file=/app/log/gunicorn.log \
    --access-logfile=/app/log/access.log \
    "$@"
