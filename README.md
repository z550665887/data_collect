# data_collect

采集服务器信息脚本 ，包括服务器，CPU，内存，硬盘，网卡，管理卡IP，Raid类型。

将Linux系统信息采集的底层命令实现封装成包 Hard_collect.py，将硬盘信息采集的底层命令实现封装成包disk_sn_collect.py

###############disk_sn_collect操作方法如下所示

#>>> import disk_sn_collect

#>>> disk_sn_collect.returnall()     ###SN号是经过型号和Megacli匹配后的得到的可能值。。。匹配不到返回UNKNOWN

#{'MediaType': ['Hard Disk Device', 'Hard Disk Device', 'Hard Disk Device', 'Hard Disk Device'], 'Raid_Size': [' 1.635 TB'], 'Type': ['SEAGATE', 'SEAGATE', 'SEAGATE', 'SEAGATE'], 'Life': [], 'Raid_Name': [' LSI MegaRAID ROMB'], 'NAME': [' SEAGATE ST600MM0006 xxxxxxxxxxxx', ' SEAGATE ST600MM0006 xxxxxxxxxxxx', ' SEAGATE ST600MM0006 xxxxxxxxxxxx', ' SEAGATE ST600MM0006 xxxxxxxxxxxx'], 'Logic_capacity': '1675G', 'Raid_Level': [' Primary-5, Secondary-0,  Qualifier-3'], 'SN': ['xxxxxxxx', 'xxxxxxxx', 'xxxxxxxx', 'xxxxxxxx'], 'PDtype': ['SAS', 'SAS', 'SAS', 'SAS'], 'Size': ['558.406GB', '558.406GB', '558.406GB', '558.406GB']}

###############Hard_collect操作方法如下所示

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

############可以通过对应的输入对应的KEY获取值

#>>> print Hard_collect.MEMORY().memory_sn()

#['280740AA', '28081B1E', '28081AC4', '28081B7D']

#>>> print Hard_collect.CPU().cpu_name()

#32*Intel(R) Xeon(R) CPU E5-2620 v4 @ 2.10GHz
