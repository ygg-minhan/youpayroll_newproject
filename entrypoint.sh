#!/bin/sh

# Print the value of the DATABASE environment variable
echo "$DATABASE"

# Check if the DATABASE variable is set to "postgres"
if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    # Loop until PostgreSQL is ready to accept connections
    while ! nc -z "$DATABASES_HOST" "$DATABASES_PORT"; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Execute the command passed as arguments to the entrypoint script
exec "$@"
