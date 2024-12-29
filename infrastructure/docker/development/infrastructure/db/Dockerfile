# pull official base image
FROM postgres:17.2-bookworm

# run create.sql on init
COPY infrastructure/docker/development/infrastructure/db/scripts/create.sql /docker-entrypoint-initdb.d/