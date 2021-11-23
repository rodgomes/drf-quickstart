#!/bin/sh

echo "Preparing server"
if [ -n "$DATABASE_HOST" ]; then
    make migrate collectstatic || exit 1
else
    if [ -n "$DEBUG" ]; then
        make migrate collectstatic || exit 1
    fi
fi

echo "Starting Webserver"

echo "$@"

exec "$@"