#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys

file_name='./callid.csv'
w_file='./callid_sql.sql'

def construct_t_call_record_sql(input_file, output_file):
    write_obj = open(output_file, 'w+')
    file_obj = open(input_file, 'r')
    sql_str_list=[]
    for line in file_obj.readlines():
        line = line.replace('\r','').replace('\n','')
        sql_str = 'select `appId`,`callId`, `provinceId`, `enterpriseId`,`status` from call_records where `callId`="%s";' % (line)
        write_obj.write(sql_str+'\n')
        sql_str_list.append(sql_str)
        print sql_str
    return sql_str_list

if __name__ ==  '__main__':
    list = construct_t_call_record_sql(file_name, w_file)
    print list[-1];
