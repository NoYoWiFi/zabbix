import sys
sys.path.append("./python/")
import xlwt
import pymysql
import xls.var_file

def len_byte(value):
    length = len(value)
    utf8_length = len(value.encode('utf-8'))
    length = (utf8_length - length) / 2 + length
    return int(length)


def xls_export_ip():
    db = pymysql.connect("127.0.0.1",
                         "root",
                         "",
                         xls.var_file.db_01,
                         )
    cursor = db.cursor()
    sql = """
    SELECT * FROM {0}
    """.format(xls.var_file.form_03)

    try:
        cursor.execute(sql)
        cursor.scroll(0, mode='absolute')
        results = cursor.fetchall()
        fields = cursor.description
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
        col_name = ["sn", "ssh_ip", "port", "pwd", "bond_if", "eth_name", "link_eth", "link_mac", "ip", "netmask",
                    "gateway", "dns1", "dns2", "bond_mode", "eth_bond1", "eth_bond2"]
        col_width = []
        for i in range(len(results)):
            for j in range(len(results[i])):
                if i == 0:
                    col_width.append(len_byte(col_name[j]))
                    #print(u"%s", col_width)
                if col_width[j] < len_byte(str(results[i][j])):
                    col_width[j] = len_byte(results[i][j])
        for i in range(len(col_width)):
            if col_width[i] > 1:
              sheet.col(i).width = 253 * (col_width[i] + 1)
              #print(u"%s" % sheet.col(i).width)
            if i == 2:
              sheet.col(i).width = 253 * 4
              #print(u"%s" % sheet.col(i).width)
            if i == 3:
              sheet.col(i).width = 253 * 8
              #print(u"%s" % sheet.col(i).width)
            if i == 4:
              sheet.col(i).width = 253 * 2
              #print(u"%s" % sheet.col(i).width)
            if i == 5:
              sheet.col(i).width = 253 * (col_width[i] + 1) * 4
              #print(u"%s" % sheet.col(i).width)
            if i == 7:
              sheet.col(i).width = 253 * (col_width[i] + 1) * 2
              #print(u"%s" % sheet.col(i).width)
        for col_num in range(0, len(col_name)):
            sheet.write(0, col_num, col_name[col_num])
            #print(u"%s" % col_name[col_num])
        row = 1
        col = 0
        for row in range(1, len(results) + 1):
            for col in range(0, 5):
                if col == 0:
                    sheet.write(row, 0, u'%s' % results[row - 1][col])
                    sheet.write(row, 2, u'22')
                    sheet.write(row, 3, u'123.com')
                    sheet.write(row, 4, u'0')
                    #print(u'%s' % results[row - 1][col])
                if col == 1:
                    sheet.write(row, 1, u'%s' % results[row - 1][col])
                    #print(u'%s' % results[row - 1][col])
                if col == 2:
                    sheet.write(row, 5, u'%s' % results[row - 1][col])
                    #print(u'%s' % results[row - 1][col])
                if col == 3:
                    sheet.write(row, 6, u'%s' % results[row - 1][col])
                    #print(u'%s' % results[row - 1][col])
                if col == 4:
                    sheet.write(row, 7, u'%s' % results[row - 1][col])
                    #print(u'%s' % results[row - 1][col])
                #else:
                    #sheet.write(row, col, u'%s' % results[row - 1][col])
                    #print(u'%s' % results[row - 1][col])
        workbook.save(xls.var_file.xls_01)
        print(u'export {0}'.format(xls.var_file.xls_01))
    except Exception as e:
        print(u"error, %s" % e)
    db.close()


xls_export_ip()
