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

Text = {'information':{}}


def getverson():
    Text['information']['system_node'] = Hard_collect.SYSTEM().system_node()
    Text['information']['system_sys_name']=Hard_collect.SYSTEM().system_sys_name()
    Text['information']['system_sys_verson']=Hard_collect.SYSTEM().system_sys_verson()
    Text['information']['system_sys_code']=Hard_collect.SYSTEM().system_sys_code()
    Text['information']['system_release']=Hard_collect.SYSTEM().system_release()
    Text['information']['system_machine']=Hard_collect.SYSTEM().system_machine()



def getmemory():

    Text['information']['memory_sn']=Hard_collect.MEMORY().memory_sn()
    Text['information']['memory_size']=Hard_collect.MEMORY().memory_size()
    Text['information']['memory_type']=Hard_collect.MEMORY().memory_type()




def getserver():
    Text['information']['server_sn']=Hard_collect.SERVER().server_sn()
    Text['information']['server_type']=Hard_collect.SERVER().server_type()
    Text['information']['server_product']=Hard_collect.SERVER().server_product()



def getnetwork():
    Text['information']['network_name']=Hard_collect.NETWORK().network_name()
    Text['information']['network_ip']=Hard_collect.NETWORK().network_ip()
    Text['information']['network_mac']=Hard_collect.NETWORK().network_mac()


def getcpu():
    Text['information']['cpu_name']=Hard_collect.CPU().cpu_name()
    Text['information']['cpu_processor']=Hard_collect.CPU().cpu_processor()
    Text['information']['physical_number']=Hard_collect.CPU().physical_number()
    Text['information']['cpu_size']=Hard_collect.CPU().cpu_size()
    Text['information']['cpu_rart']=Hard_collect.CPU().cpu_rart()



def getcontrolIP():
    Text['information']['outer_ip']=Hard_collect.IP().outer_ip()
    Text['information']['intranet_ip']=Hard_collect.IP().intranet_ip()
    Text['information']['management_ip']=Hard_collect.IP().management_ip()






def url_request(date):     ####通过POST方法发送date到指定端口
    mainurl="http://{0}:{1}/{2}".format("172.30.50.159","8000","test/api")
    try:
        # print date
        data_encode = urllib.urlencode(date)
        # print data_encode
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
    Text['information']['disk']=disk_sn_collect.returnall()
    # print Text
    url_request(Text)

if __name__ == '__main__':    
    main()
