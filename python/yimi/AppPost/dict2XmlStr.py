#!/usr/bin/python

import xml.etree.ElementTree as ET
import json

'''
# create root node
request = ET.Element("request")

# create sub node, add attr
callId = ET.SubElement(request, "callId")
callId.text = "api18010495368sfdsafas112234xbya"
accountSid = ET.SubElement(request, "accountSid")
accountSid.text = "3hf3hf3hf3fh3h3ddk3dk3dk3dkdjk3j"

# create elementtree obj
tree = ET.ElementTree(request)
print(ET.tostring(request, encoding='UTF-8'))
'''

'''
dict = {}
dict['callId']='api18010495368sfdsafas112234xbya'
dict['accountSid']='3hf3hf3hf3fh3h3ddk3dk3dk3dkdjk3j'

request = ET.Element("request")
for key in dict.keys():
    a = ET.SubElement(request, key)
    a.text = dict[key]
print(ET.tostring(request, encoding='UTF-8'))
'''

def dict2XmlString(dataDict):
    # create root node
    request = ET.Element("request")
    for key in dataDict.keys():
        # create sub node, add attr
        node = ET.SubElement(request, key)
        node.text = dataDict[key]
        #print (node.text)
    return ET.tostring(request, encoding='UTF-8')

def dict2JsonString(dataDict):
    temp_dict = {}
    temp_dict['request']=dataDict
    return json.dumps(temp_dict)

if __name__ == '__main__':
    dict = {}
    dict['callId']='api18010495368sfdsafas112234xbya'
    dict['accountSid']='3hf3hf3hf3fh3h3ddk3dk3dk3dkdjk3j'
    dict['workNumber']=None
    print(dict2XmlString(dict))
    print(dict2JsonString(dict))
