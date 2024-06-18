#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys 
import getopt
import requests
import time
import base64
import hashlib
import json
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

Host="http://apitest.emic.com.cn/"
softVersion="20170405"
accountSid="2b6d72a46e996ac75fcac9d884130f50"
token="491c060d93723664102919be073a442b"
subAccountSid="06f9b230399bfa819f240d2959c684aa"
subToken="e27cedb633ea56cb15cb40e029ddd02e"
appId="953f56dc6bbd367da37d58efd06d0c83"
XML_DATA_FORMAT = 1
JSON_DATA_FORMAT = 0

def getTimestamp():
    return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

class EmicallDevOperation(object):
    def __init__(self, url, softVersion, accountSid, token, subAccountSid, subToken, appId):
        self.__url = url
        self.__softVersion = softVersion
        self.__accountSid = accountSid
        self.__token = token
        self.__subAccountSid = subAccountSid
        self.__subToken = subToken
        self.__appId = appId

    def formatAuthorization(self, isSubAccount):
        if isSubAccount:
            return base64.b64encode(self.__subAccountSid+ ":" + getTimestamp())
        else:
            return base64.b64encode(self.__accountSid + ":" + getTimestamp())

    def formatSignature(self, isSubAccount):
        if isSubAccount:
            return (hashlib.md5(self.__subAccountSid+self.__subToken+getTimestamp())).hexdigest().upper()
        else:
            return (hashlib.md5(self.__accountSid+self.__token+getTimestamp())).hexdigest().upper()

    def formatHttpHeaders(self, isXmlOrJson, Auth, contentLength):
        if isXmlOrJson:
            header={
                    "Accept":"application/xml",
                    "Content-Type":"application/xml;charset=utf-8",
                    "Content-Length":contentLength,
                    "Authorization":Auth
                    }
        else:
            header={
                    "Accept":"application/json",
                    "Content-Type":"application/json;charset=utf-8",
                    "Content-Length":contentLength,
                    "Authorization":Auth
                    }
        return header

    def formatUrl(self, function, operation, isSubAccount):
        #if operation == "AccountInfo":
        if isSubAccount:
            return self.__url+self.__softVersion+"/SubAccounts/"+self.__subAccountSid+"/"+function+"/"\
                    +operation+"?sig="+\
                    self.formatSignature(isSubAccount)
        else:
            return self.__url+self.__softVersion+"/Accounts/"+self.__accountSid+"/"+function+"/"\
                    +operation+"?sig="+\
                    self.formatSignature(isSubAccount)
    '''
    @EmicallPost, return a dictionary struct
    '''
    def EmicallPost(self, isSubAccount, XmlOrJson, function, operation, data):
        respData = dict(code=0, data='')

        contentLength = len(data)
        auth = self.formatAuthorization(isSubAccount)
        headers = self.formatHttpHeaders(XmlOrJson, auth, contentLength)
        url = self.formatUrl(function, operation, isSubAccount)
        response = requests.post(url, headers=headers, data=data, timeout=10)
        #print ("code:%d\ninfo:%s")%(response.status_code, response.text)
        respData['code']=response.status_code
        respData['data']=response.text
        #print ("code:%d\ninfo:%s")%(respData['code'], respData['data'])
        #return respData
        return dict(code=response.status_code, data=response.text)

'''
Attention plz:
@OPERATION, different value, different operate
'''
#OPERATION="AccountInfo"
OPERATION="callBack"

def main(argv=None):
    if argv is None:
        argv=sys.argv
        '''__init__(self, url, softVersion, accountSid, token, subAccountSid, subToken, appId):'''
    function=""
    postData=""
    isSubAccount=False

    if OPERATION.strip() == "AccountInfo":
        function=""
        postData=""
    elif OPERATION.strip() == "callBack":
        function = "Calls"
        postData = {"callBack": {"appId": appId, "from": "18010495368","to": "10086", "userData": "ikkiPhoenix"}}
        postData = json.dumps(postData)
        isSubAccount=True

    EmicallOp = EmicallDevOperation(Host, softVersion, accountSid, token, subAccountSid, subToken, appId)

    respData = EmicallOp.EmicallPost(isSubAccount, JSON_DATA_FORMAT, function, OPERATION, postData)
    print ("respData: \n######\ncode:%d\ndata:%s\n")%(respData['code'],respData['data'])
    print ("######")

if __name__ == "__main__":
    main()
    #sys.exit(main)

