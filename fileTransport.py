import argparse
import os
import multiprocessing
from multiprocessing import Process, Manager, Pool
from queue import Empty
import socket
import paramiko
import datetime
import sys
import openpyxl
import shutil
import subprocess
import time
import inspect

# PROCESSNUM = multiprocessing.cpu_count() * 3
# SUBPROCESSNUM = 3
# SUBPROCESSNUM = os.cpu_count()
# SUBPROCESSNUM = 32

PROCESSNUM = 100
QUEUEMAXSIZE = 200
TIMEOUT = 3
SUBPROCESSNUM = 20
MAX_PACKET_SIZE = 10 * 1024 * 1024
DEFAULT_MAX_PACKET_SIZE = MAX_PACKET_SIZE * SUBPROCESSNUM * PROCESSNUM
FILEFLAG = ''
MAX_RETYIES = 5
RETRY_DELAY = 3


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
        self.wb_object = openpyxl.load_workbook(self.file, data_only=True)
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


class CusSFTPConnectionError(Exception):
    pass


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

    @staticmethod
    def def_write_log(_log_file_name, _write_str):
        __current_date_01 = datetime.datetime.now().strftime('%Y%m%d')
        __current_time_01 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(f'./{_log_file_name}_{__current_date_01}.log', 'a+', encoding='utf-8') as __del_file_01:
            __del_file_01.write(f'{__current_time_01} {_write_str}\n')
        print(f'{__current_time_01} | {_write_str}')

    def def_delete_os_files(self, _dic_01, _local_file_path):
        try:
            # sftpTransport.remove(_localdirpath)
            if os.path.exists(_local_file_path):
                os.remove(_local_file_path)
                self.def_write_log('upload', f'删除 | {_dic_01["文件进度"]}')
            # os.remove(_localdirpath)
            # shutil.move(remote_tmp_file, )
        except Exception as __err:
            self.def_write_log('upload', f'删除错误 | {_dic_01["文件进度"]} {str(__err)}')
            exit(1)

    def def_delete_remote_files(self, _host, _sftpport, _sftpuser, _sftppwd, _dic_01, _remote_file_path):
        try:
            __sftpTransport, __sftpClient, __sock = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
            if __sftpTransport is None:
                raise CusSFTPConnectionError(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')
            # sftpTransport.remove(_localdirpath)
            if __sftpTransport.stat(_remote_file_path):
                __sftpTransport.remove(_remote_file_path)
                self.def_write_log('download', f'删除 | {_dic_01["文件进度"]}')
            # os.remove(_localdirpath)
            # shutil.move(remote_tmp_file, )
        except Exception as __err:
            self.def_write_log('download', f'删除错误 | {_dic_01["文件进度"]} {str(__err)}')
            if '__sftpTransport' in locals() and __sftpTransport:
                __sftpTransport.close()  # 确保连接被关闭
            if '__sock' in locals() and __sock:
                __sock.close()
            if '__sftpClient' in locals() and __sftpClient:
                __sftpClient.close()
            self.def_delete_remote_files(_host, _sftpport, _sftpuser, _sftppwd, _dic_01, _remote_file_path)
        finally:
            if '__sftpTransport' in locals() and __sftpTransport:
                __sftpTransport.close()  # 确保连接被关闭
            if '__sock' in locals() and __sock:
                __sock.close()
            if '__sftpClient' in locals() and __sftpClient:
                __sftpClient.close()

    def def_rename_local_tmp_files_thread(self, _dic_01, _remote_dir_path, _local_file_path, _local_dir_path):
        _len__remote_file_path = len(_remote_dir_path)
        __local_file_dir_path = os.path.dirname(_local_file_path)
        try:
            shutil.move(os.path.abspath(f'{_local_file_path}.tmp'), os.path.abspath(_local_file_path))
            self.def_write_log('download', f'完成 | {_dic_01["文件进度"]} | {_local_file_path}')
        except Exception as __err_01:
            try:
                self.def_write_log('download', f'重命名错误本地文件已存在 {_dic_01["文件进度"]} | {_local_file_path} {str(__err_01)}')
                os.remove(_local_file_path)
            finally:
                self.def_rename_local_tmp_files_thread(_dic_01, _remote_dir_path, _local_file_path, _local_dir_path)

    def def_rename_remote_tmp_files_thread(self, _dic_01, _host, _sftpport, _sftpuser, _sftppwd, _local_dir_path, _remote_file_path, _remote_dir_path):
        _len__local_file_path = len(_local_dir_path)
        __remote_file_dir_path = os.path.dirname(_remote_file_path)
        try:
            __sftpTransport, __sftpClient, __sock = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
            if __sftpTransport is None:
                raise CusSFTPConnectionError(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')
            __sftpTransport.rename(f'{_remote_file_path}.tmp', _remote_file_path)
            self.def_write_log('upload', f'重命名远端临时文件完成 | {_dic_01["文件进度"]} | {_remote_file_path}')
        except Exception as __err_01:
            try:
                self.def_write_log('upload', f'重命名错误远端文件已存在 {_dic_01["文件进度"]} | {_remote_file_path} {str(__err_01)}')
                __sftpTransport = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
                if __sftpTransport is None:
                    raise CusSFTPConnectionError(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')
                __sftpTransport.remove(_remote_file_path)
            finally:
                if '__sftpTransport' in locals() and __sftpTransport:
                    __sftpTransport.close()  # 确保连接被关闭
                if '__sock' in locals() and __sock:
                    __sock.close()
                if '__sftpClient' in locals() and __sftpClient:
                    __sftpClient.close()
                self.def_rename_remote_tmp_files_thread(_dic_01, _host, _sftpport, _sftpuser, _sftppwd, _local_dir_path, _remote_file_path, _remote_dir_path)
        finally:
            if '__sftpTransport' in locals() and __sftpTransport:
                __sftpTransport.close()  # 确保连接被关闭
            if '__sock' in locals() and __sock:
                __sock.close()
            if '__sftpClient' in locals() and __sftpClient:
                __sftpClient.close()

    def def_consumer_rename_remote_tmp_files_thread(self, _dic_01, _host, _sftpport, _sftpuser, _sftppwd, _local_dir_path, _remote_file_path, _remote_dir_path):
        _len__local_file_path = len(_local_dir_path)
        __remote_file_dir_path = os.path.dirname(_remote_file_path)
        try:
            __sftpTransport = None
            __sftpClient = None
            __sock = None
            if __sftpTransport is None:
                __sftpTransport, __sftpClient, __sock = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
            if __sftpTransport is None:
                raise CusSFTPConnectionError(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')
            __sftpTransport.rename(f'{_remote_file_path}.tmp', _remote_file_path)
            self.def_write_log('upload', f'重命名远端临时文件完成 | {_dic_01["文件进度"]} | {_remote_file_path}')
        except Exception as __err_01:
            try:
                self.def_write_log('upload', f'重命名错误远端文件已存在 {_dic_01["文件进度"]} | {_remote_file_path} {str(__err_01)}')
                if __sftpTransport is None:
                    __sftpTransport = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
                if __sftpTransport is None:
                    raise CusSFTPConnectionError(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')
                __sftpTransport.remove(_remote_file_path)
            finally:
                if '__sftpTransport' in locals() and __sftpTransport:
                    __sftpTransport.close()  # 确保连接被关闭
                if '__sock' in locals() and __sock:
                    __sock.close()
                if '__sftpClient' in locals() and __sftpClient:
                    __sftpClient.close()
        finally:
            if '__sftpTransport' in locals() and __sftpTransport:
                __sftpTransport.close()  # 确保连接被关闭
            if '__sock' in locals() and __sock:
                __sock.close()
            if '__sftpClient' in locals() and __sftpClient:
                __sftpClient.close()

    def def_move_remote_files_thread(self, _dic_01, _host, _sftpport, _sftpuser, _sftppwd, _remote_file_path, _remote_done_file_path):
        try:
            __sftpTransport, __sftpClient, __sock = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
            if __sftpTransport is None:
                raise CusSFTPConnectionError(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')
            __sftpTransport.rename(_remote_file_path, _remote_done_file_path)
            self.def_write_log('download', f'完成 | {_dic_01["文件进度"]} | {_remote_file_path} | {_remote_done_file_path}')
        except Exception as __err_01:
            try:
                self.def_write_log('download', f'移动文件错误目录不存在 {_dic_01["文件进度"]} {str(__err_01)}')
                __sftpTransport = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
                if __sftpTransport is None:
                    raise CusSFTPConnectionError(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')
                self.def_sftp_mkdir_p(__sftpTransport, os.path.dirname(_remote_done_file_path))
            finally:
                if '__sftpTransport' in locals() and __sftpTransport:
                    __sftpTransport.close()  # 确保连接被关闭
                if '__sock' in locals() and __sock:
                    __sock.close()
                if '__sftpClient' in locals() and __sftpClient:
                    __sftpClient.close()
                self.def_move_remote_files_thread(_dic_01, _host, _sftpport, _sftpuser, _sftppwd, _remote_file_path, _remote_done_file_path)
        finally:
            if '__sftpTransport' in locals() and __sftpTransport:
                __sftpTransport.close()  # 确保连接被关闭
            if '__sock' in locals() and __sock:
                __sock.close()
            if '__sftpClient' in locals() and __sftpClient:
                __sftpClient.close()

    def def_move_local_file_process(self, _dic_01, _local_file_path, _local_done_dir_path):
        try:
            if not os.path.exists(os.path.dirname(_local_done_dir_path)):
                os.makedirs(os.path.dirname(_local_done_dir_path))
        except Exception as __err_01:
            self.def_write_log('upload', f'移动本地文件错误 {_dic_01["文件进度"]} {str(__err_01)}')
        finally:
            try:
                shutil.move(_local_file_path, _local_done_dir_path)
                self.def_write_log('upload', f'移动本地文件完成 | {_dic_01["文件进度"]} | {_local_file_path} | {_local_done_dir_path}')
            except Exception as __err_02:
                self.def_write_log('upload', f'移动本地文件错误 | {_dic_01["文件进度"]} |  {str(__err_02)}')

    def def_get_remote_sftp_file_list(self, _host, _sftpport, _sftpuser, _sftppwd, _remote_dir, _file_list, _max_length, _suffix):
        try:
            __sftpTransport, __sftpClient, __sock = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
            if __sftpTransport is None:
                raise CusSFTPConnectionError(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')
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
            if '__sftpTransport' in locals() and __sftpTransport:
                __sftpTransport.close()  # 确保连接被关闭
            if '__sock' in locals() and __sock:
                __sock.close()
            if '__sftpClient' in locals() and __sftpClient:
                __sftpClient.close()
            self.def_get_remote_sftp_file_list(_host, _sftpport, _sftpuser, _sftppwd, _remote_dir, _file_list, _max_length, _suffix)
            self.def_write_log('download', f'目录错误 | {_remote_dir} | 在SFTP服务器不存在')

        except Exception as _err:
            self.def_write_log('download', f'目录错误 |  {str(_err)}')
        finally:
            if '__sftpTransport' in locals() and __sftpTransport:
                __sftpTransport.close()  # 确保连接被关闭
            if '__sock' in locals() and __sock:
                __sock.close()
            if '__sftpClient' in locals() and __sftpClient:
                __sftpClient.close()
        return _file_list

    def def_get_os_file_list(self, _dir, _file_list, _file_lenth, _suffix):
        if os.path.isfile(_dir) and len(_file_list) < _file_lenth:
            if _dir.endswith(_suffix):
                _file_list.append(_dir)
        elif os.path.isdir(_dir):
            for __s in os.listdir(_dir):
                __newDir = os.path.join(_dir, __s)
                self.def_get_os_file_list(__newDir, _file_list, _file_lenth, _suffix)
        return _file_list

    def def_get_os_file_list_find_local(self, _dir, _file_lenth, _suffix):
        _file_list = []
        try:
            __res_out = self.def_local_find_file_list("""find {v01} -type f ! -name "*.tmp" -printf '%T@\t%p\n' | sort -n | head -n {v02} | cut -f2-""".format(v01=_dir, v02=_file_lenth))
            time.sleep(0.1)
            _file_list = __res_out.stdout.read().strip().split('\n')
        except Exception as __err:
            self.def_write_log('upload', f'获取本地文件队列错误 | {_dir} | 本地目录列表未能正常获取 | {str(__err)}')
        return _file_list

    def def_get_os_file_list_find_remote(self, _host, _sftpport, _sftpuser, _sftppwd, _dir, _file_lenth, _suffix):
        # 初始化一个空列表来存储文件名
        __file_list = []
        try:
            __ssh_channel = self.def_ssh_client_connect(_host, _sftpport, _sftpuser, _sftppwd)
            if __ssh_channel is None:
                raise CusSFTPConnectionError(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')
            __ssh_channel.exec_command("""find {v01} -type f ! -name "*.tmp" -printf '%T@\t%p\n' | sort -n | head -n {v02} | cut -f2-""".format(v01=_dir, v02=_file_lenth))
            __str = ''
            # 循环接收数据，直到没有数据可接收
            while True:
                __data = __ssh_channel.recv(1024)
                if len(__data) == 0:
                    # 没有更多数据可接收，跳出循环
                    break
                    # 将接收到的数据解码并分割成列表
                __str = __str + __data.decode().strip()
            decoded_data = __str.split('\n')
            # 移除可能的空行，并将文件名添加到列表中
            __file_list.extend([line for line in decoded_data if line])
            # 现在 file_list 是一个包含文件名的列表
            # __stderr = __ssh_channel.recv_stderr(1024).decode().split('')
            # print(__stdout, __stderr)
            __ssh_channel.close()
        except Exception as __err:
            self.def_write_log('download', f'{_host} | {_dir} | 获取错误：远端目录列表未能正常获取 | {__file_list} {str(__err)}')
        finally:
            if '__ssh_channel' in locals() and __ssh_channel:
                __ssh_channel.close()  # 确保连接被关闭
        return __file_list

    def def_rmdir_local_empty(self, _dir):
        _file_list = []
        try:
            __res_out = self.def_local_find_file_list("""find {v01} -type d -empty -not -path {v01} -delete""".format(v01=_dir))
            time.sleep(0.1)
            _file_list = __res_out.stdout.read().strip().split('\n')
        except Exception as __err:
            self.def_write_log('upload', f'删除本地空目录错误 | {_dir} | {str(__err)}')
        return _file_list

    def def_rmdir_remote_empty(self, _host, _sftpport, _sftpuser, _sftppwd, _dir):
        # 初始化一个空列表来存储文件名
        __file_list = []
        try:
            __ssh_channel = self.def_ssh_client_connect(_host, _sftpport, _sftpuser, _sftppwd)
            if __ssh_channel is None:
                raise CusSFTPConnectionError(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')
            __ssh_channel.exec_command("""find {v01} -type d -empty -not -path {v01} -delete""".format(v01=_dir))
            __str = ''
            # 循环接收数据，直到没有数据可接收
            while True:
                __data = __ssh_channel.recv(1024)
                if len(__data) == 0:
                    # 没有更多数据可接收，跳出循环
                    break
                    # 将接收到的数据解码并分割成列表
                __str = __str + __data.decode().strip()
            decoded_data = __str.split('\n')
            # 移除可能的空行，并将文件名添加到列表中
            __file_list.extend([line for line in decoded_data if line])
            # 现在 file_list 是一个包含文件名的列表
            # __stderr = __ssh_channel.recv_stderr(1024).decode().split('')
            # print(__stdout, __stderr)
            __ssh_channel.close()
        except Exception as __err:
            self.def_write_log('download', f'删除空目录错误 | {_dir} | {str(__err)}')
        finally:
            if '__ssh_channel' in locals() and __ssh_channel:
                __ssh_channel.close()  # 确保连接被关闭
        return __file_list

    @staticmethod
    def def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd):
        # print('connect creat', f'{_host}')
        __max_retries = MAX_RETYIES
        for attempt in range(__max_retries):
            try:
                __timeout = TIMEOUT
                __sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                __sock.settimeout(__timeout)
                __sock.connect((_host, _sftpport))
                __sftpClient = paramiko.Transport(__sock, default_max_packet_size=DEFAULT_MAX_PACKET_SIZE, default_window_size=DEFAULT_MAX_PACKET_SIZE)
                # sftpClient = paramiko.Transport(sock)
                __sftpClient.banner_timeout = __timeout
                # sftpClient.packetizer.REKEY_BYTES = pow(2, 40)
                # sftpClient.packetizer.REKEY_PACKETS = pow(2, 40)
                __sftpClient.start_client()  # 启动SSH客户端模式
                if __sftpClient.is_active():
                    if os.path.isfile(_sftppwd):
                        __pkey = paramiko.RSAKey.from_private_key_file(_sftppwd)
                        __sftpClient.auth_publickey(username=_sftpuser, key=__pkey)
                    else:
                        # 如果有需要，使用用户名和密码进行身份验证
                        __sftpClient.auth_password(username=_sftpuser, password=_sftppwd)
                    # 现在可以创建SFTP客户端了

                    __sftpTransport = paramiko.SFTPClient.from_transport(__sftpClient, window_size=DEFAULT_MAX_PACKET_SIZE, max_packet_size=DEFAULT_MAX_PACKET_SIZE)
                    __sftpTransport.default_max_packet_size = MAX_PACKET_SIZE
                    __sftpTransport.default_window_size = MAX_PACKET_SIZE
                    return __sftpTransport, __sftpClient, __sock
            except Exception as __err:
                print('-Exception-')
                if '__sftpTransport' in locals() and __sftpTransport:
                    __sftpTransport.close()  # 确保连接被关闭
                if '__sock' in locals() and __sock:
                    __sock.close()
                if '__sftpClient' in locals() and __sftpClient:
                    __sftpClient.close()
                if attempt < __max_retries - 1:
                    print(f'等待 {RETRY_DELAY} 秒后重试... {__err}')
                    time.sleep(RETRY_DELAY)

        print(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')
        if '__sftpTransport' in locals() and __sftpTransport:
            __sftpTransport.close()  # 确保连接被关闭
        if '__sock' in locals() and __sock:
            __sock.close()
        if '__sftpClient' in locals() and __sftpClient:
            __sftpClient.close()
        return None

    @staticmethod
    def def_ssh_client_connect(_host, _sftpport, _sftpuser, _sftppwd):
        __max_retries = MAX_RETYIES
        for attempt in range(__max_retries):
            try:
                __timeout = TIMEOUT
                __sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                __sock.settimeout(__timeout)
                __sock.connect((_host, _sftpport))
                __sftpClient = paramiko.Transport(__sock, default_max_packet_size=DEFAULT_MAX_PACKET_SIZE, default_window_size=DEFAULT_MAX_PACKET_SIZE)
                if __sftpClient.is_active():
                    # sftpClient = paramiko.Transport(sock)
                    __sftpClient.banner_timeout = __timeout
                    # sftpClient.packetizer.REKEY_BYTES = pow(2, 40)
                    # sftpClient.packetizer.REKEY_PACKETS = pow(2, 40)
                    __sftpClient.connect(username=_sftpuser, password=_sftppwd)
                    __ssh_channel = __sftpClient.open_channel(kind='session', timeout=__timeout)
                    return __ssh_channel
            except Exception as __err:
                print('-Exception-')
                if '__ssh_channel' in locals() and __ssh_channel:
                    __ssh_channel.close()  # 确保连接被关闭
                if '__sock' in locals() and __sock:
                    __sock.close()
                if '__sftpClient' in locals() and __sftpClient:
                    __sftpClient.close()
                if attempt < __max_retries - 1:
                    print(f'等待 {RETRY_DELAY} 秒后重试... {__err}')
                    time.sleep(RETRY_DELAY)

        print(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')
        return None

    @staticmethod
    def def_local_find_file_list(_command):
        __result = subprocess.Popen(_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        return __result

    def def_sftp_mkdir_p(self, _sftp, _remote_path):
        """
        递归地创建SFTP中的目录结构。
        如果目录已经存在，则不执行任何操作。

        :param _sftp: 已连接的SFTP客户端实例
        :param _remote_path: 要创建的远程目录路径
        :return: None
        """
        parts = _remote_path.split('/')
        path_so_far = ''
        for part in parts:
            if part:  # 忽略空字符串（例如，如果remote_path以'/'开头）
                path_so_far = path_so_far + '/' + part
                try:
                    _sftp.stat(path_so_far)  # 尝试获取目录的状态以检查它是否存在
                except FileNotFoundError:  # 如果目录不存在，则创建它
                    _sftp.mkdir(path_so_far, mode=0o777)

    def def_producer_upload(self, _queue, _dic_manager):
        __cus_excel_op = CusExcelOp()
        __cus_excel_op.def_load_excel(file='/etc/zabbix/scripts/fileTransport.xlsx', index=1)
        __column_1_list = __cus_excel_op.def_get_col_value(1)
        del __column_1_list[0]
        __column_2_list = []  # 协议
        __column_3_list = []  # 用户名
        __column_4_list = []  # 密码
        __column_5_list = []  # 端口
        __column_6_list = []  # 6_本地文件或目录
        __column_7_list = []  # 7_上传目录
        __column_8_list = []  # 8_上传文件数
        __column_9_list = []  # 9_是否删除源文件
        __column_10_list = []  # 10_上传完成后移动到目录
        for __i_00 in range(len(__column_1_list)):
            __column_2_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 2))
            __column_3_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 3))
            __column_4_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 4)))
            __column_5_list.append(int(__cus_excel_op.def_get_cell_value(__i_00 + 2, 5)))
            __column_6_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 6))
            __column_7_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 7))
            __column_8_list.append(int(__cus_excel_op.def_get_cell_value(__i_00 + 2, 8)))
            __column_9_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 9)))
            __column_10_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 10)))
        for __i_01 in range(len(__column_6_list)):
            __lv_list_all_file_tmp = self.def_get_os_file_list_find_local(__column_6_list[__i_01], __column_8_list[__i_01], FILEFLAG)
            __lv_list_all_file = list(filter(None, __lv_list_all_file_tmp))
            # __lv_list_all_file = []
            # __cus_file_trans_port.def_get_os_file_list(__column_6_list[__i_01], __lv_list_all_file, __column_8_list[__i_01], FILEFLAG)
            __chunk_size_03 = PROCESSNUM
            __local_file_size_02 = len(__lv_list_all_file)

            _host = __column_1_list[__i_01]
            _sftpuser = __column_3_list[__i_01]
            _local_dir_path = __column_6_list[__i_01]
            _dic_manager.update({f'{_host}_{_sftpuser}_{_local_dir_path}': __local_file_size_02})

            __current_excel_dir_process = __i_01 + 1
            __total_excel_dir_length = len(__column_6_list)
            __process_excel_dir_percentage = (__current_excel_dir_process / __total_excel_dir_length) * 100

            if __local_file_size_02 == 0:
                __current_dir_name = __column_6_list[__i_01]
                self.def_write_log('upload', f'上传 | {__total_excel_dir_length}/{__current_excel_dir_process} ({__process_excel_dir_percentage:.2f}%) {__current_dir_name} | 文件不存在或目录为空')
                continue
            __num_threads_03 = int((__local_file_size_02 + __chunk_size_03 - 1) / __chunk_size_03)
            __offsets_03 = []
            for __i_02 in range(__num_threads_03):
                if __i_02 == __num_threads_03 - 1:
                    __offsets_03.append((__i_02 * __chunk_size_03, len(__lv_list_all_file)))
                else:
                    __offsets_03.append((__i_02 * __chunk_size_03, min((__i_02 + 1) * __chunk_size_03, (__i_02 + 9) * __chunk_size_03)))
            __process_put_list01 = []
            __process_mov_list01 = []
            __process_del_list01 = []
            __dic_del_file_list = {}
            __dic_rename_file_list = {}
            __dic_mov_file_list = {}
            for __i_03, (__start, __end) in enumerate(__offsets_03):
                __dic_01 = {}
                __dic_01.update({'删除文件': __dic_del_file_list,
                                 '移动文件': __dic_mov_file_list,
                                 '重命名文件': __dic_rename_file_list,
                                 '目录进度': f'{__total_excel_dir_length}/{__current_excel_dir_process} ({__process_excel_dir_percentage:.2f}%) {__column_6_list[__i_01]} {__column_7_list[__i_01]}',
                                 })
                try:
                    for __i_04 in range(__start, __end):
                        __current_upload_file_process = __i_04 + 1
                        __total_upload_file_length = __local_file_size_02
                        __process_upload_file_percentage = (__current_upload_file_process / __total_upload_file_length) * 100
                        __dic_01.update({
                            '文件进度': f'{__total_upload_file_length}/{__current_upload_file_process} ({__process_upload_file_percentage:.2f}%) {__lv_list_all_file[__i_04]}',
                        })
                        _dic_01 = __dic_01
                        _host = __column_1_list[__i_01]
                        _sftpport = __column_5_list[__i_01]
                        _sftpuser = __column_3_list[__i_01]
                        _sftppwd = __column_4_list[__i_01]
                        _local_dir_path = __column_6_list[__i_01]
                        _local_file_path = __lv_list_all_file[__i_04]
                        _remote_dir_path = __column_7_list[__i_01]
                        _local_done_dir_path = __column_10_list[__i_01]
                        if os.path.isfile(_local_dir_path):
                            _local_dir_path = os.path.dirname(_local_dir_path) + '/'
                        _len__local_file_path = len(_local_dir_path)
                        __remote_file_path = os.path.join(_remote_dir_path, _local_file_path[_len__local_file_path:]).replace('\\', '/')
                        __remote_file_dir_path = os.path.dirname(__remote_file_path)
                        __local_done_file_dir_path = os.path.join(_local_done_dir_path, _local_file_path[_len__local_file_path:]).replace('\\', '/')
                        __chunk_size_02 = MAX_PACKET_SIZE  # 例如：每次上传1MB
                        __local_file_size_01 = os.path.getsize(_local_file_path)
                        # __remote_file_path = os.path.join(os.path.dirname(__remote_file_dir_path), os.path.basename(_local_file_path)).replace('\\', '/')

                        if __chunk_size_02 > __local_file_size_01:
                            __chunk_size_02 = __local_file_size_01
                        if __local_file_size_01 == 0:
                            _dic_01['删除文件'].update({_local_file_path: ''})
                            if _local_done_dir_path != "None":
                                _dic_01['移动文件'].update({_local_file_path: __local_done_file_dir_path})
                            _dic_01['重命名文件'].update({__remote_file_path: ''})
                            __dic_04 = {}
                            __item = (__dic_04, _host, _sftpport, _sftpuser, _sftppwd, __remote_file_path, _local_file_path, 0, 0, 0)
                            # print('生成了', __i_04, __item)
                            _queue.put(__item)
                            # print('加入了', __i_04, __item)
                            continue
                        __num_threads_02 = int((__local_file_size_01 + __chunk_size_02 - 1) / __chunk_size_02)  # 至少一个线程，但不超过4个offsets
                        __offsets_02 = []
                        with open(_local_file_path, 'rb'):
                            # 计算每个线程的起始和结束偏移量
                            __offsets_02 = [(__i * __chunk_size_02, min((__i + 1) * __chunk_size_02, __local_file_size_01)) for __i in range(__num_threads_02)]
                        __index_01 = 1
                        __dic_04 = {}
                        for __i01, (__start01, __end01) in enumerate(__offsets_02):
                            __current_process2 = __i01 + 1
                            __total_length01 = len(__offsets_02)
                            __process_percentage2 = (__current_process2 / __total_length01) * 100
                            __current_excel_dir_process_01 = _dic_01['目录进度']
                            __current_excel_file_process_01 = _dic_01['文件进度']
                            __dic_04.update({'分块进度': f'{__current_excel_dir_process_01} | {__current_excel_file_process_01} | {__total_length01}/{__current_process2} ({__process_percentage2:.2f}%) {__remote_file_path}'})
                            __item = (__dic_04, _host, _sftpport, _sftpuser, _sftppwd, __remote_file_path, _local_file_path, __start01, __end01, __local_file_size_01)
                            _queue.put(__item)
                        _dic_01['删除文件'].update({_local_file_path: ''})
                        if _local_done_dir_path != "None":
                            _dic_01['移动文件'].update({_local_file_path: __local_done_file_dir_path})
                        _dic_01['重命名文件'].update({__remote_file_path: ''})
                except Exception as __err:
                    self.def_write_log('upload', f'生成上传队列错误 | {_dic_01["文件进度"]} |  {str(__err)}')
                    _queue.put(__item)
        for _ in range(PROCESSNUM):
            _queue.put(None)

    def def_consumer_upload(self, _queue, __queue_retry):
        # print('consumer start')
        __sftpTransport = None
        __sftpClient = None
        __sock = None
        __host_dic = {}
        while True:
            # print('consumer while start')
            if __queue_retry.qsize() != 0:
                __item = __queue_retry.get(timeout=1)
                __queue_retry.task_done()
                self.def_write_log('upload', f'上传任务进入重传队列 | {__item}')
            elif _queue.qsize() != 0:
                __item = _queue.get(timeout=1)
                _queue.task_done()
            else:
                time.sleep(TIMEOUT)
                continue
            if __item is None or __item == 'None':
                _queue.all_tasks_done()
                __queue_retry.all_tasks_done()
                break
            try:
                _dic_01, _host, _sftpport, _sftpuser, _sftppwd, _remote_file_path, _local_file_path, _start, _end, _local_file_size = __item
                if __host_dic.get(f'{_host}_{_sftpuser}', None) is None:
                    __sftpTransport, __sftpClient, __sock = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
                    if __sftpTransport is None:
                        raise CusSFTPConnectionError(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')
                    __host_dic.update({f'{_host}_{_sftpuser}': __sftpTransport})
                __remote_file_dir_path = os.path.dirname(_remote_file_path)
                self.def_sftp_mkdir_p(__host_dic[f'{_host}_{_sftpuser}'], __remote_file_dir_path)
                if _local_file_size != 0:
                    with open(_local_file_path, 'rb') as __local_file:
                        __local_file.seek(_start)
                        __chunk_data = __local_file.read(_end - _start)
                        with __host_dic[f'{_host}_{_sftpuser}'].open(f'{_remote_file_path}.tmp', 'rb+') as __remote_file:
                            __remote_file.seek(_start)
                            __remote_file.write(__chunk_data)
                self.def_write_log('upload', f'分块上传 | {_dic_01["分块进度"]}')
            except Exception as err_01:
                try:
                    with __host_dic[f'{_host}_{_sftpuser}'].open(f'{_remote_file_path}.tmp', 'wb+') as __remote_file:
                        __remote_file.truncate(_local_file_size)
                        __remote_file.chmod(mode=0o777)
                    self.def_write_log('upload', f'分块上传错误需要重传 | {_dic_01["分块进度"]} {err_01}')
                    __queue_retry.put(__item)
                    continue
                except Exception as err_02:
                    self.def_write_log('upload', f'分块上传未知错误 | {_dic_01["分块进度"]} {err_02}')
                    time.sleep(TIMEOUT)
                    continue

    def def_producer_upload_rename(self, __queue_rename, _dic_manager):
        __cus_excel_op = CusExcelOp()
        __cus_excel_op.def_load_excel(file='/etc/zabbix/scripts/fileTransport.xlsx', index=1)
        __column_1_list = __cus_excel_op.def_get_col_value(1)
        del __column_1_list[0]
        __column_2_list = []  # 协议
        __column_3_list = []  # 用户名
        __column_4_list = []  # 密码
        __column_5_list = []  # 端口
        __column_6_list = []  # 6_本地文件或目录
        __column_7_list = []  # 7_上传目录
        __column_8_list = []  # 8_上传文件数
        __column_9_list = []  # 9_是否删除源文件
        __column_10_list = []  # 10_上传完成后移动到目录
        for __i_00 in range(len(__column_1_list)):
            __column_2_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 2))
            __column_3_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 3))
            __column_4_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 4)))
            __column_5_list.append(int(__cus_excel_op.def_get_cell_value(__i_00 + 2, 5)))
            __column_6_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 6))
            __column_7_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 7))
            __column_8_list.append(int(__cus_excel_op.def_get_cell_value(__i_00 + 2, 8)))
            __column_9_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 9)))
            __column_10_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 10)))

        for __i_01 in range(len(__column_6_list)):
            __lv_list_all_file_tmp = self.def_get_os_file_list_find_local(__column_6_list[__i_01], __column_8_list[__i_01], FILEFLAG)
            __lv_list_all_file = list(filter(None, __lv_list_all_file_tmp))
            # __lv_list_all_file = []
            # self.def_get_os_file_list(__column_6_list[__i_01], __lv_list_all_file, __column_8_list[__i_01], FILEFLAG)
            __chunk_size_03 = PROCESSNUM

            _host = __column_1_list[__i_01]
            _sftpuser = __column_3_list[__i_01]
            _local_dir_path = __column_6_list[__i_01]
            __min_file_lenth = _dic_manager.get(f'{_host}_{_sftpuser}_{_local_dir_path}', 0)

            __local_file_size_02 = min(len(__lv_list_all_file), __min_file_lenth)

            __current_excel_dir_process = __i_01 + 1
            __total_excel_dir_length = len(__column_6_list)
            __process_excel_dir_percentage = (__current_excel_dir_process / __total_excel_dir_length) * 100

            if __local_file_size_02 == 0:
                __current_dir_name = __column_6_list[__i_01]
                self.def_write_log('upload', f'生成重命名队列 | {__total_excel_dir_length}/{__current_excel_dir_process} ({__process_excel_dir_percentage:.2f}%) {__current_dir_name} | 文件不存在或目录为空')
                if int(f'{__i_01 + 1}') == len(__column_6_list):
                    # print(__i_01)
                    for _ in range(PROCESSNUM):
                        __queue_rename.put(None)
                    return
                continue
            __num_threads_03 = int((__local_file_size_02 + __chunk_size_03 - 1) / __chunk_size_03)
            __offsets_03 = []
            for __i_02 in range(__num_threads_03):
                if __i_02 == __num_threads_03 - 1:
                    __offsets_03.append((__i_02 * __chunk_size_03, len(__lv_list_all_file)))
                else:
                    __offsets_03.append((__i_02 * __chunk_size_03, min((__i_02 + 1) * __chunk_size_03, (__i_02 + 9) * __chunk_size_03)))

            __process_put_list01 = []
            __process_mov_list01 = []
            __process_del_list01 = []
            __dic_del_file_list = {}
            __dic_rename_file_list = {}
            __dic_mov_file_list = {}
            for __i_03, (__start, __end) in enumerate(__offsets_03):
                __dic_01 = {}
                __dic_01.update({'删除文件': __dic_del_file_list,
                                 '移动文件': __dic_mov_file_list,
                                 '重命名文件': __dic_rename_file_list,
                                 '目录进度': f'{__total_excel_dir_length}/{__current_excel_dir_process} ({__process_excel_dir_percentage:.2f}%) {__column_6_list[__i_01]} {__column_7_list[__i_01]}',
                                 })

                for __i_04 in range(__start, __end):
                    __current_upload_file_process = __i_04 + 1
                    __total_upload_file_length = __local_file_size_02
                    __process_upload_file_percentage = (__current_upload_file_process / __total_upload_file_length) * 100
                    __dic_01.update({
                        '文件进度': f'{__total_upload_file_length}/{__current_upload_file_process} ({__process_upload_file_percentage:.2f}%) {__lv_list_all_file[__i_04]}',
                    })

                    _dic_01 = __dic_01
                    _host = __column_1_list[__i_01]
                    _sftpport = __column_5_list[__i_01]
                    _sftpuser = __column_3_list[__i_01]
                    _sftppwd = __column_4_list[__i_01]
                    _local_dir_path = __column_6_list[__i_01]
                    _local_file_path = __lv_list_all_file[__i_04]
                    _remote_dir_path = __column_7_list[__i_01]
                    _local_done_dir_path = __column_10_list[__i_01]

                    if os.path.isfile(_local_dir_path):
                        _local_dir_path = os.path.dirname(_local_dir_path) + '/'
                    _len__local_file_path = len(_local_dir_path)
                    __remote_file_path = os.path.join(_remote_dir_path, _local_file_path[_len__local_file_path:]).replace('\\', '/')
                    __remote_file_dir_path = os.path.dirname(__remote_file_path)
                    __local_done_file_dir_path = os.path.join(_local_done_dir_path, _local_file_path[_len__local_file_path:]).replace('\\', '/')
                    __item = (__dic_01, __column_1_list[__i_01],
                                            __column_5_list[__i_01],
                                            __column_3_list[__i_01],
                                            __column_4_list[__i_01],
                                            __column_6_list[__i_01],
                                            __remote_file_path,
                                            __column_7_list[__i_01])
                    # print(f'get {__item} start')
                    __queue_rename.put(__item)
                    # print(f'get {__item} done')
        for _ in range(PROCESSNUM):
            # print(f'exit')
            __queue_rename.put(None)

    def def_consumer_upload_rename(self, __queue_rename, __queue_rename_retry):
        __sftpTransport = None
        __sftpClient = None
        __sock = None
        __host_dic = {}
        while True:
            if __queue_rename_retry.qsize() != 0:
                __item = __queue_rename_retry.get(timeout=1)
                __queue_rename_retry.task_done()
                self.def_write_log('upload', f'重命名任务进入重传队列 | {__item}')
            elif __queue_rename.qsize() != 0:
                __item = __queue_rename.get(timeout=1)
                __queue_rename.task_done()
            else:
                time.sleep(TIMEOUT)
                continue
            if __item is None or __item == 'None':
                __queue_rename.all_tasks_done()
                __queue_rename_retry.all_tasks_done()
                break
            try:
                _dic_01, _host, _sftpport, _sftpuser, _sftppwd, _local_dir_path, _remote_file_path, _remote_dir_path = __item
                _len__local_file_path = len(_local_dir_path)
                __remote_file_dir_path = os.path.dirname(_remote_file_path)

                if __host_dic.get(f'{_host}_{_sftpuser}', None) is None:
                    __sftpTransport, __sftpClient, __sock = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
                    if __sftpTransport is None:
                        # print(f'connect error')
                        raise CusSFTPConnectionError(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')
                    __host_dic.update({f'{_host}_{_sftpuser}': __sftpTransport})
                try:
                    __host_dic[f'{_host}_{_sftpuser}'].rename(f'{_remote_file_path}.tmp', _remote_file_path)
                    self.def_write_log('upload', f'重命名远端文件完成 | {_dic_01["文件进度"]} | {_remote_file_path}')
                except FileNotFoundError as _err_03:
                    # print(f'start task_done {__item} couse {_err_03}')
                    self.def_write_log('upload', f'重命名远端文件异常远端文件不存在忽略 | {_dic_01["文件进度"]} | {_remote_file_path}')
                except Exception as __err_02:
                    __host_dic[f'{_host}_{_sftpuser}'].remove(_remote_file_path)
                    __host_dic[f'{_host}_{_sftpuser}'].rename(f'{_remote_file_path}.tmp', _remote_file_path)
                    self.def_write_log('upload', f'删除存在文件后重命名远端文件完成 | {_dic_01["文件进度"]} | {_remote_file_path}')
            except Exception as err_01:
                __queue_rename_retry.put(__item)
                time.sleep(TIMEOUT)
                continue

    def def_producer_upload_del(self, __queue_del, _dic_manager):
        __cus_excel_op = CusExcelOp()
        __cus_excel_op.def_load_excel(file='/etc/zabbix/scripts/fileTransport.xlsx', index=1)
        __column_1_list = __cus_excel_op.def_get_col_value(1)
        del __column_1_list[0]
        __column_2_list = []  # 协议
        __column_3_list = []  # 用户名
        __column_4_list = []  # 密码
        __column_5_list = []  # 端口
        __column_6_list = []  # 6_本地文件或目录
        __column_7_list = []  # 7_上传目录
        __column_8_list = []  # 8_上传文件数
        __column_9_list = []  # 9_是否删除源文件
        __column_10_list = []  # 10_上传完成后移动到目录
        for __i_00 in range(len(__column_1_list)):
            __column_2_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 2))
            __column_3_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 3))
            __column_4_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 4)))
            __column_5_list.append(int(__cus_excel_op.def_get_cell_value(__i_00 + 2, 5)))
            __column_6_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 6))
            __column_7_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 7))
            __column_8_list.append(int(__cus_excel_op.def_get_cell_value(__i_00 + 2, 8)))
            __column_9_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 9)))
            __column_10_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 10)))

        for __i_01 in range(len(__column_6_list)):
            _local_done_dir_path = __column_10_list[__i_01]
            if __column_9_list[__i_01] == "是":
                __lv_list_all_file_tmp = self.def_get_os_file_list_find_local(__column_6_list[__i_01], __column_8_list[__i_01], FILEFLAG)
                __lv_list_all_file = list(filter(None, __lv_list_all_file_tmp))
                # __lv_list_all_file = []
                # self.def_get_os_file_list(__column_6_list[__i_01], __lv_list_all_file, __column_8_list[__i_01], FILEFLAG)
                __chunk_size_03 = PROCESSNUM

                _host = __column_1_list[__i_01]
                _sftpuser = __column_3_list[__i_01]
                _local_dir_path = __column_6_list[__i_01]
                __min_file_lenth = _dic_manager.get(f'{_host}_{_sftpuser}_{_local_dir_path}', 0)

                __local_file_size_02 = min(len(__lv_list_all_file), __min_file_lenth)

                __current_excel_dir_process = __i_01 + 1
                __total_excel_dir_length = len(__column_6_list)
                __process_excel_dir_percentage = (__current_excel_dir_process / __total_excel_dir_length) * 100

                if __local_file_size_02 == 0:
                    __current_dir_name = __column_6_list[__i_01]
                    self.def_write_log('upload', f'生成删除队列 | {__total_excel_dir_length}/{__current_excel_dir_process} ({__process_excel_dir_percentage:.2f}%) {__current_dir_name} | 文件不存在或目录为空')
                    if int(f'{__i_01 + 1}') == len(__column_6_list):
                        # print(__i_01)
                        for _ in range(PROCESSNUM):
                            __queue_del.put(None)
                        return
                    continue
                __num_threads_03 = int((__local_file_size_02 + __chunk_size_03 - 1) / __chunk_size_03)
                __offsets_03 = []
                for __i_02 in range(__num_threads_03):
                    if __i_02 == __num_threads_03 - 1:
                        __offsets_03.append((__i_02 * __chunk_size_03, len(__lv_list_all_file)))
                    else:
                        __offsets_03.append((__i_02 * __chunk_size_03, min((__i_02 + 1) * __chunk_size_03, (__i_02 + 9) * __chunk_size_03)))

                __process_put_list01 = []
                __process_mov_list01 = []
                __process_del_list01 = []
                __dic_del_file_list = {}
                __dic_rename_file_list = {}
                __dic_mov_file_list = {}
                for __i_03, (__start, __end) in enumerate(__offsets_03):
                    __dic_01 = {}
                    __dic_01.update({'删除文件': __dic_del_file_list,
                                     '移动文件': __dic_mov_file_list,
                                     '重命名文件': __dic_rename_file_list,
                                     '目录进度': f'{__total_excel_dir_length}/{__current_excel_dir_process} ({__process_excel_dir_percentage:.2f}%) {__column_6_list[__i_01]} {__column_7_list[__i_01]}',
                                     })

                    for __i_04 in range(__start, __end):
                        __current_upload_file_process = __i_04 + 1
                        __total_upload_file_length = __local_file_size_02
                        __process_upload_file_percentage = (__current_upload_file_process / __total_upload_file_length) * 100
                        __dic_01.update({
                            '文件进度': f'{__total_upload_file_length}/{__current_upload_file_process} ({__process_upload_file_percentage:.2f}%) {__lv_list_all_file[__i_04]}',
                        })
                        _local_file_path = __lv_list_all_file[__i_04]
                        __queue_del.put((__dic_01, _local_file_path))

        for _ in range(PROCESSNUM):
            __queue_del.put(None)

    def def_producer_upload_move(self, __queue_move, _dic_manager):
        __cus_excel_op = CusExcelOp()
        __cus_excel_op.def_load_excel(file='/etc/zabbix/scripts/fileTransport.xlsx', index=1)
        __column_1_list = __cus_excel_op.def_get_col_value(1)
        del __column_1_list[0]
        __column_2_list = []  # 协议
        __column_3_list = []  # 用户名
        __column_4_list = []  # 密码
        __column_5_list = []  # 端口
        __column_6_list = []  # 6_本地文件或目录
        __column_7_list = []  # 7_上传目录
        __column_8_list = []  # 8_上传文件数
        __column_9_list = []  # 9_是否删除源文件
        __column_10_list = []  # 10_上传完成后移动到目录
        for __i_00 in range(len(__column_1_list)):
            __column_2_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 2))
            __column_3_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 3))
            __column_4_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 4)))
            __column_5_list.append(int(__cus_excel_op.def_get_cell_value(__i_00 + 2, 5)))
            __column_6_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 6))
            __column_7_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 7))
            __column_8_list.append(int(__cus_excel_op.def_get_cell_value(__i_00 + 2, 8)))
            __column_9_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 9)))
            __column_10_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 10)))

        for __i_01 in range(len(__column_6_list)):
            _local_done_dir_path = __column_10_list[__i_01]
            if _local_done_dir_path != "None":
                __lv_list_all_file_tmp = self.def_get_os_file_list_find_local(__column_6_list[__i_01], __column_8_list[__i_01], FILEFLAG)
                __lv_list_all_file = list(filter(None, __lv_list_all_file_tmp))
                # __lv_list_all_file = []
                # self.def_get_os_file_list(__column_6_list[__i_01], __lv_list_all_file, __column_8_list[__i_01], FILEFLAG)
                __chunk_size_03 = PROCESSNUM
                _host = __column_1_list[__i_01]
                _sftpuser = __column_3_list[__i_01]
                _local_dir_path = __column_6_list[__i_01]
                __min_file_lenth = _dic_manager.get(f'{_host}_{_sftpuser}_{_local_dir_path}', 0)

                __local_file_size_02 = min(len(__lv_list_all_file), __min_file_lenth)

                __current_excel_dir_process = __i_01 + 1
                __total_excel_dir_length = len(__column_6_list)
                __process_excel_dir_percentage = (__current_excel_dir_process / __total_excel_dir_length) * 100

                if __local_file_size_02 == 0:
                    __current_dir_name = __column_6_list[__i_01]
                    self.def_write_log('upload', f'生成移动队列 | {__total_excel_dir_length}/{__current_excel_dir_process} ({__process_excel_dir_percentage:.2f}%) {__current_dir_name} | 文件不存在或目录为空')
                    if int(f'{__i_01 + 1}') == len(__column_6_list):
                        # print(__i_01)
                        for _ in range(PROCESSNUM):
                            __queue_move.put(None)
                        return
                    continue
                __num_threads_03 = int((__local_file_size_02 + __chunk_size_03 - 1) / __chunk_size_03)
                __offsets_03 = []
                for __i_02 in range(__num_threads_03):
                    if __i_02 == __num_threads_03 - 1:
                        __offsets_03.append((__i_02 * __chunk_size_03, len(__lv_list_all_file)))
                    else:
                        __offsets_03.append((__i_02 * __chunk_size_03, min((__i_02 + 1) * __chunk_size_03, (__i_02 + 9) * __chunk_size_03)))

                __process_put_list01 = []
                __process_mov_list01 = []
                __process_del_list01 = []
                __dic_del_file_list = {}
                __dic_rename_file_list = {}
                __dic_mov_file_list = {}
                for __i_03, (__start, __end) in enumerate(__offsets_03):
                    __dic_01 = {}
                    __dic_01.update({'删除文件': __dic_del_file_list,
                                     '移动文件': __dic_mov_file_list,
                                     '重命名文件': __dic_rename_file_list,
                                     '目录进度': f'{__total_excel_dir_length}/{__current_excel_dir_process} ({__process_excel_dir_percentage:.2f}%) {__column_6_list[__i_01]} {__column_7_list[__i_01]}',
                                     })

                    for __i_04 in range(__start, __end):
                        __current_upload_file_process = __i_04 + 1
                        __total_upload_file_length = __local_file_size_02
                        __process_upload_file_percentage = (__current_upload_file_process / __total_upload_file_length) * 100
                        __dic_01.update({
                            '文件进度': f'{__total_upload_file_length}/{__current_upload_file_process} ({__process_upload_file_percentage:.2f}%) {__lv_list_all_file[__i_04]}',
                        })

                        _dic_01 = __dic_01
                        _host = __column_1_list[__i_01]
                        _sftpport = __column_5_list[__i_01]
                        _sftpuser = __column_3_list[__i_01]
                        _sftppwd = __column_4_list[__i_01]
                        _local_dir_path = __column_6_list[__i_01]
                        _local_file_path = __lv_list_all_file[__i_04]
                        _remote_dir_path = __column_7_list[__i_01]
                        _local_done_dir_path = __column_10_list[__i_01]
                        if os.path.isfile(_local_dir_path):
                            _local_dir_path = os.path.dirname(_local_dir_path) + '/'
                        _len__local_file_path = len(_local_dir_path)
                        __remote_file_path = os.path.join(_remote_dir_path, _local_file_path[_len__local_file_path:]).replace('\\', '/')
                        __remote_file_dir_path = os.path.dirname(__remote_file_path)
                        __local_done_file_dir_path = os.path.join(_local_done_dir_path, _local_file_path[_len__local_file_path:]).replace('\\', '/')
                        __queue_move.put((__dic_01, _local_file_path, __local_done_file_dir_path))
        for _ in range(PROCESSNUM):
            __queue_move.put(None)

    def def_producer_upload_empty(self, __queue_empty):
        __cus_excel_op = CusExcelOp()
        __cus_excel_op.def_load_excel(file='/etc/zabbix/scripts/fileTransport.xlsx', index=1)
        __column_1_list = __cus_excel_op.def_get_col_value(1)
        del __column_1_list[0]
        __column_2_list = []  # 协议
        __column_3_list = []  # 用户名
        __column_4_list = []  # 密码
        __column_5_list = []  # 端口
        __column_6_list = []  # 6_本地文件或目录
        __column_7_list = []  # 7_上传目录
        __column_8_list = []  # 8_上传文件数
        __column_9_list = []  # 9_是否删除源文件
        __column_10_list = []  # 10_上传完成后移动到目录
        for __i_00 in range(len(__column_1_list)):
            __column_2_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 2))
            __column_3_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 3))
            __column_4_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 4)))
            __column_5_list.append(int(__cus_excel_op.def_get_cell_value(__i_00 + 2, 5)))
            __column_6_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 6))
            __column_7_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 7))
            __column_8_list.append(int(__cus_excel_op.def_get_cell_value(__i_00 + 2, 8)))
            __column_9_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 9)))
            __column_10_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 10)))

        for __i_01 in range(len(__column_6_list)):
            __queue_empty.put(__column_6_list[__i_01])
        for _ in range(PROCESSNUM):
            __queue_empty.put(None)

    def def_consumer_upload_del(self, __queue_del, __queue_del_retry):
        while True:
            if __queue_del_retry.qsize() != 0:
                __item = __queue_del_retry.get(timeout=1)
                __queue_del_retry.task_done()
                self.def_write_log('upload', f'删除任务进入重传队列 | {__item}')
            elif __queue_del.qsize() != 0:
                __item = __queue_del.get(timeout=1)
                __queue_del.task_done()
            else:
                time.sleep(TIMEOUT)
                continue
            if __item is None or __item == 'None':
                __queue_del.all_tasks_done()
                __queue_del_retry.all_tasks_done()
                break
            try:
                _dic_01, _local_file_path = __item
                # sftpTransport.remove(_localdirpath)
                if os.path.exists(_local_file_path):
                    os.remove(_local_file_path)
                    self.def_write_log('upload', f'上传任务删除本地文件完成 | {_dic_01["文件进度"]}')
            except Exception as err_01:
                self.def_write_log('upload', f'上传任务删除本地文件异常 | {_dic_01["分块进度"]} {err_01}')
                # __queue_del_retry.put(__item)
                time.sleep(TIMEOUT)
                continue

    def def_consumer_upload_move(self, __queue_move, __queue_move_retry):
        while True:
            if __queue_move_retry.qsize() != 0:
                __item = __queue_move_retry.get(timeout=1)
                __queue_move_retry.task_done()
                self.def_write_log('upload', f'移动任务进入重传队列 | {__item}')
            elif __queue_move.qsize() != 0:
                __item = __queue_move.get(timeout=1)
                __queue_move.task_done()
            else:
                time.sleep(TIMEOUT)
                continue
            if __item is None or __item == 'None':
                __queue_move.all_tasks_done()
                __queue_move_retry.all_tasks_done()
                break
            try:
                _dic_01, _local_file_path, _local_done_dir_path = __item
                try:
                    if not os.path.exists(os.path.dirname(_local_done_dir_path)):
                        os.makedirs(os.path.dirname(_local_done_dir_path))
                except Exception as __err_01:
                    self.def_write_log('upload', f'上传任务移动错误本地目录不存在 {_dic_01["文件进度"]} {str(__err_01)}')
                finally:
                    try:
                        shutil.move(_local_file_path, _local_done_dir_path)
                        self.def_write_log('upload', f'上传任务移动完成 | {_dic_01["文件进度"]} | {_local_file_path} | {_local_done_dir_path}')
                    except Exception as __err_02:
                        self.def_write_log('upload', f'上传任务移动未知错误 | {_dic_01["文件进度"]} |  {str(__err_02)}')
                        # __queue_move_retry.put(__item)
            except Exception as err_01:
                self.def_write_log('upload', f'上传任务移动异常需要重传 | {_dic_01["分块进度"]} {err_01}')
                # __queue_move_retry.put(__item)
                time.sleep(TIMEOUT)
                continue

    def def_consumer_upload_empty(self, __queue_empty, __queue_empty_retry):
        while True:
            if __queue_empty_retry.qsize() != 0:
                __item = __queue_empty_retry.get(timeout=1)
                __queue_empty_retry.task_done()
                self.def_write_log('upload', f'清空任务进入重传队列 | {__item}')
            elif __queue_empty.qsize() != 0:
                __item = __queue_empty.get(timeout=1)
                __queue_empty.task_done()
            else:
                time.sleep(TIMEOUT)
                continue
            if __item is None or __item == 'None':
                __queue_empty.all_tasks_done()
                __queue_empty_retry.all_tasks_done()
                break
            try:
                _dir = __item
                self.def_rmdir_local_empty(_dir)
                self.def_write_log('upload', f'上传任务清空本地目录完成 | {_dir}')
            except Exception as err_01:
                self.def_write_log('upload', f'上传任务清空本地目录错误 | {_dir} {err_01}')
                # __queue_empty_retry.put(__item)
                time.sleep(TIMEOUT)
                continue

    @staticmethod
    def def_is_queue_empty(queue):
        try:
            item = queue.get(timeout=1)  # 尝试获取元素，如果队列为空则抛出Empty异常
            # print(item)
            queue.put(item)
            return False  # 如果能获取到元素，说明队列不为空
        except Empty:
            return True  # 如果抛出Empty异常，说明队列为空

    def def_sftp_upload_process(self, _dic_01, _host, _sftpport, _sftpuser, _sftppwd, _local_dir_path, _local_file_path, _remote_dir_path, _local_done_dir_path):
        if os.path.isfile(_local_dir_path):
            _local_dir_path = os.path.dirname(_local_dir_path) + '/'
        _len__local_file_path = len(_local_dir_path)
        __remote_file_path = os.path.join(_remote_dir_path, _local_file_path[_len__local_file_path:]).replace('\\', '/')
        __remote_file_dir_path = os.path.dirname(__remote_file_path)
        __local_done_file_dir_path = os.path.join(_local_done_dir_path, _local_file_path[_len__local_file_path:]).replace('\\', '/')
        try:
            __chunk_size_02 = MAX_PACKET_SIZE  # 例如：每次上传1MB
            __local_file_size_01 = os.path.getsize(_local_file_path)
            # __remote_file_path = os.path.join(os.path.dirname(__remote_file_dir_path), os.path.basename(_local_file_path)).replace('\\', '/')

            __sftpTransport, __sftpClient, __sock = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
            if __sftpTransport is None:
                raise CusSFTPConnectionError(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')
            __sftpTransport.listdir_attr(__remote_file_dir_path)
            with __sftpTransport.open(f'{__remote_file_path}.tmp', 'wb') as __remote_file:
                # remote_file.seek(local_file_size)
                __remote_file.truncate(__local_file_size_01)
            __sftpTransport.chmod(f'{__remote_file_path}.tmp', mode=0o777)
            # self.def_write_log('upload', f'创建临时文件 | {_dic_01["文件进度"]}')
            __sftpTransport.close()

            if __chunk_size_02 > __local_file_size_01:
                __chunk_size_02 = __local_file_size_01
            if __local_file_size_01 == 0:
                _dic_01['删除文件'].update({_local_file_path: ''})
                if _local_done_dir_path != "None":
                    _dic_01['移动文件'].update({_local_file_path: __local_done_file_dir_path})
                _dic_01['重命名文件'].update({__remote_file_path: ''})
                return
            __num_threads_02 = int((__local_file_size_01 + __chunk_size_02 - 1) / __chunk_size_02)  # 至少一个线程，但不超过4个offsets
            __offsets_02 = []
            with open(_local_file_path, 'rb'):
                # 计算每个线程的起始和结束偏移量
                __offsets_02 = [(__i * __chunk_size_02, min((__i + 1) * __chunk_size_02, __local_file_size_01)) for __i in range(__num_threads_02)]

            # 创建并启动线程
            __index_01 = 1
            __dic_04 = {}
            # __pool_01 = Pool(THREADNUM)
            for __i01, (__start01, __end01) in enumerate(__offsets_02):
                __current_process2 = __i01 + 1
                __total_length01 = len(__offsets_02)
                __process_percentage2 = (__current_process2 / __total_length01) * 100
                __current_excel_dir_process_01 = _dic_01['目录进度']
                __current_excel_file_process_01 = _dic_01['文件进度']
                __dic_04.update({'分块进度': f'{__current_excel_dir_process_01} | {__current_excel_file_process_01} | {__total_length01}/{__current_process2} ({__process_percentage2:.2f}%) {__remote_file_path}'})

                __t = Process(target=self.def_sftp_upload_chunk_thread, args=(__dic_04, _host, _sftpport, _sftpuser, _sftppwd, __remote_file_path, _local_file_path, __start01, __end01))
                __t.start()
                if __index_01 == SUBPROCESSNUM or len(__offsets_02) == __index_01:
                    __t.join()
                    # __pool_01.close()
                    # __pool_01.join()
                    # __pool_01 = Pool(THREADNUM)
                    __index_01 = 0
                __index_01 = __index_01 + 1
            _dic_01['删除文件'].update({_local_file_path: ''})
            if _local_done_dir_path != "None":
                _dic_01['移动文件'].update({_local_file_path: __local_done_file_dir_path})
            _dic_01['重命名文件'].update({__remote_file_path: ''})
        except Exception as __err:
            self.def_write_log('upload', f'上传进程错误 | {_dic_01["文件进度"]} |  {str(__err)}')
            try:
                __sftpTransport, __sftpClient, __sock = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
                if __sftpTransport is None:
                    raise CusSFTPConnectionError(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')
                self.def_sftp_mkdir_p(__sftpTransport, __remote_file_dir_path)
                if '__sftpTransport' in locals() and __sftpTransport:
                    __sftpTransport.close()  # 确保连接被关闭
                if '__sock' in locals() and __sock:
                    __sock.close()
                if '__sftpClient' in locals() and __sftpClient:
                    __sftpClient.close()
                self.def_sftp_upload_process(_dic_01, _host, _sftpport, _sftpuser, _sftppwd, _local_dir_path, _local_file_path, _remote_dir_path, _local_done_dir_path)
            except Exception as err02:
                self.def_write_log('upload', f'目录错误 | {_dic_01["文件进度"]} |  {str(err02)}')
            finally:
                if '__sftpTransport' in locals() and __sftpTransport:
                    __sftpTransport.close()  # 确保连接被关闭
                if '__sock' in locals() and __sock:
                    __sock.close()
                if '__sftpClient' in locals() and __sftpClient:
                    __sftpClient.close()
        finally:
            if '__sftpTransport' in locals() and __sftpTransport:
                __sftpTransport.close()  # 确保连接被关闭
            if '__sock' in locals() and __sock:
                __sock.close()
            if '__sftpClient' in locals() and __sftpClient:
                __sftpClient.close()

    def def_sftp_upload_chunk_thread(self, _dic_01, _host, _sftpport, _sftpuser, _sftppwd, _remote_file_path, _local_file_path, _start, _end):
        # print(_host, _sftpport, _sftpuser, _sftppwd, _remotefilepath, _localdirpath, local_file, remote_base_path, start, end)
        try:
            __sftpTransport, __sftpClient, __sock = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
            if __sftpTransport is None:
                raise CusSFTPConnectionError(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')  # 读取文件的一部分

            with open(_local_file_path, 'rb') as __local_file:

                __local_file.seek(_start)
                __chunk_data = __local_file.read(_end - _start)

                # 上传文件部分到SFTP服务器的临时文件
                with __sftpTransport.open(f'{_remote_file_path}.tmp', 'rb+') as __remote_file:
                    __remote_file.seek(_start)
                    __remote_file.write(__chunk_data)
                self.def_write_log('upload', f'分块上传 | {_dic_01["分块进度"]}')
                __sftpTransport.close()
        except Exception as err_01:
            self.def_write_log('upload', f'分块上传错误 | {_dic_01["分块进度"]} {err_01}')
            if '__sftpTransport' in locals() and __sftpTransport:
                __sftpTransport.close()  # 确保连接被关闭
            if '__sock' in locals() and __sock:
                __sock.close()
            if '__sftpClient' in locals() and __sftpClient:
                __sftpClient.close()
            self.def_sftp_upload_chunk_thread(_dic_01, _host, _sftpport, _sftpuser, _sftppwd, _remote_file_path, _local_file_path, _start, _end)
        finally:
            if '__sftpTransport' in locals() and __sftpTransport:
                __sftpTransport.close()  # 确保连接被关闭
            if '__sock' in locals() and __sock:
                __sock.close()
            if '__sftpClient' in locals() and __sftpClient:
                __sftpClient.close()

    def def_sftp_download_process(self, _dic_01, _host, _sftpport, _sftpuser, _sftppwd, _remote_dir_path, _remote_file_path, _local_dir_path, _remote_done_dir_path):
        if os.path.isfile(_remote_dir_path):
            _remote_dir_path = os.path.dirname(_remote_dir_path)
        _len_remote_file_path = len(_remote_dir_path)
        __local_file_path = os.path.join(_local_dir_path, _remote_file_path[_len_remote_file_path:]).replace('\\', '/')
        __local_file_dir_path = os.path.dirname(__local_file_path)
        __remote_done_file_dir_path = os.path.join(_remote_done_dir_path, _remote_file_path[_len_remote_file_path:]).replace('\\', '/')
        try:
            __sftpTransport, __sftpClient, __sock = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
            if __sftpTransport is None:
                raise CusSFTPConnectionError(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')
            __sftp_file_size = __sftpTransport.stat(_remote_file_path).st_size
            __chunk_size_01 = MAX_PACKET_SIZE  # 例如：每次上传1MB
            if not os.path.exists(__local_file_dir_path):
                os.makedirs(__local_file_dir_path)
            with open(f'{__local_file_path}.tmp', "wb") as __open_local_file:
                __open_local_file.truncate(__sftp_file_size)
            os.chmod(f'{__local_file_path}.tmp', 0o777)

            if __chunk_size_01 > __sftp_file_size:
                __chunk_size_01 = __sftp_file_size
            if __sftp_file_size == 0:
                _dic_01['删除文件'].update({_remote_file_path: ''})
                if __remote_done_file_dir_path != "None":
                    _dic_01['移动文件'].update({_remote_file_path: __remote_done_file_dir_path})
                _dic_01['重命名文件'].update({__local_file_path: ''})
                return
            __num_threads_01 = int((__sftp_file_size + __chunk_size_01 - 1) / __chunk_size_01)  # 至少一个线程，但不超过4个offsets
            __offsets_01 = []
            with __sftpTransport.open(_remote_file_path, 'rb'):
                # 计算每个线程的起始和结束偏移量
                __offsets_01 = [(__i * __chunk_size_01, min((__i + 1) * __chunk_size_01, __sftp_file_size)) for __i in range(__num_threads_01)]
            __sftpTransport.close()

            # 创建并启动线程
            __index_01 = 1
            __dic_04 = {}
            for __i01, (__start01, __end01) in enumerate(__offsets_01):
                # __dic_02, _host, _sftpport, _sftpuser, _sftppwd, _remotefilepath, _localdirpath, local_base_path, start, end
                # __t = threading.Thread(target=self.def_sftp_download_chunk_thread, args=(__dic_02, _host, _sftpport, _sftpuser, _sftppwd, _remote_file_path, _local_dir_path, __start01, __end01))
                __current_process2 = __i01 + 1
                __total_length01 = len(__offsets_01)
                __process_percentage2 = (__current_process2 / __total_length01) * 100
                __current_excel_dir_process_01 = _dic_01['目录进度']
                __current_excel_file_process_01 = _dic_01['文件进度']
                __dic_04.update({'分块进度': f'{__current_excel_dir_process_01} | {__current_excel_file_process_01} | {__total_length01}/{__current_process2} ({__process_percentage2:.2f}%) {__local_file_path}'})

                __t = Process(target=self.def_sftp_download_chunk_thread, args=(__dic_04, _host, _sftpport, _sftpuser, _sftppwd, __local_file_path, _remote_file_path, __start01, __end01))

                __t.start()
                if __index_01 == SUBPROCESSNUM or len(__offsets_01) == __index_01:
                    __t.join()
                    # __pool_01.close()
                    # __pool_01.join()
                    # __pool_01 = Pool(THREADNUM)
                    __index_01 = 0
                __index_01 = __index_01 + 1
                # __pool_01.close()
            _dic_01['删除文件'].update({_remote_file_path: ''})
            if __remote_done_file_dir_path != "None":
                _dic_01['移动文件'].update({_remote_file_path: __remote_done_file_dir_path})
            _dic_01['重命名文件'].update({__local_file_path: ''})
        except Exception as __err:
            self.def_write_log('download', f'下载进程错误 | {_dic_01["文件进度"]} |  {str(__err)}')
            if '__sftpTransport' in locals() and __sftpTransport:
                __sftpTransport.close()  # 确保连接被关闭
            if '__sock' in locals() and __sock:
                __sock.close()
            if '__sftpClient' in locals() and __sftpClient:
                __sftpClient.close()
            self.def_sftp_download_process(_dic_01, _host, _sftpport, _sftpuser, _sftppwd, _remote_dir_path, _remote_file_path, _local_dir_path, _remote_done_dir_path)
        finally:
            if '__sftpTransport' in locals() and __sftpTransport:
                __sftpTransport.close()  # 确保连接被关闭
            if '__sock' in locals() and __sock:
                __sock.close()
            if '__sftpClient' in locals() and __sftpClient:
                __sftpClient.close()

    def def_sftp_download_chunk_thread(self, _dic_01, _host, _sftpport, _sftpuser, _sftppwd, _local_file_path, _remote_file_path, _start, _end):
        try:
            # print(_host, _sftpport, _sftpuser, _sftppwd, _remotefilepath, _localdirpath, local_file, remote_base_path, start, end)
            __sftpTransport, __sftpClient, __sock = self.def_sftp_trans_port_connect(_host, _sftpport, _sftpuser, _sftppwd)
            if __sftpTransport is None:
                raise CusSFTPConnectionError(f'无法连接到 {_host}，已尝试 {MAX_RETYIES} 次')
            # 读取文件的一部分

            with __sftpTransport.open(_remote_file_path, 'rb') as __remotepath:
                __remotepath.seek(_start)
                __chunk_data = __remotepath.read(_end - _start)
                # 上传文件部分到SFTP服务器的临时文件
                with open(f'{_local_file_path}.tmp', 'rb+') as __local_file:
                    __local_file.seek(_start)

                    __local_file.write(__chunk_data)
                self.def_write_log('download', f'分块下载 | {_dic_01["分块进度"]}')
        except Exception as __err:
            self.def_write_log('download', f'分块下载错误 | {_dic_01["分块进度"]} | {__err}')
            if '__sftpTransport' in locals() and __sftpTransport:
                __sftpTransport.close()  # 确保连接被关闭
            if '__sock' in locals() and __sock:
                __sock.close()
            if '__sftpClient' in locals() and __sftpClient:
                __sftpClient.close()
            self.def_sftp_download_chunk_thread(_dic_01, _host, _sftpport, _sftpuser, _sftppwd, _local_file_path, _remote_file_path, _start, _end)
        finally:
            if '__sftpTransport' in locals() and __sftpTransport:
                __sftpTransport.close()  # 确保连接被关闭
            if '__sock' in locals() and __sock:
                __sock.close()
            if '__sftpClient' in locals() and __sftpClient:
                __sftpClient.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='zabbix  api ', usage='%(prog)s [options]')
    # ![]
    parser.add_argument('-sftpupload_20240524', nargs='?', metavar='无参数', dest='sftpupload_20240524',
                        default='sftpupload_20240524',
                        help=u"sftp上传")
    parser.add_argument('-sftpupload', nargs='?', metavar='无参数', dest='sftpupload',
                        default='su',
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
        if args.sftpupload_20240524 != 'sftpupload_20240524':
            __cus_excel_op.def_load_excel(file='/etc/zabbix/scripts/fileTransport.xlsx', index=1)
            __column_1_list = __cus_excel_op.def_get_col_value(1)
            del __column_1_list[0]
            __column_2_list = []  # 协议
            __column_3_list = []  # 用户名
            __column_4_list = []  # 密码
            __column_5_list = []  # 端口
            __column_6_list = []  # 6_本地文件或目录
            __column_7_list = []  # 7_上传目录
            __column_8_list = []  # 8_上传文件数
            __column_9_list = []  # 9_是否删除源文件
            __column_10_list = []  # 10_上传完成后移动到目录
            for __i_00 in range(len(__column_1_list)):
                __column_2_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 2))
                __column_3_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 3))
                __column_4_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 4)))
                __column_5_list.append(int(__cus_excel_op.def_get_cell_value(__i_00 + 2, 5)))
                __column_6_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 6))
                __column_7_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 7))
                __column_8_list.append(int(__cus_excel_op.def_get_cell_value(__i_00 + 2, 8)))
                __column_9_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 9)))
                __column_10_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 10)))

            for __i_01 in range(len(__column_6_list)):
                __lv_list_all_file_tmp = __cus_file_trans_port.def_get_os_file_list_find_local(__column_6_list[__i_01], __column_8_list[__i_01], FILEFLAG)
                __lv_list_all_file = list(filter(None, __lv_list_all_file_tmp))
                # __lv_list_all_file = []
                # __cus_file_trans_port.def_get_os_file_list(__column_6_list[__i_01], __lv_list_all_file, __column_8_list[__i_01], FILEFLAG)
                __chunk_size_03 = PROCESSNUM
                __local_file_size_02 = len(__lv_list_all_file)

                __current_excel_dir_process = __i_01 + 1
                __total_excel_dir_length = len(__column_6_list)
                __process_excel_dir_percentage = (__current_excel_dir_process / __total_excel_dir_length) * 100

                if __local_file_size_02 == 0:
                    __current_dir_name = __column_6_list[__i_01]
                    __cus_file_trans_port.def_write_log('upload', f'上传 | {__total_excel_dir_length}/{__current_excel_dir_process} ({__process_excel_dir_percentage:.2f}%) {__current_dir_name} | 文件不存在或目录为空')
                __num_threads_03 = int((__local_file_size_02 + __chunk_size_03 - 1) / __chunk_size_03)
                __offsets_03 = []
                for __i_02 in range(__num_threads_03):
                    if __i_02 == __num_threads_03 - 1:
                        __offsets_03.append((__i_02 * __chunk_size_03, len(__lv_list_all_file)))
                    else:
                        __offsets_03.append((__i_02 * __chunk_size_03, min((__i_02 + 1) * __chunk_size_03, (__i_02 + 9) * __chunk_size_03)))

                __process_put_list01 = []
                __process_mov_list01 = []
                __process_del_list01 = []
                __dic_del_file_list = Manager().dict()
                __dic_rename_file_list = Manager().dict()
                __dic_mov_file_list = Manager().dict()
                for __i_03, (__start, __end) in enumerate(__offsets_03):
                    __dic_01 = {}
                    __dic_01.update({'删除文件': __dic_del_file_list,
                                     '移动文件': __dic_mov_file_list,
                                     '重命名文件': __dic_rename_file_list,
                                     '目录进度': f'{__total_excel_dir_length}/{__current_excel_dir_process} ({__process_excel_dir_percentage:.2f}%) {__column_6_list[__i_01]} {__column_7_list[__i_01]}',
                                     })
                    try:
                        for __i_04 in range(__start, __end):
                            __current_upload_file_process = __i_04 + 1
                            __total_upload_file_length = __local_file_size_02
                            __process_upload_file_percentage = (__current_upload_file_process / __total_upload_file_length) * 100
                            __dic_01.update({
                                '文件进度': f'{__total_upload_file_length}/{__current_upload_file_process} ({__process_upload_file_percentage:.2f}%) {__lv_list_all_file[__i_04]}',
                            })
                            __p = Process(target=__cus_file_trans_port.def_sftp_upload_process, args=(__dic_01, __column_1_list[__i_01], __column_5_list[__i_01], __column_3_list[__i_01],
                                                                                                      __column_4_list[__i_01], __column_6_list[__i_01], __lv_list_all_file[__i_04],
                                                                                                      __column_7_list[__i_01], __column_10_list[__i_01]))
                            __p.start()
                            __process_put_list01.append(__p)
                        for __i_05 in __process_put_list01:
                            __i_05.join()
                    except Exception as err:
                        __cus_file_trans_port.def_write_log('upload', f'上传主进程错误 | {__column_6_list[__i_01]} |  {str(err)}')

                __index = 1
                for __i_06, (key, value) in enumerate(__dic_rename_file_list.items()):
                    __dic_03 = {}
                    __current_process = __i_06 + 1
                    __total_length = len(__dic_rename_file_list.keys())
                    __process_percentage = (__current_process / __total_length) * 100
                    __dic_03.update({'文件进度': f'{__total_length}/{__current_process} ({__process_percentage:.2f}%)'})
                    __p02 = Process(target=__cus_file_trans_port.def_rename_remote_tmp_files_thread, args=(__dic_03, __column_1_list[__i_01], __column_5_list[__i_01], __column_3_list[__i_01],
                                                                                                           __column_4_list[__i_01], __column_6_list[__i_01], key, __column_7_list[__i_01]))
                    __p02.start()
                    if __index == PROCESSNUM or len(__dic_rename_file_list.items()) == __index:
                        __p02.join()
                        __index = 1
                    __index = __index + 1

                if __column_9_list[__i_01] == '否':
                    __index = 1
                    for __i_06, (key, value) in enumerate(__dic_mov_file_list.items()):
                        __dic_03 = {}
                        __current_process = __i_06 + 1
                        __total_length = len(__dic_mov_file_list.keys())
                        __process_percentage = (__current_process / __total_length) * 100
                        __dic_03.update({'文件进度': f'{__total_length}/{__current_process} ({__process_percentage:.2f}%)'})
                        __p02 = Process(target=__cus_file_trans_port.def_move_local_file_process, args=(__dic_03, key, value))
                        __p02.start()
                        if __index == PROCESSNUM or len(__dic_mov_file_list.items()) == __index:
                            __p02.join()
                            __index = 1
                        __index = __index + 1

                if __column_9_list[__i_01] == '否':
                    __dic_del_file_list = {}
                __index_01 = 1
                for __i_08, (key) in enumerate(__dic_del_file_list.keys()):
                    __dic_02 = {}
                    __current_process = __i_08 + 1
                    __total_length = len(__dic_del_file_list.keys())
                    __process_percentage = (__current_process / __total_length) * 100
                    __dic_02.update({'文件进度': f'{__total_length}/{__current_process} ({__process_percentage:.2f}%) {key}'})
                    __p03 = Process(target=__cus_file_trans_port.def_delete_os_files, args=(__dic_02, key))
                    __p03.start()
                    if __index_01 == PROCESSNUM or len(__dic_del_file_list.keys()) == __index_01:
                        __p03.join()
                        __index_01 = 0
                    __index_01 = __index_01 + 1

            __index_01 = 1
            for __i_01 in range(len(__column_6_list)):
                __p03 = Process(target=__cus_file_trans_port.def_rmdir_local_empty, args=(__column_6_list[__i_01],))
                __p03.start()
                if __index_01 == PROCESSNUM or len(__column_6_list) == __index_01:
                    __p03.join()
                    __index_01 = 0
                __index_01 = __index_01 + 1

        if args.sftpdownload != 'sftpdownload':
            __cus_excel_op.def_load_excel(file='/etc/zabbix/scripts/fileTransport.xlsx', index=2)

            __column_1_list = __cus_excel_op.def_get_col_value(1)  # IP地址
            del __column_1_list[0]
            __column_2_list = []  # 协议
            __column_3_list = []  # 用户名
            __column_4_list = []  # 密码
            __column_5_list = []  # 端口
            __column_6_list = []  # 6_远端文件或目录
            __column_7_list = []  # 7_下载目录
            __column_8_list = []  # 8_下载文件数
            __column_9_list = []  # 9_是否删除远端文件
            __column_10_list = []  # 10_下载完成后远端文件移动到目录
            for __i_00 in range(len(__column_1_list)):
                __column_2_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 2))  #
                __column_3_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 3))
                __column_4_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 4)))
                __column_5_list.append(int(__cus_excel_op.def_get_cell_value(__i_00 + 2, 5)))
                __column_6_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 6))
                __column_7_list.append(__cus_excel_op.def_get_cell_value(__i_00 + 2, 7))
                __column_8_list.append(int(__cus_excel_op.def_get_cell_value(__i_00 + 2, 8)))
                __column_9_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 9)))
                __column_10_list.append(str(__cus_excel_op.def_get_cell_value(__i_00 + 2, 10)))

            for __i_01 in range(len(__column_6_list)):
                __lv_list_all_file_tmp = list(filter(None, __cus_file_trans_port.def_get_os_file_list_find_remote(__column_1_list[__i_01], __column_5_list[__i_01], __column_3_list[__i_01], __column_4_list[__i_01],
                                                                                                                  __column_6_list[__i_01], __column_8_list[__i_01], FILEFLAG)))
                __lv_list_all_file = list(filter(None, __lv_list_all_file_tmp))
                __current_excel_dir_process = __i_01 + 1
                __total_excel_dir_length = len(__column_6_list)
                __process_excel_dir_percentage = (__current_excel_dir_process / __total_excel_dir_length) * 100

                __chunk_size_04 = PROCESSNUM
                __local_file_size_03 = len(__lv_list_all_file)
                if __local_file_size_03 == 0:
                    __current_dir_name = __column_6_list[__i_01]
                    __cus_file_trans_port.def_write_log('download', f'下载 | {__total_excel_dir_length}/{__current_excel_dir_process} ({__process_excel_dir_percentage:.2f}%) {__current_dir_name} | 文件不存在或目录为空')
                __num_threads_04 = int((__local_file_size_03 + __chunk_size_04 - 1) / __chunk_size_04)
                __offsets_04 = []
                for __i_02 in range(__num_threads_04):
                    if __i_02 == __num_threads_04 - 1:
                        __offsets_04.append((__i_02 * __chunk_size_04, len(__lv_list_all_file)))
                    else:
                        __offsets_04.append((__i_02 * __chunk_size_04, min((__i_02 + 1) * __chunk_size_04, (__i_02 + 9) * __chunk_size_04)))
                __process_put_list01 = []
                __process_mov_list01 = []
                __process_del_list01 = []
                __dic_del_file_list = Manager().dict()
                __dic_rename_file_list = Manager().dict()
                __dic_mov_file_list = Manager().dict()
                for __i_03, (__start, __end) in enumerate(__offsets_04):
                    __dic_01 = {}
                    __current_excel_dir_process = __i_01 + 1
                    __total_excel_dir_length = len(__column_6_list)
                    __process_excel_dir_percentage = (__current_excel_dir_process / __total_excel_dir_length) * 100
                    __dic_01.update({'删除文件': __dic_del_file_list,
                                     '移动文件': __dic_mov_file_list,
                                     '重命名文件': __dic_rename_file_list,
                                     '目录进度': f'{__total_excel_dir_length}/{__current_excel_dir_process} ({__process_excel_dir_percentage:.2f}%) {__column_6_list[__i_01]} {__column_7_list[__i_01]}',
                                     })
                    try:
                        for __i_04 in range(__start, __end):
                            # _host, _sftpport, _sftpuser, _sftppwd, _localdirpath, _remotefilepath
                            if __column_10_list[__i_01] != 'None':
                                if __dic_mov_file_list.get(__lv_list_all_file[__i_04], None) is None:
                                    __dic_mov_file_list.update({__lv_list_all_file[__i_04]: [{__column_10_list[__i_01]: ''}]})
                                else:
                                    __dic_mov_file_list[__lv_list_all_file[__i_04]].append({__column_10_list[__i_01]: ''})
                            __current_upload_file_process = __i_04 + 1
                            __total_upload_file_length = __local_file_size_03
                            __process_upload_file_percentage = (__current_upload_file_process / __total_upload_file_length) * 100
                            __dic_01.update({
                                '文件进度': f'{__total_upload_file_length}/{__current_upload_file_process} ({__process_upload_file_percentage:.2f}%) {__lv_list_all_file[__i_04]}',
                            })
                            __p = Process(target=__cus_file_trans_port.def_sftp_download_process, args=(__dic_01, __column_1_list[__i_01], __column_5_list[__i_01], __column_3_list[__i_01],
                                                                                                        __column_4_list[__i_01], __column_6_list[__i_01], __lv_list_all_file[__i_04],
                                                                                                        __column_7_list[__i_01], __column_10_list[__i_01]))
                            # __p04 = Process(target=__cus_file_trans_port.def_sftp_download_process, args=(__dic_01, __column_1_list[__i_01], __column_5_list[__i_01], __column_3_list[__i_01],
                            #                                                                             __column_4_list[__i_01], __lv_list_all_file[__i_04],
                            #                                                                             __column_7_list[__i_01]))
                            __p.start()
                            # __p04.start()
                            __process_put_list01.append(__p)
                        for __i_05 in __process_put_list01:
                            __i_05.join()
                    except Exception as err:
                        __cus_file_trans_port.def_write_log('download', f'下载主进程错误 | {__column_6_list[__i_01]} |  {str(err)}')

                if __column_9_list[__i_01] == '否':
                    __index = 1
                    for __i_06, (key, value) in enumerate(__dic_rename_file_list.items()):
                        __dic_03 = {}
                        __current_process = __i_06 + 1
                        __total_length = len(__dic_rename_file_list.keys())
                        __process_percentage = (__current_process / __total_length) * 100
                        __dic_03.update({'文件进度': f'{__total_length}/{__current_process} ({__process_percentage:.2f}%)'})
                        __p02 = Process(target=__cus_file_trans_port.def_rename_local_tmp_files_thread, args=(__dic_03, __column_6_list[__i_01], key, __column_7_list[__i_01]))
                        __p02.start()
                        if __index == PROCESSNUM or len(__dic_rename_file_list.items()) == __index:
                            __p02.join()
                            __index = 1
                        __index = __index + 1

                if __column_9_list[__i_01] == '否':
                    __index = 1
                    for __i_06, (key, value) in enumerate(__dic_mov_file_list.items()):
                        __dic_03 = {}
                        __current_process = __i_06 + 1
                        __total_length = len(__dic_mov_file_list.keys())
                        __process_percentage = (__current_process / __total_length) * 100
                        __dic_03.update({'文件进度': f'{__total_length}/{__current_process} ({__process_percentage:.2f}%)'})
                        __p02 = Process(target=__cus_file_trans_port.def_move_remote_files_thread, args=(__dic_03, __column_1_list[__i_01], __column_5_list[__i_01], __column_3_list[__i_01],
                                                                                                         __column_4_list[__i_01], key, value))
                        __p02.start()
                        if __index == PROCESSNUM or len(__dic_mov_file_list.items()) == __index:
                            __p02.join()
                            __index = 1
                        __index = __index + 1

                if __column_9_list[__i_01] == '否':
                    __dic_del_file_list = {}
                __index = 1
                for __i_08, (key) in enumerate(__dic_del_file_list.keys()):
                    __dic_02 = {}
                    __current_process = __i_08 + 1
                    __total_length = len(__dic_del_file_list.keys())
                    __process_percentage = (__current_process / __total_length) * 100
                    __dic_02.update({'文件进度': f'{__total_length}/{__current_process} ({__process_percentage:.2f}%) {key}'})
                    __p03 = Process(target=__cus_file_trans_port.def_delete_remote_files, args=(__column_1_list[__i_01], __column_5_list[__i_01], __column_3_list[__i_01],
                                                                                                __column_4_list[__i_01], __dic_02, key))
                    __p03.start()
                    if __index == PROCESSNUM or __index == len(__dic_del_file_list.keys()):
                        __p03.join()
                        __index = 1
                    __index = __index + 1

            __index_01 = 1
            for __i_01 in range(len(__column_6_list)):
                __p03 = Process(target=__cus_file_trans_port.def_rmdir_remote_empty, args=(__column_1_list[__i_01], __column_5_list[__i_01], __column_3_list[__i_01],
                                                                                           __column_4_list[__i_01], __column_6_list[__i_01]))
                __p03.start()
                if __index_01 == PROCESSNUM or len(__column_6_list) == __index_01:
                    __p03.join()
                    __index_01 = 0
                __index_01 = __index_01 + 1

        # ![PROCESSNUM参数调整最大并发数]
        # ![MAX_PACKET_SIZE参数调整文件切块大小]
        if args.sftpupload != 'sftpupload':
            with Manager() as __manger:
                __dic_manager = __manger.dict()
                __queue = Manager().Queue(maxsize=QUEUEMAXSIZE)
                __queue_retry = Manager().Queue()
                try:
                    with Pool(processes=PROCESSNUM) as __pool_consumer_upload:
                        __async_results = []
                        for _ in range(PROCESSNUM):
                            __async_result = __pool_consumer_upload.apply_async(func=__cus_file_trans_port.def_consumer_upload, args=(__queue, __queue_retry))
                            __async_results.append(__async_result)
                        __cus_file_trans_port.def_producer_upload(__queue, __dic_manager)
                        # __queue_retry.join()
                        # __queue.join()
                        for __async_result in __async_results:
                            __async_result.wait()
                except Exception as __err_p:
                    __cus_file_trans_port.def_write_log('upload', f'主进程生产消费队列异常 | {__err_p}')

                __queue_rename = Manager().Queue(maxsize=QUEUEMAXSIZE)
                __queue_rename_retry = Manager().Queue()
                try:
                    with Pool(processes=PROCESSNUM) as __pool_consumer_upload_rename:
                        __async_results = []
                        for _ in range(PROCESSNUM):
                            __async_result = __pool_consumer_upload_rename.apply_async(func=__cus_file_trans_port.def_consumer_upload_rename, args=(__queue_rename, __queue_rename_retry))
                            __async_results.append(__async_result)
                        __cus_file_trans_port.def_producer_upload_rename(__queue_rename, __dic_manager)
                        # __queue_rename_retry.join()
                        # __queue_rename.join()
                        for __async_result in __async_results:
                            __async_result.wait()
                except Exception as __err_p:
                    __cus_file_trans_port.def_write_log('upload', f'主进程重命名队列异常 | {__err_p}')

                __queue_del = Manager().Queue(maxsize=QUEUEMAXSIZE)
                __queue_del_retry = Manager().Queue()
                try:
                    with Pool(processes=PROCESSNUM) as __pool_consumer_upload_del:
                        __async_results = []
                        for _ in range(PROCESSNUM):
                            __async_result = __pool_consumer_upload_del.apply_async(func=__cus_file_trans_port.def_consumer_upload_del, args=(__queue_del, __queue_del_retry))
                            __async_results.append(__async_result)
                        __cus_file_trans_port.def_producer_upload_del(__queue_del, __dic_manager)
                        # __queue_del_retry.join()
                        # __queue_del.join()
                        for __async_result in __async_results:
                            __async_result.wait()
                except Exception as __err_p:
                    __cus_file_trans_port.def_write_log('upload', f'主进程删除队列异常 | {__err_p}')

                __queue_move = Manager().Queue(maxsize=QUEUEMAXSIZE)
                __queue_move_retry = Manager().Queue()
                try:
                    with Pool(processes=PROCESSNUM) as __pool_consumer_upload_move:
                        __async_results = []
                        for _ in range(PROCESSNUM):
                            __async_result = __pool_consumer_upload_move.apply_async(func=__cus_file_trans_port.def_consumer_upload_move, args=(__queue_move, __queue_move_retry))
                            __async_results.append(__async_result)
                        __cus_file_trans_port.def_producer_upload_move(__queue_move, __dic_manager)
                        # __queue_move_retry.join()
                        # __queue_move.join()
                        for __async_result in __async_results:
                            __async_result.wait()
                except Exception as __err_p:
                    __cus_file_trans_port.def_write_log('upload', f'主进程移动队列异常 | {__err_p}')

                __queue_empty = Manager().Queue(maxsize=QUEUEMAXSIZE)
                __queue_empty_retry = Manager().Queue()
                try:
                    with Pool(processes=PROCESSNUM) as __pool_consumer_upload_empty:
                        __async_results = []
                        for _ in range(PROCESSNUM):
                            __async_result = __pool_consumer_upload_empty.apply_async(func=__cus_file_trans_port.def_consumer_upload_empty, args=(__queue_empty, __queue_empty_retry))
                            __async_results.append(__async_result)
                        __cus_file_trans_port.def_producer_upload_empty(__queue_empty)
                        # __queue_empty_retry.join()
                        # __queue_empty.join()
                        for __async_result in __async_results:
                            __async_result.wait()
                except Exception as __err_p:
                    __cus_file_trans_port.def_write_log('upload', f'主进程清空队列异常 | {__err_p}')
