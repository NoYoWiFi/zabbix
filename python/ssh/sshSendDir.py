import sys
sys.path.append("./python/")
import paramiko
import threading
import time
import os
import ssh.var_file

class MyThreadSendDir(threading.Thread):
    def __init__(self, cur_num, total_num, ssh_ip, port, pwd):
        super(MyThreadSendDir, self).__init__()
        self.cur_num = cur_num
        self.total_num = total_num
        self.ssh_ip = ssh_ip
        self.port = int(port)
        self.username = "root"
        if pwd.isdigit():
            self.pwd = int(pwd)
        else:
            self.pwd = pwd
        self.transport = paramiko.Transport(sock=(self.ssh_ip, self.port))
        self.transport.connect(username=self.username, password=self.pwd)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def run(self):
        def create_remote_dir(dir):
            for item in dir:
                try:
                    self.sftp.stat(item)
                    pass
                except FileNotFoundError:
                    print("Create a new directory: ", item)
                    self.sftp.mkdir(item)

        def for_dir():
            for res in path:
                if os.path.isdir(res):
                    local_dir_path.append(res)
            remote_dir_path.append(des)

        def for_zdir():
            des_src_dir.append(remote_dir_path[1])
            des_src_dir_list = des_src_dir[0].split("/")
            des_dir_list = des_src_dir_list[1:]
            c = ""
            remote_des_src_path = []
            for item in des_dir_list:
                c += "/" + item
                remote_des_src_path.append(c)
            create_remote_dir(remote_des_src_path)
            create_remote_dir(remote_dir_path)
            for res in path:
                if os.path.isfile(res):
                    local_file_path.append(res)

        src = ssh.var_file.path_01
        des = ssh.var_file.path_02
        sep = "/"
        path = []
        local_dir_path = []
        local_file_path = []
        remote_dir_path = []
        remote_file_path = []
        des_src_dir = []
        for i in os.listdir(src):
            path.append(src + sep + i)
        for n in path:
            if os.path.isdir(n) and os.listdir(n):
                for i in os.listdir(n):
                    path.append(n + sep + i)
        local_dir_path.append(src)
        local_dir = src.split("/")
        local_dir_first = local_dir[0:-1]
        global a
        if len(local_dir_first) == 0:
            for_dir()
            for res in local_dir_path:
                remote_dir_path.append(des + "/" + res)
            for_zdir()
            for res in local_file_path:
                remote_file_path.append(des + "/" + res)
        else:
            if len(local_dir_first) == 1:
                dir_join = "/".join(local_dir_first)
                a = dir_join
            else:
                dir_join = "/".join(local_dir_first)
                a = dir_join + "/"
            for res in path:
                if os.path.isdir(res):
                    local_dir_path.append(res)
            remote_dir_path.append(des)
            b = [item.split(a)[-1] for item in local_dir_path]
            for res in b:
                if len(local_dir_first) == 1:
                    remote_dir_path.append(des + res)
                else:
                    remote_dir_path.append(des + "/" + res)
            for_zdir()
            d = [item.split(a)[-1] for item in local_file_path]
            for res in d:
                if len(local_dir_first) == 1:
                    remote_file_path.append(des + res)
                else:
                    remote_file_path.append(des + "/" + res)
        time_start = time.time()
        local_file_num = len(local_file_path)
        try:
            for i in range(local_file_num):
                self.sftp.put(local_file_path[i], remote_file_path[i])
            total_time = time.time() - time_start
            self.transport.close()
            print("""%s/%s: Send Successful, total time: %s""" % (self.cur_num, self.total_num, str(total_time)))
        except Exception as e:
            print("""%s/%s: %s""" % (self.cur_num, self.total_num, e))
