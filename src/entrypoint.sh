#!/bin/sh

echo "Waiting for MySQL to start..."

python << END
import socket
import time

host = "mysql"
port = 3306
while True:
    try:
        s = socket.create_connection((host, port), timeout=2)
        s.close()
        break
    except (socket.timeout, ConnectionRefusedError):
        print(f"Waiting for {host}:{port} to be available...")
        time.sleep(2)
END

echo "MySQL is up!"

# Run migrations & collect static files
echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn --workers 3 --bind 0.0.0.0:8000 medvoyage.wsgi:application
