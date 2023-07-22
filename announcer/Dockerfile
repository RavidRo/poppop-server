FROM python:3.11-slim

WORKDIR /opt/announcer


COPY announcer/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY libraries/mcqueue mcqueue
COPY libraries/mclogging mclogging
RUN pip install --no-cache-dir ./mcqueue ./mclogging

COPY announcer/src src

ENTRYPOINT python src/announcer.py