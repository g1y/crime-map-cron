FROM ubuntu

WORKDIR /usr/share/crime-map-cron

COPY . /usr/share/crime-map-cron

COPY crime-map-crontab /etc/cron.d/crime-map-crontab

RUN apt-get update
RUN apt-get install -y cron

CMD cron
