# -*- coding: utf-8 -*-
import os
import time
import base64
import platform
import re
import disk_sn_collect
import Hard_collect
import sys
if sys.version > '3':
    import urllib.request
    from urllib import parse
else:
    import urllib
    import urllib2

import json
import threading
import traceback

Text = {}
Text2 = {"information":{}}

def getverson():
    Text['os_info'] = {'kernel':Hard_collect.SYSTEM().system_release(),'name_id':Hard_collect.SYSTEM().system_sys_name()+' '+Hard_collect.SYSTEM().system_sys_verson()+' '+Hard_collect.SYSTEM().system_sys_code()}
    Text['hostname']=Hard_collect.SYSTEM().system_node()
    Text['os_info']['bit'] = '64' if Hard_collect.SYSTEM().system_machine() == 'x86_64' else '32'

def getmemory():
    Text['memory_info']=[]
    if check_virutal():
        Text['memory_num'] = len(Hard_collect.MEMORY().memory_size())
        sns = Hard_collect.MEMORY().memory_sn()
        types = Hard_collect.MEMORY().memory_type()
        sizes = Hard_collect.MEMORY().memory_size()
        for x in range(Text['memory_num']):
            if not re.search(r'(\w{8,})',sns[x]):
                sns[x] = "UNKNOWN"
            if types[x].replace(" ","") == '<OUTOFSPEC>' or types[x].replace(" ","") == 'Other':
                types[x] = "UNKNOWN"
            Text['memory_info'].append({'sn':sns[x],'type':types[x].replace(" ",""),'size':sizes[x]})
    else:
        Text['memory_info'].append({'sn':'','type':'','size':Hard_collect.MEMORY().memory_size()})


def getserver():
    Text['sn']=Hard_collect.SERVER().server_sn()
    Text['model_info']={'brand':Hard_collect.SERVER().server_type().upper(),'model':Hard_collect.SERVER().server_product().upper()}
    # Text['model']=Hard_collect.SERVER().server_product()
    # Text['brand']=Hard_collect.SERVER().server_type()


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


def check_virutal():    ##  python版本过低不支持三目运算符 if 'Virtual' in os.popen('dmidecode -s system-product-name').readline()
    if 'Virtual' in os.popen('dmidecode -s system-product-name').readline():
        return 0  
    else:
        return 1


def getdisk():
    if check_virutal():
        disk=disk_sn_collect.returnall()
        Text['hdd_info']=[]
        Text['ssd_info']=[]
        Text['sd_info']=[]
        Text['raid_info'] =[]
        Text['logical_capacity'] = disk['Logic_capacity']
        for x in range(len(disk['Raid_Name'])):
            Text['raid_info'].append({'name':disk['Raid_Name'][x].replace(" ",""),'level':disk['Raid_Level'][x].replace(" ",""),'size':disk['Raid_Size'][x].replace(" ","")})
        for x in range(len(disk['Size'])):
            if disk['MediaType'][x] =='Hard Disk Device':
                Text['hdd_info'].append({'sn':disk['SN'][x],'model':disk['Type'][x].upper(),'interface':disk['PDtype'][x].upper(),'size':disk['Size'][x].replace(" ",""),'life':'','commit':disk['NAME'][x]})
            elif disk['MediaType'][x] =='Solid State Device':
                Text['ssd_info'].append({'sn':disk['SN'][x],'model':disk['Type'][x].upper(),'interface':disk['PDtype'][x].upper(),'size':disk['Size'][x].replace(" ",""),'life':'','commit':disk['NAME'][x]})
            # elif "HP" in disk['MediaType'][x] :
            #     Text['hdd_info'].append({'sn':disk['SN'][x],'model':disk['Type'][x],'interface':disk['PDtype'][x],'size':disk['Size'][x],'life':'','commit':disk['NAME'][x]})
            else:
                Text['sd_info'].append({'sn':disk['SN'][x],'model':disk['Type'][x].upper(),'interface':disk['PDtype'][x].upper(),'size':disk['Size'][x].replace(" ",""),'life':'','commit':disk['NAME'][x]})
    else:
        Text['logical_capacity'] = disk_sn_collect.returnall()

def getfilesystem():
    filesystem = Hard_collect.FILESYSTEM().filesystem()
    Text['file_info'] =[]
    for x in range(len(filesystem['Name'])):
        Text['file_info'].append({'name':filesystem['Name'][x],'type':filesystem['Type'][x]})

def url_request(date):     ####通过POST方法发送date到指定端口
    mainurl="http://10.21.8.30:8090/api/Auto_Data/postPhysicalServerInfo"
    try:
        #print (date)
        # print data_encode
        if sys.version > '3':
            data_encode = urllib.parse.urlencode(date).encode('utf-8')
            res_data = urllib.request.urlopen(url=mainurl,data=data_encode,timeout = 10)
        else:
            data_encode = urllib.urlencode(date)
            req = urllib2.Request(url=mainurl,data=data_encode)
            res_data = urllib2.urlopen(req,timeout = 10)
        res = res_data.read()
    except:
        traceback.print_exc()
        pass

def url_request2(date):     ####通过POST方法发送date到指定端口
    mainurl="http://{0}:{1}/{2}".format("172.30.50.98","8000","test/api")
    try:
        #print (date)
        # print data_encode
        if sys.version > '3':
            data_encode = urllib.parse.urlencode(date).encode('utf-8')
            res_data = urllib.request.urlopen(url=mainurl,data=data_encode,timeout = 10)
        else:
            data_encode = urllib.urlencode(date)
            req = urllib2.Request(url=mainurl,data=data_encode)
            res_data = urllib2.urlopen(req,timeout = 10)
        res = res_data.read()
    except:
        traceback.print_exc()
        pass

def main():
    if check_virutal():
        getmemory()
        getserver() 
        getcpu()
        getverson()
        getnetwork()
        getcontrolIP()
        getdisk()
        getfilesystem()

        Text2['information'] = Text
        # print Text2
        # 
        t1 = threading.Thread(target = url_request,args =[Text])
        t2 = threading.Thread(target = url_request2,args =[Text2])
        t1.start()
        # t1.join()
        t2.start()

if __name__ == '__main__':    
    main()
