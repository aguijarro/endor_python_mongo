#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z   endor_python_db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

exec "$@"