# Chris - cvaras@itsec.cl
# -*- coding: utf-8 -*-

import subprocess
import stuffs
import os
import re
from random import randint

WafLogsPath = '/opt/waf/nginx/var/log/'
DownloadLogPath = '/home/www-data/waf2py_community/applications/Waf2Py/static/logs/'


@auth.requires_login()
def ExcludeLocal():
    a = stuffs.Filtro()
    try:
        b = a.CheckStr(request.vars['id_rand'])
        c = a.CheckRule(request.vars['ruleid'])
        d = a.CheckName(request.vars['attack_name'].rstrip())
        f = a.CheckPath(request.vars['path'])
        int(request.vars['type'])
    except:
        b = 'NO'

    if b == 'YES' and c == 'YES' and d == 'YES' and f == 'YES':
        data = db((db.exclusions.id_rand == request.vars['id_rand']) & (db.exclusions.type == request.vars['type']) & (
            db.exclusions.rules_id == request.vars['ruleid']) & (db.exclusions.local_path == request.vars['path'])).select(db.exclusions.rules_id, db.exclusions.local_path)
        modsec_conf = db(db.production.id_rand == request.vars['id_rand']).select(
            db.production.app_name, db.production.modsec_conf_data)
        if not data:
            # random custom_id
            custom_id = randint(0, 99999999)
            # add rule id to exclusions in db
            db.exclusions.insert(rules_id=request.vars['ruleid'], id_rand=request.vars['id_rand'], custom_id=custom_id, local_path=request.vars['path'],
                                 type=request.vars['type'], attack_name=request.vars['attack_name'].rstrip(), user=session['auth']['user']['username'])

            # get updated rules id
            rulesid = db((db.exclusions.id_rand == request.vars['id_rand']) & (db.exclusions.type == request.vars['type'])).select(
                db.exclusions.rules_id, db.exclusions.local_path, db.exclusions.custom_id)

            # Recreate the rules
            rules = '#ExclusionLocal\n'
            for i in rulesid:
                rules = rules + "SecRule REQUEST_URI \"@beginswith "+i['local_path']+"\" \"id:"+str(
                    i['custom_id'])+",phase:1,pass,nolog, ctl:ruleRemoveById="+i['rules_id']+"\"\n"
            rules_list = rules
            # replace old rules with new ones
            replace = re.sub(r'^(##\w+Local\w+##\n).*(##\w+Local\w+##)', r'\1%s\2' %
                             (rules_list), modsec_conf[0]['modsec_conf_data'], flags=re.S | re.M)
            db(db.production.id_rand == request.vars['id_rand']).update(
                modsec_conf_data=replace)  # '\n'.join(r))
            db.commit()
            UpdateFiles = stuffs.CreateFiles()
            try:
                UpdateFiles.CreateModsecConf(
                    modsec_conf[0]['app_name'], replace)
                a = stuffs.Nginx()
                b = a.Reload()
                #NewLogApp(db2, auth.user.username, "Mode: prod " +  data[0]['app_name'])
            except Exception as e:
                #NewLogError(db2, auth.user.username, "Mode: " + str(e))
                session.flash = e
            response.flash = 'Rule has been excluded locally'
            r = 'Rule has been excluded locally'
        else:
            response.flash = 'Rule ID or Path already excluded'
            r = 'Rule ID already excluded'

    else:
        response.flash = T('Error in data supplied')
        r = 'Error in data supplied'
    # print b,c,d,f
    return response.json(r)


@auth.requires_login()
def ExcludeGlobal():
    #import changeconfig
    a = stuffs.Filtro()
    try:

        b = a.CheckStr(request.vars['id_rand'])
        c = a.CheckRule(request.vars['ruleid'])
        d = a.CheckName(request.vars['attack_name'].rstrip())
        int(request.vars['type'])
    except:
        b = 'NO'
    if b == 'YES' and c == 'YES' and d == 'YES':

        data = db((db.exclusions.id_rand == request.vars['id_rand']) & (db.exclusions.type == request.vars['type']) & (
            db.exclusions.rules_id == request.vars['ruleid'])).select(db.exclusions.rules_id)
        modsec_conf = db(db.production.id_rand == request.vars['id_rand']).select(
            db.production.app_name, db.production.modsec_conf_data)
        if not data:
            # add rule id to exclusions in db
            db.exclusions.insert(rules_id=request.vars['ruleid'], id_rand=request.vars['id_rand'], type=request.vars['type'],
                                 attack_name=request.vars['attack_name'].rstrip(), user=session['auth']['user']['username'])

            # get updated rules id
            rulesid = db((db.exclusions.id_rand == request.vars['id_rand']) & (
                db.exclusions.type == request.vars['type'])).select(db.exclusions.rules_id)
            #change = changeconfig.Change()
            rules = '#ExclusionGLobally\n'
            for i in rulesid:
                rules = rules + "SecRuleRemoveById " + \
                    str(i['rules_id']) + '\n'
            rules_list = rules

            replace = re.sub(r'^(##\w+Global\w+##\n).*(##\w+Global\w+##)', r'\1%s\2' %
                             (rules_list), modsec_conf[0]['modsec_conf_data'], flags=re.S | re.M)
            db(db.production.id_rand == request.vars['id_rand']).update(
                modsec_conf_data=replace)  # '\n'.join(r))
            db.commit()
            UpdateFiles = stuffs.CreateFiles()
            try:
                UpdateFiles.CreateModsecConf(
                    modsec_conf[0]['app_name'], replace)
                a = stuffs.Nginx()
                b = a.Reload()
                #NewLogApp(db2, auth.user.username, "Mode: prod " +  data[0]['app_name'])
            except Exception as e:
                #NewLogError(db2, auth.user.username, "Mode: " + str(e))
                session.flash = e
            response.flash = 'Rule has been excluded globally'
            r = 'Rule has been excluded globally'
        else:
            response.flash = 'Rule ID already excluded'
            r = 'Rule ID already excluded'

    else:
        response.flash = T('Error in data supplied')
        r = 'Error in data supplied'

    return response.json(r)


@auth.requires_login()
def NginxLog():

    cmd = 'tac /opt/waf/nginx/var/log/error | head -600'
    out1 = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    msg = out1.communicate()[0]

    return dict(log_file=str(msg, 'utf-8').splitlines(), page=T("NGINX logs"), icon="fa fa-search", title="NGINX Logs")


@auth.requires_login()
def WafLogs():

    a = stuffs.Filtro()
    try:
        b = a.CheckStr(request.args[0])
        query = db(db.production.id_rand == request.args[0]).select(
            db.production.app_name)
        if not query:
            n = True
        else:
            n = False
    except:
        b = 'NO'
    if b == 'YES' and n == False:
        id_rand = request.args[0]
        subprocess.Popen(['sudo', 'chown', '-R', 'www-data.www-data', '/opt/waf/nginx/var/log/'],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.Popen(['sudo', 'chmod', '755', '-R', '/opt/waf/nginx/var/log/'], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        query = db(db.production.id_rand == request.args[0]).select(
            db.production.app_name)
        # Access Logs
        cmd = 'tac /opt/waf/nginx/var/log/' + \
            query[0]['app_name']+'/'+query[0]['app_name'] + \
            '_access.log | head -1000'
        out1 = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg, err = out1.communicate()
        # print err
        access_list = []
        for i in str(msg, 'utf-8', errors='ignore').splitlines():
            access_list.append(i)

        # Error Logs
        cmd2 = 'tac /opt/waf/nginx/var/log/' + \
            query[0]['app_name']+'/'+query[0]['app_name'] + \
            '_error.log | head -1000'
        out2 = subprocess.Popen(
            cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg2, err2 = out2.communicate()
        # print err2
        error_list = []
        for e in str(msg2, 'utf-8', errors='ignore').splitlines():
            error_list.append(e)

        # Modsec Json Logs
        cmd2 = 'tac /opt/waf/nginx/var/log/' + \
            query[0]['app_name']+'/'+query[0]['app_name'] + \
            '_audit.log | head -1000'
        out2 = subprocess.Popen(
            cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg2, err2 = out2.communicate()
        # print err2
        modsec_list = []
        for e in str(msg2, 'utf-8', errors='ignore').splitlines():
            modsec_list.append(e)

        # Debug Logs
        cmd3 = 'tac /opt/waf/nginx/var/log/' + \
            query[0]['app_name']+'/'+query[0]['app_name'] + \
            '_debug.log | head -1000'
        out3 = subprocess.Popen(
            cmd3, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg3, err3 = out3.communicate()
        # print err2
        debug_list = []
        for f in str(msg3, 'utf-8', errors='ignore').splitlines():
            debug_list.append(f)

        # Download Logs
        logs_file = db(db.logs_file.id_rand == request.args[0]).select(db.logs_file.id_rand, db.logs_file.log_name,
                                                                       db.logs_file.size, db.logs_file.type,
                                                                       db.logs_file.date, db.logs_file.id_rand2)

        summary_stats = db(db.summary.id_rand ==
                           request.args[0]).select().first()
    else:
        response.flash = T('Error in data supplied')
        redirect(URL('default', 'Websites'))
        id_rand = '#'

    return dict(page=query[0]['app_name']+" " + T("Logs"), title="", icon="", summary=summary_stats, logs_file=logs_file, access_logs=access_list, error_logs=error_list, debug_logs=debug_list, id_rand=id_rand, modsec_json_logs=modsec_list)

# not used yet, we still missing the view...


@auth.requires_login()
def AccessLogs():
    a = stuffs.Filtro()
    try:
        b = a.CheckStr(request.args[0])
    except:
        b = 'NO'
    if b == 'YES':
        query = db(db.production.id_rand == request.args[0]).select(
            db.production.app_name)
        cmd = 'tac /opt/waf/nginx/var/log/' + \
            query[0]['app_name']+'/'+query[0]['app_name'] + \
            '_access.log | head -400'
        out1 = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg, err = out1.communicate()
        access_list = []
        for i in msg:
            access_list.append(dict(access_log=i))

    else:
        access_list.append('Error in data suplied')
    return response.json({'access_logs': access_list})


@auth.requires_login()
def WafLogs_frame():
    import re
    import GeoIP
    import json

    gi = GeoIP.open(
        "/home/www-data/waf2py_community/applications/Waf2Py/geoip/GeoIP.dat", GeoIP.GEOIP_STANDARD)
    gi_city = GeoIP.open(
        "/home/www-data/waf2py_community/applications/Waf2Py/geoip/GeoLiteCity.dat", GeoIP.GEOIP_STANDARD)

    a = stuffs.Filtro()
    try:
        b = a.CheckStr(request.args[0])
    except:
        b = 'NO'
    logs_dict = {}
    logs_list = []

    if b == 'YES':

        query = db(db.production.id_rand == request.args[0]).select(
            db.production.app_name, db.production.id_rand)
        cmd = "tac /opt/waf/nginx/var/log/%s/%s_audit.log | head -1000" % (
            query[0]['app_name'], query[0]['app_name'])
        out1 = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg = out1.communicate()[0]
        logs_list = []
        for i in str(msg, 'utf-8', errors='ignore').splitlines():
            ii = json.loads(i)
            # print(i)
            k = i.rfind("}}")
            # This can be better
            if gi_city.record_by_addr(ii['transaction']['client_ip']) is not None:
                c = gi_city.record_by_addr(ii['transaction']['client_ip'])
                city = c['city']

            else:
                city = 'Not in GeoIp Database '
            if gi.country_code_by_addr(ii['transaction']['client_ip']) is not None:
                country_code = gi.country_code_by_addr(
                    ii['transaction']['client_ip'])
            else:
                country_code = 'Not in GeoIp Database '

            if gi.country_name_by_addr(ii['transaction']['client_ip']) is not None:
                country_name = gi.country_name_by_addr(
                    ii['transaction']['client_ip'])
            else:
                country_name = 'Not in GeoIp Database '

            if city == None or country_code == None or country_name == None:
                city = 'Not in GeoIp Database'

            new_string = i[:k] + ', "country_code":' + '"' + country_code + \
                '", "city":"'+city+'"'+',"country":"' + \
                country_name + '"}}' + i[k+2:]
            logs_list.append(new_string.replace('\n', '').replace('\r', ''))

    return response.json({'data': logs_list})


@auth.requires_login()
def UserActionLog():
    query = db2().select(db2.log_app.ALL, orderby=~db2.log_app.id)

    return dict(query=query, page=T("Application Logs"), title="", icon="")


@auth.requires_login()
def ErrorAppLogs():
    query = db2().select(db2.log_error.ALL, orderby=~db2.log_error.id)
    return dict(query=query, page=T("Error Application Logs"), title="", icon="")


@auth.requires_login()
def ExcludedRules():

    a = stuffs.Filtro()
    b = a.CheckStr(request.args[0])
    rule_list = []
    if b == 'YES':
        query = db(db.exclusions.id_rand == request.args[0]).select(db.exclusions.attack_name,
                                                                    db.exclusions.id_rand, db.exclusions.rules_id, db.exclusions.type,
                                                                    db.exclusions.user, db.exclusions.local_path,
                                                                    )
        if query:

            for row in query:
                # print row['attack_name']
                rule_list.append(dict(attack_name=row['attack_name'], rule_id=row['rules_id'],
                                      id_rand=row['id_rand'], tipo=row['type'], path=row['local_path'], user=row['user']))
        else:
            rule_list.append('There are no excluded rules')

    else:
        rule_list.append('Error in data supplied')

    return response.json({'rules': rule_list})


@auth.requires_login()
def DeleteRule():
    import changeconfig
    a = stuffs.Filtro()
    # print request.vars['type']
    try:
        b = a.CheckStr(request.vars['id_rand'])
        c = a.CheckRule(request.vars['ruleid'])
        d = int(request.vars['type'])

    except:
        b = 'NO'

    if b == 'YES' and c == 'YES' and request.vars['type'] == '0':
        # remove rule from exclusions table
        db((db.exclusions.id_rand == request.vars['id_rand']) & (
            db.exclusions.rules_id == request.vars['ruleid']) & (db.exclusions.type == 0)).delete()
        modsec = db(db.production.id_rand == request.vars['id_rand']).select(
            db.production.modsec_conf_data, db.production.app_name, db.production.mode)

        # change configuration
        # Change return a dictionary with status message and the new list whith changed configuration ex: {'newconf_list': 'data', 'message':'success or error'}
        change = changeconfig.Change()
        alter = change.Text(modsec[0]['modsec_conf_data'],
                            'SecRuleRemoveById '+request.vars['ruleid'], '')
        db(db.production.id_rand == request.vars['id_rand']).update(
            modsec_conf_data='\n'.join(alter['new_list']))

        # get new modsec conf
        new_modsec = db(db.production.id_rand == request.vars['id_rand']).select(
            db.production.modsec_conf_data)
        UpdateFiles = stuffs.CreateFiles()
        try:
            UpdateFiles.CreateModsecConf(
                modsec[0]['app_name'], new_modsec[0]['modsec_conf_data'])
            stuffs.Nginx().Reload()
            #NewLogApp(db2, auth.user.username, "Mode: prod " +  data[0]['app_name'])
        except Exception as e:
            #NewLogError(db2, auth.user.username, "Mode: " + str(e))
            session.flash = e
        response.flash = 'Rule deleted succesfully'
        r = 'Rule deleted succesfully'

    elif b == 'YES' and c == 'YES' and request.vars['type'] == '1':
        db((db.exclusions.id_rand == request.vars['id_rand']) & (
            db.exclusions.rules_id == request.vars['ruleid']) & (db.exclusions.type == 1)).delete()
        modsec = db(db.production.id_rand == request.vars['id_rand']).select(
            db.production.modsec_conf_data, db.production.app_name, db.production.mode)

        # change configuration
        # Change return a dictionary with status message and the new list whith changed configuration ex: {'newconf_list': 'data', 'message':'success or error'}
        change = changeconfig.Change()
        alter = change.Text(modsec[0]['modsec_conf_data'],
                            'ctl:ruleRemoveById='+request.vars['ruleid'], '')
        db(db.production.id_rand == request.vars['id_rand']).update(
            modsec_conf_data='\n'.join(alter['new_list']))
        # get new modsec conf
        new_modsec = db(db.production.id_rand == request.vars['id_rand']).select(
            db.production.modsec_conf_data)
        UpdateFiles = stuffs.CreateFiles()
        try:
            UpdateFiles.CreateModsecConf(
                modsec[0]['app_name'], new_modsec[0]['modsec_conf_data'])
            stuffs.Nginx().Reload()
            #NewLogApp(db2, auth.user.username, "Mode: prod " +  data[0]['app_name'])
        except Exception as e:
            #NewLogError(db2, auth.user.username, "Mode: " + str(e))
            session.flash = e
        response.flash = 'Rule deleted succesfully'
        r = 'Rule deleted succesfully'

    else:
        r = 'Error in data supplied'

    return response.json(r)


@auth.requires_login()
def DownloadError():
    a = stuffs.Filtro()
    try:
        b = a.CheckStr(request.args[0])

    except:
        b = 'NO'

    if b == 'YES':
        random = randint(0, 999999999)
        query = db(db.production.id_rand == request.args[0]).select(
            db.production.app_name, db.production.id_rand)
        out1 = subprocess.Popen(['/usr/bin/tar', '-czvf', '/home/www-data/waf2py_community/applications/Waf2Py/static/logs/error_logs_'+query[0]['app_name']+'_'+str(
            random)+'.tar.gz', '-C', '/opt/waf/nginx/var/log/'+query[0]['app_name']+'/',  query[0]['app_name']+'_error.log'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg, err = out1.communicate()
        r = A('Error_logs.tar.gz', _href='/Waf2Py/static/logs/error_logs_' +
              query[0]['app_name']+'_'+str(random)+'.tar.gz')
    else:
        session.flash = T('Error in data supplied')
        r = ''
    return r


@auth.requires_login()
def DownloadLogZip():
    import random
    import string
    import time
    import os
    a = stuffs.Filtro()
    try:
        # print request.args[1]
        b = a.CheckStr(request.args[0])
        c = a.CheckStr35(request.args[1])
        # print b,c
    except:
        b = 'NO'
        c = 'NO'
    if b == 'YES' and c == 'YES':
        chars = string.ascii_letters + string.digits
        pwdSize = 10

        rand = ''.join((random.choice(chars)) for x in range(pwdSize))
        log_name = db((db.logs_file.id_rand == request.args[0]) & (db.logs_file.id_rand2 == request.args[1])).select(
            db.logs_file.log_name
        )
        app_name = db(db.production.id_rand == request.args[0]).select(
            db.production.app_name
        )
        cmd = '/bin/cp ' + WafLogsPath + \
            app_name[0]['app_name']+'/'+log_name[0]['log_name'] + \
            ' ' + DownloadLogPath+rand+log_name[0]['log_name']
        out1 = os.system(cmd)
        if out1 == 0:
            redirect(URL('static', 'logs/'+rand+log_name[0]['log_name']))
        else:
            session.flash = T('Error in data supplied')
            redirect(URL('default', 'Websites'))

    else:
        session.flash = T('Error in data supplied')
        redirect(URL('default', 'Websites'))


@auth.requires_login()
def DownloadDebug():
    a = stuffs.Filtro()
    try:
        b = a.CheckStr(request.args[0])

    except:
        b = 'NO'

    if b == 'YES':
        random = randint(0, 999999999)
        query = db(db.production.id_rand == request.args[0]).select(
            db.production.app_name, db.production.id_rand)

        out1 = subprocess.Popen(['/usr/bin/tar', '-czf', '/home/www-data/waf2py_community/applications/Waf2Py/static/logs/debug_logs_'+query[0]['app_name']+'_'+str(
            random)+'.tar.gz', '-C', '/opt/waf/nginx/var/log/'+query[0]['app_name']+'/',  query[0]['app_name']+'_debug.log'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg, err = out1.communicate()
        r = A('Debug_logs.tar.gz', _href='/Waf2Py/static/logs/debug_logs_' +
              query[0]['app_name']+'_'+str(random)+'.tar.gz')
    else:
        session.flash = T('Error in data supplied')
        r = ''
    return r


@auth.requires_login()
def DownloadModsecJson():
    a = stuffs.Filtro()
    try:
        b = a.CheckStr(request.args[0])

    except:
        b = 'NO'

    if b == 'YES':
        random = randint(0, 999999999)
        query = db(db.production.id_rand == request.args[0]).select(
            db.production.app_name, db.production.id_rand)

        out1 = subprocess.Popen(['/usr/bin/tar', '-czf', '/home/www-data/waf2py_community/applications/Waf2Py/static/logs/modsec_logs_'+query[0]['app_name']+'_'+str(
            random)+'.tar.gz', '-C', '/opt/waf/nginx/var/log/'+query[0]['app_name']+'/',  query[0]['app_name']+'_audit.log'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg, err = out1.communicate()
        r = A('Modsecurity_logs.tar.gz', _href='/Waf2Py/static/logs/modsec_logs_' +
              query[0]['app_name']+'_'+str(random)+'.tar.gz')
    else:
        session.flash = T('Error in data supplied')
        r = ''
    return r


@auth.requires_login()
def DownloadAccess():
    a = stuffs.Filtro()
    try:
        b = a.CheckStr(request.args[0])

    except:
        b = 'NO'

    if b == 'YES':
        random = randint(0, 999999999)
        query = db(db.production.id_rand == request.args[0]).select(
            db.production.app_name, db.production.id_rand)
        out1 = subprocess.Popen(['/usr/bin/tar', '-czvf', '/home/www-data/waf2py_community/applications/Waf2Py/static/logs/access_logs_'+query[0]['app_name']+'_'+str(
            random)+'.tar.gz', '-C', '/opt/waf/nginx/var/log/'+query[0]['app_name']+'/',  query[0]['app_name']+'_access.log'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg, err = out1.communicate()
        r = A('Error_logs.tar.gz', _href='/Waf2Py/static/logs/access_logs_' +
              query[0]['app_name']+'_'+str(random)+'.tar.gz')
    else:
        session.flash = T('Error in data supplied')
        r = ''
    return r
