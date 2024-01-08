from builtins import super, int
import paramiko
import threading
import time


class MyThreadCfgSwitch(threading.Thread):
    def __init__(self, cur_num, total_num, ssh_ip, username, pwd,
                 port, main_port, standby_port, vlan_id):
        super(MyThreadCfgSwitch, self).__init__()
        self.cur_num = cur_num
        self.total_num = total_num
        self.ssh_ip = ssh_ip
        self.username = username
        self.pwd = pwd
        self.port = port
        self.main_port = main_port
        self.standby_port = standby_port
        self.vlan_id = int(vlan_id)
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.cmd_vlan1 = """
        system-view
        int %s
        port link-type access
        undo port access vlan
        shutdown
        int %s
        port link-type access
        undo port access vlan
        shutdown
        """ % (self.main_port, self.standby_port)
        self.cmd_vlan = """
        system-view
        int %s
        port link-type access
        port access vlan %s
        undo shutdown
        int %s
        port link-type access
        port access vlan %s
        undo shutdown
        """ % (self.main_port, self.vlan_id, self.standby_port, self.vlan_id)

    def run(self):
        try:
            self.ssh.connect(hostname=self.ssh_ip, port=self.port, username=self.username, password=self.pwd, timeout=3)
            ssh_shell = self.ssh.invoke_shell()
            if int(self.vlan_id) == 1:
                ssh_shell.send(self.cmd_vlan1)
                time.sleep(float(1))
            else:
                ssh_shell.send(self.cmd_vlan)
                time.sleep(float(1))
            try:
                #print(ssh_shell.recv(1024))
                # print(self.cmd_vlan)
                # print(self.cur_num, self.total_num, self.ssh_ip, self.username, self.pwd,
                #       self.port, self.main_port, self.standby_port, self.vlan_id)
                print("""%s/%s: ok""" % (self.cur_num, self.total_num))
            except Exception as e:
                print("""%s/%s: %s""" % (self.cur_num, self.total_num, e))
        except Exception as e:
            print("""%s/%s: %s""" % (self.cur_num, self.total_num, e))
            self.ssh.close()
