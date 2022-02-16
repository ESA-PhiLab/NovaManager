#!/bin/bash
if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for mysql..."

    while ! nc -z $MYSQL_HOST $MYSQL_PORT; do
      sleep 0.1
    done

    echo "MySQL started"
fi


echo "Starting server"
gunicorn --config /app/scripts/gunicorn.conf.py vmmanager.wsgi:application