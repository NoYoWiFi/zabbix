import sys
sys.path.append("./python/")
import xlrd
import xls.var_file
from xlrd.timemachine import xrange
from ssh.sshCfgOneEth import MyThreadCfgOneEth
from ssh.sshCfgBondEth import MyThreadCfgBondEth


def xls_cfg_network():
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
            link_eth = workbook.sheets()[0].cell(n_1, 6).value
            ip = workbook.sheets()[0].cell(n_1, 8).value
            netmask = workbook.sheets()[0].cell(n_1, 9).value
            gateway = workbook.sheets()[0].cell(n_1, 10).value
            dns1 = workbook.sheets()[0].cell(n_1, 11).value
            dns2 = workbook.sheets()[0].cell(n_1, 12).value
            bond_mode = workbook.sheets()[0].cell(n_1, 13).value
            if bond_mode == '':
                bond_mode = 0
            else:
                bond_mode = int(bond_mode)
            eth_bond1 = workbook.sheets()[0].cell(n_1, 14).value
            eth_bond2 = workbook.sheets()[0].cell(n_1, 15).value
            if bond_if == 0:
                try:
                    m = MyThreadCfgOneEth(cur_num, total_num, ssh_ip, port, pwd, link_eth, ip, netmask, gateway, dns1,
                                          dns2)
                    m.start()
                    m.join()
                except Exception as e:
                    print("line %s error, %s" % (n_1 + 1, e))
                    sys.exit(1)
            if bond_if == 1:
                try:
                    m = MyThreadCfgBondEth(cur_num, total_num, ssh_ip, port, pwd, link_eth, ip, netmask, gateway,
                                           dns1, dns2,
                                           bond_mode, eth_bond1, eth_bond2)
                    m.start()
                    m.join()
                except Exception as e:
                    print("line %s error, %s" % (n_1 + 1, e))
                    sys.exit(1)


xls_cfg_network()
