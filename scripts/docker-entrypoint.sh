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
gunicorn --bind :8000 --workers 2 --timeout 90 --access-logfile - vmmanager.wsgi:application