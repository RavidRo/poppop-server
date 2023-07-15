FROM python:3.11-slim

WORKDIR /opt/ip_detector

RUN apt-get update \
	&& apt-get -y install cron \
	&& rm -rf /var/lib/apt/lists/* 

COPY ip_detector_cron /etc/cron.d/ip_detector_cron
RUN chmod 0644 /etc/cron.d/ip_detector_cron

RUN crontab /etc/cron.d/ip_detector_cron

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir requests

COPY main.py main.py

ENTRYPOINT echo "IP Detector started..." && cron -f