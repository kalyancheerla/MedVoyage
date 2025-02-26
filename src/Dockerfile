# Commands to build and run
# $ docker build -t medvoyage .
# $ docker run -d --name medvoyage -p 8000:8000 medvoyage:latest

# Use an official Python runtime as a parent image
FROM python:latest
LABEL maintainer="KalyanCheerla@my.unt.edu"

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Copy Django project files
COPY . /app
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Use the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
