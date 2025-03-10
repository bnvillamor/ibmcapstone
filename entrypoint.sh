#!/bin/sh
if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for PostgreSQL..."
    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
        sleep 0.1
    done
    echo "PostgreSQL started"
fi

# Make migrations and migrate the database
echo "Making migrations and migrating the database."
python manage.py makemigrations
python manage.py migrate

# Start the application
exec "$@"