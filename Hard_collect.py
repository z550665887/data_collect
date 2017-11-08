# -*- coding: utf-8 -*-
import os
import platform
import re
import base64
import sys
#######################################################操作方法如下所示
#>>> import Hard_collect
#>>> print Hard_collect.MEMORY().memory()
#{'Memory_Sn': ['280740AA', '28081B1E', '28081AC4', '28081B7D'], 'Memory_Size': ['16384MB', '16384MB', '16384MB', '16384MB'], 'Memory_Type': [' DDR4', ' DDR4', ' DDR4', ' DDR4']}
#>>> print Hard_collect.CPU().cpu()
#{'Cpu_rart': '32*2.10GHz', 'Cpu_Size': '64', 'Cpu_Name': '32*Intel(R) Xeon(R) CPU E5-2620 v4 @ 2.10GHz', 'Physical_Number': 2, 'Cpu_Processor': 32}
#>>> print Hard_collect.NETWORK().network()
#{'Network_Ip': ['10.90.13.101', '', '', ''], 'Network_Name': ['eth0', 'eth1', 'eth2', 'eth3'], 'Network_Mac': ['18:66:da:6e', '18:66:da:6e', 'a0:36:9f:80', 'a0:36:9f:80']}
#>>> print Hard_collect.SERVER().server()
#{'Server_Sn': 'FM5FVG2', 'Server_Product': 'DSS 1500', 'Server_Type': 'Dell Inc.'}
#>>> print Hard_collect.IP().ip()
#{'Management_Ip': '192.168.84.203', 'Intranet_Ip': ['10.90.13.101'], 'Outer_Ip': []}
################################################可以通过对应的输入对应的KEY获取值
#>>> print Hard_collect.MEMORY().memory_sn()
#['280740AA', '28081B1E', '28081AC4', '28081B7D']
#>>> print Hard_collect.CPU().cpu_name()
#32*Intel(R) Xeon(R) CPU E5-2620 v4 @ 2.10GHz



def printzpc():
    banner = 'LS0tLS0tICAgfC0tLS0tLSAgICAgIC0tLS0tLQogICAgLyAgICB8ICAgICAgXCAgICAvCiAgIC8gICAgIHwgICAgICAv\
              ICAgLwogIC8gICAgICB8LS0tLS0tICAgIFwKIC8gICAgICAgfCAgICAgICAgICAgXAotLS0tLS0gICB8ICAgICAgICAgICAgLS0tLS0tCg=='
    return base64.b64decode(banner)

# def check_virutal():            ##判断虚拟机
#     return 0 if 'Virtual' in os.popen('dmidecode -s system-product-name').readline() else 1

def check_virutal():    ##  python版本过低不支持三目运算符 if 'Virtual' in os.popen('dmidecode -s system-product-name').readline()
    if 'Virtual' in os.popen('/usr/sbin/dmidecode -s system-product-name').readline():
        return 0  
    else:
        return 1

class MEMORY:                 ##内存相关信息，包括SN,型号，大小
    Memory = {'Memory_Sn':[],'Memory_Size':[],'Memory_Type':[]}

    def memory(self):
        if not check_virutal():
            self.Memory['Memory_Size'] = os.popen("free -b|awk '/Mem:/{print $2/1024/1024\"MB\"}'").read()[:-1]
            return self.Memory
        Memory_mes = {'Memory_Sn':[],'Memory_Size':[],'Memory_Type':[]}
        Sn = os.popen("/usr/sbin/dmidecode |grep -A16 'Memory Device$' |grep -i 'serial'|awk '{print $3}'").readlines()
        Size = os.popen("/usr/sbin/dmidecode  |grep -A16 'Memory Device$' |grep -i 'size'|awk '{print $2$3}'").readlines()
        Type = os.popen("/usr/sbin/dmidecode  |grep -A16 'Memory Device$' |grep -i 'Type:'|awk -F ':' '{print $2}'").readlines()
        for x in range(len(Size)):
            if re.search(r'MB',Size[x],re.IGNORECASE):
                Memory_mes['Memory_Sn'].append(Sn[x][:-1])
                Memory_mes['Memory_Size'].append(Size[x][:-1])
                Memory_mes['Memory_Type'].append(Type[x][:-1])
            elif re.search(r'GB',Size[x],re.IGNORECASE):        ##针对内存为GB的时候
                Memory_mes['Memory_Sn'].append(Sn[x][:-1])
                Memory_mes['Memory_Size'].append(str(int(Size[x][:-1].replace('GB',''))*1024)+'MB')
                Memory_mes['Memory_Type'].append(Type[x][:-1])
        self.Memory = Memory_mes
        return self.Memory

    def memory_sn(self):
        return self.memory()['Memory_Sn']
    def memory_size(self):
        return self.memory()['Memory_Size']
    def memory_type(self):
        return self.memory()['Memory_Type']

class SYSTEM:             ##系统相关信息 包括主机名，系统名，系统版本，系统别称，内核版本，操作系统位数
    System = {'Node':'','Sys_Name':'','Sys_verson':'','Sys_code':'','release':'','machine':'',}

    def system(self):
        self.System['Node'] = platform.uname()[1]
        if sys.version >= "2.5":
            self.System['Sys_Name'] = platform.linux_distribution()[0].replace("#","")  ###某些系统的名字前面有#
            self.System['Sys_verson'] = platform.linux_distribution()[1]
            self.System['Sys_code'] = platform.linux_distribution()[2]
        else:
            self.System['Sys_Name'] = os.popen("lsb_release -a|grep 'Description'|awk '{print $2}'").read().strip().replace("#","")  ###某些系统的名字前面有#
            self.System['Sys_verson'] = os.popen("lsb_release -a|grep 'Description'|awk '{print $4}'").read().strip()
            self.System['Sys_code'] = os.popen("lsb_release -a|grep 'Description'|awk '{print $5}'").read().strip().replace("(","").replace(")","")
        self.System['release'] = platform.release()
        self.System['machine'] = platform.machine()
        return self.System

    def system_node(self):
        return self.system()['Node']
    def system_sys_name(self):
        return self.system()['Sys_Name']
    def system_sys_verson(self):
        return self.system()['Sys_verson']
    def system_sys_code(self):
        return self.system()['Sys_code']
    def system_release(self):
        return self.system()['release']
    def system_machine(self):
        return self.system()['machine']


class NETWORK:            ##网卡信息采集，包括网卡名称，IP和网卡的mac地址
    Network = {'Network_Name':[],'Network_Ip':[],'Network_Mac':[]}
    
    def network(self):
        net_name=[x[:-1] for x in os.popen("/sbin/ip address |awk '/^[0-9]+: (eth|em|bond|ens|eno)/{sub(\":\",\"\",$2);print $2;}'").readlines()]
        net_ip=[]
        net_mac=[]
        ext_name=[]
        ext_ip=[]
        ext_mac=[]
        for x in net_name:
            # ip =[y[:-1] for y in  os.popen("/sbin/ip address show %s| awk '/inet /{sub(\"/.*\",\"\",$2); print $2}'|sed 's/ /,/g' "%x).readlines() ]
            ip =[k[:-1] for k in os.popen("/sbin/ip address show %s| awk '/inet /{sub(\"/.*\",\"\",$2); print $2}'|sed 's/ /,/g' "%x).readlines()]
            mac = os.popen("/sbin/ip address show %s|awk '/link\/ether /{print $2}'"%x).read()[:-1]
            if mac:
                net_mac.append(mac)
            else:
                net_mac.append("")
            if len(ip):
                net_ip.append(ip[0])
            else:
                net_ip.append('')
            if len(ip) > 1:
                for y in range(1,len(ip)):
                    ext_name.append(x+'-'+str(y))
                    ext_ip.append(ip[y])
                    ext_mac.append(mac)
        if ext_name:
            for x in range(len(ext_name)):
                net_name.append(ext_name[x])
                net_ip.append(ext_ip[x])
                net_mac.append(ext_mac[x])

        self.Network['Network_Name'],self.Network['Network_Ip'],self.Network['Network_Mac'] = net_name,net_ip,net_mac
        return self.Network
    # def network(self):
    #     net_name=[x[:-1] for x in os.popen("/sbin/ifconfig -a|sed -n '/Link encap/p'|awk '{print $1}'|grep -v lo|grep -v 'docker'").readlines()]
    #     if not net_name:
    #         net_name=[x[:-1] for x in os.popen("/sbin/ifconfig -a|sed -n '/flags=/p'|awk -F: '{print $1}'|grep -v lo").readlines()]
    #     net_ip=[]
    #     net_mac=[]
    #     for x in net_name:
    #         ip = os.popen("/sbin/ifconfig -a %s|grep -i 'inet '"%x).read()
    #         ip = re.search(r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})',ip)
    #         if ip: 
    #             net_ip.append(ip.group())
    #         else:
    #             net_ip.append("")
    #         mac = os.popen("/sbin/ifconfig -a %s|egrep  'HWaddr|ether'"%x).read()[:-1]
    #         mac = re.search(r'(\w{1,2})\:(\w{1,2})\:(\w{1,2})\:(\w{1,2})\:(\w{1,2})\:(\w{1,2})',mac)
    #         if mac:
    #             net_mac.append(mac.group())
    #         else:
    #             net_mac.append("")
    #     self.Network['Network_Name'],self.Network['Network_Ip'],self.Network['Network_Mac'] = net_name,net_ip,net_mac
    #     return self.Network

    def network_name(self):
        return self.network()['Network_Name']
    def network_ip(self):
        return self.network()['Network_Ip']
    def network_mac(self):
        return self.network()['Network_Mac']

class CPU:            ##CPU信息采集，包括CPU的名称，CPU的总核数，CPU的物理核数，CPU的位数，和CPU的频率
    Cpu = {'Cpu_Name':'','Cpu_Processor':'','Physical_Number':'','Cpu_Size':'','Cpu_Rart':''}

    def cpu(self):
        # cpu_message = {'id':0,'processor':0,'name':'','size':'',}
        cpu_message = {'Cpu_Name':'','Cpu_Processor':0,'Physical_Number':0,'Cpu_Size':'','Cpu_Rart':''}
        f = open('/proc/cpuinfo')
        # with open('/proc/cpuinfo') as f:
        for line in f:
            if 'physical id' in line:
                cpu_message['Physical_Number'] = max(int(line.split(':')[1].strip())+1,cpu_message['Physical_Number'])
                line = line.split(':')[1].strip()
            elif 'processor' in line:
                cpu_message['Cpu_Processor'] = max(int(line.split(':')[1].strip())+1,cpu_message['Cpu_Processor']) 
            elif 'model name' in line:
                cpu_message['Cpu_Name'] = line.split(':')[1].strip()
            elif 'clflush size' in line:
                cpu_message['Cpu_Size'] = line.split(':')[1].strip()
        f.close()
        cpu_message['Cpu_Name'] = str(cpu_message['Cpu_Processor'])+'*'+cpu_message['Cpu_Name']
        if os.popen('cat /proc/cpuinfo|grep -c "GHz" ').read():
            cpu_message['Cpu_Rart'] = str(cpu_message['Cpu_Processor'])+'*'+cpu_message['Cpu_Name'].split('@')[1].strip()
        # else:
        #     rart = int(os.popen("cat /proc/cpuinfo |grep -i 'MHz'|awk -F: '{print $2}'").readlines()[0].strip())
        #     cpu_message['Cpu_Rart'] = str(cpu_message['Cpu_Processor'])+'*'+str(rart/1000+1)+"GHz"
        self.Cpu = cpu_message
        return self.Cpu

    def cpu_name(self):
        return self.cpu()['Cpu_Name']
    def cpu_processor(self):
        return self.cpu()['Cpu_Processor']
    def physical_number(self):
        return self.cpu()['Physical_Number']
    def cpu_size(self):
        return self.cpu()['Cpu_Size']
    def cpu_rart(self):
        return self.cpu()['Cpu_Rart']

class SERVER:             ##服务器信息采集，包括服务器的SN号，服务器的型号和服务器的生产商。     致敬杨老师
    Server = {'Server_Sn':'','Server_Type':'','Server_Product':''}

    def server(self):
        server_message = {'Server_Sn':'','Server_Type':'','Server_Product':''}
        server_message['Server_Type'] = os.popen("/usr/sbin/dmidecode -s system-manufacturer 2>/dev/null|grep -v '^#' 2>/dev/null | sed 's/ *$//g'").readlines()[0][:-1].replace("Inc.","").strip()
        if server_message['Server_Type']:
            server_message['Server_Product'] = os.popen("/usr/sbin/dmidecode -s system-product-name |grep -v '^#' 2>/dev/null | sed 's/ *$//g'").readlines()[0][:-1]
            server_message['Server_Sn'] = os.popen("/usr/sbin/dmidecode -s system-serial-number|grep -v '^#' 2>/dev/null | sed 's/ *$//g'").readlines()[0][:-1]
        else:
            server_message['Server_Type'] = os.popen("/usr/sbin/dmidecode  | grep -A5 System\ Information | grep Manufacturer | awk -F: '{print $2}' | sed 's/^ //' | awk '{print $1}' 2>/dev/null | sed 's/ *$//g'").readlines()[0][:-1].replace("Inc.","").strip()
            server_message['Server_Product'] = os.popen("/usr/sbin/dmidecode | grep -A5 System\ Information | grep Product\ Name | awk -F: '{print $2}'| sed 's/^ //' 2>/dev/null | sed 's/ *$//g'").readlines()[0][:-1]
            server_message['Server_Sn'] = os.popen("/usr/sbin/dmidecode|grep -A0 'Serial Number'|head -1|awk -F: '{print $2}'|sed 's/^ //'|grep -v '^#' 2>/dev/null | sed 's/ *$//g'").readlines()[0][:-1]
        #服务器统一命名
        if server_message['Server_Sn'] =="(none)" and IP().intranet_ip() == "10.90.1.34":      ###10.90.1.34的sn号无法获取为(none) 写死。
            server_message['Server_Sn'] = "06FDLRB" 
        if server_message['Server_Type'] == "Huawei Technologies Co., Ltd.":
            server_message['Server_Type'] = "Huawei"
        elif server_message['Server_Type'] == "Dell" or server_message['Server_Type'] == "Dell Computer Corporation":
            server_message['Server_Type'] = "Dell"
        elif server_message['Server_Type'] == "Lenovo" or server_message['Server_Type'] == 'LENOVO':
            if 'System x3550 M5' in server_message['Server_Product']:
                m = server_message['Server_Product'].split(':')[0].split(' ')
                server_message['Server_Product'] = m[1]+' '+m[2]
            server_message['Server_Type'] = "Lenovo"
        elif server_message['Server_Type'] == "IBM":
            server_message['Server_Type'] = "IBM"
            if 'system' in server_message['Server_Product'] or 'System' in server_message['Server_Product']:    ###别问我为什么
                m = server_message['Server_Product'].replace('IBM','').split(':')[0].strip().split(' ')       
                if 'M4' in server_message['Server_Product']:            ###针对M4 和M5机型 统一命名
                    server_message['Server_Product'] = m[1]+' '+m[2]
                elif 'M5' in server_message['Server_Product']:
                    server_message['Server_Type'] = 'LENOVO'            ###针对IBM M5机型，由于被联想收购 同意品牌联想
                    server_message['Server_Product'] = m[1]+' '+m[2]
            elif 'xSeries' in server_message['Server_Product']:
                m = server_message['Server_Product'].split(':')[0].split(' ')
                server_message['Server_Product'] = m[5]+' '+m[6]
        if server_message['Server_Product'] == "DSS1500":   ###为了统一DSS1500 和DSS 1500
            server_message['Server_Product'] = "DSS 1500"
        if server_message['Server_Product'] == "ThinkServer ThinkServer RD550": ###为了去掉ThinkServer
            server_message['Server_Product'] = "ThinkServer RD550"
        #虚拟机统一命名
        if re.search(r'VMware',server_message['Server_Product'],re.IGNORECASE): 
            server_message['Server_Product'] = 'VMware'
        elif re.search(r'Red Hat KVM',server_message['Server_Product'],re.IGNORECASE):
            server_message['Server_Product'] = 'Red Hat KVM'
        #机身码统一名称
        if re.search(r'VMware',server_message['Server_Sn'],re.IGNORECASE):
            server_message['Server_Sn']=server_message['Server_Sn'].replace(" ","")
        elif server_message['Server_Sn'] =='Not Specified' or server_message['Server_Sn'] =='empty'\
            or server_message['Server_Sn'] =='N/A' or server_message['Server_Sn'] =='System Serial Number'\
            or server_message['Server_Sn'] =='............' or server_message['Server_Sn'] == '0123456789'\
            or server_message['Server_Sn'] =='To Be Filled By O.E.M.' or  not server_message['Server_Sn']:
            # server_message['Server_Sn'] = os.popen("echo %s|sha1sum|cut -c1-20"%NETWORK().network_mac()[0]).read()[:-1]
            pass
        elif server_message['Server_Product'] =='C6100':
            pass

        self.Server = server_message
        return self.Server

    def server_sn(self):
        return self.server()['Server_Sn']
    def server_product(self):
        return self.server()['Server_Product']
    def server_type(self):
        return self.server()['Server_Type']


class IP:             ##IP信息采集，包括内网IP，外网IP，管理卡IP

    Ip = {'Outer_Ip':'','Intranet_Ip':'','Management_Ip':''}

    def ip(self):
        ip_message = {'Outer_Ip':'','Intranet_Ip':'','Management_Ip':''}
        iptools = NETWORK().network_ip()
        if check_virutal():
            management_IP= os.popen("timeout 5 ipmitool lan print|grep -i 'IP Address'|grep -v 'Source'|awk -F ':' '{print $2}' ").read().strip()
            if management_IP and management_IP != "0.0.0.0":
                ip_message['Management_Ip']=management_IP  
            else:
                ip_message['Management_Ip'] = ""

        for i in iptools:
            if re.match(r'^10\.',i) or re.match(r'^192\.',i) or re.match(r'^172\.',i):
                if ip_message['Intranet_Ip'] == '':
                    ip_message['Intranet_Ip'] = i
                else:
                    ip_message['Intranet_Ip']=ip_message['Intranet_Ip']+','+i
            elif i:
                ip_message['Outer_Ip']=i
        self.Ip = ip_message
        return self.Ip

    def outer_ip(self):
        return self.ip()['Outer_Ip']
    def intranet_ip(self):
        return self.ip()['Intranet_Ip']
    def management_ip(self):
        return self.ip()['Management_Ip']


class FILESYSTEM:
    Filesystem = {'Name':[],'Type':[]}

    def filesystem(self):
        File_system = {'Name':[],'Type':[]}
        if not os.path.exists('/bin/lsblk'):
            os.system('yum install -y  util-linux')
        file =[re.sub(r"\s{2,}", " ", x[:-1]) for x in os.popen("lsblk -lf|awk '{print $1\" \"$2}'").readlines()]
        for x in file:
            if re.search(r'ext',x,re.IGNORECASE) or re.search(r'xfs',x,re.IGNORECASE):
                File_system['Name'].append(x.split(' ')[0])
                File_system['Type'].append(x.split(' ')[1])
        self.Filesystem = File_system
        return self.Filesystem

    def filesystem_name(self):
        return self.filesystem()['Name']
    def filesystem_type(self):
        return self.filesystem()['Type']
