# -*- coding: utf-8 -*-
import os
import time
import base64
import platform
import re
import disk_sn_collect
import Hard_collect
import urllib
import urllib2
import json

Text = {'Ip':'','information':[]}


def getverson():
    Text['information'].append(Hard_collect.SYSTEM().system())


def getmemory():

    Text['information'].append(Hard_collect.MEMORY().memory())


def getserver():
    Text['information'].append(Hard_collect.SERVER().server())



def getnetwork():
    Text['information'].append(Hard_collect.NETWORK().network())



def getcpu():
    Text['information'].append( Hard_collect.CPU().cpu())

def getcontrolIP():
    Text['information'].append(Hard_collect.IP().ip())


def getip():            ###get IP 
    try:
        f=os.popen('ls /etc/sysconfig/network-scripts/|grep ifcfg-|grep -v lo').readlines()
        for line in f:
            m=os.popen('cat /etc/sysconfig/network-scripts/{0}|grep IPADDR'.format(line.replace('\n',''))).readlines()
            if m:
                break
        #print "get IP ADDR "+m[0].split('=')[1].replace('\n','')
        return m[0].split('=')[1].replace('\n','')
    except:
        pass


def url_request(date):     ####通过POST方法发送date到指定端口
    mainurl="http://{0}:{1}/{2}".format("172.30.50.159","8000","test/api")
    try:
        data_encode = urllib.urlencode(date)
       
        req = urllib2.Request(url=mainurl,data=data_encode)
        res_data = urllib2.urlopen(req)
        res = res_data.read()

    except:
        pass


def main():

    getmemory()
    getserver() 
    getcpu()
    getverson()
    getnetwork()
    getcontrolIP()
    Text['information'].append(disk_sn_collect.returnall())
    # print Text
    url_request(Text)

if __name__ == '__main__':    
    Text['Ip'] = getip()
    main()
