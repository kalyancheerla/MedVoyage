# Use an official Python runtime as a parent image
FROM python:latest
LABEL maintainer="KalyanCheerla@my.unt.edu"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Open Port
EXPOSE 8000

# Run the command to start gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "medvoyage.wsgi:application"]
