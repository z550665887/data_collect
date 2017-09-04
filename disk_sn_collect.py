# -*- coding: utf-8 -*-
import os
import re
import time
from collections import deque

NAME =deque()
SN = deque()
Type = deque()
PDtype = deque()
Size = deque()
MediaType = deque()
Life = deque()
VM_Size = 0
Raid_Name = deque()
Raid_Size = deque()
Raid_Level = deque()

def getRaid():
    name = os.popen("/opt/MegaRAID/MegaCli/MegaCli -AdpAllInfo -aALL|grep -i 'Product Name'|awk -F ':' '{print $2}'").readlines()
    level = os.popen("/opt/MegaRAID/MegaCli/MegaCli -LDInfo -Lall -aALL|egrep 'RAID Level'|sed 's/RAID Level//g'|awk -F ':' '{print $2}'").readlines()
    size = os.popen("/opt/MegaRAID/MegaCli/MegaCli -LDInfo -Lall -aALL|egrep '^Size'|awk -F':' '{print $2}'").readlines()
    for x in range(len(name)):
        Raid_Name.append(name[x][:-1])
        Raid_Size.append(size[x][:-1])
        Raid_Level.append(getRaidLevel(level[x][:-1]))
        # Raid_Level.append(level[x][:-1])

def getRaidLevel(level):
    if 'Primary-1' in level and 'Secondary-3' in level and 'Qualifier-0' in level:
        return 'Raid 10'
    elif 'Primary-1' in level and 'Secondary-0' in level and 'Qualifier-0' in level:
        return 'Raid 1'
    elif 'Primary-0' in level and 'Secondary-0' in level and 'Qualifier-0' in level:
        return 'Raid 0'
    elif 'Primary-5' in level and 'Secondary-0' in level and 'Qualifier-3' in level:
        return 'Raid 5'
    else:
        return level


def getMediaType():
    data = os.popen("/opt/MegaRAID/MegaCli/MegaCli -pdlist -aall|grep -i 'Media Type'|awk -F ':' '{print $2}'").readlines()
    # if not data:
    #     data = os.popen("/opt/MegaRAID/MegaCli/MegaCli64 -pdlist -aall|grep -i 'Media Type'|awk -F ':' '{print $2}'").readlines()
    for i in data:
        MediaType.append(i.replace('\n','').strip())

def getSN():
    data = os.popen("/opt/MegaRAID/MegaCli/MegaCli -pdlist -aall|grep -i 'Inquiry Data'|awk -F ':' '{print $2}'").readlines()
    # if not data:
    #     data = os.popen("/opt/MegaRAID/MegaCli/MegaCli64 -pdlist -aall|grep -i 'Inquiry Data'|awk -F ':' '{print $2}'").readlines()
    for i in data:
        i=re.sub(r"\s{2,}", " ", i)
        if re.search(r'SEAGATE',i):              ##希捷测试OK 
            NAME.append(i[:-1])                  ##Inquiry Data: SEAGATE ST2000NM0023    GS09Z1X0LES0
            i=i.split(" ")
            SN.append(i[3][-8:])
            Type.append(i[1])
        elif re.search(r'(\W)(\w{8})ST(\w{4,})',i):     ##希捷测试OK 
            NAME.append(i[:-1])                   ##Inquiry Data:   ZC205QH1ST2000NM0055-1V4104    DA03
            i=i.split(" ")          
            SN.append(i[1][:8])
            if re.search(r'LENOVOL',i):             ###是联想品牌 
                Type.append("LENOVOL")              ##Inquiry Data:   ZC102G7SST4000NM0035 03X4440  LENOVOLJ83 
            else:
                Type.append("SEAGATE")
        elif re.search(r' ATA ',i) and re.search(r'ST(\w{10})',i):  ##希捷测试OK
            NAME.append(i[:-1])                          ##Inquiry Data: ATA  ST8000NM0055-1RMPA27 ZA1506NP
            i.split(" ")
            SN.append(i[3])
            Type.append("SEAGATE")
        elif re.search(r'(\W{1})TOSHIBA(\W{1})',i):        ##东芝测试OK 
            NAME.append(i[:-1])                  ##Inquiry Data: TOSHIBA MBF2300RC DA07EB03PBB0DM50 
            i=i.split(" ")
            SN.append(i[3][-12:])
            Type.append(i[1])
        elif re.search(r'(\W)(\w{12})TOSHIBA(\W)',i):     ##东芝测试OK 
            NAME.append(i[:-1])                  ##Inquiry Data: 76VHK1T6FVMCTOSHIBA MG04ACA200N FJ2D
            i=i.split(" ")
            SN.append(i[1][:12])
            Type.append(i[1][-6:])
        elif re.search(r'WD-',i):                       ##西数硬盘测试OK
            NAME.append(i[:-1])               ##Inquiry Data: ATA     WD1003FBYX-88   WB32     WD-WCAW34NCX95U
            if re.search(r'WD-(\w{12,})',i):     ##Inquiry Data:  WD-WMC1F0E2SFPWWDC WD4000FYYZ-88UL1B0  WD04
                SN.append(re.search(r'WD-(\w{12,})',i).group()[3:15])
                Type.append("Western Digital")      ##Inquiry Data: WD-WCAW36AS655NWD1003FBYX-88 LEN WB32
            else:
                SN.append("can't find SN")
                Type.append("Western Digital")
        elif re.search(r' WD ',i):                  ##西数硬盘测试OK
            NAME.append(i[:-1])                ##Inquiry Data: WD      WD2000FYYG      D1B3WMAWP0191532
            i=i.split(" ")
            SN.append(i[3][-12:])
            Type.append("Western Digital")
        elif re.search(r'(\W)LENOVO(\W)',i):            ##联想测试未知没有提供可靠的查询方式 
            NAME.append(i[:-1])              ##Inquiry Data: LENOVO-XST600MM0006     L56QS0M6CMMM0521B5C9
            i=i.split(" ")
            if re.match(r'(\w{4})(\w{8})\1{2,3}',i[2]): ##Inquiry Data: LENOVO-XAL13SEB600      TB3775S03QHCTB37TB37TB37
                SN.append(i[2][4:12])
            elif re.match(r'B56M(\w{8})0221B5C5',i[2]): ##Inquiry Data: LENOVO-XST600MM0006     L56QS0M5P78P0521B5C9
                SN.append(i[2][4:12])
            else:
                SN.append(i[2])
            Type.append(i[1])
        elif re.search(r'IBM',i):                       ##IBM测试未知没有提供可靠的查询方式
            NAME.append(i[:-1])                 ##Inquiry Data: IBM-ESXSWD6002BKTG-23E  ZC31E34SXD70ZC31ZC31ZC31
            i=i.split(" ")
            if re.match(r'(\w{4})(\w{8})\1{2,3}',i[2]): ##Inquiry Data: IBM-ESXSWD6002BKTG-23E  ZC31E34SXD70ZC31ZC31ZC31
                SN.append(i[2][4:12])
            elif re.match(r'B56M(\w{8})0221B5C5',i[2]): ##Inquiry Data: IBM-ESXSST600MM0006     B56MZ0M049SF0221B5C5
                SN.append(i[2][4:12])
            else:
                SN.append(i[2])
            Type.append(i[1])
        elif re.search(r'(\W)SAMSUNG(\W)',i):           ###SAMSUNG测试未知没有提供可靠的查询方式
            NAME.append(i[:-1])             ##Inquiry Data: S2UJNX0HC04768 SAMSUNG MZ7LM480HMHQ-00005   GXT5104Q
            i=i.split(" ")             ##Inquiry Data: S2NSNXAGB00259M SAMSUNG MZ7LM1T9HCJM-0E003   GXT3003Q
            SN.append(i[1])
            Type.append(i[2])
        elif re.search(r'(\W)HGST(\W)',i):              ###HGST测试未知没有提供可靠的查询方式
            NAME.append(i[:-1])                ##Inquiry Data: N8GVBZMY  HGST HUS726040ALE610   APBDT7JN
            i=i.split(" ")
            SN.append(i[1])
            Type.append(i[2])
        elif re.search(r'(\w{8})SD(\w{6})(\W)(\w{4})(\W)(\w{4})',i):    ###闪迪测试未知没有提供可靠的查询方式
            NAME.append(i[:-1])                          ##Inquiry Data:    A013D02ASDLF1DAR-960G-1HA1  ZR07RP91
            i=i.split(" ")
            SN.append(i[1][:8])
            Type.append("SanDisk")
        elif re.search('UGB88RRA',i):           ##Unigen测试未知没有提供可靠的查询方式 该品牌官网都找不到。。。
            NAME.append(i[:-1])              ##Inquiry Data: 0112210001100000200 UGB88RRA512HM3-000-00  5.0.2 
            i=i.split(" ")
            SN.append(i[1])
            Type.append("Unigen")
        elif re.search(r' HITACHI ',i):         ##HITACHI测试未知没有提供可靠的查询方式 据说日立在14年被西数收购了。。。
            NAME.append(i[:-1])              ##Inquiry Data: HITACHI HUS156030VLS600 E516JTYATJDM
            i=i.split(" ")
            SN.append(i[3])
            Type.append("HITACHI")
        elif re.search(r' STEC ',i):            ##STEC测试未知没有提供可靠的查询方式 翻墙都找不到官网
            NAME.append(i[:-1])              ##Inquiry Data: STEC    Z16IZF2E-2TBUCZ C23FSTM0001A46D3  
            i=i.split(" ")              ##Inquiry Data: STEC    S846E2000M2     E4Z1STM0001A7AA5  
            SN.append(i[3])
            Type.append("STEC")
        else:
            NAME.append(i[:-1])
            SN.append('nosn')
            Type.append('notype')

def getPDtype():
    data = os.popen("/opt/MegaRAID/MegaCli/MegaCli -pdlist -aall|grep -i 'pd type'|awk -F':' '{print $2}'").readlines()
    # if not data:
    #     data = os.popen("/opt/MegaRAID/MegaCli/MegaCli64 -pdlist -aall|grep -i 'pd type'|awk -F':' '{print $2}'").readlines()
    for i in data:
        PDtype.append(i.replace('\n','').strip())

def getSize():
    data = os.popen("/opt/MegaRAID/MegaCli/MegaCli -pdlist -aall|grep -i 'Coerced Size:'|awk '{print $3$4}'").readlines()
    # if not data:
    #     data = os.popen("/opt/MegaRAID/MegaCli/MegaCli64 -pdlist -aall|grep -i 'Coerced Size:'|awk '{print $3$4}'").readlines()
    for i in data:
        if 'Size' not in i:
            Size.append(i.replace('\n','').strip())

def getLife():
    data = os.popen("/opt/MegaRAID/MegaCli/MegaCli -pdlist -aall|grep 'Device Id'|awk -F ':' '{print $2}'").readlines()
    # if not data:
    #     data = os.popen("/opt/MegaRAID/MegaCli/MegaCli64 -pdlist -aall|grep 'Device Id'|awk -F ':' '{print $2}'").readlines()
    device_Id = [x[:-1].strip() for x in data]
    for i in device_Id:
        life = os.popen("smartctl -a -d megaraid,%s -i /dev/sda|egrep -i 'number of hours powered up|Power_On_Hours'"%i).read()[-9:-1].strip()
        Life.append(life) if life else Life.append('no data')

def check_virutal():
    return 0 if 'Virtual' in os.popen('dmidecode -s system-product-name').readline() else 1

def getvirutaldate():
    data = os.popen("fdisk -l |grep -i 'Disk /dev/sd'|awk -F ':' '{print $2}'|awk -F ',' '{print $1}'").readlines()
    datas = 0
    for x in data:
        datas= int(x[:-1].strip().split(".")[0]) + datas
    VM_Size = datas
    # print "虚拟机硬盘大小:" + str(VM_Size)+data[0].strip().split(" ")[1]
    return str(VM_Size)+data[0].strip().split(" ")[1]

def printall():
    time_start=time.time()
    if check_virutal():
        if os.path.exists("/opt/MegaRAID/MegaCli/MegaCli64"):
            os.system("cp -rf /opt/MegaRAID/MegaCli/MegaCli64 /opt/MegaRAID/MegaCli/MegaCli")
            os.system("mv /opt/MegaRAID/MegaCli/MegaCli64 /opt/MegaRAID/MegaCli/MegaCli64.bak")
        getMediaType()
        getSN()
        getPDtype()
        getSize()
        getRaid()
        # getLife()
        print NAME,SN,Type,PDtype,Size,MediaType,Life,Raid_Name,Raid_Size,Raid_Level
    else:
        print "虚拟机硬盘大小:" + getvirutaldate()

def returnall():
    time_start=time.time()
    if check_virutal():
        if os.path.exists("/opt/MegaRAID/MegaCli/MegaCli64"):
            os.system("cp -rf /opt/MegaRAID/MegaCli/MegaCli64 /opt/MegaRAID/MegaCli/MegaCli")
            os.system("mv /opt/MegaRAID/MegaCli/MegaCli64 /opt/MegaRAID/MegaCli/MegaCli64.bak")
        getMediaType()
        getSN()
        getPDtype()
        getSize()
        getRaid()
        # getLife()
        return NAME,SN,Type,PDtype,Size,MediaType,Life,Raid_Name,Raid_Size,Raid_Level
    else:
        return getvirutaldate()