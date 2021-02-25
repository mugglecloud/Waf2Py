FROM mugglecloud/nginx-modsecurity

WORKDIR /home/src

COPY sources.list .
COPY pip.conf .
RUN rm /etc/apt/sources.list && mv sources.list /etc/apt/ && mkdir -p ~/.pip && mv pip.conf ~/.pip/

RUN apt-get update
RUN apt-get install -y apt-utils unzip wget net-tools lsof sudo python3-pip openssl libgeoip-dev procps git
RUN pip3 install --upgrade pip && pip install psutil netifaces geoip gevent

RUN mkdir -p /home/web2py/web2py

RUN cd /home/web2py/ && \
  wget -c http://web2py.com/examples/static/web2py_src.zip && \
  unzip -o web2py_src.zip && \
  rm -rf /home/web2py/web2py/applications/examples && \
  rm -rf /home/web2py/web2py/applications/welcome && \
  chmod 755 -R /home/web2py/web2py

COPY . .

ENV APP=Waf2Py

WORKDIR /home/www-data/

RUN mkdir -p /var/spool/cron/crontabs/ && mv -f /home/src/cron/crontab /var/spool/cron/crontabs/root
RUN ln -s /home/web2py/web2py -T waf2py_community
RUN ln -s /home/src -T /home/web2py/web2py/applications/${APP}
RUN ln -s /home/src/web2py-routes.py -T /home/web2py/web2py/routes.py

WORKDIR /home/web2py/web2py/

EXPOSE 8000

USER root

COPY entrypoint.sh .
RUN chmod u+x ./entrypoint.sh
CMD [ "./entrypoint.sh" ]
# CMD python /home/web2py/web2py/anyserver.py -s gevent -i 0.0.0.0 -p 8000