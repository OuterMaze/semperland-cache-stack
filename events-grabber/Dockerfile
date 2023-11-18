FROM python:3.11

# Install the cron package and set up everything.
# It will trigger main.py properly every 2 minutes.
RUN apt-get update && apt-get -y install vim nano

# Install the dependencies.
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

# Set workdir and copy files.
WORKDIR /app
COPY app /app

CMD ["python3", "main.py"]
