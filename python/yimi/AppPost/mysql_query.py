#!/usr/bin/python

import MySQLdb
import MySQLdb.cursors
import time
import datetime

DB_HOST='127.0.0.1'
DB_USER='root'
DB_PASS='123456'
DB_NAME='EmicallDev_system'
#DB_PASS='Emicnet123456'
#DB_NAME='EmicallDev_system'

class emi_mysql:
    def __init__(self, host, user, passwd, db_name):
        db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db_name, cursorclass=MySQLdb.cursors.DictCursor)
        self.db = db
        self.cursor = db.cursor()
    def sql_exec(self, sql_str):
        self.cursor.execute(sql_str)
        return self.cursor.fetchall()
    def release_resource(self):
        self.cursor.close()
        self.db.close()

def construct_ep_sql(provinceId, enterpriseId):
    sql = "select `domain`, `port`, `httpPort`, `httpUser`, `httpPasswd` from enterprises where provinceId=%d and enterpriseId=%d" % (provinceId, enterpriseId)
    return sql

def construct_app_sql(appId):
    sql = "select `callreqUrl`, `callestablishUrl`, `callhangupUrl`, `voicecodeUrl`, `voicenotifyUrl`, `recordReadyNotifyUrl`, `appCallbackDataFormat` from applications where appId='%s'" % (appId)
    return sql

def construct_call_records_sql(callId):
    sql = "select `type`,`accountSid`,`subAccountSid`,`appId`,`provinceId`,`enterpriseId`,`switchNumber`,`callId`,`ccNumber`,`caller`,`called`,`status`,`duration`,`userData`,`ruleId` from call_records where `callId`='%s'" % (callId)
    return sql

def construct_call_details_sql(callId):
    sql = "select `callId`,`caller`,`called`,`ringTime`,`establishTime`,`hangupTime`,`status`,`type`,`isCaller`,`number`,`app_callback_flag`,`stopReason` from call_details where callId='%s'" %(callId)
    return sql

def construct_ep_user_sql(provinceId, enterpriseId, number):
    sql = "select `workNumber` from enterprise_users where provinceId=%lu and enterpriseId=%lu and number='%s'" % (provinceId, enterpriseId, number)
    return sql

def mysql_query(exec_sql):
    #cursorclass = MySQLdb.cursors.DictCursor
    #db = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASS, db = DB_NAME, cursorclass = MySQLdb.cursors.DictCursor)
    #cursor = db.cursor()
    db = MySQLdb.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASS, db = DB_NAME, cursorclass = MySQLdb.cursors.DictCursor)
    #cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute(exec_sql)
    res = cursor.fetchall()
    cursor.close()
    db.close()
    return res

#callId='api1010001447a1532087694215jTPIn'
callId='1533711440980702conf_1533711434203'
if __name__ == '__main__':
    # print ("hello world")
    # print mysql_query(construct_ep_sql(101, 65614))

    ret_tup = mysql_handler.sql_exec(construct_call_records_sql(callId))
    print (ret_tup[0])
    ret_tup = mysql_handler.sql_exec(construct_call_details_sql(callId))
    print (ret_tup)

    # for i in range(len(ret_tup)):
    #     print (ret_tup[i])
