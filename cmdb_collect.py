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

Text = {}
Text2 = {"information":{}}

def getverson():
    Text['os_info'] = {'kernel':Hard_collect.SYSTEM().system_release(),'bit':Hard_collect.SYSTEM().system_machine(),'name_id':Hard_collect.SYSTEM().system_sys_name()+' '+Hard_collect.SYSTEM().system_sys_verson()+' '+Hard_collect.SYSTEM().system_sys_code()}



def getmemory():
    Text['memory_info']=[]
    if check_virutal():
        Text['memory_num'] = len(Hard_collect.MEMORY().memory_size())
        for x in range(Text['memory_num']):
            Text['memory_info'].append({'sn':Hard_collect.MEMORY().memory_sn()[x],'type':Hard_collect.MEMORY().memory_type()[x],'size':Hard_collect.MEMORY().memory_size()[x]})
    else:
        Text['memory_info'].append({'sn':'','type':'','size':Hard_collect.MEMORY().memory_size()})


def getserver():
    Text['sn']=Hard_collect.SERVER().server_sn()
    Text['model']=Hard_collect.SERVER().server_type()
    Text['brand']=Hard_collect.SERVER().server_product()


def getnetwork():
    Text['nic_info']=[]

    for x in range(len(Hard_collect.NETWORK().network_name())):
        Text['nic_info'].append({'name':Hard_collect.NETWORK().network_name()[x],'ip':Hard_collect.NETWORK().network_ip()[x],'mac':Hard_collect.NETWORK().network_mac()[x]})


def getcpu():
    Text['cpu_info'] = {'model':Hard_collect.CPU().cpu_name(),'kernel_num':Hard_collect.CPU().cpu_processor(),'num':Hard_collect.CPU().physical_number(),'bit':Hard_collect.CPU().cpu_size(),'rate':Hard_collect.CPU().cpu_rart()}



def getcontrolIP():
    Text['ext_ip']=Hard_collect.IP().outer_ip()
    Text['int_ip']=Hard_collect.IP().intranet_ip()
    Text['oob_ip']=Hard_collect.IP().management_ip()


def check_virutal():
    return 0 if 'Virtual' in os.popen('dmidecode -s system-product-name').readline() else 1



def url_request(date):     ####通过POST方法发送date到指定端口
    # mainurl="http://{0}:{1}/{2}".format("172.30.50.159","8000","test/api")
    # http://10.21.8.30:8090/api/Auto_Data/postPhysicalServerInfo
    mainurl="http://10.21.8.30:8090/api/Auto_Data/postPhysicalServerInfo"
    try:
        # print date
        data_encode = urllib.urlencode(date)
        # print data_encode
        
        req = urllib2.Request(url=mainurl,data=data_encode)
        res_data = urllib2.urlopen(req)
        res = res_data.read()

    except:
        pass

def url_request2(date):     ####通过POST方法发送date到指定端口
    mainurl="http://{0}:{1}/{2}".format("172.30.50.159","8000","test/api")
    try:
        # print date
        data_encode = urllib.urlencode(date)
        # print data_encode
        req = urllib2.Request(url=mainurl,data=data_encode,timeout = 10)
        res_data = urllib2.urlopen(req)
        res = res_data.read()

    except:
        pass

def getdisk():
    if check_virutal():
        disk=disk_sn_collect.returnall()
        Text['hdd_info']=[]
        Text['ssd_info']=[]
        Text['sd_info']=[]
        Text['raid_info'] =[]
        Text['logical_capacity'] = disk['Logic_capacity']
        for x in range(len(disk['Raid_Name'])):
            Text['raid_info'].append({'name':disk['Raid_Name'][x],'level':disk['Raid_Level'][x],'size':disk['Raid_Size'][x]})
        for x in range(len(disk['Size'])):
            if disk['MediaType'][x] =='Hard Disk Device':
                Text['hdd_info'].append({'sn':disk['SN'][x],'model':disk['Type'][x],'interface':disk['PDtype'][x],'size':disk['Size'][x],'life':'','commit':disk['NAME'][x]})
            elif disk['MediaType'][x] =='Solid State Device':
                Text['ssd_info'].append({'sn':disk['SN'][x],'model':disk['Type'][x],'interface':disk['PDtype'][x],'size':disk['Size'][x],'life':'','commit':disk['NAME'][x]})
            # elif "HP" in disk['MediaType'][x] :
            #     Text['hdd_info'].append({'sn':disk['SN'][x],'model':disk['Type'][x],'interface':disk['PDtype'][x],'size':disk['Size'][x],'life':'','commit':disk['NAME'][x]})
            else:
                Text['sd_info'].append({'sn':disk['SN'][x],'model':disk['Type'][x],'interface':disk['PDtype'][x],'size':disk['Size'][x],'life':'','commit':disk['NAME'][x]})
    else:
        Text['logical_capacity'] = disk_sn_collect.returnall()

def getfilesystem():
    filesystem = Hard_collect.FILESYSTEM().filesystem()
    Text['file_info'] =[]
    for x in range(len(filesystem['Name'])):
        Text['file_info'].append({'name':filesystem['Name'][x],'type':filesystem['Type'][x]})

def main():

    getmemory()
    getserver() 
    getcpu()
    getverson()
    getnetwork()
    getcontrolIP()
    getdisk()
    getfilesystem()
    print Text
    # Text2['information'] = Text
    # print Text2
    url_request(Text)
    # url_request2(Text2)

if __name__ == '__main__':    
    main()
