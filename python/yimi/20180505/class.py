#!/usr/bin/python3
# -*- coding:utf-8 -*-

#
# Attention: for python 3.x syntax
# auth: PhoenixChan@emicnet
# 
import sys 
import getopt
import requests
import time
import base64
import hashlib
import json
try:
    from cStringIO import io
except ImportError:
    from io import StringIO

Host="http://apiusertest.emic.com.cn/"
softVersion="20171106"
accountSid="4977d4c17ec83b4102de416d4f2c9e25"
token="eddb4913c5e16511a605851f679c7262"
subAccountSid="c87db2e6a81adbadb4e092edfd8ec3bf"
subToken="32f02669b9dcd969e8329f1127e5377f"
appId="cd19d5db9b8bf1469affd75333bdbac4"
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

    def formatAuthorization(self, isSubAccount=0):
        if isSubAccount:
            #return str(base64.b64encode((self.__subAccountSid+ ":" + getTimestamp()).encode('utf-8')), 'utf-8')
            return (base64.b64encode((self.__subAccountSid+ ":" + getTimestamp()).encode('utf-8'))).decode('utf-8')
        else:
            #return str(base64.b64encode((self.__accountSid + ":" + getTimestamp()).encode('utf-8')), 'utf-8')
            return (base64.b64encode((self.__accountSid + ":" + getTimestamp()).encode('utf-8'))).decode('utf-8')

    def formatSignature(self, isSubAccount):
        if isSubAccount:
            return (hashlib.md5((self.__subAccountSid+self.__subToken+getTimestamp()).encode('utf-8'))).hexdigest().upper()
        else:
            return (hashlib.md5((self.__accountSid+self.__token+getTimestamp()).encode('utf-8'))).hexdigest().upper()

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

    def formatUrl(self, function, operation, isSubAccount=False):
        #if operation == "AccountInfo":
        if isSubAccount:
            return self.__url+self.__softVersion+"/SubAccounts/"+self.__subAccountSid+"/"+function+"/"\
                    +operation+"?sig="+self.formatSignature(isSubAccount)
        else:
            return self.__url+self.__softVersion+"/Accounts/"+self.__accountSid+"/"+function+"/"\
                    +operation+"?sig="+self.formatSignature(isSubAccount)
    def getAccountInfo(self):
        respData = dict(code=0, data='')
        auth = self.formatAuthorization()
        postData = ''
        contentLength = str(len(postData))
        headers = self.formatHttpHeaders(JSON_DATA_FORMAT, auth, contentLength)
        url = self.formatUrl("", "AccountInfo");

        response = requests.post(url, headers=headers, data=postData, timeout=10)
        respData['code'] = response.status_code
        respData['data'] = response.text
        return respData

    def callBackOp(self, caller, called, userData):
        respData = dict(code=0, data='')
        auth = self.formatAuthorization(True)
        postData = {"callBack": {"appId": self.__appId, "from": caller,"to": called, "userData": userData}}
        postData = json.dumps(postData)
        contentLength = str(len(postData))
        headers = self.formatHttpHeaders(JSON_DATA_FORMAT, auth, contentLength)
        url = self.formatUrl("Calls", "callBack", True);

        response = requests.post(url, headers=headers, data=postData, timeout=10)
        respData['code'] = response.status_code
        respData['data'] = response.text
        return respData
    '''
    @EmicallPost, return a dictionary struct
    '''
    def EmicallPost(self, isSubAccount, XmlOrJson, function, operation, data):
        respData = dict(code=0, data='')

        contentLength = str(len(data))
        auth = self.formatAuthorization(isSubAccount)
        headers = self.formatHttpHeaders(XmlOrJson, auth, contentLength)
        url = self.formatUrl(function, operation, isSubAccount)

        response = requests.post(url, headers=headers, data=data, timeout=10)
        #print ("code:%d\ninfo:%s"%(response.status_code, response.text))
        respData['code']=response.status_code
        respData['data']=response.text
        #print ("code:%d\ninfo:%s"%(respData['code'], respData['data']))
        #return respData
        return dict(code=response.status_code, data=response.text)

'''
Attention plz:
@OPERATION, different value, different operate
'''
OPERATION="AccountInfo"
#OPERATION="callBack"

def main(argv=None):
    if argv is None:
        argv=sys.argv
        '''__init__(self, url, softVersion, accountSid, token, subAccountSid, subToken, appId):'''
    print (sys.version)
    '''
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

    '''
    EmicallOp = EmicallDevOperation(Host, softVersion, accountSid, token, subAccountSid, subToken, appId)

    #respData = EmicallOp.EmicallPost(isSubAccount, JSON_DATA_FORMAT, function, OPERATION, postData)
    # 01: getAccountInfo
    if 1:
        respData = EmicallOp.getAccountInfo()
        print ("respData: \n######\ncode:%d\ndata:%s\n"%(respData['code'],respData['data']), end="")
        print ("######")
    #02: callBack
    if 0:
        respData = EmicallOp.callBackOp('18010495368','10086','ikkiPhoenix')
        print ("respData: \n######\ncode:%d\ndata:%s\n"%(respData['code'],respData['data']), end="")
        print ("######")

if __name__ == "__main__":
    main()
    #sys.exit(main)

