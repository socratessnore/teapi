ARG BUILD_FROM
FROM $BUILD_FROM

ARG PYTHON_VERSION=3.9.9

WORKDIR /workdir

# Install python
RUN \
  apk add --no-cache --update \
    python3 py3-pip dos2unix

RUN pip install --no-cache-dir paho-mqtt openpyxl requests
			
# Copy python scripts
COPY datahandler.py .
COPY get_data.py .
COPY main.py .
COPY mqtt.py .

COPY crontab .

RUN dos2unix crontab
			
# Copy data for add-on
COPY run.sh .
RUN chmod a+x run.sh

# Adding crontab to the appropriate location
ADD crontab /etc/cron.d/my-cron-file

# Giving permission to crontab file
RUN chmod 0644 /etc/cron.d/my-cron-file

# Running crontab
RUN crontab /etc/cron.d/my-cron-file

# Creating entry point for cron 
ENTRYPOINT ["crond", "-f"]