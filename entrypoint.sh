#!/bin/bash

/opt/waf/nginx/sbin/nginx
python3 /home/web2py/web2py/anyserver.py -s gunicorn -i 0.0.0.0 -p 8000