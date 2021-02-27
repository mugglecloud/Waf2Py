# Chris - cvaras@itsec.cl
# -*- coding: utf-8 -*-
from gluon.tools import Recaptcha2
from gluon.tools import Auth
from gluon.contrib.appconfig import AppConfig
import datetime

db = DAL('sqlite://waf2py.sqlite',
         folder='/home/www-data/waf2py_community/applications/Waf2Py/databases')
db2 = DAL('sqlite://waf_logs.sqlite',
          folder='/home/www-data/waf2py_community/applications/Waf2Py/databases')

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
myconf = AppConfig(reload=False)

# choose a style for forms
# -------------------------------------------------------------------------
# response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.formstyle = 'bootstrap4_stacked'
response.form_label_separator = myconf.get('forms.separator') or ': '


def widget(**kwargs):
    return lambda field, value, kwargs=kwargs: SQLFORM.widgets[field.type].widget(field, value, **kwargs)


db.define_table('examples',
                Field('conf_name', 'string', length=30,
                      requires=IS_NOT_EMPTY()),
                Field('data_conf', 'text', requires=IS_NOT_EMPTY()),
                Field('description', 'text', requires=IS_NOT_EMPTY()),
                Field('autor', 'string', length=15, requires=IS_NOT_EMPTY()),
                )

db.define_table('basic_conf',
                Field('nginx_data_conf', 'text', requires=IS_NOT_EMPTY()),
                Field('modsec3_data_conf', 'text'),
                )

db.define_table('new_app',
                Field('app_name', 'string', length=100,
                      requires=IS_NOT_EMPTY()),
                Field('nginx_conf_data', 'text', requires=IS_NOT_EMPTY()),
                Field('modsec_conf_data', 'text', requires=IS_NOT_EMPTY()),
                Field('autor', 'string', length=15, requires=IS_NOT_EMPTY()),
                Field('description', 'string', length=50,
                      requires=IS_NOT_EMPTY()),
                Field('checked', 'integer', length=1, requires=IS_NOT_EMPTY()),
                Field('deployed', 'integer',  length=1,
                      requires=IS_NOT_EMPTY()),
                Field('id_rand', 'string', length=50, requires=IS_NOT_EMPTY()),
                Field('name', 'string', length=50, requires=IS_NOT_EMPTY()),
                Field('vhost_id', 'integer', length=4,
                      requires=IS_NOT_EMPTY()),
                Field('plbsid_id', 'integer', length=4,
                      requires=IS_NOT_EMPTY()),
                Field('fail_timeout', 'integer', length=3,
                      default='60', requires=IS_NOT_EMPTY()),
                Field('max_fails', 'integer', length=2,
                      default='1', requires=IS_NOT_EMPTY()),
                Field('backend_ip', 'string', requires=IS_NOT_EMPTY()),
                Field('listen_ip', 'string', length=45,
                      requires=IS_NOT_EMPTY()),
                )

db.define_table('production',
                Field('app_name', 'string', length=100,
                      requires=IS_NOT_EMPTY()),
                Field('nginx_conf_data', 'text', requires=IS_NOT_EMPTY()),
                Field('modsec_conf_data', 'text', requires=IS_NOT_EMPTY()),
                Field('autor', 'string', length=30, requires=IS_NOT_EMPTY()),
                Field('description', 'string', length=50,
                      requires=IS_NOT_EMPTY()),
                Field('id_rand', 'string', length=50, requires=IS_NOT_EMPTY()),
                Field('enabled', 'string', length=50, requires=IS_NOT_EMPTY()),
                Field('listening', 'string', length=50,
                      requires=IS_NOT_EMPTY()),
                Field('name', 'string', length=50, requires=IS_NOT_EMPTY()),
                Field('vhost_id', 'integer', length=4,
                      requires=IS_NOT_EMPTY()),
                Field('plbsid_id', 'integer', length=4,
                      requires=IS_NOT_EMPTY()),
                Field('fail_timeout', 'integer', length=3, default='60'),
                Field('max_fails', 'integer', length=2, default='1'),
                #Field('backend_ip', 'string', requires=IS_NOT_EMPTY()),
                Field('listen_ip', 'string', length=45,
                      requires=IS_NOT_EMPTY()),
                Field('mode', 'string', length=10, default="Defend",
                      requires=IS_IN_SET(["Defend", "Vigilant", "Bridge"])),
                Field('ports_http', 'string', length=5, default="80"),
                Field('ports_https', 'string', length=5, default="443"),
                Field('extra_headers', 'string', default=""),
                Field('paths_denied', 'string', default=""),
                Field('backend_ip_http', 'string', default=""),
                Field('backend_ip_https', 'string', default=""),
                )

db.define_table('logs',
                Field('app_name', 'string'),
                Field('nginx_error', 'string'),
                Field('nginx_access', 'string'),
                Field('modsec_audit', 'string'),
                Field('application_logs', 'string'),
                Field('type_attack', 'string'),
                Field('uri', 'string'),
                Field('level', 'string'),
                Field('ip_attacker', 'string'),
                Field('ip_dst', 'string'),
                Field('date', 'string'),
                )


db.define_table('system',
                Field('iface_ip', 'string', requires=IS_NOT_EMPTY()),
                Field('iface_name', 'string', length=10,
                      requires=IS_NOT_EMPTY()),
                Field('used_by', 'string', length=100,
                      requires=IS_NOT_EMPTY()),
                Field('available', 'string', length=20,
                      default="Available", requires=IS_NOT_EMPTY()),
                Field('number', 'integer', length=2, requires=IS_NOT_EMPTY()),
                )

db.define_table('certificate',
                Field('id_rand', 'string', length=50, requires=IS_NOT_EMPTY()),
                Field('cert', 'text'),
                Field('chain', 'text'),
                Field('privkey', 'text'),
                Field('protocol', 'list:string'),
                Field('prefer_cipher', 'string'),
                Field('ciphers', 'string'))

db2.define_table('log_app',
                 Field('username'),
                 Field('time'),
                 Field('msg', 'text'))

db2.define_table('log_error',
                 Field('username'),
                 Field('time'),
                 Field('msg', 'text'))

db.define_table('exclusions',
                Field('id_rand', 'string', length=50, requires=IS_NOT_EMPTY()),
                Field('rules_id', 'string', length=10,
                      requires=IS_NOT_EMPTY()),
                Field('attack_name', 'string', length=30,
                      requires=IS_NOT_EMPTY()),
                Field('type', 'integer', length=1, requires=IS_NOT_EMPTY()),
                Field('local_path', 'string', requires=IS_NOT_EMPTY()),
                Field('user', 'string'),
                Field('custom_id', 'integer', length=6, requires=IS_NOT_EMPTY())
                )

db.define_table('routes',
                Field('id_rand', 'string', length=50, requires=IS_NOT_EMPTY()),
                Field('ip', requires=IS_NOT_EMPTY()),
                Field('gw_ip', requires=IS_NOT_EMPTY()),
                Field('iface', requires=IS_NOT_EMPTY()))

db.define_table('logs_file',
                Field('id_rand', 'string', length=50, requires=IS_NOT_EMPTY()),
                Field('log_name', 'string', length=100,
                      requires=IS_NOT_EMPTY()),
                Field('type', 'string', length=6, requires=IS_NOT_EMPTY()),
                Field('size', 'string', length=10, requires=IS_NOT_EMPTY()),
                Field('date', 'string', length=10, requires=IS_NOT_EMPTY()),
                Field('id_rand2', 'string', length=50,
                      requires=IS_NOT_EMPTY()),
                )

db.define_table('n_interfaces',
                Field('number', 'integer', default=0),
                )

db.define_table('general_config',
                Field('smtp_user', 'string', label=T('SMTP Username'), widget=widget(
                    _placeholder='user@mail.com'), requires=IS_NOT_EMPTY()),
                Field('smtp_pass', 'password', label=T('SMTP Password'), widget=widget(
                    _placeholder='****'), requires=IS_NOT_EMPTY()),
                Field('smtp_sender', 'string', label=T('SMTP Sender'), widget=widget(
                    _placeholder='some_mail@mail.com'), requires=IS_EMAIL()),
                Field('smtp_host', 'string', label=T('SMTP Host'), widget=widget(
                    _placeholder='smtp.gmail.com'), requires=IS_NOT_EMPTY()),
                Field('smtp_port', 'integer', label=T('SMTP Port'), length=5, widget=widget(
                    _placeholder='587'), requires=IS_INT_IN_RANGE(1, 65535, error_message='Invalid port')),
                Field('captcha', 'string', label=T('Enable Google Recapcha2 ?'),
                      default='disabled', requires=IS_IN_SET(['enabled', 'disabled'])),
                Field('captcha_public_key', 'string',
                      label=T('Captcha Public Key')),
                Field('captcha_private_key', 'string',
                      label=T('Captcha Private Key')),
                Field('two_factor_authentication', 'string', label=T('Enable 2 Factor Authentication ?'),
                      default='disabled', requires=IS_IN_SET(['enabled', 'disabled']))
                )

db.define_table('rules',
                Field('id_rand', 'string', length=50, requires=IS_NOT_EMPTY()),
                Field('rule_name', 'string', length=50,
                      requires=IS_NOT_EMPTY()),
                Field('status', 'string', default='On',
                      requires=IS_IN_SET(['On', 'Off'])),
                Field('body', 'text', requires=IS_NOT_EMPTY()),
                )

db.define_table('summary',
                Field('id_rand', 'string', length=50, requires=IS_NOT_EMPTY()),
                Field('app_name', 'string', length=50,
                      requires=IS_NOT_EMPTY()),
                Field('critical', 'integer', default=0),
                Field('warning', 'integer', default=0),
                Field('notice', 'integer', default=0),
                Field('error', 'integer', default=0),
                Field('total_requests', 'integer', default=0),
                Field('old_size', 'integer', default=0),
                )

db.define_table('log_size',
                Field('id_rand', 'string', length=50, requires=IS_NOT_EMPTY()),
                Field('app_name', 'string', length=50,
                      requires=IS_NOT_EMPTY()),
                Field('log_type', 'string', default='modsec'),
                Field('size', 'integer', default=0)
                )
db.define_table('dummy',
                Field('dummy_field', 'string', requires=IS_NOT_EMPTY())
                )

auth = Auth(db)
auth.settings.everybody_group_id = False

# Setup Recapcha and 2 auth factor
general_conf = db(db.general_config.id == 1).select().first()
enable_captcha = False
captcha_public_key = ''
captcha_private_key = ''
two_factor_authentication = False
smtp_user = ''
smtp_pass = ''
smtp_sender = ''
smtp_host = ''
smtp_port = ''
if general_conf:
    if general_conf.captcha_private_key:
        captcha_private_key = general_conf.captcha_private_key
    if general_conf.captcha_public_key:
        captcha_public_key = general_conf.captcha_public_key
    if general_conf.captcha == 'enabled':
        enable_captcha = True
    if general_conf.two_factor_authentication == 'enabled':
        two_factor_authentication = True
    if general_conf.smtp_user:
        smtp_user = general_conf.smtp_user
    if general_conf.smtp_pass:
        smtp_pass = general_conf.smtp_pass
    if general_conf.smtp_host:
        smtp_host = general_conf.smtp_host
    if general_conf.smtp_port:
        smtp_port = str(general_conf.smtp_port)
    if general_conf.smtp_sender:
        smtp_sender = general_conf.smtp_sender


auth.settings.captcha = Recaptcha2(request, public_key=captcha_public_key,
                                   private_key=captcha_private_key, label='Please validate the captcha')
auth.define_tables(username=True, signature=True,)
auth.settings.logout_next = URL()

# Comment the following line to allow registration
auth.settings.actions_disabled.append('register')

if enable_captcha:
    auth.settings.login_captcha = auth.settings.captcha
else:
    auth.settings.login_captcha = False
auth.settings.two_factor_authentication_group = "auth2step"
auth.settings.auth_two_factor_enabled = two_factor_authentication

# SMPT server configuration
mail = auth.settings.mailer
mail.settings.server = smtp_host+':'+smtp_port
mail.settings.sender = smtp_sender
mail.settings.login = smtp_user+':'+smtp_pass


if db(db.n_interfaces.number).isempty():
    db.n_interfaces.insert(number=0)

if db(db.auth_user.id > 0).isempty():
    id_user = db.auth_user.insert(
        username='admin',
        password=db.auth_user.password.validate('admin')[0],
        email='changeme@waf2py.org',
    )
modsec3_default_config = """
# Improve the quality of ModSecurity by sharing information about your
# current ModSecurity version and dependencies versions.
# The following information will be shared: ModSecurity version,
# Web Server version, APR version, PCRE version, Lua version, Libxml2
# version, Anonymous unique id for host.|initial conf|admin|# -- Rule engine initialization ----------------------------------------------

# Enable ModSecurity, attaching it to every transaction. Use detection
# only to start with, because that minimises the chances of post-installation
# disruption.
#
SecRuleEngine On
SecDefaultAction "phase:1,log,auditlog,deny,status:403"
SecDefaultAction "phase:2,log,auditlog,deny,status:403"

#Include rules config file
Include "/opt/waf/nginx/etc/modsec_rules/SrvName/crs-setup.conf"
#Include ruleset owasp crs 3.3
Include "/opt/waf/nginx/etc/modsec_rules/SrvName/enabled_rules/*.conf"


##startGlobalrules##
#ExclusionGLobally
##endGlobalrules##

##startLocalrules##
#ExclusionLocal
##endLocalrules##

#Disable resolv external entities (prevents xxe in modsecurity)
SecXmlExternalEntity Off

# -- Request body handling ---------------------------------------------------

# Allow ModSecurity to access request bodies. If you don't, ModSecurity
# won't be able to see any POST parameters, which opens a large security
# hole for attackers to exploit.
#
SecRequestBodyAccess On


# Enable XML request body parser.
# Initiate XML Processor in case of xml content-type
#
SecRule REQUEST_HEADERS:Content-Type "(?:text|application)/xml" \
     "id:'200000',phase:1,t:none,t:lowercase,pass,nolog,ctl:requestBodyProcessor=XML"

# Enable JSON request body parser.
# Initiate JSON Processor in case of JSON content-type; change accordingly
# if your application does not use 'application/json'
#
SecRule REQUEST_HEADERS:Content-Type "application/json" \
     "id:'200001',phase:1,t:none,t:lowercase,pass,nolog,ctl:requestBodyProcessor=JSON"

# Maximum request body size we will accept for buffering. If you support
# file uploads then the value given on the first line has to be as large
# as the largest file you are willing to accept. The second value refers
# to the size of data, with files excluded. You want to keep that value as
# low as practical.
#
SecRequestBodyLimit 13107200
SecRequestBodyNoFilesLimit 131072


# What do do if the request body size is above our configured limit.
# Keep in mind that this setting will automatically be set to ProcessPartial
# when SecRuleEngine is set to DetectionOnly mode in order to minimize
# disruptions when initially deploying ModSecurity.
#
SecRequestBodyLimitAction Reject

# Verify that we've correctly processed the request body.
# As a rule of thumb, when failing to process a request body
# you should reject the request (when deployed in blocking mode)
# or log a high-severity alert (when deployed in detection-only mode).
#
SecRule REQBODY_ERROR "!@eq 0" \
"id:'200002', phase:2,t:none,log,deny,status:400,msg:'Failed to parse request body.',logdata:'%{reqbody_error_msg}',severity:2"

# By default be strict with what we accept in the multipart/form-data
# request body. If the rule below proves to be too strict for your
# environment consider changing it to detection-only. You are encouraged
# _not_ to remove it altogether.
#
SecRule MULTIPART_STRICT_ERROR "!@eq 0" \
"id:'200003',phase:2,t:none,log,deny,status:400, \
msg:'Multipart request body failed strict validation: \
PE %{REQBODY_PROCESSOR_ERROR}, \
BQ %{MULTIPART_BOUNDARY_QUOTED}, \
BW %{MULTIPART_BOUNDARY_WHITESPACE}, \
DB %{MULTIPART_DATA_BEFORE}, \
DA %{MULTIPART_DATA_AFTER}, \
HF %{MULTIPART_HEADER_FOLDING}, \
LF %{MULTIPART_LF_LINE}, \
SM %{MULTIPART_MISSING_SEMICOLON}, \
IQ %{MULTIPART_INVALID_QUOTING}, \
IP %{MULTIPART_INVALID_PART}, \
IH %{MULTIPART_INVALID_HEADER_FOLDING}, \
FL %{MULTIPART_FILE_LIMIT_EXCEEDED}'"

# Did we see anything that might be a boundary?
#
SecRule MULTIPART_UNMATCHED_BOUNDARY "!@eq 0" \
"id:'200004',phase:2,t:none,log,deny,msg:'Multipart parser detected a possible unmatched boundary.'"

# PCRE Tuning
# We want to avoid a potential RegEx DoS condition
#
SecPcreMatchLimit 7000
SecPcreMatchLimitRecursion 7000

# Some internal errors will set flags in TX and we will need to look for these.
# All of these are prefixed with "MSC_".  The following flags currently exist:
#
# MSC_PCRE_LIMITS_EXCEEDED: PCRE match limits were exceeded.
#
SecRule TX:/^MSC_/ "!@streq 0" \
        "id:'200005',phase:2,t:none,deny,msg:'ModSecurity internal error flagged: %{MATCHED_VAR_NAME}'"


# -- Response body handling --------------------------------------------------

# Allow ModSecurity to access response bodies. 
# You should have this directive enabled in order to identify errors
# and data leakage issues.
# 
# Do keep in mind that enabling this directive does increases both
# memory consumption and response latency.
#
SecResponseBodyAccess On

# Which response MIME types do you want to inspect? You should adjust the
# configuration below to catch documents but avoid static files
# (e.g., images and archives).
#
SecResponseBodyMimeType text/plain text/html text/xml

# Buffer response bodies of up to 512 KB in length.
SecResponseBodyLimit 524288

# What happens when we encounter a response body larger than the configured
# limit? By default, we process what we have and let the rest through.
# That's somewhat less secure, but does not break any legitimate pages.
#
SecResponseBodyLimitAction ProcessPartial


# -- Filesystem configuration ------------------------------------------------

# The location where ModSecurity stores temporary files (for example, when
# it needs to handle a file upload that is larger than the configured limit).
# 
# This default setting is chosen due to all systems have /tmp available however, 
# this is less than ideal. It is recommended that you specify a location that's private.
#
SecTmpDir /tmp/

# The location where ModSecurity will keep its persistent data.  This default setting 
# is chosen due to all systems have /tmp available however, it
# too should be updated to a place that other users can't access.
#
SecDataDir /tmp/


# -- File uploads handling configuration -------------------------------------

# The location where ModSecurity stores intercepted uploaded files. This
# location must be private to ModSecurity. You don't want other users on
# the server to access the files, do you?
#
#SecUploadDir /opt/modsecurity/var/upload/

# By default, only keep the files that were determined to be unusual
# in some way (by an external inspection script). For this to work you
# will also need at least one file inspection rule.
#
#SecUploadKeepFiles RelevantOnly

# Uploaded files are by default created with permissions that do not allow
# any other user to access them. You may need to relax that if you want to
# interface ModSecurity to an external program (e.g., an anti-virus).
#
#SecUploadFileMode 0600


# -- Debug log configuration -------------------------------------------------

# The default debug log configuration is to duplicate the error, warning
# and notice messages from the error log.
#
SecDebugLog /opt/waf/nginx/var/log/SrvName/SrvName_debug.log
SecDebugLogLevel 3


# -- Audit log configuration -------------------------------------------------

# Log the transactions that are marked by a rule, as well as those that
# trigger a server error (determined by a 5xx or 4xx, excluding 404,  
# level response status codes).
#
SecAuditLogDirMode 1733
SecAuditLogFileMode 0550
SecAuditLogFormat JSON
SecAuditEngine RelevantOnly
#SecAuditLogRelevantStatus "^(?:5|4(?!04))"
SecAuditLogRelevantStatus "^(?:5|4)"
#SecAuditLogRelevantStatus "^2-5"

# Log everything we know about a transaction.
SecAuditLogParts ABCHIZ


# Use a single file for logging. This is much easier to look at, but
# assumes that you will use the audit log only ocassionally.
#
SecAuditLogType Serial
SecAuditLog /opt/waf/nginx/var/log/SrvName/SrvName_audit.log


# -- Miscellaneous -----------------------------------------------------------

# Use the most commonly used application/x-www-form-urlencoded parameter
# separator. There's probably only one application somewhere that uses
# something else so don't expect to change this value.
#
SecArgumentSeparator &

# Settle on version 0 (zero) cookies, as that is what most applications
# use. Using an incorrect cookie version may open your installation to
# evasion attacks (against the rules that examine named cookies).
#
SecCookieFormat 0

# Specify your Unicode Code Point.
# This mapping is used by the t:urlDecodeUni transformation function
# to properly map encoded data to your language. Properly setting
# these directives helps to reduce false positives and negatives.
#
SecUnicodeMapFile ../unicode.mapping 20127

# Improve the quality of ModSecurity by sharing information about your
# current ModSecurity version and dependencies versions.
# The following information will be shared: ModSecurity version,
# Web Server version, APR version, PCRE version, Lua version, Libxml2
# version, Anonymous unique id for host.
"""

nginx_default_conf = """
server {
        server_name SrvName SrvNameAlias;
        set $vhost vhost_id;
        set $scmhst $scheme:$host;
        set $dyn_cache_status "0";
        set $separator "_";
        access_log /opt/waf/nginx/var/log/SrvName/SrvName_access.log custom buffer=32k;
        error_log /opt/waf/nginx/var/log/SrvName/SrvName_error.log warn;
        client_body_temp_path /opt/waf/nginx/var/log/SrvName/tmp;
        client_body_timeout 60;
        client_header_timeout 60;
        client_max_body_size 2097152;
        keepalive_requests 50;
        keepalive_timeout 5 5;
        limit_req zone=lrz0 burst=20;
        include /opt/waf/nginx/etc/listen/SrvName/*.conf; 
        
         
        #Modsecurity block
        modsecurity ModSecStatus; #ModSecStatus
        modsecurity_rules_file /opt/waf/nginx/etc/modsecurity_conf/SrvName_modsec.conf; #Cambiar

        #Page Speed Block
        #pagespeed off;
        #pagespeed DisableRewriteOnNoTransform off;
        #pagespeed RespectVary off;
        #pagespeed EnableFilters combine_css;
        #pagespeed FileCachePath /opt/waf/nginx/cache/ngx_pagespeed_cache;
        #location ~ "\.pagespeed\.([a-z]\.)?[a-z]{2}\.[^.]{10}\.[^.]+" {
        #        add_header "" "";
        #        expires 1y;
        #        gzip on;
        #        gzip_buffers 16 8k;
        #        gzip_comp_level 3;
        #        gzip_proxied any;
        #        gzip_types text/css text/javascript text/xml text/plain text/x-component application/javascript application/x-javascript application/json application/xml a$;
        #        gzip_vary on;
        #}

        #location ~ "^/pagespeed_static/" { }
        #location ~ "^/ngx_pagespeed_beacon$" { }
        
        #include for deny paths
        include "/opt/waf/nginx/etc/rewrite/paths/SrvName/*.conf";
        error_page 403 /403.html;
        location /403.html {
             root      /opt/waf/nginx/etc/static/html;
             internal;
         }
        error_page 404 /404.html;
        location /404.html {
             root      /opt/waf/nginx/etc/static/html;
             internal;
         }
        location / {
            ##startInsertHeaders##
            ##endInsertHeaders##
            expires 1y;
            gzip on;
            gzip_buffers 16 8k;
            gzip_comp_level 3;
            gzip_proxied any;
            gzip_types text/css text/javascript text/xml text/plain text/x-component application/javascript application/x-javascript application/json application/xml application/rss+xml font/truetype font/opentype application/vnd.ms-fontobject image/svg+xml;
            gzip_vary on;
            proxy_buffering on;
            proxy_http_version 1.1;
            proxy_connect_timeout 10;
            proxy_pass $scheme://backend$separator$vhost$separator$plbsid$scheme;
            proxy_read_timeout 60;
            proxy_send_timeout 60;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host SrvName;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header Accept-Encoding "";
            proxy_temp_path /opt/waf/nginx/cache/temp/$vhost;
        }

        proxy_intercept_errors on;
        proxy_next_upstream error timeout;
        proxy_ssl_session_reuse on;
        recursive_error_pages off;
        send_timeout 60;
        set $plbsid plbsid_id;
        #ssl_certificate /opt/waf/nginx/etc/ssl/SrvName/cert.pem.chain;
        #ssl_certificate_key /opt/waf/nginx/etc/ssl/SrvName/privkey.pem;
        ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';
        ssl_prefer_server_ciphers on;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;
        ssl_session_cache shared:SSL6:16m;
    }
"""
try:
    if db(db.basic_conf.modsec3_data_conf).isempty():
        db.basic_conf.update_or_insert(
            db.basic_conf.id == 1, modsec3_data_conf=modsec3_default_config)

    if db(db.basic_conf.nginx_data_conf).isempty():
        db.basic_conf.update_or_insert(
            db.basic_conf.id == 1, nginx_data_conf=nginx_default_conf)
except:
    pass
