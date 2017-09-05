# -*- coding: utf-8 -*-
import os
import time
import base64
import platform
import re
import disk_sn_collect
import Hard_collect

def printifeng():
    banner = 'IF8gIF9fCihfKS8gX3wgX19fIF8gX18gICBfXyBfCnwgfCB8XyAvIF8gXCAnXyBcIC8gX2AgfAp8IHwgIF98ICBfX' \
             'y8gfCB8IHwgKF98IHwKfF98X3wgIFxfX198X3wgfF98XF9fLCB8CiAgICAgICAgICAgICAgICAgIHxfX18vCg=='
    print  base64.b64decode(banner)
    print ''

def printzpc():
    banner = 'LS0tLS0tICAgfC0tLS0tLSAgICAgIC0tLS0tLQogICAgLyAgICB8ICAgICAgXCAgICAvCiAgIC8gICAgIHwgICAgICAv\
              ICAgLwogIC8gICAgICB8LS0tLS0tICAgIFwKIC8gICAgICAgfCAgICAgICAgICAgXAotLS0tLS0gICB8ICAgICAgICAgICAgLS0tLS0tCg=='
    print base64.b64decode(banner)

def getverson():
    server_message = Hard_collect.SYSTEM().system()
    print '操作系统检测-start-'
    print "主机名:"+server_message['Node']
    print '系统名称:'+server_message['Sys_Name']
    print '系统版本:'+server_message['Sys_verson']
    print '系统代号:'+server_message['Sys_code']
    print '系统位数:'+server_message['release']
    print '内核版本:'+server_message['machine']
    print '操作系统检测-end-'
    print ''


def getmemory():
    print '内存信息检测-start-'
    mem_message = Hard_collect.MEMORY().memory()
    for x in range(len(mem_message['Memory_Sn'])):
        print '内存SN号'+mem_message['Memory_Sn'][x]+"  "+"内存容量"+mem_message['Memory_Size'][x]+"  "+"内存种类"+mem_message['Memory_Type'][x] 
    print '内存信息检测-end-'
    print ''

def getserver():
    print '服务器信息检测-start-'
    server_message = Hard_collect.SERVER().server()
    print "服务器SN号:"+server_message['Server_Sn']
    print "服务器品牌:"+server_message['Server_Type']
    print "服务器型号:"+server_message['Server_Product']
    print '服务器信息检测-end-'
    print ''


def getnetwork():
    print '网卡信息检测-start-'
    net_message = Hard_collect.NETWORK().network()
    for x in range(len(net_message['Network_Name'])):
        print '网卡名:'+net_message['Network_Name'][x]+'   '+'网卡MAC地址:'+net_message['Network_Mac'][x]+'   '+'网卡ip:'+net_message['Network_Ip'][x]
    print '网卡信息检测-end-'
    print ''


def getcpu():
    cpu_message = Hard_collect.CPU().cpu()
    print 'CPU信息检测-start-'
    print 'CPU型号：'+cpu_message['Cpu_Name']+'\n'+'CPU物理数量：'+str(cpu_message['Physical_Number'])+'\n'+'CPU总核数：'+str(cpu_message['Cpu_Processor'])+'\n'\
           +'CPU频率'+cpu_message['Cpu_Rart']+'\n'+'CPU位数：'+ str(cpu_message['Cpu_Size'])
    print 'CPU信息检测-end-'
    print ''

def getcontrolIP():
    print '管理卡IP检测-start-'
    ip_message = Hard_collect.IP().ip()
    for x in ip_message['Outer_Ip']:
        if x :
            print '外网IP:'+x
    for x in ip_message['Intranet_Ip']:
        if x :
            print '内网IP:'+x
    print '管理卡IP:'+ip_message['Management_Ip']
    print '管理卡IP检测-end-'
    print ''


def main():
    printifeng()  
    time_start=time.time() 
    getmemory()
    getserver() 
    getcpu()
    getverson()
    getnetwork()
    getcontrolIP()
    disk_sn_collect.printall()
    print '总耗时'+str(time.time()-time_start)

if __name__ == '__main__':    
    main()
