import sys
sys.path.append("./python/")
import xlrd
import xls.var_file
from xlrd.timemachine import xrange
from ssh.sshCfgHostName import MyThreadCfgHostName


def xls_cfg_hostName():
    workbook = xlrd.open_workbook(xls.var_file.xls_02)
    for n_1 in xrange(workbook.sheets()[0].nrows):
        if n_1 == 0:
            continue
        else:
            ssh_ip = workbook.sheets()[0].cell(n_1, 0).value
            if ssh_ip == '':
                break
            total_num = workbook.sheets()[0].nrows - 1
            cur_num = n_1
            port = int(workbook.sheets()[0].cell(n_1, 1).value)
            pwd = workbook.sheets()[0].cell(n_1, 2).value
            hostName = workbook.sheets()[0].cell(n_1, 3).value
            try:
                m = MyThreadCfgHostName(cur_num, total_num, ssh_ip, port, pwd, hostName)
                m.start()
                m.join()
            except Exception as e:
                print("line %s error, %s" % (n_1 + 1, e))
                sys.exit(1)

xls_cfg_hostName()
