from builtins import super, int
import paramiko
import threading


class MyThreadCfgZabbixAgent(threading.Thread):
    def __init__(self, cur_num, total_num, ssh_ip, port, pwd, zabbix_server_ip):
        super(MyThreadCfgZabbixAgent, self).__init__()
        self.cur_num = cur_num
        self.total_num = total_num
        self.ssh_ip = ssh_ip
        self.port = int(port)
        self.username = "root"
        self.pwd = pwd
        self.zabbix_server_ip = zabbix_server_ip
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.cmd = """
        rpm -ivhU /tmp/rpm/zabbix-agent*
        sed -i "/^Server=127.0.0.1/s/Server=127.0.0.1/Server=%s/" /etc/zabbix/zabbix_agentd.conf
        sed -i "/^ServerActive=127.0.0.1/s/ServerActive=127.0.0.1/ServerActive=%s/" /etc/zabbix/zabbix_agentd.conf
        sed -i "/^Hostname=Zabbix server/s/Hostname=Zabbix server/Hostname=%s/" /etc/zabbix/zabbix_agentd.conf
        """ % (zabbix_server_ip, zabbix_server_ip, ssh_ip)

    def run(self):
        try:
            self.ssh.connect(hostname=self.ssh_ip, port=self.port, username=self.username, password=self.pwd)
            stdin, stdout, stderr = self.ssh.exec_command(self.cmd)
            res, err = stdout.read(), stderr.read()
            result = res if res else err
            self.ssh.close()
            print("""%s/%s: %s zabbix-agent ok""" % (self.cur_num, self.total_num, self.ssh_ip))
        except Exception as e:
            print("""%s/%s: %s""" % (self.cur_num, self.total_num, e))
