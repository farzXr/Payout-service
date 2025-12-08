#!/bin/bash
set -e

echo "Running migrations..."
poetry run python manage.py migrate

exec "$@"
