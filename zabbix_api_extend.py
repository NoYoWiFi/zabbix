#!/usr/bin/python3
# coding:utf-8

import argparse
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import hashlib
import hmac
import logging
import inspect
import json
import os
import openpyxl
import re
import sys
import time
from time import mktime
import traceback
import types
import requests
from requests.adapters import HTTPAdapter
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import threading
from zabbix_api import CusZabbixApi
from zabbix_api import CusExcelOp
from zabbix_api import CusMyThreadSendDir
from zabbix_api import CusMyThreadCfgZabbixAgent
from zabbix_api import CusMyThreadCfgSj
from zabbix_api import GV_CPU_COUNT
from zabbix_api import CusLocalMethod
from zabbix_api import MyThreadCfgSshComm

LOG_FILENAME = "./stateTmpFile.log"
# sys.argv[5] contain this string "--storage_name=<storage_name_in_zabbix>". List slicing delete this part "--storage_name="
STORAGE_NAME = ''
if len(sys.argv) > 1:
    STORAGE_NAME = sys.argv[1][9:]
    # Set handler
    formatter = logging.Formatter('{0} - %(asctime)s - %(name)s - %(levelname)s - %(message)s'.format(STORAGE_NAME))
    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)
    # Set formatter for handler
    # Add handler to log-object

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='zabbix  api ', usage='%(prog)s [options]')
    # ![14]
    parser.add_argument('-get_item_history', nargs='?', metavar='无参数', dest='get_item_history', default='get_item_history',
                        help=u"按主机名批量计算历史最小值、平均值、最大值")
    # ![]
    parser.add_argument('-get_all_history', nargs='?', metavar='无参数', dest='get_all_history', default='get_all_history',
                        help=u"按主机名批量导出历史数据")
    # ![]
    parser.add_argument('-get_hostgroup_host', nargs='?', metavar='无参数', dest='get_hostgroup_host', default='get_hostgroup_host',
                        help=u"为主机组批量获取主机名")
    # ![16]
    parser.add_argument('-update_host_name', nargs='?', metavar='无参数', dest='update_host_name', default='update_host_name',
                        help=u"批量更新主机名")
    # ![]
    parser.add_argument('-get_host_key_item', nargs='?', metavar='无参数', dest='get_host_key_item', default='get_host_key_item',
                        help=u"为所有主机获取数据")
    parser.add_argument('-get_host_key_systemname', nargs='?', metavar='无参数', dest='get_host_key_systemname', default='get_host_key_systemname',
                        help=u"为所有主机获取系统名称")
    # ![]
    parser.add_argument('-get_hostgroup_item', nargs='?', metavar='无参数', dest='get_hostgroup_item', default='get_hostgroup_item',
                        help=u"为主机组批量获取主机监控项")
    # ![]
    parser.add_argument('-stop_all_priority_trigger', nargs='?', metavar='无参数', dest='stop_all_priority_trigger', default='stop_all_priority_trigger',
                        help=u"批量停止已启用触发器")
    parser.add_argument('-stop_all_priority_trigger_by_description', nargs='?', metavar='无参数', dest='stop_all_priority_trigger_by_description', default='stop_all_priority_trigger_by_description',
                        help=u"批量停止已启用触发器模糊搜索触发器名称")
    parser.add_argument('-start_all_priority_trigger', nargs='?', metavar='无参数', dest='start_all_priority_trigger', default='start_all_priority_trigger',
                        help=u"批量启用已停止触发器")
    # ![]
    parser.add_argument('-stop_all_unsupport_item', nargs='?', metavar='无参数', dest='stop_all_unsupport_item', default='stop_all_unsupport_item',
                        help=u"批量停止不支持的监控项")
    parser.add_argument('-start_all_unsupport_item', nargs='?', metavar='无参数', dest='start_all_unsupport_item', default='start_all_unsupport_item',
                        help=u"批量启用不支持的监控项")
    parser.add_argument('-massadd_host_template_base_20221003', nargs='?', metavar='无参数', dest='massadd_host_template_base_20221003', default='massadd_host_template_base_20221003',
                        help=u"主机组下所有主机附加模板")
    parser.add_argument('-massupdate_host_template_base_20221003', nargs='?', metavar='无参数', dest='massupdate_host_template_base_20221003', default='massupdate_host_template_base_20221003',
                        help=u"主机组下所有主机更新模板")
    parser.add_argument('-def_massremove_host_templateids_clear_base_20221003', nargs='?', metavar='无参数', dest='def_massremove_host_templateids_clear_base_20221003', default='def_massremove_host_templateids_clear_base_20221003',
                        help=u"主机组下所有主机脱离模板清理监控项")
    parser.add_argument('-get_all_alert', nargs='?', metavar='无参数', dest='get_all_alert', default='get_all_alert',
                        help=u"获取所有告警信息")
    parser.add_argument('-get_all_problem', nargs='?', metavar='无参数', dest='get_all_problem', default='get_all_problem',
                        help=u"获取所有问题信息")
    parser.add_argument('-get_all_event', nargs='?', metavar='无参数', dest='get_all_event', default='get_all_event',
                        help=u"获取所有事件信息")
    parser.add_argument('-createfile', nargs='?', metavar='无参数', dest='createfile', default='createfile',
                        help=u"生成配置文件")
    parser.add_argument('-senddir', nargs='?', metavar='无参数', dest='senddir', default='senddir',
                        help=u"下发文件")
    parser.add_argument('-sendcomm', nargs='?', metavar='无参数', dest='sendcomm', default='sendcomm',
                        help=u"下发SSH命令")
    parser.add_argument('-sendcfg', nargs='?', metavar='无参数', dest='sendcfg', default='sendcfg',
                        help=u"配置代理")
    parser.add_argument('-sendsj', nargs='?', metavar='无参数', dest='sendsj', default='sendsj',
                        help=u"配置审计")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 如有问题请联系作者QQ1284524409',
                        help=u"如有问题请联系作者QQ1284524409")
    parser.add_argument('--output')
    args = parser.parse_args()
    cus_excel_op = CusExcelOp()
    if len(sys.argv) == 1:
        print(parser.print_help())
        # 在主执行部分添加日志文件统计
    elif args.sendcomm != 'sendcomm':
        """
        处理SSH命令执行的主函数
        """


        def read_cfgswap_and_create_excel(cfgswap_file='cfg.swap', excel_file='sshcomm.xlsx'):
            """
            从cfg.swap文件中读取[diagramItemMemSwitch]下的JSON数据，
            提取ip、用户、密码、端口信息，并创建sshcomm.xlsx文件

            Args:
                cfgswap_file: cfg.swap文件路径
                excel_file: 输出的Excel文件路径
            """
            try:
                print(f"正在读取配置文件: {cfgswap_file}")

                # 读取文件内容
                with open(cfgswap_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 查找[diagramItemMemSwitch]部分
                pattern = r'\[diagramItemMemSwitch\](.*?)(?=\n\[|\Z)'
                match = re.search(pattern, content, re.DOTALL)

                if not match:
                    print("错误: 在配置文件中找不到 [diagramItemMemSwitch] 部分")
                    return False

                switch_section = match.group(1).strip()

                # 提取所有switch行
                switch_lines = []
                for line in switch_section.split('\n'):
                    line = line.strip()
                    if line and '=' in line:
                        switch_lines.append(line)

                print(f"找到 {len(switch_lines)} 个交换机配置")

                # 解析JSON数据
                devices = []
                for line in switch_lines:
                    try:
                        # 分割键值对
                        if '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip().strip('"')

                            # 处理JSON字符串中的转义字符
                            # 首先处理双引号的转义
                            value = value.replace('\\"', '"')
                            # 然后移除多余的反斜杠
                            value = value.replace('\\\\', '\\')

                            # 解析JSON
                            device_data = json.loads(value)

                            # 提取所需字段
                            ip = device_data.get('ipAddress', '')
                            user = device_data.get('userName', '')
                            password = device_data.get('password', '')
                            port = device_data.get('port', '22')

                            # 清理密码字段（移除可能的引号）
                            if password.startswith('"') and password.endswith('"'):
                                password = password[1:-1]

                            devices.append({
                                'ip': ip,
                                'user': user,
                                'password': password,
                                'port': port
                            })

                    except json.JSONDecodeError as e:
                        print(f"解析JSON时出错 (行: {line[:50]}...): {e}")
                        continue
                    except Exception as e:
                        print(f"处理行时出错: {e}")
                        continue

                if not devices:
                    print("错误: 没有找到有效的设备配置")
                    return False

                print(f"成功解析 {len(devices)} 个设备配置")

                # 创建Excel文件
                print(f"正在创建Excel文件: {excel_file}")

                # 创建新的工作簿
                cus_excel_op.create_new_workbook()

                # 创建sheet
                cus_excel_op.create_sheet("设备列表")

                # 设置表头（新增编码列）
                headers = ['IP地址', '用户名', '密码', '端口', '预设命令', '编码']
                for col_idx, header in enumerate(headers, start=1):
                    cus_excel_op.set_cell_value(1, col_idx, header)

                # 预设命令
                preset_commands = "sys\ndis cu\nquit\nquit"
                # 默认编码
                default_encoding = 'gbk'

                # 填充数据
                for row_idx, device in enumerate(devices, start=2):
                    cus_excel_op.set_cell_value(row_idx, 1, device['ip'])
                    cus_excel_op.set_cell_value(row_idx, 2, device['user'])
                    cus_excel_op.set_cell_value(row_idx, 3, device['password'])
                    cus_excel_op.set_cell_value(row_idx, 4, device['port'])
                    cus_excel_op.set_cell_value(row_idx, 5, preset_commands)
                    cus_excel_op.set_cell_value(row_idx, 6, default_encoding)

                # 保存Excel文件
                cus_excel_op.save_workbook(excel_file)

                print(f"Excel文件已成功创建: {excel_file}")
                print(f"共添加了 {len(devices)} 个设备")
                print(f"预设命令已添加到第5列")
                print(f"默认编码 '{default_encoding}' 已添加到第6列")

                # 显示前几个设备的摘要信息
                print("\n设备配置摘要:")
                print(f"{'序号':<5} {'IP地址':<15} {'用户名':<10} {'端口':<6} {'编码':<8}")
                print("-" * 45)
                for i, device in enumerate(devices[:5], 1):
                    print(f"{i:<5} {device['ip']:<15} {device['user']:<10} {device['port']:<6} {default_encoding:<8}")
                if len(devices) > 5:
                    print(f"... 还有 {len(devices) - 5} 个设备")

                return True

            except FileNotFoundError:
                print(f"错误: 找不到配置文件 {cfgswap_file}")
                return False
            except Exception as e:
                print(f"处理配置文件时出错: {str(e)}")
                traceback.print_exc()
                return False


        try:
            # 首先检查是否存在sshcomm.xlsx，如果不存在则从cfg.swap创建
            if not os.path.exists('sshcomm.xlsx'):
                print("未找到sshcomm.xlsx文件，尝试从cfg.swap创建...")
                success = read_cfgswap_and_create_excel()
                if not success:
                    print("无法创建sshcomm.xlsx文件，请检查cfg.swap文件")
                    exit(1)

            # 创建日志目录
            log_dir = 'ssh_execution_logs'
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            # 1. 加载Excel数据
            cus_excel_op.load_excel('sshcomm.xlsx', 1)

            # 获取各列数据
            column_1_list = cus_excel_op.get_column_values(1)
            if len(column_1_list) <= 1:
                print("Excel文件中没有数据或只有表头")
                exit(1)

            del column_1_list[0]

            # 准备任务数据（新增编码字段）
            tasks = []
            for i in range(len(column_1_list)):
                encoding = cus_excel_op.get_cell_value(i + 2, 6)
                if not encoding:
                    encoding = 'gbk'  # 默认编码

                tasks.append({
                    'ip': column_1_list[i],
                    'username': cus_excel_op.get_cell_value(i + 2, 2),
                    'password': cus_excel_op.get_cell_value(i + 2, 3),
                    'port': cus_excel_op.get_cell_value(i + 2, 4) or 22,
                    'command': cus_excel_op.get_cell_value(i + 2, 5),
                    'encoding': encoding
                })

            total_tasks = len(tasks)

            print(f"找到 {total_tasks} 个任务:")
            for i, task in enumerate(tasks):
                print(
                    f"  任务{i + 1}: {task['ip']}:{task['port']} 用户:{task['username']} 编码:{task['encoding']} 命令:{task['command'][:50]}...")

            # 创建结果Excel
            cus_excel_op.create_new_workbook()
            cus_excel_op.create_sheet("上传结果")
            title_name = ['IP', '是否成功', '过程', '错误详情']
            [cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]

            # 初始化IP地址
            for idx, task in enumerate(tasks, start=2):
                cus_excel_op.set_cell_value(idx, 1, task['ip'])

            # 线程安全锁
            excel_lock = threading.Lock()

            print(f"\n开始执行SSH命令，共 {total_tasks} 个任务...")
            print(f"日志文件将保存到: {log_dir} 目录")
            print(f"每个IP将生成一个独立的.log文件\n")

            # 使用线程池
            max_workers = min(GV_CPU_COUNT, total_tasks, 5)  # 最多5个线程，减少并发
            print(f"使用 {max_workers} 个线程")

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # 提交任务
                futures = []
                for idx, task in enumerate(tasks):
                    cur_num = idx + 1

                    print(f"\n准备执行任务 {cur_num}:")
                    print(f"  IP: {task['ip']}:{task['port']}")
                    print(f"  用户: {task['username']}")
                    print(f"  编码: {task['encoding']}")
                    print(f"  命令: {task['command'][:100]}...")

                    future = executor.submit(
                        MyThreadCfgSshComm(
                            cur_num=cur_num,
                            total_num=total_tasks,
                            ssh_ip=task['ip'],
                            port=task['port'],
                            usr=task['username'],
                            pwd=task['password'],
                            cmd=task['command'],
                            encoding=task['encoding']  # 新增编码参数
                        )
                    )
                    futures.append((future, cur_num, task))
                    print(f"  任务 {cur_num} 已提交")

                print(f"\n所有任务已提交，开始执行...")

                # 处理完成的任务
                completed = 0
                for future, cur_num, task in futures:
                    try:
                        # 设置更长的超时时间
                        result = future.result(timeout=180)  # 每个任务最多等待3分钟
                        completed += 1

                        print(f"\n任务 {cur_num} 完成:")
                        print(f"  IP: {task['ip']}")
                        print(f"  编码: {task['encoding']}")
                        print(f"  结果: {'成功' if result['success'] else '失败'}")

                        if not result['success']:
                            print(f"  错误: {result.get('error', '未知错误')}")
                            print(f"  摘要: {result.get('summary', '')}")

                        # 保存结果到Excel
                        with excel_lock:
                            row = cur_num + 1

                            if result['success']:
                                cus_excel_op.set_cell_value(row, 2, "是")
                                output = result.get('output', '')
                                if output:
                                    if len(output) > 30000:
                                        output = output[:28000] + "\n...（输出过长已截断）"
                                    cus_excel_op.set_cell_value(row, 3, output)
                                else:
                                    cus_excel_op.set_cell_value(row, 3, "无输出")
                                cus_excel_op.set_cell_value(row, 4, "")
                            else:
                                cus_excel_op.set_cell_value(row, 2, "否")
                                cus_excel_op.set_cell_value(row, 3, "执行失败")
                                error_msg = result.get('error', '未知错误')
                                summary = result.get('summary', '')
                                error_detail = f"错误: {error_msg}\n摘要: {summary}"
                                if len(error_detail) > 30000:
                                    error_detail = error_detail[:28000] + "..."
                                cus_excel_op.set_cell_value(row, 4, error_detail)

                        # 定期保存
                        if completed % 2 == 0:
                            try:
                                cus_excel_op.save_workbook('commResult_tmp.xlsx')
                                print(f"  已保存临时文件")
                            except Exception as e:
                                print(f"  保存临时文件失败: {str(e)}")

                    except TimeoutError:
                        print(f"\n任务 {cur_num} ({task['ip']}) 执行超时")
                        with excel_lock:
                            row = cur_num + 1
                            cus_excel_op.set_cell_value(row, 2, "否")
                            cus_excel_op.set_cell_value(row, 3, "执行超时(3分钟)")
                            cus_excel_op.set_cell_value(row, 4, "任务执行时间超过3分钟限制")
                        completed += 1
                    except Exception as e:
                        print(f"\n任务 {cur_num} ({task['ip']}) 执行出错: {str(e)}")
                        with excel_lock:
                            row = cur_num + 1
                            cus_excel_op.set_cell_value(row, 2, "否")
                            cus_excel_op.set_cell_value(row, 3, "执行异常")
                            cus_excel_op.set_cell_value(row, 4, f"异常: {str(e)[:200]}")
                        completed += 1

            print(f"\n{'=' * 60}")
            print("所有任务处理完成！")

            # 最终保存Excel
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"commResult_{timestamp}.xlsx"
            try:
                cus_excel_op.save_workbook(output_file)
                cus_excel_op.save_workbook('commResult.xlsx')
                print(f"Excel结果已保存到: commResult.xlsx")
            except Exception as e:
                print(f"保存Excel结果文件失败: {str(e)}")
                # 尝试保存备份
                try:
                    cus_excel_op.save_workbook('commResult_backup.xlsx')
                    print(f"Excel结果已备份到: commResult_backup.xlsx")
                except:
                    print("备份文件也保存失败")

            # 统计Excel结果
            success_count = 0
            for idx in range(len(tasks)):
                success_cell = cus_excel_op.get_cell_value(idx + 2, 2)
                if success_cell == "是":
                    success_count += 1

            print(f"\nExcel执行统计:")
            print(f"  总任务: {total_tasks}")
            print(f"  成功: {success_count}")
            print(f"  失败: {total_tasks - success_count}")
            print(f"  成功率: {success_count / total_tasks * 100:.1f}%")

            # 统计日志文件
            print(f"\n{'=' * 60}")
            print("日志文件统计:")
            print(f"  日志目录: {log_dir}")

            # 检查日志文件
            log_files = []
            ip_log_links = []

            if os.path.exists(log_dir):
                for filename in os.listdir(log_dir):
                    filepath = os.path.join(log_dir, filename)
                    if os.path.isfile(filepath):
                        if filename.endswith('.log'):
                            # 检查是否是IP链接文件（不带时间戳的）
                            if re.match(r'^[\w\._-]+\.log$', filename) and not re.search(r'\d{8}_\d{6}', filename):
                                ip_log_links.append(filename)
                            else:
                                log_files.append(filename)

            print(f"  生成的日志文件: {len(log_files)} 个")
            print(f"  IP链接文件: {len(ip_log_links)} 个")

            if ip_log_links:
                print("\n  IP链接文件列表:")
                for link_file in sorted(ip_log_links):
                    safe_ip = link_file.replace('.log', '')
                    print(f"    {safe_ip} -> {link_file}")

            if log_files:
                print(f"\n  详细日志文件:")
                for log_file in sorted(log_files):
                    file_size = os.path.getsize(os.path.join(log_dir, log_file))
                    print(f"    {log_file} ({file_size / 1024:.1f} KB)")

            print(f"{'=' * 60}")
            print(f"提示: 您可以通过以下命令查看日志文件:")
            print(f"  查看所有IP的日志文件: ls -la {log_dir}/")
            print(f"  查看特定IP的日志: cat {log_dir}/[IP地址].log")
            print(f"  查看最近的执行日志: tail -f {log_dir}/*.log | grep -A5 -B5 'ERROR\|成功'")
            print(f"{'=' * 60}")

        except FileNotFoundError:
            print("错误: 找不到sshcomm.xlsx文件")
            print("请确保sshcomm.xlsx文件存在，或确保cfg.swap文件存在以便自动创建")
        except Exception as e:
            print(f"处理SSH命令时发生错误: {str(e)}")
            traceback.print_exc()
    else:
        cus_zabbix_api = CusZabbixApi()
        cus_local_method = CusLocalMethod()
        # ![14_按主机批量计算历史最小值、平均值、最大值]
        if args.get_item_history != 'get_item_history':
            cus_excel_op.load_excel('zabbix_api.xlsx', 14)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]
            column_2_list = []
            column_3_list = []
            column_5_list = []
            column_6_list = []
            column_4_list = []
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.get_cell_value(i + 2, 2))
                column_3_list.append(cus_excel_op.get_cell_value(i + 2, 3))
                column_5_list.append(cus_zabbix_api.def_timecovert(str(cus_excel_op.get_cell_value(i + 2, 5))))
                column_6_list.append(cus_zabbix_api.def_timecovert(str(cus_excel_op.get_cell_value(i + 2, 6))))
                column_4_list.append(cus_excel_op.get_cell_value(i + 2, 4))

            title_name = ['主机名', '监控项键值', '数据类型', '单位', '开始时间', '结束时间', '最小值', '平均值', '最大值']
            cus_excel_op.create_new_workbook()
            cus_excel_op.create_sheet(first_active_sheet_name)
            [cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]

            lv_list_get_all_host_itemid = []
            lv_result = None
            executor = ThreadPoolExecutor(GV_CPU_COUNT)
            for lv_result in executor.map(cus_zabbix_api.def_get_host_item, column_1_list, column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_host_itemid.append(lv_result['result'][0]['itemid'])
                else:
                    lv_list_get_all_host_itemid.append('')
                # 等待所有线程完成
            executor.shutdown(wait=True)

            lv_list_get_all_item_history = []
            lv_result = None
            lv_list_01 = []
            i = 1
            executor = ThreadPoolExecutor(GV_CPU_COUNT)
            for lv_result in executor.map(cus_zabbix_api.def_get_item_history, lv_list_get_all_host_itemid, column_3_list, column_5_list, column_6_list):
                if lv_result['tag'] is True:
                    for lv_int_01 in range(len(lv_result['result'])):
                        lv_list_get_all_item_history.append(float(lv_result['result'][lv_int_01]['value']))
                    if column_4_list[i - 1] is None:
                        lv_list_01.append({'value': lv_list_get_all_item_history, 'type': 'N'})
                        # print(dict4)
                    else:
                        lv_list_01.append({'value': lv_list_get_all_item_history, 'type': column_4_list[i - 1]})
                    lv_list_get_all_item_history = []
                else:
                    lv_list_01.append({'value': [], 'type': ''})
                i = i + 1
                # 等待所有线程完成
            executor.shutdown(wait=True)
            i = 0
            for value_list in lv_list_01:
                min_value = None
                avge_value = None
                max_value = None
                if value_list['type'] == 'Mb':
                    min_value = float('%.2f' % (min(value_list['value']) / 1024 / 1024))
                    avge_value = float('%.2f' % (sum(value_list['value']) / len(value_list['value']) / 1024 / 1024))
                    max_value = float('%.2f' % (max(value_list['value']) / 1024 / 1024))
                elif value_list['type'] == 'N':
                    min_value = float('%.2f' % (min(value_list['value'])))
                    avge_value = float('%.2f' % (sum(value_list['value']) / len(value_list['value'])))
                    max_value = float('%.2f' % (max(value_list['value'])))
                print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 按主机批量计算历史值: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m \033[;32m%s\033[0m \033[;32m%s\033[0m'
                      % (len(lv_list_01), i + 1, column_1_list[i], min_value, avge_value, max_value))
                for x in range(1, cus_excel_op.get_dimensions()['columns'] + 1):
                    if x <= 6:
                        cus_excel_op.set_cell_value(i + 2, x, cus_excel_op.get_cell_value(i + 2, x))
                    if x == 7:
                        cus_excel_op.set_cell_value(i + 2, x, min_value)
                    if x == 8:
                        cus_excel_op.set_cell_value(i + 2, x, avge_value)
                    if x == 9:
                        cus_excel_op.set_cell_value(i + 2, x, max_value)
                i = i + 1
            cus_excel_op.save_workbook(first_active_sheet_name + '.xlsx')
        # ![15_按主机批量导出历史数据]
        elif args.get_all_history != 'get_all_history':
            cus_excel_op.load_excel('zabbix_api.xlsx', 15)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]
            column_2_list = []
            column_3_list = []
            column_4_list = []
            column_5_list = []
            column_6_list = []
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.get_cell_value(i + 2, 2))
                column_3_list.append(cus_excel_op.get_cell_value(i + 2, 3))
                column_4_list.append(cus_excel_op.get_cell_value(i + 2, 4))
                column_5_list.append(cus_zabbix_api.def_timecovert(str(cus_excel_op.get_cell_value(i + 2, 5))))
                column_6_list.append(cus_zabbix_api.def_timecovert(str(cus_excel_op.get_cell_value(i + 2, 6))))

            lv_list_get_all_host_itemid = []
            lv_result = None
            executor = ThreadPoolExecutor(GV_CPU_COUNT)
            for lv_result in executor.map(cus_zabbix_api.def_get_host_item, column_1_list, column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_host_itemid.append(lv_result['result'][0]['itemid'])
                else:
                    lv_list_get_all_host_itemid.append('')
                # 等待所有线程完成
            executor.shutdown(wait=True)

            lv_list_get_all_item_history = []
            lv_result = None
            lv_list_01 = []
            lv_list_02 = []
            i = 1
            executor = ThreadPoolExecutor(GV_CPU_COUNT)
            for lv_result in executor.map(cus_zabbix_api.def_get_all_history, lv_list_get_all_host_itemid, column_3_list, column_5_list, column_6_list):
                if lv_result['tag'] is True:
                    if column_4_list[i - 1] == 'Mb':
                        for lv_int_01 in range(len(lv_result['result'])):
                            lv_list_get_all_item_history.append(float(lv_result['result'][lv_int_01]['value']) / 1024 / 1024)
                            lv_list_02.append(time.strftime("%Y-%m-%d %H:%M:%S",
                                                            time.localtime(float(lv_result['result'][lv_int_01]['clock']))))
                        lv_list_01.append({'value': lv_list_get_all_item_history, 'type': column_4_list[i - 1], 'clock': lv_list_02})
                    else:
                        for lv_int_01 in range(len(lv_result['result'])):
                            lv_list_get_all_item_history.append(lv_result['result'][lv_int_01]['value'])
                            lv_list_02.append(time.strftime("%Y-%m-%d %H:%M:%S",
                                                            time.localtime(float(lv_result['result'][lv_int_01]['clock']))))
                        lv_list_01.append({'value': lv_list_get_all_item_history, 'type': column_4_list[i - 1], 'clock': lv_list_02})
                    lv_list_get_all_item_history = []
                else:
                    lv_list_01.append({'value': [], 'type': '', "clock": []})
                i = i + 1
                # 等待所有线程完成
            executor.shutdown(wait=True)
            i = None
            cus_excel_op.create_new_workbook()
            for lv_int_01 in range(len(lv_list_01)):
                item_name = re.sub(r'\W', "", column_2_list[lv_int_01])
                pattern = re.compile(r'^(.{1,29}).*$')
                item_name = re.search(pattern, item_name).group(1)
                cus_excel_op.create_sheet(str(lv_int_01 + 1) + '_' + item_name)
                title_name = ['主机名', '监控项键值', '数据类型', '单位', '开始时间', '结束时间', '收到值的时间', '收到的值']
                [cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
                for y in range(len(title_name)):
                    for lv_int_03 in range(len(lv_list_01[lv_int_01]['value'])):
                        if y <= 5:
                            cus_excel_op.set_cell_value(lv_int_03 + 2, y + 1, cus_excel_op.get_cell_value(lv_int_01 + 2, y + 1))
                        elif y == 6:
                            cus_excel_op.set_cell_value(lv_int_03 + 2, y + 1, lv_list_01[lv_int_01]['clock'][lv_int_03])
                        elif y == 7:
                            cus_excel_op.set_cell_value(lv_int_03 + 2, y + 1, lv_list_01[lv_int_01]['value'][lv_int_03])
                print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 按主机批量获取历史值: \033[;32m%s\033[0m 成功'
                      % (len(column_1_list), lv_int_01 + 1, column_1_list[lv_int_01]))
            cus_excel_op.save_workbook(first_active_sheet_name + '.xlsx')
        elif args.get_hostgroup_host != 'get_hostgroup_host':
            cus_excel_op.load_excel('zabbix_api.xlsx', 16)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]

            lv_list_get_all_host_groupid = [""] * len(column_1_list)  # 预初始化
            with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
                future_to_index = {}
                for i, col in enumerate(column_1_list):
                    if col:  # 只有当col非空时才提交任务
                        future = executor.submit(cus_zabbix_api.def_get_hostgroup_6_4, col)
                        future_to_index[future] = i

                for future in as_completed(future_to_index):
                    index = future_to_index[future]
                    try:
                        result = future.result()
                        groupid = result['result'][0]['groupid'] if result.get('tag') else ""
                    except (KeyError, IndexError, TypeError):
                        groupid = ""
                    lv_list_get_all_host_groupid[index] = groupid

            lv_list_get_all_host_name = [""] * len(lv_list_get_all_host_groupid)  # 预初始化
            with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
                future_to_index = {}
                for i, col in enumerate(lv_list_get_all_host_groupid):
                    if col:  # 只有当col非空时才提交任务
                        future = executor.submit(cus_zabbix_api.def_get_hostgroup_host, col)
                        future_to_index[future] = i

                for future in as_completed(future_to_index):
                    index = future_to_index[future]
                    host_info_list = []
                    try:
                        result = future.result()
                        if result.get('tag') is True and isinstance(result.get('result'), list):
                            # 初始化存储所有结果的列表

                            # 遍历result['result']中的每个主机信息
                            for host_info in result['result']:
                                # 安全获取每个字段
                                host = host_info.get('host', '')
                                name = host_info.get('name', '')
                                groupname = host_info.get('hostgroups', [])
                                template = host_info.get('parentTemplates', [])
                                interface = host_info.get('interfaces', [])
                                proxyid = host_info.get('proxyid', '')
                                proxy_groupid = host_info.get('proxy_groupid', '')

                                # 添加到结果列表
                                host_info_list.append({
                                    'host': host,
                                    'name': name,
                                    'hostgroups': groupname,
                                    'parentTemplates': template,
                                    'interfaces': interface,
                                    'proxyid': proxyid,
                                    'proxy_groupid': proxy_groupid
                                })

                    except (KeyError, IndexError, TypeError):
                        # 添加到结果列表
                        host_info_list.append({
                            'host': "",
                            'name': "",
                            'hostgroups': [],
                            'parentTemplates': [],
                            'interfaces': [],
                            'proxyid': "",
                            'proxy_groupid': "",
                        })
                    # 将整个列表存入结果（或根据需求选择第一个元素）
                    lv_list_get_all_host_name[index] = host_info_list

            # 方法1：使用字典推导式高效去重（推荐）
            unique_hosts = {}
            for sublist in lv_list_get_all_host_name:
                for host_dict in sublist:
                    unique_hosts[host_dict['host']] = host_dict  # 自动去重，保留最后出现的记录

            # 转换为去重后的列表
            deduplicated_list = list(unique_hosts.values())

            #################
            lv_list_get_all_host_Proxyid = [""] * len(deduplicated_list)  # 预初始化
            lv_list_get_all_host_Proxygroupid = [""] * len(deduplicated_list)  # 预初始化

            with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
                # 提交任务：获取 Proxy 和 ProxyGroup 名称
                future_to_proxy = {}
                future_to_proxygroup = {}

                for i, host_data in enumerate(deduplicated_list):
                    if host_data.get("proxyid", ""):  # 非空检查
                        # 提交获取 Proxy 名称的任务
                        future_proxy = executor.submit(
                            cus_zabbix_api.def_get_proxy_name,
                            host_data.get("proxyid", "")
                        )
                        future_to_proxy[future_proxy] = i
                    if host_data.get("proxy_groupid", ""):  # 非空检查
                        # 提交获取 ProxyGroup 名称的任务
                        future_proxygroup = executor.submit(
                            cus_zabbix_api.def_get_proxygroup_name,
                            host_data.get("proxy_groupid", "")
                        )
                        future_to_proxygroup[future_proxygroup] = i

                # 处理 Proxy 结果
                for future in as_completed(future_to_proxy):
                    index = future_to_proxy[future]
                    try:
                        result = future.result()
                        proxyname = result['result'][0]['name'] if result.get('tag') else ""
                    except (KeyError, IndexError, TypeError):
                        proxyname = ""
                    lv_list_get_all_host_Proxyid[index] = {
                        "host": deduplicated_list[index].get("host", ""),
                        "proxyname": proxyname
                    }

                # 处理 ProxyGroup 结果
                for future in as_completed(future_to_proxygroup):
                    index = future_to_proxygroup[future]
                    try:
                        result = future.result()
                        proxygroupname = result['result'][0]['name'] if result.get('tag') else ""
                    except (KeyError, IndexError, TypeError):
                        proxygroupname = ""
                    lv_list_get_all_host_Proxygroupid[index] = {
                        "host": deduplicated_list[index].get("host", ""),
                        "proxygroupname": proxygroupname
                    }

            excel_info = ["主机", "主机组", "模板", "接口", "Proxy", "Proxy组"]
            cus_excel_op.create_new_workbook()

            # 统一配置所有表的结构和数据映射
            sheet_configs = {
                "主机": {
                    "headers": ['主机名', '主机组', '可见名'],
                    "columns": {'主机名': 1, '主机组': 3, '可见名': 15},
                    "data_mapping": {
                        "主机名": lambda data: data.get("host", ""),
                        "主机组": lambda data: data.get("hostgroups", [{}])[0].get("name", ""),
                        "可见名": lambda data: data.get("name", "")
                    },
                    "data_source": deduplicated_list,
                    "is_single_row": True  # 每个主机单行显示
                },
                "主机组": {
                    "headers": ['主机名', '主机组'],
                    "columns": {'主机名': 1, '主机组': 2},
                    "data_mapping": {
                        "主机名": lambda data: data.get("host", ""),
                        "主机组": lambda item: item.get("name", "")  # 注意：这里处理的是hostgroups中的单个项
                    },
                    "data_source": deduplicated_list,
                    "list_field": "hostgroups"  # 需要展开的列表字段
                },
                "模板": {
                    "headers": ['主机名', '模板名称'],
                    "columns": {'主机名': 1, '模板名称': 2},
                    "data_mapping": {
                        "主机名": lambda data: data.get("host", ""),
                        "模板名称": lambda item: item.get("host", "")  # 处理parentTemplates中的项
                    },
                    "data_source": deduplicated_list,
                    "list_field": "parentTemplates"
                },
                "接口": {
                    "headers": ['主机名', '接口类型', '接口IP', '端口号', 'SNMP版本', '安全级别',
                                '认证协议', '隐私协议', '团体字', '安全名称', '认证口令', '私钥'],
                    "columns": {h: i + 1 for i, h in enumerate(['主机名', '接口类型', '接口IP', '端口号', 'SNMP版本',
                                                                '安全级别', '认证协议', '隐私协议', '团体字',
                                                                '安全名称', '认证口令', '私钥'])},
                    "data_mapping": {
                        "主机名": lambda data: data.get("host", ""),
                        "接口类型": lambda item: item.get("type", ""),
                        "接口IP": lambda item: item.get("ip", ""),
                        "端口号": lambda item: item.get("port", ""),
                        "SNMP版本": lambda item: cus_local_method.def_get_nested_value(item, "details", "version"),
                        "安全级别": lambda item: cus_local_method.def_get_nested_value(item, "details", "securitylevel"),
                        "认证协议": lambda item: cus_local_method.def_get_nested_value(item, "details", "authprotocol"),
                        "隐私协议": lambda item: cus_local_method.def_get_nested_value(item, "details", "privprotocol"),
                        "团体字": lambda item: cus_local_method.def_get_nested_value(item, "details", "community"),
                        "安全名称": lambda item: cus_local_method.def_get_nested_value(item, "details", "securityname"),
                        "认证口令": lambda item: cus_local_method.def_get_nested_value(item, "details", "authpassphrase"),
                        "私钥": lambda item: cus_local_method.def_get_nested_value(item, "details", "privpassphrase"),
                    },
                    "data_source": deduplicated_list,
                    "list_field": "interfaces"
                },
                "Proxy": {
                    "headers": ['主机名', 'Proxy'],
                    "columns": {'主机名': 1, 'Proxy': 2},
                    "data_source": lv_list_get_all_host_Proxyid,
                    "data_mapping": {
                        "主机名": lambda data: data.get("host", ""),
                        "Proxy": lambda data: data.get("proxyname", "")
                    },
                    "is_single_row": True,
                    "skip_condition": lambda data: not data.get("proxyname")  # 新增：proxyname为空时跳过
                },
                "Proxy组": {
                    "headers": ['主机名', 'Proxy组'],
                    "columns": {'主机名': 1, 'Proxy组': 2},
                    "data_source": lv_list_get_all_host_Proxygroupid,
                    "data_mapping": {
                        "主机名": lambda data: data.get("host", ""),
                        "Proxy组": lambda data: data.get("proxygroupname", "")
                    },
                    "is_single_row": True,
                    "skip_condition": lambda data: not data.get("proxygroupname")  # 新增：proxygroupname为空时跳过
                }
            }

            # 统一处理所有工作表
            for sheet_name in excel_info:
                if sheet_name not in sheet_configs:
                    continue

                config = sheet_configs[sheet_name]
                cus_excel_op.create_sheet(sheet_name)
                cus_excel_op.activate_sheet(sheet_name)

                # 1. 写入表头
                headers = config["headers"]
                columns = config["columns"] if config.get("columns") else {h: i + 1 for i, h in enumerate(headers)}
                for header in headers:
                    cus_excel_op.set_cell_value(1, columns[header], header)
                # 2. 写入数据（带进度显示）
                total_items = len(config["data_source"])
                print(f"\n\033[1;34m▶ 开始处理工作表 [{sheet_name}] (共 {total_items} 条数据)\033[0m")
                # 2. 写入数据
                row_idx = 2
                success_count = 0
                skipped_count = 0
                for data_idx, data in enumerate(config["data_source"], 1):
                    # 进度显示（每处理10条显示一次，或最后一条）
                    if data_idx % 10 == 0 or data_idx == total_items:
                        print(f"\033[36m进度: {data_idx}/{total_items} | 成功: {success_count} | 跳过: {skipped_count}\033[0m", end='\r')
                    # 新增：检查跳过条件
                    if config.get("skip_condition") and config["skip_condition"](data):
                        skipped_count += 1
                        continue
                    try:
                        if config.get("is_single_row"):
                            # 单行模式处理
                            for header, col in columns.items():
                                value = config["data_mapping"][header](data)
                                cus_excel_op.set_cell_value(row_idx, col, value)

                            # 成功写入后显示（示例显示主机名）
                            host_name = config["data_mapping"]["主机名"](data) if "主机名" in columns else ""
                            print(f'(\033[34m{data_idx}\033[0m/\033[34m{total_items}\033[0m): -> {sheet_name}记录: \033[32m{host_name}\033[0m 成功')
                            success_count += 1
                            row_idx += 1

                        elif "list_field" in config:
                            # 多行展开模式处理
                            list_items = data.get(config["list_field"], [])
                            for item in list_items:
                                for header, col in columns.items():
                                    value = config["data_mapping"][header](item if header != "主机名" else data)
                                    cus_excel_op.set_cell_value(row_idx, col, value)
                                row_idx += 1

                            if list_items:  # 只有实际写入时才计数
                                host_name = config["data_mapping"]["主机名"](data) if "主机名" in columns else ""
                                print(f'(\033[34m{data_idx}\033[0m/\033[34m{total_items}\033[0m): -> {sheet_name}记录: \033[32m{host_name}\033[0m 成功 ({len(list_items)}条)')
                                success_count += len(list_items)

                    except Exception as e:
                        # 获取当前异常的traceback对象
                        tb = traceback.extract_tb(e.__traceback__)
                        # 获取异常发生时的行号
                        line_number = tb[-1][1]
                        # 输出异常信息和行号
                        print(f'\033[31m错误在行号 {line_number} -> 处理第 {data_idx} 条数据失败 - {str(e)}\033[0m')
                        continue

                # 工作表处理完成统计
                print(f"\n\033[1;32m✓ 工作表 [{sheet_name}] 处理完成 - 成功: {success_count} | 跳过: {skipped_count} | 总进度: {data_idx}/{total_items}\033[0m\n")
            cus_excel_op.save_workbook(first_active_sheet_name + '.xlsx')

        elif args.update_host_name != 'update_host_name':
            cus_excel_op.load_excel('zabbix_api.xlsx', 55)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            column_1_list = cus_excel_op.get_column_values(1)
            column_2_list = []
            del column_1_list[0]
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.get_cell_value(i + 2, 2))

            total_hosts = len(column_1_list)
            print(f"\033[34m开始处理 {total_hosts} 个主机...\033[0m")

            # 第一部分：获取所有主机ID
            lv_list_get_all_host_id = [""] * total_hosts  # 预初始化
            with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
                future_to_index = {}
                for i, col in enumerate(column_1_list):
                    if col:  # 只有当col非空时才提交任务
                        future = executor.submit(cus_zabbix_api.def_get_host, col)
                        future_to_index[future] = i

                completed = 0
                for future in as_completed(future_to_index):
                    index = future_to_index[future]
                    try:
                        result = future.result()
                        hostid = {"hostid": result['result'][0]['hostid'], "hostname": column_2_list[index]} if result.get('tag') else {}
                    except (KeyError, IndexError, TypeError):
                        hostid = {}
                    lv_list_get_all_host_id[index] = hostid

                    completed += 1
                    print(f'(\033[34m{completed}\033[0m/\033[34m{total_hosts}\033[0m): -> {column_1_list[index]} 获取主机ID: \033[32m{column_2_list[index] if column_1_list[index] else "空"}\033[0m {"成功" if hostid else "失败"}', end='\r')

            print()  # 换行

            # 第二部分：更新主机名
            valid_hosts = sum(1 for host in lv_list_get_all_host_id if host)
            print(f"\033[34m开始更新 {valid_hosts} 个有效主机名...\033[0m")

            lv_list_get_all_host_name = [""] * len(lv_list_get_all_host_id)  # 预初始化
            with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
                future_to_index = {}
                submitted = 0
                for i, col in enumerate(lv_list_get_all_host_id):
                    if col:  # 只有当col非空时才提交任务
                        future = executor.submit(cus_zabbix_api.def_update_host_name, col.get("hostid"), col.get("hostname"))
                        future_to_index[future] = i
                        submitted += 1

                completed = 0
                for future in as_completed(future_to_index):
                    index = future_to_index[future]
                    try:
                        result = future.result()
                        hostid = result['result']['hostids'][0] if result.get('tag') else ""
                    except (KeyError, IndexError, TypeError):
                        hostid = ""

                    completed += 1
                    hostname = lv_list_get_all_host_id[index].get("hostname", "未知")
                    print(f'(\033[34m{completed}\033[0m/\033[34m{submitted}\033[0m): -> {column_1_list[index]} 更新主机名: \033[32m{hostname}\033[0m {"成功" if hostid else "失败"}', end='\r')

            print("\n\033[32m所有操作完成!\033[0m")  # 最终换行和完成提示

        # ![17_批量停止已启用触发器]
        elif args.stop_all_priority_trigger != 'stop_all_priority_trigger':
            cus_excel_op.load_excel('zabbix_api.xlsx', 17)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            priority = []
            for i in range(2, cus_excel_op.get_dimensions()['rows'] + 1):
                try:
                    priority.append(cus_excel_op.get_cell_value(i, 1))
                except Exception as e:
                    print(u"%s 表第\033[;31m%s\033[0m行数据异常 共\033[;31m%s\033[0m行\n\033[;31m%s\033[0m" % (first_active_sheet_name, i, cus_excel_op.get_dimensions()['rows'] + 1, e))
                    sys.exit(1)
            cus_zabbix_api.def_stop_all_priority_trigger(priority)
        # ![17_批量停止已启用触发器]
        elif args.stop_all_priority_trigger_by_description != 'stop_all_priority_trigger_by_description':
            cus_excel_op.load_excel('zabbix_api.xlsx', 17)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            priority = []
            description = cus_excel_op.get_cell_value(2, 2)
            for i in range(2, cus_excel_op.get_dimensions()['rows'] + 1):
                try:
                    priority.append(cus_excel_op.get_cell_value(i, 1))

                except Exception as e:
                    print(u"%s 表第\033[;31m%s\033[0m行数据异常 共\033[;31m%s\033[0m行\n\033[;31m%s\033[0m" % (first_active_sheet_name, i, cus_excel_op.get_dimensions()['rows'] + 1, e))
                    sys.exit(1)
            cus_zabbix_api.def_stop_all_priority_trigger_by_description(priority, description)
        elif args.start_all_priority_trigger != 'start_all_priority_trigger':
            cus_excel_op.load_excel('zabbix_api.xlsx', 17)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            priority = []
            for i in range(2, cus_excel_op.get_dimensions()['rows'] + 1):
                try:
                    priority.append(cus_excel_op.get_cell_value(i, 1))
                except Exception as e:
                    print(u"%s 表第\033[;31m%s\033[0m行数据异常 共\033[;31m%s\033[0m行\n\033[;31m%s\033[0m" % (first_active_sheet_name, i, cus_excel_op.get_dimensions()['rows'] + 1, e))
                    sys.exit(1)
            cus_zabbix_api.def_start_all_priority_trigger(priority)
        # ![批量停止不支持监控项]
        elif args.stop_all_unsupport_item != 'stop_all_unsupport_item':
            cus_zabbix_api.def_stop_all_unsupport_item()
        elif args.start_all_unsupport_item != 'start_all_unsupport_item':
            cus_zabbix_api.def_start_all_unsupport_item()

        # ![18_根据监控项历史值关联模板]
        elif args.massadd_host_template_base_20221003 != 'massadd_host_template_base_20221003':
            cus_excel_op.load_excel('zabbix_api.xlsx', 18)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]
            sheet_name = u'附加模板'
            title_name = ['序号', '主机名', 'IP', '模板名称', '结果', '原因']
            cus_excel_op.create_new_workbook()
            cus_excel_op.create_sheet(first_active_sheet_name)
            [cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
            [
                [
                    [
                        (
                            (print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> ' % (len(cus_zabbix_api.def_get_hostgroup_host(o['groupid'])), x + 1), end=''), cus_zabbix_api.def_massadd_host_template_base_20221003(cus_excel_op, x + 1, cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['host'], ''.join([f_i['ip'] for f_i in cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['interfaces']]), cus_excel_op.get_cell_value(2, 5), [{'hostid': cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['hostid']}], cus_zabbix_api.def_get_template(cus_excel_op.get_cell_value(2, 5))))
                            if cus_zabbix_api.def_get_template(cus_excel_op.get_cell_value(2, 5)) != [] else
                            [print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 主机: \033[;31m%s\033[0m 关联模板 \033[;31m%s\033[0m 失败! 原因: \033[;31m%s\033[0m"' % (len(cus_zabbix_api.def_get_hostgroup_host(o['groupid'])), x + 1, cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['host'], cus_excel_op.get_cell_value(2, 5), '未找到定义的模板名')), cus_excel_op.set_cell_value(x + 2, 1, x + 1), cus_excel_op.set_cell_value(x + 2, 2, cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['host']), cus_excel_op.set_cell_value(x + 2, 3, ''.join([f_i['ip'] for f_i in cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['interfaces']])), cus_excel_op.set_cell_value(x + 2, 4, cus_excel_op.get_cell_value(2, 5)), cus_excel_op.set_cell_value(x + 2, 5, '失败'), cus_excel_op.set_cell_value(x + 2, 6, '未找到定义的模板名')]
                        ) for x in range(len(cus_zabbix_api.def_get_hostgroup_host(o['groupid'])))
                    ] for o in cus_zabbix_api.def_get_hostgroup_6_0(column_1_list[i])
                ] for i in range(len(column_1_list))
            ]
            cus_excel_op.save_workbook('01_' + sheet_name + '.xlsx')
        elif args.massupdate_host_template_base_20221003 != 'massupdate_host_template_base_20221003':
            cus_excel_op.load_excel('zabbix_api.xlsx', 18)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]
            column_2_list = cus_excel_op.get_column_values(2)
            del column_2_list[0]
            column_3_list = cus_excel_op.get_column_values(3)
            del column_3_list[0]
            dic_key_list = cus_excel_op.get_column_values(6)
            del dic_key_list[0]
            dic_value_list = cus_excel_op.get_column_values(7)
            del dic_value_list[0]
            dic_res = {}
            [dic_res.update({dic_key_list[f_i]: dic_value_list[f_i]}) for f_i in range(len(dic_key_list))]
            sheet_name = u'更新模板'
            title_name = ['序号', '主机名', 'IP', '历史值', '模板名称', '结果', '原因']
            cus_excel_op.create_new_workbook()
            cus_excel_op.create_sheet(first_active_sheet_name)
            [cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
            [
                [
                    [
                        [
                            (print('(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> ' % (len(cus_zabbix_api.def_get_hostgroup_host(o['groupid'])), x + 1), end=''),
                             cus_zabbix_api.def_massadd_host_template_base_item_20221003(cus_excel_op,
                                                                                         x + 1,
                                                                                         cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['host'],
                                                                                         ''.join([f_i['ip'] for f_i in cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['interfaces']]),
                                                                                         ''.join([''.join([''.join([a['value'] for a in cus_zabbix_api.def_get_item_history_base_20221003(z['itemid'], column_3_list[y])]) for z in cus_zabbix_api.def_get_host_item(cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['host'], column_2_list[y])]) for y in range(len(column_2_list))]),
                                                                                         dic_res.get(''.join([''.join([''.join([a['value'] for a in cus_zabbix_api.def_get_item_history_base_20221003(z['itemid'], column_3_list[y])]) for z in cus_zabbix_api.def_get_host_item(cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['host'], column_2_list[y])]) for y in range(len(column_2_list))])),
                                                                                         [{'hostid': c['hostid']}],
                                                                                         cus_zabbix_api.def_get_template(dic_res.get(''.join([''.join([''.join([a['value'] for a in cus_zabbix_api.def_get_item_history_base_20221003(z['itemid'], column_3_list[y])]) for z in cus_zabbix_api.def_get_host_item(cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['host'], column_2_list[y])]) for y in range(len(column_2_list))]))))
                             ) for c in cus_zabbix_api.def_get_host(cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['host'])

                        ]
                        if dic_res.get(''.join([''.join([''.join([a['value'] for a in cus_zabbix_api.def_get_item_history_base_20221003(z['itemid'], column_3_list[y])]) for z in cus_zabbix_api.def_get_host_item(cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['host'], column_2_list[y])]) for y in range(len(column_2_list))])) is not None else
                        [
                            print('(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 主机: \033[;31m%s\033[0m 获取监控项值为: \033[;31m%s\033[0m 关联模板失败! 原因: 历史值对应关系异常' % (len(cus_zabbix_api.def_get_hostgroup_host(o['groupid'])), x + 1, cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['host'], ''.join([''.join([''.join([a['value'] for a in cus_zabbix_api.def_get_item_history_base_20221003(z['itemid'], column_3_list[y])]) for z in cus_zabbix_api.def_get_host_item(cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['host'], column_2_list[y])]) for y in range(len(column_2_list))]))),
                            cus_excel_op.set_cell_value(x + 2, 1, x + 1),
                            cus_excel_op.set_cell_value(x + 2, 2, cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['host']),
                            cus_excel_op.set_cell_value(x + 2, 3, ''.join([f_i['ip'] for f_i in cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['interfaces']])),
                            cus_excel_op.set_cell_value(x + 2, 4, ''.join([''.join([''.join([a['value'] for a in cus_zabbix_api.def_get_item_history_base_20221003(z['itemid'], column_3_list[y])]) for z in cus_zabbix_api.def_get_host_item(cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['host'], column_2_list[y])]) for y in range(len(column_2_list))])),
                            cus_excel_op.set_cell_value(x + 2, 5, ''),
                            cus_excel_op.set_cell_value(x + 2, 6, '失败'),
                            cus_excel_op.set_cell_value(x + 2, 7, '历史值对应关系异常')
                        ] for x in range(len(cus_zabbix_api.def_get_hostgroup_host(o['groupid'])))
                    ] for o in cus_zabbix_api.def_get_hostgroup_6_0(column_1_list[i])
                ] for i in range(len(column_1_list))
            ]
            cus_excel_op.save_workbook('02_' + sheet_name + '.xlsx')
        elif args.def_massremove_host_templateids_clear_base_20221003 != 'def_massremove_host_templateids_clear_base_20221003':
            cus_excel_op.load_excel('zabbix_api.xlsx', 18)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]
            sheet_name = u'脱离模板'
            title_name = ['序号', '主机名', 'IP', '模板名称', '结果', '原因']
            cus_excel_op.create_new_workbook()
            cus_excel_op.create_sheet(first_active_sheet_name)
            [cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
            [
                [
                    [
                        (
                            (
                                print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> ' % (len(cus_zabbix_api.def_get_hostgroup_host(o['groupid'])), x + 1), end=''),
                                cus_zabbix_api.def_massremove_host_templateids_clear_base_20221003(cus_excel_op,
                                                                                                   x + 1,
                                                                                                   cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['host'],
                                                                                                   ''.join([f_i['ip'] for f_i in cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['interfaces']]),
                                                                                                   cus_excel_op.get_cell_value(2, 5),
                                                                                                   [cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['hostid']],
                                                                                                   [u['templateid'] for u in cus_zabbix_api.def_get_template(cus_excel_op.get_cell_value(2, 5))]
                                                                                                   )
                            )
                            if cus_zabbix_api.def_get_template(cus_excel_op.get_cell_value(2, 5)) != [] else
                            [print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 主机: \033[;31m%s\033[0m 脱离模板 \033[;31m%s\033[0m 失败! 原因: \033[;31m%s\033[0m"' % (len(cus_zabbix_api.def_get_hostgroup_host(o['groupid'])), x + 1, cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['host'], cus_excel_op.get_cell_value(2, 5), '未找到定义的模板名')), cus_excel_op.set_cell_value(x + 2, 1, x + 1), cus_excel_op.set_cell_value(x + 2, 2, cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['host']), cus_excel_op.set_cell_value(x + 2, 3, ''.join([f_i['ip'] for f_i in cus_zabbix_api.def_get_hostgroup_host(o['groupid'])[x]['interfaces']])), cus_excel_op.set_cell_value(x + 2, 4, cus_excel_op.get_cell_value(2, 5)), cus_excel_op.set_cell_value(x + 2, 5, '失败'), cus_excel_op.set_cell_value(x + 2, 6, '未找到定义的模板名')]
                        ) for x in range(len(cus_zabbix_api.def_get_hostgroup_host(o['groupid'])))
                    ] for o in cus_zabbix_api.def_get_hostgroup_6_0(column_1_list[i])
                ] for i in range(len(column_1_list))]
            cus_excel_op.save_workbook('03_' + sheet_name + '.xlsx')
        # ![34_获取所有告警信息]
        elif args.get_all_alert != 'get_all_alert':
            cus_excel_op.load_excel('zabbix_api.xlsx', 34)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]
            cus_excel_op.create_new_workbook()
            # def_get_all_alert | def_get_all_alert_custom
            lv_list_get_action = []
            lv_result = None
            executor = ThreadPoolExecutor(GV_CPU_COUNT)
            for lv_result in executor.map(cus_zabbix_api.def_get_action, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_action.append(lv_result['result'][0]['actionid'])
                else:
                    lv_list_get_action.append('')
                # 等待所有线程完成
            executor.shutdown(wait=True)

            res = [cus_zabbix_api.def_get_all_alert("".join(lv_list_get_action),
                                                    cus_zabbix_api.def_timecovert(str(cus_excel_op.get_cell_value(i_01 + 2, 2))),
                                                    cus_zabbix_api.def_timecovert(str(cus_excel_op.get_cell_value(i_01 + 2, 3))))
                   for i_01 in range(len(column_1_list))]
            for i_01 in range(len(res)):
                cus_excel_op.create_sheet(str(i_01 + 1))
                lv_list_02 = []
                if not res[i_01]:
                    print('告警列表为空，请检查告警动作与excel导出日期')
                    exit(1)
                [lv_list_02.append(i_04) for i_04 in res[i_01][0].keys()]
                for i in range(len(lv_list_02)):
                    cus_excel_op.set_cell_value(1, i + 1, lv_list_02[i])
                for i_02 in range(len(res[i_01])):
                    lv_list_01 = []
                    [lv_list_01.append(i_03) for i_03 in res[i_01][i_02].values()]
                    for i_04 in range(len(lv_list_02)):
                        try:
                            if lv_list_01[i_04] == '':
                                pass
                            # elif lv_list_02[i_04] == u'告警日期':
                            #     excel_op.set_cell_value(i_02 + 2, i_04 + 1, time.strftime("%Y-%m-%d", time.localtime(float(res[i_01][i_02][u'告警日期']))))
                            # elif lv_list_02[i_04] == u'告警时间':
                            #     excel_op.set_cell_value(i_02 + 2, i_04 + 1, time.strftime("%H:%M:%S", time.localtime(float(res[i_01][i_02][u'告警时间']))))
                            elif lv_list_02[i_04] == u'执行状态' or lv_list_02[i_04] == u'告警级别':
                                cus_excel_op.set_cell_value(i_02 + 2, i_04 + 1,
                                                                cus_zabbix_api.def_convert_numeric_to_text(
                                                                    lv_list_01[i_04]))
                            elif lv_list_02[i_04] == u'触发器状态':
                                cus_excel_op.set_cell_value(i_02 + 2, i_04 + 1,
                                                                cus_zabbix_api.def_convert_numeric_to_text_problem(
                                                                    lv_list_01[i_04]))
                            else:
                                cus_excel_op.set_cell_value(i_02 + 2, i_04 + 1, lv_list_01[i_04])
                        except:
                            pass

                    print(u'(进度: -> \033[;34m%s\033[0m/\033[;34m%s\033[0m)\n' % (len(res[i_01]), i_02 + 1), end='')
            cus_excel_op.save_workbook(first_active_sheet_name + '.xlsx')

        elif args.get_all_problem != 'get_all_problem':
            cus_excel_op.load_excel('zabbix_api.xlsx', 49)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            cus_excel_op.create_new_workbook()
            cus_excel_op.create_sheet(first_active_sheet_name)
            res = cus_zabbix_api.def_get_all_problem(cus_zabbix_api.def_timecovert(str(cus_excel_op.get_cell_value(2, 1))),
                                                     cus_zabbix_api.def_timecovert(str(cus_excel_op.get_cell_value(2, 2))))
            lv_int01 = 0
            for key, value in res[0].items():
                if key == 'triggerid':
                    continue
                cus_excel_op.set_cell_value(1, lv_int01 + 1, key)
                lv_int01 = lv_int01 + 1
            for i_01 in range(len(res)):
                for key, value in res[i_01].items():
                    # elif lv_list_02[i_04] == u'告警日期':
                    #     excel_op.set_cell_value(i_02 + 2, i_04 + 1, time.strftime("%Y-%m-%d", time.localtime(float(res[i_01][i_02][u'告警日期']))))
                    # elif lv_list_02[i_04] == u'告警时间':
                    #     excel_op.set_cell_value(i_02 + 2, i_04 + 1, time.strftime("%H:%M:%S", time.localtime(float(res[i_01][i_02][u'告警时间']))))
                    if key == u'triggerid':
                        lv_strHostObject = cus_zabbix_api.def_get_host_trigger(value)['result'][0]
                        lv_strGroupName = ''
                        lv_list01 = ['Linux服务器', '000 队列']
                        for int01 in lv_strHostObject['groups']:
                            if lv_list01.count(int01['name']) != 1:
                                lv_strGroupName = int01['name']
                        cus_excel_op.set_cell_value(i_01 + 2, 1, str(lv_strGroupName))
                        cus_excel_op.set_cell_value(i_01 + 2, 2, str(lv_strHostObject['hosts'][0]['host']))
                        cus_excel_op.set_cell_value(i_01 + 2, 3, str(lv_strHostObject['hosts'][0]['name']))

                    elif key == u'问题名称':
                        cus_excel_op.set_cell_value(i_01 + 2, 4, value)
                    elif key == u'是否确认':
                        cus_excel_op.set_cell_value(i_01 + 2, 5, value)
                    elif key == u'问题等级':
                        cus_excel_op.set_cell_value(i_01 + 2, 6, cus_zabbix_api.def_convert_numeric_to_text_problem_severity(value))
                    elif key == u'运营数据':
                        cus_excel_op.set_cell_value(i_01 + 2, 7, value)
                    elif key == u'问题日期':
                        cus_excel_op.set_cell_value(i_01 + 2, 8,
                                                        time.strftime("%Y-%m-%d", time.localtime(
                                                            int(value))))
                        cus_excel_op.set_cell_value(i_01 + 2, 9,
                                                        time.strftime("%H:%M:%S", time.localtime(
                                                            int(value))))
                print(u'(进度: -> \033[;34m%s\033[0m/\033[;34m%s\033[0m)\n' % (len(res), i_01 + 1), end='')
            cus_excel_op.save_workbook(first_active_sheet_name + '.xlsx')

        # ![35_获取所有事件信息]
        elif args.get_all_event != 'get_all_event':
            cus_excel_op.load_excel('zabbix_api.xlsx', 35)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]
            list_group_host = []
            for i in range(len(column_1_list)):
                for o in cus_zabbix_api.def_get_hostgroup_6_0(column_1_list[i])['result']:
                    for x in range(len(cus_zabbix_api.def_get_hostgroup_host(o['groupid'])['result'])):
                        list_group_host.append(cus_zabbix_api.def_get_hostgroup_host(o['groupid'])['result'][x]['host'])
            column_2_list = cus_excel_op.get_column_values(2)
            del column_2_list[0]
            list_all_event_host = []
            for i_01 in range(len(column_2_list)):
                for str_01 in cus_zabbix_api.def_get_all_event(cus_excel_op.get_cell_value(i_01 + 2, 2),
                                                               cus_zabbix_api.def_timecovert(str(cus_excel_op.get_cell_value(i_01 + 2, 3))),
                                                               cus_zabbix_api.def_timecovert(str(cus_excel_op.get_cell_value(i_01 + 2, 4))))['result']:
                    for str_02 in str_01['hosts']:
                        list_all_event_host.append(str_02['host'])
            res = [val for val in list_group_host if val in list_all_event_host]
            list_ip = []
            str_ip = ""
            list_ip_tmp = []
            for i in range(len(res)):
                for o in cus_zabbix_api.def_get_host(res[i])['result']:
                    for u in cus_zabbix_api.def_get_host_ip([(o["hostid"])])['result']:
                        for x in u['interfaces']:
                            list_ip_tmp.append(x['ip'])
                        str_ip = ",".join(list_ip_tmp)
                        list_ip.append(str_ip)
                        list_ip_tmp = []
                        str_ip = ""
            title_name = ['主机名', 'IP地址']
            cus_excel_op.create_new_workbook()
            cus_excel_op.create_sheet(first_active_sheet_name)
            [cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
            for i in range(len(res)):
                for o in range(len(title_name)):
                    if o == 0:
                        cus_excel_op.set_cell_value(i + 2, 1, res[i])
                    if o == 1:
                        cus_excel_op.set_cell_value(i + 2, 2, list_ip[i])
            cus_excel_op.save_workbook(first_active_sheet_name + '.xlsx')
            [[print(u'(进度: -> \033[;34m%s\033[0m/\033[;34m%s\033[0m)' % (len(res), i + 1), end=''), cus_zabbix_api.def_delete_host([(o["hostid"]) for o in cus_zabbix_api.def_get_host(res[i])['result']])['result']] for i in range(len(res))]

        # ![36_下发文件]
        elif args.createfile != 'createfile':
            cus_excel_op.load_excel('zabbix_api.xlsx', 36)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]
            # 根据需要生成配置文件
            with open('senddir/ip/hosts', 'w') as s_hosts:
                for n_1 in range(len(column_1_list)):
                    s_hosts.write(cus_excel_op.get_cell_value(n_1 + 2, 6) +
                                  ' ' + cus_excel_op.get_cell_value(n_1 + 2, 11) +
                                  ' ' + cus_excel_op.get_cell_value(n_1 + 2, 12) + '\n')
            s_hosts.close()
            with open('senddir/ip/ip.txt', 'w') as s_hosts:
                for n_1 in range(len(column_1_list)):
                    s_hosts.write(cus_excel_op.get_cell_value(n_1 + 2, 6) + " " + cus_excel_op.get_cell_value(n_1 + 2, 3) + '\n')
            s_hosts.close()
            with open('senddir/ip/mysql.txt', 'w') as s_hosts:
                s_hosts.write(cus_excel_op.get_cell_value(11, 6) + '\n')
            s_hosts.close()
            with open('senddir/ip/zookeeper.txt', 'w') as s_hosts:
                s_hosts.write(cus_excel_op.get_cell_value(5, 11) + ' ')
                s_hosts.write(cus_excel_op.get_cell_value(6, 11) + ' ')
                s_hosts.write(cus_excel_op.get_cell_value(7, 11) + ' \n')
            s_hosts.close()
            with open('senddir/ip/kafka.txt', 'w') as s_hosts:
                s_hosts.write(cus_excel_op.get_cell_value(5, 11) + ' ')
                s_hosts.write(cus_excel_op.get_cell_value(6, 11) + ' ')
                s_hosts.write(cus_excel_op.get_cell_value(7, 11) + ' \n')
            s_hosts.close()
            with open('senddir/ip/elasticsearch.txt', 'w') as s_hosts:
                s_hosts.write(cus_excel_op.get_cell_value(8, 6) + ' ')
                s_hosts.write(cus_excel_op.get_cell_value(9, 6) + ' ')
                s_hosts.write(cus_excel_op.get_cell_value(10, 6) + ' \n')
                s_hosts.write(cus_excel_op.get_cell_value(8, 11) + ' ')
                s_hosts.write(cus_excel_op.get_cell_value(9, 11) + ' ')
                s_hosts.write(cus_excel_op.get_cell_value(10, 11) + ' \n')
            s_hosts.close()
            with open('senddir/ip/kibana.txt', 'w') as s_hosts:
                s_hosts.write(cus_excel_op.get_cell_value(8, 6) + ' ')
                s_hosts.write(cus_excel_op.get_cell_value(9, 6) + ' ')
                s_hosts.write(cus_excel_op.get_cell_value(10, 6) + ' \n')
                s_hosts.write(cus_excel_op.get_cell_value(8, 11) + ' ')
                s_hosts.write(cus_excel_op.get_cell_value(9, 11) + ' ')
                s_hosts.write(cus_excel_op.get_cell_value(10, 11) + ' \n')
            s_hosts.close()
            with open('senddir/ip/nacos.txt', 'w') as s_hosts:
                s_hosts.write('mysql ' + cus_excel_op.get_cell_value(11, 6) + ' \n')
                s_hosts.write('redis ' + cus_excel_op.get_cell_value(11, 6) + ' \n')
                s_hosts.write('kafka ' + cus_excel_op.get_cell_value(5, 6) + ':9092,')
                s_hosts.write(cus_excel_op.get_cell_value(6, 6) + ':9092,')
                s_hosts.write(cus_excel_op.get_cell_value(7, 6) + ':9092 \n')
                s_hosts.write('elasticsearch ' + cus_excel_op.get_cell_value(8, 6) + ':9200,')
                s_hosts.write(cus_excel_op.get_cell_value(9, 6) + ':9200,')
                s_hosts.write(cus_excel_op.get_cell_value(10, 6) + ':9200 \n')
            s_hosts.close()
            with open('senddir/ip/spark.txt', 'w') as s_hosts:
                s_hosts.write(cus_excel_op.get_cell_value(3, 11) + ' \n')
                s_hosts.write(cus_excel_op.get_cell_value(4, 11) + ' \n')
                s_hosts.write(cus_excel_op.get_cell_value(5, 11) + ' \n')
            s_hosts.close()
            # 根据需要生成配置文件
            print('配置文件生成完毕')

        # ![36_下发文件]
        elif args.senddir != 'senddir':
            cus_excel_op.load_excel('sshcomm.xlsx', 1)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            column_1_list = cus_excel_op.get_column_values(1)
            cus_excel_op.create_new_workbook()
            cus_excel_op.create_sheet("上传结果")
            title_name = ['IP', '是否成功', '过程']
            [cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
            del column_1_list[0]
            for n_1 in range(len(column_1_list)):
                total_num = len(column_1_list)
                cur_num = n_1 + 1
                ssh_ip = cus_excel_op.get_cell_value(n_1 + 2, 1)
                port = int(cus_excel_op.get_cell_value(n_1 + 2, 4))
                pwd = cus_excel_op.get_cell_value(n_1 + 2, 3)
                # print(ssh_ip, port, pwd)
                cus_excel_op.set_cell_value(cur_num + 1, 1, ssh_ip)
                try:
                    m = CusMyThreadSendDir(cur_num, total_num, ssh_ip, port, pwd, cus_excel_op)
                    m.start()
                except Exception as e:
                    pass

        elif args.sendcfg != 'sendcfg':
            cus_excel_op.load_excel('zabbix_api.xlsx', 36)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            column_1_list = cus_excel_op.get_column_values(1)
            cus_excel_op.create_new_workbook()
            cus_excel_op.create_sheet('安装结果')
            title_name = ['IP', '是否成功']
            del column_1_list[0]
            for n_1 in range(len(column_1_list)):
                total_num = len(column_1_list)
                cur_num = n_1 + 1
                ssh_ip = cus_excel_op.get_cell_value(n_1 + 2, 1)
                port = int(cus_excel_op.get_cell_value(n_1 + 2, 2))
                pwd = cus_excel_op.get_cell_value(n_1 + 2, 3)
                zabbix_server_ip = cus_excel_op.get_cell_value(n_1 + 2, 4)
                # print(ssh_ip, port, pwd)
                try:
                    m = CusMyThreadCfgZabbixAgent(cur_num, total_num, ssh_ip, port, pwd, zabbix_server_ip)
                    m.start()
                    print(u'(进度: -> \033[;34m%s\033[0m/\033[;34m%s\033[0m \033[;34m%s\033[0m)' % (
                    total_num, cur_num, ssh_ip), end='')
                except Exception as e:
                    print(u'(进度: -> \033[;34m%s\033[0m/\033[;34m%s\033[0m \033[;34m%s\033[0m \033[;31m%s\033[0m)' % (
                    total_num, cur_num, ssh_ip, e), end='')
                    sys.exit(1)
            cus_excel_op.save_workbook(first_active_sheet_name + 'conf' + '.xlsx')

        elif args.sendsj != 'sendsj':
            cus_excel_op.load_excel('zabbix_api.xlsx', 36)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]
            for n_1 in range(len(column_1_list)):
                total_num = len(column_1_list)
                cur_num = n_1 + 1
                s_dic = {'ssh_ip': "", 'port': "", 'pwd': "", 's_eth': "", 's_ip': "", 's_newmask': "", 's_gateway': "",
                         's_dns1': "", 's_dns2': "", 's_host': "", 's_app': ""}
                s_dic['ssh_ip'] = cus_excel_op.get_cell_value(n_1 + 2, 1)
                s_dic['port'] = int(cus_excel_op.get_cell_value(n_1 + 2, 2))
                s_dic['pwd'] = cus_excel_op.get_cell_value(n_1 + 2, 3)
                s_dic['s_eth'] = cus_excel_op.get_cell_value(n_1 + 2, 5)
                s_dic['s_ip'] = cus_excel_op.get_cell_value(n_1 + 2, 6)
                s_dic['s_newmask'] = cus_excel_op.get_cell_value(n_1 + 2, 7)
                s_dic['s_gateway'] = cus_excel_op.get_cell_value(n_1 + 2, 8)
                s_dic['s_dns1'] = cus_excel_op.get_cell_value(n_1 + 2, 9)
                s_dic['s_dns2'] = cus_excel_op.get_cell_value(n_1 + 2, 10)
                s_dic['s_host'] = cus_excel_op.get_cell_value(n_1 + 2, 11)
                s_dic['s_app'] = cus_excel_op.get_cell_value(n_1 + 2, 12)
                # print(ssh_ip, port, pwd)
                try:
                    m = CusMyThreadCfgSj(cur_num, total_num, s_dic)
                    m.start()
                except Exception as e:
                    print(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], e))
                    sys.exit(1)
        # ![]
        elif args.get_hostgroup_item != 'get_hostgroup_item':
            cus_excel_op.load_excel('zabbix_api.xlsx', 48)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()

            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]
            column_2_list = []
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.get_cell_value(i + 2, 2))
            # executor = ThreadPoolExecutor(GV_CPU_COUNT)
            cus_excel_op.create_new_workbook()
            for lv_int_05 in range(len(column_2_list)):
                lv_result = cus_zabbix_api.def_get_group_item(column_1_list[lv_int_05], column_2_list[lv_int_05])
                lv_list_itemid = []
                lv_list_hostid = []
                lv_list_name = []
                lv_list_key_ = []
                lv_list_lastclock = []
                lv_list_lastvalue = []
                lv_list_prevvalue = []
                if lv_result['tag'] is True:
                    for lv_int01 in range(len(lv_result['result'])):
                        lv_list_itemid.append(lv_result['result'][lv_int01]['itemid'])
                        lv_list_hostid.append(lv_result['result'][lv_int01]['hostid'])
                        lv_list_name.append(lv_result['result'][lv_int01]['name'])
                        lv_list_key_.append(lv_result['result'][lv_int01]['key_'])
                        lv_list_lastclock.append(cus_zabbix_api.def_timeCovertIntToYMD(int(lv_result['result'][lv_int01]['lastclock'])))
                        try:
                            lv_list_lastvalue.append(int(lv_result['result'][lv_int01]['lastvalue']))
                            lv_list_prevvalue.append(int(lv_result['result'][lv_int01]['prevvalue']))
                        except:
                            lv_list_lastvalue.append(lv_result['result'][lv_int01]['lastvalue'])
                            lv_list_prevvalue.append(lv_result['result'][lv_int01]['prevvalue'])
                else:
                    lv_list_itemid.append('')
                    lv_list_hostid.append('')
                    lv_list_name.append('')
                    lv_list_key_.append('')
                    lv_list_lastclock.append('')
                    lv_list_lastvalue.append('')
                    lv_list_prevvalue.append('')
                    # 等待所有线程完成
                # executor.shutdown(wait=True)
                lv_int_11 = 0
                export_sheet_name = cus_local_method.def_batch_replace(column_2_list[lv_int_05], {"[": "", "]": ""})[:31]
                cus_excel_op.create_sheet(export_sheet_name)
                if "dirMTime" in export_sheet_name:
                    title_name = ['脚本位置', '格式化IP', '任务名称', '机房位置', '所属业务', '所属应用', '数据来源', '监控目录', '已持续多久未收到数据', '对比上一次历史数据的差值', '时间', 'id']
                elif "dirFileNum" in export_sheet_name:
                    title_name = ['脚本位置', '格式化IP', '任务名称', '机房位置', '所属业务', '所属应用', '数据来源', '监控目录', '目录积压文件个数', '对比上一次历史数据的差值', '时间', 'id']
                elif "vfs.fs.dependent.size" in export_sheet_name:
                    title_name = ['脚本位置', '盘符', '归属', '来源', '协议', '-', '磁盘使用率', '对比上一次历史数据的差值', '时间','', '', 'id']
                else:
                    title_name = ['脚本位置', 'IP', '归属', '来源', '协议', '目录', '队列积压情况', '队列消费情况', '时间','', '', 'id']

                [cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
                for lv_int02 in range(len(lv_list_itemid)):
                    try:
                        if lv_list_itemid == [""]:
                            continue
                        cu_host = cus_zabbix_api.def_get_host_ip(lv_list_hostid[lv_int02])['result'][0]['interfaces'][0]['ip']
                        cus_excel_op.set_cell_value(lv_int_11 + 2, 12, lv_int_11 + 1)
                        cus_excel_op.set_cell_value(lv_int_11 + 2, 1, cu_host)
                        # 定义需要检查的字符串列表
                        check_strings = ["dirMTime", "dirFileNum"]

                        # 使用 any() 函数和生成器表达式进行判断
                        if any(check_str in export_sheet_name for check_str in check_strings):
                            if len(lv_list_name[lv_int02].split('____')[0].split('__')) == 6:
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 2, lv_list_name[lv_int02].split('____')[0].split('__')[0])
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 3, lv_list_name[lv_int02].split('____')[0].split('__')[1])
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 4, lv_list_name[lv_int02].split('____')[0].split('__')[2])
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 5, lv_list_name[lv_int02].split('____')[0].split('__')[3])
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 6, lv_list_name[lv_int02].split('____')[0].split('__')[4])
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 7, lv_list_name[lv_int02].split('____')[0].split('__')[5])
                                dic_replace = {"__": "/", "通道队列深度": "", "目录挂载状态": "", "通道目录修改时间": "", "/sh进程存在状态": ".sh"}
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 8, '/' + cus_local_method.def_batch_replace(lv_list_name[lv_int02].split('____')[1], dic_replace))
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 9, int(lv_list_lastvalue[lv_int02]))
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 10, int(lv_list_lastvalue[lv_int02] - lv_list_prevvalue[lv_int02]))
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 11, lv_list_lastclock[lv_int02])
                        elif len(lv_list_name[lv_int02].split('____')) > 1:
                            cus_excel_op.set_cell_value(lv_int_11 + 2, 2, lv_list_name[lv_int02].split('____')[0].split('__')[0])
                            cus_excel_op.set_cell_value(lv_int_11 + 2, 3, lv_list_name[lv_int02].split('____')[0].split('__')[1])
                            cus_excel_op.set_cell_value(lv_int_11 + 2, 4, lv_list_name[lv_int02].split('____')[0].split('__')[2])
                            cus_excel_op.set_cell_value(lv_int_11 + 2, 5, lv_list_name[lv_int02].split('____')[0].split('__')[3])
                            dic_replace = {"__": "/", "通道队列深度": "", "目录挂载状态": "", "通道目录修改时间": "", "/sh进程存在状态": ".sh"}
                            cus_excel_op.set_cell_value(lv_int_11 + 2, 6, '/' + cus_local_method.def_batch_replace(lv_list_name[lv_int02].split('____')[1], dic_replace))
                            cus_excel_op.set_cell_value(lv_int_11 + 2, 7, int(lv_list_lastvalue[lv_int02]))
                            cus_excel_op.set_cell_value(lv_int_11 + 2, 8, int(lv_list_lastvalue[lv_int02] - lv_list_prevvalue[lv_int02]))
                            cus_excel_op.set_cell_value(lv_int_11 + 2, 9, lv_list_lastclock[lv_int02])
                        else:
                            if(len((lv_list_name[lv_int02].split('__')))) > 2:
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 2, lv_list_name[lv_int02].split('__')[0])
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 3, lv_list_name[lv_int02].split('__')[1])
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 4, lv_list_name[lv_int02].split('__')[2])
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 5, lv_list_name[lv_int02].split('__')[3])
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 6, lv_list_name[lv_int02].split('__')[4])
                            else:
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 2, lv_list_name[lv_int02].split('__')[0])
                                cu_name = cus_zabbix_api.def_get_host_name(lv_list_hostid[lv_int02])['result'][0]['name']
                                if (len((cu_name.split('_')))) > 2:
                                    cus_excel_op.set_cell_value(lv_int_11 + 2, 1, cu_host)
                                    # cus_excel_op.set_cell_value(lv_int_11 + 2, 2, cu_name.split('_')[0])
                                    cus_excel_op.set_cell_value(lv_int_11 + 2, 3, cu_name.split('_')[1])
                                    cus_excel_op.set_cell_value(lv_int_11 + 2, 4, cu_name.split('_')[2])
                                    cus_excel_op.set_cell_value(lv_int_11 + 2, 5, cu_name.split('_')[3])
                                else:
                                    cus_excel_op.set_cell_value(lv_int_11 + 2, 4, cu_name)
                            if isinstance(lv_list_lastvalue[lv_int02], str) and "|" in lv_list_lastvalue[lv_int02]:
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 7, lv_list_lastvalue[lv_int02].split("|")[4])
                            else:
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 7, lv_list_lastvalue[lv_int02])
                            cus_excel_op.set_cell_value(lv_int_11 + 2, 8, lv_list_prevvalue[lv_int02])
                            cus_excel_op.set_cell_value(lv_int_11 + 2, 9, lv_list_lastclock[lv_int02])
                    except ValueError:
                        list_errorValue = lv_list_lastvalue[lv_int02].replace('%', '').split("|")
                        if len(list_errorValue) > 1:
                            errorValue = lv_list_lastvalue[lv_int02].replace('%', '').split("|")[4]
                        else:
                            errorValue = lv_list_lastvalue[lv_int02].replace('%', '').split("|")[0]
                        cus_excel_op.set_cell_value(lv_int_11 + 2, 6, lv_list_lastvalue[lv_int02])
                        if isinstance(lv_list_lastvalue[lv_int02], str) and "|" in lv_list_lastvalue[lv_int02]:
                            if errorValue != "异常":
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 7, int(errorValue))
                            else:
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 7, errorValue)
                        else:
                            cus_excel_op.set_cell_value(lv_int_11 + 2, 7, lv_list_lastvalue[lv_int02])
                        cus_excel_op.set_cell_value(lv_int_11 + 2, 9, lv_list_lastclock[lv_int02])
                    except:
                        cu_host = cus_zabbix_api.def_get_host_ip(lv_list_hostid[lv_int02])['result'][0]['hostid']
                        cu_name = cus_zabbix_api.def_get_host_name(lv_list_hostid[lv_int02])['result'][0]['name']
                        cus_excel_op.set_cell_value(lv_int_11 + 2, 1, cu_host)
                        cus_excel_op.set_cell_value(lv_int_11 + 2, 2, cu_name.split('_')[0])
                        cus_excel_op.set_cell_value(lv_int_11 + 2, 3, cu_name.split('_')[1])
                        cus_excel_op.set_cell_value(lv_int_11 + 2, 4, cu_name.split('_')[2])
                        cus_excel_op.set_cell_value(lv_int_11 + 2, 5, cu_name.split('_')[3])
                        errorValue = lv_list_lastvalue[lv_int02].replace('%', '').split("|")[4]
                        if isinstance(lv_list_lastvalue[lv_int02], str) and "|" in lv_list_lastvalue[lv_int02]:
                            if errorValue != "异常":
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 7, int(errorValue))
                            else:
                                cus_excel_op.set_cell_value(lv_int_11 + 2, 7, errorValue)
                        else:
                            cus_excel_op.set_cell_value(lv_int_11 + 2, 7, lv_list_lastvalue[lv_int02])
                        cus_excel_op.set_cell_value(lv_int_11 + 2, 8, lv_list_prevvalue[lv_int02])
                        cus_excel_op.set_cell_value(lv_int_11 + 2, 9, lv_list_lastclock[lv_int02])
                        pass
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 按主机组导出主机: \033[;32m%s\033[0m 成功'
                          % (len(lv_list_itemid), lv_int_11 + 1, lv_list_name[lv_int02]))
                    lv_int_11 = lv_int_11 + 1
            if args.output:
                cus_excel_op.save_workbook(args.output + first_active_sheet_name + '.xlsx')
                cus_excel_op.load_excel(args.output + '48_按主机组批量导出监控项.xlsx')
            else:
                cus_excel_op.save_workbook(first_active_sheet_name + '.xlsx')
                cus_excel_op.load_excel('48_按主机组批量导出监控项.xlsx')
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            for lv_int_06 in range(len(column_2_list)):
                export_sheet_name_1 = cus_local_method.def_batch_replace(column_2_list[lv_int_06], {"[": "", "]": ""})[:31]
                if "dirMTime" in export_sheet_name_1:
                    cus_excel_op.activate_sheet("dirMTime")
                    cus_excel_op.process_time_column("I")
                    cus_excel_op.activate_sheet("dirMTime")
                    cus_excel_op.process_time_column("J", format_only=True)
                elif "linuxDf" in export_sheet_name_1:
                    cus_excel_op.activate_sheet("linuxDf")
                    cus_excel_op.process_time_column("G", sort_only=True)
                elif "dirFileNum" in export_sheet_name_1:
                    cus_excel_op.activate_sheet("dirFileNum")
                    cus_excel_op.process_time_column("G", sort_only=True)
                elif "mountstatus" in export_sheet_name_1:
                    cus_excel_op.activate_sheet("mountstatus")
                    cus_excel_op.process_time_column("G", sort_only=True)
            if args.output:
                cus_excel_op.save_workbook(args.output + '48_按主机组批量导出监控项.xlsx')
            else:
                cus_excel_op.save_workbook('48_按主机组批量导出监控项.xlsx')

        elif args.get_host_key_item != 'get_host_key_item':
            cus_excel_op.load_excel('zabbix_api.xlsx', 50)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]

            lv_list_itemid = []
            lv_list_hostid = []
            lv_list_host = []
            lv_list_name = []
            lv_list_key_ = []
            lv_list_lastclock = []
            lv_list_lastvalue = []
            lv_list_prevvalue = []
            lv_list_dir = []
            lv_result = None
            executor = ThreadPoolExecutor(GV_CPU_COUNT)
            for lv_result in executor.map(cus_zabbix_api.def_get_host_key_item, column_1_list):
                if lv_result['tag'] is True:
                    for lv_int01 in range(len(lv_result['result'])):
                        lv_list_itemid.append(lv_result['result'][lv_int01]['itemid'])
                        lv_list_hostid.append(lv_result['result'][lv_int01]['hostid'])
                        lv_list_dir.append(lv_result['result'][lv_int01]['name'])
                        lv_list_name.append(lv_result['result'][lv_int01]['hosts'][0]['name'])
                        lv_list_host.append(lv_result['result'][lv_int01]['hosts'][0]['host'])
                        lv_list_key_.append(lv_result['result'][lv_int01]['key_'])
                        lv_list_lastclock.append(cus_zabbix_api.def_timeCovertIntToYMD(int(lv_result['result'][lv_int01]['lastclock'])))
                        try:
                            lv_list_lastvalue.append(float(lv_result['result'][lv_int01]['lastvalue']))
                            lv_list_prevvalue.append(float(lv_result['result'][lv_int01]['prevvalue']))
                        except ValueError:
                            lv_list_lastvalue.append(lv_result['result'][lv_int01]['lastvalue'])
                            lv_list_prevvalue.append(lv_result['result'][lv_int01]['prevvalue'])

                    else:
                        lv_list_itemid.append('')
                        lv_list_hostid.append('')
                        lv_list_name.append('')
                        lv_list_key_.append('')
                        lv_list_lastclock.append('')
                        lv_list_lastvalue.append('')
                        lv_list_prevvalue.append('')
                # 等待所有线程完成
            executor.shutdown(wait=True)
            cus_excel_op.create_new_workbook()
            for lv_int_03 in range(len(column_1_list)):
                cus_excel_op.create_sheet('目录积压情况')
                title_name = ['IP', '归属', '协议', '用途', '磁盘', '使用率%', '增减%', '时间']
                [cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
                rownum = 1
                for lv_int02 in range(len(lv_list_itemid)):
                    try:
                        if lv_list_name[lv_int02].find('_') == -1 or lv_list_dir[lv_int02].find('boot') == 1:
                            continue
                        cus_excel_op.set_cell_value(rownum + 1, 1, f'{lv_list_name[lv_int02].split("__")[0].split("_")[0]}')
                        cus_excel_op.set_cell_value(rownum + 1, 2, lv_list_name[lv_int02].split('__')[0].split('_')[1])
                        cus_excel_op.set_cell_value(rownum + 1, 3, lv_list_name[lv_int02].split('__')[0].split('_')[2])
                        cus_excel_op.set_cell_value(rownum + 1, 4, lv_list_name[lv_int02].split('__')[0].split('_')[3])
                        cus_excel_op.set_cell_value(rownum + 1, 5, lv_list_dir[lv_int02])
                        cus_excel_op.set_cell_value(rownum + 1, 6, float(f'{lv_list_lastvalue[lv_int02]:.2f}'))
                        cus_excel_op.set_cell_value(rownum + 1, 7, float(f'{lv_list_lastvalue[lv_int02] - lv_list_prevvalue[lv_int02]:.2f}'))
                        cus_excel_op.set_cell_value(rownum + 1, 8, lv_list_lastclock[lv_int02])
                    except:
                        cus_excel_op.set_cell_value(rownum + 1, 6, float(f'{lv_list_lastvalue[lv_int02]:.2f}'))
                        cus_excel_op.set_cell_value(rownum + 1, 7, float(f'{lv_list_lastvalue[lv_int02] - lv_list_prevvalue[lv_int02]:.2f}'))
                        cus_excel_op.set_cell_value(rownum + 1, 8, lv_list_lastclock[lv_int02])
                        pass
                    rownum = rownum + 1
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 按主机组导出主机: \033[;32m%s\033[0m 成功'
                          % (len(lv_list_itemid), lv_int02 + 1, lv_list_name[lv_int02]))
            cus_excel_op.save_workbook(first_active_sheet_name + '.xlsx')

        elif args.get_host_key_systemname != 'get_host_key_systemname':
            cus_excel_op.load_excel('zabbix_api.xlsx', 50)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]

            lv_list_itemid = []
            lv_list_hostid = []
            lv_list_host = []
            lv_list_name = []
            lv_list_key_ = []
            lv_list_lastclock = []
            lv_list_lastvalue = []
            lv_list_prevvalue = []
            lv_list_dir = []
            lv_result = None
            executor = ThreadPoolExecutor(GV_CPU_COUNT)
            for lv_result in executor.map(cus_zabbix_api.def_get_host_key_item, column_1_list):
                if lv_result['tag'] is True:
                    for lv_int01 in range(len(lv_result['result'])):
                        if len(lv_result['result'][lv_int01]['interfaces']) == 0:
                            continue
                        lv_list_itemid.append(lv_result['result'][lv_int01]['itemid'])
                        lv_list_hostid.append(lv_result['result'][lv_int01]['hostid'])
                        lv_list_dir.append(lv_result['result'][lv_int01]['name'])
                        lv_list_name.append(lv_result['result'][lv_int01]['hosts'][0]['name'])
                        lv_list_host.append(lv_result['result'][lv_int01]['hosts'][0]['host'])
                        lv_list_key_.append(lv_result['result'][lv_int01]['key_'])
                        lv_list_lastclock.append(cus_zabbix_api.def_timeCovertIntToYMD(int(lv_result['result'][lv_int01]['lastclock'])))
                        lv_list_lastvalue.append(lv_result['result'][lv_int01]['lastvalue'])
                        lv_list_prevvalue.append(lv_result['result'][lv_int01]['prevvalue'])

                else:
                    lv_list_itemid.append('')
                    lv_list_hostid.append('')
                    lv_list_host.append('')
                    lv_list_name.append('')
                    lv_list_key_.append('')
                    lv_list_lastclock.append('')
                    lv_list_lastvalue.append('')
                    lv_list_prevvalue.append('')
                # 等待所有线程完成
            executor.shutdown(wait=True)
            cus_excel_op.create_new_workbook()
            for lv_int_03 in range(len(column_1_list)):
                cus_excel_op.create_sheet('系统名称')
                title_name = ['主机名称','可见名称', '监控项名称', '最新数据', '获取时间']
                [cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
                for lv_int02 in range(len(lv_list_itemid)):
                    cus_excel_op.set_cell_value(lv_int02 + 2, 1, f'{lv_list_host[lv_int02]}')
                    cus_excel_op.set_cell_value(lv_int02 + 2, 2, f'{lv_list_name[lv_int02]}')
                    cus_excel_op.set_cell_value(lv_int02 + 2, 3, lv_list_dir[lv_int02])
                    cus_excel_op.set_cell_value(lv_int02 + 2, 4, f'{lv_list_lastvalue[lv_int02]}')
                    cus_excel_op.set_cell_value(lv_int02 + 2, 5, lv_list_lastclock[lv_int02])
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 按监控项导出主机: \033[;32m%s\033[0m 成功'
                          % (len(lv_list_itemid), lv_int02 + 1, lv_list_name[lv_int02]))
            cus_excel_op.save_workbook(first_active_sheet_name + '.xlsx')
