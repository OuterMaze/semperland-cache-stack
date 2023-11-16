FROM python:3.11

# Install the cron package and set up everything.
# It will trigger main.py properly every 2 minutes.
RUN apt-get update && apt-get -y install vim nano

# Set workdir and copy files.
WORKDIR /app
COPY app /app
COPY requirements.txt /tmp

# Install the dependencies.
RUN pip install -r /tmp/requirements.txt

CMD ["python3", "main.py"]
