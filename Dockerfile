FROM mugglecloud/web2py-gevent

USER root

RUN apt-get update
RUN apt-get install -y apt-utils net-tools lsof sudo python3-pip openssl libgeoip-dev
RUN pip3 install psutil netifaces geoip

WORKDIR /home/src
COPY . .

ENV APP=Waf2Py

WORKDIR /home/www-data/

RUN mkdir -p /var/spool/cron/crontabs/ && mv -f /home/src/cron/crontab /var/spool/cron/crontabs/root
RUN ln -s /home/web2py/web2py -T waf2py_community
RUN ln -s /home/src -T ./waf2py_community/applications/${APP}
RUN ln -s /home/src/web2py-routes.py ./waf2py_community/routes.py
