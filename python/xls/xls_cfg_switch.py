import sys
sys.path.append("./python/")
import pymysql
import xls.var_file
from ssh.sshCfgSwitch import MyThreadCfgSwitch


def db_count(db_name, form_name):
    db = pymysql.connect("127.0.0.1",
                         "root",
                         "",
                         db_name,
                         )
    cursor = db.cursor()
    sql = """
    select count(*) from {0}
    """.format(form_name)
    cursor.execute(sql)
    db.commit()
    results = cursor.fetchall()
    return results[0][0]


def xls_cfg_switch():
    db = pymysql.connect("127.0.0.1",
                         "root",
                         "",
                         xls.var_file.db_01,
                         )
    cursor_vlan = db.cursor()
    sql_vlan = """
    SELECT * FROM {0}
    """.format(xls.var_file.form_01)
    try:
        total_num = db_count(xls.var_file.db_01, xls.var_file.form_01)
        cursor_vlan.execute(sql_vlan)
        cursor_vlan.scroll(0, mode='absolute')
        results_vlan = cursor_vlan.fetchall()
        cur_num = 1
        for row_vlan in results_vlan:
            ssh_ip = row_vlan[1]
            port_num = int(row_vlan[2])
            vlan_id = int(row_vlan[3])
            try:
                cursor_connect = db.cursor()
                sql_connect = """
                            select * from {0} where IP='{1}'; 
                            """.format(xls.var_file.form_02, ssh_ip)
                # print(ssh_ip, port_num, vlan_num)
                # print(sql_connect)
                cursor_connect.execute(sql_connect)
                cursor_connect.scroll(0, mode='absolute')
                results_connect = cursor_connect.fetchall()
                for row_connect in results_connect:
                    username = row_connect[1]
                    pwd = row_connect[2]
                    port = row_connect[3]
                    main_port = row_connect[4] + str(port_num)
                    standby_port = row_connect[5] + str(port_num)
                    try:
                        m = MyThreadCfgSwitch(cur_num, total_num, ssh_ip, username, pwd,
                                              port, main_port, standby_port, vlan_id)
                        m.start()
                        m.join()
                        print(cur_num, total_num, ssh_ip, username, pwd,
                              port, main_port, standby_port, vlan_id)
                    except Exception as e:
                        print(u"line %s error, %s" % (cur_num, e))
                        sys.exit(1)
                    cur_num = cur_num + 1
            except Exception as e:
                print(u"error, %s" % e)
                sys.exit(1)
        db.close()
    except Exception as e:
        print(u"error, %s" % e)
        sys.exit(1)


xls_cfg_switch()
