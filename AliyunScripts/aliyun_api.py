#!/usr/bin/python2
# -*- coding:utf-8 -*-

import sys
import urllib, urllib2
import base64
import hmac
from hashlib import sha1
import time
import uuid

class AliyunAPI:
    def __init__(self):
        self.interface = sys.argv[1]
        self.ecs_server_address = "http://" + interface + ".aliyuncs.com"
        self.access_key_id = ''
        self.access_key_secret = ''

    def percentEncode(self, str):
        res = urllib.quote(str.decode(sys.stdin.encoding).encode('utf8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

    def computeSignature(self, parameters, access_key_secret):
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        canonicalizedQueryString = ''
        for (k,v) in sortedParameters:
            canonicalizedQueryString += '&' + self.percentEncode(k) + '=' + self.percentEncode(v)
        stringToSign = 'GET&%2F&' + self.percentEncode(canonicalizedQueryString[1:])
        h = hmac.new(access_key_secret + "&", stringToSign, sha1)
        signature = base64.encodestring(h.digest()).strip()
        return signature

    def composeUrl(self, user_params,user_version):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        parameters = { \
                'Format'        : 'JSON', \
                'Version'       : user_version, \
                'AccessKeyId'   : self.access_key_id, \
                'SignatureVersion'  : '1.0', \
                'SignatureMethod'   : 'HMAC-SHA1', \
                'SignatureNonce'    : str(uuid.uuid1()), \
                'Timestamp'         : timestamp, \
        }
        for key in user_params.keys():
            parameters[key] = user_params[key]
        signature = self.computeSignature(parameters, self.access_key_secret)
        parameters['Signature'] = signature
        url = self.ecs_server_address + "/?" + urllib.urlencode(parameters)
        return url

    def makeRequest(self, user_params,user_version,quiet=False):
        url = self.composeUrl(user_params,user_version)
        try:
            req = urllib2.Request(url)
            res_data = urllib2.urlopen(req)
            res = res_data.read()
            return res
        except Exception,e:
            return e.read()

if __name__ == '__main__':
    interface = sys.argv[1]
    with open('params.txt','r') as f:
        params = eval(f.read())

    with open('VersionApi.txt','r') as g:
        version = eval(g.read())[interface]

    f=AliyunAPI()
    res=f.makeRequest(params,version)
    print(res)
