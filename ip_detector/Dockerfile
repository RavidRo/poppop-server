FROM python:3.11-slim

WORKDIR /opt/ip_detector

RUN apt-get update \
	&& apt-get -y install cron \
	&& rm -rf /var/lib/apt/lists/* 

COPY ip_detector/ip_detector_cron /etc/cron.d/ip_detector_cron
RUN chmod 0644 /etc/cron.d/ip_detector_cron

RUN crontab /etc/cron.d/ip_detector_cron

COPY ip_detector/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY libraries/mcqueue mcqueue
COPY libraries/mclogging mclogging
RUN pip install --no-cache-dir ./mcqueue ./mclogging

COPY ip_detector/src src

CMD echo "IP Detector started..." && cron -f