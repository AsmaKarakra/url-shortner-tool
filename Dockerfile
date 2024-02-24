# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
COPY wait-for-it.sh /wait-for-it.sh

# Make wait-for-it.sh executable
RUN chmod +x /wait-for-it.sh

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_ENV=production

# The actual command to start the app will be overridden in docker-compose.yml
CMD ["waitress-serve", "--listen=*:5000", "--call", "main:app"]

