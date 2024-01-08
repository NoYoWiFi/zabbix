from builtins import super, int
import paramiko
import threading


class MyThreadCfgBondEth(threading.Thread):
    def __init__(self, cur_num, total_num, ssh_ip, port, pwd, link_eth,
                 ip, netmask, gateway, dns1, dns2, bond_mode, eth_bond1, eth_bond2):
        super(MyThreadCfgBondEth, self).__init__()
        self.cur_num = cur_num
        self.total_num = total_num
        self.ssh_ip = ssh_ip
        self.port = int(port)
        self.username = "root"
        self.pwd = pwd
        self.link_eth = link_eth
        self.ip = ip
        self.netmask = netmask
        self.gateway = gateway
        self.dns1 = dns1
        self.dns2 = dns2
        self.bond_mode = bond_mode
        self.eth_bond1 = eth_bond1
        self.eth_bond2 = eth_bond2
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.cmd = """
        localremoteEth=%s
        localip=%s
        localnetmask=%s
        localnetgateway=%s
        localdns1=%s
        localdns2=%s
        localbondMode=%s
        localethbond1=%s
        localethbond2=%s
		ifcfg=/etc/sysconfig/network-scripts
		#bond0 cfg
		rm -rf $ifcfg/ifcfg-$localremoteEth
		touch $ifcfg/ifcfg-$localremoteEth
		echo "DEVICE=$localremoteEth" >> $ifcfg/ifcfg-$localremoteEth
		echo "TYPE=Ethernet" >> $ifcfg/ifcfg-$localremoteEth
		echo "ONBOOT=yes" >> $ifcfg/ifcfg-$localremoteEth
		echo "NM_CONTROLLED=no" >> $ifcfg/ifcfg-$localremoteEth
		echo "BOOTPROTO=none" >> $ifcfg/ifcfg-$localremoteEth
		echo "IPADDR=$localip" >> $ifcfg/ifcfg-$localremoteEth
		echo "NETMASK=$localnetmask" >> $ifcfg/ifcfg-$localremoteEth
		echo "GATEWAY=$localnetgateway" >> $ifcfg/ifcfg-$localremoteEth
		echo "DNS1=$localdns1" >> $ifcfg/ifcfg-$localremoteEth
		echo "DNS2=$localdns2" >> $ifcfg/ifcfg-$localremoteEth
		echo "BONDING_OPTS='mode=$localbondMode miimon=100'" >> $ifcfg/ifcfg-$localremoteEth
		#first ifcfg
		hwaddr1=$(ethtool -P $localethbond1 |awk \'{print $3}\')
		rm -rf $ifcfg/ifcfg-$localethbond1
		touch $ifcfg/ifcfg-$localethbond1
		echo "DEVICE=$localethbond1" >> $ifcfg/ifcfg-$localethbond1
		echo "HWADDR=$hwaddr1" >> $ifcfg/ifcfg-$localethbond1
		echo "TYPE=Ethernet" >> $ifcfg/ifcfg-$localethbond1
		echo "ONBOOT=yes" >> $ifcfg/ifcfg-$localethbond1
		echo "NM_CONTROLLED=no" >> $ifcfg/ifcfg-$localethbond1
		echo "BOOTPROTO=none" >> $ifcfg/ifcfg-$localethbond1
		echo "MASTER=$localremoteEth" >> $ifcfg/ifcfg-$localethbond1
		echo "SLAVE=yes" >> $ifcfg/ifcfg-$localethbond1
		#second ifcfg
		hwaddr2=$(ethtool -P $localethbond2 |awk \'{print $3}\')
		rm -rf $ifcfg/ifcfg-$localethbond2
		touch $ifcfg/ifcfg-$localethbond2
		echo "DEVICE=$localethbond2" >> $ifcfg/ifcfg-$localethbond2
		echo "HWADDR=$hwaddr2" >> $ifcfg/ifcfg-$localethbond2
		echo "TYPE=Ethernet" >> $ifcfg/ifcfg-$localethbond2
		echo "ONBOOT=yes" >> $ifcfg/ifcfg-$localethbond2
		echo "NM_CONTROLLED=no" >> $ifcfg/ifcfg-$localethbond2
		echo "BOOTPROTO=none" >> $ifcfg/ifcfg-$localethbond2
		echo "MASTER=$localremoteEth" >> $ifcfg/ifcfg-$localethbond2
		echo "SLAVE=yes" >> $ifcfg/ifcfg-$localethbond2
		chkconfig --level 2345 NetworkManager off
		service NetworkManager stop
		ifdown %s && ifup %s
        """ % (self.link_eth, self.ip, self.netmask, self.gateway, self.dns1, self.dns2,
               self.bond_mode, self.eth_bond1, self.eth_bond2, self.link_eth, self.link_eth)

    def run(self):
        try:
            self.ssh.connect(hostname=self.ssh_ip, port=self.port, username=self.username, password=self.pwd, timeout=3)
            stdin, stdout, stderr = self.ssh.exec_command(self.cmd, get_pty=True, timeout=3)
            try:
                res, err = stdout.readline(), stderr.readline()
                # result = res if res else err
                # print(result)
                print("""%s/%s: ok""" % (self.cur_num, self.total_num))
            except Exception as e:
                print("""%s/%s: ok""" % (self.cur_num, self.total_num))
        except Exception as e:
            print("""%s/%s: %s""" % (self.cur_num, self.total_num, e))
        self.ssh.close()
