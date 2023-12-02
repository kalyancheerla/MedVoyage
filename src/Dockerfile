# Commands to build and run
# $ docker build -t medvoyage .
# $ docker run -d --name medvoyage -p 8000:8000 medvoyage:latest

# Use an official Python runtime as a parent image
FROM python:latest
LABEL maintainer="KalyanCheerla@my.unt.edu"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Execute the DB migration setup
RUN python manage.py makemigrations && python manage.py migrate

# Open Port
EXPOSE 8000

# Run the command to start gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "medvoyage.wsgi:application"]
