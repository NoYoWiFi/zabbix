from builtins import super, int
import paramiko
import threading


class MyThreadCfgOneEth(threading.Thread):
    def __init__(self, cur_num, total_num, ssh_ip, port, pwd, link_eth, ip, netmask, gateway, dns1, dns2):
        super(MyThreadCfgOneEth, self).__init__()
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
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.cmd = """
        localremoteEth=%s
        localip=%s
        localnetmask=%s
        localnetgateway=%s
        localdns1=%s
        localdns2=%s
        myifcfg=/etc/sysconfig/network-scripts
        myhwaddr=$(ethtool -P $localremoteEth |awk \'{print $3}\')
        rm -rf $myifcfg/ifcfg-$localremoteEth
        touch $myifcfg/ifcfg-$localremoteEth
        echo \"DEVICE=$localremoteEth\" >> $myifcfg/ifcfg-$localremoteEth
        echo \"HWADDR=$myhwaddr\" >> $myifcfg/ifcfg-$localremoteEth
        echo \"TYPE=Ethernet\" >> $myifcfg/ifcfg-$localremoteEth
        echo \"ONBOOT=yes\" >> $myifcfg/ifcfg-$localremoteEth
        echo \"BOOTPROTO=none\" >> $myifcfg/ifcfg-$localremoteEth
        echo \"IPADDR=$localip\" >> $myifcfg/ifcfg-$localremoteEth
        echo \"NETMASK=$localnetmask\" >> $myifcfg/ifcfg-$localremoteEth
        echo \"GATEWAY=$localnetgateway\" >> $myifcfg/ifcfg-$localremoteEth
        echo \"DNS1=\"$localdns1\"\" >> $myifcfg/ifcfg-$localremoteEth
        echo \"DNS2=\"$localdns2\"\" >> $myifcfg/ifcfg-$localremoteEth
        ifdown %s && ifup %s
        """ % (self.link_eth, self.ip, self.netmask, self.gateway,
               self.dns1, self.dns2, self.link_eth, self.link_eth)

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
