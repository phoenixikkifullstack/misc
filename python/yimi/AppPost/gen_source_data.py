#!/usr/bin/python

import time
import datetime
from mysql_query import *
from dict2XmlStr import *

CALL_PUSH_RINGING   = 0
CALL_PUSH_ESTABLISH = 2
CALL_PUSH_HANGUP    = 3
CALL_PUSH_RECORDS   = 5

# 0000 0000
CALL_PUSH_URL_BIT_INIT          = 1
CALL_PUSH_URL_BIT_ESTABLISH     = CALL_PUSH_URL_BIT_INIT << 1
CALL_PUSH_URL_BIT_HANGUP        = CALL_PUSH_URL_BIT_INIT << 2
CALL_PUSH_URL_BIT_RECORDS       = CALL_PUSH_URL_BIT_INIT << 3
CALL_PUSH_URL_BIT_CALLREQ       = CALL_PUSH_URL_BIT_INIT << 4

def app_callpush_url_type(mysql_handler, callId):
    callpush_dict = {}
    push_url_flag = 0
    call_records = mysql_handler.sql_exec(construct_call_records_sql(callId))
    if call_records[0]['appId'].strip() != '':
        callpush_dict['call_records'] = call_records
        applications = mysql_handler.sql_exec(construct_app_sql(call_records[0]['appId']))
        if not applications:
            print ("Cann't get applications, check the source of callId first.")
            callpush_dict['push_url_flag'] = 0
            return callpush_dict
        if applications[0]['callreqUrl'] and applications[0]['callreqUrl'].strip() != '':
            push_url_flag = push_url_flag | CALL_PUSH_URL_BIT_CALLREQ 
            callpush_dict['callreqUrl'] = applications[0]['callreqUrl']
        if applications[0]['callestablishUrl'] and applications[0]['callestablishUrl'].strip() != '':
            push_url_flag = push_url_flag | CALL_PUSH_URL_BIT_ESTABLISH
            callpush_dict['callestablishUrl'] = applications[0]['callestablishUrl']
        if applications[0]['callhangupUrl'] and applications[0]['callhangupUrl'].strip() != '':
            push_url_flag = push_url_flag | CALL_PUSH_URL_BIT_HANGUP
            callpush_dict['callhangupUrl'] = applications[0]['callhangupUrl']
        if applications[0]['recordReadyNotifyUrl'] and applications[0]['recordReadyNotifyUrl'].strip() != '':
            push_url_flag = push_url_flag | CALL_PUSH_URL_BIT_RECORDS
            callpush_dict['recordReadyNotifyUrl'] = applications[0]['recordReadyNotifyUrl']
        callpush_dict['push_url_flag'] = push_url_flag
        callpush_dict['appCallbackDataFormat'] = applications[0]['appCallbackDataFormat']
        return callpush_dict
    else:
        callpush_dict['push_url_flag'] = push_url_flag
        return callpush_dict

def gen_ringing_data(mysql_handler, call_records):
    local_list = []
    #call_records = mysql_query(construct_call_records_sql(callId))
    if call_records[0]['status'] != 1 and call_records[0]['status'] != 3:
        print('Incomplete records, callId=%s' % (call_records[0]['callId']))
        return local_list

    #print("Ringing state data handling......")
    # call_details = mysql_query(construct_call_details_sql(call_records[0]['callId']))
    call_details = mysql_handler.sql_exec(construct_call_details_sql(call_records[0]['callId']))
    #print(call_details)
    for i in range(len(call_details)):
        local_dict = {}
        local_dict['callId'] = call_records[0]['callId']
        local_dict['accountSid'] = call_records[0]['accountSid']
        if call_records[0]['userData'].strip() != '':
            local_dict['userData'] = call_records[0]['userData']
        local_dict['appId'] = call_records[0]['appId']
        local_dict['caller'] = call_details[i]['caller']
        local_dict['called'] = call_details[i]['called']
        local_dict['type'] = str(0)
        #print("AAAAAAAAAAAA %d" % (call_records[0]['type']))
        local_dict['callType'] = str(call_records[0]['type'])
        if call_records[0]['type'] == 1:
            if call_records[0]['switchNumber'].strip() != '':
                local_dict['switchNumber'] = call_records[0]['switchNumber']
        if call_details[i]['number'].strip() != '':
            local_dict['number'] = call_details[i]['number'].split("_")[0]
            # work_number_dict = mysql_query(construct_ep_user_sql(call_records[0]['provinceId'], call_records[0]['enterpriseId'], call_details[i]['number']))
            work_number_dict = mysql_handler.sql_exec(construct_ep_user_sql(call_records[0]['provinceId'], call_records[0]['enterpriseId'], call_details[i]['number']))
            if work_number_dict:
                local_dict['workNumber'] = work_number_dict[0]['workNumber']
            else:
                local_dict['workNumber'] = ''
        local_list.append(local_dict)

    return local_list

def gen_establish_data(mysql_handler, call_records):
    local_list = []
    #call_records = mysql_query(construct_call_records_sql(callId))
    #call_records = mysql_handler.sql_exec(construct_call_records_sql(call_records[0]['callId']))
    if call_records[0]['status'] != 1 and call_records[0]['status'] != 3:
        print('Incomplete records, callId=%s' % (call_records[0]['callId']))
        return local_list

    #print("Establish state data handling......")
    # call_details = mysql_query(construct_call_details_sql(call_records[0]['callId']))
    call_details = mysql_handler.sql_exec(construct_call_details_sql(call_records[0]['callId']))
    for i in range(len(call_details)):
        local_dict = {}
        local_dict['callId'] = call_records[0]['callId']
        local_dict['accountSid'] = call_records[0]['accountSid']
        if call_records[0]['userData'].strip() != '':
            local_dict['userData'] = call_records[0]['userData']
        local_dict['appId'] = call_records[0]['appId']
        local_dict['caller'] = call_details[i]['caller']
        local_dict['called'] = call_details[i]['called']
        if call_details[i]['establishTime']:
            local_dict['startTime'] = call_details[i]['establishTime'].strftime("%Y%m%d%H%M%S")
        local_dict['type'] = str(2)
        #print("AAAAAAAAAAAA %d" % (call_records[0]['type']))
        local_dict['callType'] = str(call_records[0]['type'])
        if call_records[0]['type'] == 1:
            if call_records[0]['switchNumber'].strip() != '':
                local_dict['switchNumber'] = call_records[0]['switchNumber']

        if call_details[i]['ringTime'] and call_details[i]['establishTime']:
            if time.mktime(call_details[i]['ringTime'].timetuple()) > 0 and time.mktime(call_details[i]['establishTime'].timetuple()) > 0:
                local_dict['ringDuration'] = str(int(time.mktime(call_details[i]['establishTime'].timetuple()) - time.mktime(call_details[i]['ringTime'].timetuple())))
        
        if call_details[i]['number'].strip() != '':
            local_dict['number'] = call_details[i]['number'].split("_")[0]
            # work_number_dict = mysql_query(construct_ep_user_sql(call_records[0]['provinceId'], call_records[0]['enterpriseId'], call_details[i]['number']))
            work_number_dict = mysql_handler.sql_exec(construct_ep_user_sql(call_records[0]['provinceId'], call_records[0]['enterpriseId'], call_details[i]['number']))
            if work_number_dict:
                local_dict['workNumber'] = work_number_dict[0]['workNumber']
            else:
                local_dict['workNumber'] = ''
        local_list.append(local_dict)

    return local_list

def gen_hangup_data(mysql_handler, call_records):
    local_list = []
    #call_records = mysql_query(construct_call_records_sql(callId))
    if call_records[0]['status'] != 1 and call_records[0]['status'] != 3:
        print('Incomplete records, callId=%s' % (call_records[0]['callId']))
        return local_list

    #print("Hangup state data handling......")
    # call_details = mysql_query(construct_call_details_sql(call_records[0]['callId']))
    call_details = mysql_handler.sql_exec(construct_call_details_sql(call_records[0]['callId']))
    for i in range(len(call_details)):
        local_dict = {}
        local_dict['callId'] = call_records[0]['callId']
        local_dict['accountSid'] = call_records[0]['accountSid']
        if call_records[0]['userData'].strip() != '':
            local_dict['userData'] = call_records[0]['userData']
        local_dict['appId'] = call_records[0]['appId']
        local_dict['caller'] = call_details[i]['caller']
        local_dict['called'] = call_details[i]['called']

        if call_details[i]['establishTime'] and call_details[i]['hangupTime']:
            if time.mktime(call_details[i]['establishTime'].timetuple()) > 0:
                local_dict['startTime'] = call_details[i]['establishTime'].strftime("%Y%m%d%H%M%S")
                if time.mktime(call_details[i]['hangupTime'].timetuple()) > 0:
                    local_dict['stopTime'] = call_details[i]['hangupTime'].strftime("%Y%m%d%H%M%S")
                    local_dict['duration'] = str(int(time.mktime(call_details[i]['hangupTime'].timetuple()) - time.mktime(call_details[i]['establishTime'].timetuple())))

        if call_records[0]['status'] == 3:
            local_dict['state'] = str(0)
        else:
            local_dict['state'] = str(1)

        if call_details[i]['status'] == 1:
            local_dict['type'] = str(1)
        elif call_details[i]['status'] == 3:
            local_dict['type'] = str(3)
        local_dict['callType'] = str(call_records[0]['type'])
        if call_records[0]['type'] == 1:
            if call_records[0]['switchNumber'].strip() != '':
                local_dict['switchNumber'] = call_records[0]['switchNumber']
        
        if call_details[i]['ringTime'] and call_details[i]['establishTime']:
            if time.mktime(call_details[i]['ringTime'].timetuple()) > 0 and time.mktime(call_details[i]['establishTime'].timetuple()) > 0:
                local_dict['ringDuration'] = str(int(time.mktime(call_details[i]['establishTime'].timetuple()) - time.mktime(call_details[i]['ringTime'].timetuple())))

        if call_details[i]['number'].strip() != '':
            local_dict['number'] = call_details[i]['number'].split("_")[0]
            # work_number_dict = mysql_query(construct_ep_user_sql(call_records[0]['provinceId'], call_records[0]['enterpriseId'], call_details[i]['number']))
            work_number_dict = mysql_handler.sql_exec(construct_ep_user_sql(call_records[0]['provinceId'], call_records[0]['enterpriseId'], call_details[i]['number']))
            if work_number_dict:
                local_dict['workNumber'] = work_number_dict[0]['workNumber']
            else:
                local_dict['workNumber'] = ''
        if call_records[0]['ruleId'].strip() != '':
            local_dict['ruleId'] = call_records[0]['ruleId']

        local_list.append(local_dict)

    return local_list

def gen_record_notify_data(mysql_handler, call_records, record_voice_file_url):
    local_list = []
    if call_records[0]['status'] != 3 or call_records[0]['duration'] == 0:
        print('Incomplete records, callId=%s,duration:%d' % (call_records[0]['callId'], call_records[0]['duration']))
        return local_list

    #print("record_notify data handling......")
    local_dict = {}
    local_dict['callId'] = call_records[0]['callId']
    local_dict['accountSid'] = call_records[0]['accountSid']
    local_dict['appId'] = call_records[0]['appId']
    '''
    Attention: voice code/voice notify haven't voice record
    '''
    local_dict['caller'] = call_records[0]['caller']
    local_dict['called'] = call_records[0]['called']
    local_dict['type'] = str(54)
    local_dict['state'] = str(0)
    local_dict['url'] = record_voice_file_url

    local_list.append(local_dict)
    return local_list

callId='api1010001447a1532087694215jTPIn'
if __name__ == '__main__':
    '''
    establish_list = gen_establish_data(callId)
    #print (establish_list)
    for i in range(len(establish_list)):
        temp = dict2XmlString(establish_list[i])
        print (temp)
    hangup_list = gen_hangup_data(callId)
    #print (hangup_list)
    for j in range(len(hangup_list)):
        print (dict2XmlString(hangup_list[j]))
    '''
    '''
    print (genRealPushData(True, CALL_PUSH_ESTABLISH, callId))
    print (genRealPushData(True, CALL_PUSH_HANGUP, callId))
    '''
    temp_dict = app_callpush_url_type(callId)
    print (temp_dict)
    temp_list = gen_establish_data(temp_dict['call_records'])
    print (temp_list)


