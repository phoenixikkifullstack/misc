#!/usr/bin/python

import requests

DATA_FORMAT_XML     =   0
DATA_FORMAT_JSON    =   1
DATA_FORMAT_FORM    =   2

def call_push(url, xmlOrJson, post_data=None, time_out=10):
    response={}
    if post_data:
        content_length=len(post_data)
    else:
        content_length=0
    if xmlOrJson == DATA_FORMAT_XML:
        header = {
            "Accept":"application/xml",
            "Content-Type":"application/xml;charset=utf-8",
            "Content-Length":content_length
        }
    elif xmlOrJson == DATA_FORMAT_JSON:
        header = {
            "Accept":"application/json",
            "Content-Type":"application/json;charset=utf-8",
            "Content-Length":content_length
        }
    elif xmlOrJson == DATA_FORMAT_FORM:
        header = {
            "Accept":"application/json",
            "Content-Type":"application/x-www-form-urlencoded",
            "Content-Length":content_length
        }
    r = requests.post(url, headers=header, data=post_data, timeout=time_out, verify=False)
    response['code'] = r.status_code
    response['data'] = r.text.encode('utf-8')
    return response

url='http://121.42.167.166/hello/aaa'
post_data="hello world"
if __name__ == '__main__':
    try:
        res = call_push(url, DATA_FORMAT_JSON, post_data)
        print(res['code'], res['data'])
    except Exception, e:
        print ("call_push failed,%s" % repr(e))

