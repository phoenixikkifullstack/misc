#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import getopt
import requests
import time
import base64
import hashlib
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

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
#print ("timestamp:%s")%(getTimestamp())

def formatAuthorization(isSubAccount, accountSid, subAccountSid):
    if isSubAccount:
        return base64.b64encode(subAccountSid+ ":" + getTimestamp())
    else:
        return base64.b64encode(accountSid + ":" + getTimestamp())
#print ("Authorization: %s")% (formatAuthorization(False, accountSid, subAccountSid))

def formatSignature(isSubAccount, accountSid, Token, subAccountSid, subToken):
    if isSubAccount:
        return (hashlib.md5(subAccountSid+subToken+getTimestamp())).hexdigest().upper()
    else:
        return (hashlib.md5(accountSid+Token+getTimestamp())).hexdigest().upper()
#print ("sig:%s")% (formatSignature(False, accountSid, token, "", ""))

def formatHttpHeaders(isXmlOrJson, Auth, contentLength):
    if isXmlOrJson:
        header={
                "Accept":"application/xml",
                "Content-Type":"application/xml;charset=utf-8",
                "Authorization":Auth
                }
    else:
        header={
                "Accept":"application/json",
                "Content-Type":"application/json;charset=utf-8",
                "Authorization":Auth
                }
    return header
#print ("header:%s")%(formatHttpHeaders(1, formatAuthorization(False, accountSid, subAccountSid), 0))

def formatUrl(host, softVersion, accountSid, token, subAccountSid, subToken, function, operation, isSubAccount):
    if isSubAccount:
        return host+softVersion+"/SubAccounts/"+subAccountSid+"/"+function+"/"\
                +operation+"?sig="+formatSignature(isSubAccount,accountSid,token,subAccountSid,subToken)
    else:
        return host+softVersion+"/Accounts/"+accountSid+"/"+function+"/"\
                +operation+"?sig="+formatSignature(isSubAccount,accountSid,token,subAccountSid,subToken)
        '''
        if operation == "AccountInfo":
            return host+softVersion+"/Accounts/"+accountSid+"/"+function+"/"\
                    +operation+"?sig="+formatSignature(isSubAccount,accountSid,token,subAccountSid,subToken)
        else:
            return host+softVersion+"/Accounts/"+accountSid+"/"+function+"/"\
                    +operation+"?sig="+formatSignature(isSubAccount,accountSid,token,subAccountSid,subToken)
        '''
print formatUrl(Host, softVersion, accountSid, token, subAccountSid, subToken, "", "AccountInfo", False)
print ("header:%s")%(formatHttpHeaders(1, formatAuthorization(False, accountSid, subAccountSid), 0))

'''
url="http://apitest.emic.com.cn/"+SoftVersion+"/Accounts/"+accountSid+"/"+"AccountInfo"+"?sig="+sig
print url
'''
url=formatUrl(Host, softVersion, accountSid, token, subAccountSid, subToken, "", "AccountInfo", False)
headers=formatHttpHeaders(JSON_DATA_FORMAT, formatAuthorization(False, accountSid, subAccountSid), 0)

response=requests.post(url,headers=headers, timeout=10)
print ("response.status_code:%d, headers:%s"% (response.status_code,response.headers))
print response.text

def main(argv=None):
    if argv is None:
        argv = sys.argv

'''
if __name__ == "__main__":
    sys.exit((main))
'''


