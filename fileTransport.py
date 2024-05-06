import argparse
import os
from multiprocessing import Process, Manager
import threading
import socket
import paramiko
import time
import sys
import openpyxl
import shutil

# THREADNUM = multiprocessing.cpu_count()
# THREADNUM = os.cpu_count()
THREADNUM = 5
MAX_PACKET_SIZE = 10 * 1024 * 1024
FILEFLAG = ''


class CusExcelOp(object):
    def __init__(self):
        """
        excel_op = ExcelOp(file='zabbix_api.xlsx', index=16)
        column_1_list = excel_op.def_get_col_value(1)
        del column_1_list[0]
        title_name = ['主机名']
        excel_op.def_create_sheet(excel_op.sheet_name)
        [excel_op.def_set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
        [excel_op.def_set_cell_value(i + 2, 1, column_1_list[i]) for i in range(len(column_1_list))]
        excel_op.def_save_create_xlsx(excel_op.sheet_name)
        """
        self.file = None
        self.wb_object = None
        self.sheet_name = None
        self.ws_object = None

        self.create_file = None
        self.create_ws_object = None
        self.create_wb_object = None

    def def_load_excel(self, file, index):
        if index == 0:
            print("index must at least 1")
            exit(1)
        self.file = file
        self.wb_object = openpyxl.load_workbook(self.file)
        sheet_name_list = self.wb_object.sheetnames
        self.sheet_name = sheet_name_list[index - 1]
        self.ws_object = self.wb_object[self.sheet_name]

    def def_creat_excel(self):
        self.create_wb_object = openpyxl.Workbook()

    def def_create_sheet(self, sheet_name):
        """
        创建sheet页

        :param sheet_name: sheet名称: '页面1'
        :return: None
        """
        self.create_ws_object = self.create_wb_object.create_sheet(sheet_name)

    def def_update_sheet_name(self, sheet_name):
        self.sheet_name = sheet_name
        try:
            self.ws_object = self.wb_object[sheet_name]
        except Exception as e:
            print(u"数据异常当前Zabbix版本不支持汉化: %s" % e)
            exit(1)
        return None

    # 获取表格的总行数和总列数
    def def_get_row_clo_num(self):
        """
        :return: {"rows": rows, "columns": columns}
        """
        rows = self.ws_object.max_row
        columns = self.ws_object.max_column
        return {"rows": rows, "columns": columns}

    # 获取某个单元格的值
    def def_get_cell_value(self, row, column):
        """
        获取单元格的值

        :param row: 行号
        :param column: 列号
        :return: 返回字符串
        """
        cell_value = self.ws_object.cell(row=row, column=column).value
        return cell_value

    # 获取某列的所有值
    def def_get_col_value(self, column):
        """
        根据列号返回一列数据

        :param column: 列号: 3
        :return: 表格数据: ['a','b','c']
        """
        # rows = self.ws_object.max_row
        # cell_value = [self.ws_object.cell(row=i, column=column).value if self.ws_object.cell(row=i, column=column).value is not None else (
        #     print('第 %s 行错误! 原因: %s' % (i, u'错误! 列表存在空行')), exit(1)) for i in range(1, rows + 1)]
        v_dic_num = {"row": 1}
        v_flag = True
        v_list_row = []
        while v_flag:
            v_cell_value = self.ws_object.cell(row=v_dic_num['row'], column=column).value
            if v_cell_value is not None:
                v_list_row.append(v_cell_value)
                v_dic_num.update(row=v_dic_num['row'] + 1)
            else:
                v_flag = False
        return v_list_row

        # return cell_value

    def def_get_creat_col_value(self, column):
        """
        根据列号返回一列数据

        :param column: 列号: 3
        :return: 表格数据: ['a','b','c']
        """
        # rows = self.ws_object.max_row
        # cell_value = [self.ws_object.cell(row=i, column=column).value if self.ws_object.cell(row=i, column=column).value is not None else (
        #     print('第 %s 行错误! 原因: %s' % (i, u'错误! 列表存在空行')), exit(1)) for i in range(1, rows + 1)]
        v_dic_num = {"row": 1}
        v_flag = True
        v_list_row = []
        while v_flag:
            v_cell_value = self.create_ws_object.cell(row=v_dic_num['row'], column=column).value
            if v_cell_value is not None:
                v_list_row.append(v_cell_value)
                v_dic_num.update(row=v_dic_num['row'] + 1)
            else:
                v_flag = False
        return v_list_row

        # return cell_value

    def def_get_col_value_base_20221003(self, column):
        """
        根据列号返回一列数据

        :param column: 列号: 3
        :return: 表格数据: ['a','b','c']
        """
        rows = self.ws_object.max_row
        cell_value = [self.ws_object.cell(row=i, column=column).value for i in range(1, rows + 1) if self.ws_object.cell(row=i, column=column).value is not None]
        return cell_value

    # 获取某行所有值
    def def_get_row_value(self, row):
        """
        根据行号返回一行数据

        :param row: 行号: 1
        :return: 表格数据: ['a','b','c']
        """
        columns = self.ws_object.max_column
        row_data = []
        for __i01 in range(1, columns + 1):
            cell_value = self.ws_object.cell(row=row, column=__i01).value
            row_data.append(cell_value)
        return row_data

    def def_load_create_sheet(self, sheet_name):
        """
        加载sheet页

        :param sheet_name: sheet名称: '页面1'
        :return: None
        """
        self.create_wb_object = openpyxl.load_workbook(self.create_file)
        self.create_ws_object = self.create_wb_object[sheet_name]

    def def_save_create_xlsx(self, xlsx_name):
        """
        保存为:excel名称_时间戳.xlsx

        :param xlsx_name: excel名称: 表格1
        :return: None
        """
        del self.create_wb_object['Sheet']
        self.create_wb_object.save(xlsx_name)

    # 设置某个单元格的值
    def def_set_cell_value(self, row, colunm, cellvalue):
        """
        设置某个单元格的值

        :param row: 行号: 1
        :param colunm: 列号: 3
        :param cellvalue: 单元格值: '成功'
        :return: None
        """
        try:
            self.create_ws_object.cell(row=row, column=colunm).value = cellvalue
        except Exception as ee:
            self.create_ws_object.cell(row=row, column=colunm).value = u'{0}'.format(ee)


class CusFileTransPort(object):
    def __init__(self):
        """
        excel_op = ExcelOp(file='zabbix_api.xlsx', index=16)
        column_1_list = excel_op.def_get_col_value(1)
        del column_1_list[0]
        title_name = ['主机名']
        excel_op.def_create_sheet(excel_op.sheet_name)
        [excel_op.def_set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
        [excel_op.def_set_cell_value(i + 2, 1, column_1_list[i]) for i in range(len(column_1_list))]
        excel_op.def_save_create_xlsx(excel_op.sheet_name)
        """
        self.file = None
        self.wb_object = None
        self.sheet_name = None
        self.ws_object = None

        self.create_file = None
        self.create_ws_object = None
        self.create_wb_object = None

    def def_delete_os_files(self, _dic_01, _local_file_path):
        try:
            # sftpTransport.remove(_localdirpath)
            if os.path.exists(_local_file_path):
                os.remove(_local_file_path)
                print('删除', _dic_01['文件进度'])
            # os.remove(_localdirpath)
            # shutil.move(remote_tmp_file, )
        except Exception as __err:
            print('删除错误：', __err, ' ', '程序退出')
            exit(1)

    def def_delete_remote_files(self, _host, _sftpport, _sftpuser, _sftppwd, _dic_01, _remote_file_path):
        __sftpTransport = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
        try:
            # sftpTransport.remove(_localdirpath)
            if __sftpTransport.stat(_remote_file_path):
                __sftpTransport.remove(_remote_file_path)
                print('删除', _dic_01['文件进度'])
            # os.remove(_localdirpath)
            # shutil.move(remote_tmp_file, )
        except Exception as __err:
            print('删除错误：', __err, ' ', '程序退出')
            exit(1)

    def def_move_files_backup_thread(self, _dic_01, _local_file_path, _bak_file_path):
        try:
            if not os.path.exists(os.path.dirname(_bak_file_path)):
                os.makedirs(os.path.dirname(_bak_file_path))
        except Exception as __err_01:
            print('复制错误：', __err_01, ' ', '程序退出')
        finally:
            try:
                shutil.copyfile(_local_file_path, _bak_file_path)
                print('复制', _dic_01['文件进度'], _local_file_path, _bak_file_path)
            except Exception as __err_02:
                print('复制错误：', __err_02, ' ', '程序退出')

    def def_move_files_backup_process(self, _dic_01, _local_file_path, _bak_dir_path_list):
        try:
            # sftpTransport.remove(_localdirpath)
            __threadList = []
            for _int_01 in range(len(_bak_dir_path_list)):
                # 使用os.path.join()拼接目录和文件名
                _bak_file_path = os.path.join(next(iter(_bak_dir_path_list[_int_01])), os.path.basename(_local_file_path))
                # 使用os.path.abspath()获取绝对路径
                _bak_file_abspath = os.path.abspath(_bak_file_path)
                __t = threading.Thread(target=self.def_move_files_backup_thread, args=(_dic_01, _local_file_path, _bak_file_abspath))
                __t.start()
                __threadList.append(__t)
            for __pp in __threadList:
                __pp.join()
        except Exception as __err:
            print('移动错误：', __err, ' ', '程序退出')
            exit(1)

    # 从本地上传文件到ftp
    def def_get_os_file_list(self, _dir, _file_list, _file_lenth, _suffix):
        if os.path.isfile(_dir) and len(_file_list) < _file_lenth:
            if _dir.endswith(_suffix):
                _file_list.append(_dir)
        elif os.path.isdir(_dir):
            for __s in os.listdir(_dir):
                __newDir = os.path.join(_dir, __s)
                self.def_get_os_file_list(__newDir, _file_list, _file_lenth, _suffix)
        return _file_list

    def def_get_remote_sftp_file_list(self, _host, _sftpport, _sftpuser, _sftppwd, _remote_dir, _file_list, _max_length, _suffix):
        __sftpTransport = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
        try:
            # 遍历SFTP服务器上的目录
            for __entry in __sftpTransport.listdir_attr(_remote_dir):
                # 如果是目录，递归遍历
                if __entry.st_mode & 0o40000:  # 检查是否是目录
                    __subdir_path = os.path.join(_remote_dir, __entry.filename)
                    self.def_get_remote_sftp_file_list(_host, _sftpport, _sftpuser, _sftppwd, __subdir_path, _file_list, _max_length, _suffix)
                else:
                    __file_path = os.path.join(_remote_dir, __entry.filename).replace('\\', '/')
                    if __entry.filename.endswith(_suffix) and len(_file_list) < _max_length:
                        _file_list.append(__file_path)
        except FileNotFoundError:
            print(f"目录 {_remote_dir} 在SFTP服务器不存在.")
        except Exception as _err:
            print(f"发生了一个错误: {_err}")
        finally:
            # 关闭SFTP连接（通常在类的析构函数或关闭方法中）
            # 这里为了简单起见，我们不在每次调用后都关闭它
            pass
        return _file_list

    def def_sftp_trans_port_connect(self, _host, _sftpport, _sftpuser, _sftppwd):
        __timeout = 5
        __sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        __sock.settimeout(__timeout)
        __sock.connect((_host, _sftpport))
        __sftpClient = paramiko.Transport(__sock, default_max_packet_size=MAX_PACKET_SIZE, default_window_size=MAX_PACKET_SIZE)
        # sftpClient = paramiko.Transport(sock)
        __sftpClient.banner_timeout = __timeout
        # sftpClient.packetizer.REKEY_BYTES = pow(2, 40)
        # sftpClient.packetizer.REKEY_PACKETS = pow(2, 40)
        __sftpClient.connect(username=_sftpuser, password=_sftppwd)
        __sftpTransport = paramiko.SFTPClient.from_transport(__sftpClient, window_size=MAX_PACKET_SIZE, max_packet_size=MAX_PACKET_SIZE)
        __sftpTransport.default_max_packet_size = MAX_PACKET_SIZE
        __sftpTransport.default_window_size = MAX_PACKET_SIZE
        return __sftpTransport

    def def_sftp_download_chunk_thread(self, _dic_01, _host, _sftpport, _sftpuser, _sftppwd, _remote_file_path, _local_dir_path, _start, _end):
        # print(_host, _sftpport, _sftpuser, _sftppwd, _remotefilepath, _localdirpath, local_file, remote_base_path, start, end)
        __sftpTransport = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
        # 读取文件的一部分
        __local_tmp_file = os.path.join(_local_dir_path, os.path.basename(_remote_file_path))

        with __sftpTransport.open(_remote_file_path, 'rb') as __remotepath:
            __remotepath.seek(_start)
            __chunk_data = __remotepath.read(_end - _start)
            # 上传文件部分到SFTP服务器的临时文件
            try:
                with open(__local_tmp_file, 'rb+') as __local_file:
                    __local_file.seek(_start)
                    __local_file.write(__chunk_data)
                print('下载', _dic_01['目录进度']['目录进度'], _dic_01['文件进度'])
                __sftpTransport.close()
            except Exception as __err:
                print('下载线程错误：', __err)

    def def_sftp_upload_chunk_thread(self, __dic_01, _host, _sftpport, _sftpuser, _sftppwd, _remote_dir_path, _local_file_path, _start, _end):
        # print(_host, _sftpport, _sftpuser, _sftppwd, _remotefilepath, _localdirpath, local_file, remote_base_path, start, end)
        __sftpTransport = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
        # 读取文件的一部分
        __remote_tmp_file = os.path.join(os.path.dirname(_remote_dir_path), os.path.basename(_local_file_path)).replace('\\', '/')

        with open(_local_file_path, 'rb') as __local_file:

            __local_file.seek(_start)
            __chunk_data = __local_file.read(_end - _start)

            # 上传文件部分到SFTP服务器的临时文件
            try:
                with __sftpTransport.open(__remote_tmp_file, 'rb+') as __remote_file:
                    __remote_file.seek(_start)
                    __remote_file.write(__chunk_data)
                print('上传', __dic_01['目录进度']['目录进度'], __dic_01['文件进度'])
                __sftpTransport.close()
            except Exception as err:
                print('上传错误：', err)
                __sftpTransport.mkdir(_remote_dir_path)
                self.def_sftp_upload_chunk_thread(__dic_01, _host, _sftpport, _sftpuser, _sftppwd, _remote_dir_path, _local_file_path, _start, _end)

    def def_sftp_download_process(self, _dic_01, _host, _sftpport, _sftpuser, _sftppwd, _remote_file_path, _local_dir_path):
        try:
            __sftpTransport = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
            __sftp_file_size = __sftpTransport.stat(_remote_file_path).st_size
            __chunk_size = MAX_PACKET_SIZE  # 例如：每次上传1MB

            if not os.path.exists(_local_dir_path):
                if os.path.isdir(_local_dir_path):
                    os.mkdir(_local_dir_path)
                else:
                    os.mkdir(os.path.dirname(_local_dir_path))
            with open(os.path.join(_local_dir_path, os.path.basename(_remote_file_path)), "wb") as __open_local_file:
                __open_local_file.truncate(__sftp_file_size)
            print('临时 ', _dic_01['目录进度'], _remote_file_path, os.path.join(_local_dir_path, os.path.basename(_remote_file_path)))

            if __chunk_size > __sftp_file_size:
                __chunk_size = __sftp_file_size
            elif __sftp_file_size == 0:
                return
            __num_threads = int((__sftp_file_size + __chunk_size - 1) / __chunk_size)  # 至少一个线程，但不超过4个offsets
            __offsets = []
            with __sftpTransport.open(_remote_file_path, 'rb') as local_file:
                # 计算每个线程的起始和结束偏移量
                __offsets = [(__i * __chunk_size, min((__i + 1) * __chunk_size, __sftp_file_size)) for __i in range(__num_threads)]

                # 创建并启动线程
                __index = 0
                __dic_02 = {}
                for __i01, (__start01, __end01) in enumerate(__offsets):
                    __current_process2 = __i01 + 1
                    __total_length01 = len(__offsets)
                    __process_percentage2 = (__current_process2 / __total_length01) * 100
                    __local_tmp_file = os.path.join(_local_dir_path, os.path.basename(_remote_file_path))
                    __dic_02.update({'目录进度': _dic_01, '文件进度': __local_tmp_file + ' ' + f'{__total_length01}/{__current_process2} ({__process_percentage2:.2f}%)'})
                    # __dic_02, _host, _sftpport, _sftpuser, _sftppwd, _remotefilepath, _localdirpath, local_base_path, start, end
                    __t = threading.Thread(target=self.def_sftp_download_chunk_thread, args=(__dic_02, _host, _sftpport, _sftpuser, _sftppwd, _remote_file_path, _local_dir_path, __start01, __end01))
                    __t.start()
                    if __index == THREADNUM or len(__offsets) <= THREADNUM:
                        __t.join()
                        __index = 0
                    __index = __index + 1
            __sftpTransport.close()
            _dic_01['删除文件'].update({_remote_file_path: ''})
            _dic_01['备份文件'].update({_remote_file_path: ''})
            with open('./下载日志.log', 'a+', encoding='utf-8') as __del_file:
                __del_file.write(_dic_01 + '|' + _remote_file_path + '|' + f'{__total_length01}/{__current_process2} ({__process_percentage2:.2f}%)' + '\n')
        except Exception as __err:
            print('下载进程错误：', __err)

    def def_sftp_upload_process(self, _dic_01, _host, _sftpport, _sftpuser, _sftppwd, _local_file_path, _remote_dir_path):
        try:
            __chunk_size = MAX_PACKET_SIZE  # 例如：每次上传1MB
            __local_file_size = os.path.getsize(_local_file_path)

            __sftpTransport = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)

            try:
                __sftpTransport.listdir_attr(_remote_dir_path)
            except Exception as err01:
                print('目录：', err01, _remote_dir_path)
                try:
                    __sftpTransport.mkdir(_remote_dir_path)
                except Exception as err02:
                    print('目录：', err02, _remote_dir_path)
            finally:
                with __sftpTransport.open(os.path.join(os.path.dirname(_remote_dir_path), os.path.basename(_local_file_path)).replace('\\', '/'), 'wb') as __remote_file:
                    # remote_file.seek(local_file_size)
                    __remote_file.truncate(__local_file_size)
                print('临时 ', _dic_01['目录进度'], os.path.join(os.path.dirname(_remote_dir_path), os.path.basename(_local_file_path)).replace('\\', '/'))
                __sftpTransport.close()

            if __chunk_size > __local_file_size:
                __chunk_size = __local_file_size
            elif __local_file_size == 0:
                return
            __num_threads = int((__local_file_size + __chunk_size - 1) / __chunk_size)  # 至少一个线程，但不超过4个offsets
            __offsets = []
            with open(_local_file_path, 'rb') as local_file:
                # 计算每个线程的起始和结束偏移量
                __offsets = [(__i * __chunk_size, min((__i + 1) * __chunk_size, __local_file_size)) for __i in range(__num_threads)]

                # 创建并启动线程
                __index = 0
                __dic_02 = {}
                for __i01, (__start01, __end01) in enumerate(__offsets):
                    __current_process2 = __i01 + 1
                    __total_length01 = len(__offsets)
                    __process_percentage2 = (__current_process2 / __total_length01) * 100
                    __remote_tmp_file = os.path.join(os.path.dirname(_remote_dir_path), os.path.basename(_local_file_path)).replace('\\', '/')
                    __dic_02.update({'目录进度': _dic_01, '文件进度': __remote_tmp_file + ' ' + f'{__total_length01}/{__current_process2} ({__process_percentage2:.2f}%)'})

                    __t = threading.Thread(target=self.def_sftp_upload_chunk_thread, args=(__dic_02, _host, _sftpport, _sftpuser, _sftppwd, _remote_dir_path, _local_file_path, __start01, __end01))
                    __t.start()
                    if __index == THREADNUM or len(__offsets) <= THREADNUM:
                        __t.join()
                        __index = 0
                    __index = __index + 1
            _dic_01['删除文件'].update({_local_file_path: ''})
            _dic_01['备份文件'].update({_local_file_path: ''})
            with open('./上传日志.log', 'a+', encoding='utf-8') as __del_file:
                __del_file.write(_dic_01 + '|' + _local_file_path + '|' + f'{__total_length01}/{__current_process2} ({__process_percentage2:.2f}%)' + '\n')
        except Exception as __err:
            print('上传进程错误：', __err)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='zabbix  api ', usage='%(prog)s [options]')
    # ![]
    parser.add_argument('-sftpupload', nargs='?', metavar='无参数', dest='sftpupload',
                        default='sftpupload',
                        help=u"sftp上传")
    parser.add_argument('-sftpdownload', nargs='?', metavar='无参数', dest='sftpdownload',
                        default='sftpdownload',
                        help=u"sftp下载")
    if len(sys.argv) == 1:
        print(parser.print_help())
    else:
        args = parser.parse_args()
        __cus_excel_op = CusExcelOp()
        __cus_file_trans_port = CusFileTransPort()
        if args.sftpupload != 'sftpupload':
            __cus_excel_op.def_load_excel(file='fileTransport.xlsx', index=1)

            __column_1_list = __cus_excel_op.def_get_col_value(1)
            del __column_1_list[0]
            __column_2_list = []  # 协议
            __column_3_list = []  # 用户名
            __column_4_list = []  # 密码
            __column_5_list = []  # 端口
            __column_6_list = []  # 源目录
            __column_7_list = []  # 目的目录
            __column_8_list = []  # 文件队列
            __column_9_list = []  # 备份目录
            for __i_00 in range(len(__column_1_list)):
                __column_2_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 2))
                __column_3_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 3))
                __column_4_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 4))
                __column_5_list.append(int(__cus_excel_op.def_get_cell_value(__i_00 + 2, 5)))
                __column_6_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 6))
                __column_7_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 7))
                __column_8_list.append(int(__cus_excel_op.def_get_cell_value(__i_00 + 2, 8)))
                __column_9_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 9)))

            __process_put_list01 = []
            __process_mov_list01 = []
            __process_del_list01 = []
            __dic_del_file_list = Manager().dict()
            __dic_mov_file_list = Manager().dict()
            for __i_01 in range(len(__column_6_list)):
                __lv_list_all_file = []
                __cus_file_trans_port.def_get_os_file_list(__column_6_list[__i_01], __lv_list_all_file, __column_8_list[__i_01], FILEFLAG)
                __chunk_size = THREADNUM
                __local_file_size = len(__lv_list_all_file)
                if __local_file_size == 0:
                    print(__column_6_list[__i_01], '文件不存在或目录为空')
                __num_threads = int((__local_file_size + __chunk_size - 1) / __chunk_size)
                __offsets = []
                for __i_02 in range(__num_threads):
                    if __i_02 == __num_threads - 1:
                        __offsets.append((__i_02 * __chunk_size, len(__lv_list_all_file)))
                    else:
                        __offsets.append((__i_02 * __chunk_size, min((__i_02 + 1) * __chunk_size, (__i_02 + 9) * __chunk_size)))
                for __i_03, (__start, __end) in enumerate(__offsets):
                    __dic_01 = {}
                    __current_process = __i_03 + 1
                    __total_length = len(__offsets)
                    __process_percentage = (__current_process / __total_length) * 100
                    __dic_01.update({'删除文件': __dic_del_file_list, '备份文件': __dic_mov_file_list, '目录进度': f'{__total_length}/{__current_process} ({__process_percentage:.2f}%) {__column_6_list[__i_01]}'})
                    try:
                        for __i_04 in range(__start, __end):
                            # _host, _sftpport, _sftpuser, _sftppwd, _localdirpath, _remotefilepath
                            if __column_9_list[__i_01] != 'None':
                                if __dic_mov_file_list.get(__lv_list_all_file[__i_04], None) is None:
                                    __dic_mov_file_list.update({__lv_list_all_file[__i_04]: [{__column_9_list[__i_01]: ''}]})
                                else:
                                    __dic_mov_file_list[__lv_list_all_file[__i_04]].append({__column_9_list[__i_01]: ''})
                            __p = Process(target=__cus_file_trans_port.def_sftp_upload_process, args=(__dic_01, __column_1_list[__i_01], __column_5_list[__i_01], __column_3_list[__i_01],
                                                                                                      __column_4_list[__i_01], __lv_list_all_file[__i_04],
                                                                                                      __column_7_list[__i_01]))
                            __p.start()
                            __process_put_list01.append(__p)
                        for __i_05 in __process_put_list01:
                            __i_05.join()
                    except Exception as err:
                        print(__column_6_list[__i_01], ' 主进程错误：', err)
            for __i_06, (key, value) in enumerate(__dic_mov_file_list.items()):
                __dic_03 = {}
                __current_process = __i_06 + 1
                __total_length = len(__dic_mov_file_list.keys())
                __process_percentage = (__current_process / __total_length) * 100
                __dic_03.update({'文件进度': f'{__total_length}/{__current_process} ({__process_percentage:.2f}%)'})
                __p02 = Process(target=__cus_file_trans_port.def_move_files_backup_process, args=(__dic_03, key, value))
                __p02.start()
                __process_mov_list01.append(__p02)
            for __i_07 in __process_mov_list01:
                __i_07.join()

            for __i_08, (key) in enumerate(__dic_del_file_list.keys()):
                __dic_02 = {}
                __current_process = __i_08 + 1
                __total_length = len(__dic_del_file_list.keys())
                __process_percentage = (__current_process / __total_length) * 100
                __dic_02.update({'文件进度': f'{__total_length}/{__current_process} ({__process_percentage:.2f}%) {key}'})
                __p03 = Process(target=__cus_file_trans_port.def_delete_os_files, args=(__dic_02, key))
                __p03.start()
                __process_del_list01.append(__p03)
            for __i_09 in __process_del_list01:
                __i_09.join()

        if args.sftpdownload != 'sftpdownload':
            __cus_excel_op.def_load_excel(file='fileTransport.xlsx', index=2)

            __column_1_list = __cus_excel_op.def_get_col_value(1)  # IP地址
            del __column_1_list[0]
            __column_2_list = []  # 协议
            __column_3_list = []  # 用户名
            __column_4_list = []  # 密码
            __column_5_list = []  # 端口
            __column_6_list = []  # 源目录
            __column_7_list = []  # 目的目录
            __column_8_list = []  # 文件队列
            __column_9_list = []  # 备份目录
            for __i_00 in range(len(__column_1_list)):
                __column_2_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 2))  #
                __column_3_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 3))
                __column_4_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 4))
                __column_5_list.append(int(__cus_excel_op.def_get_cell_value(__i_00 + 2, 5)))
                __column_6_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 6))
                __column_7_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 7))
                __column_8_list.append(int(__cus_excel_op.def_get_cell_value(__i_00 + 2, 8)))
                __column_9_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 9)))

            __process_put_list01 = []
            __process_mov_list01 = []
            __process_del_list01 = []
            __dic_del_file_list = Manager().dict()
            __dic_mov_file_list = Manager().dict()
            for __i_01 in range(len(__column_6_list)):
                __lv_list_all_file = []
                # _host, _sftpport, _sftpuser, _sftppwd, remote_dir, file_list, max_length, suffix
                __cus_file_trans_port.def_get_remote_sftp_file_list(__column_1_list[__i_01], __column_5_list[__i_01], __column_3_list[__i_01], __column_4_list[__i_01],
                                                                    __column_6_list[__i_01], __lv_list_all_file, __column_8_list[__i_01], FILEFLAG)
                __chunk_size = THREADNUM
                __local_file_size = len(__lv_list_all_file)
                if __local_file_size == 0:
                    print(__column_6_list[__i_01], '文件不存在或目录为空')
                __num_threads = int((__local_file_size + __chunk_size - 1) / __chunk_size)
                __offsets = []
                for __i_02 in range(__num_threads):
                    if __i_02 == __num_threads - 1:
                        __offsets.append((__i_02 * __chunk_size, len(__lv_list_all_file)))
                    else:
                        __offsets.append((__i_02 * __chunk_size, min((__i_02 + 1) * __chunk_size, (__i_02 + 9) * __chunk_size)))
                for __i_03, (__start, __end) in enumerate(__offsets):
                    __dic_01 = {}
                    __current_process = __i_03 + 1
                    __total_length = len(__offsets)
                    __process_percentage = (__current_process / __total_length) * 100
                    __dic_01.update({'删除文件': __dic_del_file_list, '备份文件': __dic_mov_file_list, '目录进度': f'{__total_length}/{__current_process} ({__process_percentage:.2f}%) {__column_6_list[__i_01]}'})
                    try:
                        for __i_04 in range(__start, __end):
                            # _host, _sftpport, _sftpuser, _sftppwd, _localdirpath, _remotefilepath
                            if __column_9_list[__i_01] != 'None':
                                if __dic_mov_file_list.get(__lv_list_all_file[__i_04], None) is None:
                                    __dic_mov_file_list.update({__lv_list_all_file[__i_04]: [{__column_9_list[__i_01]: ''}]})
                                else:
                                    __dic_mov_file_list[__lv_list_all_file[__i_04]].append({__column_9_list[__i_01]: ''})
                            # _host, _sftpport, _sftpuser, _sftppwd, _remotefilepath, _localdirpath,
                            # column_2_list = []  # 协议
                            # column_3_list = []  # 用户名
                            # column_4_list = []  # 密码
                            # column_5_list = []  # 端口
                            # column_6_list = []  # 源目录
                            # column_7_list = []  # 目的目录
                            # column_8_list = []  # 文件队列
                            # column_9_list = []  # 备份目录
                            __p = Process(target=__cus_file_trans_port.def_sftp_download_process, args=(__dic_01, __column_1_list[__i_01], __column_5_list[__i_01], __column_3_list[__i_01],
                                                                                                        __column_4_list[__i_01], __lv_list_all_file[__i_04],
                                                                                                        __column_7_list[__i_01]))
                            __p.start()
                            __process_put_list01.append(__p)
                        for __i_05 in __process_put_list01:
                            __i_05.join()
                    except Exception as err:
                        print(__column_6_list[__i_01], '下载主进程错误：', err)

            for __i_10 in range(len(__column_6_list)):
                for __i_08, (key) in enumerate(__dic_del_file_list.keys()):
                    __dic_02 = {}
                    __current_process = __i_08 + 1
                    __total_length = len(__dic_del_file_list.keys())
                    __process_percentage = (__current_process / __total_length) * 100
                    __dic_02.update({'文件进度': f'{__total_length}/{__current_process} ({__process_percentage:.2f}%) {key}'})
                    __p03 = Process(target=__cus_file_trans_port.def_delete_remote_files, args=(__column_1_list[__i_10], __column_5_list[__i_10], __column_3_list[__i_10],
                                                                                                __column_4_list[__i_10], __dic_02, key))
                    __p03.start()
                    __process_del_list01.append(__p03)
                for __i_09 in __process_del_list01:
                    __i_09.join()
