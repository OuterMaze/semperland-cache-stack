FROM python:3.11

# Set workdir and copy files.
WORKDIR /app
COPY app /app
COPY requirements.txt /tmp

# Install the dependencies.
RUN pip install -r /tmp/requirements.txt

# Install the cron package and set up everything.
# It will trigger main.py properly every 2 minutes.
RUN apt-get update && apt-get -y install cron vim
RUN echo '*/2 * * * * python /app/main.py > /proc/1/fd/1 2> /proc/1/fd/2' > /etc/crontab.d/crontab
RUN chmod 0644 /etc/crontab.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
CMD ["cron", "-f"]
