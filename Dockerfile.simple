FROM mugglecloud/web2py-gevent

USER root

RUN apt-get update
RUN apt-get install -y apt-utils net-tools lsof sudo python3-pip openssl libgeoip-dev procps git
RUN pip3 install psutil netifaces geoip

WORKDIR /home/src
COPY . .

#create folders and set permissions
RUN ["/bin/bash", "-c", "mkdir -p /opt/waf/nginx/etc/{sites-available,geoip,sites-available,sites-enabled,backend,modsec_rules,modsecurity_conf,ssl,listen,rewrite/paths,rewrite/headers,crs,static/html}"]
RUN ["/bin/bash", "-c", "mkdir -p /opt/waf/nginx/cache/{static,temp}"]

RUN cd /opt/waf/nginx/etc/crs/ \
  && git clone https://github.com/coreruleset/coreruleset.git \
  && cd coreruleset \
  && mv crs-setup.conf.example  crs-setup.conf \
  && sed -i 's/SecDefaultAction/#SetDefaultAction/g' crs-setup.conf
RUN cd /opt/waf/nginx/etc/crs/ \
  && ln -s coreruleset -T owasp-modsecurity-crs

ENV APP=Waf2Py

WORKDIR /home/www-data/

RUN mkdir -p /var/spool/cron/crontabs/ && mv -f /home/src/cron/crontab /var/spool/cron/crontabs/root
RUN ln -s /home/web2py/web2py -T waf2py_community
RUN ln -s /home/src -T /home/web2py/web2py/applications/${APP}
RUN ln -s /home/src/web2py-routes.py -T /home/web2py/web2py/routes.py

WORKDIR /home/web2py/web2py/
