# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for MongoDB URI
ENV MONGO_URI=""

# Run app.py using gunicorn when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]

