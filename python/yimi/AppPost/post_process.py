#!/usr/bin/python

import sys
import traceback
from mysql_query import *
from gen_source_data import *
from http_post import *

def call_id_print(*args):
    print ("[\033[1;32;42m%s:%d\033[0m]callId:\033[1;35m %s\033[0m" % (sys._getframe().f_back.f_code.co_name, sys._getframe().f_back.f_lineno, args[0]))

def stdout_print(*args):
    print ("[\033[1;32;42m%s:%d\033[0m] %s:%s") % (sys._getframe().f_back.f_code.co_name, sys._getframe().f_back.f_lineno, args[0], args[1])

'''
    TODO: if http_connect failed, write callId into a new exception file
'''
def format_record_url_data(mysql_handler, call_records):
    #print(type(call_records))
    url_data = ''
    resp_data = {}
    # ep_info = mysql_query(construct_ep_sql(call_records[0]['provinceId'], call_records[0]['enterpriseId']))
    ep_info = mysql_handler.sql_exec(construct_ep_sql(call_records[0]['provinceId'], call_records[0]['enterpriseId']))
    if not ep_info:
        return url_data
    ep_url = "http://%s:%d%s?un=%s&pwd=%s&eid=%d&cc_number=%s" % \
            (ep_info[0]['domain'], ep_info[0]['httpPort'], '/Talk/Api/getAccessUrl',\
            ep_info[0]['httpUser'], ep_info[0]['httpPasswd'], call_records[0]['enterpriseId'], call_records[0]['ccNumber'])
    try:
        resp_data = call_push(ep_url, DATA_FORMAT_FORM)
    except Exception, e:
        print ("call_push failed:%s" % repr(e))

    if resp_data['code'] == 200:
        es_resp_dict = json.loads(resp_data['data'])
        if es_resp_dict['status'] == 0:
            record_url_data = es_resp_dict['data']['url']
            #print ("[\033[1;32;42m%s:%d\033[0m]record_url_data:%s") % (sys._getframe().f_back.f_code.co_name, sys._getframe().f_back.f_lineno, record_url_data)
            stdout_print("record_url_data", record_url_data);
            url_data = record_url_data
        else:
            print ("Es resp info:%s") % (es_resp_dict['info'])
    else:
        print ("Es server connect failed")
    return url_data


def call_push_process(mysql_handler, callId):
    app_call_info = app_callpush_url_type(mysql_handler, callId)
    #print (app_call_info)
    xmlDataFormat = 1
    if not app_call_info['appCallbackDataFormat']:
        xmlDataFormat = 1
    else:
        xmlDataFormat = 0

    if (app_call_info['push_url_flag'] & CALL_PUSH_URL_BIT_CALLREQ):
        http_resp = {}
        ringing_list = gen_ringing_data(mysql_handler, app_call_info['call_records'])
        if not ringing_list:
            print ("No ringing data be generated.")
        elif xmlDataFormat:
            for i in range(len(ringing_list)):
                post_data = dict2XmlString(ringing_list[i])
                print ("RINGING:i:%d,post_data:%s" % (i, post_data))
                try:
                    http_resp = call_push(app_call_info['callreqUrl'], DATA_FORMAT_XML, post_data)
                except Exception, e:
                    print ("call_push failed:%s" % repr(e))
        else:
            for i in range(len(ringing_list)):
                post_data = dict2JsonString(ringing_list[i])
                print ("RINGING:i:%d,post_data:%s" % (i, post_data))
                data_format = DATA_FORMAT_JSON
                try:
                    http_resp = call_push(app_call_info['callreqUrl'], DATA_FORMAT_JSON, post_data)
                except Exception, e:
                    print ("call_push failed:%s" % repr(e))
    if (app_call_info['push_url_flag'] & CALL_PUSH_URL_BIT_ESTABLISH):
        http_resp = {}
        establish_list = gen_establish_data(mysql_handler, app_call_info['call_records'])
        if not establish_list:
            print ("No establish data be generated.")
        elif xmlDataFormat:
            for i in range(len(establish_list)):
                post_data = dict2XmlString(establish_list[i])
                print ("ESTABLISH:i:%d,post_data:%s" % (i, post_data))
                try:
                    http_resp = call_push(app_call_info['callestablishUrl'], DATA_FORMAT_XML, post_data)
                except Exception, e:
                    print ("call_push failed:%s" % repr(e))
        else:
            for i in range(len(establish_list)):
                post_data = dict2JsonString(establish_list[i])
                print ("ESTABLISH:i:%d,post_data:%s" % (i, post_data))
                try:
                    http_resp = call_push(app_call_info['callestablishUrl'], DATA_FORMAT_JSON, post_data)
                except Exception, e:
                    print ("call_push failed:%s" % repr(e))
    if (app_call_info['push_url_flag'] & CALL_PUSH_URL_BIT_HANGUP):
        http_resp = {}
        hangup_list = gen_hangup_data(mysql_handler, app_call_info['call_records'])
        if not hangup_list:
            print ("No hangup data be generated.")
        elif xmlDataFormat:
            for i in range(len(hangup_list)):
                post_data = dict2XmlString(hangup_list[i])
                print ("HANGUP:i:%d,post_data:%s" % (i, post_data))
                try:
                    http_resp = call_push(app_call_info['callhangupUrl'], DATA_FORMAT_XML, post_data)
                except Exception, e:
                    print ("call_push failed:%s" % repr(e))
        else:
            for i in range(len(hangup_list)):
                post_data = dict2JsonString(hangup_list[i])
                print ("HANGUP:i:%d,post_data:%s" % (i, post_data))
                try:
                    http_resp = call_push(app_call_info['callhangupUrl'], DATA_FORMAT_JSON, post_data)
                except Exception, e:
                    print ("call_push failed:%s" % repr(e))
    if (app_call_info['push_url_flag'] & CALL_PUSH_URL_BIT_RECORDS):
        http_resp = {}
        record_voice_file_url = format_record_url_data(mysql_handler, app_call_info['call_records'])
        if record_voice_file_url:
            record_notify_list = gen_record_notify_data(mysql_handler, app_call_info['call_records'], record_voice_file_url)
            if not record_notify_list:
                print ("No record data be generated.")
            elif xmlDataFormat:
                post_data = dict2XmlString(record_notify_list[0])
                print ("RECORD-NOTIFY:i:%d, post_data:%s" % (i, post_data))
                try:
                    http_resp = call_push(app_call_info['recordReadyNotifyUrl'], DATA_FORMAT_XML, post_data)
                except Exception, e:
                    print ("call_push failed:%s" % repr(e))
            else:
                post_data = dict2JsonString(record_notify_list[0])
                print ("RECORD-NOTIFY:i:%d, post_data:%s" % (i, post_data))
                data_format = DATA_FORMAT_JSON
                try:
                    http_resp = call_push(app_call_info['recordReadyNotifyUrl'], DATA_FORMAT_JSON, post_data)
                except Exception, e:
                    print ("call_push failed:%s" % repr(e))
        else:
            print ("None of record_voice_file_url.")
    return 0

DB_HOST='127.0.0.1'
DB_USER='root'
DB_PASS='123456'
DB_NAME='EmicallDev_system'

#callId='api1010001447a1532087694215jTPIn'
#callid_source_file='20180722-callid-00.csv'
#callid_source_file='temp.csv'
callid_source_file='callid.csv'
if __name__ == '__main__':
    if len(sys.argv) == 2:
        callid_source_file = sys.argv[1]

    mysql_handler = ""
    try:
        mysql_handler = emi_mysql(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    except Exception, e:
        print ("new emi_mysql obj failed:%s" % repr(e))
        sys.exit(1)

    i = 0
    file_obj = open(callid_source_file, 'r')
    for callid_line in file_obj.readlines():
        callid_line = callid_line.replace('\r','').replace('\n','')
        print ("BEGIN,--------i:%d"% (i))
        # print ("callId:\033[1;35m %s\033[0m" % callid_line)
        call_id_print (callid_line)
        call_push_process(mysql_handler, callid_line)
        print ("END,--------i:%d" % (i))
        i = i + 1

    mysql_handler.release_resource()

