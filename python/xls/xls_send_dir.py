import sys
sys.path.append("./python/")
import xlrd
import xls.var_file
from xlrd.timemachine import xrange
from ssh.sshSendDir import MyThreadSendDir


def xls_send_dir():
    workbook = xlrd.open_workbook(xls.var_file.xls_01)
    for n_1 in xrange(workbook.sheets()[0].nrows):
        if n_1 == 0:
            continue
        else:
            SN = workbook.sheets()[0].cell(n_1, 0).value
            if SN == '':
                break
            total_num = workbook.sheets()[0].nrows - 1
            cur_num = n_1
            ssh_ip = workbook.sheets()[0].cell(n_1, 1).value
            port = int(workbook.sheets()[0].cell(n_1, 2).value)
            pwd = workbook.sheets()[0].cell(n_1, 3).value
            bond_if = int(workbook.sheets()[0].cell(n_1, 4).value)
            eth_name = workbook.sheets()[0].cell(n_1, 5).value
            remote_eth = workbook.sheets()[0].cell(n_1, 6).value
            ip = workbook.sheets()[0].cell(n_1, 7).value
            netmask = workbook.sheets()[0].cell(n_1, 8).value
            gateway = workbook.sheets()[0].cell(n_1, 9).value
            dns1 = workbook.sheets()[0].cell(n_1, 10).value
            dns2 = workbook.sheets()[0].cell(n_1, 11).value
            bond_mode = workbook.sheets()[0].cell(n_1, 12).value
            if bond_mode == '':
                bond_mode = 0
            else:
                bond_mode = int(bond_mode)
            eth_bond1 = workbook.sheets()[0].cell(n_1, 13).value
            eth_bond2 = workbook.sheets()[0].cell(n_1, 14).value
            try:
                m = MyThreadSendDir(cur_num, total_num, ssh_ip, port, pwd)
                m.start()
                m.join()
            except Exception as e:
                print(u"line %s error, %s" % (n_1 + 1, e))
                sys.exit(1)


xls_send_dir()
