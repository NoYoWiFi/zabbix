from builtins import super, int
import paramiko
import threading


class MyThreadRestartNetwork(threading.Thread):
    def __init__(self, cur_num, total_num, ssh_ip, port, pwd):
        super(MyThreadRestartNetwork, self).__init__()
        self.cur_num = cur_num
        self.total_num = total_num
        self.ssh_ip = ssh_ip
        self.port = int(port)
        self.username = "root"
        self.pwd = pwd
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.cmd = """
		systemctl restart nework.service
        service network restart
        """

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
