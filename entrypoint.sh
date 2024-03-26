#!/bin/sh

# Wait for the DB to be ready
until nc -z -v -w30 $DB_HOST $(( $DB_PORT ));
do
 echo 'Waiting for the DB to be ready...'
 sleep 2
done

alembic upgrade head
gunicorn -k uvicorn.workers.UvicornWorker -b :$PORT service.app:APP
