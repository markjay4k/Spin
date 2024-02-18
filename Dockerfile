FROM python:3.12-slim
RUN apt-get update && apt-get -y install cron git gcc

WORKDIR /app

COPY cron_spin_scheduler.sh .
COPY requirements.txt .
COPY __init__.py .
COPY _images.py .
COPY clogger.py .
COPY movies.py .
COPY spin.py .
COPY red.py .

ARG DOWNLOAD_COVER_IMAGE
ARG DATABASE_NETWORK
ARG DATABASE_NAME
ARG REDIS_EXPIRE_SECONDS
ARG REDIS_IP_ADDR
ARG REDIS_PORT
ARG LOG_LEVEL
ARG JF_MOVIE_DIR
ARG TORRENT_API_HOST
ARG TORRENT_API_PORT
ARG TORRENT_API_PATH
ARG TRANSMISSION_IP
ARG TRANSMISSION_PORT
ARG TRANSMISSION_USER
ARG TRANSMISSION_PASS
ARG CRON_SCHEDULE

RUN echo "DOWNLOAD_COVER_IMAGE=$DOWNLOAD_COVER_IMAGE" >> /etc/environment
RUN echo "DATABASE_NETWORK=$DATABASE_NETWORK" >> /etc/environment
RUN echo "DATABASE_NAME=$DATABASE_NAME" >> /etc/environment
RUN echo "REDIS_EXPIRE_SECONDS=$REDIS_EXPIRE_SECONDS" >> /etc/environment
RUN echo "REDIS_IP_ADDR=$REDIS_IP_ADDR" >> /etc/environment
RUN echo "REDIS_PORT=$REDIS_PORT" >> /etc/environment
RUN echo "LOG_LEVEL=$LOG_LEVEL" >> /etc/environment
RUN echo "JF_MOVIE_DIR=$JF_MOVIE_DIR" >> /etc/environment
RUN echo "TORRENT_API_HOST=$TORRENT_API_HOST" >> /etc/environment
RUN echo "TORRENT_API_PORT=$TORRENT_API_PORT" >> /etc/environment
RUN echo "TORRENT_API_PATH=$TORRENT_API_PATH" >> /etc/environment
RUN echo "TRANSMISSION_IP=$TRANSMISSION_IP" >> /etc/environment
RUN echo "TRANSMISSION_PORT=$TRANSMISSION_PORT" >> /etc/environment
RUN echo "TRANSMISSION_USER=$TRANSMISSION_USER" >> /etc/environment
RUN echo "TRANSMISSION_PASS=$TRANSMISSION_PASS" >> /etc/environment
RUN echo "CRON_SCHEDULE=$CRON_SCHEDULE" >> /etc/environment

RUN pip3 install -r requirements.txt

RUN chmod +x cron_spin_scheduler.sh
RUN touch /var/log/cron.log
RUN echo "SPIN: update redis DB with IMDb movie data" >> /var/log/cron.log
RUN echo "cron schedule: ${CRON_SCHEDULE}" >> /var/log/cron.log
RUN echo "    log level: ${LOG_LEVEL}" >> /var/log/cron.log

RUN ./cron_spin_scheduler.sh

CMD cron && tail -f /var/log/cron.log

