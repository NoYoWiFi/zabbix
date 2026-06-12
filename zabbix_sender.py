#!/etc/zabbix/venv_centos8/bin/python3
### !/etc/zabbix/venv_centos7/bin/python3
# -*- coding: utf-8 -*-

import argparse
import inspect
import logging
import logging.handlers
import json
import socket
import threading
from openpyxl.utils import get_column_letter, column_index_from_string
from typing import Optional, List, Dict, Union, Any
from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from datetime import datetime
import os
from ping3 import ping
import paramiko
import re
import subprocess
import sys
import telnetlib
import time
import traceback
from stat import S_ISDIR as isdir
from concurrent.futures import ThreadPoolExecutor, as_completed, wait

import requests
from requests.adapters import HTTPAdapter
from urllib.parse import urlencode

# python3 -m pip install --upgrade pip
# pip3 install openpyxl paramiko requests
# pip3 install  cryptography==3.4.8
# telnet ./zabbix_sender.py --type='telnet' --ip='172.169.10.10' --port='23' --user='admin' --pwd='admin123' --host="test" --discovery
# ssh ./zabbix_sender.py  --type='ssh' --ip='127.0.0.1' --port='22' --user='root' --pwd='123.com' --host="test" --discovery
# web ./zabbix_sender.py  --type='web' --url_schoolid='2c9f83fd6cc8d788016ccc71706b01de' --url_userid='000000082702' --url_pwd='1f82c942befda29b6ed487a51da199f78fce7f05' --url_http='http://testwww.qlzhy.com/trade-web/login/login.do' --host="test" --discovery
# web ./zabbix_sender.py  --type='web' --url_schoolid='' --url_userid='Admin' --url_pwd='zabbix' --url_http='http://172.169.10.4/api_jsonrpc.php' --host="test" --discovery
# linux ./zabbix_sender.py  --type='linux' --host="test" --discovery
# Create log-object


LOG_FILENAME = "/tmp/stateTmpFile.log"
# sys.argv[5] contain this string "--storage_name=<storage_name_in_zabbix>". List slicing delete this part "--storage_name="
STORAGE_NAME = ''
if len(sys.argv) > 2:
    STORAGE_NAME = sys.argv[2][9:]
    # Set handler
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=(1024 ** 2) * 10, backupCount=5)
    formatter = logging.Formatter('{0} - %(asctime)s - %(name)s - %(levelname)s - %(message)s'.format(STORAGE_NAME))
    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)
    # Set formatter for handler
    handler.setFormatter(formatter)
    # Add handler to log-object
    logger.addHandler(handler)
XLSX_FILENAME = '/tmp/zabbix_sender.xlsx'
SERVER_IP = '127.0.0.1'
SERVER_PORT = '10051'

GV_CPU_COUNT = os.cpu_count()

TIMESTAMPNOW = None


class CusExcelOp:
    """增强版Excel操作类，提供更安全、高效的Excel文件操作"""

    def __init__(self):
        """初始化Excel操作对象"""
        self._source_file: Optional[str] = None
        self._workbook: Optional[Workbook] = None  # 统一管理 Workbook（加载或新建）
        self._worksheet: Optional[Worksheet] = None  # 当前操作的工作表
        self._cached_dimensions: Optional[Dict[str, int]] = None
        self._last_accessed: Optional[datetime] = None

    # --------------------------
    # 文件加载与基础操作
    # --------------------------
    def load_excel(self, file_path: str, sheet_index: int = 1) -> None:
        """
        加载Excel文件并指定工作表

        参数:
            file_path: Excel文件路径
            sheet_index: 工作表索引(从1开始)

        异常:
            ValueError: 如果索引无效或文件不存在
            IOError: 如果文件无法读取
        """
        if sheet_index < 1:
            raise ValueError("工作表索引必须大于等于1")

        try:
            self._source_file = file_path
            self._workbook = load_workbook(file_path, data_only=True)  # 加载到 _workbook
            sheet_names = self._workbook.sheetnames
            self._worksheet = self._workbook[sheet_names[sheet_index - 1]]  # 设置当前工作表
            self._update_cache()
        except Exception as e:
            logger.error(f"加载Excel文件失败: {str(e)}")
            raise IOError(f"无法读取文件: {file_path}") from e

    def _update_cache(self) -> None:
        """更新缓存数据"""
        if self._worksheet:
            self._cached_dimensions = {
                'rows': self._worksheet.max_row,
                'columns': self._worksheet.max_column
            }
        self._last_accessed = datetime.now()

    # --------------------------
    # 工作表操作
    # --------------------------
    def clear_worksheet(self,
                        sheet_name: Optional[str] = None,
                        preserve_headers: bool = True,
                        preserve_attributes: bool = True) -> None:
        """
        安全清空工作表内容

        参数:
            sheet_name: 目标工作表名称(默认当前工作表)
            preserve_headers: 是否保留标题行
            preserve_attributes: 是否保留工作表属性

        异常:
            ValueError: 如果工作表不存在
        """
        target_ws = self._get_worksheet(sheet_name)

        # 保留标题行
        start_row = 2 if preserve_headers and target_ws.max_row > 1 else 1

        try:
            target_ws.delete_rows(start_row, target_ws.max_row)
            logger.info(f"已清空工作表: {target_ws.title}")
        except Exception as e:
            logger.error(f"清空工作表失败: {str(e)}")
            raise RuntimeError("清空操作失败") from e

    def _get_worksheet(self, sheet_name: Optional[str] = None) -> Worksheet:
        """获取工作表对象(带验证)"""
        if sheet_name:
            if sheet_name not in self._workbook.sheetnames:
                raise ValueError(f"工作表 '{sheet_name}' 不存在")
            return self._workbook[sheet_name]
        return self._worksheet or self._workbook.active

    # --------------------------
    # 创建和保存操作
    # --------------------------
    def create_new_workbook(self, sheet_name: str = None, titles: List[str] = None) -> None:
        """
        创建新工作簿

        参数:
            sheet_name: 初始工作表名称
            titles: 标题行内容
        """
        """创建新工作簿（不再需要 _create_wb，直接使用 _workbook）"""
        self._workbook = Workbook()  # 新建工作簿，存入 _workbook
        if sheet_name:
            self.create_sheet(sheet_name, titles)  # 调用 create_sheet

    def create_sheet(self, sheet_name: str, titles: List[str] = None) -> None:
        """
        创建工作表并设置标题

        参数:
            sheet_name: 工作表名称
            titles: 标题行内容
        """
        if not self._workbook:
            self.create_new_workbook()  # 如果没有工作簿，先创建

        self._worksheet = self._workbook.create_sheet(sheet_name)  # 创建并激活
        if titles:
            self.set_row_values(1, titles)  # 写入标题

    def activate_sheet(self, sheet_name: str) -> None:
        """激活指定名称的工作表（如果存在）"""
        self._worksheet = self._get_worksheet(sheet_name)

    def _get_actual_dimensions(self) -> Dict[str, int]:
        """
        获取当前工作表的数据范围（遇到空行/空列停止计算）

        返回:
            {"rows": 实际行数, "columns": 实际列数}

        异常:
            RuntimeError: 如果没有激活的工作表
        """
        if self._worksheet is None:
            raise RuntimeError("没有激活的工作表")

        # 初始化行列计数器
        max_row = 0
        max_col = 0

        # 检查行（从上到下，遇到空行停止）
        for row in self._worksheet.iter_rows():
            if all(cell.value is None for cell in row):  # 如果整行为空，停止计数
                break
            max_row += 1

        # 检查列（从左到右，遇到空列停止）
        for col in self._worksheet.iter_cols():
            if all(cell.value is None for cell in col):  # 如果整列为空，停止计数
                break
            max_col += 1

        return {"rows": max_row, "columns": max_col}

    def get_dimensions(self, skip_empty: bool = True) -> Dict[str, int]:
        if skip_empty:
            return self._get_actual_dimensions()
        return {
            "rows": self._worksheet.max_row,
            "columns": self._worksheet.max_column
        }

    def save_workbook(self, file_path: str) -> None:
        """
        保存工作簿到文件

        参数:
            file_path: 目标文件路径

        异常:
            IOError: 如果保存失败
        """
        """保存工作簿（直接使用 _workbook）"""
        if not self._workbook:
            raise RuntimeError("没有可保存的工作簿")

        try:
            # 删除默认创建的 "Sheet"（如果有）
            if 'Sheet' in self._workbook.sheetnames:
                del self._workbook['Sheet']

            self._workbook.save(file_path)
            logger.info(f"文件已保存到: {file_path}")
        except Exception as e:
            logger.error(f"保存文件失败: {str(e)}")
            raise IOError("文件保存失败") from e

    # --------------------------
    # 数据读取操作
    # --------------------------
    def get_cell_value(self, row: int, column: Union[int, str]) -> Any:
        """
        获取单元格值(支持列字母和数字)

        参数:
            row: 行号(从1开始)
            column: 列号(数字)或列字母(如'A')

        返回:
            单元格值

        异常:
            ValueError: 如果坐标无效
        """
        col_idx = self._convert_column(column)
        self._validate_coordinates(row, col_idx)

        return self._worksheet.cell(row=row, column=col_idx).value

    def get_column_values(self, column: Union[int, str],
                          skip_empty: bool = True,
                          skip_header: bool = False) -> List[Any]:
        """
        获取整列数据，遇到空行则停止读取

        参数:
            column: 列号(数字)或列字母
            skip_empty: 是否跳过空值
            skip_header: 是否跳过标题行

        返回:
            列值列表
        """
        col_idx = self._convert_column(column)
        start_row = 2 if skip_header else 1

        values = []
        for row in range(start_row, self._worksheet.max_row + 1):
            value = self._worksheet.cell(row=row, column=col_idx).value

            # 检查整行是否为空
            is_row_empty = True
            for col in range(1, self._worksheet.max_column + 1):
                if self._worksheet.cell(row=row, column=col).value is not None:
                    is_row_empty = False
                    break

            # 如果遇到空行则停止
            if is_row_empty:
                break

            # 处理当前单元格值
            if not skip_empty or value is not None:
                values.append(value)

        return values

    def get_row_values(self, row: int) -> List[Any]:
        """
        获取整行数据

        参数:
            row: 行号(从1开始)

        返回:
            行值列表
        """
        return [cell.value for cell in self._worksheet[row]]

    # --------------------------
    # 数据写入操作
    # --------------------------
    def set_cell_value(self, row: int, column: Union[int, str], value: Any) -> None:
        """
        设置单元格值

        参数:
            row: 行号
            column: 列号(数字)或列字母
            value: 要设置的值
        """
        col_idx = self._convert_column(column)
        self._validate_coordinates(row, col_idx)

        try:
            self._worksheet.cell(row=row, column=col_idx).value = value
        except Exception as e:
            logger.warning(f"设置单元格({row},{col_idx})失败: {str(e)}")
            self._worksheet.cell(row=row, column=col_idx).value = str(e)

    def set_row_values(self, row: int, values: List[Any]) -> None:
        """
        设置整行数据

        参数:
            row: 行号
            values: 值列表
        """
        for col, value in enumerate(values, start=1):
            self.set_cell_value(row, col, value)

    # --------------------------
    # 工具方法
    # --------------------------
    def _convert_column(self, column: Union[int, str]) -> int:
        """转换列标识为数字索引"""
        if isinstance(column, str):
            try:
                return column_index_from_string(column)
            except ValueError:
                raise ValueError(f"无效的列标识: {column}")
        return column

    def _validate_coordinates(self, row: int, column: int) -> None:
        """验证行列坐标是否有效"""
        if row < 1 or column < 1:
            raise ValueError(f"无效的行列坐标: ({row}, {column})")

        if self._worksheet is None:
            raise RuntimeError("没有活动的工作表")

    # --------------------------
    # 高级功能
    # --------------------------
    def process_time_column(self,
                            column: Union[int, str],
                            sort_only: bool = False,
                            format_only: bool = False) -> None:
        """
        处理时间列(排序/格式化)

        参数:
            column: 目标列(列字母如'A'或列号如1)
            sort_only: 仅排序
            format_only: 仅格式化

        异常:
            ValueError: 如果参数冲突
            RuntimeError: 如果处理失败
        """
        if sort_only and format_only:
            raise ValueError("不能同时指定sort_only和format_only")

        if self._worksheet is None:
            raise RuntimeError("没有活动的工作表")

        col_idx = self._convert_column(column)

        try:
            # 收集数据（明确指定数据范围）
            max_row = self._worksheet.max_row
            rows_data = []

            # 读取所有行数据
            for row in self._worksheet.iter_rows(min_row=1, max_row=max_row):
                cell = row[col_idx - 1]
                rows_data.append({
                    'full_row': [cell.value for cell in row],
                    'sort_value': cell.value if cell.value is not None else 0,
                    'row_num': row[0].row
                })

            if not rows_data:
                return  # 没有数据可处理

            # 处理数据
            header = rows_data[0]
            data_rows = rows_data[1:]

            if not format_only:
                # 使用第一个方法的排序逻辑
                def sort_key(item):
                    value = item['sort_value']
                    # 将-999和"异常"都排在最前面
                    if value == -999 or (isinstance(value, str) and value == "异常"):
                        return (0,)
                    else:
                        return (1, -value if isinstance(value, (int, float)) else 0)

                data_rows = sorted(data_rows, key=sort_key)

            # 清空并重写数据（从第二行开始）
            self.clear_worksheet(preserve_headers=True)

            # 写入标题行
            self.set_row_values(1, header['full_row'])

            # 写入处理后的数据（从第二行开始，使用连续行号）
            for i, row_data in enumerate(data_rows, start=2):
                processed_row = row_data['full_row']
                if not sort_only:
                    # 处理目标列的值
                    cell_value = processed_row[col_idx - 1]
                    if not (isinstance(cell_value, str) and cell_value == "异常"):
                        processed_row[col_idx - 1] = self._format_time_value(
                            cell_value if cell_value is not None else 0
                        )
                self.set_row_values(i, processed_row)

        except Exception as e:
            logger.error(f"处理时间列失败: {str(e)}")
            raise RuntimeError(f"时间列处理失败: {str(e)}") from e

    @staticmethod
    def _format_time_value(value: Any) -> str:
        """格式化时间值（优先使用CusLocalMethod.format_time）"""
        if value == "异常":
            return value
        try:
            # 优先使用CusLocalMethod.format_time
            if hasattr(CusLocalMethod, 'format_time'):
                return CusLocalMethod.format_time(value if value is not None else 0)
            # 后备方案
            return str(value) if value else ""
        except Exception:
            return "异常"

    @property
    def worksheet(self):
        return self._worksheet

    def get_active_sheet_name(self) -> str:
        """
        获取当前激活的工作表名称

        返回:
            str: 当前工作表的名称

        异常:
            RuntimeError: 如果没有激活的工作表
        """
        if self._worksheet is None:
            raise RuntimeError("没有激活的工作表")
        return self._worksheet.title


class CusTelnetClient(object):
    def __init__(self, ):
        self.zabbix_sender = CusZabbixSender()
        self.tn = telnetlib.Telnet()
        self.cus_excel_op = CusExcelOp()
        self.cus_excel_op.create_new_workbook()
        self.value = None
        self.cus_localMethord = CusLocalMethod()
        self.cus_zabbixSender = CusZabbixSender()
        self.lv_dic01 = {}

    def def_connect_dispower(self, funcIp):
        try:
            # self.tn = telnetlib.Telnet(host_ip,port=23)
            self.tn.open(funcIp, port=self.lv_dic01[funcIp]['port'])
            time.sleep(0.1)
        except:
            logger.error(u"错误: {0}".format(inspect.stack()[0][2]))
            self.lv_dic01[funcIp].update({'status': "连接失败"})
            return False
        # 等待login出现后输入用户名，最多等待10秒
        self.tn.read_until(b'Username:', timeout=10)
        print(self.lv_dic01[funcIp])
        self.tn.write(self.lv_dic01[funcIp]['usr'].encode('ascii') + b'\n')
        time.sleep(0.3)
        # 等待Password出现后输入用户名，最多等待10秒
        self.tn.read_until(b'Password:', timeout=10)
        self.tn.write(self.lv_dic01[funcIp]['pwd'].encode('ascii') + b'\n')
        time.sleep(0.3)
        # 延时两秒再收取返回结果，给服务端足够响应时间
        # 获取登录结果
        # read_very_eager()获取到的是的是上次获取之后本次获取之前的所有输出
        command_result = self.tn.read_very_eager().decode('ascii')
        if 'Login incorrect' not in command_result:
            logger.info('%s登录成功' % funcIp)
            stdout = self.def_execute_command_with_more("""sys\ndis power\n""")
            stdout = """Slot    PowerID  Online   Mode   State      Power(W)
------------------------------------------------------------
0       PWR1     Present  AC     Supply     500.00
0       PWR2     Present  AC     Supply     500.00
1       PWR1     Present  AC     Supply     500.00
1       PWR2     Present  AC     Supply     500.00
2       PWR1     Present  AC     Supply     500.00
2       PWR2     Present  AC     Supply     500.00
3       PWR1     Present  AC     Supply     500.00
3       PWR2     Present  AC     Supply     500.00"""
            if len(stdout) > 0:
                logger.info("Starting discovering resource - {0}".format(funcIp))

                title_name = ["Slot", "PowerID", "Online", "Mode", "State", "Power"]
                self.cus_excel_op.create_sheet(funcIp)
                [self.cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
                pattern = "(\d+)\s+(\w+)\s+(Present|\w+)\s+(AC|\w+)\s+(Supply|nosupply)\s+(\d+\.\d+)"
                result = re.findall(pattern, stdout)
                for i_01 in range(0, len(result)):
                    if self.lv_dic01.get(funcIp, []):
                        lvList03 = self.lv_dic01[funcIp]['attr']
                        lvList03.append([{'Slot': result[i_01][0].replace("42D", "")},
                                         {'PowerID': result[i_01][1].replace("42D", "")},
                                         {'Online': result[i_01][2].replace("42D", "")},
                                         {'Mode': result[i_01][3].replace("42D", "")},
                                         {'State': result[i_01][4].replace("42D", "")},
                                         {'Power': result[i_01][5].replace("42D", "")}])
                        # print(lvList03)
                        self.lv_dic01.update({funcIp: {'attr': lvList03, 'usr': self.lv_dic01[funcIp]['usr'],
                                                       'pwd': self.lv_dic01[funcIp]['pwd'], 'port': self.lv_dic01[funcIp]['port'],
                                                       'status': ''}})
                    else:
                        lvList02 = [[{'Slot': result[i_01][0].replace("42D", "")},
                                     {'PowerID': result[i_01][1].replace("42D", "")},
                                     {'Online': result[i_01][2].replace("42D", "")},
                                     {'Mode': result[i_01][3].replace("42D", "")},
                                     {'State': result[i_01][4].replace("42D", "")},
                                     {'Power': result[i_01][5].replace("42D", "")}]]
                        # print(lvList02)
                        self.lv_dic01.update({funcIp: {'attr': lvList02, 'usr': self.lv_dic01[funcIp]['usr'],
                                                       'pwd': self.lv_dic01[funcIp]['pwd'], 'port': self.lv_dic01[funcIp]['port'],
                                                       'status': ''}})
            self.lv_dic01[funcIp].update({'status': "连接成功"})
            return True
        else:
            logger.error('%s登录失败，用户名或密码错误' % funcIp)
            self.lv_dic01[funcIp].update({'status': "用户名密码错误"})
            return False

    # 此函数实现telnet登录主机
    def def_connect(self, funcIp):
        try:
            # self.tn = telnetlib.Telnet(host_ip,port=23)
            self.tn.open(funcIp, port=self.lv_dic01[funcIp]['port'])
            time.sleep(0.1)
        except:
            logger.error(u"错误: {0}".format(inspect.stack()[0][2]))
            return False
        # 等待login出现后输入用户名，最多等待10秒
        self.tn.read_until(b'Username:', timeout=10)
        self.tn.write(self.lv_dic01[funcIp]['usr'].encode('ascii') + b'\n')
        time.sleep(0.3)
        # 等待Password出现后输入用户名，最多等待10秒
        self.tn.read_until(b'Password:', timeout=10)
        self.tn.write(self.lv_dic01[funcIp]['pwd'].encode('ascii') + b'\n')
        time.sleep(0.3)
        # 延时两秒再收取返回结果，给服务端足够响应时间
        # 获取登录结果
        # read_very_eager()获取到的是的是上次获取之后本次获取之前的所有输出
        command_result = self.tn.read_very_eager().decode('ascii')
        if 'Login incorrect' not in command_result:
            logger.info('%s登录成功' % funcIp)
            return True
        else:
            logger.error('%s登录失败，用户名或密码错误' % funcIp)
            return False

    # 此函数实现执行传过来的命令，并输出其执行结果
    def def_execute_command_with_more(self, command):
        # 执行命令
        self.tn.write(command.encode('ascii'))
        rackreply = self.tn.expect([], timeout=1)[2].decode().strip()
        # print(rackreply)
        while True:
            self.tn.read_until(b'\r\n[', timeout=0.1)
            self.tn.write(b'\r\n')
            time.sleep(0.1)
            stdout = self.tn.expect([], timeout=1)[2]
            if stdout.find(b'\r\n[') != -1:
                break
            else:
                self.tn.read_until(b'  ---- More ----', timeout=0.1)
                self.tn.write(b' ')
                time.sleep(0.1)
                stdout = self.tn.expect([], timeout=1)[2].decode().strip()
                rackreply = rackreply + stdout
                if stdout.find(u'\r\n[') != -1:
                    break
        # 获取命令结果
        return rackreply

    # 退出telnet
    def def_logout(self):
        try:
            self.tn.close()
            logger.info("Connection Closed Successfully")
            print(0)
        except Exception as oops:
            logger.info(u"错误: {0} {1}".format(inspect.stack()[0][2], oops))
            sys.exit("{0}".format(inspect.currentframe().f_lineno))

    def def_discovering_resources(self, host, list_resources):
        # try:
        for resource in list_resources:
            if ['disname'].count(resource) == 1:
                logger.info("Starting discovering resource - {0}".format(resource))
                one_object_list = {}
                discovered_resource = []
                one_object_list["{#INDEX}"] = 1
                discovered_resource.append(one_object_list)
                logger.info("Succes get resource - {0}".format(resource))
                converted_resource = self.zabbix_sender.def_convert_to_zabbix_json(discovered_resource)
                timestampnow = int(time.time())
                TIMESTAMPNOW = timestampnow
                xer = []
                xer.append("%s %s %s %s" % (host, resource, timestampnow, converted_resource))
                self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, xer, host)
            elif ['discpu'].count(resource) == 1:
                logger.info("Starting discovering resource - {0}".format(resource))
                one_object_list = {}
                discovered_resource = []
                one_object_list["{#INDEX}"] = 1
                discovered_resource.append(one_object_list)
                logger.info("Succes get resource - {0}".format(resource))
                converted_resource = self.zabbix_sender.def_convert_to_zabbix_json(discovered_resource)
                timestampnow = int(time.time())
                TIMESTAMPNOW = timestampnow
                xer = []
                xer.append("%s %s %s %s" % (host, resource, timestampnow, converted_resource))
                self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, xer, host)
            elif ['discpu_20230104'].count(resource) == 1:
                logger.info("Starting discovering resource - {0}".format(resource))
                one_object_list = {}
                discovered_resource = []
                one_object_list["{#INDEX}"] = 1
                discovered_resource.append(one_object_list)
                logger.info("Succes get resource - {0}".format(resource))
                converted_resource = self.zabbix_sender.def_convert_to_zabbix_json(discovered_resource)
                timestampnow = int(time.time())
                TIMESTAMPNOW = timestampnow
                xer = []
                xer.append("%s %s %s %s" % (host, resource, timestampnow, converted_resource))
                self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, xer, host)
            elif ['dismem_20230104'].count(resource) == 1:
                logger.info("Starting discovering resource - {0}".format(resource))
                one_object_list = {}
                discovered_resource = []
                one_object_list["{#INDEX}"] = 1
                discovered_resource.append(one_object_list)
                logger.info("Succes get resource - {0}".format(resource))
                converted_resource = self.zabbix_sender.def_convert_to_zabbix_json(discovered_resource)
                timestampnow = int(time.time())
                TIMESTAMPNOW = timestampnow
                xer = []
                xer.append("%s %s %s %s" % (host, resource, timestampnow, converted_resource))
                self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, xer, host)
            elif ['disinterface'].count(resource) == 1:
                discovered_resource = []
                stdout = self.def_execute_command_with_more("""sys\ndis int brief\n""")
                # stdout = self.execute_command_with_more("""sys\ndis cu | include sysname\n""")
                # stdout = self.execute_command_with_more("""sys\n dis cpu-usage\n""")
                if len(stdout) > 0:
                    logger.info("Starting discovering resource - {0}".format(resource))

                    title_name = ['index', 'Interface', 'IP Address/Mask', 'Physical', 'Protocol']
                    self.cus_excel_op.create_sheet(resource)
                    [self.cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
                    pattern = "(\w+\d+/*\d*/*\d*)\s*(\w*\.?\d*\.?\d*\.?\d*/?\d*)\s*(up|down)\s*(up|down)"
                    result = re.findall(pattern, stdout)
                    for i_01 in range(0, len(result)):
                        self.cus_excel_op.set_cell_value(i_01 + 2, 1, i_01 + 1)
                        for i_02 in range(0, len(result[i_01])):
                            self.cus_excel_op.set_cell_value(i_01 + 2, i_02 + 2, result[i_01][i_02].replace("42D", ""))

                col_02_list = self.cus_excel_op.get_column_values(2)
                del col_02_list[0]
                for len_col_02 in range(len(col_02_list)):
                    one_object_list = {}
                    one_object_list["{#INTERFACE}"] = col_02_list[len_col_02]
                    discovered_resource.append(one_object_list)
                logger.info("Succes get resource - {0}".format(resource))
                converted_resource = self.zabbix_sender.def_convert_to_zabbix_json(discovered_resource)
                timestampnow = int(time.time())
                TIMESTAMPNOW = timestampnow
                xer = []
                xer.append("%s %s %s %s" % (host, resource, timestampnow, converted_resource))
                self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, xer, host)
            elif ['dispower'].count(resource) == 1:
                def process_dispower_data():
                    # 1. 加载Excel数据
                    self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkdispower.xlsx', 1)

                    # 获取各列数据(跳过表头)
                    columns = {
                        'channel_id': self.cus_excel_op.get_column_values(1)[1:],
                        'from_location': [self.cus_excel_op.get_cell_value(i + 2, 2) for i in range(len(self.cus_excel_op.get_column_values(1)[1:]))],
                        'to_location': [self.cus_excel_op.get_cell_value(i + 2, 3) for i in range(len(self.cus_excel_op.get_column_values(1)[1:]))],
                        'ip_address': [self.cus_excel_op.get_cell_value(i + 2, 4) for i in range(len(self.cus_excel_op.get_column_values(1)[1:]))],
                        'username': [self.cus_excel_op.get_cell_value(i + 2, 6) for i in range(len(self.cus_excel_op.get_column_values(1)[1:]))],
                        'password': [self.cus_excel_op.get_cell_value(i + 2, 7) for i in range(len(self.cus_excel_op.get_column_values(1)[1:]))],
                        'port': [self.cus_excel_op.get_cell_value(i + 2, 8) for i in range(len(self.cus_excel_op.get_column_values(1)[1:]))],
                        'alarm_count': [self.cus_excel_op.get_cell_value(i + 2, 9) for i in range(len(self.cus_excel_op.get_column_values(1)[1:]))],
                        'monitor_dir': [self.cus_excel_op.get_cell_value(i + 2, 10) for i in range(len(self.cus_excel_op.get_column_values(1)[1:]))]
                    }

                    # 初始化字典结构
                    self.lv_dic01 = {ip: {'attr': [], 'usr': user, 'pwd': pwd, 'port': port}
                                     for ip, user, pwd, port in zip(
                            columns['ip_address'],
                            columns['username'],
                            columns['password'],
                            columns['port'])}

                    # 2. 多线程连接处理
                    def connect_callback(future, ip):
                        try:
                            result = future.result()
                            logger.info(f"成功处理IP: {ip}")
                        except Exception as e:
                            logger.error(f"处理IP {ip} 时出错: {str(e)}")

                    discovered_resource = []
                    with ThreadPoolExecutor(GV_CPU_COUNT) as executor:
                        futures = []
                        for ip in self.lv_dic01.keys():
                            future = executor.submit(self.def_connect_dispower, ip)
                            future.add_done_callback(lambda f, lip=ip: connect_callback(f, lip))
                            futures.append(future)
                        wait(futures)

                    # 3. 准备Zabbix数据
                    dic_replace = {".": "__", "/": "__", "%": "", "$": "", "\"": "", "+": "", "(": "", ")": "", " ": ""}
                    for ip, ip_info in self.lv_dic01.items():
                        for attr in ip_info['attr']:
                            one_object = {
                                "{#IPLIST}": self.cus_localMethord.def_batch_replace(ip, dic_replace) + "__" +
                                             self.cus_localMethord.def_batch_replace(attr[0]['Slot'], dic_replace) + "__" +
                                             self.cus_localMethord.def_batch_replace(attr[1]['PowerID'], dic_replace)
                            }
                            discovered_resource.append(one_object)

                    # 4. 发送到Zabbix
                    timestamp = int(time.time())
                    converted_data = self.zabbix_sender.def_convert_to_zabbix_json(discovered_resource)
                    zabbix_data = [f"\"{host}\" \"dispower\" {timestamp} {converted_data}"]
                    self.cus_zabbixSender.def_send_data_to_zabbix("dispower", zabbix_data, host)

                    # 5. 处理第二列数据
                    interface_list = self.cus_excel_op.get_column_values(2)[1:]
                    for interface in interface_list:
                        discovered_resource.append({"{#INTERFACE}": interface})

                    logger.info(f"Success get resource - {resource}")
                    converted_data = self.zabbix_sender.def_convert_to_zabbix_json(discovered_resource)
                    timestamp = int(time.time())
                    zabbix_data = [f"{host} {resource} {timestamp} {converted_data}"]
                    self.zabbix_sender.def_send_data_to_zabbix(timestamp, zabbix_data, host)

                try:
                    process_dispower_data()
                except Exception as e:
                    logger.error(f"处理dispower资源时出错: {str(e)}")
            else:
                logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], u'没有匹配的自动发现规则'))

            self.def_logout()

    def def_get_status_resources(self, host, list_resources):
        try:
            for resource in list_resources:
                if ['disname'].count(resource) == 1:
                    stdout = self.def_execute_command_with_more("""sys\ndis cu | include sysname\n""")
                    if len(stdout) > 0:
                        logger.info("Starting collecting status of resource - {0}".format(resource))

                        title_name = ['index', 'name']
                        self.cus_excel_op.create_sheet(resource)
                        [self.cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
                        pattern = "sysname\s(\w.*)"
                        result = re.search(pattern, stdout).group(1).replace('\r', '')
                        self.cus_excel_op.set_cell_value(2, 1, 1)
                        self.cus_excel_op.set_cell_value(2, 2, result)

                        col_01_list = self.cus_excel_op.get_column_values(1)
                        del col_01_list[0]
                        col_02_list = self.cus_excel_op.get_column_values(2)
                        del col_02_list[0]
                        TIMESTAMPNOW = int(time.time())
                        state_resources = []
                        for len_col_01 in range(len(col_01_list)):
                            key_name = "{0}[{1}]".format(resource, col_01_list[len_col_01])
                            state_resources.append("%s %s %s %s" % ("\"" + host + "\"", key_name, TIMESTAMPNOW, col_02_list[len_col_01]))
                        self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, state_resources, host)
                elif ['discpu'].count(resource) == 1:
                    stdout = self.def_execute_command_with_more("""sys\n dis cpu-usage\n""")
                    if len(stdout) > 0:
                        logger.info("Starting collecting status of resource - {0}".format(resource))

                        title_name = ['index', 'name']
                        self.cus_excel_op.create_sheet(resource)
                        [self.cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
                        pattern = "CPU\sUsage\s+:\s(\d.*%)\sMax"
                        result = re.search(pattern, stdout).group(1).replace('%', '')
                        self.cus_excel_op.set_cell_value(2, 1, 1)
                        self.cus_excel_op.set_cell_value(2, 2, result)

                        col_01_list = self.cus_excel_op.get_column_values(1)
                        del col_01_list[0]
                        col_02_list = self.cus_excel_op.get_column_values(2)
                        del col_02_list[0]
                        TIMESTAMPNOW = int(time.time())
                        state_resources = []
                        for len_col_01 in range(len(col_01_list)):
                            key_used = "{0}.[{1}]".format(resource, col_01_list[len_col_01])
                            state_resources.append("%s %s %s %s" % ("\"" + host + "\"", key_used, TIMESTAMPNOW, col_02_list[len_col_01]))
                        self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, state_resources, host)
                elif ['discpu_20230104'].count(resource) == 1:
                    stdout = self.def_execute_command_with_more("""sys\n dis cpu\n""")
                    if len(stdout) > 0:
                        logger.info("Starting collecting status of resource - {0}".format(resource))

                        title_name = ['index', 'name']
                        self.cus_excel_op.create_sheet(resource)
                        [self.cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
                        pattern = re.compile(r'(\d*%)\sin')
                        result = re.search(pattern, stdout).group(1).replace('%', '')
                        self.cus_excel_op.set_cell_value(2, 1, 1)
                        self.cus_excel_op.set_cell_value(2, 2, result)

                        col_01_list = self.cus_excel_op.get_column_values(1)
                        del col_01_list[0]
                        col_02_list = self.cus_excel_op.get_column_values(2)
                        del col_02_list[0]
                        timestampnow = int(time.time())
                        TIMESTAMPNOW = timestampnow
                        state_resources = []
                        for len_col_01 in range(len(col_01_list)):
                            key_used = "{0}.[{1}]".format(resource, col_01_list[len_col_01])
                            state_resources.append("%s %s %s %s" % ("\"" + host + "\"", key_used, timestampnow, col_02_list[len_col_01]))
                        self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, state_resources, host)
                elif ['dismem_20230104'].count(resource) == 1:
                    stdout = self.def_execute_command_with_more("""sys\n dis mem\n""")
                    if len(stdout) > 0:
                        logger.info("Starting collecting status of resource - {0}".format(resource))

                        title_name = ['index', 'name']
                        self.cus_excel_op.create_sheet(resource)
                        [self.cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
                        pattern = re.compile(r'Rate:\s(\d*%)')
                        result = re.search(pattern, stdout).group(1).replace('%', '')
                        self.cus_excel_op.set_cell_value(2, 1, 1)
                        self.cus_excel_op.set_cell_value(2, 2, result)

                        col_01_list = self.cus_excel_op.get_column_values(1)
                        del col_01_list[0]
                        col_02_list = self.cus_excel_op.get_column_values(2)
                        del col_02_list[0]
                        timestampnow = int(time.time())
                        TIMESTAMPNOW = timestampnow
                        state_resources = []
                        for len_col_01 in range(len(col_01_list)):
                            key_used = "{0}.[{1}]".format(resource, col_01_list[len_col_01])
                            state_resources.append("%s %s %s %s" % ("\"" + host + "\"", key_used, timestampnow, col_02_list[len_col_01]))
                        self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, state_resources, host)
                elif ['disinterface'].count(resource) == 1:
                    stdout = self.def_execute_command_with_more("""sys\ndis int brief\n""")
                    # stdout = self.execute_command_with_more("""sys\ndis cu | include sysname\n""")
                    # stdout = self.execute_command_with_more("""sys\n dis cpu-usage\n""")
                    if len(stdout) > 0:
                        logger.info("Starting collecting status of resource - {0}".format(resource))

                        title_name = ['index', 'Interface', 'IP Address/Mask', 'Physical', 'Protocol']
                        self.cus_excel_op.create_sheet(resource)
                        [self.cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
                        pattern = "(\w+\d+/*\d*/*\d*)\s*(\w*\.?\d*\.?\d*\.?\d*/?\d*)\s*(up|down)\s*(up|down)"
                        result = re.findall(pattern, stdout)
                        for i_01 in range(0, len(result)):
                            self.cus_excel_op.set_cell_value(i_01 + 2, 1, i_01 + 1)
                            for i_02 in range(0, len(result[i_01])):
                                self.cus_excel_op.set_cell_value(i_01 + 2, i_02 + 2, result[i_01][i_02].replace("42D", ""))

                        col_02_list = self.cus_excel_op.get_column_values(2)
                        del col_02_list[0]
                        col_04_list = self.cus_excel_op.get_column_values(4)
                        del col_04_list[0]
                        col_05_list = self.cus_excel_op.get_column_values(5)
                        del col_05_list[0]
                        timestampnow = int(time.time())
                        TIMESTAMPNOW = timestampnow
                        state_resources = []
                        for len_col_02 in range(len(col_02_list)):
                            key_phy = "physical.{0}[{1}]".format(resource, col_02_list[len_col_02])
                            key_pro = "protocol.{0}[{1}]".format(resource, col_02_list[len_col_02])
                            state_resources.append("%s %s %s %s" % ("\"" + host + "\"", key_phy, timestampnow, self.cus_localMethord.def_convert_text_to_numeric(col_04_list[len_col_02])))
                            state_resources.append("%s %s %s %s" % ("\"" + host + "\"", key_pro, timestampnow, self.cus_localMethord.def_convert_text_to_numeric(col_05_list[len_col_02])))
                        self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, state_resources, host)
                elif ['dispower'].count(resource) == 1:
                    try:
                        # 1. 加载Excel数据
                        self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkdispower.xlsx', 1)

                        # 2. 准备数据收集回调函数
                        def data_collection_callback(future, ip):
                            try:
                                result = future.result()
                                logger.info(f"成功收集IP {ip} 的数据")
                                return result
                            except Exception as e:
                                logger.error(f"收集IP {ip} 数据时出错: {str(e)}")
                                return None

                        # 3. 多线程处理主逻辑
                        def process_dispower_data():
                            # 获取各列数据(跳过表头)
                            row_count = len(self.cus_excel_op.get_column_values(1)) - 1
                            columns = {
                                'channel_id': [self.cus_excel_op.get_cell_value(i + 2, 1) for i in range(row_count)],
                                'from_loc': [self.cus_excel_op.get_cell_value(i + 2, 2) for i in range(row_count)],
                                'to_loc': [self.cus_excel_op.get_cell_value(i + 2, 3) for i in range(row_count)],
                                'ip': [self.cus_excel_op.get_cell_value(i + 2, 4) for i in range(row_count)],
                                'user': [self.cus_excel_op.get_cell_value(i + 2, 6) for i in range(row_count)],
                                'pwd': [self.cus_excel_op.get_cell_value(i + 2, 7) for i in range(row_count)],
                                'port': [self.cus_excel_op.get_cell_value(i + 2, 8) for i in range(row_count)],
                                'alarm_count': [self.cus_excel_op.get_cell_value(i + 2, 9) for i in range(row_count)],
                                'monitor_dir': [self.cus_excel_op.get_cell_value(i + 2, 10) for i in range(row_count)]
                            }

                            # 初始化设备字典
                            self.lv_dic01 = {ip: {'attr': [], 'usr': user, 'pwd': pwd, 'port': port}
                                             for ip, user, pwd, port in zip(columns['ip'], columns['user'],
                                                                            columns['pwd'], columns['port'])}

                            # 多线程连接设备
                            with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
                                futures = []
                                for ip in self.lv_dic01.keys():
                                    future = executor.submit(self.def_connect_dispower, ip)
                                    future.add_done_callback(
                                        lambda f, lip=ip: data_collection_callback(f, lip))
                                    futures.append(future)

                                # 显示进度
                                completed = 0
                                total = len(futures)
                                for future in as_completed(futures):
                                    completed += 1
                                    logger.info(f"处理进度: {completed}/{total} ({completed / total:.1%})")
                                    try:
                                        future.result()  # 触发可能的异常
                                    except Exception:
                                        continue

                            # 准备Zabbix监控数据
                            state_resources = []
                            dic_replace = {".": "__", "/": "__", "%": "", "$": "", "\"": "",
                                           "+": "", "(": "", ")": "", " ": ""}

                            for ip, ip_info in self.lv_dic01.items():
                                for attr in ip_info['attr']:
                                    slot = self.cus_localMethord.def_batch_replace(attr[0]['Slot'], dic_replace)
                                    power_id = self.cus_localMethord.def_batch_replace(attr[1]['PowerID'], dic_replace)
                                    ip_clean = self.cus_localMethord.def_batch_replace(ip, dic_replace)

                                    key = f"powerstatus.[{ip_clean}__{slot}__{power_id}]"
                                    state = attr[4]['State']

                                    state_resources.append(
                                        f"\"{host}\" \"{key}\" {int(time.time())} {state}"
                                    )

                            # 发送数据到Zabbix
                            if state_resources:
                                self.cus_zabbixSender.def_send_data_to_zabbix(
                                    'dispower', state_resources, host)
                                logger.info(f"成功发送 {len(state_resources)} 条电源状态数据到Zabbix")
                            else:
                                logger.warning("没有收集到有效的电源状态数据")

                        # 执行主处理逻辑
                        process_dispower_data()

                    except Exception as e:
                        logger.error(f"处理dispower资源时发生错误: {str(e)}")
                        raise
                else:
                    logger.error(f"错误: {inspect.stack()[0][2]} 没有匹配的自动发现规则")
            self.def_logout()
            # self.cus_excel_op.def_save_create_xlsx(XLSX_FILENAME)
        except Exception as pizdec:
            logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], pizdec))
            self.def_logout()
            sys.exit("{0}".format(inspect.currentframe().f_lineno))


class CusSSHClient(object):
    def __init__(self, ):
        self.cus_sshClient = None
        self.cus_zabbixSender = CusZabbixSender()
        self.cus_excel_op = CusExcelOp()
        self.cus_excel_op.create_new_workbook()
        self.cus_localMethord = CusLocalMethod()
        self.lv_dic01 = {}

    def def_connect_dir_mtime_filenum(self, funcIp, attr, lvInt01):
        ssh_client = paramiko.SSHClient()
        try:
            # print(funcIp)
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            __timeout = 5
            __sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            __sock.settimeout(__timeout)
            __sock.connect((funcIp, self.lv_dic01[funcIp]['port']))
            ssh_client = paramiko.Transport(__sock)
            if os.path.isfile(self.lv_dic01[funcIp]['pwd']):
                # print('rsa', funcIp, self.lv_dic01[funcIp]['usr'], self.lv_dic01[funcIp]['port'], self.lv_dic01[funcIp]['pwd'])
                # print(self.lv_dic01[funcIp])
                __pkey = paramiko.RSAKey.from_private_key_file(self.lv_dic01[funcIp]['pwd'])
                ssh_client.connect(username=self.lv_dic01[funcIp]['usr'], pkey=__pkey)
            else:
                # 如果有需要，使用用户名和密码进行身份验证
                # print('pwd', funcIp)
                # print(self.lv_dic01[funcIp])
                ssh_client.connect(username=self.lv_dic01[funcIp]['usr'], password=self.lv_dic01[funcIp]['pwd'])

            ssh_channel_current_time = ssh_client.open_channel(kind='session')
            ssh_channel_current_time.settimeout(60)
            ssh_channel_current_time.exec_command("""date +%s""")
            stdout_current_time = ssh_channel_current_time.recv(1024).decode()
            # print(funcIp, ' stdout_current_time:', stdout_current_time)
            ssh_channel_change_time = ssh_client.open_channel(kind='session')
            ssh_channel_change_time.settimeout(60)
            command = f"""
            if [[ -d {attr[1]['fileName']} ]]; then
              find {attr[1]['fileName']} -mindepth 0 -maxdepth 1 -type d -exec stat -c %Y {{}} \; | sort -n | tail -1
            else
              echo -999
            fi
            """
            ssh_channel_change_time.exec_command(command)
            # 循环读取直到没有更多数据或通道关闭
            stdout_change_time = b''
            stderr_change_time = b''
            while True:
                if ssh_channel_change_time.recv_ready():
                    stdout_change_time += ssh_channel_change_time.recv(1024)
                if ssh_channel_change_time.recv_stderr_ready():
                    stderr_change_time += ssh_channel_change_time.recv_stderr(1024)
                if not ssh_channel_change_time.recv_ready() and not ssh_channel_change_time.recv_stderr_ready() and ssh_channel_change_time.exit_status_ready():
                    break
                time.sleep(0.1)  # 增加延迟，给命令执行的时间
            stdout_change_time = stdout_change_time.decode().replace('：', ":")
            # print(funcIp, ' stdout_change_time:', stdout_change_time)
            if int(stdout_change_time.replace('\n', '')) == -999:
                attr[3]['dirchangetime'] = -999
            else:
                attr[3]['dirchangetime'] = int(stdout_current_time.replace('\n', '')) - int(stdout_change_time.replace('\n', ''))
            ssh_channel = ssh_client.open_channel(kind='session')
            ssh_channel.settimeout(60)
            command = f"""
            if [[ -d {attr[1]['fileName']} ]]; then
              find {attr[1]['fileName']} -type f | head -n {attr[0]['fileDepth']} | wc -l
            else
              echo -999
            fi
            """
            ssh_channel.exec_command(command)
            # 循环读取直到没有更多数据或通道关闭
            stdout = b''
            stderr = b''
            while True:
                if ssh_channel.recv_ready():
                    stdout += ssh_channel.recv(1024)
                if ssh_channel.recv_stderr_ready():
                    stderr += ssh_channel.recv_stderr(1024)
                if not ssh_channel.recv_ready() and not ssh_channel.recv_stderr_ready() and ssh_channel.exit_status_ready():
                    break
                time.sleep(0.1)  # 增加延迟，给命令执行的时间
            stdout = stdout.decode()
            attr[2]['fileCount'] = stdout.replace('\n', '')
            stderr = stderr.decode()
            # print(stdout, stderr)
            if len(stderr) != 0 and len(stdout.replace('\n', '')) == 0:
                pattern = re.compile(r'.*No such file.*')
                result = re.findall(pattern, str(stderr))
                if len(result) != 0:
                    attr[2]['fileCount'] = 1000002  # [Errno 2] No such file
                pattern = re.compile(r'.*Permission denied')
                result = re.findall(pattern, str(stderr))
                if len(result) != 0:
                    attr[2]['fileCount'] = 1000005  # Permission denied
            print(f"dirchangetime : {lvInt01} ([ {funcIp} | {attr[1]['fileName']} ] -> {attr[3]['dirchangetime']}")
            print(f"fileCount : {lvInt01} ([ {funcIp} | {attr[1]['fileName']} ] -> {attr[2]['fileCount']}")
            ssh_channel_change_time.close()
            ssh_channel.close()
        except FileNotFoundError:
            print(f"{lvInt01} 错误：[ {funcIp} | {attr[1]['fileName']} ] -> 私钥文件 {self.lv_dic01[funcIp]['pwd']} 不存在")
        except paramiko.AuthenticationException:
            print(f"{lvInt01} 错误：[ {funcIp} | {attr[1]['fileName']} ] -> 认证失败，请检查用户名和私钥")
        except paramiko.SSHException as e:
            print(f"SSH错误: {lvInt01} : [ {funcIp} | {attr[1]['fileName']} ] -> {str(e)}")
        except Exception as e:
            # 获取当前异常的traceback对象
            tb = traceback.extract_tb(e.__traceback__)
            # 获取异常发生时的行号
            line_number = tb[-1][1]
            # 输出异常信息和行号
            print(f"SSH未知错误在行号 {line_number}: {lvInt01} : [ {funcIp} | {attr[1]['fileName']} ] -> {str(e)}")
            pattern = re.compile(r'Authentication failed.*')
            result = re.findall(pattern, str(e))
            if len(result) != 0:
                attr[2]['fileCount'] = 1000001  # Authentication failed.
                attr[3]['dirchangetime'] = 1000001  # Authentication failed.
            pattern = re.compile(r'.*Connection refused')
            result = re.findall(pattern, str(e))
            if len(result) != 0:
                attr[2]['fileCount'] = 1000003  # [Errno 111] Connection refused
                attr[3]['dirchangetime'] = 1000003  # [Errno 111] Connection refused
            pattern = re.compile(r'timed out.*')
            result = re.findall(pattern, str(e))
            if len(result) != 0:
                attr[2]['fileCount'] = 1000004  # timed out
                attr[3]['dirchangetime'] = 1000004  # timed out
        finally:
            ssh_client.close()
        return {'fileCount': attr[2]['fileCount'], 'dirchangetime': attr[3]['dirchangetime']}

    from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

    @retry(
        stop=stop_after_attempt(3),                          # 最多重试3次
        wait=wait_fixed(2),                                   # 每次间隔2秒
        retry=retry_if_exception_type((
            paramiko.SSHException,
            TimeoutError,
            ConnectionRefusedError,
            ConnectionError,
            socket.timeout,
            EOFError
        )),
        reraise=True
    )
    def def_connect_dir_filenum(self, funcIp, attr, lvInt01):  # 修改函数签名使其接受attr参数
        ssh_client = paramiko.SSHClient()
        try:
            # print(funcIp)
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            __timeout = 5
            __sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            __sock.settimeout(__timeout)
            __sock.connect((funcIp, self.lv_dic01[funcIp]['port']))
            ssh_client = paramiko.Transport(__sock)
            if os.path.isfile(self.lv_dic01[funcIp]['pwd']):
                # print(f"{lvInt01} -使用私钥开始认证- {funcIp} {attr[1]['fileName']} start")
                __pkey = paramiko.RSAKey.from_private_key_file(self.lv_dic01[funcIp]['pwd'])
                ssh_client.connect(username=self.lv_dic01[funcIp]['usr'], pkey=__pkey)
            else:
                # 如果有需要，使用用户名和密码进行身份验证
                # print(f"{lvInt01} -使用密码开始认证- {funcIp} {attr[1]['fileName']} start")
                ssh_client.connect(username=self.lv_dic01[funcIp]['usr'], password=self.lv_dic01[funcIp]['pwd'])
            # print(f"{lvInt01} check {funcIp} {attr[1]['fileName']} start")
            ssh_channel = ssh_client.open_channel(kind='session')
            ssh_channel.settimeout(60)
            command = f"""
            if [[ -d {attr[1]['fileName']} ]]; then
              find {attr[1]['fileName']} -type f | head -n {attr[0]['fileDepth']} | wc -l
            else
              echo -999
            fi
            """
            ssh_channel.exec_command(command)
            # 循环读取直到没有更多数据或通道关闭
            stdout = b''
            stderr = b''
            while True:
                if ssh_channel.recv_ready():
                    stdout += ssh_channel.recv(1024)
                if ssh_channel.recv_stderr_ready():
                    stderr += ssh_channel.recv_stderr(1024)
                if not ssh_channel.recv_ready() and not ssh_channel.recv_stderr_ready() and ssh_channel.exit_status_ready():
                    break
                time.sleep(0.1)  # 增加延迟，给命令执行的时间
            if stdout.decode():
                attr[2]['fileCount'] = stdout.decode().replace('\n', '').splitlines()[-1]
            if len(stderr.decode()) != 0 and len(stdout.decode().replace('\n', '')) == 0:
                pattern = re.compile(r'.*No such file.*')
                result = re.findall(pattern, str(stderr.decode()))
                if len(result) != 0:
                    attr[2]['fileCount'] = 1000002  # [Errno 2] No such file
                pattern = re.compile(r'.*Permission denied')
                result = re.findall(pattern, str(stderr.decode()))
                if len(result) != 0:
                    attr[2]['fileCount'] = 1000005  # Permission denied
            print(f"fileCount: {lvInt01} ([ {funcIp} | {attr[1]['fileName']} ] -> {attr[2]['fileCount']}")
            ssh_channel.close()
        except FileNotFoundError:
            print(f"{lvInt01} 错误：[ {funcIp} | {attr[1]['fileName']} ] -> 私钥文件 {self.lv_dic01[funcIp]['pwd']} 不存在")
        except paramiko.AuthenticationException:
            print(f"{lvInt01} 错误：[ {funcIp} | {attr[1]['fileName']} ] -> 认证失败，请检查用户名和私钥")
        except paramiko.SSHException as e:
            print(f"SSH错误: {lvInt01} : [ {funcIp} | {attr[1]['fileName']} ] -> {str(e)}")
            raise  # 🔧 抛出，让 retry 重试
        except (TimeoutError, ConnectionRefusedError, ConnectionError, socket.timeout, EOFError) as e:
            # 连接/超时错误，需要重试 → raise
            print(f"连接错误: {lvInt01} : [ {funcIp} | {attr[1]['fileName']} ] -> {str(e)}")
            raise  # 🔧 抛出，让 retry 重试
        except Exception as e:
            # 获取当前异常的traceback对象
            tb = traceback.extract_tb(e.__traceback__)
            # 获取异常发生时的行号
            line_number = tb[-1][1]
            # 输出异常信息和行号
            print(f"SSH未知错误在行号 {line_number}: {lvInt01} : [ {funcIp} | {attr[1]['fileName']} ] -> {str(e)}")
            pattern = re.compile(r'Authentication failed.*')
            result = re.findall(pattern, str(e))
            if len(result) != 0:
                attr[2]['fileCount'] = 1000001  # Authentication failed.
            pattern = re.compile(r'.*Connection refused')
            result = re.findall(pattern, str(e))
            if len(result) != 0:
                attr[2]['fileCount'] = 1000003  # [Errno 111] Connection refused
            pattern = re.compile(r'timed out.*')
            result = re.findall(pattern, str(e))
            if len(result) != 0:
                attr[2]['fileCount'] = 1000004  # timed out
                raise  # 🔧 超时可以重试
            # 🔧 如果是连接类错误，重试
            if any(kw in str(e).lower() for kw in ['timed out', 'refused', 'reset', 'broken pipe']):
                raise
        finally:
            ssh_client.close()
        return attr[2]['fileCount']

    from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type((
            paramiko.SSHException,
            TimeoutError,
            ConnectionRefusedError,
            ConnectionError,
            socket.timeout,
            EOFError
        )),
        reraise=True
    )
    def def_connect_dir_mtime(self, funcIp, attr, lvInt01):
        ssh_client = paramiko.SSHClient()
        try:
            # print(funcIp)
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            __timeout = 5
            __sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            __sock.settimeout(__timeout)
            __sock.connect((funcIp, self.lv_dic01[funcIp]['port']))
            ssh_client = paramiko.Transport(__sock)
            if os.path.isfile(self.lv_dic01[funcIp]['pwd']):
                # print('rsa', funcIp, self.lv_dic01[funcIp]['usr'], self.lv_dic01[funcIp]['port'], self.lv_dic01[funcIp]['pwd'])
                # print(self.lv_dic01[funcIp])
                __pkey = paramiko.RSAKey.from_private_key_file(self.lv_dic01[funcIp]['pwd'])
                ssh_client.connect(username=self.lv_dic01[funcIp]['usr'], pkey=__pkey)
            else:
                # 如果有需要，使用用户名和密码进行身份验证
                # print('pwd', funcIp)
                # print(self.lv_dic01[funcIp])
                ssh_client.connect(username=self.lv_dic01[funcIp]['usr'], password=self.lv_dic01[funcIp]['pwd'])

            ssh_channel_current_time = ssh_client.open_channel(kind='session')
            ssh_channel_current_time.settimeout(60)
            command = f"""date +%s"""
            ssh_channel_current_time.exec_command(command)
            # 循环读取直到没有更多数据或通道关闭
            stdout_current_time = b''
            stderr_current_time = b''
            while True:
                if ssh_channel_current_time.recv_ready():
                    stdout_current_time += ssh_channel_current_time.recv(1024)
                if ssh_channel_current_time.recv_stderr_ready():
                    stderr_current_time += ssh_channel_current_time.recv_stderr(1024)
                if not ssh_channel_current_time.recv_ready() and not ssh_channel_current_time.recv_stderr_ready() and ssh_channel_current_time.exit_status_ready():
                    break
                time.sleep(0.1)  # 增加延迟，给命令执行的时间
            # print(funcIp, ' stdout_current_time:', stdout_current_time)
            ssh_channel_change_time = ssh_client.open_channel(kind='session')
            ssh_channel_change_time.settimeout(60)
            command = f"""
            if [[ -d {attr[0]['dirName']} ]]; then
              find {attr[0]['dirName']} -mindepth 0 -maxdepth 1 -type d -exec stat -c %Y {{}} \; | sort -n | tail -1
            else
              echo -999
            fi
            """
            ssh_channel_change_time.exec_command(command)
            # 循环读取直到没有更多数据或通道关闭
            stdout_change_time = b''
            stderr_change_time = b''
            while True:
                if ssh_channel_change_time.recv_ready():
                    stdout_change_time += ssh_channel_change_time.recv(1024)
                if ssh_channel_change_time.recv_stderr_ready():
                    stdout_change_time += ssh_channel_change_time.recv_stderr(1024)
                if not ssh_channel_change_time.recv_ready() and not ssh_channel_change_time.recv_stderr_ready() and ssh_channel_change_time.exit_status_ready():
                    break
                time.sleep(0.1)  # 增加延迟，给命令执行的时间
            stdout_change_time = stdout_change_time.decode().replace('：', ":")
            # print(funcIp, ' stdout_change_time:', stdout_change_time)
            if int(stdout_change_time.replace('\n', '')) == -999:
                attr[1]['dirMTime'] = -999
            else:
                attr[1]['dirMTime'] = int(stdout_current_time.decode().replace('\n', '')) - int(stdout_change_time.replace('\n', ''))

            stderr = stderr_change_time.decode()
            # print(stdout, stderr)
            if len(stderr) != 0 and len(stdout_change_time.replace('\n', '')) == 0:
                pattern = re.compile(r'.*No such attr.*')
                result = re.findall(pattern, str(stderr))
                if len(result) != 0:
                    attr[1]['dirMTime'] = '文件或文件夹不存在'  # [Errno 2] No such attr
                pattern = re.compile(r'.*Permission denied')
                result = re.findall(pattern, str(stderr))
                if len(result) != 0:
                    attr[1]['dirMTime'] = '权限不足'  # Permission denied
            print(f"dirMTime: {lvInt01} ([ {funcIp} | {attr[0]['dirName']} ] -> {attr[1]['dirMTime']}")
            ssh_channel_current_time.close()
            ssh_channel_change_time.close()
        except FileNotFoundError:
            print(f"{lvInt01} 错误：[ {funcIp} | {attr[0]['dirName']} ] -> 私钥文件 {self.lv_dic01[funcIp]['pwd']} 不存在")
        except paramiko.AuthenticationException:
            print(f"{lvInt01} 错误：[ {funcIp} | {attr[0]['dirName']} ] -> 认证失败，请检查用户名和私钥")
        except paramiko.SSHException as e:
            print(f"SSH错误: {lvInt01} : [ {funcIp} | {attr[0]['dirName']} ] -> {str(e)}")
            raise  # 🔧 重试
        except (TimeoutError, ConnectionRefusedError, ConnectionError, socket.timeout, EOFError) as e:
            print(f"连接错误: {lvInt01} : [ {funcIp} | {attr[0]['dirName']} ] -> {str(e)}")
            raise  # 🔧 重试
        except Exception as e:
            # 获取当前异常的traceback对象
            tb = traceback.extract_tb(e.__traceback__)
            # 获取异常发生时的行号
            line_number = tb[-1][1]
            # 输出异常信息和行号
            print(f"SSH未知错误在行号 {line_number}: {lvInt01} : [ {funcIp} | {attr[0]['dirName']} ] -> {str(e)}")
            pattern = re.compile(r'Authentication failed.*')
            result = re.findall(pattern, str(e))
            if len(result) != 0:
                attr[1]['dirMTime'] = '验证失败'  # Authentication failed.
            pattern = re.compile(r'.*Connection refused')
            result = re.findall(pattern, str(e))
            if len(result) != 0:
                attr[1]['dirMTime'] = '连接拒绝'  # [Errno 111] Connection refused
            pattern = re.compile(r'timed out.*')
            result = re.findall(pattern, str(e))
            if 'timed out' in str(e).lower():
                raise  # 🔧 重试
            if len(result) != 0:
                attr[1]['dirMTime'] = '连接超时'  # timed out
        finally:
            ssh_client.close()
        return attr[1]['dirMTime']

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type((paramiko.SSHException, TimeoutError, ConnectionRefusedError, ConnectionError, socket.timeout, EOFError)),
        reraise=True
    )
    def def_connect_linux_mount(self, funcIp, attr, lvInt01):  # 修改函数签名使其接受attr参数
        ssh_client = paramiko.SSHClient()
        try:
            # print(funcIp)
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            __timeout = 5
            __sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            __sock.settimeout(__timeout)
            __sock.connect((funcIp, self.lv_dic01[funcIp]['port']))
            ssh_client = paramiko.Transport(__sock)
            if os.path.isfile(self.lv_dic01[funcIp]['pwd']):
                # print('rsa', funcIp, self.lv_dic01[funcIp]['usr'], self.lv_dic01[funcIp]['port'], self.lv_dic01[funcIp]['pwd'])
                # print(self.lv_dic01[funcIp])
                # print(f"{lvInt01} -使用私钥开始认证- {funcIp} {attr[0]['mountPath']} start")
                __pkey = paramiko.RSAKey.from_private_key_file(self.lv_dic01[funcIp]['pwd'])
                ssh_client.connect(username=self.lv_dic01[funcIp]['usr'], pkey=__pkey)
            else:
                # 如果有需要，使用用户名和密码进行身份验证
                # print('pwd', funcIp)
                # print(self.lv_dic01[funcIp])
                # print(f"{lvInt01} -使用密码开始认证- {funcIp} {attr[0]['mountPath']} start")
                ssh_client.connect(username=self.lv_dic01[funcIp]['usr'], password=self.lv_dic01[funcIp]['pwd'])
            # print(f"{lvInt01} check {funcIp} {attr[0]['mountPath']} start")
            ssh_channel = ssh_client.open_channel(kind='session')
            ssh_channel.settimeout(60)
            command = f"if mount | grep {attr[0]['mountPath']} | grep -v 'color' | grep -v 'grep' > /dev/null 2>&1; then echo '正常'; else echo '异常'; fi"
            ssh_channel.exec_command(command)
            # 循环读取直到没有更多数据或通道关闭
            stdout = b''
            stderr = b''
            while True:
                if ssh_channel.recv_ready():
                    stdout += ssh_channel.recv(1024)
                if ssh_channel.recv_stderr_ready():
                    stderr += ssh_channel.recv_stderr(1024)
                if not ssh_channel.recv_ready() and not ssh_channel.recv_stderr_ready() and ssh_channel.exit_status_ready():
                    break
                time.sleep(0.1)  # 增加延迟，给命令执行的时间
            if stdout.decode():
                attr[1]['mountStatus'] = stdout.decode().replace('\n', '').splitlines()[-1]
            if len(stderr.decode()) != 0 and len(stdout.decode().replace('\n', '')) == 0:
                pattern = re.compile(r'.*No such attr.*')
                result = re.findall(pattern, str(stderr.decode()))
                if len(result) != 0:
                    attr[1]['mountStatus'] = '文件或文件夹不存在'  # [Errno 2] No such attr
                pattern = re.compile(r'.*Permission denied')
                result = re.findall(pattern, str(stderr.decode()))
                if len(result) != 0:
                    attr[1]['mountStatus'] = '权限不足'  # Permission denied
            print(f"mountStatus: {lvInt01} ([ {funcIp} | {attr[0]['mountPath']} ] -> {attr[1]['mountStatus']}")
            ssh_channel.close()
        except FileNotFoundError:
            print(f"{lvInt01} 错误：[ {funcIp} | {attr[0]['mountPath']} ] -> 私钥文件 {self.lv_dic01[funcIp]['pwd']} 不存在")
        except paramiko.AuthenticationException:
            print(f"{lvInt01} 错误：[ {funcIp} | {attr[0]['mountPath']} ] -> 认证失败，请检查用户名和私钥")
        except paramiko.SSHException as e:
            print(f"SSH错误: {lvInt01} : [ {funcIp} | {attr[0]['mountPath']} ] -> {str(e)}")
            raise  # 🔧 重试
        except (TimeoutError, ConnectionRefusedError, ConnectionError, socket.timeout, EOFError) as e:
            print(f"连接错误: {lvInt01} : [ {funcIp} | {attr[0]['mountPath']} ] -> {str(e)}")
            raise  # 🔧 重试
        except Exception as e:
            # 获取当前异常的traceback对象
            tb = traceback.extract_tb(e.__traceback__)
            # 获取异常发生时的行号
            line_number = tb[-1][1]
            # 输出异常信息和行号
            print(f"SSH未知错误在行号 {line_number}: {lvInt01} : [ {funcIp} | {attr[0]['mountPath']} ] -> {str(e)}")
            pattern = re.compile(r'Authentication failed.*')
            result = re.findall(pattern, str(e))
            if len(result) != 0:
                attr[1]['mountStatus'] = '验证失败'  # Authentication failed.
            pattern = re.compile(r'.*Connection refused')
            result = re.findall(pattern, str(e))
            if len(result) != 0:
                attr[1]['mountStatus'] = '连接拒绝'  # [Errno 111] Connection refused
            pattern = re.compile(r'timed out.*')
            result = re.findall(pattern, str(e))
            if 'timed out' in str(e).lower():
                raise  # 🔧 重试
            if len(result) != 0:
                attr[1]['mountStatus'] = '连接超时'  # timed out
        finally:
            ssh_client.close()
        return attr[1]['mountStatus']

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type((paramiko.SSHException, TimeoutError, ConnectionRefusedError, ConnectionError, socket.timeout, EOFError)),
        reraise=True
    )
    def def_connect_linux_df(self, funcIp, attr, lvInt01):
        ssh_client = paramiko.SSHClient()
        try:
            # print(funcIp)
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            __timeout = 5
            __sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            __sock.settimeout(__timeout)
            __sock.connect((funcIp, self.lv_dic01[funcIp]['port']))
            ssh_client = paramiko.Transport(__sock)
            if os.path.isfile(self.lv_dic01[funcIp]['pwd']):
                # print('rsa', funcIp, self.lv_dic01[funcIp]['usr'], self.lv_dic01[funcIp]['port'], self.lv_dic01[funcIp]['pwd'])
                # print(self.lv_dic01[funcIp])
                __pkey = paramiko.RSAKey.from_private_key_file(self.lv_dic01[funcIp]['pwd'])
                ssh_client.connect(username=self.lv_dic01[funcIp]['usr'], pkey=__pkey)
            else:
                # 如果有需要，使用用户名和密码进行身份验证
                # print('pwd', funcIp)
                # print(self.lv_dic01[funcIp])
                ssh_client.connect(username=self.lv_dic01[funcIp]['usr'], password=self.lv_dic01[funcIp]['pwd'])

            ssh_channel = ssh_client.open_channel(kind='session')
            ssh_channel.settimeout(60)
            dic_replace = {".*": "_"}
            command = f"""
            if mount | grep -w "{attr[0]['mountPath']}" | grep -v 'grep' | grep -v 'color'; then
                df -h | grep -w "{attr[0]['mountPath']}" | awk -F ' ' '{{print $1"__"$6,$2,$3,$4,$5}}'
            else
                echo "{attr[0]['mountPath']} 异常 异常 异常 异常"
            fi
            """
            ssh_channel.exec_command(command)
            # 循环读取直到没有更多数据或通道关闭
            stdout = b''
            stderr = b''
            while True:
                if ssh_channel.recv_ready():
                    stdout += ssh_channel.recv(1024)
                if ssh_channel.recv_stderr_ready():
                    stderr += ssh_channel.recv_stderr(1024)
                if not ssh_channel.recv_ready() and not ssh_channel.recv_stderr_ready() and ssh_channel.exit_status_ready():
                    break
                time.sleep(0.1)  # 增加延迟，给命令执行的时间
            attr[0]['mountPath'] = '异常'
            attr[1]['Size'] = '异常'
            attr[2]['Used'] = '异常'
            attr[3]['Avail'] = '异常'
            attr[4]['Use'] = '异常'
            if stdout.decode():
                attr[0]['mountPath'] = stdout.decode().splitlines()[-1].split()[0]
                attr[1]['Size'] = stdout.decode().splitlines()[-1].split()[1]
                attr[2]['Used'] = stdout.decode().splitlines()[-1].split()[2]
                attr[3]['Avail'] = stdout.decode().splitlines()[-1].split()[3]
                attr[4]['Use'] = stdout.decode().splitlines()[-1].split()[4]
            if len(stderr.decode()) != 0 and len(stdout.decode().replace('\n', '')) == 0:
                attr[0]['mountPath'] = '异常'
                attr[1]['Size'] = '异常'
                attr[2]['Used'] = '异常'
                attr[3]['Avail'] = '异常'
                attr[4]['Use'] = '异常'
            print(f"Size: {lvInt01} ([ {funcIp} | {attr[0]['mountPath']} ] -> {attr[1]['Size']}")
            ssh_channel.close()
        except FileNotFoundError:
            print(f"{lvInt01} 错误：[ {funcIp} | {attr[0]['mountPath']} ] -> 私钥文件 {self.lv_dic01[funcIp]['pwd']} 不存在")
        except paramiko.AuthenticationException:
            print(f"{lvInt01} 错误：[ {funcIp} | {attr[0]['mountPath']} ] -> 认证失败，请检查用户名和私钥")
        except paramiko.SSHException as e:
            print(f"SSH错误: {lvInt01} : [ {funcIp} | {attr[0]['mountPath']} ] -> {str(e)}")
            raise  # 🔧 重试
        except (TimeoutError, ConnectionRefusedError, ConnectionError, socket.timeout, EOFError) as e:
            print(f"连接错误: {lvInt01} : [ {funcIp} | {attr[0]['mountPath']} ] -> {str(e)}")
            raise  # 🔧 重试
        except Exception as e:
            # 获取当前异常的traceback对象
            tb = traceback.extract_tb(e.__traceback__)
            # 获取异常发生时的行号
            line_number = tb[-1][1]
            # 输出异常信息和行号
            print(f"SSH未知错误在行号 {line_number}: {lvInt01} : [ {funcIp} | {attr[0]['mountPath']} ] -> {str(e)}")
            pattern = re.compile(r'Authentication failed.*')
            result = re.findall(pattern, str(e))
            if len(result) != 0:
                attr[1]['Size'] = '验证失败'  # Authentication failed.
            pattern = re.compile(r'.*Connection refused')
            result = re.findall(pattern, str(e))
            if len(result) != 0:
                attr[1]['Size'] = '连接拒绝'  # [Errno 111] Connection refused
            pattern = re.compile(r'timed out.*')
            result = re.findall(pattern, str(e))
            if 'timed out' in str(e).lower():
                raise  # 🔧 重试
            if len(result) != 0:
                attr[1]['Size'] = '连接超时'  # timed out
        finally:
            ssh_client.close()
        return {'Size': attr[1]['Size'], 'Used': attr[2]['Used'], 'Avail': attr[3]['Avail'], 'Use': attr[4]['Use']}

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2),
        retry=retry_if_exception_type((paramiko.SSHException, TimeoutError, ConnectionRefusedError, ConnectionError, socket.timeout, EOFError)),
        reraise=True
    )
    def def_connect_linux_ps(self, funcIp, attr, lvInt01):  # 修改函数签名使其接受attr参数
        ssh_client = paramiko.SSHClient()
        try:
            # print(funcIp)
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            __timeout = 5
            __sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            __sock.settimeout(__timeout)
            __sock.connect((funcIp, self.lv_dic01[funcIp]['port']))
            ssh_client = paramiko.Transport(__sock)
            if os.path.isfile(self.lv_dic01[funcIp]['pwd']):
                # print('rsa', funcIp, self.lv_dic01[funcIp]['usr'], self.lv_dic01[funcIp]['port'], self.lv_dic01[funcIp]['pwd'])
                # print(self.lv_dic01[funcIp])
                __pkey = paramiko.RSAKey.from_private_key_file(self.lv_dic01[funcIp]['pwd'])
                ssh_client.connect(username=self.lv_dic01[funcIp]['usr'], pkey=__pkey)
            else:
                # 如果有需要，使用用户名和密码进行身份验证
                # print('pwd', funcIp)
                # print(self.lv_dic01[funcIp])
                ssh_client.connect(username=self.lv_dic01[funcIp]['usr'], password=self.lv_dic01[funcIp]['pwd'])
            # print(f"{lvInt01} check {funcIp} {attr[0]['psPath']} start")
            max_attempts = 360
            attempt = 0
            stdout = ''
            stderr = ''
            while attempt < max_attempts:
                ssh_channel = ssh_client.open_channel(kind='session')
                ssh_channel.settimeout(60)
                command = f"if ps -ef | grep {attr[0]['psPath']} | grep -v 'color' | grep -v 'grep' > /dev/null 2>&1; then echo '正常'; else echo '异常'; fi"
                ssh_channel.exec_command(command)
                # 循环读取直到没有更多数据或通道关闭
                stdout = b''
                stderr = b''
                while True:
                    if ssh_channel.recv_ready():
                        stdout += ssh_channel.recv(1024)
                    if ssh_channel.recv_stderr_ready():
                        stderr += ssh_channel.recv_stderr(1024)
                    if not ssh_channel.recv_ready() and not ssh_channel.recv_stderr_ready() and ssh_channel.exit_status_ready():
                        break
                    time.sleep(0.1)  # 增加延迟，给命令执行的时间
                attr[1]['psStatus'] = stdout.decode().replace('\n', '')
                print(f"psStatus: {lvInt01} ({max_attempts}/{attempt}): [ {funcIp} | {attr[0]['psPath']} ] -> {attr[1]['psStatus']}")
                # 如果状态为异常，等待10秒并重新尝试，否则跳出循环
                if attr[1]['psStatus'] == '异常':
                    attr[1]['psStatus'] = '异常'
                    time.sleep(1)  # 等待10秒
                    attempt += 1  # 增加尝试次数
                    ssh_channel.close()
                else:
                    ssh_channel.close()
                    break  # 如果状态为正常，跳出循环
            # print(f"{lvInt01} check {funcIp} {attr[0]['psPath']} done")
            if len(stderr.decode()) != 0 and len(stdout.decode().replace('\n', '')) == 0:
                pattern = re.compile(r'.*No such attr.*')
                result = re.findall(pattern, str(stderr.decode()))
                if len(result) != 0:
                    attr[1]['psStatus'] = '文件或文件夹不存在'  # [Errno 2] No such attr
                pattern = re.compile(r'.*Permission denied')
                result = re.findall(pattern, str(stderr.decode()))
                if len(result) != 0:
                    attr[1]['psStatus'] = '权限不足'  # Permission denied
        except FileNotFoundError:
            print(f"{lvInt01} 错误：[ {funcIp} | {attr[0]['psPath']} ] -> 私钥文件 {self.lv_dic01[funcIp]['pwd']} 不存在")
        except paramiko.AuthenticationException:
            print(f"{lvInt01} 错误：[ {funcIp} | {attr[0]['psPath']} ] -> 认证失败，请检查用户名和私钥")
        except paramiko.SSHException as e:
            print(f"SSH错误: {lvInt01} : [ {funcIp} | {attr[0]['mountPath']} ] -> {str(e)}")
            raise  # 🔧 重试
        except (TimeoutError, ConnectionRefusedError, ConnectionError, socket.timeout, EOFError) as e:
            print(f"连接错误: {lvInt01} : [ {funcIp} | {attr[0]['mountPath']} ] -> {str(e)}")
            raise  # 🔧 重试
        except Exception as e:
            # 获取当前异常的traceback对象
            tb = traceback.extract_tb(e.__traceback__)
            # 获取异常发生时的行号
            line_number = tb[-1][1]
            # 输出异常信息和行号
            print(f"SSH未知错误在行号 {line_number}: {lvInt01} : [ {funcIp} | {attr[0]['psPath']} ] -> {str(e)}")
            pattern = re.compile(r'Authentication failed.*')
            result = re.findall(pattern, str(e))
            if len(result) != 0:
                attr[1]['psStatus'] = '验证失败'  # Authentication failed.
            pattern = re.compile(r'.*Connection refused')
            result = re.findall(pattern, str(e))
            if len(result) != 0:
                attr[1]['psStatus'] = '连接拒绝'  # [Errno 111] Connection refused
            pattern = re.compile(r'timed out.*')
            result = re.findall(pattern, str(e))
            if 'timed out' in str(e).lower():
                raise  # 🔧 重试
            if len(result) != 0:
                attr[1]['psStatus'] = '连接超时'  # timed out
        finally:
            ssh_client.close()
        return attr[1]['psStatus']

    def def_discovering_resources(self, host, list_resources):
        for resource in list_resources:
            if ['linuxDf'].count(resource) == 1:
                self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkLinuxDisk.xlsx', 1)

                column_1_list = self.cus_excel_op.get_column_values(1)
                del column_1_list[0]
                column_2_list = []
                column_3_list = []
                column_4_list = []
                column_6_list = []
                column_7_list = []
                column_8_list = []
                column_9_list = []
                column_10_list = []

                for i in range(len(column_1_list)):
                    column_1_list.append(self.cus_excel_op.get_cell_value(i + 2, 1))  # 通道ID
                    column_2_list.append(self.cus_excel_op.get_cell_value(i + 2, 2))  # 通道从哪
                    column_3_list.append(self.cus_excel_op.get_cell_value(i + 2, 3))  # 通道到哪
                    column_4_list.append(self.cus_excel_op.get_cell_value(i + 2, 4))  # 属地通道IP地址
                    column_6_list.append(self.cus_excel_op.get_cell_value(i + 2, 6))  # 用户名
                    column_7_list.append(self.cus_excel_op.get_cell_value(i + 2, 7))  # 密码
                    column_8_list.append(self.cus_excel_op.get_cell_value(i + 2, 8))  # 端口
                    column_9_list.append(self.cus_excel_op.get_cell_value(i + 2, 9))  # 告警文件数
                    column_10_list.append(self.cus_excel_op.get_cell_value(i + 2, 10))  # 监控目录

                discovered_resource = []
                dic_replace = {".": "__", "/": "__", "%": "", "$": "", "\"": "",
                               "+": "", "(": "", ")": "", " ": "", "*": ""}
                for col_01 in range(len(column_4_list)):
                    one_object_list = {}
                    one_object_list["{#IPLIST}"] = self.cus_localMethord.def_batch_replace(column_4_list[col_01], dic_replace) + "__" + \
                                                   self.cus_localMethord.def_batch_replace(column_10_list[col_01], dic_replace)
                    one_object_list["{#ADDRESSLIST}"] = str(column_1_list[col_01]) + "__" + \
                                                        column_2_list[col_01] + "__" + \
                                                        column_3_list[col_01] + "__" + \
                                                        self.cus_localMethord.def_batch_replace(column_10_list[col_01], dic_replace)
                    discovered_resource.append(one_object_list)
                converted_resource = self.cus_zabbixSender.def_convert_to_zabbix_json(discovered_resource)
                xer = []
                id_name = 'linuxDf'
                timestampnow = int(time.time())
                TIMESTAMPNOW = timestampnow
                xer.append("%s %s %s %s" % ("\"" + host + "\"", id_name, TIMESTAMPNOW, converted_resource))
                print(xer)
                self.cus_zabbixSender.def_send_data_to_zabbix(id_name, xer, host)
            elif ['netstat'].count(resource) == 1:
                self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkLinuxPort.xlsx', 1)

                column_1_list = self.cus_excel_op.get_column_values(1)
                del column_1_list[0]
                column_2_list = []
                column_3_list = []
                column_4_list = []
                column_6_list = []
                column_7_list = []

                for i in range(len(column_1_list)):
                    column_1_list.append(self.cus_excel_op.get_cell_value(i + 2, 1))  # 主机名
                    column_2_list.append(self.cus_excel_op.get_cell_value(i + 2, 2))  # IP地址
                    column_3_list.append(self.cus_excel_op.get_cell_value(i + 2, 3))  # 协议
                    column_4_list.append(self.cus_excel_op.get_cell_value(i + 2, 4))  # 用户名
                    column_6_list.append(self.cus_excel_op.get_cell_value(i + 2, 6))  # 密码
                    column_7_list.append(self.cus_excel_op.get_cell_value(i + 2, 7))  # 端口
                    connection = self.def_connect(self.cus_excel_op.get_cell_value(i + 2, 4),
                                                  self.cus_excel_op.get_cell_value(i + 2, 6),
                                                  self.cus_excel_op.get_cell_value(i + 2, 2),
                                                  self.cus_excel_op.get_cell_value(i + 2, 7))
                    stdin, stdout, stderr = connection.exec_command("""netstat -ntlp | awk -v OFS=',' '{{print $7,$4,$6}}'""")
                    time.sleep(0.1)
                    if len(stderr.read().decode().strip()) > 0:
                        logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], stderr.read()))
                        connection.close()
                        sys.exit("{0}".format(inspect.currentframe().f_lineno))
                    else:
                        logger.info("Starting discovering resource - {0}".format(resource))

                        title_name = ['index', 'name', 'port', 'state']
                        self.cus_excel_op.create_sheet(resource)
                        [self.cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
                        pattern = re.compile(r'(\d*/\w*).*,.*:(\d*),(\w*)n*')
                        result = re.findall(pattern, stdout.read().decode().strip())
                        # 去重
                        unit_column_1_list = list(set(result))
                        # 使用index保持不乱序
                        unit_column_1_list.sort(key=result.index)
                        for i_01 in range(0, len(unit_column_1_list)):
                            self.cus_excel_op.set_cell_value(i_01 + 2, 1, i_01 + 1)
                            for i_02 in range(0, len(unit_column_1_list[i_01])):
                                self.cus_excel_op.set_cell_value(i_01 + 2, i_02 + 2, unit_column_1_list[i_01][i_02].replace("/", "-"))
                        discovered_resource = []
                        col_02_list = self.cus_excel_op.get_column_values(2)
                        del col_02_list[0]
                        col_03_list = self.cus_excel_op.get_column_values(3)
                        del col_03_list[0]
                        for len_col_01 in range(len(col_02_list)):
                            one_object_list = {}
                            one_object_list["{#NAME}"] = col_02_list[len_col_01].replace("/", "-") + '_' + col_03_list[len_col_01]
                            discovered_resource.append(one_object_list)
                        logger.info("Succes get resource - {0}".format(resource))
                        converted_resource = self.cus_zabbixSender.def_convert_to_zabbix_json(discovered_resource)
                        xer = []
                        timestampnow = int(time.time())
                        TIMESTAMPNOW = timestampnow
                        xer.append("%s %s %s %s" % (host, resource, timestampnow, converted_resource))
                        # print(xer)
                        self.cus_zabbixSender.def_send_data_to_zabbix(TIMESTAMPNOW, xer, host)
            elif ['dirMTimeFileNum'].count(resource) == 1:
                self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkDirMTimeFileNum.xlsx', 1)

                column_1_list = self.cus_excel_op.get_column_values(1)
                del column_1_list[0]
                column_2_list = []
                column_3_list = []
                column_4_list = []
                column_6_list = []
                column_7_list = []
                column_8_list = []
                column_9_list = []
                column_10_list = []

                for i in range(len(column_1_list)):
                    column_1_list.append(self.cus_excel_op.get_cell_value(i + 2, 1))  # 通道ID
                    column_2_list.append(self.cus_excel_op.get_cell_value(i + 2, 2))  # 通道从哪
                    column_3_list.append(self.cus_excel_op.get_cell_value(i + 2, 3))  # 通道到哪
                    column_4_list.append(self.cus_excel_op.get_cell_value(i + 2, 4))  # 属地通道IP地址
                    column_6_list.append(self.cus_excel_op.get_cell_value(i + 2, 6))  # 用户名
                    column_7_list.append(self.cus_excel_op.get_cell_value(i + 2, 7))  # 密码
                    column_8_list.append(self.cus_excel_op.get_cell_value(i + 2, 8))  # 端口
                    column_9_list.append(self.cus_excel_op.get_cell_value(i + 2, 9))  # 告警文件数
                    column_10_list.append(self.cus_excel_op.get_cell_value(i + 2, 10))  # 监控目录

                discovered_resource = []
                dic_replace = {".": "__", "/": "__", "%": "", "$": "", "\"": "", "+": "", "(": "", ")": "", " ": ""}
                for col_01 in range(len(column_4_list)):
                    one_object_list = {}
                    one_object_list["{#IPLIST}"] = self.cus_localMethord.def_batch_replace(column_4_list[col_01], dic_replace) + "__" + \
                                                   self.cus_localMethord.def_batch_replace(column_10_list[col_01], dic_replace)
                    one_object_list["{#ADDRESSLIST}"] = str(column_1_list[col_01]) + "__" + \
                                                        column_2_list[col_01] + "__" + \
                                                        column_3_list[col_01] + "__" + \
                                                        self.cus_localMethord.def_batch_replace(column_10_list[col_01], dic_replace)
                    discovered_resource.append(one_object_list)
                converted_resource = self.cus_zabbixSender.def_convert_to_zabbix_json(discovered_resource)
                xer = []
                id_name = 'dirMTimeFileNum'
                timestampnow = int(time.time())
                TIMESTAMPNOW = timestampnow
                xer.append("%s %s %s %s" % ("\"" + host + "\"", id_name, TIMESTAMPNOW, converted_resource))
                print(xer)
                self.cus_zabbixSender.def_send_data_to_zabbix(id_name, xer, host)
            elif ['dirFileNum'].count(resource) == 1:
                self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkDirFileNum.xlsx', 1)

                column_1_list = self.cus_excel_op.get_column_values(1)
                del column_1_list[0]
                column_2_list = []
                column_3_list = []
                column_4_list = []
                column_5_list = []
                column_6_list = []
                column_7_list = []
                column_8_list = []
                column_9_list = []
                column_10_list = []
                column_11_list = []
                column_12_list = []
                column_13_list = []

                for i in range(len(column_1_list)):
                    column_1_list.append(self.cus_excel_op.get_cell_value(i + 2, 1))  # 格式化IP
                    column_2_list.append(self.cus_excel_op.get_cell_value(i + 2, 2))  # 任务名称
                    column_3_list.append(self.cus_excel_op.get_cell_value(i + 2, 3))  # 机房位置
                    column_4_list.append(self.cus_excel_op.get_cell_value(i + 2, 4))  # 所属业务
                    column_5_list.append(self.cus_excel_op.get_cell_value(i + 2, 5))  # 所属应用
                    column_6_list.append(self.cus_excel_op.get_cell_value(i + 2, 6))  # 数据来源
                    column_7_list.append(self.cus_excel_op.get_cell_value(i + 2, 7))  # IP地址
                    column_8_list.append(self.cus_excel_op.get_cell_value(i + 2, 8))  # 协议
                    column_9_list.append(self.cus_excel_op.get_cell_value(i + 2, 9))  # 用户名
                    column_10_list.append(self.cus_excel_op.get_cell_value(i + 2, 10))  # 密码
                    column_11_list.append(self.cus_excel_op.get_cell_value(i + 2, 11))  # 端口
                    column_12_list.append(self.cus_excel_op.get_cell_value(i + 2, 12))  # 告警文件数
                    column_13_list.append(self.cus_excel_op.get_cell_value(i + 2, 13))  # 监控目录

                discovered_resource = []
                dic_replace = {".": "__", "/": "__", "%": "", "$": "", "\"": "", "+": "", "(": "", ")": "", " ": ""}
                for col_01 in range(len(column_4_list)):
                    one_object_list = {}
                    IPLIST = [self.cus_localMethord.def_batch_replace(column_7_list[col_01], dic_replace),
                              self.cus_localMethord.def_batch_replace(column_13_list[col_01], dic_replace)]
                    one_object_list["{#IPLIST}"] = "__".join(IPLIST)
                    ADDRESSLIST = [str(column_1_list[col_01]), str(column_2_list[col_01]), str(column_3_list[col_01]),
                                   str(column_4_list[col_01]), str(column_5_list[col_01]), str(column_6_list[col_01]),
                                   self.cus_localMethord.def_batch_replace(column_13_list[col_01], dic_replace)]
                    one_object_list["{#ADDRESSLIST}"] = "__".join(ADDRESSLIST)
                    discovered_resource.append(one_object_list)
                converted_resource = self.cus_zabbixSender.def_convert_to_zabbix_json(discovered_resource)
                xer = []
                id_name = 'dirFileNum'
                timestampnow = int(time.time())
                TIMESTAMPNOW = timestampnow
                xer.append("%s %s %s %s" % ("\"" + host + "\"", id_name, TIMESTAMPNOW, converted_resource))
                print(xer)
                self.cus_zabbixSender.def_send_data_to_zabbix(id_name, xer, host)
            elif ['dirMTime'].count(resource) == 1:
                self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkDirMTime.xlsx', 1)

                column_1_list = self.cus_excel_op.get_column_values(1)
                del column_1_list[0]
                column_2_list = []
                column_3_list = []
                column_4_list = []
                column_5_list = []
                column_6_list = []
                column_7_list = []
                column_8_list = []
                column_9_list = []
                column_10_list = []
                column_11_list = []
                column_12_list = []
                column_13_list = []

                for i in range(len(column_1_list)):
                    column_1_list.append(self.cus_excel_op.get_cell_value(i + 2, 1))  # 格式化IP
                    column_2_list.append(self.cus_excel_op.get_cell_value(i + 2, 2))  # 任务名称
                    column_3_list.append(self.cus_excel_op.get_cell_value(i + 2, 3))  # 机房位置
                    column_4_list.append(self.cus_excel_op.get_cell_value(i + 2, 4))  # 所属业务
                    column_5_list.append(self.cus_excel_op.get_cell_value(i + 2, 5))  # 所属应用
                    column_6_list.append(self.cus_excel_op.get_cell_value(i + 2, 6))  # 数据来源
                    column_7_list.append(self.cus_excel_op.get_cell_value(i + 2, 7))  # IP地址
                    column_8_list.append(self.cus_excel_op.get_cell_value(i + 2, 8))  # 协议
                    column_9_list.append(self.cus_excel_op.get_cell_value(i + 2, 9))  # 用户名
                    column_10_list.append(self.cus_excel_op.get_cell_value(i + 2, 10))  # 密码
                    column_11_list.append(self.cus_excel_op.get_cell_value(i + 2, 11))  # 端口
                    column_12_list.append(self.cus_excel_op.get_cell_value(i + 2, 12))  # 告警文件数
                    column_13_list.append(self.cus_excel_op.get_cell_value(i + 2, 13))  # 监控目录

                discovered_resource = []
                dic_replace = {".": "__", "/": "__", "%": "", "$": "", "\"": "", "+": "", "(": "", ")": "", " ": ""}
                for col_01 in range(len(column_4_list)):
                    one_object_list = {}
                    IPLIST = [self.cus_localMethord.def_batch_replace(column_7_list[col_01], dic_replace),
                              self.cus_localMethord.def_batch_replace(column_13_list[col_01], dic_replace)]
                    one_object_list["{#IPLIST}"] = "__".join(IPLIST)
                    ADDRESSLIST = [str(column_1_list[col_01]), str(column_2_list[col_01]), str(column_3_list[col_01]),
                                   str(column_4_list[col_01]), str(column_5_list[col_01]), str(column_6_list[col_01]),
                                   self.cus_localMethord.def_batch_replace(column_13_list[col_01], dic_replace)]
                    one_object_list["{#ADDRESSLIST}"] = "__".join(ADDRESSLIST)
                    discovered_resource.append(one_object_list)
                converted_resource = self.cus_zabbixSender.def_convert_to_zabbix_json(discovered_resource)
                xer = []
                id_name = 'dirMTime'
                timestampnow = int(time.time())
                TIMESTAMPNOW = timestampnow
                xer.append("%s %s %s %s" % ("\"" + host + "\"", id_name, TIMESTAMPNOW, converted_resource))
                print(xer)
                self.cus_zabbixSender.def_send_data_to_zabbix(id_name, xer, host)
            elif ['linuxMount'].count(resource) == 1:
                self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkLinuxMount.xlsx', 1)

                column_1_list = self.cus_excel_op.get_column_values(1)
                del column_1_list[0]
                column_2_list = []
                column_3_list = []
                column_4_list = []
                column_6_list = []
                column_7_list = []
                column_8_list = []
                column_9_list = []
                column_10_list = []

                for i in range(len(column_1_list)):
                    column_1_list.append(self.cus_excel_op.get_cell_value(i + 2, 1))  # 通道ID
                    column_2_list.append(self.cus_excel_op.get_cell_value(i + 2, 2))  # 通道从哪
                    column_3_list.append(self.cus_excel_op.get_cell_value(i + 2, 3))  # 通道到哪
                    column_4_list.append(self.cus_excel_op.get_cell_value(i + 2, 4))  # 属地通道IP地址
                    column_6_list.append(self.cus_excel_op.get_cell_value(i + 2, 6))  # 用户名
                    column_7_list.append(self.cus_excel_op.get_cell_value(i + 2, 7))  # 密码
                    column_8_list.append(self.cus_excel_op.get_cell_value(i + 2, 8))  # 端口
                    column_9_list.append(self.cus_excel_op.get_cell_value(i + 2, 9))  # 告警文件数
                    column_10_list.append(self.cus_excel_op.get_cell_value(i + 2, 10))  # 监控目录

                discovered_resource = []
                dic_replace = {".": "__", "/": "__", "%": "", "$": "", "\"": "", "+": "", "(": "", ")": "", " ": ""}
                for col_01 in range(len(column_4_list)):
                    one_object_list = {}
                    one_object_list["{#IPLIST}"] = self.cus_localMethord.def_batch_replace(column_4_list[col_01], dic_replace) + "__" + \
                                                   self.cus_localMethord.def_batch_replace(column_10_list[col_01], dic_replace)
                    one_object_list["{#ADDRESSLIST}"] = str(column_1_list[col_01]) + "__" + \
                                                        column_2_list[col_01] + "__" + \
                                                        column_3_list[col_01] + "__" + \
                                                        self.cus_localMethord.def_batch_replace(column_10_list[col_01], dic_replace)
                    discovered_resource.append(one_object_list)
                converted_resource = self.cus_zabbixSender.def_convert_to_zabbix_json(discovered_resource)
                xer = []
                id_name = 'linuxMount'
                timestampnow = int(time.time())
                TIMESTAMPNOW = timestampnow
                xer.append("%s %s %s %s" % ("\"" + host + "\"", id_name, TIMESTAMPNOW, converted_resource))
                print(xer)
                self.cus_zabbixSender.def_send_data_to_zabbix(id_name, xer, host)
            elif ['linuxPs'].count(resource) == 1:
                self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkLinuxPs.xlsx', 1)

                column_1_list = self.cus_excel_op.get_column_values(1)
                del column_1_list[0]
                column_2_list = []
                column_3_list = []
                column_4_list = []
                column_6_list = []
                column_7_list = []
                column_8_list = []
                column_9_list = []
                column_10_list = []

                for i in range(len(column_1_list)):
                    column_1_list.append(self.cus_excel_op.get_cell_value(i + 2, 1))  # 通道ID
                    column_2_list.append(self.cus_excel_op.get_cell_value(i + 2, 2))  # 通道从哪
                    column_3_list.append(self.cus_excel_op.get_cell_value(i + 2, 3))  # 通道到哪
                    column_4_list.append(self.cus_excel_op.get_cell_value(i + 2, 4))  # 属地通道IP地址
                    column_6_list.append(self.cus_excel_op.get_cell_value(i + 2, 6))  # 用户名
                    column_7_list.append(self.cus_excel_op.get_cell_value(i + 2, 7))  # 密码
                    column_8_list.append(self.cus_excel_op.get_cell_value(i + 2, 8))  # 端口
                    column_9_list.append(self.cus_excel_op.get_cell_value(i + 2, 9))  # 告警文件数
                    column_10_list.append(self.cus_excel_op.get_cell_value(i + 2, 10))  # 监控目录

                discovered_resource = []
                dic_replace = {".": "__", "/": "__", "%": "", "$": "", "\"": "", "+": "", "(": "", ")": "", " ": ""}
                for col_01 in range(len(column_4_list)):
                    one_object_list = {}
                    one_object_list["{#IPLIST}"] = self.cus_localMethord.def_batch_replace(column_4_list[col_01], dic_replace) + "__" + \
                                                   self.cus_localMethord.def_batch_replace(column_10_list[col_01], dic_replace)
                    one_object_list["{#ADDRESSLIST}"] = str(column_1_list[col_01]) + "__" + \
                                                        column_2_list[col_01] + "__" + \
                                                        column_3_list[col_01] + "__" + \
                                                        self.cus_localMethord.def_batch_replace(column_10_list[col_01], dic_replace)
                    discovered_resource.append(one_object_list)
                converted_resource = self.cus_zabbixSender.def_convert_to_zabbix_json(discovered_resource)
                xer = []
                id_name = 'linuxPs'
                timestampnow = int(time.time())
                TIMESTAMPNOW = timestampnow
                xer.append("%s %s %s %s" % ("\"" + host + "\"", id_name, TIMESTAMPNOW, converted_resource))
                print(xer)
                self.cus_zabbixSender.def_send_data_to_zabbix(id_name, xer, host)

    def def_get_status_resources(self, host, list_resources):
        for resource in list_resources:
            if ['linuxDf'].count(resource) == 1:
                try:
                    # 1. 加载Excel数据
                    self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkLinuxDisk.xlsx', 1)

                    # 2. 定义回调函数
                    def process_callback(future, ip, mount_path):
                        try:
                            result = future.result()
                            logger.info(f"成功处理 {ip} 的挂载点: {mount_path}")
                            return result
                        except Exception as e:
                            logger.error(f"处理 {ip} 的 {mount_path} 时出错: {str(e)}")
                            return None

                    # 3. 主处理函数
                    def process_linux_disk():
                        # 获取各列数据(跳过表头)
                        row_count = len(self.cus_excel_op.get_column_values(1)) - 1
                        columns = {
                            'channel_id': [self.cus_excel_op.get_cell_value(i + 2, 1) for i in range(row_count)],
                            'from_loc': [self.cus_excel_op.get_cell_value(i + 2, 2) for i in range(row_count)],
                            'to_loc': [self.cus_excel_op.get_cell_value(i + 2, 3) for i in range(row_count)],
                            'ip': [self.cus_excel_op.get_cell_value(i + 2, 4) for i in range(row_count)],
                            'user': [self.cus_excel_op.get_cell_value(i + 2, 6) for i in range(row_count)],
                            'pwd': [self.cus_excel_op.get_cell_value(i + 2, 7) for i in range(row_count)],
                            'port': [self.cus_excel_op.get_cell_value(i + 2, 8) for i in range(row_count)],
                            'alarm_count': [self.cus_excel_op.get_cell_value(i + 2, 9) for i in range(row_count)],
                            'mount_path': [self.cus_excel_op.get_cell_value(i + 2, 10) for i in range(row_count)]
                        }

                        # 初始化设备字典
                        self.lv_dic01 = {}
                        for ip, user, pwd, port, mount in zip(columns['ip'], columns['user'],
                                                              columns['pwd'], columns['port'],
                                                              columns['mount_path']):
                            if ip not in self.lv_dic01:
                                self.lv_dic01[ip] = {
                                    'attr': [],
                                    'usr': user,
                                    'pwd': pwd,
                                    'port': port
                                }
                            self.lv_dic01[ip]['attr'].append([
                                {'mountPath': mount},
                                {'Size': '异常'},
                                {'Used': '异常'},
                                {'Avail': '异常'},
                                {'Use': '异常'}
                            ])

                        # 多线程处理磁盘检查
                        with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
                            futures = []
                            total_tasks = 0

                            # 统计总任务数
                            for ip, ip_data in self.lv_dic01.items():
                                total_tasks += len(ip_data['attr'])

                            # 提交任务
                            completed = 0
                            for ip, ip_data in self.lv_dic01.items():
                                for idx, attr in enumerate(ip_data['attr']):
                                    mount_path = attr[0]['mountPath']
                                    future = executor.submit(
                                        self.def_connect_linux_df, ip, attr, idx)
                                    future.add_done_callback(
                                        lambda f, lip=ip, mp=mount_path: process_callback(f, lip, mp))
                                    futures.append(future)

                            # 显示进度
                            for future in as_completed(futures):
                                completed += 1
                                logger.info(f"处理进度: {completed}/{total_tasks} ({completed / total_tasks:.1%})")
                                try:
                                    result = future.result()
                                    if result:
                                        ip, idx = result['ip'], result['idx']
                                        self.lv_dic01[ip]['attr'][idx][1]['Size'] = result.get("Size", "")
                                        self.lv_dic01[ip]['attr'][idx][2]['Used'] = result.get("Used", "")
                                        self.lv_dic01[ip]['attr'][idx][3]['Avail'] = result.get("Avail", "")
                                        self.lv_dic01[ip]['attr'][idx][4]['Use'] = result.get("Use", "")
                                except Exception as e:
                                    logger.error(f"处理结果时出错: {str(e)}")

                        # 准备Zabbix数据
                        state_resources = []
                        dic_replace = {".": "__", "/": "__", "%": "", "$": "", "\"": "",
                                       "+": "", "(": "", ")": "", " ": "", "*": ""}

                        for ip, ip_data in self.lv_dic01.items():
                            for attr in ip_data['attr']:
                                ip_clean = self.cus_localMethord.def_batch_replace(ip, dic_replace)
                                path_clean = self.cus_localMethord.def_batch_replace(
                                    attr[0]['mountPath'], dic_replace)

                                key = f"linuxDf.[{ip_clean}__{path_clean}]"
                                values = (
                                    attr[0]['mountPath'],
                                    attr[1]['Size'],
                                    attr[2]['Used'],
                                    attr[3]['Avail'],
                                    attr[4]['Use']
                                )

                                state_resources.append(
                                    f"\"{host}\" \"{key}\" {int(time.time())} \"{'|'.join(values)}\""
                                )

                        # 发送数据到Zabbix
                        if state_resources:
                            self.cus_zabbixSender.def_send_data_to_zabbix(
                                'linuxDf', state_resources, host)
                            logger.info(f"成功发送 {len(state_resources)} 条磁盘状态数据到Zabbix")
                        else:
                            logger.warning("没有收集到有效的磁盘状态数据")

                    # 执行主处理逻辑
                    process_linux_disk()

                except Exception as e:
                    logger.error(f"处理linuxDf资源时发生错误: {str(e)}")
                    raise
            elif ['netstat'].count(resource) == 1:
                self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkLinuxPort.xlsx', 1)

                column_1_list = self.cus_excel_op.get_column_values(1)
                del column_1_list[0]
                column_2_list = []
                column_3_list = []
                column_4_list = []
                column_6_list = []
                column_7_list = []

                for i in range(len(column_1_list)):
                    column_1_list.append(self.cus_excel_op.get_cell_value(i + 2, 1))  # 主机名
                    column_2_list.append(self.cus_excel_op.get_cell_value(i + 2, 2))  # IP地址
                    column_3_list.append(self.cus_excel_op.get_cell_value(i + 2, 3))  # 协议
                    column_4_list.append(self.cus_excel_op.get_cell_value(i + 2, 4))  # 用户名
                    column_6_list.append(self.cus_excel_op.get_cell_value(i + 2, 6))  # 密码
                    column_7_list.append(self.cus_excel_op.get_cell_value(i + 2, 7))  # 端口
                    connection = self.def_connect(self.cus_excel_op.get_cell_value(i + 2, 4),
                                                  self.cus_excel_op.get_cell_value(i + 2, 6),
                                                  self.cus_excel_op.get_cell_value(i + 2, 2),
                                                  self.cus_excel_op.get_cell_value(i + 2, 7))
                    stdin, stdout, stderr = connection.exec_command("""netstat -ntlp | awk -v OFS=',' '{{print $7,$4,$6}}'""")
                    time.sleep(0.1)
                    if len(stderr.read()) > 0:
                        logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], stderr.read()))
                        connection.close()
                        sys.exit("{0}".format(inspect.currentframe().f_lineno))
                    else:
                        logger.info("Starting collecting status of resource - {0}".format(resource))

                        title_name = ['index', 'name', 'port', 'state']
                        self.cus_excel_op.create_sheet(resource)
                        [self.cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
                        pattern = re.compile(r'(\d*/\w*).*,.*:(\d*),(\w*)n*')
                        result = re.findall(pattern, stdout.read().decode().strip())
                        # 去重
                        unit_column_1_list = list(set(result))
                        # 使用index保持不乱序
                        unit_column_1_list.sort(key=result.index)
                        for i_01 in range(0, len(unit_column_1_list)):
                            self.cus_excel_op.set_cell_value(i_01 + 2, 1, i_01 + 1)
                            for i_02 in range(0, len(unit_column_1_list[i_01])):
                                self.cus_excel_op.set_cell_value(i_01 + 2, i_02 + 2, unit_column_1_list[i_01][i_02].replace("/", "-"))
                                if i_02 == 2:
                                    stdin, stdout, stderr = connection.exec_command("""tcping {0} {1}""".format(self.cus_excel_op.get_cell_value(i + 2, 2), unit_column_1_list[i_01][i_02 - 1]))
                                    time.sleep(0.1)
                                    pattern = re.compile(r'.*(open|closed).*')
                                    result = re.search(pattern, stdout.read().decode().strip())
                                    if self.cus_localMethord.def_convert_text_to_numeric(result.group(1)) == 0 and \
                                            self.cus_localMethord.def_convert_text_to_numeric(unit_column_1_list[i_01][i_02]) == 0:
                                        self.cus_excel_op.set_cell_value(i_01 + 2, i_02 + 2, 0)
                                    else:
                                        self.cus_excel_op.set_cell_value(i_01 + 2, i_02 + 2, 1)
                        col_02_list = self.cus_excel_op.get_column_values(2)
                        del col_02_list[0]
                        col_03_list = self.cus_excel_op.get_column_values(3)
                        del col_03_list[0]
                        col_04_list = self.cus_excel_op.get_column_values(4)
                        del col_04_list[0]
                        timestampnow = int(time.time())
                        TIMESTAMPNOW = timestampnow
                        state_resources = []
                        for len_col_01 in range(len(col_02_list)):
                            key_state = "state.{0}[{1}]".format(resource, col_02_list[len_col_01] + '_' + col_03_list[len_col_01])
                            state_resources.append("%s %s %s %s" % ("\"" + host + "\"", "\"" + key_state + "\"", timestampnow, col_04_list[len_col_01]))
                        self.cus_zabbixSender.def_send_data_to_zabbix(TIMESTAMPNOW, state_resources, host)
                    connection.close()
            elif ['dirMTimeFileNum'].count(resource) == 1:
                try:
                    # 1. 加载Excel数据
                    self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkDirMTimeFileNum.xlsx', 1)

                    # 2. 定义回调函数
                    def processing_callback(future, ip, file_path):
                        try:
                            result = future.result()
                            logger.info(f"成功处理 {ip} 的目录: {file_path} - 文件数: {result}")
                            return result
                        except Exception as e:
                            logger.error(f"处理 {ip} 的 {file_path} 时出错: {str(e)}")
                            return None

                    # 3. 主处理函数
                    def process_directory_data():
                        # 获取各列数据(跳过表头)
                        row_count = len(self.cus_excel_op.get_column_values(1)) - 1
                        columns = {
                            'ip': [self.cus_excel_op.get_cell_value(i + 2, 4) for i in range(row_count)],
                            'user': [self.cus_excel_op.get_cell_value(i + 2, 6) for i in range(row_count)],
                            'pwd': [self.cus_excel_op.get_cell_value(i + 2, 7) for i in range(row_count)],
                            'port': [self.cus_excel_op.get_cell_value(i + 2, 8) for i in range(row_count)],
                            'file_depth': [self.cus_excel_op.get_cell_value(i + 2, 9) for i in range(row_count)],
                            'file_path': [self.cus_excel_op.get_cell_value(i + 2, 10) for i in range(row_count)]
                        }

                        # 初始化设备字典
                        self.lv_dic01 = {}
                        for ip, user, pwd, port, depth, path in zip(
                                columns['ip'], columns['user'], columns['pwd'],
                                columns['port'], columns['file_depth'], columns['file_path']):

                            if ip not in self.lv_dic01:
                                self.lv_dic01[ip] = {
                                    'attr': [],
                                    'usr': user,
                                    'pwd': pwd,
                                    'port': port
                                }

                            self.lv_dic01[ip]['attr'].append([
                                {'fileDepth': depth},
                                {'fileName': path},
                                {'fileCount': 0},  # 初始值
                                {'dirchangetime': 0}  # 初始值
                            ])

                        # 多线程处理目录检查
                        with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
                            futures = []
                            total_tasks = sum(len(data['attr']) for data in self.lv_dic01.values())
                            completed = 0

                            # 提交任务
                            for ip, ip_data in self.lv_dic01.items():
                                for idx, attr in enumerate(ip_data['attr']):
                                    file_path = attr[1]['fileName']
                                    future = executor.submit(
                                        self.def_connect_dir_mtime_filenum, ip, attr, idx)
                                    future.add_done_callback(
                                        lambda f, ipl=ip, fp=file_path: processing_callback(f, ipl, fp))
                                    futures.append(future)

                            # 显示进度并处理结果
                            for future in as_completed(futures):
                                completed += 1
                                logger.info(f"处理进度: {completed}/{total_tasks} ({completed / total_tasks:.1%})")

                                try:
                                    result = future.result()
                                    if result:
                                        ip, idx = result['ip'], result['idx']
                                        self.lv_dic01[ip]['attr'][idx][2]['fileCount'] = result.get('fileCount', 0)
                                        self.lv_dic01[ip]['attr'][idx][3]['dirchangetime'] = result.get('dirchangetime', 0)
                                except Exception as e:
                                    logger.error(f"处理结果时出错: {str(e)}")

                        # 准备Zabbix数据
                        state_resources = []
                        dic_replace = {".": "__", "/": "__", "%": "", "$": "", "\"": "",
                                       "+": "", "(": "", ")": "", " ": ""}

                        for ip, ip_data in self.lv_dic01.items():
                            for attr in ip_data['attr']:
                                ip_clean = self.cus_localMethord.def_batch_replace(ip, dic_replace)
                                path_clean = self.cus_localMethord.def_batch_replace(
                                    attr[1]['fileName'], dic_replace)

                                # 文件数监控项
                                key_queue = f"queueDepth.[{ip_clean}__{path_clean}]"
                                state_resources.append(
                                    f"\"{host}\" \"{key_queue}\" {int(time.time())} {attr[2]['fileCount']}")

                                # 目录修改时间监控项
                                key_time = f"dirchangetime.[{ip_clean}__{path_clean}]"
                                state_resources.append(
                                    f"\"{host}\" \"{key_time}\" {int(time.time())} {attr[3]['dirchangetime']}")

                        # 发送数据到Zabbix
                        if state_resources:
                            self.cus_zabbixSender.def_send_data_to_zabbix(
                                'dirMTimeFileNum', state_resources, host)
                            logger.info(f"成功发送 {len(state_resources)} 条目录监控数据到Zabbix")
                        else:
                            logger.warning("没有收集到有效的目录监控数据")

                    # 执行主处理逻辑
                    process_directory_data()

                except Exception as e:
                    logger.error(f"处理dirMTimeFileNum资源时发生错误: {str(e)}")
                    raise
            elif ['dirFileNum'].count(resource) == 1:
                try:
                    # 1. 加载Excel数据
                    self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkDirFileNum.xlsx', 1)

                    # 2. 定义回调函数
                    def filecount_callback(future, ip, dir_path):
                        """处理文件数统计结果的回调函数"""
                        try:
                            result = future.result()
                            logger.info(f"成功统计 {ip} 的目录 {dir_path} 文件数: {result}")
                            return result
                        except Exception as e:
                            logger.error(f"统计 {ip} 的 {dir_path} 文件数时出错: {str(e)}")
                            return None

                    # 3. 主处理函数
                    def process_directory_files():
                        # 获取各列数据(跳过表头)
                        row_count = len(self.cus_excel_op.get_column_values(1)) - 1
                        columns = {
                            'ip': [self.cus_excel_op.get_cell_value(i + 2, 7) for i in range(row_count)],
                            'user': [self.cus_excel_op.get_cell_value(i + 2, 9) for i in range(row_count)],
                            'pwd': [self.cus_excel_op.get_cell_value(i + 2, 10) for i in range(row_count)],
                            'port': [self.cus_excel_op.get_cell_value(i + 2, 11) for i in range(row_count)],
                            'file_depth': [self.cus_excel_op.get_cell_value(i + 2, 12) for i in range(row_count)],
                            'dir_path': [self.cus_excel_op.get_cell_value(i + 2, 13) for i in range(row_count)]
                        }

                        # 初始化设备字典
                        self.lv_dic01 = {}
                        for ip, user, pwd, port, depth, path in zip(
                                columns['ip'], columns['user'], columns['pwd'],
                                columns['port'], columns['file_depth'], columns['dir_path']):

                            if ip not in self.lv_dic01:
                                self.lv_dic01[ip] = {
                                    'attr': [],
                                    'usr': user,
                                    'pwd': pwd,
                                    'port': port
                                }

                            self.lv_dic01[ip]['attr'].append([
                                {'fileDepth': depth},
                                {'fileName': path},
                                {'fileCount': 0}  # 初始值
                            ])

                        # 多线程处理目录文件数统计
                        with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
                            futures = []
                            total_tasks = sum(len(data['attr']) for data in self.lv_dic01.values())
                            completed = 0

                            # 提交任务
                            for ip, ip_data in self.lv_dic01.items():
                                for idx, attr in enumerate(ip_data['attr']):
                                    dir_path = attr[1]['fileName']
                                    future = executor.submit(
                                        self.def_connect_dir_filenum, ip, attr, idx)
                                    future.add_done_callback(
                                        lambda f, lip=ip, dp=dir_path: filecount_callback(f, lip, dp))
                                    futures.append(future)

                            # 显示进度并处理结果
                            for future in as_completed(futures):
                                completed += 1
                                logger.info(f"处理进度: {completed}/{total_tasks} ({completed / total_tasks:.1%})")

                                try:
                                    result = future.result()
                                    if result:
                                        ip, idx = result['ip'], result['idx']
                                        self.lv_dic01[ip]['attr'][idx][2]['fileCount'] = result.get('fileCount', 0)
                                except Exception as e:
                                    logger.error(f"处理结果时出错: {str(e)}")

                        # 准备Zabbix数据
                        state_resources = []
                        dic_replace = {".": "__", "/": "__", "%": "", "$": "", "\"": "",
                                       "+": "", "(": "", ")": "", " ": ""}

                        for ip, ip_data in self.lv_dic01.items():
                            for attr in ip_data['attr']:
                                ip_clean = self.cus_localMethord.def_batch_replace(ip, dic_replace)
                                path_clean = self.cus_localMethord.def_batch_replace(
                                    attr[1]['fileName'], dic_replace)

                                # 文件数监控项
                                key = f"dirFileNum.[{ip_clean}__{path_clean}]"
                                state_resources.append(
                                    f"\"{host}\" \"{key}\" {int(time.time())} {attr[2]['fileCount']}")

                        # 发送数据到Zabbix
                        if state_resources:
                            self.cus_zabbixSender.def_send_data_to_zabbix(
                                'dirFileNum', state_resources, host)
                            logger.info(f"成功发送 {len(state_resources)} 条目录文件数数据到Zabbix")
                        else:
                            logger.warning("没有收集到有效的目录文件数数据")

                    # 执行主处理逻辑
                    process_directory_files()

                except Exception as e:
                    logger.error(f"处理dirFileNum资源时发生错误: {str(e)}")
                    raise
            elif ['dirMTime'].count(resource) == 1:
                try:
                    # 1. 加载Excel数据
                    self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkDirMTime.xlsx', 1)

                    # 2. 定义回调函数
                    def mtime_callback(future, ip, dir_path):
                        """处理目录修改时间检查的回调函数"""
                        try:
                            result = future.result()
                            logger.info(f"成功获取 {ip} 的目录 {dir_path} 修改时间: {result}")
                            return result
                        except Exception as e:
                            logger.error(f"获取 {ip} 的 {dir_path} 修改时间时出错: {str(e)}")
                            return None

                    # 3. 主处理函数
                    def process_directory_mtime():
                        # 获取各列数据(跳过表头)
                        row_count = len(self.cus_excel_op.get_column_values(1)) - 1
                        columns = {
                            'ip': [self.cus_excel_op.get_cell_value(i + 2, 7) for i in range(row_count)],
                            'user': [self.cus_excel_op.get_cell_value(i + 2, 9) for i in range(row_count)],
                            'pwd': [self.cus_excel_op.get_cell_value(i + 2, 10) for i in range(row_count)],
                            'port': [self.cus_excel_op.get_cell_value(i + 2, 11) for i in range(row_count)],
                            'dir_path': [self.cus_excel_op.get_cell_value(i + 2, 13) for i in range(row_count)]
                        }

                        # 初始化设备字典
                        self.lv_dic01 = {}
                        for ip, user, pwd, port, path in zip(
                                columns['ip'], columns['user'], columns['pwd'],
                                columns['port'], columns['dir_path']):

                            if ip not in self.lv_dic01:
                                self.lv_dic01[ip] = {
                                    'attr': [],
                                    'usr': user,
                                    'pwd': pwd,
                                    'port': port
                                }

                            self.lv_dic01[ip]['attr'].append([
                                {'dirName': path},
                                {'dirMTime': '-999'}  # 初始值
                            ])

                        # 多线程处理目录修改时间检查
                        with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
                            futures = []
                            total_tasks = sum(len(data['attr']) for data in self.lv_dic01.values())
                            completed = 0

                            # 提交任务
                            for ip, ip_data in self.lv_dic01.items():
                                for idx, attr in enumerate(ip_data['attr']):
                                    dir_path = attr[0]['dirName']
                                    future = executor.submit(
                                        self.def_connect_dir_mtime, ip, attr, idx)
                                    future.add_done_callback(
                                        lambda f, lip=ip, dp=dir_path: mtime_callback(f, lip, dp))
                                    futures.append(future)

                            # 显示进度并处理结果
                            for future in as_completed(futures):
                                completed += 1
                                logger.info(f"处理进度: {completed}/{total_tasks} ({completed / total_tasks:.1%})")

                                try:
                                    result = future.result()
                                    if result:
                                        ip, idx = result['ip'], result['idx']
                                        self.lv_dic01[ip]['attr'][idx][1]['dirMTime'] = result.get('dirMTime', '-999')
                                except Exception as e:
                                    logger.error(f"处理结果时出错: {str(e)}")

                        # 准备Zabbix数据
                        state_resources = []
                        dic_replace = {".": "__", "/": "__", "%": "", "$": "", "\"": "",
                                       "+": "", "(": "", ")": "", " ": ""}

                        for ip, ip_data in self.lv_dic01.items():
                            for attr in ip_data['attr']:
                                ip_clean = self.cus_localMethord.def_batch_replace(ip, dic_replace)
                                path_clean = self.cus_localMethord.def_batch_replace(
                                    attr[0]['dirName'], dic_replace)
                                IPLIST = [ip_clean, path_clean]
                                STR_IPLIST = "__".join(IPLIST)
                                key = f"dirMTime.[{STR_IPLIST}]"
                                state_resources.append(
                                    f"\"{host}\" \"{key}\" {int(time.time())} {attr[1]['dirMTime']}")

                        # 发送数据到Zabbix
                        if state_resources:
                            self.cus_zabbixSender.def_send_data_to_zabbix(
                                'dirMTime', state_resources, host)
                            logger.info(f"成功发送 {len(state_resources)} 条目录修改时间数据到Zabbix")
                        else:
                            logger.warning("没有收集到有效的目录修改时间数据")

                    # 执行主处理逻辑
                    process_directory_mtime()

                except Exception as e:
                    logger.error(f"处理dirMTime资源时发生错误: {str(e)}")
                    raise
            elif ['linuxMount'].count(resource) == 1:
                try:
                    # 1. 加载Excel数据
                    self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkLinuxMount.xlsx', 1)

                    # 2. 定义回调函数
                    def mount_status_callback(future, ip, mount_path):
                        """处理挂载点状态检查的回调函数"""
                        try:
                            result = future.result()
                            status = "正常" if result else "异常"
                            logger.info(f"成功检查 {ip} 的挂载点 {mount_path} 状态: {status}")
                            return result
                        except Exception as e:
                            logger.error(f"检查 {ip} 的 {mount_path} 挂载状态时出错: {str(e)}")
                            return None

                    # 3. 主处理函数
                    def process_mount_status():
                        # 获取各列数据(跳过表头)
                        row_count = len(self.cus_excel_op.get_column_values(1)) - 1
                        columns = {
                            'ip': [self.cus_excel_op.get_cell_value(i + 2, 4) for i in range(row_count)],
                            'user': [self.cus_excel_op.get_cell_value(i + 2, 6) for i in range(row_count)],
                            'pwd': [self.cus_excel_op.get_cell_value(i + 2, 7) for i in range(row_count)],
                            'port': [self.cus_excel_op.get_cell_value(i + 2, 8) for i in range(row_count)],
                            'mount_path': [self.cus_excel_op.get_cell_value(i + 2, 10) for i in range(row_count)]
                        }

                        # 初始化设备字典
                        self.lv_dic01 = {}
                        for ip, user, pwd, port, path in zip(
                                columns['ip'], columns['user'], columns['pwd'],
                                columns['port'], columns['mount_path']):

                            if ip not in self.lv_dic01:
                                self.lv_dic01[ip] = {
                                    'attr': [],
                                    'usr': user,
                                    'pwd': pwd,
                                    'port': port
                                }

                            self.lv_dic01[ip]['attr'].append([
                                {'mountPath': path},
                                {'mountStatus': '异常'}  # 初始值
                            ])

                        # 多线程处理挂载点状态检查
                        with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
                            futures = []
                            total_tasks = sum(len(data['attr']) for data in self.lv_dic01.values())
                            completed = 0

                            # 提交任务
                            for ip, ip_data in self.lv_dic01.items():
                                for idx, attr in enumerate(ip_data['attr']):
                                    mount_path = attr[0]['mountPath']
                                    future = executor.submit(
                                        self.def_connect_linux_mount, ip, attr, idx)
                                    future.add_done_callback(
                                        lambda f, lip=ip, mp=mount_path: mount_status_callback(f, lip, mp))
                                    futures.append(future)

                            # 显示进度并处理结果
                            for future in as_completed(futures):
                                completed += 1
                                logger.info(f"处理进度: {completed}/{total_tasks} ({completed / total_tasks:.1%})")

                                try:
                                    result = future.result()
                                    if result is not None:
                                        ip, idx = result['ip'], result['idx']
                                        self.lv_dic01[ip]['attr'][idx][1]['mountStatus'] = "正常" if result else "异常"
                                except Exception as e:
                                    logger.error(f"处理结果时出错: {str(e)}")

                        # 准备Zabbix数据
                        state_resources = []
                        dic_replace = {".": "__", "/": "__", "%": "", "$": "", "\"": "",
                                       "+": "", "(": "", ")": "", " ": ""}

                        for ip, ip_data in self.lv_dic01.items():
                            for attr in ip_data['attr']:
                                ip_clean = self.cus_localMethord.def_batch_replace(ip, dic_replace)
                                path_clean = self.cus_localMethord.def_batch_replace(
                                    attr[0]['mountPath'], dic_replace)

                                key = f"mountstatus.[{ip_clean}__{path_clean}]"
                                state_resources.append(
                                    f"\"{host}\" \"{key}\" {int(time.time())} {attr[1]['mountStatus']}")

                        # 发送数据到Zabbix
                        if state_resources:
                            self.cus_zabbixSender.def_send_data_to_zabbix(
                                'linuxMount', state_resources, host)
                            logger.info(f"成功发送 {len(state_resources)} 条挂载状态数据到Zabbix")
                        else:
                            logger.warning("没有收集到有效的挂载状态数据")

                    # 执行主处理逻辑
                    process_mount_status()

                except Exception as e:
                    logger.error(f"处理linuxMount资源时发生错误: {str(e)}")
                    raise
            elif ['linuxPs'].count(resource) == 1:
                try:
                    # 1. 加载Excel数据
                    self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkLinuxPs.xlsx', 1)

                    # 2. 定义回调函数
                    def process_status_callback(future, ip, process_path):
                        """处理进程状态检查的回调函数"""
                        try:
                            result = future.result()
                            status = "正常" if result else "异常"
                            logger.info(f"成功检查 {ip} 的进程 {process_path} 状态: {status}")
                            return result
                        except Exception as e:
                            logger.error(f"检查 {ip} 的 {process_path} 进程状态时出错: {str(e)}")
                            return None

                    # 3. 主处理函数
                    def process_ps_status():
                        # 获取各列数据(跳过表头)
                        row_count = len(self.cus_excel_op.get_column_values(1)) - 1
                        columns = {
                            'ip': [self.cus_excel_op.get_cell_value(i + 2, 4) for i in range(row_count)],
                            'user': [self.cus_excel_op.get_cell_value(i + 2, 6) for i in range(row_count)],
                            'pwd': [self.cus_excel_op.get_cell_value(i + 2, 7) for i in range(row_count)],
                            'port': [self.cus_excel_op.get_cell_value(i + 2, 8) for i in range(row_count)],
                            'process_path': [self.cus_excel_op.get_cell_value(i + 2, 10) for i in range(row_count)]
                        }

                        # 初始化设备字典
                        self.lv_dic01 = {}
                        for ip, user, pwd, port, path in zip(
                                columns['ip'], columns['user'], columns['pwd'],
                                columns['port'], columns['process_path']):

                            if ip not in self.lv_dic01:
                                self.lv_dic01[ip] = {
                                    'attr': [],
                                    'usr': user,
                                    'pwd': pwd,
                                    'port': port
                                }

                            self.lv_dic01[ip]['attr'].append([
                                {'psPath': path},
                                {'psStatus': '异常'}  # 初始值
                            ])

                        # 多线程处理进程状态检查
                        with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
                            futures = []
                            total_tasks = sum(len(data['attr']) for data in self.lv_dic01.values())
                            completed = 0

                            # 提交任务
                            for ip, ip_data in self.lv_dic01.items():
                                for idx, attr in enumerate(ip_data['attr']):
                                    process_path = attr[0]['psPath']
                                    future = executor.submit(
                                        self.def_connect_linux_ps, ip, attr, idx)
                                    future.add_done_callback(
                                        lambda f, lip=ip, pp=process_path: process_status_callback(f, lip, pp))
                                    futures.append(future)

                            # 显示进度并处理结果
                            for future in as_completed(futures):
                                completed += 1
                                progress = f"处理进度: {completed}/{total_tasks} ({completed / total_tasks:.1%})"
                                logger.info(progress)
                                print(f"\r{progress}", end="", flush=True)

                                try:
                                    result = future.result()
                                    if result is not None:
                                        ip, idx = result['ip'], result['idx']
                                        self.lv_dic01[ip]['attr'][idx][1]['psStatus'] = "正常" if result else "异常"
                                except Exception as e:
                                    logger.error(f"处理结果时出错: {str(e)}")
                            print()  # 换行

                        # 准备Zabbix数据
                        state_resources = []
                        dic_replace = {".": "__", "/": "__", "%": "", "$": "", "\"": "",
                                       "+": "", "(": "", ")": "", " ": ""}

                        for ip, ip_data in self.lv_dic01.items():
                            for attr in ip_data['attr']:
                                ip_clean = self.cus_localMethord.def_batch_replace(ip, dic_replace)
                                path_clean = self.cus_localMethord.def_batch_replace(
                                    attr[0]['psPath'], dic_replace)

                                key = f"psStatus.[{ip_clean}__{path_clean}]"
                                state_resources.append(
                                    f"\"{host}\" \"{key}\" {int(time.time())} {attr[1]['psStatus']}")

                        # 发送数据到Zabbix
                        if state_resources:
                            self.cus_zabbixSender.def_send_data_to_zabbix(
                                'linuxPs', state_resources, host)
                            logger.info(f"成功发送 {len(state_resources)} 条进程状态数据到Zabbix")
                        else:
                            logger.warning("没有收集到有效的进程状态数据")

                    # 执行主处理逻辑
                    process_ps_status()

                except Exception as e:
                    logger.error(f"处理linuxPs资源时发生错误: {str(e)}")
                    raise
            else:
                logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], u'没有匹配的自动发现规则'))


class CusSftpClient(object):
    def __init__(self, ):
        self.sftpClient = None
        self.sftp = None
        self.sftpCount = 0
        self.zabbix_sender = CusZabbixSender()
        self.cus_excel_op = CusExcelOp()
        self.cus_excel_op.create_new_workbook()
        self.local_methord = CusLocalMethod()

    def def_connect(self, ip, user, password, port, queueDepth, remote):
        try:
            timeout = 5
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((ip, port))
            self.sftpClient = paramiko.Transport(sock)
            self.sftpClient.connect(username=user, password=password)
            self.sftp = paramiko.SFTPClient.from_transport(self.sftpClient)
            self.sftpCount = 0
            self.def_get(int(queueDepth), str(remote))
            time.sleep(0.1)
            self.sftpClient.close()
            return self.sftpCount
        except Exception as e:
            print(e)
            pattern = re.compile(r'Authentication failed.*')
            result = re.findall(pattern, str(e))
            if len(result) != 0:
                self.sftpCount = 100001  # Authentication failed.
                return self.sftpCount
            pattern = re.compile(r'.*No such file')
            result = re.findall(pattern, str(e))
            if len(result) != 0:
                self.sftpCount = 100002  # [Errno 2] No such file
                return self.sftpCount
            pattern = re.compile(r'.*Connection refused')
            result = re.findall(pattern, str(e))
            if len(result) != 0:
                self.sftpCount = 100003  # [Errno 111] Connection refused
                return self.sftpCount
            pattern = re.compile(r'timed out.*')
            result = re.findall(pattern, str(e))
            if len(result) != 0:
                self.sftpCount = 100004  # timed out
                return self.sftpCount

    def def_get(self, queueDepth, remote):
        # 检查远程文件是否存在
        result = self.sftp.stat(remote)
        if isdir(result.st_mode):
            for file in self.sftp.listdir(remote):
                sub_remote = os.path.join(remote, file)
                sub_remote = sub_remote.replace('\\', '/')
                self.def_get(queueDepth, sub_remote)
        else:
            # 拷贝文件
            pattern = re.compile(r'^/\..*')
            result = re.findall(pattern, str(remote))
            if len(result) == 0:
                self.sftpCount = self.sftpCount + 1
                if self.sftpCount > queueDepth:
                    self.sftpCount = 999999
                    return self.sftpCount

    def def_discovering_resources(self, host, list_resources):
        for resource in list_resources:
            if ['queueDepth'].count(resource) == 1:
                self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkFileCount.xlsx', 1)

                column_1_list = self.cus_excel_op.get_column_values(1)
                del column_1_list[0]
                column_2_list = []
                column_3_list = []
                column_4_list = []
                column_6_list = []
                column_7_list = []
                column_8_list = []
                column_9_list = []
                column_10_list = []

                for i in range(len(column_1_list)):
                    column_1_list.append(self.cus_excel_op.get_cell_value(i + 2, 1))  # 通道ID
                    column_2_list.append(self.cus_excel_op.get_cell_value(i + 2, 2))  # 通道从哪
                    column_3_list.append(self.cus_excel_op.get_cell_value(i + 2, 3))  # 通道到哪
                    column_4_list.append(self.cus_excel_op.get_cell_value(i + 2, 4))  # 属地通道IP地址
                    column_6_list.append(self.cus_excel_op.get_cell_value(i + 2, 6))  # 用户名
                    column_7_list.append(self.cus_excel_op.get_cell_value(i + 2, 7))  # 密码
                    column_8_list.append(self.cus_excel_op.get_cell_value(i + 2, 8))  # 端口
                    column_9_list.append(self.cus_excel_op.get_cell_value(i + 2, 9))  # 告警文件数
                    column_10_list.append(self.cus_excel_op.get_cell_value(i + 2, 10))  # 监控目录

                discovered_resource = []
                for col_01 in range(len(column_4_list)):
                    one_object_list = {}
                    one_object_list["{#IPLIST}"] = str(column_4_list[col_01].replace(".", "__")) + "__" + \
                                                   column_10_list[col_01].replace("/", "__")
                    one_object_list["{#ADDRESSLIST}"] = str(column_1_list[col_01]) + "__" + \
                                                        column_2_list[col_01] + "__" + \
                                                        column_3_list[col_01] + "__" + \
                                                        column_10_list[col_01].replace("/", "__")
                    discovered_resource.append(one_object_list)
                converted_resource = self.zabbix_sender.def_convert_to_zabbix_json(discovered_resource)
                xer = []
                timestampnow = int(time.time())
                TIMESTAMPNOW = timestampnow
                xer.append("%s %s %s %s" % (host, resource, timestampnow, converted_resource))
                # print(xer)
                self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, xer, host)

    def def_get_status_resources(self, host, list_resources):
        for resource in list_resources:
            if ['queueDepth'].count(resource) == 1:
                try:
                    # 1. 加载Excel数据
                    self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkFileCount.xlsx', 1)

                    # 2. 定义回调函数
                    def filecount_callback(future, ip, file_path, index, total):
                        """处理文件数统计结果的回调函数"""
                        try:
                            result = future.result()
                            progress = f"[{index + 1}/{total}] {ip}:{file_path} - 文件数: {result}"
                            logger.info(progress)
                            print(f"\r{progress}", end="", flush=True)
                            return result
                        except Exception as e:
                            error_msg = f"处理 {ip} 的 {file_path} 时出错: {str(e)}"
                            logger.error(error_msg)
                            print(f"\r{error_msg}", end="", flush=True)
                            return None

                    # 3. 获取各列数据(跳过表头)
                    column_1_list = self.cus_excel_op.get_column_values(1)[1:]
                    column_4_list = [self.cus_excel_op.get_cell_value(i + 2, 4) for i in range(len(column_1_list))]  # IP地址
                    column_6_list = [self.cus_excel_op.get_cell_value(i + 2, 6) for i in range(len(column_1_list))]  # 用户名
                    column_7_list = [self.cus_excel_op.get_cell_value(i + 2, 7) for i in range(len(column_1_list))]  # 密码
                    column_8_list = [self.cus_excel_op.get_cell_value(i + 2, 8) for i in range(len(column_1_list))]  # 端口
                    column_9_list = [self.cus_excel_op.get_cell_value(i + 2, 9) for i in range(len(column_1_list))]  # 告警文件数
                    column_10_list = [self.cus_excel_op.get_cell_value(i + 2, 10) for i in range(len(column_1_list))]  # 监控目录

                    # 4. 多线程处理文件数统计
                    lv_listGetAllSftCount = []
                    total_tasks = len(column_4_list)

                    with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
                        futures = []
                        for idx, (ip, user, pwd, port, depth, path) in enumerate(
                                zip(column_4_list, column_6_list, column_7_list,
                                    column_8_list, column_9_list, column_10_list)):
                            future = executor.submit(
                                self.def_connect, ip, user, pwd, port, depth, path)
                            future.add_done_callback(
                                lambda f, lip=ip, fp=path, i=idx, t=total_tasks:
                                filecount_callback(f, lip, fp, i, t))
                            futures.append(future)

                        # 等待所有任务完成
                        for future in as_completed(futures):
                            try:
                                result = future.result()
                                if result is not None:
                                    lv_listGetAllSftCount.append(result)
                            except Exception:
                                continue

                    # 5. 准备Zabbix数据
                    timestampnow = int(time.time())
                    state_resources = []
                    for idx in range(len(column_4_list)):
                        ip_clean = column_4_list[idx].replace(".", "__")
                        path_clean = column_10_list[idx].replace("/", "__")
                        key = f"queueDepth.[{ip_clean}__{path_clean}]"
                        state_resources.append(
                            f"\"{host}\" \"{key}\" {timestampnow} {lv_listGetAllSftCount[idx]}")

                    # 6. 发送数据到Zabbix
                    if state_resources:
                        self.zabbix_sender.def_send_data_to_zabbix(
                            timestampnow, state_resources, host)
                        logger.info(f"成功发送 {len(state_resources)} 条队列深度数据到Zabbix")
                    else:
                        logger.warning("没有收集到有效的队列深度数据")

                except Exception as e:
                    logger.error(f"处理queueDepth资源时发生错误: {str(e)}")
                    raise


class CusLinuxClient(object):
    def __init__(self, ):
        self.zabbix_sender = CusZabbixSender()
        self.cus_excel_op = CusExcelOp()
        self.cus_excel_op.create_new_workbook()
        self.local_methord = CusLocalMethod()

    def def_cmd(self, command):
        result = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        return result

    def def_discovering_resources(self, host, list_resources):
        for resource in list_resources:
            if ['linux_df'].count(resource) == 1:
                cmdline = self.def_cmd("""df | awk -v OFS=',' '{{print $6,$2,$5}}'""")
                time.sleep(0.1)
                if len(cmdline.stderr.read().strip()) > 0:
                    logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], cmdline.stderr.read().strip()))
                    sys.exit("{0}".format(inspect.currentframe().f_lineno))
                else:
                    logger.info("Starting discovering resource - {0}".format(resource))
                    title_name = ['index', 'name', 'size', 'used']
                    self.cus_excel_op.create_sheet(resource)
                    [self.cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
                    res_01 = cmdline.stdout.read().strip().split('\n')
                    del res_01[0]
                    for i_01 in range(len(res_01)):
                        res_02 = res_01[i_01].split(',')
                        self.cus_excel_op.set_cell_value(i_01 + 2, 1, i_01 + 1)
                        for i_02 in range(len(res_02)):
                            self.cus_excel_op.set_cell_value(i_01 + 2, i_02 + 2, res_02[i_02])

                    discovered_resource = []
                    col_01_list = self.cus_excel_op.get_column_values(2)
                    del col_01_list[0]
                    for col_01 in col_01_list:
                        one_object_list = {}
                        one_object_list["{#MOUNTED}"] = col_01.replace("/", "_")
                        discovered_resource.append(one_object_list)
                    logger.info("Succes get resource - {0}".format(resource))
                    converted_resource = self.zabbix_sender.def_convert_to_zabbix_json(discovered_resource)
                    xer = []
                    TIMESTAMPNOW = int(time.time())
                    xer.append("%s %s %s %s" % (host, resource, TIMESTAMPNOW, converted_resource))
                    # print(xer)
                    self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, xer, host)
                    print("df done")
            elif ['linux_netstat'].count(resource) == 1:
                cmdline = self.def_cmd("""netstat -ntlp | awk -v OFS=',' '{{print $7,$4,$6}}'""")
                time.sleep(0.1)
                # print(cmdline.stdout.read().strip())
                if len(cmdline.stderr.read().strip()) > 0:
                    # print(cmdline.stdout.read().strip())
                    logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], cmdline.stderr.read().strip()))
                    sys.exit("{0}".format(inspect.currentframe().f_lineno))
                else:
                    logger.info("Starting discovering resource - {0}".format(resource))
                    title_name = ['index', 'name', 'ip', 'port', 'state']
                    self.cus_excel_op.create_sheet(resource)
                    [self.cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
                    pattern = re.compile(r'\d*/(\w*).*,(.*):(\d*),(\w*)n*')
                    result = re.findall(pattern, cmdline.stdout.read().strip())
                    # 去重
                    unit_column_1_list = list(set(result))
                    # 使用index保持不乱序
                    unit_column_1_list.sort(key=result.index)
                    for i_01 in range(0, len(unit_column_1_list)):
                        self.cus_excel_op.set_cell_value(i_01 + 2, 1, i_01 + 1)
                        for i_02 in range(0, len(unit_column_1_list[i_01])):
                            self.cus_excel_op.set_cell_value(i_01 + 2, i_02 + 2, unit_column_1_list[i_01][i_02].replace("/", "-"))
                    discovered_resource = []
                    col_02_list = self.cus_excel_op.get_column_values(2)
                    del col_02_list[0]
                    col_03_list = self.cus_excel_op.get_column_values(4)
                    del col_03_list[0]
                    col_04_list = self.cus_excel_op.get_column_values(3)
                    del col_04_list[0]
                    for len_col_01 in range(len(col_02_list)):
                        one_object_list = {}
                        one_object_list["{#NAME}"] = col_02_list[len_col_01].replace("/", "-") + '_' + col_03_list[len_col_01]
                        discovered_resource.append(one_object_list)
                    logger.info("Succes get resource - {0}".format(resource))
                    converted_resource = self.zabbix_sender.def_convert_to_zabbix_json(discovered_resource)
                    xer = []
                    TIMESTAMPNOW = int(time.time())
                    xer.append("%s %s %s %s" % (host, resource, TIMESTAMPNOW, converted_resource))
                    # print(xer)
                    self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, xer, host)
                    print("netstat done")
            elif ['linux_checkping'].count(resource) == 1:
                logger.info("Starting discovering resource - {0}".format(resource))
                self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkping.xlsx', 1)
                col_02_list = self.cus_excel_op.get_column_values(1)
                del col_02_list[0]
                col_01_list = self.cus_excel_op.get_column_values(2)
                del col_01_list[0]
                col_03_list = self.cus_excel_op.get_column_values(3)
                del col_03_list[0]
                discovered_resource = []
                for len_col_01 in range(len(col_02_list)):
                    one_object_list = {}
                    one_object_list["{#NAME}"] = col_01_list[len_col_01]
                    one_object_list["{#INDEX}"] = col_02_list[len_col_01]
                    discovered_resource.append(one_object_list)
                logger.info("Succes get resource - {0}".format(resource))
                converted_resource = self.zabbix_sender.def_convert_to_zabbix_json(discovered_resource)
                xer = []
                TIMESTAMPNOW = int(time.time())
                xer.append("%s %s %s %s" % ("\"" + host + "\"", "\"" + resource + "\"", TIMESTAMPNOW, converted_resource))
                print(discovered_resource)
                self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, xer, host)
                print("checkping done")
            else:
                logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], u'没有匹配的自动发现规则'))
                print(u"错误: {0} {1}".format(inspect.stack()[0][2], u'没有匹配的自动发现规则'))
        # self.cus_excel_op.def_save_create_xlsx(XLSX_FILENAME)

    def def_get_status_resources(self, host, list_resources):
        # try:
        for resource in list_resources:
            if ['linux_df'].count(resource) == 1:
                cmdline = self.def_cmd("""df | awk -v OFS=',' '{{print $6,$2,$5}}'""")
                time.sleep(0.1)
                if len(cmdline.stderr.read().strip()) > 0:
                    logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], cmdline.stderr.read().strip()))
                    sys.exit("{0}".format(inspect.currentframe().f_lineno))
                else:
                    logger.info("Starting collecting status of resource - {0}".format(resource))

                    title_name = ['index', 'name', 'size', 'used']
                    self.cus_excel_op.create_sheet(resource)
                    [self.cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
                    res_01 = cmdline.stdout.read().strip().split('\n')
                    del res_01[0]
                    for i_01 in range(len(res_01)):
                        res_02 = res_01[i_01].split(',')
                        self.cus_excel_op.set_cell_value(i_01 + 2, 1, i_01 + 1)
                        for i_02 in range(len(res_02)):
                            self.cus_excel_op.set_cell_value(i_01 + 2, i_02 + 2, res_02[i_02])

                    col_02_list = self.cus_excel_op.get_column_values(2)
                    del col_02_list[0]
                    col_03_list = self.cus_excel_op.get_column_values(3)
                    del col_03_list[0]
                    col_04_list = self.cus_excel_op.get_column_values(4)
                    del col_04_list[0]
                    TIMESTAMPNOW = int(time.time())
                    state_resources = []
                    for len_col_01 in range(len(col_02_list)):
                        key_size = "size.{0}[{1}]".format(resource, col_02_list[len_col_01].replace("/", "_"))
                        key_used = "used.{0}[{1}]".format(resource, col_02_list[len_col_01].replace("/", "_"))
                        state_resources.append("%s %s %s %s" % ("\"" + host + "\"", "\"" + key_size + "\"", TIMESTAMPNOW, col_03_list[len_col_01]))
                        state_resources.append("%s %s %s %s" % ("\"" + host + "\"", "\"" + key_used + "\"", TIMESTAMPNOW, col_04_list[len_col_01].replace("%", "")))
                    self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, state_resources, host)
                    print("df done")
            elif ['linux_netstat'].count(resource) == 1:
                cmdline = self.def_cmd("""netstat -ntlp | awk -v OFS=',' '{{print $7,$4,$6}}'""")
                time.sleep(0.1)
                if len(cmdline.stderr.read().strip()) > 0:
                    logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], cmdline.stderr.read().strip()))
                    sys.exit("{0}".format(inspect.currentframe().f_lineno))
                else:
                    logger.info("Starting collecting status of resource - {0}".format(resource))

                    title_name = ['index', 'name', 'ip', 'port', 'state']
                    self.cus_excel_op.create_sheet(resource)
                    [self.cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
                    cmd_stdout = cmdline.stdout.read().strip()
                    pattern = re.compile(r'\d*/(\w*).*,(.*):(\d*),(\w*)n*')
                    result = re.findall(pattern, cmd_stdout)
                    # 去重
                    unit_column_1_list = list(set(result))
                    # 使用index保持不乱序
                    unit_column_1_list.sort(key=result.index)
                    for i_01 in range(0, len(unit_column_1_list)):
                        self.cus_excel_op.set_cell_value(i_01 + 2, 1, i_01 + 1)
                        for i_02 in range(0, len(unit_column_1_list[i_01])):
                            self.cus_excel_op.set_cell_value(i_01 + 2, i_02 + 2, unit_column_1_list[i_01][i_02].replace("/", "-"))
                            if i_02 == 3:
                                cmdline = self.def_cmd("""tcping {0} {1}""".format(self.local_methord.def_convert_text_to_text(unit_column_1_list[i_01][i_02 - 2]), unit_column_1_list[i_01][i_02 - 1]))
                                time.sleep(0.1)
                                pattern = re.compile(r'.*(open|closed).*')
                                cmd_stdout = cmdline.stdout.read().strip()
                                result = re.search(pattern, cmd_stdout)
                                if self.local_methord.def_convert_text_to_numeric(result.group(1)) == 0 and \
                                        self.local_methord.def_convert_text_to_numeric(unit_column_1_list[i_01][i_02]) == 0:
                                    self.cus_excel_op.set_cell_value(i_01 + 2, i_02 + 2, 0)
                                else:
                                    self.cus_excel_op.set_cell_value(i_01 + 2, i_02 + 2, 1)
                    col_02_list = self.cus_excel_op.get_column_values(2)
                    del col_02_list[0]
                    col_04_list = self.cus_excel_op.get_column_values(4)
                    del col_04_list[0]
                    col_05_list = self.cus_excel_op.get_column_values(5)
                    del col_05_list[0]
                    TIMESTAMPNOW = int(time.time())
                    state_resources = []
                    for len_col_01 in range(len(col_02_list)):
                        key_state = "state.{0}[{1}]".format(resource, col_02_list[len_col_01] + '_' + col_04_list[len_col_01])
                        state_resources.append("%s %s %s %s" % ("\"" + host + "\"", "\"" + key_state + "\"", TIMESTAMPNOW, col_05_list[len_col_01]))
                    self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, state_resources, host)
                    print("netstat done")
            elif ['linux_checkping'].count(resource) == 1:
                try:
                    logger.info("Starting collecting status of resource - {0}".format(resource))

                    # 1. 加载Excel数据
                    self.cus_excel_op.load_excel('/etc/zabbix/scripts/checkping.xlsx', 1)

                    # 2. 定义回调函数
                    def ping_callback(future, target_ip, host_name):
                        """处理ping结果的回调函数"""
                        try:
                            result = future.result()
                            if result == 9999:
                                logger.error(f"ping {host_name} ({target_ip}) 失败")
                            else:
                                logger.info(f"成功ping通 {host_name} ({target_ip}): {result:.2f}ms")
                            return result
                        except Exception as e:
                            logger.error(f"ping {host_name} ({target_ip}) 时出错: {str(e)}")
                            return 9999.00

                    # 3. 执行ping检测的辅助函数
                    def def_ping_target(target_ip, host_name):
                        """执行ping检测的线程函数"""
                        for i_03 in range(3):  # 重试3次
                            try:
                                response = ping(target_ip, timeout=1, size=56, unit='ms')
                                if response is not None and response is not False:
                                    # 保留2位小数
                                    return round(float(response), 2)
                                else:
                                    logger.warning(f"第 {i_03 + 1} 次ping {host_name} ({target_ip}) 无响应")
                            except Exception as e:
                                logger.warning(f"第 {i_03 + 1} 次ping {host_name} ({target_ip}) 失败: {str(e)}")
                                continue
                        return 9999.00  # 所有重试都失败

                    # 4. 主处理函数
                    def process_ping_check():
                        # 获取各列数据(跳过表头)
                        col_02_list = self.cus_excel_op.get_column_values(1)
                        del col_02_list[0]  # 删除表头
                        col_03_list = self.cus_excel_op.get_column_values(3)
                        del col_03_list[0]  # 删除表头

                        TIMESTAMPNOW = int(time.time())
                        state_resources = []

                        # 多线程处理ping检测
                        with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
                            futures = []
                            total_tasks = len(col_02_list)
                            completed = 0

                            # 提交ping任务
                            for i in range(total_tasks):
                                host_name = col_02_list[i]
                                target_ip = col_03_list[i]

                                future = executor.submit(
                                    def_ping_target, target_ip, host_name
                                )
                                future.add_done_callback(
                                    lambda f, ip=target_ip, name=host_name: ping_callback(f, ip, name)
                                )
                                futures.append((future, host_name, target_ip))

                            # 显示进度并处理结果
                            for future, host_name, target_ip in futures:
                                completed += 1
                                try:
                                    v_result = future.result()
                                    key_state = "{0}.status[{1}]".format(resource, host_name)
                                    logger.info(f"Ping进度: [( {total_tasks}/{completed} ) {completed / total_tasks:.1%} ] {target_ip}  -> {v_result} ")
                                    print((f"Ping进度: [( {total_tasks}/{completed} ) {completed / total_tasks:.1%} ] {target_ip}  -> {v_result} "))
                                    state_resources.append("%s %s %s %s" % (
                                        "\"" + host + "\"",
                                        "\"" + key_state + "\"",
                                        TIMESTAMPNOW,
                                        v_result
                                    ))
                                except Exception as e:
                                    logger.error(f"处理ping结果时出错 (目标: {host_name}): {str(e)}")
                                    # 出错时添加默认值
                                    print((f"Ping进度: [( {total_tasks}/{completed} ) {completed / total_tasks:.1%} ] {target_ip}  -> 9999.00 "))
                                    key_state = "{0}.status[{1}]".format(resource, host_name)
                                    state_resources.append("%s %s %s %s" % (
                                        "\"" + host + "\"",
                                        "\"" + key_state + "\"",
                                        TIMESTAMPNOW,
                                        9999.00
                                    ))

                        # 发送数据到Zabbix
                        if state_resources:
                            self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, state_resources, host)
                            logger.info(f"成功发送 {len(state_resources)} 条ping检测数据到Zabbix")
                        else:
                            logger.warning("没有收集到有效的ping检测数据")

                        print("checkping done")

                    # 执行主处理逻辑
                    process_ping_check()

                except Exception as e:
                    logger.error(f"处理linux_checkping资源时发生错误: {str(e)}")
                    raise
            elif ['linux_test'].count(resource) == 1:
                logger.info("Starting collecting status of resource - {0}".format(resource))
                col_02_list = [{'EventCount': 1, 'Domain': None, "User": "slt1-admin@takenaka.cn", "IPAddress": "192.168.100.1"},
                               {'EventCount': 2, 'Domain': None, "User": "slt2-admin@takenaka.cn", "IPAddress": "192.168.100.2"}]
                TIMESTAMPNOW = int(time.time())
                state_resources = []
                key_Event = "{0}.[1]".format(resource)
                for len_col_01 in range(len(col_02_list)):
                    state_resources.append("%s %s %s %s" % ("\"" + host + "\"", "\"" + key_Event + "\"", TIMESTAMPNOW, col_02_list[len_col_01]))
                    self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, state_resources, host)
                print("test done")

            else:
                logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], u'没有匹配的自动发现规则'))
                print(u"错误: {0} {1}".format(inspect.stack()[0][2], u'没有匹配的自动发现规则'))
        # self.cus_excel_op.def_save_create_xlsx(XLSX_FILENAME)


class CusDirectClient(object):
    def __init__(self, ):
        self.zabbix_sender = CusZabbixSender()
        self.local_methord = CusLocalMethod()

    def def_get_status_resources(self, host, list_resources, value):
        # try:
        for resource in list_resources:
            if ['ssh_login_log'].count(resource) == 1:
                logger.info("Starting collecting status of resource - {0}".format(resource))
                timestampnow = int(time.time())
                TIMESTAMPNOW = timestampnow
                state_resources = []
                state_resources.append("%s %s %s %s" % ("\"" + host + "\"", "ssh_login_log", timestampnow, "\"" + value + "\""))
                self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, state_resources, host)
                print(0)
            else:
                logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], u'没有匹配的自动发现规则'))
                print(1)
        # self.cus_excel_op.def_save_create_xlsx(XLSX_FILENAME)
    # except Exception as pizdec:
    #     logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], pizdec))
    #     sys.exit("{0}".format(inspect.currentframe().f_lineno))


class MyThreadCfgSshComm(threading.Thread):
    def __init__(self, cur_num, total_num, ssh_ip, port, usr, pwd, cmd):
        super(MyThreadCfgSshComm, self).__init__()
        self.cur_num = cur_num
        self.total_num = total_num
        self.ssh_ip = ssh_ip
        self.port = int(port)
        self.username = usr
        self.pwd = pwd
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.cmd = u'{v01}'.format(v01=cmd)

    def def_connect(self, hostname, port, username, password):
        try:
            # print(funcIp)
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            __timeout = 5
            __sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            __sock.settimeout(__timeout)
            __sock.connect((hostname, port))
            ssh_client = paramiko.Transport(__sock)
            if os.path.isfile(password):
                # print('rsa', funcIp, self.lv_dic01[funcIp]['usr'], self.lv_dic01[funcIp]['port'], self.lv_dic01[funcIp]['pwd'])
                # print(self.lv_dic01[funcIp])
                __pkey = paramiko.RSAKey.from_private_key_file(password)
                ssh_client.connect(username=username, pkey=__pkey)
            else:
                # 如果有需要，使用用户名和密码进行身份验证
                # print('pwd', funcIp)
                # print(self.lv_dic01[funcIp])
                ssh_client.connect(username=username, password=password)
            return ssh_client
            # pattern = re.compile(r'.*')
            # result = re.findall(pattern, stdout)
            # self.fileCount = stdout
        except Exception as e:
            print(e)

    def run(self):
        try:
            cus_ssh_client = self.def_connect(hostname=self.ssh_ip, port=self.port, username=self.username, password=self.pwd)
            ssh_channel = cus_ssh_client.open_channel(kind='session')
            ssh_channel.settimeout(60)
            list_cmd = self.cmd.split('\n')
            ssh_channel.get_pty()
            ssh_channel.invoke_shell()
            for i in range(len(list_cmd)):
                while True:
                    if ssh_channel.recv_ready():
                        data = ssh_channel.recv(1024)
                        print(data.decode('utf-8'), end='')
                        print(list_cmd[i].lower())
                        if data and (data.endswith('>'.encode('utf-8')) or data.endswith(']'.encode('utf-8'))):
                            ssh_channel.send(list_cmd[i].encode('utf-8') + b'\n')
                            time.sleep(1)
                            while True:
                                print(data.find(b'  ---- More ----'))
                                if data.find(b'  ---- More ----') != -1:
                                    ssh_channel.send(b'\n')
                                    time.sleep(1)
                                elif data.find(b'>') != -1:
                                    time.sleep(1)
                                    break
                                elif data.find(b']') != -1:
                                    time.sleep(1)
                                    break
                            data = ssh_channel.recv(1024)
                            print(data.decode('utf-8'), end='')
                            print(list_cmd[i].lower())
                            print(data.find(b']'))
                            if data.find(b'>') != -1:
                                time.sleep(1)
                                ssh_channel.send(b'\n')
                                break
                            if data.find(b']') != -1:
                                time.sleep(1)
                                ssh_channel.send(b'\n')
                                break
                            if data.find(b'  ---- More ----') != -1:
                                while True:
                                    ssh_channel.send(b' ')
                                    data = ssh_channel.recv(1024)
                                    time.sleep(1)
                                    print(data.decode('utf-8'), end='')
                                    if data.find(b']') != -1:
                                        time.sleep(1)
                                        ssh_channel.send(b'\n')
                                        break
                                break
                    if list_cmd[i].lower() == 'exit':
                        break
                print("""cfg {v00} {v01} start""".format(v00=self.ssh_ip, v01=list_cmd[i]))
                # ssh_channel.send("""{v01}""".format(v01=list_cmd[i]).encode('utf-8'))
                print("""cfg {v00} {v01} done""".format(v00=self.ssh_ip, v01=list_cmd[i]))
            ssh_channel.close()
            cus_ssh_client.close()
            print("""%s/%s: OK!""" % (self.cur_num, self.total_num))
        except Exception as e:
            print("""%s/%s: ERROR: %s""" % (self.cur_num, self.total_num, e))


class CusCfgSshComm(object):
    def __init__(self, ):
        self.cus_excel_op = CusExcelOp()
        # self.cus_excel_op.create_new_workbook()
        self.local_methord = CusLocalMethod()

    def def_cfg_ssh_comm(self):

        self.cus_excel_op.load_excel('/etc/zabbix/scripts/sshcomm.xlsx', 1)

        column_1_list = self.cus_excel_op.get_column_values(1)
        del column_1_list[0]
        column_2_list = []
        column_3_list = []
        column_4_list = []
        column_5_list = []

        for i in range(len(column_1_list)):
            column_2_list.append(self.cus_excel_op.get_cell_value(i + 2, 2))  # 端口
            column_3_list.append(self.cus_excel_op.get_cell_value(i + 2, 3))  # 用户名
            column_4_list.append(self.cus_excel_op.get_cell_value(i + 2, 4))  # 密码
            column_5_list.append(self.cus_excel_op.get_cell_value(i + 2, 5))  # 执行命令
        for n_1 in range(len(column_1_list)):
            try:
                m = MyThreadCfgSshComm(n_1 + 1, len(column_1_list), column_1_list[n_1], column_2_list[n_1],
                                       column_3_list[n_1], column_4_list[n_1], column_5_list[n_1])
                m.start()
            except Exception as e:
                print(u"配置表第%s行数据异常%s" % (n_1 + 1, e))
                sys.exit(1)


class CusWebClinet(object):
    def __init__(self, ):
        self.zabbix_sender = CusZabbixSender()
        self.cus_excel_op = CusExcelOp()
        self.cus_excel_op.create_new_workbook()
        self.local_methord = CusLocalMethod()

        self.header = {"Content-Type": "application/json"}
        self.session = requests.Session()

    def def_discovering_resources_webcode_schoolid(self, host, list_resources):
        try:
            for resource in list_resources:
                if ['webcode_schoolid'].count(resource) == 1:
                    logger.info("Starting discovering resource - {0}".format(resource))
                    one_object_list = {}
                    discovered_resource = []
                    one_object_list["{#INDEX}"] = 1
                    discovered_resource.append(one_object_list)
                    logger.info("Succes get resource - {0}".format(resource))
                    converted_resource = self.zabbix_sender.def_convert_to_zabbix_json(discovered_resource)
                    timestampnow = int(time.time())
                    TIMESTAMPNOW = timestampnow
                    xer = []
                    xer.append("%s %s %s %s" % (host, resource, timestampnow, converted_resource))
                    self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, xer, host)
                else:
                    logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], u'没有匹配的自动发现规则'))
            # self.cus_excel_op.def_save_create_xlsx(XLSX_FILENAME)
            print(0)
        except Exception as oops:
            logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], oops))
            sys.exit("{0}".format(inspect.currentframe().f_lineno))

    def def_discovering_resources_web_service(self, host, list_resources, url_http, serviceid_str, marketid_int, stockcode_list):
        try:
            for resource in list_resources:
                if ['serviceid'].count(resource) == 1:
                    try:
                        logger.info("Starting discovering resource - {0}".format(resource))
                        self.session.mount(url_http, requests.adapters.HTTPAdapter(max_retries=3))

                        json_data_1 = {
                            "serviceid": serviceid_str,
                            "body": {
                                "marketid": marketid_int,
                                "stockcode": stockcode_list,
                            }
                        }
                        request = self.session.post(url=url_http, headers=self.header, json=json_data_1)
                        response = request.json()
                        if response.get('result', '') != '':
                            self.authID = response['result']
                        elif response.get('error', '') != '':
                            sys.exit("{0}".format(inspect.currentframe().f_lineno))
                        time.sleep(0.1)

                        title_name = ['index', 'name', 'now', 'volume', 'amount']
                        self.cus_excel_op.create_sheet(resource)
                        [self.cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]

                        for i_01 in range(len(response['data'])):
                            self.cus_excel_op.set_cell_value(i_01 + 2, 1, i_01 + 1)
                            for i_02 in range(len(title_name)):
                                if i_02 == 1:
                                    self.cus_excel_op.set_cell_value(i_01 + 2, 2, response['data'][i_01]['code'] + '_' + response['data'][i_01]['name'])
                        discovered_resource = []
                        col_01_list = self.cus_excel_op.get_column_values(2)
                        del col_01_list[0]
                        for col_01 in col_01_list:
                            one_object_list = {}
                            one_object_list["{#NAME}"] = col_01
                            discovered_resource.append(one_object_list)
                        logger.info("Succes get resource - {0}".format(resource))
                        converted_resource = self.zabbix_sender.def_convert_to_zabbix_json(discovered_resource)
                        xer = []
                        timestampnow = int(time.time())
                        TIMESTAMPNOW = timestampnow
                        xer.append("%s %s %s %s" % (host, resource, timestampnow, converted_resource))
                        self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, xer, host)
                    except Exception as ee:
                        logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], ee))
                        sys.exit("{0}".format(inspect.currentframe().f_lineno))
                else:
                    logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], u'没有匹配的自动发现规则'))
            # self.cus_excel_op.def_save_create_xlsx(XLSX_FILENAME)
            print(0)
        except Exception as oops:
            logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], oops))
            sys.exit("{0}".format(inspect.currentframe().f_lineno))

    def def_get_status_resources_webcode_schoolid(self, host, list_resources, url_http, url_userid, url_pwd, url_schoolid):
        try:
            for resource in list_resources:
                if ['webcode_schoolid'].count(resource) == 1:
                    logger.info("Starting discovering resource - {0}".format(resource))
                    self.session.mount(url_http, requests.adapters.HTTPAdapter(max_retries=3))
                    try:
                        json_data_1 = {
                            'schoolid': url_schoolid,
                            'userid': url_userid,
                            'password': url_pwd,
                        }
                        json_data_2 = json.dumps({
                            "jsonrpc": "2.0",
                            "method": "user.login",
                            "params": {
                                "user": url_userid,  # web页面登录用户名
                                "password": url_pwd  # web页面登录密码
                            },
                            "id": 0
                        })
                        request = self.session.post(url=url_http, headers=self.header, json=json_data_1)
                        # request = self.session.post(url=url_http, headers=self.header, data=json_data_2)
                        response = request.json()
                        if response.get('result', '') != '':
                            self.authID = response['result']
                        elif response.get('error', '') != '':
                            sys.exit("{0}".format(inspect.currentframe().f_lineno))
                        time.sleep(0.1)
                        title_name = ['index', 'status']
                        self.cus_excel_op.create_sheet(resource)
                        [self.cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
                        self.cus_excel_op.set_cell_value(2, 1, 1)
                        self.cus_excel_op.set_cell_value(2, 2, response['status'])

                        col_01_list = self.cus_excel_op.get_column_values(1)
                        del col_01_list[0]
                        col_02_list = self.cus_excel_op.get_column_values(2)
                        del col_02_list[0]
                        timestampnow = int(time.time())
                        TIMESTAMPNOW = timestampnow
                        state_resources = []
                        for len_col_01 in range(len(col_01_list)):
                            key_name = "{0}[{1}]".format(resource, col_01_list[len_col_01])
                            state_resources.append("%s %s %s %s" % ("\"" + host + "\"", key_name, timestampnow, col_02_list[len_col_01]))
                        self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, state_resources, host)
                    except Exception as ee:
                        state_resources = []
                        timestampnow = int(time.time())
                        TIMESTAMPNOW = timestampnow
                        key_name = "{0}[{1}]".format(resource, 1)
                        state_resources.append("%s %s %s %s" % ("\"" + host + "\"", key_name, timestampnow, 1))
                        self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, state_resources, host)
                        logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], ee))
                        sys.exit("{0}".format(inspect.currentframe().f_lineno))
                else:
                    logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], u'没有匹配的自动发现规则'))
            # self.cus_excel_op.def_save_create_xlsx(XLSX_FILENAME)
            print(0)
        except Exception as pizdec:
            logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], pizdec))
            sys.exit("{0}".format(inspect.currentframe().f_lineno))

    def def_get_status_resources_web_service(self, host, list_resources, url_http, serviceid_str, marketid_int, stockcode_list):
        try:
            for resource in list_resources:
                if ['serviceid'].count(resource) == 1:
                    try:
                        logger.info("Starting discovering resource - {0}".format(resource))
                        self.session.mount(url_http, requests.adapters.HTTPAdapter(max_retries=3))

                        json_data_1 = {
                            "serviceid": serviceid_str,
                            "body": {
                                "marketid": marketid_int,
                                "stockcode": stockcode_list,
                            }
                        }
                        request = self.session.post(url=url_http, headers=self.header, json=json_data_1)
                        response = request.json()
                        if response.get('result', '') != '':
                            self.authID = response['result']
                        elif response.get('error', '') != '':
                            sys.exit("{0}".format(inspect.currentframe().f_lineno))
                        time.sleep(0.1)

                        title_name = ['index', 'name', 'now', 'volume', 'amount']
                        self.cus_excel_op.create_sheet(resource)
                        [self.cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]

                        for i_01 in range(len(response['data'])):
                            self.cus_excel_op.set_cell_value(i_01 + 2, 1, i_01 + 1)
                            for i_02 in range(len(title_name)):
                                if i_02 == 1:
                                    self.cus_excel_op.set_cell_value(i_01 + 2, 2, response['data'][i_01]['code'] + '_' + response['data'][i_01]['name'])
                                elif i_02 == 2:
                                    self.cus_excel_op.set_cell_value(i_01 + 2, 3, response['data'][i_01]['now'])
                                elif i_02 == 3:
                                    self.cus_excel_op.set_cell_value(i_01 + 2, 4, response['data'][i_01]['volume'])
                                elif i_02 == 4:
                                    self.cus_excel_op.set_cell_value(i_01 + 2, 5, response['data'][i_01]['amount'])
                        col_02_list = self.cus_excel_op.get_column_values(2)
                        del col_02_list[0]
                        col_03_list = self.cus_excel_op.get_column_values(3)
                        del col_03_list[0]
                        col_04_list = self.cus_excel_op.get_column_values(4)
                        del col_04_list[0]
                        col_05_list = self.cus_excel_op.get_column_values(5)
                        del col_05_list[0]
                        timestampnow = int(time.time())
                        TIMESTAMPNOW = timestampnow
                        state_resources = []
                        for len_col_01 in range(len(col_02_list)):
                            key_name = "{0}[{1}]".format(resource, col_02_list[len_col_01])
                            state_resources.append("%s %s %s %s" % ("\"" + host + "\"", key_name, timestampnow, col_02_list[len_col_01]))
                        self.zabbix_sender.def_send_data_to_zabbix(TIMESTAMPNOW, state_resources, host)
                    except Exception as ee:
                        logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], ee))
                        sys.exit("{0}".format(inspect.currentframe().f_lineno))
                else:
                    logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], u'没有匹配的自动发现规则'))
            # self.cus_excel_op.def_save_create_xlsx(XLSX_FILENAME)
            print(0)
        except Exception as pizdec:
            logger.error(u"错误: {0} {1}".format(inspect.stack()[0][2], pizdec))
            sys.exit("{0}".format(inspect.currentframe().f_lineno))


class CusZabbixSender(object):
    def __init__(self, ):
        self.send_code = None
        self.output = None

    def def_convert_to_zabbix_json(self, data):
        self.output = json.dumps({"data": data}, indent=None, separators=(',', ': '))
        return self.output

    def def_send_data_to_zabbix(self, id_name, zabbix_data, host):
        time_of_create_file = id_name
        temp_file = "/tmp/{0}_{1}.tmp".format(host, time_of_create_file)
        with open(temp_file, "w") as f:
            f.write("")
            f.write(u"\n".join(zabbix_data))
        sender_command = f"/usr/bin/zabbix_sender -vv -z {SERVER_IP} -p {SERVER_PORT} -s {host} -T -i {temp_file}"
        # self.send_code = subprocess.call([sender_command, "-vv", "-z", SERVER_IP, "-p", SERVER_PORT, "-s", host, "-T", "-i", temp_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        self.send_code = subprocess.run(sender_command,
                                        shell=True,
                                        timeout=30,
                                        env=os.environ)
        print("STDOUT:", self.send_code.stdout)
        print("STDERR:", self.send_code.stderr)
        print("Return Code:", self.send_code.stdout)
        time.sleep(0.1)
        if os.path.isfile(temp_file):
            os.remove(temp_file)
            # pass
        if os.path.isfile(LOG_FILENAME):
            os.remove(LOG_FILENAME)
            pass


class CusLocalMethod(object):
    def __init__(self, ):
        self.value = None
        self.numericValue = None
        self.textreplace = None

    @staticmethod
    def def_batch_replace(text: str, replacements: dict):
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def def_hum_convert(self, value):
        # units = ["B", "KB", "MB", "GB", "TB", "PB"]
        units = ["KB", "MB", "GB", "TB", "PB"]
        size = 1024.0
        for i in range(len(units)):
            if (float(value) / size) < 1:
                self.value = "%.2f%s" % (value, units[i])
                return value
            value = float(value) / size

    def def_convert_text_to_numeric(self, value):
        if value == 'online':
            self.numericValue = 0
        elif value == 'offline':
            self.numericValue = 1
        elif value == 'degraded':
            self.numericValue = 2
        elif value == 'active':
            self.numericValue = 3
        elif value == 'inactive_configured':
            self.numericValue = 4
        elif value == 'inactive_unconfigured':
            self.numericValue = 5
        elif value == 'offline_unconfigured':
            self.numericValue = 6
        elif value == 'excluded':
            self.numericValue = 7
        elif value == 'on':
            self.numericValue = 8
        elif value == 'off':
            self.numericValue = 9
        elif value == 'slow_flashing':
            self.numericValue = 10
        elif value == 'degraded_paths':
            self.numericValue = 11
        elif value == 'degraded_ports':
            self.numericValue = 12
        elif value == 'up':
            self.numericValue = 0
        elif value == 'down':
            self.numericValue = 1
        elif value == 'LISTEN':
            self.numericValue = 0
        elif value == 'open':
            self.numericValue = 0
        elif value == 'closed':
            self.numericValue = 1
        else:
            self.numericValue = 100
        return self.numericValue

    def def_convert_text_to_text(self, value):
        if value == "::1" or value == "::" or value == "0.0.0.0":
            self.textreplace = "127.0.0.1"
        else:
            self.textreplace = value
        return self.textreplace

    def def_ping(self, ip):
        """
        获取节点的延迟的作用
        :param node:
        :return:
        """
        ip_address = ip
        response = ping(ip_address)
        if response is not None:
            delay = int(response * 1000)
            return delay


def main():
    cus_telnet_client = CusTelnetClient()
    cus_ssh_client = CusSSHClient()
    cus_web_client = CusWebClinet()
    cus_linux_client = CusLinuxClient()
    cus_direct_client = CusDirectClient()
    cus_sftp_client = CusSftpClient()
    cus_ssh_comm = CusCfgSshComm()
    ###########################################################
    parser = argparse.ArgumentParser()
    parser.add_argument('--type')
    parser.add_argument('--ip', help="Where to connect")
    parser.add_argument('--port')
    parser.add_argument('--user')
    parser.add_argument('--pwd')
    parser.add_argument('--host')
    parser.add_argument('--url_schoolid')
    parser.add_argument('--url_userid')
    parser.add_argument('--url_pwd')
    parser.add_argument('--url_http')
    parser.add_argument('--serviceid_str')
    parser.add_argument('--marketid_int')
    parser.add_argument('--stockcode_list')
    parser.add_argument('--value')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--discovery', action='store_true')
    group.add_argument('--status', action='store_true')
    group.add_argument('--sshcomm', action='store_true')
    arguments = parser.parse_args()

    list_resources = []
    if ['telnet'].count(arguments.type) == 1:
        list_resources = ['disname', 'discpu', 'disinterface']
        list_resources = ['disname', 'discpu_20230104', 'dismem_20230104']
    elif ['dispower'].count(arguments.type) == 1:
        list_resources = ['dispower']
    elif ['dirMTimeFileNum'].count(arguments.type) == 1:
        list_resources = ['dirMTimeFileNum']
    elif ['dirFileNum'].count(arguments.type) == 1:
        list_resources = ['dirFileNum']
    elif ['dirMTime'].count(arguments.type) == 1:
        list_resources = ['dirMTime']
    elif ['linuxMount'].count(arguments.type) == 1:
        list_resources = ['linuxMount']
    elif ['linuxDf'].count(arguments.type) == 1:
        list_resources = ['linuxDf']
    elif ['linuxPs'].count(arguments.type) == 1:
        list_resources = ['linuxPs']
    elif ['sftp'].count(arguments.type) == 1:
        list_resources = ['queueDepth']
    elif ['linux'].count(arguments.type) == 1:
        # linux_checkping /etc/zabbix/venv_centos8/bin/python3 /etc/zabbix/scripts/zabbix_sender.py --type='linux' --host='172.16.51.250' --status
        # list_resources = ['linux_df', 'linux_netstat', 'linux_checkping']
        list_resources = ['linux_checkping']
    elif ['web'].count(arguments.type) == 1:
        list_resources = ['webcode_schoolid']
    elif ['web_service'].count(arguments.type) == 1:
        list_resources = ['serviceid']
    elif ['direct'].count(arguments.type) == 1:
        list_resources = ['ssh_login_log']

    if arguments.discovery:
        logger.info("********************************* Starting Discovering *********************************")
        if ['telnet'].count(arguments.type) == 1:
            cus_telnet_client.def_discovering_resources(arguments.user, list_resources)
        if ['dispower'].count(arguments.type) == 1:
            cus_telnet_client.def_discovering_resources(arguments.host, list_resources)
        elif ['dirMTimeFileNum'].count(arguments.type) == 1:
            cus_ssh_client.def_discovering_resources(arguments.host, list_resources)
        elif ['dirFileNum'].count(arguments.type) == 1:
            cus_ssh_client.def_discovering_resources(arguments.host, list_resources)
        elif ['dirMTime'].count(arguments.type) == 1:
            cus_ssh_client.def_discovering_resources(arguments.host, list_resources)
        elif ['linuxMount'].count(arguments.type) == 1:
            cus_ssh_client.def_discovering_resources(arguments.host, list_resources)
        elif ['linuxDf'].count(arguments.type) == 1:
            cus_ssh_client.def_discovering_resources(arguments.host, list_resources)
        elif ['linuxPs'].count(arguments.type) == 1:
            cus_ssh_client.def_discovering_resources(arguments.host, list_resources)
        elif ['sftp'].count(arguments.type) == 1:
            cus_sftp_client.def_discovering_resources(arguments.host, list_resources)
        elif ['linux'].count(arguments.type) == 1:
            cus_linux_client.def_discovering_resources(arguments.host, list_resources)
        elif ['web'].count(arguments.type) == 1:
            cus_web_client.def_discovering_resources_webcode_schoolid(arguments.host, list_resources)
        elif ['web_service'].count(arguments.type) == 1:
            cus_web_client.def_discovering_resources_web_service(arguments.host, list_resources, arguments.url_http, arguments.serviceid_str, arguments.marketid_int, arguments.stockcode_list)

    elif arguments.status:
        logger.info("********************************* Starting Get Status *********************************")
        if ['telnet'].count(arguments.type) == 1:
            cus_telnet_client.def_get_status_resources(arguments.user, list_resources)
        elif ['dispower'].count(arguments.type) == 1:
            cus_telnet_client.def_get_status_resources(arguments.host, list_resources)
        elif ['dirMTimeFileNum'].count(arguments.type) == 1:
            cus_ssh_client.def_get_status_resources(arguments.host, list_resources)
        elif ['dirFileNum'].count(arguments.type) == 1:
            cus_ssh_client.def_get_status_resources(arguments.host, list_resources)
        elif ['dirMTime'].count(arguments.type) == 1:
            cus_ssh_client.def_get_status_resources(arguments.host, list_resources)
        elif ['linuxMount'].count(arguments.type) == 1:
            cus_ssh_client.def_get_status_resources(arguments.host, list_resources)
        elif ['linuxDf'].count(arguments.type) == 1:
            cus_ssh_client.def_get_status_resources(arguments.host, list_resources)
        elif ['linuxPs'].count(arguments.type) == 1:
            cus_ssh_client.def_get_status_resources(arguments.host, list_resources)
        elif ['sftp'].count(arguments.type) == 1:
            cus_sftp_client.def_get_status_resources(arguments.host, list_resources)
        elif ['linux'].count(arguments.type) == 1:
            cus_linux_client.def_get_status_resources(arguments.host, list_resources)
        elif ['direct'].count(arguments.type) == 1:
            cus_direct_client.def_get_status_resources(arguments.host, list_resources, arguments.value)
        elif ['web'].count(arguments.type) == 1:
            cus_web_client.def_get_status_resources_webcode_schoolid(arguments.host, list_resources, arguments.url_http, arguments.url_userid, arguments.url_pwd, arguments.url_schoolid)
        elif ['web_service'].count(arguments.type) == 1:
            cus_web_client.def_get_status_resources_web_service(arguments.host, list_resources, arguments.url_http, arguments.serviceid_str, arguments.marketid_int, arguments.stockcode_list)

    elif arguments.sshcomm:
        cus_ssh_comm.def_cfg_ssh_comm()


# result_status = get_status_resources(arguments.user, arguments.password, arguments.ip, arguments.port, arguments.storage_name, list_resources)
# print(result_status)


if __name__ == "__main__":
    #     a="""System Total Memory(bytes): 34590336
    # Total Used Memory(bytes): 14141896
    # Used Rate: 40%
    #
    #     """
    #     b = re.compile(r'Rate:\s(\d*%)')
    #     r = re.search(b, a)
    #     print(r.group(1))
    #     exit(1)
    main()
