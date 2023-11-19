# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app /app

# Copy the requirements file into the container at /tmp
COPY ./requirements.txt /tmp/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN pip install gunicorn==21.2.0

# Make port 80 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
