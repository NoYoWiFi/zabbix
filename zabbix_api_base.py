#!/usr/bin/python3
# coding:utf-8

import argparse
from collections import defaultdict
import base64
import datetime
from datetime import datetime
from lxml import etree
import hashlib
import hmac
import inspect
import json
import openpyxl
import os
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from functools import partial
import re
import sys
import time
from time import mktime
import requests
from requests.adapters import HTTPAdapter
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import win32clipboard as w
import win32api
import win32con
import win32gui
import sys
import random
import pyautogui
from pprint import pprint
from pathlib import Path
import zabbix_api
from zabbix_api import CusZabbixApi
from zabbix_api import CusExcelOp
from zabbix_api import CusPoEdit
from zabbix_api import Cusxliff
from zabbix_api import GV_CPU_COUNT
from zabbix_api import GV_FIREFOX_TIMEOUT
from zabbix_api import GV_FIREFOX_WAITTIMEOUT
from zabbix_api import CusLanguageTransDeepSeek
from zabbix_api import CusLanguageTransDeepSeekQianWen
from zabbix_api import CusLanguageTransDeepSeekDify
from zabbix_api import CusTermProcessor
from zabbix_api import CusTranslationProcessor
from zabbix_api import CusLocalMethod
from zabbix_api import PasswordGenerator
from zabbix_api import PyPIMirrorSync

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='zabbix  api;PyPI镜像同步工具', usage='%(prog)s [options]')
    # ![01_创建主机组]
    parser.add_argument('-create_proxygroup', nargs='?', metavar='无参数', dest='create_proxygroup', default='create_proxygroup',
                        help=u"创建Proxy组")
    parser.add_argument('-delete_proxygroup', nargs='?', metavar='无参数', dest='delete_proxygroup', default='delete_proxygroup',
                        help=u"删除Proxy组")
    parser.add_argument('-create_proxy', nargs='?', metavar='无参数', dest='create_proxy', default='create_proxy',
                        help=u"创建Proxy")
    parser.add_argument('-delete_proxy', nargs='?', metavar='无参数', dest='delete_proxy', default='delete_proxy',
                        help=u"删除Proxy")
    parser.add_argument('-create_hostgroup', nargs='?', metavar='无参数', dest='create_hostgroup', default='create_hostgroup',
                        help=u"创建主机组")
    parser.add_argument('-delete_hostgroup', nargs='?', metavar='无参数', dest='delete_hostgroup', default='delete_hostgroup',
                        help=u"删除主机组")
    # 在参数解析部分添加新的参数
    parser.add_argument('-create_templategroup', nargs='?', metavar='无参数', dest='create_templategroup', default='create_templategroup',
                        help=u"创建模板组")
    parser.add_argument('-delete_templategroup', nargs='?', metavar='无参数', dest='delete_templategroup', default='delete_templategroup',
                        help=u"删除模板组")
    # ![02_创建模板]
    parser.add_argument('-create_template', nargs='?', metavar='无参数', dest='create_template', default='create_template',
                        help=u"创建模板")
    parser.add_argument('-delete_template', nargs='?', metavar='无参数', dest='delete_template', default='delete_template',
                        help=u"删除模板")
    parser.add_argument('-massadd_template_groups', nargs='?', metavar='无参数', dest='massadd_template_groups', default='massadd_template_groups',
                        help=u"模板添加主机组")
    parser.add_argument('-massremove_template_groups', nargs='?', metavar='无参数', dest='massremove_template_groups', default='massremove_template_groups',
                        help=u"模板删除主机组")
    # ![03_模板添加用户宏]
    parser.add_argument('-massadd_template_macros', nargs='?', metavar='无参数', dest='massadd_template_macros', default='massadd_template_macros',
                        help=u"模板添加用户宏")
    parser.add_argument('-massremove_template_macros', nargs='?', metavar='无参数', dest='massremove_template_macros', default='massremove_template_macros',
                        help=u"模板删除用户宏")
    # ![04_模板关联模板]
    parser.add_argument('-massadd_template_templates_link', nargs='?', metavar='无参数', dest='massadd_template_templates_link', default='massadd_template_templates_link',
                        help=u"模板关联模板")
    parser.add_argument('-massremove_templateids_clear', nargs='?', metavar='无参数', dest='massremove_templateids_clear', default='massremove_templateids_clear',
                        help=u"模板脱离模板清理监控项")
    parser.add_argument('-massremove_templateids_link', nargs='?', metavar='无参数', dest='massremove_templateids_link', default='massremove_templateids_link',
                        help=u"模板脱离模板保留监控项")
    # ![05_模板更新标签]
    parser.add_argument('-update_tags', nargs='?', metavar='无参数', dest='update_tags', default='update_tags',
                        help=u"模板更新替换所有标签")
    parser.add_argument('-delete_tags', nargs='?', metavar='无参数', dest='delete_tags', default='delete_tags',
                        help=u"模板删除标签")
    # ![06_模板创建监控项]
    parser.add_argument('-create_template_item', nargs='?', metavar='无参数', dest='create_template_item', default='create_template_item',
                        help=u"模板创建监控项")
    parser.add_argument('-delete_template_item', nargs='?', metavar='无参数', dest='delete_template_item', default='delete_template_item',
                        help=u"模板删除监控项")
    # ![07_模板更新监控项标签]
    parser.add_argument('-update_template_item_tags', nargs='?', metavar='无参数', dest='update_template_item_tags', default='update_template_item_tags',
                        help=u"模板更新监控项标签")
    parser.add_argument('-delete_template_item_tags', nargs='?', metavar='无参数', dest='delete_template_item_tags', default='delete_template_item_tags',
                        help=u"模板删除监控项标签")
    # ![08_模板创建触发器]
    parser.add_argument('-create_template_trigger', nargs='?', metavar='无参数', dest='create_template_trigger', default='create_template_trigger',
                        help=u"模板创建触发器")
    parser.add_argument('-delete_template_trigger', nargs='?', metavar='无参数', dest='delete_template_trigger', default='delete_template_trigger',
                        help=u"模板删除触发器")
    # ![09_模板更新标签]
    parser.add_argument('-update_template_trigger_tags', nargs='?', metavar='无参数', dest='update_template_trigger_tags', default='update_template_trigger_tags',
                        help=u"模板更新触发器标签")
    parser.add_argument('-delete_template_trigger_tags', nargs='?', metavar='无参数', dest='delete_template_trigger_tags', default='delete_template_trigger_tags',
                        help=u"模板删除触发器标签")
    # ![10_创建主机]
    parser.add_argument('-create_host', nargs='?', metavar='无参数', dest='create_host', default='create_host',
                        help=u"创建主机")
    parser.add_argument('-delete_host', nargs='?', metavar='无参数', dest='delete_host', default='delete_host',
                        help=u"删除主机")
    # ![11_主机创建接口]
    parser.add_argument('-massadd_host_interface', nargs='?', metavar='无参数', dest='massadd_host_interface', default='massadd_host_interface',
                        help=u"主机创建接口")
    parser.add_argument('-massremove_host_interface', nargs='?', metavar='无参数', dest='massremove_host_interface', default='massremove_host_interface',
                        help=u"主机删除接口")
    # ![12_主机关联模板]
    parser.add_argument('-massadd_host_template', nargs='?', metavar='无参数', dest='massadd_host_template', default='massadd_host_template',
                        help=u"主机关联模板")
    parser.add_argument('-massremove_host_templateids', nargs='?', metavar='无参数', dest='massremove_host_templateids', default='massremove_host_templateids',
                        help=u"主机脱离模板保留监控项")
    parser.add_argument('-massremove_host_templateids_clear', nargs='?', metavar='无参数', dest='massremove_host_templateids_clear', default='massremove_host_templateids_clear',
                        help=u"主机脱离模板清理监控项")
    # ![13_主机关联主机组]
    parser.add_argument('-massadd_host_groups', nargs='?', metavar='无参数', dest='massadd_host_groups', default='massadd_host_groups',
                        help=u"主机关联主机组")
    parser.add_argument('-massremove_host_group', nargs='?', metavar='无参数', dest='massremove_host_group', default='massremove_host_group',
                        help=u"主机脱离主机组")
    # ![31_自动发现规则]
    parser.add_argument('-create_discoveryrule', nargs='?', metavar='无参数', dest='create_discoveryrule', default='create_discoveryrule',
                        help=u"创建发现规则")
    parser.add_argument('-delete_discoveryrule', nargs='?', metavar='无参数', dest='delete_discoveryrule', default='delete_discoveryrule',
                        help=u"删除发现规则")
    # ![32_模板创建监控项原型]
    parser.add_argument('-create_itemprototype', nargs='?', metavar='无参数', dest='create_itemprototype', default='create_itemprototype',
                        help=u"模板创建发现规则监控项")
    parser.add_argument('-delete_itemprototype', nargs='?', metavar='无参数', dest='delete_itemprototype', default='delete_itemprototype',
                        help=u"模板删除发现规则监控项")
    # ![33_模板创建发现规则触发器]
    parser.add_argument('-create_template_triggerprototype', nargs='?', metavar='无参数', dest='create_template_triggerprototype', default='create_template_triggerprototype',
                        help=u"模板创建发现规则触发器")
    parser.add_argument('-delete_template_triggerprototype', nargs='?', metavar='无参数', dest='delete_template_triggerprototype', default='delete_template_triggerprototype',
                        help=u"模板删除发现规则触发器")
    # ![导出所有模板]
    parser.add_argument('-export_configuration', nargs='?', metavar='无参数', dest='export_configuration', default='export_configuration',
                        help=u"导出所有模板")
    parser.add_argument('-import_configuration', nargs='?', metavar='无参数', dest='import_configuration', default='import_configuration',
                        help=u"入所有模板")
    parser.add_argument('-poedit_zabbix_ui_to_excel', nargs='?', metavar='无参数', dest='poedit_zabbix_ui_to_excel', default='poedit_zabbix_ui_to_excel',
                        help=u"从poedit导出zabbix ui 6.0翻译文本到excel")
    parser.add_argument('--v')
    parser.add_argument('-excel_zabbix_ui_to_poedit', nargs='?', metavar='无参数', dest='excel_zabbix_ui_to_poedit', default='excel_zabbix_ui_to_poedit',
                        help=u"从excel导出zabbix ui 6.0翻译文本到poedit")
    parser.add_argument('-xliff_zabbix_document_to_excel', nargs='?', metavar='无参数', dest='xliff_zabbix_document_to_excel', default='xliff_zabbix_document_to_excel',
                        help=u"从xliff导出zabbix document 7.0翻译文本到excel")
    parser.add_argument('-excel_zabbix_document_to_xliff', nargs='?', metavar='无参数', dest='excel_zabbix_document_to_xliff', default='excel_zabbix_document_to_xliff',
                        help=u"从excel导出zabbix document 7.0翻译文本到xliff")
    parser.add_argument('-excel_zabbix_deepseek_to_excel', nargs='?', metavar='无参数', dest='excel_zabbix_deepseek_to_excel', default='excel_zabbix_deepseek_to_excel',
                        help=u"使用deepseek翻译文本到excel")
    parser.add_argument('-excel_zabbix_deepseek_to_excel_dify', nargs='?', metavar='无参数', dest='excel_zabbix_deepseek_to_excel_dify', default='excel_zabbix_deepseek_to_excel_dify',
                        help=u"使用dify翻译文本到excel")
    parser.add_argument('-excel_zabbix_deepseek_to_excel_qwen', nargs='?', metavar='无参数', dest='excel_zabbix_deepseek_to_excel_qwen', default='excel_zabbix_deepseek_to_excel_qwen',
                        help=u"使用千问翻译文本到excel")
    parser.add_argument('-remove_command_lines', nargs='?', metavar='无参数', dest='remove_command_lines', default='remove_command_lines',
                        help=u"从Excel移除冗余文本")
    parser.add_argument('-generate_password', nargs='?', metavar='无参数', dest='generate_password', default='generate_password',
                        help=u"生成8位随机密码")
    parser.add_argument('-users_with_passwords', nargs='?', metavar='无参数', dest='users_with_passwords', default='users_with_passwords',
                        help=u"为A列用户生成密码到B列")
    parser.add_argument('-hanzi_to_pinyin', nargs='?', metavar='无参数', dest='hanzi_to_pinyin', default='hanzi_to_pinyin',
                        help=u"将汉字转换为小写拼音")
    parser.add_argument('-PyPIMirrorSync', nargs='?', metavar='无参数', dest='PyPIMirrorSync', default='PyPIMirrorSync',
                        help=u"Python实现pip源同步到本地")
    parser.add_argument('--mirror', default='https://mirrors.aliyun.com/pypi/simple/',
                        help='镜像URL')
    parser.add_argument('--dir', default='./packages',
                        help='下载目录')
    parser.add_argument('--workers', type=int, default=5,
                        help='并发工作线程数')
    parser.add_argument('--limit', type=int, default=None,
                        help='最大下载包数')
    parser.add_argument('--timeout', type=float, default=30.0,
                        help='超时时间（秒）')
    parser.add_argument('--type')
    parser.add_argument('--len')
    parser.add_argument('-firefox_upload_file_to_translate_zabbix'
                        '', nargs='?', metavar='无参数', dest='firefox_upload_file_to_translate_zabbix', default='firefox_upload_file_to_translate_zabbix',
                        help=u"上传翻译文本到zabbix翻译官网")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 如有问题请联系作者QQ1284524409',
                        help=u"如有问题请联系作者QQ1284524409")

    args = parser.parse_args()
    cus_excel_op = CusExcelOp()
    cus_deepseek = CusLanguageTransDeepSeek(args)
    cus_deepseekdify = CusLanguageTransDeepSeekDify()
    cus_deepseekqianwen = CusLanguageTransDeepSeekQianWen()

    if len(sys.argv) == 1:
        print(parser.print_help())
        # ![导出po到excel]
    # ![] venv\Scripts\python.exe zabbix_api_base.py -poedit_zabbix_ui_to_excel
    elif args.poedit_zabbix_ui_to_excel != 'poedit_zabbix_ui_to_excel':
        title_name = ['注释', 'msgid', 'msgid_plural', 'msgstr', 'msgstr0', 'msgctxt']
        cus_excel_op.create_new_workbook()
        cus_excel_op.create_sheet("frontend")
        [cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]

        cus_poEdit = CusPoEdit()
        res_poreturn = cus_poEdit.def_translate("frontend.po")

        for i in range(len(res_poreturn['msgcomment'])):
            for x in range(1, 7):
                if x == 1:
                    cus_excel_op.set_cell_value(i + 2, x, res_poreturn['msgcomment'][i])
                elif x == 2:
                    cus_excel_op.set_cell_value(i + 2, x, res_poreturn['msgid'][i])
                elif x == 3:
                    cus_excel_op.set_cell_value(i + 2, x, res_poreturn['msgid_plural'][i])
                elif x == 4:
                    cus_excel_op.set_cell_value(i + 2, x, res_poreturn['msgstr'][i])
                elif x == 5:
                    cus_excel_op.set_cell_value(i + 2, x, res_poreturn['msgstr0'][i])
                elif x == 6:
                    cus_excel_op.set_cell_value(i + 2, x, res_poreturn['msgctxt'][i])
            i = i + 1
        cus_excel_op.save_workbook('frontend.xlsx')
    # ![] venv\Scripts\python.exe zabbix_api_base.py -excel_zabbix_ui_to_poedit
    elif args.excel_zabbix_ui_to_poedit != 'excel_zabbix_ui_to_poedit':
        cus_poEdit = CusPoEdit()
        for var_i in range(1, 5):
            cus_excel_op.load_excel('trans/frontend_.xlsx', var_i)
            column_1_list = cus_excel_op.get_column_values(1)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            del column_1_list[0]
            column_2_list = []
            column_3_list = []
            column_4_list = []
            column_5_list = []
            column_6_list = []
            with open('frontend_{0}.po'.format(first_active_sheet_name), 'w', encoding='utf-8') as s_hosts:
                s_hosts.truncate()
                s_hosts.write(
"""
msgid ""
msgstr ""
"Project-Id-Version: Zabbix {1}\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: {0}+0800\\n"
"PO-Revision-Date: {0}+0800\\n"
"Last-Translator: NoYoWiFi <1284524409@qq.com>\\n"
"Language-Team: Zabbix <info@zabbix.com>\\n"
"Language: zh_CN\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=1; plural=0;\\n"
"X-Generator: Poedit 2.2\\n"
"X-POOTLE-MTIME: {2}\\n"
"X-Poedit-Basepath: ../..\\n"
""".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), first_active_sheet_name,
                   time.mktime(time.strptime(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()), "%a %b %d %H:%M:%S %Y"))))
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.get_cell_value(i + 2, 2))
                column_3_list.append(cus_excel_op.get_cell_value(i + 2, 3))
                column_4_list.append(cus_excel_op.get_cell_value(i + 2, 4))
                column_5_list.append(cus_excel_op.get_cell_value(i + 2, 5))
                column_6_list.append(cus_excel_op.get_cell_value(i + 2, 6))
                cus_poEdit.def_create_pofile('frontend_{0}.po'.format(cus_excel_op.worksheet.title), column_1_list[i], column_2_list[i], column_3_list[i],
                                             column_4_list[i], column_5_list[i], column_6_list[i])
            print(len(column_2_list))
    # ![] venv\Scripts\python.exe zabbix_api_base.py -xliff_zabbix_document_to_excel --v=6.0
    # ![] venv\Scripts\python.exe zabbix_api_base.py -xliff_zabbix_document_to_excel --v=7.0
    # ![] venv\Scripts\python.exe zabbix_api_base.py -xliff_zabbix_document_to_excel --v=7.4
    elif args.xliff_zabbix_document_to_excel != 'xliff_zabbix_document_to_excel':
        title_name = ['路径', 'ID', '英文', '中文']
        cus_excel_op.create_new_workbook()
        cus_excel_op.create_sheet("document")
        [cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]

        cus_xliff = Cusxliff()
        __get_file_list_tmp = []
        __get_file_list = cus_xliff.def_get_filelist(f'D:\\00_development\\pycharm\\zabbix_documentation_{args.v}\\zh-CN', __get_file_list_tmp, 'xliff')
        i = 0
        for _int_01 in range(len(__get_file_list)):
            trans_units = cus_xliff.def_translate(__get_file_list[_int_01])
            # 打印结果
            for id_value, (source_value, target_value, original_file) in trans_units.items():
                # print(f"ID: {id_value}")
                # print(f"Source: {source_value}")
                # print(f"Target: {target_value}")
                # print(f"Original File: {original_file}")
                current_progress = _int_01 + 1
                total_length = len(__get_file_list)
                progress_percentage = (current_progress / total_length) * 100

                # 输出当前进度和总进度
                print(f'当前进度: {current_progress}/{total_length} ({progress_percentage:.2f}%)')
                for x in range(len(title_name)):
                    if x == 0:
                        cus_excel_op.set_cell_value(i + 2, x + 1, f'{original_file}')
                    elif x == 1:
                        cus_excel_op.set_cell_value(i + 2, x + 1, f'{str(id_value)}')
                    elif x == 2:
                        cus_excel_op.set_cell_value(i + 2, x + 1, f'{source_value}')
                    elif x == 3:
                        cus_excel_op.set_cell_value(i + 2, x + 1, f'{target_value}')
                i = i + 1
        cus_excel_op.save_workbook(f'document_{args.v}.xlsx')

    # ![] venv\Scripts\python.exe zabbix_api_base.py -excel_zabbix_document_to_xliff --v=7.4
    elif args.excel_zabbix_document_to_xliff != 'excel_zabbix_document_to_xliff':
        cus_excel_op_01 = CusExcelOp()
        cus_excel_op_02 = CusExcelOp()
        cus_excel_op_03 = CusExcelOp()
        cus_excel_op_01.load_excel(f'document_{args.v}.xlsx', 1)
        column_1_list = cus_excel_op_01.get_column_values(1)
        del column_1_list[0]
        column_2_list = []
        column_3_list = []
        column_4_list = []
        # 创建根元素
        xliff_root = etree.Element("xliff", nsmap={None: "urn:oasis:names:tc:xliff:document:1.2"}, attrib={"version": "1.2"})

        title_name_01 = ['路径', 'ID', '链接个数', '链接', '中文翻译']
        cus_excel_op_02.create_new_workbook()
        cus_excel_op_02.create_sheet("link")
        [cus_excel_op_02.set_cell_value(1, i + 1, title_name_01[i]) for i in range(len(title_name_01))]
        cus_excel_op_02.save_workbook(f'link_{args.v}.xlsx')

        title_name_02 = ['路径', 'ID', '标题个数', '英文标题', '中文标题']
        cus_excel_op_03.create_new_workbook()
        cus_excel_op_03.create_sheet("head")
        [cus_excel_op_03.set_cell_value(1, i + 1, title_name_02[i]) for i in range(len(title_name_02))]
        zabbix_api.def_rmtree_ignore_errors(f'.\\zh-CN_{args.v}\\', ignore_dirs={'.obsidian'})
        var_int_01 = 1
        var_int_03 = 1
        for i in range(len(column_1_list)):
            me_md_path = column_1_list[i]
            me_id = str(cus_excel_op_01.get_cell_value(i + 2, 2))
            me_source = cus_excel_op_01.get_cell_value(i + 2, 3)
            me_target = cus_excel_op_01.get_cell_value(i + 2, 4)
            var_source = me_source
            var_target = me_target
            links_en = Cusxliff.def_extract_links_from_md(var_source)
            if var_target is None:
                continue
            links_zh = Cusxliff.def_extract_links_from_md(var_target)
            for var_int_02 in range(len(links_en)):
                cus_excel_op_02.set_cell_value(var_int_01 + 1, 1, f'{me_md_path}')
                cus_excel_op_02.set_cell_value(var_int_01 + 1, 2, f'{me_id}')
                cus_excel_op_02.set_cell_value(var_int_01 + 1, 3, f'{len(links_en)}/{var_int_02 + 1}')
                cus_excel_op_02.set_cell_value(var_int_01 + 1, 4, f'{links_en[var_int_02]}')
                try:
                    cus_excel_op_02.set_cell_value(var_int_01 + 1, 5, f'{links_zh[var_int_02]}')
                except IndexError:
                    pass
                var_int_01 = var_int_01 + 1
            heads_en = Cusxliff.def_extract_headers_from_md(var_source)
            heads_zh = Cusxliff.def_extract_headers_from_md(var_target)
            for var_int_04 in range(len(heads_en)):
                cus_excel_op_03.set_cell_value(var_int_03 + 1, 1, f'{me_md_path}')
                cus_excel_op_03.set_cell_value(var_int_03 + 1, 2, f'{me_id}')
                cus_excel_op_03.set_cell_value(var_int_03 + 1, 3, f'{len(heads_en)}/{var_int_04 + 1}')
                cus_excel_op_03.set_cell_value(var_int_03 + 1, 4, f'{heads_en[var_int_04]}')
                try:
                    cus_excel_op_03.set_cell_value(var_int_03 + 1, 5, f'{heads_zh[var_int_04]}')
                except IndexError:
                    pass
                var_int_03 = var_int_03 + 1
            # 创建file元素
            file_elem = etree.SubElement(xliff_root, "file", attrib={"source-language": "en", "target-language": "zh-CN", "datatype": "plaintext", "original": me_md_path})

            # 创建body元素
            body_elem = etree.SubElement(file_elem, "body")

            # 创建trans-unit元素
            trans_unit_elem = etree.SubElement(body_elem, "trans-unit", attrib={"id": str(me_id), "{http://www.w3.org/XML/1998/namespace}space": "preserve"})

            # 创建source元素
            source_elem = etree.SubElement(trans_unit_elem, "source")
            source_elem.text = me_source

            # 创建target元素
            target_elem = etree.SubElement(trans_unit_elem, "target")
            target_elem.text = me_target
            var_md_path = os.path.join(f".\\zh-CN_{args.v}\\", me_md_path.replace("/","\\"))
            if not os.path.exists(os.path.dirname(var_md_path)):
                os.makedirs(os.path.dirname(var_md_path))

            print(zabbix_api.def_percentage(column_1_list, i), var_md_path)
            with open(f'{var_md_path}', "a", encoding="utf-8") as f:
                f.write(f'{me_target} \n')

        # 转换为XML字符串
        xml_str = etree.tostring(xliff_root, encoding="utf-8", pretty_print=True, xml_declaration=True)
        cus_excel_op_02.save_workbook(f'link_{args.v}.xlsx')
        cus_excel_op_03.save_workbook(f'head_{args.v}.xlsx')
        # 将XML字符串写入文件
        with open(f"document_{args.v}.xliff", "wb") as f:
            f.write(xml_str)

    elif args.excel_zabbix_deepseek_to_excel != 'excel_zabbix_deepseek_to_excel':
        cus_termProcessor = CusTermProcessor("zabbix_terms.xlsx")
        # 初始化处理器
        processor = CusTranslationProcessor(
            args=args,
            cus_termProcessor=cus_termProcessor,
            cus_excel_op=cus_excel_op,
            cus_deepseekdify=cus_deepseek
        )

        # 执行处理
        processor.process()
    # ![] venv\Scripts\python.exe zabbix_api_base.py -excel_zabbix_deepseek_to_excel_dify
    elif args.excel_zabbix_deepseek_to_excel_dify != 'excel_zabbix_deepseek_to_excel_dify':
        cus_termProcessor = CusTermProcessor("zabbix_terms.xlsx")
        # 初始化处理器
        processor = CusTranslationProcessor(
            args=args,
            cus_termProcessor=cus_termProcessor,
            cus_excel_op=cus_excel_op,
            cus_deepseekdify=cus_deepseekdify
        )

        # 执行处理
        processor.process()

    elif args.excel_zabbix_deepseek_to_excel_qwen != 'excel_zabbix_deepseek_to_excel_qwen':
        cus_termProcessor = CusTermProcessor("zabbix_terms.xlsx")
        # 初始化处理器
        processor = CusTranslationProcessor(
            args=args,
            cus_termProcessor=cus_termProcessor,
            cus_excel_op=cus_excel_op,
            cus_deepseekdify=cus_deepseekqianwen
        )

        # 执行处理
        processor.process()

    elif args.remove_command_lines != 'remove_command_lines':
        # 将主逻辑包装在函数中，以便使用nonlocal
        def process_data():
            cus_localMethord = CusLocalMethod()
            xlsx_file = '6.15-7.3 to侯建明.xlsx'
            sheet_title = '图形审计'
            output_file = '审计日志处理结果.xlsx'

            # 先删除旧文件（如果存在）
            if os.path.exists(output_file):
                os.remove(output_file)

            cus_excel_op.load_excel(xlsx_file, 1)
            column_1_list = cus_excel_op.get_column_values(7)
            del column_1_list[0]

            # 初始化结果列表
            lv_list_get_all_host_groupid = [""] * len(column_1_list)

            # 分批处理配置
            batch_size = 100
            total_items = len(column_1_list)
            start_index = 0
            print(f"\033[;33m从第 {start_index + 1} 项开始处理（跳过前 {start_index} 项）\033[0m")

            # 进度统计变量
            total_completed = 0
            total_success = 0
            total_failed = 0

            # 回调函数：处理每个任务的完成状态（现在嵌套在process_data函数内）
            def task_callback(future, batch_num, index, batch_size, total_batches):
                nonlocal total_completed, total_success, total_failed

                try:
                    result = future.result()
                    total_success += 1
                    status = "\033[;32m✓\033[0m"
                except Exception as e:
                    total_failed += 1
                    status = "\033[;31m✗\033[0m"
                    print(f"\n错误处理行 {index + 1}: {str(e)}")

                total_completed += 1

                # 实时进度显示（每10个或最后一条更新）
                if total_completed % 10 == 0 or total_completed == batch_size:
                    batch_progress = total_completed / batch_size * 100
                    total_progress = (start_index + total_completed) / total_items * 100
                    print(
                        f"\r批次 {batch_num}/{total_batches}: "
                        f"进度 {total_completed}/{batch_size} ({batch_progress:.1f}%) | "
                        f"总计 {start_index + total_completed}/{total_items} ({total_progress:.1f}%) | "
                        f"成功 {total_success} | 失败 {total_failed} {status}",
                        end="", flush=True
                    )

            # 主处理循环
            for batch_start in range(start_index, total_items, batch_size):
                batch_end = min(batch_start + batch_size, total_items)
                current_batch = column_1_list[batch_start:batch_end]
                batch_num = (batch_start // batch_size) + 1
                total_batches = (total_items + batch_size - 1) // batch_size

                print(f"\n\033[1;36m处理批次 {batch_num}/{total_batches} (行 {batch_start + 1}-{batch_end})\033[0m")

                with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
                    futures = []
                    for i, col in enumerate(current_batch):
                        if col:
                            row_num = batch_start + i + 2
                            result_txt = cus_localMethord.remove_command_lines(col)
                            future = executor.submit(
                                cus_excel_op.set_cell_value,
                                row_num,
                                7,
                                result_txt
                            )
                            future.add_done_callback(
                                lambda f, b=batch_num, idx=i, bs=len(current_batch), tb=total_batches:
                                task_callback(f, b, idx, bs, tb)
                            )
                            futures.append(future)

                    # 等待批次完成
                    wait(futures)

                # 保存当前批次结果
                cus_excel_op.save_workbook(output_file)
                print(f"\n\033[;33m批次 {batch_num} 结果已保存至 {output_file}\033[0m")

                # 更新总进度
                print(
                    f"批次 {batch_num} 完成: "
                    f"成功 {total_success}/{total_completed} | "
                    f"失败 {total_failed}"
                )


        # 执行处理函数
        process_data()
    # venv\Scripts\python.exe zabbix_api_base.py -generate_password --len=15
    elif args.generate_password != 'generate_password':
        # 将主逻辑包装在函数中，以便使用nonlocal
        cus_localMethord = CusLocalMethod()
        print("\n强密码:")
        # 生成强密码
        for i in range(10):
            pwd = cus_localMethord.generate_strong_password(length=int(args.len))
            print(f"{i+1}. {pwd}")
    # venv\Scripts\python.exe zabbix_api_base.py -users_with_passwords --len=8
    elif args.users_with_passwords != 'users_with_passwords':
        # 1. 初始化密码生成器（加载历史密码）
        password_generator = PasswordGenerator("passwords.xlsx")

        # 2. 加载用户文件
        cus_excel_op = CusExcelOp()
        cus_excel_op.load_excel("users.xlsm", 1)  # 假设有6个用户

        # 3. 为用户文件生成密码
        password_mapping = password_generator.generate_for_excel_column(cus_excel_op, 'B', int(args.len))

        # 4. 保存用户文件
        cus_excel_op.save_workbook("users_with_passwords.xlsx")

    # venv\Scripts\python.exe zabbix_api_base.py -firefox_upload_file_to_translate_zabbix
    elif args.firefox_upload_file_to_translate_zabbix != 'firefox_upload_file_to_translate_zabbix':
        # 准备导入文件
        fileName_fanyi = "fanyi.png"
        fileName_noresult = "noresult.png"
        fileName_find = "find.png"
        fileName_downlist = "downlist.png"
        fileName_potton = "potton.png"
        fileName_open = ("open.png", "open_20250903.png")
        rect_fanyi = (1328,389, 50, 50) # x=100, y=200, width=300, height=400，0,0在左上角
        rect_result = (341,216, 160, 60)  # x=100, y=200, width=300, height=400，0,0在左上角
        rect_find = (346, 149, 44, 60)
        rect_downlist = (356, 100, 400, 60)
        rect_open = (786,652, 100, 40)
        # 预设分辨率
        PRESET_RESOLUTION = (1600, 900)
        # 获取当前屏幕分辨率
        screen_width = win32api.GetSystemMetrics(0)  # SM_CXSCREEN
        screen_height = win32api.GetSystemMetrics(1)  # SM_CYSCREEN
        current_resolution = (screen_width, screen_height)
        print(f"当前屏幕分辨率: {current_resolution}")


        def wait_for_image(image_path, region, timeout=30):
            start_time = time.time()
            while time.time() - start_time < timeout:
                # confidence参数要求安装opencv venv\Scripts\pip.exe install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple
                location = pyautogui.locateCenterOnScreen(image_path, region=region, confidence=0.95)
                if location:
                    return location
                time.sleep(0.5)
            return None

        def wait_for_find_image(image_path, region, timeout=30):
            start_time = time.time()
            while time.time() - start_time < timeout:
                # 1.移动鼠标到404.xliffi
                pyautogui.moveTo(x=380, y=119, duration=0.3)
                pyautogui.click(clicks=1, button='left', interval=0.05)  # 点击
                time.sleep(0.5)
                # confidence参数要求安装opencv venv\Scripts\pip.exe install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple
                location = pyautogui.locateCenterOnScreen(image_path, region=region, confidence=0.95)
                if location:
                    return location
                time.sleep(1)
            return None

        def wait_for_find_downlist(image_path, region, timeout=30):
            start_time = time.time()
            while time.time() - start_time < timeout:
                # confidence参数要求安装opencv venv\Scripts\pip.exe install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple
                location = pyautogui.locateCenterOnScreen(image_path, region=region, confidence=0.95)
                if location:
                    return location
                # 1.移动鼠标到404.xliffi
                pyautogui.moveTo(x=25, y=60, duration=0.3)
                pyautogui.click(clicks=1, button='left', interval=0.05)  # 点击
                time.sleep(20)
            return None

        def wait_for_potton(x, y, image_path, region, timeout=360):
            start_time = time.time()
            while time.time() - start_time < timeout:
                # confidence参数要求安装opencv venv\Scripts\pip.exe install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple
                location = pyautogui.locateCenterOnScreen(image_path, region=region, confidence=0.95)
                if location:
                    return location
                time.sleep(10)
                if time.time() - start_time >= timeout * 0.9:
                    pyautogui.moveTo(x=x, y=y, duration=0.3)
                    pyautogui.click(clicks=1, button='left', interval=0.05)
                    pyautogui.moveTo(x=25, y=60, duration=0.3)
                    pyautogui.click(clicks=1, button='left', interval=0.05)  # 点击
                    time.sleep(30)
            return None

        def wait_for_find_open(image_paths, region, timeout=30):
            start_time = time.time()
            current_image_index = 0

            while time.time() - start_time < timeout:
                pyautogui.moveTo(1454,397, duration=0.3)
                pyautogui.click(clicks=1, button='left', interval=0.05)  # 点击
                time.sleep(0.5)  # 别问我为什么要停1秒，问就是给微信一个反应的时间，他反应慢反应不过来

                def wait_for_window_ready(window_class, window_caption, timeout=10):
                    """
                    等待窗口完全就绪
                    """
                    start_time = time.time()
                    while time.time() - start_time < timeout:
                        handle = win32gui.FindWindow(window_class, window_caption)

                        if handle and handle != 0:
                            # 检查窗口是否可见
                            if not win32gui.IsWindowVisible(handle):
                                time.sleep(0.2)
                                continue

                            # 检查窗口是否有有效矩形
                            try:
                                rect = win32gui.GetWindowRect(handle)
                                if rect[2] - rect[0] > 0 and rect[3] - rect[1] > 0:
                                    return handle
                            except:
                                pass

                        time.sleep(0.2)

                    return 0
                window_class = None  # 或者你查到的具体类名
                window_caption = '文件上传'  # 确保与实际标题完全一致
                handle = wait_for_window_ready(window_class, window_caption)
                if handle and handle != 0:
                    try:
                        # 缩放窗口至1000,700大小，位置（0,0）
                        win32gui.SetWindowPos(handle, win32con.HWND_TOP, 0, 0, 1000, 700, win32con.SWP_SHOWWINDOW)
                        time.sleep(0.5)
                        print("窗口调整成功")
                    except Exception as e:
                        print(f"窗口操作失败: {e}")
                        continue
                else:
                    print("等待窗口超时")
                    continue
                win32gui.SetForegroundWindow(handle)
                # confidence参数要求安装opencv venv\Scripts\pip.exe install opencv-python -i https://pypi.tuna.tsinghua.edu.cn/simple
                # 尝试当前图像路径
                current_image_path = image_paths[current_image_index]
                location = pyautogui.locateCenterOnScreen(current_image_path, region=region, confidence=0.95)
                if location:
                    return location
                # 切换到下一个图像路径
                current_image_index = (current_image_index + 1) % len(image_paths)
                pyautogui.moveTo(832, 666, duration=0.3)
                time.sleep(1)
            return None

        def fireFox(aString, bString):
            def setText(aString):
                try:
                    # print(f"正在打开剪贴板...")
                    w.OpenClipboard()
                    # print(f"正在清空剪贴板...")
                    w.EmptyClipboard()
                    # print(f"正在设置剪贴板数据: {aString}")
                    # 尝试使用不同的剪贴板格式
                    # w.SetClipboardData(win32con.CF_TEXT, aString.encode('utf-8'))
                    #或者使用: ()
                    w.SetClipboardText(f"{aString}")
                    time.sleep(0.5)
                    # print(f"正在关闭剪贴板...")
                    w.CloseClipboard()
                    print(f"成功设置剪贴板内容: {aString}")
                    time.sleep(0.5)  # 别问我为什么要停1秒，问就是给微信一个反应的时间，他反应慢反应不过来，其他位置暂停的原因同样
                    pyautogui.hotkey('ctrl', 'v', interval=0.5)  # 增加按键间隔
                    return True
                except Exception as e:
                    print(f"设置剪贴板内容失败: {e}")
                    return False

            qunliao_2 = wait_for_find_image(fileName_find, rect_find, timeout=30)
            if not qunliao_2:
                print(u"超时未找到图标: %s" % aString)
                pyautogui.alert(text="超时未找到图标", title="警告", button="ok")
                exit(1)

            # 2.移动鼠标到搜索框，单击，输入要搜索的名字
            pyautogui.moveTo(x=404, y=168, duration=0.3)
            pyautogui.click(clicks=1, button='left', interval=0.05)  # 点击
            time.sleep(0.5)
            setText(aString)  # 假设我的好友里有胡歌

            res_noresult = pyautogui.locateCenterOnScreen(fileName_noresult, region=rect_result, confidence=0.95)
            if res_noresult:
                print(u"未找到对应翻译继续下一个翻译: %s" % aString)
                return
            pyautogui.moveTo(x=498, y=235, duration=0.3)
            pyautogui.click(clicks=1, button='left', interval=0.05)  # 点击
            time.sleep(0.5)
            pyautogui.moveTo(1570, 116, duration=0.3)
            pyautogui.click(clicks=1, button='left', interval=0.05)  # 点击
            time.sleep(0.5)
            # 使用方式
            qunliao_1 = wait_for_image(fileName_fanyi, rect_fanyi, timeout=30)
            if not qunliao_1:
                print(u"超时未找到图标: %s" % aString)
                pyautogui.alert(text="超时未找到图标", title="警告", button="ok")
                exit(1)
            else:
                print(u"找到图标，继续执行...")
                qunliao_4 = wait_for_find_open(fileName_open, rect_open, timeout=30)
                if not qunliao_4:
                    print(u"超时未找到open图标: %s" % aString)
                    pyautogui.alert(text="超时未找到open图标", title="警告", button="ok")
                    exit(1)
                pyautogui.moveTo(368,635, duration=0.3)
                pyautogui.click(clicks=1, button='left', interval=0.05)  # 点击
                time.sleep(0.5)  # 别问我为什么要停1秒，问就是给微信一个反应的时间，他反应慢反应不过来
                setText(bString)
                pyautogui.moveTo(832,666, duration=0.3)
                pyautogui.click(clicks=1, button='left', interval=0.05)  # 点击
                time.sleep(0.5)  # 别问我为什么要停1秒，问就是给微信一个反应的时间，他反应慢反应不过来
                # pyautogui.press('Enter')
                time.sleep(0.5)

        def fanyi():
            # 加载Excel文件（第33个工作表）
            cus_excel_op.load_excel('document_.xlsx', 2)
            # 获取主机名和主机组名列（跳过表头）
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]
            column_2_list = [cus_excel_op.get_cell_value(i + 2, 2) for i in range(len(column_1_list))]
            coordinates = [
                (173,26),  # 坐标1: 404.xliffi
                (401,22),  # 坐标2: 搜索框
                (600,22),  # 坐标3: 搜索结果点击
                (842,24),  # 坐标4: 菜单按钮
                (1049,19)  # 坐标5: 文件上传
            ]

            coordinates1 = [
                (53,13),
                (278,13),
                (504,13),
                (731,13),
                (952,13)
            ]
            # print("{0}全省 ".format(aString) + bString)
            # return
            window_class = 'MozillaWindowClass'  # 或者你查到的具体类名
            window_caption = None  # 确保与实际标题完全一致
            handle = win32gui.FindWindow(window_class, window_caption)
            time.sleep(random.randint(1, 3))
            # 检查分辨率是否匹配预设值
            if current_resolution != PRESET_RESOLUTION:
                print(f"警告: 当前分辨率 {current_resolution} 与预设分辨率 {PRESET_RESOLUTION} 不匹配，程序退出。")
                pyautogui.alert(text=f"分辨率不匹配: 当前{current_resolution} 预设{PRESET_RESOLUTION}", title="分辨率错误", button="OK")
                sys.exit(1)
            # 判断窗口是否最小化状态
            if win32gui.IsIconic(handle):
                # 如果最小化，恢复默认状态
                win32gui.ShowWindow(handle, win32con.SW_SHOWDEFAULT)

            # 将窗口最大化
            win32gui.ShowWindow(handle, win32con.SW_MAXIMIZE)
            time.sleep(0.5)
            # 窗口放在所有窗口前面
            win32gui.SetForegroundWindow(handle)
            for i in range(len(column_1_list)):
                try:
                    # 使用模运算来循环选择坐标点
                    coord_index = i % len(coordinates)  # 当i>=5时，会回到0开始
                    x, y = coordinates[coord_index]

                    # 使用模运算来循环选择坐标点
                    coord_index1 = i % len(coordinates1)  # 当i>=5时，会回到0开始
                    x1, y1 = coordinates1[coord_index1]

                    print(f"正在处理第{i + 1}行数据，使用坐标 {coord_index + 1}: ({x}, {y})")
                    qunliao_4 = wait_for_potton(x, y, fileName_potton, (x1, y1, 20, 20), timeout=30)
                    if not qunliao_4:
                        print(u"超时网站不可用")
                        pyautogui.alert(text="超时网站不可用", title="警告", button="ok")
                        exit(1)

                    pyautogui.moveTo(x=x, y=y, duration=0.3)
                    pyautogui.click(clicks=1, button='left', interval=0.05)
                    qunliao_3 = wait_for_find_downlist(fileName_downlist, rect_downlist, timeout=30)
                    if not qunliao_3:
                        print(u"超时未找到下拉列表图标")
                        pyautogui.alert(text="超时未找到下拉列表图标", title="警告", button="ok")
                        exit(1)
                    # 执行fireFox函数
                    fireFox(column_1_list[i], column_2_list[i])
                    time.sleep(1)  # 每个数据处理后暂停1秒
                except Exception as e:
                    print(u"0表第\033[041m%s\033[0m行数据异常\n\033[041m%s\033[0m" % (i + 2, e))
                    sys.exit(1)
            # 提醒OK消息框
            pyautogui.alert(text="程序执行完毕", title="提醒", button="ok")
        fanyi()
    # venv\Scripts\python.exe zabbix_api_base.py -hanzi_to_pinyin
    elif args.hanzi_to_pinyin != 'hanzi_to_pinyin':
        # 加载Excel文件（第11个工作表）
        cus_excel_op.load_excel('hanzi_to_pinyin.xlsx', 1)
        cus_localMethord = CusLocalMethod()
        # 获取各列数据
        column_1_list = cus_excel_op.get_column_values(1)
        del column_1_list[0]  # 删除标题行
        cus_excel_op.create_new_workbook()
        title_name = ['汉字', '拼音']
        cus_excel_op.create_sheet("hanzi_to_pinyin")
        [cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
        for row_index in range(len(column_1_list)):
            result = cus_localMethord.hanzi_to_pinyin(column_1_list[row_index])
            cus_excel_op.set_cell_value(row_index + 2, 1, f"{column_1_list[row_index]}")
            cus_excel_op.set_cell_value(row_index + 2, 2, f"{result}")
            print(f"'{column_1_list[row_index]}' -> '{result}'")
        cus_excel_op.save_workbook("hanzi_to_pinyin_result.xlsx")
        # venv\Scripts\python.exe zabbix_api_base.py -hanzi_to_pinyin
    # 仅列出包名
    # venv\Scripts\python.exe zabbix_api_base.py --PyPIMirrorSync
    elif args.PyPIMirrorSync != 'PyPIMirrorSync':
        # # 查看帮助
        # python pypi_mirror_sync.py --help
        #
        # # 仅列出包
        # python pypi_mirror_sync.py --list-only --mirror https://mirrors.aliyun.com/pypi/simple/
        #
        # # 同步包
        # python pypi_mirror_sync.py --dir ./packages --workers 10 --limit 100
        #
        # # 断点续传
        # python pypi_mirror_sync.py --resume
        """主函数"""
        # 极简配置 - 专门针对第一次同步
        config = {
            'mirror_url': 'https://mirrors.aliyun.com/pypi/simple/',
            'download_dir': Path('D:/python/pip.download/packages'),
            'log_dir': Path('D:/python/pip.download/logs'),
            'max_workers': 1,  # 单线程，避免并发问题
            'timeout': 60.0,  # 较长的超时时间
            'retries': 1,  # 较少重试
            'skip_existing': True,
            'verify_checksum': False,  # 关闭哈希验证
            'file_types': ['.whl', '.tar.gz', '*'],  # 简化文件类型
            'max_packages': 5,  # 只下载5个包用于测试
            'show_progress': False,  # 关闭进度条
            'safe_mode': True,  # 启用安全模式
        }

        # config = {
        #     'mirror_url': 'https://mirrors.aliyun.com/pypi/simple/',
        #     'max_packages': None,  # 下载所有包
        #     'verify_checksum': True,  # 启用验证
        #     'show_progress': True,  # 显示进度
        #     'max_workers': 5,  # 多线程
        #     'download_strategy': 'simple',  # 简单策略
        # }

        print("=" * 60)
        print("PyPI镜像同步工具 - 安全测试版")
        print("=" * 60)

        try:
            # 创建同步器
            sync = PyPIMirrorSync(config)

            # 开始同步
            print("\n开始同步...")
            success = sync.sync(resume=True)

            if success:
                print("\n✅ 同步成功完成！")
            else:
                print("\n⚠️  同步完成，但有失败的项目")

        except KeyboardInterrupt:
            print("\n⏹️  同步被用户中断")
        except Exception as e:
            print(f"\n❌ 同步过程中发生错误: {e}")
            import traceback

            traceback.print_exc()


    else:
        cus_zabbix_api = CusZabbixApi()
        # ![01_创建Proxy组]
        if args.create_proxygroup != 'create_proxygroup':
            def process_data():
                cus_excel_op.load_excel('zabbix_api.xlsx', 51)
                column_1_list = cus_excel_op.get_column_values(1)
                del column_1_list[0]

                # 去重并保持原始顺序
                unit_column_1_list = sorted(set(column_1_list), key=column_1_list.index)

                # 准备数据
                column_2_list = [cus_excel_op.get_cell_value(i + 2, 2) for i in range(len(column_1_list))]
                column_3_list = [cus_excel_op.get_cell_value(i + 2, 3) for i in range(len(column_1_list))]

                total_tasks = len(unit_column_1_list)
                completed_tasks = 0
                success_count = 0
                failed_count = 0

                # 进度回调函数
                def progress_callback(future, index):
                    nonlocal completed_tasks, success_count, failed_count
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            success_count += 1
                            status = "\033[;32m✓\033[0m"
                            print(f"\r[{completed_tasks + 1}/{total_tasks}] 创建Proxy组: \033[;34m{unit_column_1_list[index]}\033[0m {status} 返回: \033[;32m{lv_result['result']}\033[0m")
                        else:
                            failed_count += 1
                            status = "\033[;31m✗\033[0m"
                            print(f"\r[{completed_tasks + 1}/{total_tasks}] 创建Proxy组: \033[;34m{unit_column_1_list[index]}\033[0m {status} 返回: \033[;31m{lv_result['result']}\033[0m")
                    except Exception as e:
                        failed_count += 1
                        print(f"\r[{completed_tasks + 1}/{total_tasks}] 创建Proxy组: \033[;34m{unit_column_1_list[index]}\033[0m \033[;31m错误: {str(e)}\033[0m")
                    finally:
                        completed_tasks += 1
                        progress = (completed_tasks / total_tasks) * 100
                        print(f"\r总进度: {completed_tasks}/{total_tasks} ({progress:.1f}%) | 成功: {success_count} | 失败: {failed_count}", end="", flush=True)


                # 使用线程池处理
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for index, (name, val2, val3) in enumerate(zip(unit_column_1_list, column_2_list, column_3_list)):
                        future = executor.submit(cus_zabbix_api.def_create_proxygroup, name, val2, val3)
                        future.add_done_callback(lambda f, idx=index: progress_callback(f, idx))
                        futures.append(future)

                    # 等待所有任务完成
                    wait(futures)

                # 最终统计
                print(f"\n\n处理完成: 总计 {total_tasks} 个任务")
                print(f"成功: \033[;32m{success_count}\033[0m | 失败: \033[;31m{failed_count}\033[0m")
                if failed_count > 0:
                    print("请注意检查失败的Proxy组创建任务")

            process_data()
        elif args.delete_proxygroup != 'delete_proxygroup':
            def process_proxygroup_deletion():
                cus_excel_op.load_excel('zabbix_api.xlsx', 51)
                column_1_list = cus_excel_op.get_column_values(1)
                del column_1_list[0]

                # 去重并保持原始顺序
                unit_column_1_list = sorted(set(column_1_list), key=column_1_list.index)
                total_tasks = len(unit_column_1_list)

                # 进度显示函数
                def print_progress(current, total, success, failed, action):
                    progress = (current / total) * 100
                    print(f"\r{action}进度: {current}/{total} ({progress:.1f}%) | 成功: \033[32m{success}\033[0m | 失败: \033[31m{failed}\033[0m", end="", flush=True)

                # 第一阶段：获取Proxy组ID
                print("\n\033[1;36m=== 开始获取Proxy组ID ===\033[0m")
                lv_list_all_proxygroupid = []
                get_success = 0
                get_failed = 0

                def get_callback(future, index, name):
                    nonlocal get_success, get_failed, lv_list_all_proxygroupid
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            lv_list_all_proxygroupid.append([lv_result['result'][0]['proxy_groupid']])
                            get_success += 1
                        else:
                            get_failed += 1
                            print(f"\n获取Proxy组ID失败: {name} | 返回值: {lv_result['result']}")

                        print_progress(get_success + get_failed, total_tasks, get_success, get_failed, "获取")
                    except Exception as e:
                        get_failed += 1
                        print(f"\n获取Proxy组ID异常: {name} | 错误: {str(e)}")
                        print_progress(get_success + get_failed, total_tasks, get_success, get_failed, "获取")

                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, name in enumerate(unit_column_1_list):
                        future = executor.submit(cus_zabbix_api.def_get_proxygroup, name)
                        future.add_done_callback(partial(get_callback, index=idx, name=name))
                        futures.append(future)
                    wait(futures)

                print(f"\n\n获取完成: 总计 {total_tasks} | 成功: \033[32m{get_success}\033[0m | 失败: \033[31m{get_failed}\033[0m")

                # 检查是否有可删除的Proxy组
                if not lv_list_all_proxygroupid:
                    print("\033[31m没有可删除的Proxy组，终止操作\033[0m")
                    return  # 现在这个return在函数内部，是合法的

                # 第二阶段：删除Proxy组
                print("\n\033[1;36m=== 开始删除Proxy组 ===\033[0m")
                del_success = 0
                del_failed = 0

                def del_callback(future, index, name):
                    nonlocal del_success, del_failed
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            del_success += 1
                            print(f"\n删除成功: {name} | 返回值: {lv_result['result']}")
                        else:
                            del_failed += 1
                            print(f"\n删除失败: {name} | 返回值: {lv_result['result']}")

                        print_progress(del_success + del_failed, len(lv_list_all_proxygroupid), del_success, del_failed, "删除")
                    except Exception as e:
                        del_failed += 1
                        print(f"\n删除异常: {name} | 错误: {str(e)}")
                        print_progress(del_success + del_failed, len(lv_list_all_proxygroupid), del_success, del_failed, "删除")

                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, (proxy_id, name) in enumerate(zip(lv_list_all_proxygroupid, unit_column_1_list)):
                        future = executor.submit(cus_zabbix_api.def_delete_proxygroup, proxy_id)
                        future.add_done_callback(partial(del_callback, index=idx, name=name))
                        futures.append(future)
                    wait(futures)

                print(f"\n\n删除完成: 总计 {len(lv_list_all_proxygroupid)} | 成功: \033[32m{del_success}\033[0m | 失败: \033[31m{del_failed}\033[0m")


            # 执行处理函数
            process_proxygroup_deletion()
        # ![01_创建Proxy]
        elif args.create_proxy != 'create_proxy':
            def process_proxy_creation():
                # 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 52)
                column_1_list = cus_excel_op.get_column_values(1)
                del column_1_list[0]

                # 去重并保持原始顺序
                unit_column_1_list = sorted(set(column_1_list), key=column_1_list.index)
                total_tasks = len(unit_column_1_list)

                # 读取其他列数据
                column_data = {
                    2: [], 3: [], 4: [], 5: [],
                    6: [], 7: [], 8: []
                }
                for i in range(len(column_1_list)):
                    for col in column_data:
                        column_data[col].append(cus_excel_op.get_cell_value(i + 2, col))

                # 进度显示函数
                def print_progress(action, current, total, success, failed):
                    progress = (current / total) * 100
                    print(f"\r{action}进度: {current}/{total} ({progress:.1f}%) | 成功: \033[32m{success}\033[0m | 失败: \033[31m{failed}\033[0m",
                          end="", flush=True)

                # 第一阶段：获取Proxy组ID
                print("\n\033[1;36m=== 开始获取Proxy组ID ===\033[0m")
                lv_list_all_proxygroupid = []
                get_success = 0
                get_failed = 0

                def get_callback(future, index, name):
                    nonlocal get_success, get_failed, lv_list_all_proxygroupid
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            lv_list_all_proxygroupid.append(lv_result['result'][0]['proxy_groupid'])
                            get_success += 1
                        else:
                            get_failed += 1
                            print(f"\n获取Proxy组ID失败: {name} | 返回值: {lv_result['result']}")

                        print_progress("获取", get_success + get_failed, total_tasks, get_success, get_failed)
                    except Exception as e:
                        get_failed += 1
                        print(f"\n获取Proxy组ID异常: {name} | 错误: {str(e)}")
                        print_progress("获取", get_success + get_failed, total_tasks, get_success, get_failed)

                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, name in enumerate(column_data[2]):  # column_2_list
                        future = executor.submit(cus_zabbix_api.def_get_proxygroup, name)
                        future.add_done_callback(partial(get_callback, index=idx, name=name))
                        futures.append(future)
                    wait(futures)

                print(f"\n\n获取完成: 总计 {total_tasks} | 成功: \033[32m{get_success}\033[0m | 失败: \033[31m{get_failed}\033[0m")

                # 检查是否获取到足够的Proxy组ID
                if len(lv_list_all_proxygroupid) != total_tasks:
                    print("\033[31m错误: 获取的Proxy组ID数量不匹配，终止操作\033[0m")
                    return

                # 第二阶段：创建Proxy
                print("\n\033[1;36m=== 开始创建Proxy ===\033[0m")
                create_success = 0
                create_failed = 0

                def create_callback(future, index, name):
                    nonlocal create_success, create_failed
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            create_success += 1
                            print(f"\n创建成功: {name} | 返回值: {lv_result['result']}")
                        else:
                            create_failed += 1
                            print(f"\n创建失败: {name} | 返回值: {lv_result['result']}")

                        print_progress("创建", create_success + create_failed, total_tasks, create_success, create_failed)
                    except Exception as e:
                        create_failed += 1
                        print(f"\n创建异常: {name} | 错误: {str(e)}")
                        print_progress("创建", create_success + create_failed, total_tasks, create_success, create_failed)

                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx in range(total_tasks):
                        future = executor.submit(
                            cus_zabbix_api.def_create_proxy,
                            unit_column_1_list[idx],  # column_1
                            lv_list_all_proxygroupid[idx],  # proxy_groupid
                            column_data[3][idx],  # column_3
                            column_data[4][idx],  # column_4
                            column_data[5][idx],  # column_5
                            column_data[6][idx],  # column_6
                            column_data[7][idx],  # column_7
                            column_data[8][idx]  # column_8
                        )
                        future.add_done_callback(partial(create_callback, index=idx, name=unit_column_1_list[idx]))
                        futures.append(future)
                    wait(futures)

                print(f"\n\n创建完成: 总计 {total_tasks} | 成功: \033[32m{create_success}\033[0m | 失败: \033[31m{create_failed}\033[0m")


            # 执行处理函数
            process_proxy_creation()
        elif args.delete_proxy != 'delete_proxy':

            def process_proxy_deletion():
                # 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 52)
                column_1_list = cus_excel_op.get_column_values(1)
                del column_1_list[0]

                # 去重并保持原始顺序
                unit_column_1_list = sorted(set(column_1_list), key=column_1_list.index)
                total_tasks = len(unit_column_1_list)

                # 进度显示函数
                def print_progress(action, current, total, success, failed):
                    progress = (current / total) * 100
                    print(f"\r{action}进度: {current}/{total} ({progress:.1f}%) | 成功: \033[32m{success}\033[0m | 失败: \033[31m{failed}\033[0m",
                          end="", flush=True)

                # 第一阶段：获取Proxy ID
                print("\n\033[1;36m=== 开始获取Proxy ID ===\033[0m")
                lv_list_all_proxyid = []
                get_success = 0
                get_failed = 0

                def get_callback(future, index, name):
                    nonlocal get_success, get_failed, lv_list_all_proxyid
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            lv_list_all_proxyid.append(lv_result['result'][0]['proxyid'])
                            get_success += 1
                        else:
                            get_failed += 1
                            print(f"\n获取Proxy ID失败: {name} | 返回值: {lv_result['result']}")

                        print_progress("获取", get_success + get_failed, total_tasks, get_success, get_failed)
                    except Exception as e:
                        get_failed += 1
                        print(f"\n获取Proxy ID异常: {name} | 错误: {str(e)}")
                        print_progress("获取", get_success + get_failed, total_tasks, get_success, get_failed)

                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, name in enumerate(unit_column_1_list):
                        future = executor.submit(cus_zabbix_api.def_get_proxy, name)
                        future.add_done_callback(partial(get_callback, index=idx, name=name))
                        futures.append(future)
                    wait(futures)

                print(f"\n\n获取完成: 总计 {total_tasks} | 成功: \033[32m{get_success}\033[0m | 失败: \033[31m{get_failed}\033[0m")

                # 检查是否获取到足够的Proxy ID
                if not lv_list_all_proxyid:
                    print("\033[31m错误: 未获取到任何Proxy ID，终止操作\033[0m")
                    return

                # 第二阶段：删除Proxy
                print("\n\033[1;36m=== 开始删除Proxy ===\033[0m")
                del_success = 0
                del_failed = 0

                def del_callback(future, index, name):
                    nonlocal del_success, del_failed
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            del_success += 1
                            print(f"\n删除成功: {name} | 返回值: {lv_result['result']}")
                        else:
                            del_failed += 1
                            print(f"\n删除失败: {name} | 返回值: {lv_result['result']}")

                        print_progress("删除", del_success + del_failed, len(lv_list_all_proxyid), del_success, del_failed)
                    except Exception as e:
                        del_failed += 1
                        print(f"\n删除异常: {name} | 错误: {str(e)}")
                        print_progress("删除", del_success + del_failed, len(lv_list_all_proxyid), del_success, del_failed)

                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, (proxy_id, name) in enumerate(zip(lv_list_all_proxyid, unit_column_1_list)):
                        future = executor.submit(cus_zabbix_api.def_delete_proxy, [proxy_id])
                        future.add_done_callback(partial(del_callback, index=idx, name=name))
                        futures.append(future)
                    wait(futures)

                print(f"\n\n删除完成: 总计 {len(lv_list_all_proxyid)} | 成功: \033[32m{del_success}\033[0m | 失败: \033[31m{del_failed}\033[0m")


            # 执行处理函数
            process_proxy_deletion()
        # ![01_创建主机组]
        elif args.create_hostgroup != 'create_hostgroup':
            def process_data():
                # 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 1)
                column_1_list = cus_excel_op.get_column_values(1)
                del column_1_list[0]

                # 去重并保持原始顺序
                unit_column_1_list = sorted(set(column_1_list), key=column_1_list.index)
                total_tasks = len(unit_column_1_list)

                # 进度统计
                completed_tasks = 0
                success_count = 0
                failed_count = 0


                # 回调函数
                def hostgroup_callback(future, hostgroup_name, index):
                    nonlocal completed_tasks, success_count, failed_count
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            success_count += 1
                            status = "\033[32m✓\033[0m"
                            result_msg = f"返回值: \033[32m{lv_result['result']}\033[0m"
                        else:
                            failed_count += 1
                            status = "\033[31m✗\033[0m"
                            result_msg = f"返回值: \033[31m{lv_result['result']}\033[0m"

                        # 实时更新进度
                        completed_tasks += 1
                        progress = (completed_tasks / total_tasks) * 100

                        # 打印当前任务结果
                        print(f"\r[{index + 1}/{total_tasks}] 创建主机组: {hostgroup_name} {status} {result_msg}")

                        # 打印汇总进度
                        print(f"\r总进度: {completed_tasks}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{success_count}\033[0m | "
                              f"失败: \033[31m{failed_count}\033[0m", end="", flush=True)

                    except Exception as e:
                        failed_count += 1
                        completed_tasks += 1
                        print(f"\r[{index + 1}/{total_tasks}] 创建主机组: {hostgroup_name} \033[31m错误: {str(e)}\033[0m")


                # 使用线程池处理
                print(f"\n\033[1;36m=== 开始创建主机组 (共 {total_tasks} 个) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, hostgroup_name in enumerate(unit_column_1_list):
                        future = executor.submit(cus_zabbix_api.def_create_hostgroup, hostgroup_name)
                        future.add_done_callback(partial(hostgroup_callback, hostgroup_name=hostgroup_name, index=idx))
                        futures.append(future)

                    # 等待所有任务完成
                    wait(futures)

                # 最终统计
                print(f"\n\n\033[1;36m=== 创建完成 ===\033[0m")
                print(f"总计: {total_tasks} 个主机组")
                print(f"成功: \033[32m{success_count}\033[0m")
                print(f"失败: \033[31m{failed_count}\033[0m")
                if failed_count > 0:
                    print("\033[33m请注意检查失败的主机组创建任务\033[0m")


            process_data()
        elif args.delete_hostgroup != 'delete_hostgroup':
            def process_data():
                # 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 1)
                column_1_list = cus_excel_op.get_column_values(1)
                del column_1_list[0]

                # 去重并保持原始顺序
                unit_column_1_list = sorted(set(column_1_list), key=column_1_list.index)
                total_groups = len(unit_column_1_list)

                # 进度统计
                completed_tasks = 0
                success_count = 0
                failed_count = 0


                # 第一阶段回调函数：获取主机组ID
                def get_callback(future, hostgroup_name, index):
                    nonlocal completed_tasks, success_count, failed_count
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            return lv_result['result'][0]['groupid']
                        else:
                            print(f"\r[{index + 1}/{total_groups}] 获取主机组ID: {hostgroup_name} \033[31m失败\033[0m 返回值: \033[31m{lv_result['result']}\033[0m")
                            return None
                    except Exception as e:
                        print(f"\r[{index + 1}/{total_groups}] 获取主机组ID: {hostgroup_name} \033[31m错误\033[0m: {str(e)}")
                        return None
                    finally:
                        completed_tasks += 1
                        progress = (completed_tasks / total_groups) * 100
                        print(f"\r总进度: {completed_tasks}/{total_groups} ({progress:.1f}%)", end="", flush=True)


                # 第二阶段回调函数：删除主机组
                def delete_callback(future, hostgroup_name, index):
                    nonlocal success_count, failed_count
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            success_count += 1
                            status = "\033[32m成功\033[0m"
                            result_msg = f"返回值: \033[32m{lv_result['result']}\033[0m"
                        else:
                            failed_count += 1
                            status = "\033[31m失败\033[0m"
                            result_msg = f"返回值: \033[31m{lv_result['result']}\033[0m"

                        print(f"\r[{index + 1}/{total_groups}] 删除主机组: {hostgroup_name} {status} {result_msg}")
                    except Exception as e:
                        failed_count += 1
                        print(f"\r[{index + 1}/{total_groups}] 删除主机组: {hostgroup_name} \033[31m错误\033[0m: {str(e)}")


                # 第一阶段：获取主机组ID
                print(f"\n\033[1;36m=== 开始获取主机组ID (共 {total_groups} 个) ===\033[0m")
                hostgroup_ids = []
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, hostgroup_name in enumerate(unit_column_1_list):
                        future = executor.submit(cus_zabbix_api.def_get_hostgroup_6_0, hostgroup_name)
                        future.add_done_callback(lambda f, name=hostgroup_name, i=idx:
                                                 hostgroup_ids.append((i, name, get_callback(f, name, i))))
                        futures.append(future)
                    wait(futures)

                # 筛选有效ID
                valid_hostgroup_ids = [x[2] for x in sorted(hostgroup_ids) if x[2] is not None]
                if not valid_hostgroup_ids:
                    print("\n\033[31m错误: 未获取到任何有效的主机组ID，终止操作\033[0m")
                    exit(1)

                # 第二阶段：删除主机组
                print(f"\n\033[1;36m=== 开始删除主机组 (共 {len(valid_hostgroup_ids)} 个) ===\033[0m")
                completed_tasks = 0
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, (_, hostgroup_name, groupid) in enumerate(sorted([x for x in hostgroup_ids if x[2] is not None])):
                        future = executor.submit(cus_zabbix_api.def_delete_hostgroup, [groupid])
                        future.add_done_callback(partial(delete_callback, hostgroup_name=hostgroup_name, index=idx))
                        futures.append(future)
                    wait(futures)

                # 最终统计
                print(f"\n\033[1;36m=== 操作完成 ===\033[0m")
                print(f"获取主机组ID: 总计 {total_groups} | 有效 {len(valid_hostgroup_ids)}")
                print(f"删除主机组: 成功 \033[32m{success_count}\033[0m | 失败 \033[31m{failed_count}\033[0m")
                if failed_count > 0:
                    print("\033[33m请注意检查失败的主机组删除任务\033[0m")


            process_data()
        # 在主处理逻辑中添加模板组创建和删除的处理代码
        # ![01_创建模板组]
        elif args.create_templategroup != 'create_templategroup':
            def process_data():
                # 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 58)
                column_1_list = cus_excel_op.get_column_values(1)
                del column_1_list[0]

                # 去重并保持原始顺序
                unit_column_1_list = sorted(set(column_1_list), key=column_1_list.index)
                total_tasks = len(unit_column_1_list)

                # 进度统计
                completed_tasks = 0
                success_count = 0
                failed_count = 0

                # 回调函数
                def templategroup_callback(future, templategroup_name, index):
                    nonlocal completed_tasks, success_count, failed_count
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            success_count += 1
                            status = "\033[32m✓\033[0m"
                            result_msg = f"返回值: \033[32m{lv_result['result']}\033[0m"
                        else:
                            failed_count += 1
                            status = "\033[31m✗\033[0m"
                            result_msg = f"返回值: \033[31m{lv_result['result']}\033[0m"

                        # 实时更新进度
                        completed_tasks += 1
                        progress = (completed_tasks / total_tasks) * 100

                        # 打印当前任务结果
                        print(f"\r[{index + 1}/{total_tasks}] 创建模板组: {templategroup_name} {status} {result_msg}")

                        # 打印汇总进度
                        print(f"\r总进度: {completed_tasks}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{success_count}\033[0m | "
                              f"失败: \033[31m{failed_count}\033[0m", end="", flush=True)

                    except Exception as e:
                        failed_count += 1
                        completed_tasks += 1
                        print(f"\r[{index + 1}/{total_tasks}] 创建模板组: {templategroup_name} \033[31m错误: {str(e)}\033[0m")

                # 使用线程池处理
                print(f"\n\033[1;36m=== 开始创建模板组 (共 {total_tasks} 个) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, templategroup_name in enumerate(unit_column_1_list):
                        future = executor.submit(cus_zabbix_api.def_create_template_group, templategroup_name)
                        future.add_done_callback(partial(templategroup_callback, templategroup_name=templategroup_name, index=idx))
                        futures.append(future)

                    # 等待所有任务完成
                    wait(futures)

                # 最终统计
                print(f"\n\n\033[1;36m=== 创建完成 ===\033[0m")
                print(f"总计: {total_tasks} 个模板组")
                print(f"成功: \033[32m{success_count}\033[0m")
                print(f"失败: \033[31m{failed_count}\033[0m")
                if failed_count > 0:
                    print("\033[33m请注意检查失败的模板组创建任务\033[0m")

            process_data()
        elif args.delete_templategroup != 'delete_templategroup':
            def process_data():
                # 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 58)
                column_1_list = cus_excel_op.get_column_values(1)
                del column_1_list[0]

                # 去重并保持原始顺序
                unit_column_1_list = sorted(set(column_1_list), key=column_1_list.index)
                total_groups = len(unit_column_1_list)

                # 进度统计
                completed_tasks = 0
                success_count = 0
                failed_count = 0

                # 第一阶段回调函数：获取模板组ID
                def get_callback(future, templategroup_name, index):
                    nonlocal completed_tasks, success_count, failed_count
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            return lv_result['result'][0]['groupid']
                        else:
                            print(f"\r[{index + 1}/{total_groups}] 获取模板组ID: {templategroup_name} \033[31m失败\033[0m 返回值: \033[31m{lv_result['result']}\033[0m")
                            return None
                    except Exception as e:
                        print(f"\r[{index + 1}/{total_groups}] 获取模板组ID: {templategroup_name} \033[31m错误\033[0m: {str(e)}")
                        return None
                    finally:
                        completed_tasks += 1
                        progress = (completed_tasks / total_groups) * 100
                        print(f"\r总进度: {completed_tasks}/{total_groups} ({progress:.1f}%)", end="", flush=True)

                # 第二阶段回调函数：删除模板组
                def delete_callback(future, templategroup_name, index):
                    nonlocal success_count, failed_count
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            success_count += 1
                            status = "\033[32m成功\033[0m"
                            result_msg = f"返回值: \033[32m{lv_result['result']}\033[0m"
                        else:
                            failed_count += 1
                            status = "\033[31m失败\033[0m"
                            result_msg = f"返回值: \033[31m{lv_result['result']}\033[0m"

                        print(f"\r[{index + 1}/{total_groups}] 删除模板组: {templategroup_name} {status} {result_msg}")
                    except Exception as e:
                        failed_count += 1
                        print(f"\r[{index + 1}/{total_groups}] 删除模板组: {templategroup_name} \033[31m错误\033[0m: {str(e)}")

                # 第一阶段：获取模板组ID
                print(f"\n\033[1;36m=== 开始获取模板组ID (共 {total_groups} 个) ===\033[0m")
                templategroup_ids = []
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, templategroup_name in enumerate(unit_column_1_list):
                        future = executor.submit(cus_zabbix_api.def_get_templategroup, templategroup_name)
                        future.add_done_callback(lambda f, name=templategroup_name, i=idx:
                                                 templategroup_ids.append((i, name, get_callback(f, name, i))))
                        futures.append(future)
                    wait(futures)

                # 筛选有效ID
                valid_templategroup_ids = [x[2] for x in sorted(templategroup_ids) if x[2] is not None]
                if not valid_templategroup_ids:
                    print("\n\033[31m错误: 未获取到任何有效的模板组ID，终止操作\033[0m")
                    exit(1)

                # 第二阶段：删除模板组
                print(f"\n\033[1;36m=== 开始删除模板组 (共 {len(valid_templategroup_ids)} 个) ===\033[0m")
                completed_tasks = 0
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, (_, templategroup_name, groupid) in enumerate(sorted([x for x in templategroup_ids if x[2] is not None])):
                        future = executor.submit(cus_zabbix_api.def_delete_template_group, [groupid])
                        future.add_done_callback(partial(delete_callback, templategroup_name=templategroup_name, index=idx))
                        futures.append(future)
                    wait(futures)

                # 最终统计
                print(f"\n\033[1;36m=== 操作完成 ===\033[0m")
                print(f"获取模板组ID: 总计 {total_groups} | 有效 {len(valid_templategroup_ids)}")
                print(f"删除模板组: 成功 \033[32m{success_count}\033[0m | 失败 \033[31m{failed_count}\033[0m")
                if failed_count > 0:
                    print("\033[33m请注意检查失败的模板组删除任务\033[0m")

            process_data()
        # ![02_创建模板]
        elif args.create_template != 'create_template':
            def process_data():
                # 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 2)
                column_1_list = cus_excel_op.get_column_values(1)  # 模板名称列
                column_2_list = cus_excel_op.get_column_values(2)  # 组名称列（主机组或模板组）
                del column_1_list[0]  # 删除标题行
                del column_2_list[0]  # 删除标题行

                total_tasks = len(column_1_list)

                # 进度统计
                get_success = 0
                get_failed = 0
                create_success = 0
                create_failed = 0

                # 版本适配字典
                lv_dic_zbx_version = {
                    '6.0': {
                        'hostgroup': cus_zabbix_api.def_get_hostgroup_6_0,
                        'templategroup': cus_zabbix_api.def_get_hostgroup_6_0  # 6.0没有模板组概念
                    },
                    '6.4': {
                        'hostgroup': cus_zabbix_api.def_get_hostgroup_6_4,
                        'templategroup': cus_zabbix_api.def_get_hostgroup_6_4  # 6.4没有模板组概念
                    },
                    '7.0': {
                        'hostgroup': cus_zabbix_api.def_get_hostgroup_6_4,
                        'templategroup': cus_zabbix_api.def_get_templategroup  # 7.0引入模板组
                    }
                }

                zbx_version = cus_zabbix_api.def_check_zbx_version()['result'][0:3]

                # 根据版本选择使用主机组还是模板组
                group_type = 'templategroup' if zbx_version == '7.0' else 'hostgroup'

                def progress_callback(task_index, total_tasks, item_name, result, operation_name):
                    """统一进度显示回调函数"""
                    status_color = '32' if result['tag'] else '31'
                    status_msg = '成功' if result['tag'] else '失败'
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> %s: \033[;%sm%s\033[0m %s 返回值为: \033[;%sm%s\033[0m' % (
                        total_tasks, task_index + 1, operation_name,
                        status_color, item_name, status_msg,
                        status_color, result['result']))

                # 第一阶段回调函数：获取组ID
                def get_group_callback(future, index, template_name, group_name):
                    nonlocal get_success, get_failed
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            get_success += 1
                            groupid = int(lv_result['result'][0]['groupid'])
                            status = "\033[32m✓\033[0m"
                            print(f"\r[{index + 1}/{total_tasks}] 获取{group_type}: {group_name} {status} ID: {groupid}")
                            return {"groupid": groupid}
                        else:
                            get_failed += 1
                            status = "\033[31m✗\033[0m"
                            print(f"\r[{index + 1}/{total_tasks}] 获取{group_type}: {group_name} {status} 错误: {lv_result['result']}")
                            return {"groupid": None}
                    except Exception as e:
                        get_failed += 1
                        print(f"\r[{index + 1}/{total_tasks}] 获取{group_type}: {group_name} \033[31m异常\033[0m: {str(e)}")
                        return {"groupid": None}
                    finally:
                        progress = ((get_success + get_failed) / total_tasks) * 100
                        print(f"\r获取进度: {get_success + get_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{get_success}\033[0m | 失败: \033[31m{get_failed}\033[0m", end="", flush=True)

                # 第二阶段回调函数：创建模板
                def create_template_callback(future, index, template_name):
                    nonlocal create_success, create_failed
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            create_success += 1
                            status = "\033[32m✓\033[0m"
                            result_msg = f"返回值: \033[32m{lv_result['result']}\033[0m"
                        else:
                            create_failed += 1
                            status = "\033[31m✗\033[0m"
                            result_msg = f"返回值: \033[31m{lv_result['result']}\033[0m"

                        print(f"\r[{index + 1}/{total_tasks}] 创建模板: {template_name} {status} {result_msg}")
                    except Exception as e:
                        create_failed += 1
                        print(f"\r[{index + 1}/{total_tasks}] 创建模板: {template_name} \033[31m异常\033[0m: {str(e)}")
                    finally:
                        progress = ((create_success + create_failed) / total_tasks) * 100
                        print(f"\r创建进度: {create_success + create_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{create_success}\033[0m | 失败: \033[31m{create_failed}\033[0m", end="", flush=True)

                # 第一阶段：获取组ID（根据Zabbix版本选择主机组或模板组）
                print(f"\n\033[1;36m=== 开始获取{group_type}ID (共 {total_tasks} 个) ===\033[0m")
                group_data = []

                if zbx_version in lv_dic_zbx_version:
                    # 获取组ID
                    with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                        futures = []
                        for idx, (template_name, group_name) in enumerate(zip(column_1_list, column_2_list)):
                            # 根据版本和组类型选择合适的方法
                            method = lv_dic_zbx_version[zbx_version][group_type]
                            future = executor.submit(method, group_name)
                            future.add_done_callback(lambda f, i=idx, tn=template_name, gn=group_name:
                                                     group_data.append((i, tn, gn, get_group_callback(f, i, tn, gn))))
                            futures.append(future)
                        wait(futures)

                    # 准备创建模板的数据
                    template_data = []
                    for item in sorted(group_data, key=lambda x: x[0]):  # 按索引排序
                        if item[3] is not None and item[3]['groupid'] is not None:  # 确保组ID有效
                            template_data.append((item[1], [item[3]]))  # (template_name, [{"groupid": ...}])

                    print(f"\n准备创建模板的数据: {template_data}")

                    # 第二阶段：创建模板
                    print(f"\n\033[1;36m=== 开始创建模板 (共 {len(template_data)} 个) ===\033[0m")
                    with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                        futures = []
                        for idx, (template_name, group_info) in enumerate(template_data):
                            if group_info[0]['groupid'] is not None:  # 只处理获取到有效组ID的
                                future = executor.submit(cus_zabbix_api.def_create_template, template_name, group_info)
                                future.add_done_callback(partial(create_template_callback, index=idx, template_name=template_name))
                                futures.append(future)
                            else:
                                create_failed += 1
                                print(f"\r[{idx + 1}/{len(template_data)}] 创建模板: {template_name} \033[31m跳过\033[0m (无效组ID)")
                        wait(futures)

                    # 最终统计
                    print(f"\n\n\033[1;36m=== 操作完成 ===\033[0m")
                    print(f"获取{group_type}ID: 成功 \033[32m{get_success}\033[0m | 失败 \033[31m{get_failed}\033[0m")
                    print(f"创建模板: 成功 \033[32m{create_success}\033[0m | 失败 \033[31m{create_failed}\033[0m")
                    if create_failed > 0:
                        print("\033[33m请注意检查失败的模板创建任务\033[0m")
                else:
                    print(f"\033[31m不支持的Zabbix版本: {zbx_version}\033[0m")


            process_data()
        elif args.delete_template != 'delete_template':
            def process_data():
                # 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 2)
                column_1_list = cus_excel_op.get_column_values(1)  # 模板名称列
                del column_1_list[0]  # 删除标题行

                total_templates = len(column_1_list)

                # 进度统计
                get_success = 0
                get_failed = 0
                delete_success = 0
                delete_failed = 0
                template_ids = []


                # 第一阶段回调函数：获取模板ID
                def get_template_callback(future, index, template_name):
                    nonlocal get_success, get_failed, template_ids
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            get_success += 1
                            template_id = result['result'][0]['templateid']
                            template_ids.append((index, template_name, template_id))
                            status = "\033[32m成功\033[0m"
                            msg = f"模板ID: {template_id}"
                        else:
                            get_failed += 1
                            template_ids.append((index, template_name, None))
                            status = "\033[31m失败\033[0m"
                            msg = f"错误: {result['result']}"

                        # 实时更新进度
                        progress = ((get_success + get_failed) / total_templates) * 100
                        print(f"\r[{index + 1}/{total_templates}] 获取模板: {template_name} {status} {msg}")
                        print(f"\r获取进度: {get_success + get_failed}/{total_templates} ({progress:.1f}%) | "
                              f"成功: \033[32m{get_success}\033[0m | 失败: \033[31m{get_failed}\033[0m", end="", flush=True)
                    except Exception as e:
                        get_failed += 1
                        template_ids.append((index, template_name, None))
                        print(f"\r[{index + 1}/{total_templates}] 获取模板: {template_name} \033[31m异常\033[0m: {str(e)}")


                # 第二阶段回调函数：删除模板
                def delete_template_callback(future, index, template_name):
                    nonlocal delete_success, delete_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            delete_success += 1
                            status = "\033[32m成功\033[0m"
                            msg = f"返回值: \033[32m{result['result']}\033[0m"
                        else:
                            delete_failed += 1
                            status = "\033[31m失败\033[0m"
                            msg = f"返回值: \033[31m{result['result']}\033[0m"

                        # 实时更新进度
                        progress = ((delete_success + delete_failed) / total_templates) * 100
                        print(f"\r[{index + 1}/{total_templates}] 删除模板: {template_name} {status} {msg}")
                        print(f"\r删除进度: {delete_success + delete_failed}/{total_templates} ({progress:.1f}%) | "
                              f"成功: \033[32m{delete_success}\033[0m | 失败: \033[31m{delete_failed}\033[0m", end="", flush=True)
                    except Exception as e:
                        delete_failed += 1
                        print(f"\r[{index + 1}/{total_templates}] 删除模板: {template_name} \033[31m异常\033[0m: {str(e)}")


                # 第一阶段：获取模板ID
                print(f"\n\033[1;36m=== 开始获取模板ID (共 {total_templates} 个) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, template_name in enumerate(column_1_list):
                        future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                        future.add_done_callback(partial(get_template_callback, index=idx, template_name=template_name))
                        futures.append(future)
                    wait(futures)

                # 准备删除模板的数据（只处理获取到有效ID的模板）
                valid_templates = [x for x in sorted(template_ids, key=lambda x: x[0]) if x[2] is not None]

                # 第二阶段：删除模板
                print(f"\n\033[1;36m=== 开始删除模板 (共 {len(valid_templates)} 个) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, (_, template_name, template_id) in enumerate(valid_templates):
                        future = executor.submit(cus_zabbix_api.def_delete_template, [template_id])
                        future.add_done_callback(partial(delete_template_callback, index=idx, template_name=template_name))
                        futures.append(future)
                    wait(futures)

                # 最终统计
                print(f"\n\n\033[1;36m=== 操作完成 ===\033[0m")
                print(f"获取模板ID: 成功 \033[32m{get_success}\033[0m | 失败 \033[31m{get_failed}\033[0m")
                print(f"删除模板: 成功 \033[32m{delete_success}\033[0m | 失败 \033[31m{delete_failed}\033[0m")
                if get_failed > 0 or delete_failed > 0:
                    print("\033[33m请注意检查失败的任务\033[0m")
            process_data()
        # ![02_模板添加主机组]
        elif args.massadd_template_groups != 'massadd_template_groups':
            def process_data():
                # 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 2)
                column_1_list = cus_excel_op.get_column_values(1)  # 模板名称列
                column_2_list = cus_excel_op.get_column_values(2)  # 主机组名称列
                del column_1_list[0]  # 删除标题行
                del column_2_list[0]  # 删除标题行

                total_tasks = len(column_1_list)

                # 进度统计
                template_get_success = 0
                template_get_failed = 0
                group_get_success = 0
                group_get_failed = 0
                add_success = 0
                add_failed = 0

                # 存储获取到的ID
                template_data = []
                group_data = []


                # 第一阶段回调函数：获取模板ID
                def get_template_callback(future, index, template_name):
                    nonlocal template_get_success, template_get_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            template_get_success += 1
                            template_id = result['result'][0]['templateid']
                            template_data.append((index, template_name, template_id))
                            status = "\033[32m成功\033[0m"
                            msg = f"模板ID: {template_id}"
                        else:
                            template_get_failed += 1
                            template_data.append((index, template_name, None))
                            status = "\033[31m失败\033[0m"
                            msg = f"错误: {result['result']}"

                        progress = ((template_get_success + template_get_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 获取模板: {template_name} {status} {msg}")
                        print(f"\r模板获取进度: {template_get_success + template_get_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{template_get_success}\033[0m | 失败: \033[31m{template_get_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        template_get_failed += 1
                        template_data.append((index, template_name, None))
                        print(f"\r[{index + 1}/{total_tasks}] 获取模板: {template_name} \033[31m异常\033[0m: {str(e)}")


                # 第二阶段回调函数：获取主机组ID
                def get_group_callback(future, index, group_name):
                    nonlocal group_get_success, group_get_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            group_get_success += 1
                            group_id = result['result'][0]['groupid']
                            group_data.append((index, group_name, group_id))
                            status = "\033[32m成功\033[0m"
                            msg = f"主机组ID: {group_id}"
                        else:
                            group_get_failed += 1
                            group_data.append((index, group_name, None))
                            status = "\033[31m失败\033[0m"
                            msg = f"错误: {result['result']}"

                        progress = ((group_get_success + group_get_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 获取主机组: {group_name} {status} {msg}")
                        print(f"\r主机组获取进度: {group_get_success + group_get_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{group_get_success}\033[0m | 失败: \033[31m{group_get_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        group_get_failed += 1
                        group_data.append((index, group_name, None))
                        print(f"\r[{index + 1}/{total_tasks}] 获取主机组: {group_name} \033[31m异常\033[0m: {str(e)}")


                # 第三阶段回调函数：添加主机组到模板
                def add_group_callback(future, index, template_name, group_name):
                    nonlocal add_success, add_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            add_success += 1
                            status = "\033[32m成功\033[0m"
                            msg = f"返回值: \033[32m{result['result']}\033[0m"
                        else:
                            add_failed += 1
                            status = "\033[31m失败\033[0m"
                            msg = f"返回值: \033[31m{result['result']}\033[0m"

                        progress = ((add_success + add_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 添加主机组: {template_name} <- {group_name} {status} {msg}")
                        print(f"\r添加进度: {add_success + add_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{add_success}\033[0m | 失败: \033[31m{add_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        add_failed += 1
                        print(f"\r[{index + 1}/{total_tasks}] 添加主机组: {template_name} <- {group_name} \033[31m异常\033[0m: {str(e)}")


                # 第一阶段：获取模板ID
                print(f"\n\033[1;36m=== 开始获取模板ID (共 {total_tasks} 个) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, template_name in enumerate(column_1_list):
                        future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                        future.add_done_callback(partial(get_template_callback, index=idx, template_name=template_name))
                        futures.append(future)
                    wait(futures)

                # 第二阶段：获取主机组ID
                print(f"\n\033[1;36m=== 开始获取主机组ID (共 {total_tasks} 个) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, group_name in enumerate(column_2_list):
                        future = executor.submit(cus_zabbix_api.def_get_hostgroup_6_0, group_name)
                        future.add_done_callback(partial(get_group_callback, index=idx, group_name=group_name))
                        futures.append(future)
                    wait(futures)

                # 准备关联数据（只处理两者都获取成功的）
                valid_pairs = []
                template_dict = {idx: (name, tid) for idx, name, tid in sorted(template_data, key=lambda x: x[0])}
                group_dict = {idx: (name, gid) for idx, name, gid in sorted(group_data, key=lambda x: x[0])}

                for idx in range(total_tasks):
                    template_name, template_id = template_dict.get(idx, (None, None))
                    group_name, group_id = group_dict.get(idx, (None, None))
                    if template_id and group_id:
                        valid_pairs.append((idx, template_name, template_id, group_name, group_id))
                    else:
                        print(f"\r[{idx + 1}/{total_tasks}] 跳过: {template_name or '未知模板'} <- {group_name or '未知主机组'} (缺少ID)")

                # 第三阶段：添加主机组到模板
                print(f"\n\033[1;36m=== 开始添加主机组到模板 (共 {len(valid_pairs)} 个有效组合) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, template_name, template_id, group_name, group_id in valid_pairs:
                        future = executor.submit(
                            cus_zabbix_api.def_massadd_template_groups,
                            [{'templateid': template_id}],
                            [{'groupid': group_id}]
                        )
                        future.add_done_callback(partial(
                            add_group_callback,
                            index=idx,
                            template_name=template_name,
                            group_name=group_name
                        ))
                        futures.append(future)
                    wait(futures)

                # 最终统计
                print(f"\n\n\033[1;36m=== 操作完成 ===\033[0m")
                print(f"获取模板ID: 成功 \033[32m{template_get_success}\033[0m | 失败 \033[31m{template_get_failed}\033[0m")
                print(f"获取主机组ID: 成功 \033[32m{group_get_success}\033[0m | 失败 \033[31m{group_get_failed}\033[0m")
                print(f"添加主机组到模板: 成功 \033[32m{add_success}\033[0m | 失败 \033[31m{add_failed}\033[0m")
                if template_get_failed > 0 or group_get_failed > 0 or add_failed > 0:
                    print("\033[33m请注意检查失败的任务\033[0m")
            process_data()
        elif args.massremove_template_groups != 'massremove_template_groups':
            def process_data():
                # 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 2)
                column_1_list = cus_excel_op.get_column_values(1)  # 模板名称列
                column_2_list = cus_excel_op.get_column_values(2)  # 主机组名称列
                del column_1_list[0]  # 删除标题行
                del column_2_list[0]  # 删除标题行

                total_tasks = len(column_1_list)

                # 进度统计
                template_get_success = 0
                template_get_failed = 0
                group_get_success = 0
                group_get_failed = 0
                remove_success = 0
                remove_failed = 0

                # 存储获取到的ID
                template_data = []
                group_data = []


                # 第一阶段回调函数：获取模板ID
                def get_template_callback(future, index, template_name):
                    nonlocal template_get_success, template_get_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            template_get_success += 1
                            template_id = result['result'][0]['templateid']
                            template_data.append((index, template_name, template_id))
                            status = "\033[32m成功\033[0m"
                            msg = f"模板ID: {template_id}"
                        else:
                            template_get_failed += 1
                            template_data.append((index, template_name, None))
                            status = "\033[31m失败\033[0m"
                            msg = f"错误: {result['result']}"

                        progress = ((template_get_success + template_get_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 获取模板: {template_name} {status} {msg}")
                        print(f"\r模板获取进度: {template_get_success + template_get_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{template_get_success}\033[0m | 失败: \033[31m{template_get_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        template_get_failed += 1
                        template_data.append((index, template_name, None))
                        print(f"\r[{index + 1}/{total_tasks}] 获取模板: {template_name} \033[31m异常\033[0m: {str(e)}")


                # 第二阶段回调函数：获取主机组ID
                def get_group_callback(future, index, group_name):
                    nonlocal group_get_success, group_get_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            group_get_success += 1
                            group_id = result['result'][0]['groupid']
                            group_data.append((index, group_name, group_id))
                            status = "\033[32m成功\033[0m"
                            msg = f"主机组ID: {group_id}"
                        else:
                            group_get_failed += 1
                            group_data.append((index, group_name, None))
                            status = "\033[31m失败\033[0m"
                            msg = f"错误: {result['result']}"

                        progress = ((group_get_success + group_get_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 获取主机组: {group_name} {status} {msg}")
                        print(f"\r主机组获取进度: {group_get_success + group_get_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{group_get_success}\033[0m | 失败: \033[31m{group_get_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        group_get_failed += 1
                        group_data.append((index, group_name, None))
                        print(f"\r[{index + 1}/{total_tasks}] 获取主机组: {group_name} \033[31m异常\033[0m: {str(e)}")


                # 第三阶段回调函数：从模板移除主机组
                def remove_group_callback(future, index, template_name, group_name):
                    nonlocal remove_success, remove_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            remove_success += 1
                            status = "\033[32m成功\033[0m"
                            msg = f"返回值: \033[32m{result['result']}\033[0m"
                        else:
                            remove_failed += 1
                            status = "\033[31m失败\033[0m"
                            msg = f"返回值: \033[31m{result['result']}\033[0m"

                        progress = ((remove_success + remove_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 移除主机组: {template_name} <- {group_name} {status} {msg}")
                        print(f"\r移除进度: {remove_success + remove_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{remove_success}\033[0m | 失败: \033[31m{remove_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        remove_failed += 1
                        print(f"\r[{index + 1}/{total_tasks}] 移除主机组: {template_name} <- {group_name} \033[31m异常\033[0m: {str(e)}")


                # 第一阶段：获取模板ID
                print(f"\n\033[1;36m=== 开始获取模板ID (共 {total_tasks} 个) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, template_name in enumerate(column_1_list):
                        future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                        future.add_done_callback(partial(get_template_callback, index=idx, template_name=template_name))
                        futures.append(future)
                    wait(futures)

                # 第二阶段：获取主机组ID
                print(f"\n\033[1;36m=== 开始获取主机组ID (共 {total_tasks} 个) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, group_name in enumerate(column_2_list):
                        future = executor.submit(cus_zabbix_api.def_get_hostgroup_6_0, group_name)
                        future.add_done_callback(partial(get_group_callback, index=idx, group_name=group_name))
                        futures.append(future)
                    wait(futures)

                # 准备关联数据（只处理两者都获取成功的）
                valid_pairs = []
                template_dict = {idx: (name, tid) for idx, name, tid in sorted(template_data, key=lambda x: x[0])}
                group_dict = {idx: (name, gid) for idx, name, gid in sorted(group_data, key=lambda x: x[0])}

                for idx in range(total_tasks):
                    template_name, template_id = template_dict.get(idx, (None, None))
                    group_name, group_id = group_dict.get(idx, (None, None))
                    if template_id and group_id:
                        valid_pairs.append((idx, template_name, template_id, group_name, group_id))
                    else:
                        print(f"\r[{idx + 1}/{total_tasks}] 跳过: {template_name or '未知模板'} <- {group_name or '未知主机组'} (缺少ID)")

                # 第三阶段：从模板移除主机组（限制并发数为1）
                print(f"\n\033[1;36m=== 开始从模板移除主机组 (共 {len(valid_pairs)} 个有效组合，单线程执行) ===\033[0m")
                with ThreadPoolExecutor(max_workers=1) as executor:  # 保持原代码的单线程设置
                    futures = []
                    for idx, template_name, template_id, group_name, group_id in valid_pairs:
                        future = executor.submit(
                            cus_zabbix_api.def_massremove_template_groups,
                            [template_id],
                            [group_id]
                        )
                        future.add_done_callback(partial(
                            remove_group_callback,
                            index=idx,
                            template_name=template_name,
                            group_name=group_name
                        ))
                        futures.append(future)
                    wait(futures)

                # 最终统计
                print(f"\n\n\033[1;36m=== 操作完成 ===\033[0m")
                print(f"获取模板ID: 成功 \033[32m{template_get_success}\033[0m | 失败 \033[31m{template_get_failed}\033[0m")
                print(f"获取主机组ID: 成功 \033[32m{group_get_success}\033[0m | 失败 \033[31m{group_get_failed}\033[0m")
                print(f"移除主机组: 成功 \033[32m{remove_success}\033[0m | 失败 \033[31m{remove_failed}\033[0m")
                if template_get_failed > 0 or group_get_failed > 0 or remove_failed > 0:
                    print("\033[33m请注意检查失败的任务\033[0m")
            process_data()
        # ![03_模板添加用户宏]
        elif args.massadd_template_macros != 'massadd_template_macros':
            def process_data():
                # 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 3)
                column_1_list = cus_excel_op.get_column_values(1)  # 模板名称列
                column_2_list = cus_excel_op.get_column_values(2)  # 宏名称列
                column_3_list = cus_excel_op.get_column_values(3)  # 宏值列
                del column_1_list[0]  # 删除标题行
                del column_2_list[0]  # 删除标题行
                del column_3_list[0]  # 删除标题行

                total_tasks = len(column_1_list)

                # 进度统计
                template_get_success = 0
                template_get_failed = 0
                macro_add_success = 0
                macro_add_failed = 0

                # 存储获取到的模板ID和宏数据
                template_data = []
                macro_data = []


                # 第一阶段回调函数：获取模板ID
                def get_template_callback(future, index, template_name):
                    nonlocal template_get_success, template_get_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            template_get_success += 1
                            template_id = result['result'][0]['templateid']
                            template_data.append((index, template_name, template_id))
                            status = "\033[32m成功\033[0m"
                            msg = f"模板ID: {template_id}"
                        else:
                            template_get_failed += 1
                            template_data.append((index, template_name, None))
                            status = "\033[31m失败\033[0m"
                            msg = f"错误: {result['result']}"

                        progress = ((template_get_success + template_get_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 获取模板: {template_name} {status} {msg}")
                        print(f"\r模板获取进度: {template_get_success + template_get_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{template_get_success}\033[0m | 失败: \033[31m{template_get_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        template_get_failed += 1
                        template_data.append((index, template_name, None))
                        print(f"\r[{index + 1}/{total_tasks}] 获取模板: {template_name} \033[31m异常\033[0m: {str(e)}")


                # 第二阶段回调函数：添加宏到模板
                def add_macro_callback(future, index, template_name, macro_name):
                    nonlocal macro_add_success, macro_add_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            macro_add_success += 1
                            status = "\033[32m成功\033[0m"
                            msg = f"返回值: \033[32m{result['result']}\033[0m"
                        else:
                            macro_add_failed += 1
                            status = "\033[31m失败\033[0m"
                            msg = f"返回值: \033[31m{result['result']}\033[0m"

                        progress = ((macro_add_success + macro_add_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 添加宏: {template_name} -> {macro_name} {status} {msg}")
                        print(f"\r宏添加进度: {macro_add_success + macro_add_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{macro_add_success}\033[0m | 失败: \033[31m{macro_add_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        macro_add_failed += 1
                        print(f"\r[{index + 1}/{total_tasks}] 添加宏: {template_name} -> {macro_name} \033[31m异常\033[0m: {str(e)}")


                # 第一阶段：获取模板ID
                print(f"\n\033[1;36m=== 开始获取模板ID (共 {total_tasks} 个) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, template_name in enumerate(column_1_list):
                        future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                        future.add_done_callback(partial(get_template_callback, index=idx, template_name=template_name))
                        futures.append(future)
                    wait(futures)

                # 准备宏数据
                macro_data = []
                for idx in range(total_tasks):
                    macro_name = column_2_list[idx]
                    macro_value = str(column_3_list[idx])
                    macro_data.append([{"macro": macro_name, "value": macro_value}])

                # 第二阶段：添加宏到模板（只处理获取到有效模板ID的）
                print(f"\n\033[1;36m=== 开始添加宏到模板 (共 {len([x for x in template_data if x[2] is not None])} 个有效模板) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, (_, template_name, template_id) in enumerate(sorted(template_data, key=lambda x: x[0])):
                        if template_id is not None:
                            future = executor.submit(
                                cus_zabbix_api.def_massadd_template_macros,
                                [{"templateid": template_id}],
                                macro_data[idx]
                            )
                            future.add_done_callback(partial(
                                add_macro_callback,
                                index=idx,
                                template_name=template_name,
                                macro_name=column_2_list[idx]
                            ))
                            futures.append(future)
                        else:
                            print(f"\r[{idx + 1}/{total_tasks}] 跳过: {template_name} (无效模板ID)")
                    wait(futures)

                # 最终统计
                print(f"\n\n\033[1;36m=== 操作完成 ===\033[0m")
                print(f"获取模板ID: 成功 \033[32m{template_get_success}\033[0m | 失败 \033[31m{template_get_failed}\033[0m")
                print(f"添加宏: 成功 \033[32m{macro_add_success}\033[0m | 失败 \033[31m{macro_add_failed}\033[0m")
                if template_get_failed > 0 or macro_add_failed > 0:
                    print("\033[33m请注意检查失败的任务\033[0m")
            process_data()
        elif args.massremove_template_macros != 'massremove_template_macros':
            def process_data():
                # 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 3)
                column_1_list = cus_excel_op.get_column_values(1)  # 模板名称列
                column_2_list = cus_excel_op.get_column_values(2)  # 宏名称列
                del column_1_list[0]  # 删除标题行
                del column_2_list[0]  # 删除标题行

                total_tasks = len(column_1_list)

                # 进度统计
                template_get_success = 0
                template_get_failed = 0
                macro_remove_success = 0
                macro_remove_failed = 0

                # 存储获取到的模板ID和宏数据
                template_data = []
                macro_data = []


                # 第一阶段回调函数：获取模板ID
                def get_template_callback(future, index, template_name):
                    nonlocal template_get_success, template_get_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            template_get_success += 1
                            template_id = result['result'][0]['templateid']
                            template_data.append((index, template_name, template_id))
                            status = "\033[32m成功\033[0m"
                            msg = f"模板ID: {template_id}"
                        else:
                            template_get_failed += 1
                            template_data.append((index, template_name, None))
                            status = "\033[31m失败\033[0m"
                            msg = f"错误: {result['result']}"

                        progress = ((template_get_success + template_get_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 获取模板: {template_name} {status} {msg}")
                        print(f"\r模板获取进度: {template_get_success + template_get_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{template_get_success}\033[0m | 失败: \033[31m{template_get_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        template_get_failed += 1
                        template_data.append((index, template_name, None))
                        print(f"\r[{index + 1}/{total_tasks}] 获取模板: {template_name} \033[31m异常\033[0m: {str(e)}")


                # 第二阶段回调函数：从模板删除宏
                def remove_macro_callback(future, index, template_name, macro_name):
                    nonlocal macro_remove_success, macro_remove_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            macro_remove_success += 1
                            status = "\033[32m成功\033[0m"
                            msg = f"返回值: \033[32m{result['result']}\033[0m"
                        else:
                            macro_remove_failed += 1
                            status = "\033[31m失败\033[0m"
                            msg = f"返回值: \033[31m{result['result']}\033[0m"

                        progress = ((macro_remove_success + macro_remove_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 删除宏: {template_name} -> {macro_name} {status} {msg}")
                        print(f"\r宏删除进度: {macro_remove_success + macro_remove_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{macro_remove_success}\033[0m | 失败: \033[31m{macro_remove_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        macro_remove_failed += 1
                        print(f"\r[{index + 1}/{total_tasks}] 删除宏: {template_name} -> {macro_name} \033[31m异常\033[0m: {str(e)}")


                # 第一阶段：获取模板ID
                print(f"\n\033[1;36m=== 开始获取模板ID (共 {total_tasks} 个) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, template_name in enumerate(column_1_list):
                        future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                        future.add_done_callback(partial(get_template_callback, index=idx, template_name=template_name))
                        futures.append(future)
                    wait(futures)

                # 准备宏数据（保持原代码的单线程设置）
                print(f"\n\033[1;36m=== 准备宏数据 (共 {total_tasks} 个) ===\033[0m")
                macro_data = []
                for idx in range(total_tasks):
                    macro_name = cus_excel_op.get_cell_value(idx + 2, 2)
                    macro_data.append([macro_name])
                    progress = ((idx + 1) / total_tasks) * 100
                    print(f"\r[{idx + 1}/{total_tasks}] 准备宏: {macro_name}")
                    print(f"\r宏准备进度: {idx + 1}/{total_tasks} ({progress:.1f}%)", end="", flush=True)

                # 第二阶段：从模板删除宏（保持原代码的单线程设置）
                print(f"\n\033[1;36m=== 开始从模板删除宏 (共 {len([x for x in template_data if x[2] is not None])} 个有效模板，单线程执行) ===\033[0m")
                with ThreadPoolExecutor(max_workers=1) as executor:  # 保持原代码的单线程设置
                    futures = []
                    for idx, (_, template_name, template_id) in enumerate(sorted(template_data, key=lambda x: x[0])):
                        if template_id is not None:
                            future = executor.submit(
                                cus_zabbix_api.def_massremove_template_macros,
                                [template_id],
                                macro_data[idx]
                            )
                            future.add_done_callback(partial(
                                remove_macro_callback,
                                index=idx,
                                template_name=template_name,
                                macro_name=macro_data[idx][0]
                            ))
                            futures.append(future)
                        else:
                            print(f"\r[{idx + 1}/{total_tasks}] 跳过: {template_name} (无效模板ID)")
                    wait(futures)

                # 最终统计
                print(f"\n\n\033[1;36m=== 操作完成 ===\033[0m")
                print(f"获取模板ID: 成功 \033[32m{template_get_success}\033[0m | 失败 \033[31m{template_get_failed}\033[0m")
                print(f"删除宏: 成功 \033[32m{macro_remove_success}\033[0m | 失败 \033[31m{macro_remove_failed}\033[0m")
                if template_get_failed > 0 or macro_remove_failed > 0:
                    print("\033[33m请注意检查失败的任务\033[0m")
            process_data()
        # ![04_模板关联模板]
        elif args.massadd_template_templates_link != 'massadd_template_templates_link':
            def process_data():
                # 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 4)
                column_1_list = cus_excel_op.get_column_values(1)  # 主模板名称列
                column_2_list = cus_excel_op.get_column_values(2)  # 链接模板名称列
                del column_1_list[0]  # 删除标题行
                del column_2_list[0]  # 删除标题行

                total_tasks = len(column_1_list)

                # 进度统计
                main_template_success = 0
                main_template_failed = 0
                link_template_success = 0
                link_template_failed = 0
                link_operation_success = 0
                link_operation_failed = 0

                # 存储获取到的模板ID
                main_template_data = []
                link_template_data = []


                # 第一阶段回调函数：获取主模板ID
                def get_main_template_callback(future, index, template_name):
                    nonlocal main_template_success, main_template_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            main_template_success += 1
                            template_id = result['result'][0]['templateid']
                            main_template_data.append((index, template_name, template_id))
                            status = "\033[32m成功\033[0m"
                            msg = f"模板ID: {template_id}"
                        else:
                            main_template_failed += 1
                            main_template_data.append((index, template_name, None))
                            status = "\033[31m失败\033[0m"
                            msg = f"错误: {result['result']}"

                        progress = ((main_template_success + main_template_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 获取主模板: {template_name} {status} {msg}")
                        print(f"\r主模板获取进度: {main_template_success + main_template_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{main_template_success}\033[0m | 失败: \033[31m{main_template_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        main_template_failed += 1
                        main_template_data.append((index, template_name, None))
                        print(f"\r[{index + 1}/{total_tasks}] 获取主模板: {template_name} \033[31m异常\033[0m: {str(e)}")


                # 第二阶段回调函数：获取链接模板ID
                def get_link_template_callback(future, index, template_name):
                    nonlocal link_template_success, link_template_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            link_template_success += 1
                            template_id = result['result'][0]['templateid']
                            link_template_data.append((index, template_name, template_id))
                            status = "\033[32m成功\033[0m"
                            msg = f"模板ID: {template_id}"
                        else:
                            link_template_failed += 1
                            link_template_data.append((index, template_name, None))
                            status = "\033[31m失败\033[0m"
                            msg = f"错误: {result['result']}"

                        progress = ((link_template_success + link_template_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 获取链接模板: {template_name} {status} {msg}")
                        print(f"\r链接模板获取进度: {link_template_success + link_template_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{link_template_success}\033[0m | 失败: \033[31m{link_template_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        link_template_failed += 1
                        link_template_data.append((index, template_name, None))
                        print(f"\r[{index + 1}/{total_tasks}] 获取链接模板: {template_name} \033[31m异常\033[0m: {str(e)}")


                # 第三阶段回调函数：模板关联操作
                def link_template_callback(future, index, main_template_name, link_template_name):
                    nonlocal link_operation_success, link_operation_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            link_operation_success += 1
                            status = "\033[32m成功\033[0m"
                            msg = f"返回值: \033[32m{result['result']}\033[0m"
                        else:
                            link_operation_failed += 1
                            status = "\033[31m失败\033[0m"
                            msg = f"返回值: \033[31m{result['result']}\033[0m"

                        progress = ((link_operation_success + link_operation_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 关联模板: {main_template_name} <- {link_template_name} {status} {msg}")
                        print(f"\r关联进度: {link_operation_success + link_operation_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{link_operation_success}\033[0m | 失败: \033[31m{link_operation_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        link_operation_failed += 1
                        print(f"\r[{index + 1}/{total_tasks}] 关联模板: {main_template_name} <- {link_template_name} \033[31m异常\033[0m: {str(e)}")


                # 第一阶段：获取主模板ID
                print(f"\n\033[1;36m=== 开始获取主模板ID (共 {total_tasks} 个) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, template_name in enumerate(column_1_list):
                        future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                        future.add_done_callback(partial(get_main_template_callback, index=idx, template_name=template_name))
                        futures.append(future)
                    wait(futures)

                # 第二阶段：获取链接模板ID
                print(f"\n\033[1;36m=== 开始获取链接模板ID (共 {total_tasks} 个) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, template_name in enumerate(column_2_list):
                        future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                        future.add_done_callback(partial(get_link_template_callback, index=idx, template_name=template_name))
                        futures.append(future)
                    wait(futures)

                # 准备关联数据（只处理两者都获取成功的）
                valid_pairs = []
                main_dict = {idx: (name, tid) for idx, name, tid in sorted(main_template_data, key=lambda x: x[0])}
                link_dict = {idx: (name, tid) for idx, name, tid in sorted(link_template_data, key=lambda x: x[0])}

                for idx in range(total_tasks):
                    main_name, main_id = main_dict.get(idx, (None, None))
                    link_name, link_id = link_dict.get(idx, (None, None))
                    if main_id and link_id:
                        valid_pairs.append((idx, main_name, main_id, link_name, link_id))
                    else:
                        print(f"\r[{idx + 1}/{total_tasks}] 跳过: {main_name or '未知模板'} <- {link_name or '未知模板'} (缺少ID)")

                # 第三阶段：执行模板关联
                print(f"\n\033[1;36m=== 开始模板关联操作 (共 {len(valid_pairs)} 个有效组合) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, main_name, main_id, link_name, link_id in valid_pairs:
                        future = executor.submit(
                            cus_zabbix_api.def_massadd_template_templates_link,
                            [{'templateid': main_id}],
                            [{'templateid': link_id}]
                        )
                        future.add_done_callback(partial(
                            link_template_callback,
                            index=idx,
                            main_template_name=main_name,
                            link_template_name=link_name
                        ))
                        futures.append(future)
                    wait(futures)

                # 最终统计
                print(f"\n\n\033[1;36m=== 操作完成 ===\033[0m")
                print(f"获取主模板ID: 成功 \033[32m{main_template_success}\033[0m | 失败 \033[31m{main_template_failed}\033[0m")
                print(f"获取链接模板ID: 成功 \033[32m{link_template_success}\033[0m | 失败 \033[31m{link_template_failed}\033[0m")
                print(f"模板关联操作: 成功 \033[32m{link_operation_success}\033[0m | 失败 \033[31m{link_operation_failed}\033[0m")
                if main_template_failed > 0 or link_template_failed > 0 or link_operation_failed > 0:
                    print("\033[33m请注意检查失败的任务\033[0m")
            process_data()
        elif args.massremove_templateids_clear != 'massremove_templateids_clear':
            def process_data():
                # 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 4)
                column_1_list = cus_excel_op.get_column_values(1)  # 主模板名称列
                column_2_list = cus_excel_op.get_column_values(2)  # 链接模板名称列
                del column_1_list[0]  # 删除标题行
                del column_2_list[0]  # 删除标题行

                total_tasks = len(column_1_list)

                # 进度统计
                main_template_success = 0
                main_template_failed = 0
                link_template_success = 0
                link_template_failed = 0
                unlink_success = 0
                unlink_failed = 0

                # 存储获取到的模板ID
                main_template_data = []
                link_template_data = []


                # 第一阶段回调函数：获取主模板ID
                def get_main_template_callback(future, index, template_name):
                    nonlocal main_template_success, main_template_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            main_template_success += 1
                            template_id = result['result'][0]['templateid']
                            main_template_data.append((index, template_name, template_id))
                            status = "\033[32m成功\033[0m"
                            msg = f"模板ID: {template_id}"
                        else:
                            main_template_failed += 1
                            main_template_data.append((index, template_name, None))
                            status = "\033[31m失败\033[0m"
                            msg = f"错误: {result['result']}"

                        progress = ((main_template_success + main_template_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 获取主模板: {template_name} {status} {msg}")
                        print(f"\r主模板获取进度: {main_template_success + main_template_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{main_template_success}\033[0m | 失败: \033[31m{main_template_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        main_template_failed += 1
                        main_template_data.append((index, template_name, None))
                        print(f"\r[{index + 1}/{total_tasks}] 获取主模板: {template_name} \033[31m异常\033[0m: {str(e)}")


                # 第二阶段回调函数：获取链接模板ID
                def get_link_template_callback(future, index, template_name):
                    nonlocal link_template_success, link_template_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            link_template_success += 1
                            template_id = result['result'][0]['templateid']
                            link_template_data.append((index, template_name, template_id))
                            status = "\033[32m成功\033[0m"
                            msg = f"模板ID: {template_id}"
                        else:
                            link_template_failed += 1
                            link_template_data.append((index, template_name, None))
                            status = "\033[31m失败\033[0m"
                            msg = f"错误: {result['result']}"

                        progress = ((link_template_success + link_template_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 获取链接模板: {template_name} {status} {msg}")
                        print(f"\r链接模板获取进度: {link_template_success + link_template_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{link_template_success}\033[0m | 失败: \033[31m{link_template_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        link_template_failed += 1
                        link_template_data.append((index, template_name, None))
                        print(f"\r[{index + 1}/{total_tasks}] 获取链接模板: {template_name} \033[31m异常\033[0m: {str(e)}")


                # 第三阶段回调函数：模板脱离操作
                def unlink_template_callback(future, index, main_template_name, link_template_name):
                    nonlocal unlink_success, unlink_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            unlink_success += 1
                            status = "\033[32m成功\033[0m"
                            msg = f"返回值: \033[32m{result['result']}\033[0m"
                        else:
                            unlink_failed += 1
                            status = "\033[31m失败\033[0m"
                            msg = f"返回值: \033[31m{result['result']}\033[0m"

                        progress = ((unlink_success + unlink_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 脱离模板: {main_template_name} <- {link_template_name} {status} {msg}")
                        print(f"\r脱离进度: {unlink_success + unlink_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{unlink_success}\033[0m | 失败: \033[31m{unlink_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        unlink_failed += 1
                        print(f"\r[{index + 1}/{total_tasks}] 脱离模板: {main_template_name} <- {link_template_name} \033[31m异常\033[0m: {str(e)}")


                # 第一阶段：获取主模板ID
                print(f"\n\033[1;36m=== 开始获取主模板ID (共 {total_tasks} 个) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, template_name in enumerate(column_1_list):
                        future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                        future.add_done_callback(partial(get_main_template_callback, index=idx, template_name=template_name))
                        futures.append(future)
                    wait(futures)

                # 第二阶段：获取链接模板ID
                print(f"\n\033[1;36m=== 开始获取链接模板ID (共 {total_tasks} 个) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, template_name in enumerate(column_2_list):
                        future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                        future.add_done_callback(partial(get_link_template_callback, index=idx, template_name=template_name))
                        futures.append(future)
                    wait(futures)

                # 准备关联数据（只处理两者都获取成功的）
                valid_pairs = []
                main_dict = {idx: (name, tid) for idx, name, tid in sorted(main_template_data, key=lambda x: x[0])}
                link_dict = {idx: (name, tid) for idx, name, tid in sorted(link_template_data, key=lambda x: x[0])}

                for idx in range(total_tasks):
                    main_name, main_id = main_dict.get(idx, (None, None))
                    link_name, link_id = link_dict.get(idx, (None, None))
                    if main_id and link_id:
                        valid_pairs.append((idx, main_name, main_id, link_name, link_id))
                    else:
                        print(f"\r[{idx + 1}/{total_tasks}] 跳过: {main_name or '未知模板'} <- {link_name or '未知模板'} (缺少ID)")

                # 第三阶段：执行模板脱离操作（保持原代码的单线程设置）
                print(f"\n\033[1;36m=== 开始模板脱离操作 (共 {len(valid_pairs)} 个有效组合，单线程执行) ===\033[0m")
                with ThreadPoolExecutor(max_workers=1) as executor:
                    futures = []
                    for idx, main_name, main_id, link_name, link_id in valid_pairs:
                        future = executor.submit(
                            cus_zabbix_api.def_massremove_templateids_clear,
                            [main_id],
                            [link_id]
                        )
                        future.add_done_callback(partial(
                            unlink_template_callback,
                            index=idx,
                            main_template_name=main_name,
                            link_template_name=link_name
                        ))
                        futures.append(future)
                    wait(futures)

                # 最终统计
                print(f"\n\n\033[1;36m=== 操作完成 ===\033[0m")
                print(f"获取主模板ID: 成功 \033[32m{main_template_success}\033[0m | 失败 \033[31m{main_template_failed}\033[0m")
                print(f"获取链接模板ID: 成功 \033[32m{link_template_success}\033[0m | 失败 \033[31m{link_template_failed}\033[0m")
                print(f"模板脱离操作: 成功 \033[32m{unlink_success}\033[0m | 失败 \033[31m{unlink_failed}\033[0m")
                if main_template_failed > 0 or link_template_failed > 0 or unlink_failed > 0:
                    print("\033[33m请注意检查失败的任务\033[0m")

            process_data()
        elif args.massremove_templateids_link != 'massremove_templateids_link':
            def process_data():
                # 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 4)
                column_1_list = cus_excel_op.get_column_values(1)  # 主模板名称列
                column_2_list = cus_excel_op.get_column_values(2)  # 链接模板名称列
                del column_1_list[0]  # 删除标题行
                del column_2_list[0]  # 删除标题行

                total_tasks = len(column_1_list)

                # 进度统计
                template_get_success = 0
                template_get_failed = 0
                link_template_success = 0
                link_template_failed = 0
                unlink_success = 0
                unlink_failed = 0

                # 存储获取到的模板ID
                main_template_data = []
                link_template_data = []


                # 第一阶段回调函数：获取主模板ID
                def get_main_template_callback(future, index, template_name):
                    nonlocal template_get_success, template_get_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            template_get_success += 1
                            template_id = result['result'][0]['templateid']
                            main_template_data.append((index, template_name, template_id))
                            status = "\033[32m✓\033[0m"
                            msg = f"模板ID: {template_id}"
                        else:
                            template_get_failed += 1
                            main_template_data.append((index, template_name, None))
                            status = "\033[31m✗\033[0m"
                            msg = f"错误: {result['result']}"

                        progress = ((template_get_success + template_get_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 获取主模板: {template_name} {status} {msg}")
                        print(f"\r主模板进度: {template_get_success + template_get_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{template_get_success}\033[0m | 失败: \033[31m{template_get_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        template_get_failed += 1
                        main_template_data.append((index, template_name, None))
                        print(f"\r[{index + 1}/{total_tasks}] 获取主模板: {template_name} \033[31m异常\033[0m: {str(e)}")


                # 第二阶段回调函数：获取链接模板ID
                def get_link_template_callback(future, index, template_name):
                    nonlocal link_template_success, link_template_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            link_template_success += 1
                            template_id = result['result'][0]['templateid']
                            link_template_data.append((index, template_name, template_id))
                            status = "\033[32m✓\033[0m"
                            msg = f"模板ID: {template_id}"
                        else:
                            link_template_failed += 1
                            link_template_data.append((index, template_name, None))
                            status = "\033[31m✗\033[0m"
                            msg = f"错误: {result['result']}"

                        progress = ((link_template_success + link_template_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 获取链接模板: {template_name} {status} {msg}")
                        print(f"\r链接模板进度: {link_template_success + link_template_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{link_template_success}\033[0m | 失败: \033[31m{link_template_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        link_template_failed += 1
                        link_template_data.append((index, template_name, None))
                        print(f"\r[{index + 1}/{total_tasks}] 获取链接模板: {template_name} \033[31m异常\033[0m: {str(e)}")


                # 第三阶段回调函数：模板脱离操作（保留监控项）
                def unlink_template_callback(future, index, main_template_name, link_template_name):
                    nonlocal unlink_success, unlink_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            unlink_success += 1
                            status = "\033[32m✓\033[0m"
                            msg = f"返回值: \033[32m{result['result']}\033[0m"
                        else:
                            unlink_failed += 1
                            status = "\033[31m✗\033[0m"
                            msg = f"返回值: \033[31m{result['result']}\033[0m"

                        progress = ((unlink_success + unlink_failed) / total_tasks) * 100
                        print(f"\r[{index + 1}/{total_tasks}] 脱离模板(保留监控项): {main_template_name} <- {link_template_name} {status} {msg}")
                        print(f"\r脱离进度: {unlink_success + unlink_failed}/{total_tasks} ({progress:.1f}%) | "
                              f"成功: \033[32m{unlink_success}\033[0m | 失败: \033[31m{unlink_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        unlink_failed += 1
                        print(f"\r[{index + 1}/{total_tasks}] 脱离模板(保留监控项): {main_template_name} <- {link_template_name} \033[31m异常\033[0m: {str(e)}")


                # 第一阶段：获取主模板ID
                print(f"\n\033[1;36m=== 开始获取主模板ID (共 {total_tasks} 个) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, template_name in enumerate(column_1_list):
                        future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                        future.add_done_callback(partial(get_main_template_callback, index=idx, template_name=template_name))
                        futures.append(future)
                    wait(futures)

                # 第二阶段：获取链接模板ID
                print(f"\n\033[1;36m=== 开始获取链接模板ID (共 {total_tasks} 个) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, template_name in enumerate(column_2_list):
                        future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                        future.add_done_callback(partial(get_link_template_callback, index=idx, template_name=template_name))
                        futures.append(future)
                    wait(futures)

                # 准备关联数据（只处理两者都获取成功的）
                valid_pairs = []
                for idx in range(total_tasks):
                    main_name, main_id = main_template_data[idx][1], main_template_data[idx][2]
                    link_name, link_id = link_template_data[idx][1], link_template_data[idx][2]
                    if main_id and link_id:
                        valid_pairs.append((idx, main_name, main_id, link_name, link_id))
                    else:
                        print(f"\r[{idx + 1}/{total_tasks}] 跳过: {main_name or '未知模板'} <- {link_name or '未知模板'} (缺少ID)")

                # 第三阶段：执行模板脱离操作（保留监控项，单线程）
                print(f"\n\033[1;36m=== 开始模板脱离操作(保留监控项) (共 {len(valid_pairs)} 个有效组合，单线程执行) ===\033[0m")
                with ThreadPoolExecutor(max_workers=1) as executor:
                    futures = []
                    for idx, main_name, main_id, link_name, link_id in valid_pairs:
                        future = executor.submit(
                            cus_zabbix_api.def_massremove_templateids_link,
                            [main_id],
                            [link_id]
                        )
                        future.add_done_callback(partial(
                            unlink_template_callback,
                            index=idx,
                            main_template_name=main_name,
                            link_template_name=link_name
                        ))
                        futures.append(future)
                    wait(futures)

                # 最终统计
                print(f"\n\n\033[1;36m=== 操作完成 ===\033[0m")
                print(f"获取主模板ID: 成功 \033[32m{template_get_success}\033[0m | 失败 \033[31m{template_get_failed}\033[0m")
                print(f"获取链接模板ID: 成功 \033[32m{link_template_success}\033[0m | 失败 \033[31m{link_template_failed}\033[0m")
                print(f"模板脱离操作(保留监控项): 成功 \033[32m{unlink_success}\033[0m | 失败 \033[31m{unlink_failed}\033[0m")
                if template_get_failed > 0 or link_template_failed > 0 or unlink_failed > 0:
                    print("\033[33m请注意检查失败的任务\033[0m")
            process_data()
        # ![05_模板更新标签]
        elif args.update_tags != 'update_tags':
            def process_data():
                # 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 5)
                column_1_list = cus_excel_op.get_column_values(1)  # 模板名称列
                column_2_list = cus_excel_op.get_column_values(2)  # 标签名称列
                column_3_list = cus_excel_op.get_column_values(3)  # 标签值列
                del column_1_list[0]  # 删除标题行
                del column_2_list[0]  # 删除标题行
                del column_3_list[0]  # 删除标题行

                # 去重并保持原始顺序
                unit_column_1_list = sorted(set(column_1_list), key=column_1_list.index)
                total_templates = len(unit_column_1_list)

                # 进度统计
                template_get_success = 0
                template_get_failed = 0
                tag_update_success = 0
                tag_update_failed = 0

                # 准备标签数据
                print("\n\033[1;36m=== 准备标签数据 ===\033[0m")
                tag_data = {}
                for idx in range(len(column_1_list)):
                    template_name = column_1_list[idx]
                    tag_name = column_2_list[idx]
                    tag_value = str(column_3_list[idx])

                    if template_name not in tag_data:
                        tag_data[template_name] = []

                    tag_data[template_name].append({
                        "tag": tag_name,
                        "value": tag_value
                    })
                    progress = ((idx + 1) / len(column_1_list)) * 100
                    print(f"\r处理标签数据: {idx + 1}/{len(column_1_list)} ({progress:.1f}%)", end="", flush=True)


                # 回调函数：获取模板ID
                def get_template_callback(future, index, template_name):
                    nonlocal template_get_success, template_get_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            template_get_success += 1
                            template_id = result['result'][0]['templateid']
                            status = "\033[32m✓\033[0m"
                            msg = f"模板ID: {template_id}"
                        else:
                            template_get_failed += 1
                            template_id = ''
                            status = "\033[31m✗\033[0m"
                            msg = f"错误: {result['result']}"

                        # 存储模板ID和标签数据的映射
                        future.template_id = template_id
                        future.template_name = template_name

                        progress = ((template_get_success + template_get_failed) / total_templates) * 100
                        print(f"\r[{index + 1}/{total_templates}] 获取模板: {template_name} {status} {msg}")
                        print(f"\r模板获取进度: {template_get_success + template_get_failed}/{total_templates} ({progress:.1f}%) | "
                              f"成功: \033[32m{template_get_success}\033[0m | 失败: \033[31m{template_get_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        template_get_failed += 1
                        print(f"\r[{index + 1}/{total_templates}] 获取模板: {template_name} \033[31m异常\033[0m: {str(e)}")


                # 回调函数：更新标签
                def update_tags_callback(future, index, template_name):
                    nonlocal tag_update_success, tag_update_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            tag_update_success += 1
                            status = "\033[32m✓\033[0m"
                            msg = f"返回值: \033[32m{result['result']}\033[0m"
                        else:
                            tag_update_failed += 1
                            status = "\033[31m✗\033[0m"
                            msg = f"返回值: \033[31m{result['result']}\033[0m"

                        progress = ((tag_update_success + tag_update_failed) / total_templates) * 100
                        print(f"\r[{index + 1}/{total_templates}] 更新标签: {template_name} {status} {msg}")
                        print(f"\r标签更新进度: {tag_update_success + tag_update_failed}/{total_templates} ({progress:.1f}%) | "
                              f"成功: \033[32m{tag_update_success}\033[0m | 失败: \033[31m{tag_update_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        tag_update_failed += 1
                        print(f"\r[{index + 1}/{total_templates}] 更新标签: {template_name} \033[31m异常\033[0m: {str(e)}")


                # 第一阶段：获取模板ID
                print(f"\n\033[1;36m=== 开始获取模板ID (共 {total_templates} 个) ===\033[0m")
                template_ids = []
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, template_name in enumerate(unit_column_1_list):
                        future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                        future.add_done_callback(partial(get_template_callback, index=idx, template_name=template_name))
                        futures.append(future)
                    wait(futures)

                    # 收集有效的模板ID
                    for future in futures:
                        if hasattr(future, 'template_id') and future.template_id:
                            template_ids.append((future.template_name, future.template_id))

                # 第二阶段：更新标签（只处理获取到有效ID的模板）
                print(f"\n\033[1;36m=== 开始更新标签 (共 {len(template_ids)} 个有效模板) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, (template_name, template_id) in enumerate(template_ids):
                        if template_name in tag_data:
                            tags = tag_data[template_name]
                            future = executor.submit(
                                cus_zabbix_api.def_update_tags,
                                template_id,
                                tags
                            )
                            future.add_done_callback(partial(
                                update_tags_callback,
                                index=idx,
                                template_name=template_name
                            ))
                            futures.append(future)
                        else:
                            print(f"\r[{idx + 1}/{len(template_ids)}] 跳过: {template_name} (无标签数据)")
                    wait(futures)

                # 最终统计
                print(f"\n\n\033[1;36m=== 操作完成 ===\033[0m")
                print(f"获取模板ID: 成功 \033[32m{template_get_success}\033[0m | 失败 \033[31m{template_get_failed}\033[0m")
                print(f"更新标签: 成功 \033[32m{tag_update_success}\033[0m | 失败 \033[31m{tag_update_failed}\033[0m")
                if template_get_failed > 0 or tag_update_failed > 0:
                    print("\033[33m请注意检查失败的任务\033[0m")
            process_data()
        elif args.delete_tags != 'delete_tags':
            def process_data():
                # 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 5)
                column_1_list = cus_excel_op.get_column_values(1)  # 模板名称列
                column_2_list = cus_excel_op.get_column_values(2)  # 标签名称列
                column_3_list = cus_excel_op.get_column_values(3)  # 标签值列
                del column_1_list[0]  # 删除标题行
                del column_2_list[0]  # 删除标题行
                del column_3_list[0]  # 删除标题行

                # 去重并保持原始顺序
                unit_column_1_list = sorted(set(column_1_list), key=column_1_list.index)
                total_templates = len(unit_column_1_list)

                # 进度统计
                template_get_success = 0
                template_get_failed = 0
                tags_get_success = 0
                tags_get_failed = 0
                tag_delete_success = 0
                tag_delete_failed = 0

                # 准备要删除的标签数据
                print("\n\033[1;36m=== 准备要删除的标签数据 ===\033[0m")
                tags_to_delete = {}
                for idx in range(len(column_1_list)):
                    template_name = column_1_list[idx]
                    tag_name = column_2_list[idx]
                    tag_value = str(column_3_list[idx])

                    if template_name not in tags_to_delete:
                        tags_to_delete[template_name] = []

                    tags_to_delete[template_name].append({
                        "tag": tag_name,
                        "value": tag_value
                    })
                    progress = ((idx + 1) / len(column_1_list)) * 100
                    print(f"\r处理标签数据: {idx + 1}/{len(column_1_list)} ({progress:.1f}%)", end="", flush=True)

                # 存储模板数据和标签数据
                template_data = []
                old_tags_data = []


                # 回调函数：获取模板ID
                def get_template_callback(future, index, template_name):
                    nonlocal template_get_success, template_get_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            template_get_success += 1
                            template_id = result['result'][0]['templateid']
                            status = "\033[32m✓\033[0m"
                            msg = f"模板ID: {template_id}"
                        else:
                            template_get_failed += 1
                            template_id = ''
                            status = "\033[31m✗\033[0m"
                            msg = f"错误: {result['result']}"

                        # 存储模板数据
                        future.template_id = template_id
                        future.template_name = template_name

                        progress = ((template_get_success + template_get_failed) / total_templates) * 100
                        print(f"\r[{index + 1}/{total_templates}] 获取模板: {template_name} {status} {msg}")
                        print(f"\r模板获取进度: {template_get_success + template_get_failed}/{total_templates} ({progress:.1f}%) | "
                              f"成功: \033[32m{template_get_success}\033[0m | 失败: \033[31m{template_get_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        template_get_failed += 1
                        print(f"\r[{index + 1}/{total_templates}] 获取模板: {template_name} \033[31m异常\033[0m: {str(e)}")


                # 回调函数：获取模板原有标签
                def get_tags_callback(future, index, template_name):
                    nonlocal tags_get_success, tags_get_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            tags_get_success += 1
                            tags = result['result'][0]['tags']
                            status = "\033[32m✓\033[0m"
                            msg = f"获取到 {len(tags)} 个标签"
                        else:
                            tags_get_failed += 1
                            tags = []
                            status = "\033[31m✗\033[0m"
                            msg = f"错误: {result['result']}"

                        # 存储标签数据
                        future.tags = tags
                        future.template_name = template_name

                        progress = ((tags_get_success + tags_get_failed) / total_templates) * 100
                        print(f"\r[{index + 1}/{total_templates}] 获取标签: {template_name} {status} {msg}")
                        print(f"\r标签获取进度: {tags_get_success + tags_get_failed}/{total_templates} ({progress:.1f}%) | "
                              f"成功: \033[32m{tags_get_success}\033[0m | 失败: \033[31m{tags_get_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        tags_get_failed += 1
                        print(f"\r[{index + 1}/{total_templates}] 获取标签: {template_name} \033[31m异常\033[0m: {str(e)}")


                # 回调函数：删除标签
                def delete_tags_callback(future, index, template_name):
                    nonlocal tag_delete_success, tag_delete_failed
                    try:
                        result = future.result()
                        if result['tag'] is True:
                            tag_delete_success += 1
                            status = "\033[32m✓\033[0m"
                            msg = f"返回值: \033[32m{result['result']}\033[0m"
                        else:
                            tag_delete_failed += 1
                            status = "\033[31m✗\033[0m"
                            msg = f"返回值: \033[31m{result['result']}\033[0m"

                        progress = ((tag_delete_success + tag_delete_failed) / total_templates) * 100
                        print(f"\r[{index + 1}/{total_templates}] 移除标签: {template_name} {status} {msg}")
                        print(f"\r标签移除进度: {tag_delete_success + tag_delete_failed}/{total_templates} ({progress:.1f}%) | "
                              f"成功: \033[32m{tag_delete_success}\033[0m | 失败: \033[31m{tag_delete_failed}\033[0m",
                              end="", flush=True)
                    except Exception as e:
                        tag_delete_failed += 1
                        print(f"\r[{index + 1}/{total_templates}] 移除标签: {template_name} \033[31m异常\033[0m: {str(e)}")


                # 第一阶段：获取模板ID
                print(f"\n\033[1;36m=== 开始获取模板ID (共 {total_templates} 个) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, template_name in enumerate(unit_column_1_list):
                        future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                        future.add_done_callback(partial(get_template_callback, index=idx, template_name=template_name))
                        futures.append(future)
                    wait(futures)

                    # 收集有效的模板数据
                    template_data = []
                    for future in futures:
                        if hasattr(future, 'template_id') and future.template_id:
                            template_data.append((future.template_name, future.template_id))

                # 第二阶段：获取模板原有标签
                print(f"\n\033[1;36m=== 开始获取模板原有标签 (共 {len(template_data)} 个有效模板) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, (template_name, template_id) in enumerate(template_data):
                        future = executor.submit(cus_zabbix_api.def_get_template_tags, template_name)
                        future.add_done_callback(partial(get_tags_callback, index=idx, template_name=template_name))
                        futures.append(future)
                    wait(futures)

                    # 准备要更新的标签数据（原有标签减去要删除的标签）
                    update_data = []
                    for future in futures:
                        if hasattr(future, 'tags') and hasattr(future, 'template_name'):
                            template_name = future.template_name
                            old_tags = future.tags

                            # 找出要保留的标签
                            if template_name in tags_to_delete:
                                tags_to_remove = tags_to_delete[template_name]
                                new_tags = [tag for tag in old_tags if tag not in tags_to_remove]
                            else:
                                new_tags = old_tags

                            update_data.append((template_name, new_tags))

                # 第三阶段：更新标签（删除指定标签）
                print(f"\n\033[1;36m=== 开始移除标签 (共 {len(update_data)} 个模板) ===\033[0m")
                with ThreadPoolExecutor(max_workers=zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, (template_name, new_tags) in enumerate(update_data):
                        # 找到对应的模板ID
                        template_id = next((tid for name, tid in template_data if name == template_name), None)
                        if template_id:
                            future = executor.submit(
                                cus_zabbix_api.def_update_tags,
                                template_id,
                                new_tags
                            )
                            future.add_done_callback(partial(
                                delete_tags_callback,
                                index=idx,
                                template_name=template_name
                            ))
                            futures.append(future)
                        else:
                            print(f"\r[{idx + 1}/{len(update_data)}] 跳过: {template_name} (无效模板ID)")
                    wait(futures)

                # 最终统计
                print(f"\n\n\033[1;36m=== 操作完成 ===\033[0m")
                print(f"获取模板ID: 成功 \033[32m{template_get_success}\033[0m | 失败 \033[31m{template_get_failed}\033[0m")
                print(f"获取原有标签: 成功 \033[32m{tags_get_success}\033[0m | 失败 \033[31m{tags_get_failed}\033[0m")
                print(f"移除标签: 成功 \033[32m{tag_delete_success}\033[0m | 失败 \033[31m{tag_delete_failed}\033[0m")
                if template_get_failed > 0 or tags_get_failed > 0 or tag_delete_failed > 0:
                    print("\033[33m请注意检查失败的任务\033[0m")
            process_data()
        # ![06_模板创建监控项]
        elif args.create_template_item != 'create_template_item':
            def process_data():
                # 加载Excel文件并读取各列数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 6)
                column_1_list = cus_excel_op.get_column_values(1)
                del column_1_list[0]  # 删除标题行

                # 初始化各列数据列表
                column_2_list = []
                column_3_list = []
                column_4_list = []
                column_5_list = []
                column_6_list = []
                column_7_list = []

                # 填充各列数据
                for i in range(len(column_1_list)):
                    column_2_list.append(cus_excel_op.get_cell_value(i + 2, 2))
                    column_3_list.append(cus_excel_op.get_cell_value(i + 2, 3))
                    column_4_list.append(cus_excel_op.get_cell_value(i + 2, 4))
                    column_5_list.append(cus_excel_op.get_cell_value(i + 2, 5))
                    column_6_list.append(cus_excel_op.get_cell_value(i + 2, 6))
                    column_7_list.append(cus_excel_op.get_cell_value(i + 2, 7))

                # 获取所有模板ID（多线程）
                lv_list_get_all_templateid = []


                def template_callback(future):
                    """获取模板ID的回调函数"""
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            templateid = lv_result['result'][0]['templateid']
                            lv_list_get_all_templateid.append(templateid)
                        else:
                            lv_list_get_all_templateid.append('')
                    except Exception as e:
                        lv_list_get_all_templateid.append('')
                        print(f"获取模板ID时出错: {str(e)}")


                # 使用线程池获取模板ID
                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for template_name in column_1_list:
                        future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                        future.add_done_callback(template_callback)
                        futures.append(future)

                    # 等待所有任务完成
                    wait(futures)

                # 创建模板监控项（多线程）
                lv_sum_v01 = 0
                results = [None] * len(column_1_list)  # 预分配结果列表


                def item_callback(future, index):
                    """创建监控项的回调函数"""
                    nonlocal lv_sum_v01
                    try:
                        lv_result = future.result()
                        results[index] = lv_result  # 存储结果

                        if lv_result['tag'] is True:
                            print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板创建监控项: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                                  % (len(column_1_list), index + 1, column_1_list[index], lv_result['result']))
                        else:
                            print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板创建监控项: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                                  % (len(column_1_list), index + 1, column_1_list[index], lv_result['result']))

                        lv_sum_v01 += 1
                    except Exception as e:
                        print(f"处理监控项 {column_1_list[index]} 时出错: {str(e)}")


                # 使用线程池创建监控项
                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for i in range(len(column_1_list)):
                        future = executor.submit(
                            cus_zabbix_api.def_create_template_item,
                            lv_list_get_all_templateid[i],
                            column_2_list[i],
                            column_3_list[i],
                            column_4_list[i],
                            column_5_list[i],
                            column_6_list[i],
                            column_7_list[i]
                        )
                        future.add_done_callback(lambda f, idx=i: item_callback(f, idx))
                        futures.append(future)

                    # 等待所有任务完成
                    wait(futures)
            process_data()
        elif args.delete_template_item != 'delete_template_item':
            def process_data():
                # 1. 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 6)
                column_1_list = cus_excel_op.get_column_values(1)  # 模板名称列
                del column_1_list[0]  # 移除标题行

                # 读取监控项key列（第4列）
                column_4_list = []
                for i in range(len(column_1_list)):
                    column_4_list.append(cus_excel_op.get_cell_value(i + 2, 4))

                # 2. 获取模板ID（多线程）
                lv_list_get_all_templateid = []


                def get_template_callback(future, index):
                    """获取模板ID的回调函数"""
                    try:
                        lv_result = future.result()
                        if lv_result['tag']:
                            templateid = lv_result['result'][0]['templateid']
                            lv_list_get_all_templateid.append(templateid)
                            print(f"({index + 1}/{len(column_1_list)}) 获取模板ID成功: {templateid}")
                        else:
                            lv_list_get_all_templateid.append('')
                            print(f"\033[31m({index + 1}/{len(column_1_list)}) 获取模板ID失败: {lv_result['result']}\033[0m")
                    except Exception as e:
                        lv_list_get_all_templateid.append('')
                        print(f"\033[31m({index + 1}/{len(column_1_list)}) 获取模板ID异常: {str(e)}\033[0m")


                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, template_name in enumerate(column_1_list):
                        future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                        future.add_done_callback(lambda f, i=idx: get_template_callback(f, i))
                        futures.append(future)
                    wait(futures)  # 等待所有任务完成

                # 3. 获取监控项ID（多线程）
                lv_list_get_all_template_itemid = []


                def get_item_callback(future, index):
                    """获取监控项ID的回调函数"""
                    try:
                        lv_result = future.result()
                        if lv_result['tag']:
                            itemid = lv_result['result'][0]['itemid']
                            lv_list_get_all_template_itemid.append([itemid])
                            print(f"({index + 1}/{len(column_1_list)}) 获取监控项ID成功: {itemid}")
                        else:
                            lv_list_get_all_template_itemid.append([])
                            print(f"\033[31m({index + 1}/{len(column_1_list)}) 获取监控项ID失败: {lv_result['result']}\033[0m")
                    except Exception as e:
                        lv_list_get_all_template_itemid.append([])
                        print(f"\033[31m({index + 1}/{len(column_1_list)}) 获取监控项ID异常: {str(e)}\033[0m")


                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, (templateid, key) in enumerate(zip(lv_list_get_all_templateid, column_4_list)):
                        if templateid:  # 只有模板ID有效时才执行
                            future = executor.submit(cus_zabbix_api.def_get_template_item, templateid, key)
                            future.add_done_callback(lambda f, i=idx: get_item_callback(f, i))
                            futures.append(future)
                        else:
                            lv_list_get_all_template_itemid.append([])
                    wait(futures)

                # 4. 删除监控项（多线程）
                completed_count = 0


                def delete_item_callback(future, index):
                    """删除监控项的回调函数"""
                    nonlocal completed_count
                    try:
                        lv_result = future.result()
                        template_name = column_1_list[index]
                        if lv_result['tag']:
                            print(u'(\033[;34m{}\033[0m/\033[;34m{}\033[0m): 删除监控项: \033[;32m{}\033[0m 成功 返回值: \033[;32m{}\033[0m'
                                  .format(len(column_1_list), index + 1, template_name, lv_result['result']))
                        else:
                            print(u'(\033[;31m{}\033[0m/\033[;31m{}\033[0m): 删除监控项: \033[;31m{}\033[0m 失败 返回值: \033[;31m{}\033[0m'
                                  .format(len(column_1_list), index + 1, template_name, lv_result['result']))
                        completed_count += 1
                    except Exception as e:
                        print(f"\033[31m({index + 1}/{len(column_1_list)}) 删除监控项异常: {str(e)}\033[0m")
                        completed_count += 1


                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, itemids in enumerate(lv_list_get_all_template_itemid):
                        if itemids:  # 只有监控项ID存在时才执行删除
                            future = executor.submit(cus_zabbix_api.def_delete_template_item, itemids)
                            future.add_done_callback(lambda f, i=idx: delete_item_callback(f, i))
                            futures.append(future)
                        else:
                            print(f"({idx + 1}/{len(column_1_list)}) 跳过无效的监控项删除")
                            completed_count += 1
                    wait(futures)
            process_data()
        # ![07_模板更新监控项标签]
        elif args.update_template_item_tags != 'update_template_item_tags':
            def process_data():
                # 1. 加载Excel数据
                try:
                    cus_excel_op.load_excel('zabbix_api.xlsx', 7)  # 修复拼写错误：load_excel → load_excel
                    column_1_list = cus_excel_op.get_column_values(1)  # 模板名称列
                    del column_1_list[0]  # 移除标题行

                    # 读取各列数据
                    column_2_list, column_3_list, column_4_list, column_5_list = [], [], [], []
                    for i in range(len(column_1_list)):
                        column_2_list.append(cus_excel_op.get_cell_value(i + 2, 2))  # 监控项key
                        column_3_list.append(cus_excel_op.get_cell_value(i + 2, 3))  # 标签名
                        column_4_list.append(cus_excel_op.get_cell_value(i + 2, 4))  # 标签值
                        column_5_list.append(f"{cus_excel_op.get_cell_value(i + 2, 1)}_{cus_excel_op.get_cell_value(i + 2, 2)}")  # 组合键
                except Exception as e:
                    print(f"\033[31m[ERROR] 加载Excel数据失败: {str(e)}\033[0m")
                    exit(1)

                # 2. 获取模板ID（多线程+回调）
                lv_list_get_all_templateid = [None] * len(column_1_list)  # 预分配列表


                def get_template_callback(future, index):
                    """获取模板ID的回调函数"""
                    try:
                        lv_result = future.result()
                        if lv_result['tag']:
                            templateid = lv_result['result'][0]['templateid']
                            lv_list_get_all_templateid[index] = templateid
                            print(f"\033[34m[SUCCESS] ({index + 1}/{len(column_1_list)}) 获取模板ID成功: {column_1_list[index]} → {templateid}\033[0m")
                        else:
                            lv_list_get_all_templateid[index] = ''
                            print(f"\033[31m[FAILED] ({index + 1}/{len(column_1_list)}) 获取模板ID失败: {column_1_list[index]} → {lv_result['result']}\033[0m")
                    except Exception as e:
                        lv_list_get_all_templateid[index] = ''
                        print(f"\033[31m[ERROR] ({index + 1}/{len(column_1_list)}) 处理模板 {column_1_list[index]} 时异常: {str(e)}\033[0m")


                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, template_name in enumerate(column_1_list):
                        future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                        future.add_done_callback(lambda f, i=idx: get_template_callback(f, i))
                        futures.append(future)
                    wait(futures)

                # 3. 获取监控项ID（多线程+回调）
                lv_list_get_all_template_itemid = [None] * len(column_1_list)


                def get_item_callback(future, index):
                    """获取监控项ID的回调函数"""
                    try:
                        lv_result = future.result()
                        template_name = column_1_list[index]
                        if lv_result['tag'] and lv_result['result']:
                            itemid = lv_result['result'][0]['itemid']
                            lv_list_get_all_template_itemid[index] = itemid
                            print(f"\033[34m[SUCCESS] ({index + 1}/{len(column_1_list)}) 获取监控项成功: {template_name}/{column_2_list[index]} → {itemid}\033[0m")
                        else:
                            lv_list_get_all_template_itemid[index] = ''
                            print(f"\033[31m[FAILED] ({index + 1}/{len(column_1_list)}) 获取监控项失败: {template_name}/{column_2_list[index]} → {lv_result.get('result', '无结果')}\033[0m")
                    except Exception as e:
                        lv_list_get_all_template_itemid[index] = ''
                        print(f"\033[31m[ERROR] ({index + 1}/{len(column_1_list)}) 处理监控项 {column_1_list[index]}/{column_2_list[index]} 时异常: {str(e)}\033[0m")


                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, (templateid, key) in enumerate(zip(lv_list_get_all_templateid, column_2_list)):
                        if templateid:  # 仅当模板ID有效时执行
                            future = executor.submit(cus_zabbix_api.def_get_template_item, templateid, key)
                            future.add_done_callback(lambda f, i=idx: get_item_callback(f, i))
                            futures.append(future)
                        else:
                            lv_list_get_all_template_itemid[idx] = ''
                            print(f"\033[33m[SKIPPED] ({idx + 1}/{len(column_1_list)}) 跳过无效模板: {column_1_list[idx]}\033[0m")
                    wait(futures)

                # 4. 处理标签数据
                try:
                    # 去重并保持原始顺序
                    unit_column_1_list = sorted(set(column_5_list), key=column_5_list.index)

                    # 构建标签字典 {唯一键: [标签列表]}
                    tag_dict = {}
                    for idx, key in enumerate(column_5_list):
                        tag_info = {
                            "tag": column_3_list[idx],
                            "value": column_4_list[idx]
                        }
                        if key in tag_dict:
                            tag_dict[key].append(tag_info)
                        else:
                            tag_dict[key] = [tag_info]

                    # 按原始顺序生成最终标签列表
                    lv_list_get_all_pre_delete_tag = [tag_dict[key] for key in unit_column_1_list]
                except Exception as e:
                    print(f"\033[31m[ERROR] 处理标签数据时异常: {str(e)}\033[0m")
                    exit(1)

                # 5. 更新标签（多线程+回调）
                completed_count = 0


                def update_tags_callback(future, index):
                    """更新标签的回调函数"""
                    nonlocal completed_count
                    try:
                        lv_result = future.result()
                        template_name = column_1_list[index]
                        if lv_result['tag']:
                            print(u'\033[34m[SUCCESS] (%d/%d) 更新标签成功: %s → %s\033[0m' %
                                  (index + 1, len(column_1_list), template_name, lv_result['result']))
                        else:
                            print(u'\033[31m[FAILED] (%d/%d) 更新标签失败: %s → %s\033[0m' %
                                  (index + 1, len(column_1_list), template_name, lv_result['result']))
                        completed_count += 1
                    except Exception as e:
                        print(f"\033[31m[ERROR] ({index + 1}/{len(column_1_list)}) 更新标签异常: {str(e)}\033[0m")
                        completed_count += 1


                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    valid_itemids = sorted(set(i for i in lv_list_get_all_template_itemid if i),
                                           key=lv_list_get_all_template_itemid.index)

                    for idx, itemid in enumerate(valid_itemids):
                        if idx < len(lv_list_get_all_pre_delete_tag):  # 确保不越界
                            future = executor.submit(
                                cus_zabbix_api.def_update_template_item_tags,
                                itemid,
                                lv_list_get_all_pre_delete_tag[idx]
                            )
                            future.add_done_callback(lambda f, i=idx: update_tags_callback(f, i))
                            futures.append(future)
                        else:
                            print(f"\033[33m[SKIPPED] ({idx + 1}/{len(valid_itemids)}) 标签数据不足，跳过\033[0m")
                    wait(futures)
            process_data()
        elif args.delete_template_item_tags != 'delete_template_item_tags':
            def process_data():
                # 1. 加载Excel数据
                try:
                    cus_excel_op.load_excel('zabbix_api.xlsx', 7)
                    column_1_list = cus_excel_op.get_column_values(1)  # 模板名称列
                    del column_1_list[0]  # 移除标题行

                    # 读取各列数据
                    column_2_list, column_3_list, column_4_list, column_5_list = [], [], [], []
                    for i in range(len(column_1_list)):
                        column_2_list.append(cus_excel_op.get_cell_value(i + 2, 2))  # 监控项key
                        column_3_list.append(cus_excel_op.get_cell_value(i + 2, 3))  # 标签名
                        column_4_list.append(cus_excel_op.get_cell_value(i + 2, 4))  # 标签值
                        column_5_list.append(f"{cus_excel_op.get_cell_value(i + 2, 1)}_{cus_excel_op.get_cell_value(i + 2, 2)}")  # 组合键
                except Exception as e:
                    print(f"\033[31m[ERROR] 加载Excel数据失败: {str(e)}\033[0m")
                    exit(1)

                # 2. 获取模板ID（多线程+回调）
                lv_list_get_all_templateid = [None] * len(column_1_list)


                def get_template_callback(future, index):
                    """获取模板ID的回调函数"""
                    try:
                        lv_result = future.result()
                        template_name = column_1_list[index]
                        if lv_result['tag'] and lv_result['result']:
                            templateid = lv_result['result'][0]['templateid']
                            lv_list_get_all_templateid[index] = templateid
                            print(f"\033[34m[SUCCESS] ({index + 1}/{len(column_1_list)}) 获取模板ID成功: {template_name} → {templateid}\033[0m")
                        else:
                            lv_list_get_all_templateid[index] = ''
                            print(f"\033[31m[FAILED] ({index + 1}/{len(column_1_list)}) 获取模板ID失败: {template_name} → {lv_result.get('result', '无结果')}\033[0m")
                    except Exception as e:
                        lv_list_get_all_templateid[index] = ''
                        print(f"\033[31m[ERROR] ({index + 1}/{len(column_1_list)}) 处理模板 {column_1_list[index]} 时异常: {str(e)}\033[0m")


                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, template_name in enumerate(column_1_list):
                        future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                        future.add_done_callback(lambda f, i=idx: get_template_callback(f, i))
                        futures.append(future)
                    wait(futures)

                # 3. 获取监控项ID（多线程+回调）
                lv_list_get_all_template_itemid = [None] * len(column_1_list)


                def get_item_callback(future, index):
                    """获取监控项ID的回调函数"""
                    try:
                        lv_result = future.result()
                        template_name = column_1_list[index]
                        item_key = column_2_list[index]
                        if lv_result['tag'] and lv_result['result']:
                            itemid = lv_result['result'][0]['itemid']
                            lv_list_get_all_template_itemid[index] = itemid
                            print(f"\033[34m[SUCCESS] ({index + 1}/{len(column_1_list)}) 获取监控项成功: {template_name}/{item_key} → {itemid}\033[0m")
                        else:
                            lv_list_get_all_template_itemid[index] = ''
                            print(f"\033[31m[FAILED] ({index + 1}/{len(column_1_list)}) 获取监控项失败: {template_name}/{item_key} → {lv_result.get('result', '无结果')}\033[0m")
                    except Exception as e:
                        lv_list_get_all_template_itemid[index] = ''
                        print(f"\033[31m[ERROR] ({index + 1}/{len(column_1_list)}) 处理监控项 {column_1_list[index]}/{column_2_list[index]} 时异常: {str(e)}\033[0m")


                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, (templateid, key) in enumerate(zip(lv_list_get_all_templateid, column_2_list)):
                        if templateid:  # 仅当模板ID有效时执行
                            future = executor.submit(cus_zabbix_api.def_get_template_item, templateid, key)
                            future.add_done_callback(lambda f, i=idx: get_item_callback(f, i))
                            futures.append(future)
                        else:
                            lv_list_get_all_template_itemid[idx] = ''
                            print(f"\033[33m[SKIPPED] ({idx + 1}/{len(column_1_list)}) 跳过无效模板: {column_1_list[idx]}\033[0m")
                    wait(futures)

                # 4. 处理标签数据
                try:
                    # 去重并保持原始顺序
                    unit_column_1_list = sorted(set(column_5_list), key=column_5_list.index)

                    # 构建待删除标签字典 {唯一键: [标签列表]}
                    tags_to_remove = {}
                    for idx, key in enumerate(column_5_list):
                        tag_info = {"tag": column_3_list[idx], "value": column_4_list[idx]}
                        if key in tags_to_remove:
                            tags_to_remove[key].append(tag_info)
                        else:
                            tags_to_remove[key] = [tag_info]

                    # 按原始顺序生成待删除标签列表
                    lv_list_get_all_pre_delete_tag = [tags_to_remove[key] for key in unit_column_1_list]
                except Exception as e:
                    print(f"\033[31m[ERROR] 处理标签数据时异常: {str(e)}\033[0m")
                    exit(1)

                # 5. 获取现有标签（多线程+回调）
                valid_itemids = [itemid for itemid in lv_list_get_all_template_itemid if itemid]
                lv_list_get_all_template_item_tags = [None] * len(valid_itemids)


                def get_tags_callback(future, index):
                    """获取现有标签的回调函数"""
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] and lv_result['result']:
                            lv_list_get_all_template_item_tags[index] = lv_result['result'][0]['tags']
                            print(f"\033[34m[SUCCESS] ({index + 1}/{len(valid_itemids)}) 获取标签成功: ItemID {valid_itemids[index]}\033[0m")
                        else:
                            lv_list_get_all_template_item_tags[index] = []
                            print(f"\033[31m[FAILED] ({index + 1}/{len(valid_itemids)}) 获取标签失败: ItemID {valid_itemids[index]} → {lv_result.get('result', '无结果')}\033[0m")
                    except Exception as e:
                        lv_list_get_all_template_item_tags[index] = []
                        print(f"\033[31m[ERROR] ({index + 1}/{len(valid_itemids)}) 获取标签异常: {str(e)}\033[0m")


                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, itemid in enumerate(valid_itemids):
                        future = executor.submit(cus_zabbix_api.def_get_template_item_tags, itemid)
                        future.add_done_callback(lambda f, i=idx: get_tags_callback(f, i))
                        futures.append(future)
                    wait(futures)

                # 6. 计算最终标签（移除指定标签）
                for i in range(min(len(lv_list_get_all_template_item_tags), len(lv_list_get_all_pre_delete_tag))):
                    if lv_list_get_all_template_item_tags[i]:
                        for tag in lv_list_get_all_pre_delete_tag[i]:
                            try:
                                lv_list_get_all_template_item_tags[i] = [t for t in lv_list_get_all_template_item_tags[i]
                                                                         if not (t['tag'] == tag['tag'] and t['value'] == tag['value'])]
                            except Exception as e:
                                print(f"\033[33m[WARNING] 处理标签时跳过异常: {str(e)}\033[0m")
                                continue

                # 7. 更新标签（多线程+回调）
                completed_count = 0


                def update_tags_callback(future, index):
                    """更新标签的回调函数"""
                    nonlocal completed_count
                    try:
                        lv_result = future.result()
                        itemid = valid_itemids[index]
                        if lv_result['tag']:
                            print(u'\033[34m[SUCCESS] (%d/%d) 移除标签成功: ItemID %s → %s\033[0m' %
                                  (index + 1, len(valid_itemids), itemid, lv_result['result']))
                        else:
                            print(u'\033[31m[FAILED] (%d/%d) 移除标签失败: ItemID %s → %s\033[0m' %
                                  (index + 1, len(valid_itemids), itemid, lv_result['result']))
                        completed_count += 1
                    except Exception as e:
                        print(f"\033[31m[ERROR] ({index + 1}/{len(valid_itemids)}) 更新标签异常: {str(e)}\033[0m")
                        completed_count += 1


                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, itemid in enumerate(valid_itemids):
                        if idx < len(lv_list_get_all_template_item_tags):  # 确保不越界
                            future = executor.submit(
                                cus_zabbix_api.def_update_template_item_tags,
                                itemid,
                                lv_list_get_all_template_item_tags[idx]
                            )
                            future.add_done_callback(lambda f, i=idx: update_tags_callback(f, i))
                            futures.append(future)
                        else:
                            print(f"\033[33m[SKIPPED] ({idx + 1}/{len(valid_itemids)}) 标签数据不足，跳过 ItemID {itemid}\033[0m")
                            completed_count += 1
                    wait(futures)
            process_data()
        # ![08_模板创建触发器]
        elif args.create_template_trigger != 'create_template_trigger':
            def process_data():
                # 加载Excel文件（第8个工作表）
                cus_excel_op.load_excel('zabbix_api.xlsx', 8)

                # 获取第一列的值（跳过表头）
                column_1_list = cus_excel_op.get_column_values(1)
                del column_1_list[0]

                # 初始化其他列的空列表
                column_2_list = []
                column_3_list = []
                column_4_list = []

                # 填充各列数据
                for i in range(len(column_1_list)):
                    column_2_list.append(cus_excel_op.get_cell_value(i + 2, 2))
                    column_3_list.append(cus_excel_op.get_cell_value(i + 2, 3))
                    column_4_list.append(cus_excel_op.get_cell_value(i + 2, 4))

                # 计数器初始化
                lv_sum_v01 = 0


                # 定义callback函数用于实时处理结果
                def process_result(future):
                    nonlocal lv_sum_v01
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板创建触发器: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                                  % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                        else:
                            print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板创建触发器: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                                  % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                        lv_sum_v01 += 1
                    except Exception as e:
                        print(f"处理结果时发生错误: {str(e)}")


                # 创建线程池
                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    # 存储所有的future对象
                    futures = []

                    # 提交所有任务到线程池
                    for i in range(len(column_1_list)):
                        future = executor.submit(
                            cus_zabbix_api.def_create_template_trigger,
                            column_1_list[i],
                            column_2_list[i],
                            column_3_list[i],
                            column_4_list[i]
                        )
                        future.add_done_callback(process_result)
                        futures.append(future)

                    # 等待所有任务完成
                    wait(futures)

            process_data()
        elif args.delete_template_trigger != 'delete_template_trigger':
            def process_data():
                # 1. 加载Excel数据
                cus_excel_op.load_excel('zabbix_api.xlsx', 8)

                # 获取第一列(跳过表头)和第五列数据
                column_1_list = cus_excel_op.get_column_values(1)
                del column_1_list[0]
                column_5_list = [cus_excel_op.get_cell_value(i + 2, 5) for i in range(len(column_1_list))]


                # 2. 获取所有模板ID (第一阶段)
                def get_template_callback(future, index):
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            lv_list_get_all_templateid[index] = lv_result['result'][0]['templateid']
                        else:
                            lv_list_get_all_templateid[index] = ''
                    except Exception as e:
                        print(f"获取模板ID时出错(索引{index}): {str(e)}")
                        lv_list_get_all_templateid[index] = ''


                lv_list_get_all_templateid = [''] * len(column_5_list)  # 预初始化列表
                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, template_name in enumerate(column_5_list):
                        future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                        future.add_done_callback(lambda f, i=idx: get_template_callback(f, i))
                        futures.append(future)
                    wait(futures)


                # 3. 获取所有触发器ID (第二阶段)
                def get_trigger_callback(future, index):
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True and lv_result['result']:
                            lv_list_get_all_template_trigger[index] = [lv_result['result'][0]['triggerid']]
                        else:
                            lv_list_get_all_template_trigger[index] = []
                    except Exception as e:
                        print(f"获取触发器ID时出错(索引{index}): {str(e)}")
                        lv_list_get_all_template_trigger[index] = []


                lv_list_get_all_template_trigger = [[] for _ in range(len(column_1_list))]  # 预初始化二维列表
                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, (template_id, trigger_name) in enumerate(zip(lv_list_get_all_templateid, column_1_list)):
                        future = executor.submit(cus_zabbix_api.def_get_template_trigger, template_id, trigger_name)
                        future.add_done_callback(lambda f, i=idx: get_trigger_callback(f, i))
                        futures.append(future)
                    wait(futures)


                # 4. 删除触发器 (第三阶段)
                def delete_trigger_callback(future, index):
                    nonlocal lv_sum_v01
                    try:
                        lv_result = future.result()
                        if lv_result['tag'] is True:
                            print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板删除触发器: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                                  % (len(column_1_list), index + 1, column_1_list[index], lv_result['result']))
                        else:
                            print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板删除触发器: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                                  % (len(column_1_list), index + 1, column_1_list[index], lv_result['result']))
                        lv_sum_v01 += 1
                    except Exception as e:
                        print(f"删除触发器时出错(索引{index}): {str(e)}")


                lv_sum_v01 = 0
                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for idx, trigger_ids in enumerate(lv_list_get_all_template_trigger):
                        if trigger_ids:  # 只处理有触发器ID的情况
                            future = executor.submit(cus_zabbix_api.def_delete_template_trigger, trigger_ids)
                            future.add_done_callback(lambda f, i=idx: delete_trigger_callback(f, i))
                            futures.append(future)
                    wait(futures)
            process_data()
        # ![09_模板更新触发器标签]
        elif args.update_template_trigger_tags != 'update_template_trigger_tags':
            # 加载Excel文件（第9个工作表）
            cus_excel_op.load_excel('zabbix_api.xlsx', 9)

            # 获取各列数据
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]  # 删除标题行
            column_2_list = []
            column_3_list = []
            column_4_list = []
            column_5_list = []
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.get_cell_value(i + 2, 2))
                column_3_list.append(cus_excel_op.get_cell_value(i + 2, 3))
                column_4_list.append(cus_excel_op.get_cell_value(i + 2, 4))
                column_5_list.append(cus_excel_op.get_cell_value(i + 2, 1) + '_' +
                                     cus_excel_op.get_cell_value(i + 2, 2))
            i = None


            # 定义callback函数用于实时显示结果
            def progress_callback(task_index, total_tasks, item_id, result, success_msg, error_msg):
                """进度回调函数，用于统一格式化输出结果"""
                if result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> %s: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (total_tasks, task_index + 1, success_msg, item_id, result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> %s: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (total_tasks, task_index + 1, error_msg, item_id, result['result']))


            # 获取所有模板ID（多线程）
            lv_list_get_all_templateid = []


            def get_template_callback(future, template_name, index):
                """获取模板ID的回调函数"""
                result = future.result()
                if result['tag'] is True:
                    lv_list_get_all_templateid.append(result['result'][0]['templateid'])
                else:
                    lv_list_get_all_templateid.append('')
                progress_callback(index, len(column_1_list), template_name, result,
                                  "获取模板ID", "获取模板ID")


            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            futures = []
            for idx, template in enumerate(column_1_list):
                future = executor.submit(cus_zabbix_api.def_get_template, template)
                future.add_done_callback(lambda f, t=template, i=idx: get_template_callback(f, t, i))
                futures.append(future)
            wait(futures)  # 等待所有任务完成

            # 获取所有触发器ID（多线程）
            lv_list_get_all_template_itemid = []


            def get_trigger_callback(future, trigger_name, index):
                """获取触发器ID的回调函数"""
                result = future.result()
                if result['tag'] is True:
                    lv_list_get_all_template_itemid.append(result['result'][0]['triggerid'])
                else:
                    lv_list_get_all_template_itemid.append('')
                progress_callback(index, len(column_2_list), trigger_name, result,
                                  "获取触发器ID", "获取触发器ID")


            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            futures = []
            for idx, (templateid, trigger_name) in enumerate(zip(lv_list_get_all_templateid, column_2_list)):
                future = executor.submit(cus_zabbix_api.def_get_template_trigger, templateid, trigger_name)
                future.add_done_callback(lambda f, t=trigger_name, i=idx: get_trigger_callback(f, t, i))
                futures.append(future)
            wait(futures)  # 等待所有任务完成

            # 数据处理：去重和排序
            unit_column_1_list = list(set(column_5_list))
            unit_column_1_list.sort(key=column_5_list.index)

            # 准备要更新的标签数据
            lv_list_tmp_get_all_tag = []
            for o in range(len(column_5_list)):
                for i in range(len(unit_column_1_list)):
                    if column_5_list[o] == unit_column_1_list[i]:
                        lv_list_tmp_get_all_tag.append({unit_column_1_list[i]: {
                            "tag": cus_excel_op.get_cell_value(o + 2, 3),
                            "value": cus_excel_op.get_cell_value(o + 2, 4)
                        }})

            # 将标签数据转换为字典格式
            dict4 = {}
            for i in range(len(lv_list_tmp_get_all_tag)):
                for key in lv_list_tmp_get_all_tag[i].keys():
                    if key in unit_column_1_list:
                        dict4.setdefault(key, []).append(lv_list_tmp_get_all_tag[i][key])
            lv_list_get_all_pre_delete_tag = list(dict4.values())

            # 触发器ID去重和排序
            unit_column_2_list = list(set(lv_list_get_all_template_itemid))
            unit_column_2_list.sort(key=lv_list_get_all_template_itemid.index)


            # 更新触发器标签（多线程）
            def update_tags_callback(future, trigger_id, index):
                """更新触发器标签的回调函数"""
                result = future.result()
                progress_callback(index, len(unit_column_2_list), trigger_id, result,
                                  "模板更新触发器标签", "模板更新触发器标签")


            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            futures = []
            for idx, (trigger_id, tags) in enumerate(zip(unit_column_2_list, lv_list_get_all_pre_delete_tag)):
                future = executor.submit(cus_zabbix_api.def_update_template_trigger_tags, trigger_id, tags)
                future.add_done_callback(lambda f, tid=trigger_id, i=idx: update_tags_callback(f, tid, i))
                futures.append(future)
            wait(futures)  # 等待所有任务完成
        elif args.delete_template_trigger_tags != 'delete_template_trigger_tags':
            # 加载Excel文件（第9个工作表）
            cus_excel_op.load_excel('zabbix_api.xlsx', 9)

            # 获取各列数据
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]  # 删除标题行
            column_2_list = []
            column_3_list = []
            column_4_list = []
            column_5_list = []
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.get_cell_value(i + 2, 2))
                column_3_list.append(cus_excel_op.get_cell_value(i + 2, 3))
                column_4_list.append(cus_excel_op.get_cell_value(i + 2, 4))
                column_5_list.append(cus_excel_op.get_cell_value(i + 2, 1) + '_' +
                                     cus_excel_op.get_cell_value(i + 2, 2))
            i = None


            # 定义callback函数用于实时显示结果
            def progress_callback(task_index, total_tasks, item_id, result, success_msg, error_msg):
                if result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> %s: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (total_tasks, task_index + 1, success_msg, item_id, result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> %s: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (total_tasks, task_index + 1, error_msg, item_id, result['result']))


            # 获取所有模板ID（多线程）
            lv_list_get_all_templateid = []


            def get_template_callback(future):
                result = future.result()
                if result['tag'] is True:
                    lv_list_get_all_templateid.append(result['result'][0]['templateid'])
                else:
                    lv_list_get_all_templateid.append('')
                progress_callback(len(lv_list_get_all_templateid) - 1, len(column_1_list),
                                  column_1_list[len(lv_list_get_all_templateid) - 1], result,
                                  "获取模板ID", "获取模板ID")


            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            futures = []
            for template in column_1_list:
                future = executor.submit(cus_zabbix_api.def_get_template, template)
                future.add_done_callback(get_template_callback)
                futures.append(future)
            wait(futures)  # 等待所有任务完成

            # 获取所有触发器ID（多线程）
            lv_list_get_all_template_itemid = []


            def get_trigger_callback(future, trigger_name):
                result = future.result()
                if result['tag'] is True:
                    lv_list_get_all_template_itemid.append(result['result'][0]['triggerid'])
                else:
                    lv_list_get_all_template_itemid.append('')
                progress_callback(len(lv_list_get_all_template_itemid) - 1, len(column_2_list),
                                  trigger_name, result,
                                  "获取触发器ID", "获取触发器ID")


            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            futures = []
            for templateid, trigger_name in zip(lv_list_get_all_templateid, column_2_list):
                future = executor.submit(cus_zabbix_api.def_get_template_trigger, templateid, trigger_name)
                future.add_done_callback(lambda f, name=trigger_name: get_trigger_callback(f, name))
                futures.append(future)
            wait(futures)  # 等待所有任务完成

            # 数据处理：去重和排序
            unit_column_1_list = list(set(column_5_list))
            unit_column_1_list.sort(key=column_5_list.index)

            # 准备要删除的标签数据
            lv_list_tmp_get_all_tag = []
            for o in range(len(column_5_list)):
                for i in range(len(unit_column_1_list)):
                    if column_5_list[o] == unit_column_1_list[i]:
                        lv_list_tmp_get_all_tag.append({unit_column_1_list[i]: {
                            "tag": cus_excel_op.get_cell_value(o + 2, 3),
                            "value": cus_excel_op.get_cell_value(o + 2, 4)
                        }})

            # 将标签数据转换为字典格式
            dict4 = {}
            for i in range(len(lv_list_tmp_get_all_tag)):
                for key in lv_list_tmp_get_all_tag[i].keys():
                    if key in unit_column_1_list:
                        dict4.setdefault(key, []).append(lv_list_tmp_get_all_tag[i][key])
            lv_list_get_all_pre_delete_tag = list(dict4.values())

            # 触发器ID去重和排序
            unit_column_2_list = list(set(lv_list_get_all_template_itemid))
            unit_column_2_list.sort(key=lv_list_get_all_template_itemid.index)

            # 获取所有触发器当前标签（多线程）
            lv_list_get_all_template_item_tags = []


            def get_tags_callback(future, trigger_id):
                result = future.result()
                if result['tag'] is True:
                    lv_list_get_all_template_item_tags.append(result['result'][0]['tags'])
                else:
                    lv_list_get_all_template_item_tags.append('')
                progress_callback(len(lv_list_get_all_template_item_tags) - 1, len(unit_column_2_list),
                                  trigger_id, result,
                                  "获取触发器标签", "获取触发器标签")


            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            futures = []
            for trigger_id in unit_column_2_list:
                future = executor.submit(cus_zabbix_api.def_get_template_trigger_tags, trigger_id)
                future.add_done_callback(lambda f, tid=trigger_id: get_tags_callback(f, tid))
                futures.append(future)
            wait(futures)  # 等待所有任务完成

            # 从触发器标签中移除指定的标签
            for i in range(len(lv_list_get_all_template_item_tags)):
                for o in lv_list_get_all_pre_delete_tag[i]:
                    try:
                        lv_list_get_all_template_item_tags[i].remove(o)
                    except:
                        continue


            # 更新触发器标签（多线程）
            def update_tags_callback(future, trigger_id):
                result = future.result()
                progress_callback(lv_sum_v01, len(unit_column_2_list),
                                  trigger_id, result,
                                  "模板移除触发器标签", "模板移除触发器标签")
                globals()['lv_sum_v01'] += 1


            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            futures = []
            lv_sum_v01 = 0
            for trigger_id, tags in zip(unit_column_2_list, lv_list_get_all_template_item_tags):
                future = executor.submit(cus_zabbix_api.def_update_template_trigger_tags, trigger_id, tags)
                future.add_done_callback(lambda f, tid=trigger_id: update_tags_callback(f, tid))
                futures.append(future)
            wait(futures)  # 等待所有任务完成
        # ![10_创建主机]
        elif args.create_host != 'create_host':
            cus_excel_op.load_excel('zabbix_api.xlsx', 10)

            # 获取各列数据（共19列）
            column_lists = [[] for _ in range(19)]  # 创建19个空列表
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]  # 删除标题行

            # 使用循环优化多列数据读取
            for i in range(len(column_1_list)):
                for col in range(2, 20):  # 第2到19列
                    column_lists[col - 1].append(cus_excel_op.get_cell_value(i + 2, col))

            # 解构为独立变量（保持与原代码兼容）
            column_2_list, column_3_list, column_4_list, column_5_list, \
                column_6_list, column_7_list, column_8_list, column_9_list, \
                column_10_list, column_11_list, column_12_list, column_13_list, \
                column_14_list, column_15_list, column_16_list, column_17_list, \
                column_18_list, column_19_list = column_lists[1:]


            # 定义进度回调函数
            def progress_callback(task_index, total_tasks, item_name, result, operation_name):
                """统一进度显示回调函数"""
                status_color = '32' if result['tag'] else '31'
                status_msg = '成功' if result['tag'] else '失败'
                print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> %s: \033[;%sm%s\033[0m %s 返回值为: \033[;%sm%s\033[0m' % (
                    total_tasks, task_index + 1, operation_name,
                    status_color, item_name, status_msg,
                    status_color, result['result']))


            # 1. 获取模板ID（多线程）
            def get_template_callback(future, index, template_name):
                """获取模板ID回调函数"""
                result = future.result()
                template_data = [{"templateid": int(result['result'][0]['templateid'])}] if result['tag'] else []
                progress_callback(index, len(column_2_list), template_name, result, "获取模板ID")
                return template_data


            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            futures = []
            for idx, template in enumerate(column_2_list):
                future = executor.submit(cus_zabbix_api.def_get_template, template)
                future.add_done_callback(lambda f, i=idx, t=template:
                                         lv_list_get_all_templateid.append(get_template_callback(f, i, t)))
                futures.append(future)
            lv_list_get_all_templateid = []
            wait(futures)

            # 2. 获取主机组ID（根据Zabbix版本）
            lv_dic_zbx_version = {
                '6.0': cus_zabbix_api.def_get_hostgroup_6_0,
                '6.4': cus_zabbix_api.def_get_hostgroup_6_4,
                '7.0': cus_zabbix_api.def_get_hostgroup_6_4
            }

            zbx_version = cus_zabbix_api.def_check_zbx_version()['result'][0:3]
            if zbx_version in lv_dic_zbx_version:
                def get_group_callback(future, index, group_name):
                    """获取主机组ID回调函数"""
                    result = future.result()
                    group_data = [{"groupid": int(result['result'][0]['groupid'])}] if result['tag'] else []
                    progress_callback(index, len(column_3_list), group_name, result, "获取主机组ID")
                    return group_data


                executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
                futures = []
                lv_list_get_all_groupid = []
                for idx, group in enumerate(column_3_list):
                    future = executor.submit(lv_dic_zbx_version[zbx_version], group)
                    future.add_done_callback(lambda f, i=idx, g=group:
                                             lv_list_get_all_groupid.append(get_group_callback(f, i, g)))
                    futures.append(future)
                wait(futures)


            # 3. 创建主机（多线程）
            def create_host_callback(future, index, host_name):
                """创建主机回调函数"""
                result = future.result()
                progress_callback(index, len(column_1_list), host_name, result, "创建主机")


            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            futures = []
            for idx in range(len(column_1_list)):
                print(idx, len(lv_list_get_all_groupid))
                future = executor.submit(
                    cus_zabbix_api.def_create_host,
                    column_1_list[idx],  # host_name
                    lv_list_get_all_templateid[idx] if idx <= len(lv_list_get_all_templateid) else [],
                    lv_list_get_all_groupid[idx] if idx <= len(lv_list_get_all_groupid) else [],
                    column_4_list[idx], column_5_list[idx], column_6_list[idx],
                    column_7_list[idx], column_8_list[idx], column_9_list[idx],
                    column_10_list[idx], column_11_list[idx], column_12_list[idx],
                    column_13_list[idx], column_14_list[idx], column_15_list[idx],
                    column_16_list[idx], column_17_list[idx], column_18_list[idx],
                    column_19_list[idx]
                )
                future.add_done_callback(lambda f, i=idx, h=column_1_list[idx]: create_host_callback(f, i, h))
                futures.append(future)
            wait(futures)
        elif args.delete_host != 'delete_host':
            # 1. 加载Excel文件（第10个工作表）
            cus_excel_op.load_excel('zabbix_api.xlsx', 10)

            # 获取主机名列（跳过表头）
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]


            # 2. 获取所有主机ID（第一阶段）
            def get_host_callback(future, index):
                """获取主机ID的回调函数"""
                try:
                    lv_result = future.result()
                    if lv_result['tag'] is True and lv_result['result']:
                        lv_list_get_all_hostid[index] = [lv_result['result'][0]['hostid']]
                        print(f"({index + 1}/{len(column_1_list)}) 获取主机ID成功: {column_1_list[index]}")
                    else:
                        lv_list_get_all_hostid[index] = []
                        print(f"({index + 1}/{len(column_1_list)}) \033[31m获取主机ID失败: {column_1_list[index]}\033[0m")
                except Exception as e:
                    lv_list_get_all_hostid[index] = []
                    print(f"({index + 1}/{len(column_1_list)}) \033[31m获取主机ID异常: {column_1_list[index]} | 错误: {str(e)}\033[0m")


            # 预初始化主机ID列表
            lv_list_get_all_hostid = [[] for _ in range(len(column_1_list))]

            # 使用线程池并行获取主机ID
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = []
                for idx, host_name in enumerate(column_1_list):
                    future = executor.submit(cus_zabbix_api.def_get_host, host_name)
                    future.add_done_callback(lambda f, i=idx: get_host_callback(f, i))
                    futures.append(future)
                wait(futures)  # 等待所有任务完成


            # 3. 删除主机（第二阶段）
            def delete_host_callback(future, index):
                """删除主机的回调函数"""
                try:
                    lv_result = future.result()
                    if lv_result['tag'] is True:
                        print(u'(\033[34m{}\033[0m/\033[34m{}\033[0m): 删除主机: \033[32m{}\033[0m 成功 | 返回值: \033[32m{}\033[0m'
                              .format(len(column_1_list), index + 1, column_1_list[index], lv_result['result']))
                    else:
                        print(u'(\033[31m{}\033[0m/\033[31m{}\033[0m): 删除主机: \033[31m{}\033[0m 失败 | 返回值: \033[31m{}\033[0m'
                              .format(len(column_1_list), index + 1, column_1_list[index], lv_result['result']))
                except Exception as e:
                    print(u'(\033[31m{}\033[0m/\033[31m{}\033[0m): 删除主机异常: \033[31m{}\033[0m | 错误: \033[31m{}\033[0m'
                          .format(len(column_1_list), index + 1, column_1_list[index], str(e)))


            # 使用线程池并行删除主机
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = []
                for idx, host_ids in enumerate(lv_list_get_all_hostid):
                    if host_ids:  # 只处理成功获取到hostid的记录
                        future = executor.submit(cus_zabbix_api.def_delete_host, host_ids)
                        future.add_done_callback(lambda f, i=idx: delete_host_callback(f, i))
                        futures.append(future)
                    else:
                        print(u'(\033[33m{}\033[0m/\033[33m{}\033[0m): 跳过未找到的主机: \033[33m{}\033[0m'
                              .format(len(column_1_list), idx + 1, column_1_list[idx]))
                wait(futures)  # 等待所有任务完成
        # ![11_主机创建接口]
        elif args.massadd_host_interface != 'massadd_host_interface':
            # 1. 加载Excel数据（第11个工作表）
            cus_excel_op.load_excel('zabbix_api.xlsx', 11)

            # 获取主机名列（跳过表头）
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]

            # 2. 初始化接口参数列（优化为列表推导式）
            columns = {
                'ip': [], 'dns': [], 'port': [], 'type': [],
                'main': [], 'useip': [], 'details': [], 'bulk': [],
                'interface_ref': [], 'disabled': [], 'hostid': []
            }

            # 动态填充各列数据（修复了原代码中column_6重复添加的问题）
            for i in range(len(column_1_list)):
                columns['ip'].append(cus_excel_op.get_cell_value(i + 2, 2))
                columns['dns'].append(cus_excel_op.get_cell_value(i + 2, 3))
                columns['port'].append(cus_excel_op.get_cell_value(i + 2, 4))
                columns['type'].append(cus_excel_op.get_cell_value(i + 2, 5))
                columns['main'].append(cus_excel_op.get_cell_value(i + 2, 6))
                columns['useip'].append(cus_excel_op.get_cell_value(i + 2, 7))
                columns['details'].append(cus_excel_op.get_cell_value(i + 2, 8))
                columns['bulk'].append(cus_excel_op.get_cell_value(i + 2, 9))
                columns['interface_ref'].append(cus_excel_op.get_cell_value(i + 2, 10))
                columns['disabled'].append(cus_excel_op.get_cell_value(i + 2, 11))
                columns['hostid'].append(cus_excel_op.get_cell_value(i + 2, 12))


            # 3. 获取主机ID（第一阶段）
            def get_host_callback(future, index):
                """获取主机ID的回调函数"""
                try:
                    lv_result = future.result()
                    if lv_result['tag'] and lv_result['result']:
                        hostid = int(lv_result['result'][0]['hostid'])
                        lv_list_get_all_hostid[index] = [{"hostid": hostid}]
                        print(f"({index + 1}/{len(column_1_list)}) 获取主机ID成功: {column_1_list[index]} → {hostid}")
                    else:
                        lv_list_get_all_hostid[index] = []
                        print(f"({index + 1}/{len(column_1_list)}) \033[31m获取主机ID失败: {column_1_list[index]}\033[0m")
                except Exception as e:
                    lv_list_get_all_hostid[index] = []
                    print(f"({index + 1}/{len(column_1_list)}) \033[31m获取主机ID异常: {column_1_list[index]} | 错误: {str(e)}\033[0m")


            # 预初始化主机ID列表
            lv_list_get_all_hostid = [[] for _ in range(len(column_1_list))]

            # 使用线程池并行获取主机ID
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = []
                for idx, host_name in enumerate(column_1_list):
                    future = executor.submit(cus_zabbix_api.def_get_host, host_name)
                    future.add_done_callback(lambda f, i=idx: get_host_callback(f, i))
                    futures.append(future)
                wait(futures)


            # 4. 批量添加主机接口（第二阶段）
            def add_interface_callback(future, index):
                """添加接口的回调函数"""
                try:
                    lv_result = future.result()
                    status = "成功" if lv_result['tag'] else "失败"
                    color = "32" if lv_result['tag'] else "31"

                    # 构建接口参数摘要
                    params = f"IP: {columns['ip'][index]}, Port: {columns['port'][index]}, Type: {columns['type'][index]}"

                    print(u'(\033[;34m{}\033[0m/\033[;34m{}\033[0m): 主机 \033[{}m{}\033[0m 接口添加{} | {} | 返回值: \033[{}m{}\033[0m'
                    .format(
                        len(column_1_list), index + 1,
                        color, column_1_list[index],
                        status, params,
                        color, lv_result['result']
                    ))
                except Exception as e:
                    print(u'(\033[;31m{}\033[0m/\033[;31m{}\033[0m): 主机接口添加异常: \033[31m{}\033[0m | 错误: \033[31m{}\033[0m'
                          .format(len(column_1_list), index + 1, column_1_list[index], str(e)))


            # 使用线程池并行添加接口
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = []
                for idx in range(len(column_1_list)):
                    if lv_list_get_all_hostid[idx]:  # 只处理有效主机
                        future = executor.submit(
                            cus_zabbix_api.def_massadd_host_interface,
                            lv_list_get_all_hostid[idx],
                            columns['ip'][idx],
                            columns['dns'][idx],
                            columns['port'][idx],
                            columns['type'][idx],
                            columns['main'][idx],
                            columns['useip'][idx],
                            columns['details'][idx],
                            columns['bulk'][idx],
                            columns['interface_ref'][idx],
                            columns['disabled'][idx],
                            columns['hostid'][idx]
                        )
                        future.add_done_callback(lambda f, i=idx: add_interface_callback(f, i))
                        futures.append(future)
                    else:
                        print(u'(\033[;33m{}\033[0m/\033[;33m{}\033[0m): 跳过无效主机: \033[33m{}\033[0m'
                              .format(len(column_1_list), idx + 1, column_1_list[idx]))
                wait(futures)
        elif args.massremove_host_interface != 'massremove_host_interface':
            # 加载Excel文件（第11个工作表）
            cus_excel_op.load_excel('zabbix_api.xlsx', 11)

            # 获取各列数据
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]  # 删除标题行
            column_2_list = []
            column_3_list = []
            column_4_list = []

            # 使用列表推导式优化数据读取
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.get_cell_value(i + 2, 2))  # 接口类型
                column_3_list.append(cus_excel_op.get_cell_value(i + 2, 3))  # 主机名称
                column_4_list.append(cus_excel_op.get_cell_value(i + 2, 4))  # IP地址


            # 定义统一回调函数
            def progress_callback(index, total, item_name, result, operation):
                """统一进度显示回调函数"""
                color = '32' if result['tag'] else '31'
                status = '成功' if result['tag'] else '失败'
                print(u'(\033[;34m{}\033[0m/\033[;34m{}\033[0m): -> {}: \033[;{}m{}\033[0m {} 返回: \033[;{}m{}\033[0m'.format(
                    total, index + 1, operation, color, item_name, status, color, result['result']))


            # 1. 获取主机ID（多线程）
            def get_host_callback(future, index, host_name):
                """获取主机ID回调函数"""
                result = future.result()
                host_data = [result['result'][0]['hostid']] if result['tag'] else []
                progress_callback(index, len(column_3_list), host_name, result, "获取主机ID")
                return host_data


            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            futures = []
            lv_list_get_all_hostid = []

            for idx, host in enumerate(column_3_list):
                future = executor.submit(cus_zabbix_api.def_get_host, host)
                future.add_done_callback(lambda f, i=idx, h=host:
                                         lv_list_get_all_hostid.append(get_host_callback(f, i, h)))
                futures.append(future)

            wait(futures)  # 等待所有获取主机ID任务完成


            # 2. 批量删除主机接口（单线程执行，避免并发问题）
            def remove_interface_callback(future, index, host_name):
                """删除接口回调函数"""
                result = future.result()
                progress_callback(index, len(column_1_list), host_name, result, "删除主机接口")


            # 注意：此处使用单线程执行(executor=1)，因为批量删除操作可能有依赖关系
            executor = ThreadPoolExecutor(1)
            futures = []

            for idx in range(len(column_1_list)):
                # 检查数组边界
                hostid = lv_list_get_all_hostid[idx] if idx <= len(lv_list_get_all_hostid) else []

                future = executor.submit(
                    cus_zabbix_api.def_massremove_host_interface,
                    hostid,
                    column_2_list[idx],
                    column_3_list[idx],
                    column_4_list[idx]
                )

                # 使用方案1修复（推荐）
                future.add_done_callback(
                    lambda f, i=idx, h=column_1_list[idx]: remove_interface_callback(f, i, h)
                )

                futures.append(future)

            wait(futures)  # 等待所有删除操作完成
        # ![12_主机关联模板]
        elif args.massadd_host_template != 'massadd_host_template':
            # 1. 加载Excel数据（第12个工作表）
            cus_excel_op.load_excel('zabbix_api.xlsx', 12)

            # 获取主机名和模板名列（跳过表头）
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]
            column_2_list = [cus_excel_op.get_cell_value(i + 2, 2) for i in range(len(column_1_list))]


            # 2. 定义回调函数
            def get_host_callback(future, index):
                """获取主机ID的回调函数"""
                try:
                    lv_result = future.result()
                    if lv_result['tag'] and lv_result['result']:
                        hostid = int(lv_result['result'][0]['hostid'])
                        lv_list_get_all_hostid[index] = [{"hostid": hostid}]
                        print(f"({index + 1}/{len(column_1_list)}) 获取主机ID成功: {column_1_list[index]} → {hostid}")
                    else:
                        lv_list_get_all_hostid[index] = []
                        print(f"({index + 1}/{len(column_1_list)}) \033[31m获取主机ID失败: {column_1_list[index]}\033[0m")
                except Exception as e:
                    lv_list_get_all_hostid[index] = []
                    print(f"({index + 1}/{len(column_1_list)}) \033[31m获取主机ID异常: {column_1_list[index]} | 错误: {str(e)}\033[0m")


            def get_template_callback(future, index):
                """获取模板ID的回调函数"""
                try:
                    lv_result = future.result()
                    if lv_result['tag'] and lv_result['result']:
                        templateid = int(lv_result['result'][0]['templateid'])
                        lv_list_get_all_templateid[index] = [{"templateid": templateid}]
                        print(f"({index + 1}/{len(column_2_list)}) 获取模板ID成功: {column_2_list[index]} → {templateid}")
                    else:
                        lv_list_get_all_templateid[index] = []
                        print(f"({index + 1}/{len(column_2_list)}) \033[31m获取模板ID失败: {column_2_list[index]}\033[0m")
                except Exception as e:
                    lv_list_get_all_templateid[index] = []
                    print(f"({index + 1}/{len(column_2_list)}) \033[31m获取模板ID异常: {column_2_list[index]} | 错误: {str(e)}\033[0m")


            def add_template_callback(future, index):
                """关联模板的回调函数"""
                try:
                    lv_result = future.result()
                    host_name = column_1_list[index]
                    template_name = column_2_list[index]

                    if lv_result['tag']:
                        print(u'(\033[34m{}\033[0m/\033[34m{}\033[0m): 主机 \033[32m{}\033[0m 关联模板 \033[32m{}\033[0m 成功 | 返回值: {}'
                              .format(len(column_1_list), index + 1, host_name, template_name, lv_result['result']))
                    else:
                        print(u'(\033[31m{}\033[0m/\033[31m{}\033[0m): 主机 \033[31m{}\033[0m 关联模板 \033[31m{}\033[0m 失败 | 返回值: {} | 错误: {}'
                              .format(len(column_1_list), index + 1, host_name, template_name,
                                      lv_result['result'], lv_result.get('error', '未知')))
                except Exception as e:
                    print(u'(\033[31m{}\033[0m/\033[31m{}\033[0m): 关联模板异常: \033[31m{} -> {}\033[0m | 错误: {}'
                          .format(len(column_1_list), index + 1, column_1_list[index],
                                  column_2_list[index], str(e)))


            # 3. 预初始化结果列表
            lv_list_get_all_hostid = [[] for _ in range(len(column_1_list))]
            lv_list_get_all_templateid = [[] for _ in range(len(column_2_list))]

            # 4. 第一阶段：并行获取主机ID
            print("\n=== 开始获取主机ID ===")
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = []
                for idx, host_name in enumerate(column_1_list):
                    future = executor.submit(cus_zabbix_api.def_get_host, host_name)
                    future.add_done_callback(lambda f, i=idx: get_host_callback(f, i))
                    futures.append(future)
                wait(futures)

            # 5. 第二阶段：并行获取模板ID
            print("\n=== 开始获取模板ID ===")
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = []
                for idx, template_name in enumerate(column_2_list):
                    future = executor.submit(cus_zabbix_api.def_get_template, template_name)
                    future.add_done_callback(lambda f, i=idx: get_template_callback(f, i))
                    futures.append(future)
                wait(futures)

            # 6. 第三阶段：批量关联模板
            print("\n=== 开始关联模板 ===")
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = []
                for idx in range(len(column_1_list)):
                    if lv_list_get_all_hostid[idx] and lv_list_get_all_templateid[idx]:
                        future = executor.submit(
                            cus_zabbix_api.def_massadd_host_template,
                            lv_list_get_all_hostid[idx],
                            lv_list_get_all_templateid[idx]
                        )
                        future.add_done_callback(lambda f, i=idx: add_template_callback(f, i))
                        futures.append(future)
                    else:
                        print(u'(\033[33m{}\033[0m/\033[33m{}\033[0m): 跳过无效记录: 主机 \033[33m{}\033[0m -> 模板 \033[33m{}\033[0m'
                              .format(len(column_1_list), idx + 1, column_1_list[idx], column_2_list[idx]))
                wait(futures)
        elif args.massremove_host_templateids != 'massremove_host_templateids':
            # 加载Excel文件（第12个工作表）
            cus_excel_op.load_excel('zabbix_api.xlsx', 12)

            # 获取各列数据
            column_1_list = cus_excel_op.get_column_values(1)  # 主机名称列
            del column_1_list[0]  # 删除标题行
            column_2_list = []  # 模板名称列

            # 使用列表推导式读取模板名称数据
            column_2_list = [cus_excel_op.get_cell_value(i + 2, 2) for i in range(len(column_1_list))]


            # 定义统一回调函数
            def progress_callback(index, total, item_name, result, operation):
                """统一进度显示回调函数
                Args:
                    index: 当前任务序号
                    total: 总任务数
                    item_name: 操作对象名称
                    result: API返回结果
                    operation: 操作类型描述
                """
                color = '32' if result['tag'] else '31'
                status = '成功' if result['tag'] else '失败'
                print(u'(\033[;34m{}\033[0m/\033[;34m{}\033[0m): -> {}: \033[;{}m{}\033[0m {} 返回: \033[;{}m{}\033[0m'.format(
                    total, index + 1, operation, color, item_name, status, color, result['result']))


            # 1. 获取主机ID（多线程）
            def get_host_callback(future, index, host_name):
                """获取主机ID回调函数"""
                result = future.result()
                host_data = [result['result'][0]['hostid']] if result['tag'] else []
                progress_callback(index, len(column_1_list), host_name, result, "获取主机ID")
                return host_data


            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            futures = []
            lv_list_get_all_hostid = []

            for idx, host in enumerate(column_1_list):
                future = executor.submit(cus_zabbix_api.def_get_host, host)
                future.add_done_callback(lambda f, i=idx, h=host:
                                         lv_list_get_all_hostid.append(get_host_callback(f, i, h)))
                futures.append(future)

            wait(futures)  # 等待所有获取主机ID任务完成


            # 2. 获取模板ID（多线程）
            def get_template_callback(future, index, template_name):
                """获取模板ID回调函数"""
                result = future.result()
                template_data = [result['result'][0]['templateid']] if result['tag'] else []
                progress_callback(index, len(column_2_list), template_name, result, "获取模板ID")
                return template_data


            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            futures = []
            lv_list_get_all_templateid = []

            for idx, template in enumerate(column_2_list):
                future = executor.submit(cus_zabbix_api.def_get_template, template)
                future.add_done_callback(lambda f, i=idx, t=template:
                                         lv_list_get_all_templateid.append(get_template_callback(f, i, t)))
                futures.append(future)

            wait(futures)  # 等待所有获取模板ID任务完成


            # 3. 主机脱离模板（单线程执行，避免并发问题）
            def remove_template_callback(future, index, host_name):
                """主机脱离模板回调函数"""
                result = future.result()
                progress_callback(index, len(column_1_list), host_name, result, "主机脱离模板")


            # 使用单线程执行敏感操作
            executor = ThreadPoolExecutor(1)
            futures = []

            for idx in range(len(column_1_list)):
                # 检查数组边界
                hostid = lv_list_get_all_hostid[idx] if idx <= len(lv_list_get_all_hostid) else []
                templateid = lv_list_get_all_templateid[idx] if idx <= len(lv_list_get_all_templateid) else []

                future = executor.submit(
                    cus_zabbix_api.def_massremove_host_templateids,
                    hostid,
                    templateid
                )

                # 使用方案1修复（推荐）
                future.add_done_callback(
                    lambda f, i=idx, h=column_1_list[idx]: remove_template_callback(f, i, h)
                )

                futures.append(future)

            wait(futures)  # 等待所有脱离操作完成
        elif args.massremove_host_templateids_clear != 'massremove_host_templateids_clear':
            # 1. 加载Excel数据（第12个工作表）
            cus_excel_op.load_excel('zabbix_api.xlsx', 12)

            # 获取主机名和模板名列（跳过表头）
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]
            column_2_list = [cus_excel_op.get_cell_value(i + 2, 2) for i in range(len(column_1_list))]

            # 2. 预初始化结果列表
            lv_list_get_all_hostid = [[] for _ in range(len(column_1_list))]
            lv_list_get_all_templateid = [[] for _ in range(len(column_2_list))]


            # 3. 定义回调函数
            def get_host_callback(future, index):
                """获取主机ID的回调函数"""
                try:
                    lv_result = future.result()
                    if lv_result['tag'] and lv_result['result']:
                        hostid = lv_result['result'][0]['hostid']
                        lv_list_get_all_hostid[index] = [hostid]
                        print(f"({index + 1}/{len(column_1_list)}) 获取主机ID成功: {column_1_list[index]} → {hostid}")
                    else:
                        error = lv_result.get('error', '未知错误')
                        print(f"({index + 1}/{len(column_1_list)}) \033[31m获取主机ID失败: {column_1_list[index]} | 错误: {error}\033[0m")
                except Exception as e:
                    print(f"({index + 1}/{len(column_1_list)}) \033[31m获取主机ID异常: {column_1_list[index]} | 错误: {str(e)}\033[0m")


            def get_template_callback(future, index):
                """获取模板ID的回调函数"""
                try:
                    lv_result = future.result()
                    if lv_result['tag'] and lv_result['result']:
                        templateid = lv_result['result'][0]['templateid']
                        lv_list_get_all_templateid[index] = [templateid]
                        print(f"({index + 1}/{len(column_2_list)}) 获取模板ID成功: {column_2_list[index]} → {templateid}")
                    else:
                        error = lv_result.get('error', '未知错误')
                        print(f"({index + 1}/{len(column_2_list)}) \033[31m获取模板ID失败: {column_2_list[index]} | 错误: {error}\033[0m")
                except Exception as e:
                    print(f"({index + 1}/{len(column_2_list)}) \033[31m获取模板ID异常: {column_2_list[index]} | 错误: {str(e)}\033[0m")


            def remove_template_callback(future, index):
                """移除模板并清理监控项的回调函数"""
                try:
                    lv_result = future.result()
                    host_name = column_1_list[index]
                    template_name = column_2_list[index]

                    if lv_result['tag']:
                        print(u'(\033[34m{}\033[0m/\033[34m{}\033[0m): 主机 \033[32m{}\033[0m 脱离模板 \033[32m{}\033[0m 并清理监控项成功 | 影响项数: {}'
                              .format(len(column_1_list), index + 1, host_name, template_name, lv_result['result'].get('items_removed', '未知')))
                    else:
                        error = lv_result.get('error', lv_result.get('result', '未知错误'))
                        print(u'(\033[31m{}\033[0m/\033[31m{}\033[0m): 主机 \033[31m{}\033[0m 脱离模板 \033[31m{}\033[0m 失败 | 错误: {}'
                              .format(len(column_1_list), index + 1, host_name, template_name, error))
                except Exception as e:
                    print(u'(\033[31m{}\033[0m/\033[31m{}\033[0m): 移除模板异常: \033[31m{} -> {}\033[0m | 错误: {}'
                          .format(len(column_1_list), index + 1, column_1_list[index], column_2_list[index], str(e)))


            # 4. 第一阶段：并行获取主机ID（多线程）
            print("\n=== 开始获取主机ID ===")
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = [executor.submit(cus_zabbix_api.def_get_host, host) for host in column_1_list]
                for idx, future in enumerate(futures):
                    future.add_done_callback(lambda f, i=idx: get_host_callback(f, i))
                wait(futures)

            # 5. 第二阶段：并行获取模板ID（多线程）
            print("\n=== 开始获取模板ID ===")
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = [executor.submit(cus_zabbix_api.def_get_template, template) for template in column_2_list]
                for idx, future in enumerate(futures):
                    future.add_done_callback(lambda f, i=idx: get_template_callback(f, i))
                wait(futures)

            # 6. 第三阶段：串行移除模板（单线程，避免Zabbix服务器压力过大）
            print("\n=== 开始移除模板并清理监控项 ===")
            with ThreadPoolExecutor(1) as executor:  # 注意这里限制为单线程
                futures = []
                for idx in range(len(column_1_list)):
                    if lv_list_get_all_hostid[idx] and lv_list_get_all_templateid[idx]:
                        future = executor.submit(
                            cus_zabbix_api.def_massremove_host_templateids_clear,
                            lv_list_get_all_hostid[idx],
                            lv_list_get_all_templateid[idx]
                        )
                        future.add_done_callback(lambda f, i=idx: remove_template_callback(f, i))
                        futures.append(future)
                    else:
                        print(u'(\033[33m{}\033[0m/\033[33m{}\033[0m): 跳过无效记录: 主机 \033[33m{}\033[0m -> 模板 \033[33m{}\033[0m'
                              .format(len(column_1_list), idx + 1, column_1_list[idx], column_2_list[idx]))
                wait(futures)
        # ![13_主机关联主机组]
        elif args.massadd_host_groups != 'massadd_host_groups':
            # 1. 加载Excel数据（第13个工作表）
            cus_excel_op.load_excel('zabbix_api.xlsx', 13)

            # 获取主机名和主机组名列（跳过表头）
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]
            column_2_list = [cus_excel_op.get_cell_value(i + 2, 2) for i in range(len(column_1_list))]

            # 2. 预初始化结果列表
            lv_list_get_all_hostid = [[] for _ in range(len(column_1_list))]
            lv_list_get_all_groupid = [[] for _ in range(len(column_2_list))]


            # 3. 定义回调函数
            def get_host_callback(future, index):
                """获取主机ID的回调函数"""
                try:
                    lv_result = future.result()
                    if lv_result['tag'] and lv_result['result']:
                        hostid = int(lv_result['result'][0]['hostid'])
                        lv_list_get_all_hostid[index] = [{"hostid": hostid}]
                        print(f"({index + 1}/{len(column_1_list)}) 获取主机ID成功: {column_1_list[index]} → {hostid}")
                    else:
                        error = lv_result.get('error', '未知错误')
                        print(f"({index + 1}/{len(column_1_list)}) \033[31m获取主机ID失败: {column_1_list[index]} | 错误: {error}\033[0m")
                except Exception as e:
                    print(f"({index + 1}/{len(column_1_list)}) \033[31m获取主机ID异常: {column_1_list[index]} | 错误: {str(e)}\033[0m")


            def get_group_callback(future, index):
                """获取主机组ID的回调函数"""
                try:
                    lv_result = future.result()
                    if lv_result['tag'] and lv_result['result']:
                        groupid = int(lv_result['result'][0]['groupid'])
                        lv_list_get_all_groupid[index] = [{"groupid": groupid}]
                        print(f"({index + 1}/{len(column_2_list)}) 获取主机组ID成功: {column_2_list[index]} → {groupid}")
                    else:
                        error = lv_result.get('error', '未知错误')
                        print(f"({index + 1}/{len(column_2_list)}) \033[31m获取主机组ID失败: {column_2_list[index]} | 错误: {error}\033[0m")
                except Exception as e:
                    print(f"({index + 1}/{len(column_2_list)}) \033[31m获取主机组ID异常: {column_2_list[index]} | 错误: {str(e)}\033[0m")


            def add_group_callback(future, index):
                """关联主机组的回调函数"""
                try:
                    lv_result = future.result()
                    host_name = column_1_list[index]
                    group_name = column_2_list[index]

                    if lv_result['tag']:
                        print(u'(\033[34m{}\033[0m/\033[34m{}\033[0m): 主机 \033[32m{}\033[0m 关联主机组 \033[32m{}\033[0m 成功'
                              .format(len(column_1_list), index + 1, host_name, group_name))
                    else:
                        error = lv_result.get('error', lv_result.get('result', '未知错误'))
                        print(u'(\033[31m{}\033[0m/\033[31m{}\033[0m): 主机 \033[31m{}\033[0m 关联主机组 \033[31m{}\033[0m 失败 | 错误: {}'
                              .format(len(column_1_list), index + 1, host_name, group_name, error))
                except Exception as e:
                    print(u'(\033[31m{}\033[0m/\033[31m{}\033[0m): 关联主机组异常: \033[31m{} -> {}\033[0m | 错误: {}'
                          .format(len(column_1_list), index + 1, host_name, group_name, str(e)))


            # 4. 第一阶段：并行获取主机ID
            print("\n=== 开始获取主机ID ===")
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = []
                for idx, host_name in enumerate(column_1_list):
                    future = executor.submit(cus_zabbix_api.def_get_host, host_name)
                    future.add_done_callback(lambda f, i=idx: get_host_callback(f, i))
                    futures.append(future)
                wait(futures)

            # 5. 第二阶段：并行获取主机组ID（根据Zabbix版本选择API）
            print("\n=== 开始获取主机组ID ===")
            zbx_version = cus_zabbix_api.def_check_zbx_version()['result'][0:3]
            group_api_map = {
                '6.0': cus_zabbix_api.def_get_hostgroup_6_0,
                '6.4': cus_zabbix_api.def_get_hostgroup_6_4,
                '7.0': cus_zabbix_api.def_get_hostgroup_6_4
            }
            get_group_func = group_api_map.get(zbx_version, cus_zabbix_api.def_get_hostgroup_6_4)

            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = []
                for idx, group_name in enumerate(column_2_list):
                    future = executor.submit(get_group_func, group_name)
                    future.add_done_callback(lambda f, i=idx: get_group_callback(f, i))
                    futures.append(future)
                wait(futures)

            # 6. 第三阶段：批量关联主机组
            print("\n=== 开始关联主机组 ===")
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = []
                for idx in range(len(column_1_list)):
                    if lv_list_get_all_hostid[idx] and lv_list_get_all_groupid[idx]:
                        future = executor.submit(
                            cus_zabbix_api.def_massadd_host_groups,
                            lv_list_get_all_hostid[idx],
                            lv_list_get_all_groupid[idx]
                        )
                        future.add_done_callback(lambda f, i=idx: add_group_callback(f, i))
                        futures.append(future)
                    else:
                        print(u'(\033[33m{}\033[0m/\033[33m{}\033[0m): 跳过无效记录: 主机 \033[33m{}\033[0m -> 主机组 \033[33m{}\033[0m'
                              .format(len(column_1_list), idx + 1, column_1_list[idx], column_2_list[idx]))
                wait(futures)
        elif args.massremove_host_group != 'massremove_host_group':
            # 1. 加载Excel数据（第13个工作表）
            cus_excel_op.load_excel('zabbix_api.xlsx', 13)

            # 获取主机名和主机组名列（跳过表头）
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]
            column_2_list = [cus_excel_op.get_cell_value(i + 2, 2) for i in range(len(column_1_list))]

            # 2. 预初始化结果列表
            lv_list_get_all_hostid = [[] for _ in range(len(column_1_list))]
            lv_list_get_all_groupid = [[] for _ in range(len(column_2_list))]


            # 3. 定义回调函数
            def get_host_callback(future, index):
                """获取主机ID的回调函数"""
                try:
                    lv_result = future.result()
                    if lv_result['tag'] and lv_result['result']:
                        hostid = int(lv_result['result'][0]['hostid'])
                        lv_list_get_all_hostid[index] = [hostid]
                        print(f"({index + 1}/{len(column_1_list)}) 获取主机ID成功: {column_1_list[index]} → {hostid}")
                    else:
                        error = lv_result.get('error', '未知错误')
                        print(f"({index + 1}/{len(column_1_list)}) \033[31m获取主机ID失败: {column_1_list[index]} | 错误: {error}\033[0m")
                except Exception as e:
                    print(f"({index + 1}/{len(column_1_list)}) \033[31m获取主机ID异常: {column_1_list[index]} | 错误: {str(e)}\033[0m")


            def get_group_callback(future, index):
                """获取主机组ID的回调函数"""
                try:
                    lv_result = future.result()
                    if lv_result['tag'] and lv_result['result']:
                        groupid = int(lv_result['result'][0]['groupid'])
                        lv_list_get_all_groupid[index] = [groupid]
                        print(f"({index + 1}/{len(column_2_list)}) 获取主机组ID成功: {column_2_list[index]} → {groupid}")
                    else:
                        error = lv_result.get('error', '未知错误')
                        print(f"({index + 1}/{len(column_2_list)}) \033[31m获取主机组ID失败: {column_2_list[index]} | 错误: {error}\033[0m")
                except Exception as e:
                    print(f"({index + 1}/{len(column_2_list)}) \033[31m获取主机组ID异常: {column_2_list[index]} | 错误: {str(e)}\033[0m")


            def remove_group_callback(future, index):
                """移除主机组的回调函数"""
                try:
                    lv_result = future.result()
                    host_name = column_1_list[index]
                    group_name = column_2_list[index]

                    if lv_result['tag']:
                        print(u'(\033[34m{}\033[0m/\033[34m{}\033[0m): 主机 \033[32m{}\033[0m 脱离主机组 \033[32m{}\033[0m 成功'
                              .format(len(column_1_list), index + 1, host_name, group_name))
                    else:
                        error = lv_result.get('error', lv_result.get('result', '未知错误'))
                        print(u'(\033[31m{}\033[0m/\033[31m{}\033[0m): 主机 \033[31m{}\033[0m 脱离主机组 \033[31m{}\033[0m 失败 | 错误: {}'
                              .format(len(column_1_list), index + 1, host_name, group_name, error))
                except Exception as e:
                    print(u'(\033[31m{}\033[0m/\033[31m{}\033[0m): 移除主机组异常: \033[31m{} -> {}\033[0m | 错误: {}'
                          .format(len(column_1_list), index + 1, host_name, group_name, str(e)))


            # 4. 第一阶段：并行获取主机ID
            print("\n=== 开始获取主机ID ===")
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = []
                for idx, host_name in enumerate(column_1_list):
                    future = executor.submit(cus_zabbix_api.def_get_host, host_name)
                    future.add_done_callback(lambda f, i=idx: get_host_callback(f, i))
                    futures.append(future)
                wait(futures)

            # 5. 第二阶段：并行获取主机组ID（根据Zabbix版本选择API）
            print("\n=== 开始获取主机组ID ===")
            zbx_version = cus_zabbix_api.def_check_zbx_version()['result'][0:3]
            group_api_map = {
                '6.0': cus_zabbix_api.def_get_hostgroup_6_0,
                '6.4': cus_zabbix_api.def_get_hostgroup_6_4,
                '7.0': cus_zabbix_api.def_get_hostgroup_6_4
            }
            get_group_func = group_api_map.get(zbx_version, cus_zabbix_api.def_get_hostgroup_6_4)

            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = []
                for idx, group_name in enumerate(column_2_list):
                    future = executor.submit(get_group_func, group_name)
                    future.add_done_callback(lambda f, i=idx: get_group_callback(f, i))
                    futures.append(future)
                wait(futures)

            # 6. 第三阶段：串行移除主机组（单线程避免Zabbix服务器压力过大）
            print("\n=== 开始移除主机组 ===")
            with ThreadPoolExecutor(1) as executor:  # 注意这里限制为单线程
                futures = []
                for idx in range(len(column_1_list)):
                    if lv_list_get_all_hostid[idx] and lv_list_get_all_groupid[idx]:
                        future = executor.submit(
                            cus_zabbix_api.def_massremove_host_group,
                            lv_list_get_all_hostid[idx],
                            lv_list_get_all_groupid[idx]
                        )
                        future.add_done_callback(lambda f, i=idx: remove_group_callback(f, i))
                        futures.append(future)
                    else:
                        print(u'(\033[33m{}\033[0m/\033[33m{}\033[0m): 跳过无效记录: 主机 \033[33m{}\033[0m -> 主机组 \033[33m{}\033[0m'
                              .format(len(column_1_list), idx + 1, column_1_list[idx], column_2_list[idx]))
                wait(futures)
        # ![31_发现规则]
        elif args.create_discoveryrule != 'create_discoveryrule':
            # 1. 加载Excel数据（第31个工作表）
            cus_excel_op.load_excel('zabbix_api.xlsx', 31)

            # 获取第一列数据（跳过表头）
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]


            # 2. 定义回调函数
            def create_rule_callback(future, index):
                """创建发现规则的回调函数"""
                try:
                    lv_result = future.result()
                    template_name = cus_excel_op.get_cell_value(index + 2, 1)
                    rule_name = cus_excel_op.get_cell_value(index + 2, 2)

                    if lv_result['tag']:
                        print(u'(\033[34m{}\033[0m/\033[34m{}\033[0m): 模板 \033[32m{}\033[0m 创建发现规则 \033[32m{}\033[0m 成功 | 规则ID: {}'
                              .format(len(column_1_list), index + 1, template_name, rule_name, lv_result['result'].get('itemids', ['未知'])[0]))
                    else:
                        error = lv_result.get('error', lv_result.get('result', '未知错误'))
                        print(u'(\033[31m{}\033[0m/\033[31m{}\033[0m): 模板 \033[31m{}\033[0m 创建发现规则 \033[31m{}\033[0m 失败 | 错误: {}'
                              .format(len(column_1_list), index + 1, template_name, rule_name, error))
                except Exception as e:
                    print(u'(\033[31m{}\033[0m/\033[31m{}\033[0m): 创建发现规则异常: \033[31m{}\033[0m | 错误: {}'
                          .format(len(column_1_list), index + 1, cus_excel_op.get_cell_value(index + 2, 1), str(e)))


            # 3. 并行创建发现规则
            print("\n=== 开始创建发现规则 ===")
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = []
                for i in range(len(column_1_list)):
                    # 获取模板ID
                    template_result = cus_zabbix_api.def_get_template(cus_excel_op.get_cell_value(i + 2, 1))
                    if not template_result['tag'] or not template_result['result']:
                        print(u'(\033[33m{}\033[0m/\033[33m{}\033[0m): 跳过无效模板: \033[33m{}\033[0m'
                              .format(len(column_1_list), i + 1, cus_excel_op.get_cell_value(i + 2, 1)))
                        continue

                    templateid = "".join([o['templateid'] for o in template_result['result']])

                    # 提交创建任务
                    future = executor.submit(
                        cus_zabbix_api.def_create_discoveryrule,
                        templateid,
                        cus_excel_op.get_cell_value(i + 2, 2),  # 规则名称
                        cus_excel_op.get_cell_value(i + 2, 3),  # 键值
                        cus_excel_op.get_cell_value(i + 2, 4)  # 类型
                    )
                    future.add_done_callback(lambda f, idx=i: create_rule_callback(f, idx))
                    futures.append(future)

                # 等待所有任务完成
                wait(futures)
        elif args.delete_discoveryrule != 'delete_discoveryrule':
            # 1. 加载Excel数据（第31个工作表）
            cus_excel_op.load_excel('zabbix_api.xlsx', 31)

            # 获取第一列数据（跳过表头）
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]


            # 2. 定义回调函数
            def delete_rule_callback(future, index):
                """删除发现规则的回调函数"""
                try:
                    lv_result = future.result()
                    template_name = cus_excel_op.get_cell_value(index + 2, 1)
                    rule_name = cus_excel_op.get_cell_value(index + 2, 2)

                    if lv_result['tag']:
                        print(u'(\033[34m{}\033[0m/\033[34m{}\033[0m): 模板 \033[32m{}\033[0m 删除发现规则 \033[32m{}\033[0m 成功'
                              .format(len(column_1_list), index + 1, template_name, rule_name))
                    else:
                        error = lv_result.get('error', lv_result.get('result', '未知错误'))
                        print(u'(\033[31m{}\033[0m/\033[31m{}\033[0m): 模板 \033[31m{}\033[0m 删除发现规则 \033[31m{}\033[0m 失败 | 错误: {}'
                              .format(len(column_1_list), index + 1, template_name, rule_name, error))
                except Exception as e:
                    print(u'(\033[31m{}\033[0m/\033[31m{}\033[0m): 删除发现规则异常: \033[31m{}\033[0m | 错误: {}'
                          .format(len(column_1_list), index + 1, template_name, str(e)))


            # 3. 并行删除发现规则
            print("\n=== 开始删除发现规则 ===")
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = []
                for i in range(len(column_1_list)):
                    # 获取模板ID
                    template_result = cus_zabbix_api.def_get_template(cus_excel_op.get_cell_value(i + 2, 1))
                    if not template_result['tag'] or not template_result['result']:
                        print(u'(\033[33m{}\033[0m/\033[33m{}\033[0m): 跳过无效模板: \033[33m{}\033[0m'
                              .format(len(column_1_list), i + 1, cus_excel_op.get_cell_value(i + 2, 1)))
                        continue

                    templateid = "".join([o['templateid'] for o in template_result['result']])
                    rule_name = cus_excel_op.get_cell_value(i + 2, 2)

                    # 获取发现规则ID
                    rule_result = cus_zabbix_api.def_get_discoveryrule(templateid, rule_name)
                    if not rule_result['tag'] or not rule_result['result']:
                        print(u'(\033[33m{}\033[0m/\033[33m{}\033[0m): 跳过未找到的规则: 模板 \033[33m{}\033[0m -> 规则 \033[33m{}\033[0m'
                              .format(len(column_1_list), i + 1, cus_excel_op.get_cell_value(i + 2, 1), rule_name))
                        continue

                    rule_ids = [o['itemid'] for o in rule_result['result']]

                    # 提交删除任务
                    future = executor.submit(
                        cus_zabbix_api.def_delete_discoveryrule,
                        rule_ids
                    )
                    future.add_done_callback(lambda f, idx=i: delete_rule_callback(f, idx))
                    futures.append(future)

                # 等待所有任务完成
                wait(futures)
        # ![32_模板创建监控项原型]
        elif args.create_itemprototype != 'create_itemprototype':
            # 1. 加载Excel数据（第32个工作表）
            cus_excel_op.load_excel('zabbix_api.xlsx', 32)

            # 获取第一列数据（跳过表头）
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]

            # 去重并保持原始顺序
            unit_column_1_list = sorted(set(column_1_list), key=column_1_list.index)


            # 2. 定义回调函数
            def create_prototype_callback(future, template_name, rule_name, item_name):
                """创建监控项原型的回调函数"""
                try:
                    lv_result = future.result()
                    if lv_result['tag']:
                        print(u'模板 \033[32m{}\033[0m 发现规则 \033[32m{}\033[0m 创建监控项原型 \033[32m{}\033[0m 成功 | 原型ID: {}'
                              .format(template_name, rule_name, item_name, lv_result['result'].get('itemids', ['未知'])[0]))
                    else:
                        error = lv_result.get('error', lv_result.get('result', '未知错误'))
                        print(u'模板 \033[31m{}\033[0m 发现规则 \033[31m{}\033[0m 创建监控项原型 \033[31m{}\033[0m 失败 | 错误: {}'
                              .format(template_name, rule_name, item_name, error))
                except Exception as e:
                    print(u'创建监控项原型异常: 模板 \033[31m{}\033[0m 规则 \033[31m{}\033[0m 项 \033[31m{}\033[0m | 错误: {}'
                          .format(template_name, rule_name, item_name, str(e)))


            # 3. 并行创建监控项原型
            print("\n=== 开始创建监控项原型 ===")
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                for i, template_name in enumerate(unit_column_1_list):
                    print(f"\n正在处理模板: {template_name} ({i + 1}/{len(unit_column_1_list)})")

                    # 获取模板ID
                    template_result = cus_zabbix_api.def_get_template(template_name)
                    if not template_result['tag'] or not template_result['result']:
                        print(f"  \033[33m跳过无效模板: {template_name}\033[0m")
                        continue

                    template_ids = ','.join([u['templateid'] for u in template_result['result']])

                    # 处理该模板下的所有规则
                    futures = []
                    for o in [o for o in range(len(column_1_list)) if column_1_list[o] == template_name]:
                        # 获取发现规则ID
                        rule_name = cus_excel_op.get_cell_value(o + 2, 2)
                        rule_result = cus_zabbix_api.def_get_discoveryrule(
                            "".join([i_02['templateid'] for i_02 in cus_zabbix_api.def_get_template(cus_excel_op.get_cell_value(o + 2, 1))]),
                            rule_name
                        )

                        if not rule_result['tag'] or not rule_result['result']:
                            print(f"  \033[33m跳过未找到的发现规则: {rule_name}\033[0m")
                            continue

                        rule_ids = ",".join([i_01['itemid'] for i_01 in rule_result['result']])

                        # 准备监控项原型参数
                        item_name = cus_excel_op.get_cell_value(o + 2, 3)
                        key = cus_excel_op.get_cell_value(o + 2, 4)
                        type_ = cus_excel_op.get_cell_value(o + 2, 5)
                        value_type = cus_excel_op.get_cell_value(o + 2, 6)
                        delay = cus_excel_op.get_cell_value(o + 2, 7)
                        history = cus_excel_op.get_cell_value(o + 2, 8)
                        trends = cus_excel_op.get_cell_value(o + 2, 9)

                        # 提交创建任务
                        future = executor.submit(
                            cus_zabbix_api.def_create_itemprototype,
                            rule_ids,
                            template_ids,
                            item_name,
                            key,
                            type_,
                            value_type,
                            delay,
                            history,
                            trends
                        )
                        future.add_done_callback(
                            lambda f, t=template_name, r=rule_name, i=item_name: create_prototype_callback(f, t, r, i)
                        )
                        futures.append(future)

                    # 等待当前模板的所有任务完成
                    wait(futures)
                    print(f"模板 {template_name} 处理完成")
        elif args.delete_itemprototype != 'delete_itemprototype':
            # 加载Excel文件
            cus_excel_op.load_excel('zabbix_api.xlsx', 32)

            # 获取数据列并去重
            column_1_list = cus_excel_op.get_column_values(1)[1:]  # 跳过标题行
            unit_column_1_list = sorted(set(column_1_list), key=column_1_list.index)  # 去重保持顺序


            # 定义进度回调函数
            def progress_callback(current, total, item_name, result, stage):
                """显示操作进度和结果"""
                status = '成功' if result['tag'] else '失败'
                color = '32' if result['tag'] else '31'
                print(f'(\033[34m{current}\033[0m/\033[34m{total}\033[0m) [{stage}] \033[{color}m{item_name}\033[0m {status}: \033[{color}m{result["result"]}\033[0m')


            # 定义处理函数
            def process_item(o):
                """处理单个监控项原型的删除"""
                try:
                    # 获取Excel数据
                    template_name = cus_excel_op.get_cell_value(o + 2, 1)
                    discovery_key = cus_excel_op.get_cell_value(o + 2, 2)
                    item_key = cus_excel_op.get_cell_value(o + 2, 5)

                    # 获取模板ID
                    template_result = cus_zabbix_api.def_get_template(template_name)
                    if not template_result['tag']:
                        return {'tag': False, 'result': f"模板获取失败: {template_result['result']}"}

                    template_id = template_result['result'][0]['templateid']
                    progress_callback(o + 1, len(column_1_list), template_name, template_result, "获取模板")

                    # 获取发现规则
                    discovery_result = cus_zabbix_api.def_get_discoveryrule(template_id, discovery_key)
                    if not discovery_result['tag']:
                        return {'tag': False, 'result': f"发现规则获取失败: {discovery_result['result']}"}

                    discovery_ids = ",".join([i['itemid'] for i in discovery_result['result']])
                    progress_callback(o + 1, len(column_1_list), discovery_key, discovery_result, "获取发现规则")

                    # 获取监控项原型
                    item_result = cus_zabbix_api.def_get_itemprototype_item(discovery_ids, item_key)
                    if not item_result['tag']:
                        return {'tag': False, 'result': f"监控项原型获取失败: {item_result['result']}"}

                    progress_callback(o + 1, len(column_1_list), item_key, item_result, "获取监控项原型")

                    # 删除监控项原型
                    item_ids = [x['itemid'] for x in item_result['result']]
                    delete_result = cus_zabbix_api.def_delete_itemprototype(item_ids)
                    progress_callback(o + 1, len(column_1_list), f"{len(item_ids)}项", delete_result, "删除操作")

                    return delete_result

                except Exception as e:
                    return {'tag': False, 'result': f"处理异常: {str(e)}"}


            # 使用线程池处理
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                # 按去重后的模板分组处理
                for i, unique_template in enumerate(unit_column_1_list):
                    # 获取该模板对应的所有行
                    tasks = [o for o in range(len(column_1_list)) if column_1_list[o] == unique_template]

                    # 提交任务
                    futures = []
                    for o in tasks:
                        future = executor.submit(process_item, o)
                        futures.append(future)

                    # 等待当前模板的所有任务完成
                    for future in as_completed(futures):
                        result = future.result()
                        if not result['tag']:
                            print(f"\033[31m错误: {result['result']}\033[0m")
        # ![33_模板创建触发器]
        elif args.create_template_triggerprototype != 'create_template_triggerprototype':
            # 加载Excel文件（第33个工作表）
            cus_excel_op.load_excel('zabbix_api.xlsx', 33)

            # 获取第一列数据（跳过标题行）
            column_1_list = cus_excel_op.get_column_values(1)[1:]


            # 定义进度回调函数
            def progress_callback(index, total, item_name, result, operation):
                """统一进度显示回调函数"""
                status_color = '32' if result['tag'] else '31'
                status_msg = '成功' if result['tag'] else '失败'
                print(u'(\033[;34m{}\033[0m/\033[;34m{}\033[0m): -> {}: \033[;{}m{}\033[0m {} 返回: \033[;{}m{}\033[0m'.format(
                    total, index + 1, operation, status_color, item_name, status_msg, status_color, result['result']))


            # 定义触发器原型创建函数
            def create_trigger_prototype(index):
                """创建触发器原型并返回结果"""
                try:
                    # 获取Excel中的参数
                    template_name = cus_excel_op.get_cell_value(index + 2, 1)
                    trigger_name = cus_excel_op.get_cell_value(index + 2, 2)
                    expression = cus_excel_op.get_cell_value(index + 2, 3)
                    priority = cus_excel_op.get_cell_value(index + 2, 4)

                    # 调用API创建触发器原型
                    result = cus_zabbix_api.def_create_template_triggerprototype(
                        template_name, trigger_name, expression, priority
                    )

                    # 返回结果和相关信息
                    return {
                        'index': index,
                        'trigger_name': trigger_name,
                        'result': result
                    }
                except Exception as e:
                    return {
                        'index': index,
                        'trigger_name': 'N/A',
                        'result': {'tag': False, 'result': str(e)}
                    }


            # 使用线程池处理
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = []
                total_tasks = len(column_1_list)

                # 提交所有任务
                for i in range(len(column_1_list)):
                    future = executor.submit(create_trigger_prototype, i)
                    future.add_done_callback(
                        lambda f: progress_callback(
                            f.result()['index'],
                            total_tasks,
                            f.result()['trigger_name'],
                            f.result()['result'],
                            "创建触发器原型"
                        )
                    )
                    futures.append(future)

                # 等待所有任务完成
                wait(futures)

            # 输出总结信息
            success_count = sum(1 for f in futures if f.result()['result']['tag'])
            print(f"\n操作完成: 成功 {success_count}/{total_tasks}，失败 {total_tasks - success_count}/{total_tasks}")
        elif args.delete_template_triggerprototype != 'delete_template_triggerprototype':
            # 加载Excel文件（第33个工作表）
            cus_excel_op.load_excel('zabbix_api.xlsx', 33)

            # 获取第三列数据（跳过标题行）
            column_1_list = cus_excel_op.get_column_values(3)[1:]


            # 定义进度回调函数
            def progress_callback(index, total, trigger_name, result, stage):
                """统一进度显示回调函数"""
                status_color = '32' if result['tag'] else '31'
                status_msg = '成功' if result['tag'] else '失败'
                print(u'(\033[;34m{}\033[0m/\033[;34m{}\033[0m): [{}] \033[;{}m{}\033[0m {} 返回: \033[;{}m{}\033[0m'.format(
                    index + 1, total, stage, status_color, trigger_name, status_msg, status_color, result['result']))


            # 定义处理函数
            def process_triggerprototype(index):
                """处理单个触发器原型的删除"""
                try:
                    # 获取模板名称
                    template_name = cus_excel_op.get_cell_value(index + 2, 1)

                    # 获取触发器原型ID
                    get_result = cus_zabbix_api.def_get_template_triggerprototype(template_name)
                    if not get_result['tag']:
                        return {
                            'index': index,
                            'trigger_name': template_name,
                            'result': {'tag': False, 'result': f"获取触发器原型失败: {get_result['result']}"}
                        }

                    progress_callback(index, len(column_1_list), template_name, get_result, "获取触发器原型")

                    # 删除触发器原型
                    triggerprototype_ids = [x['triggerid'] for x in get_result['result']] if get_result['result'] else []
                    if not triggerprototype_ids:
                        return {
                            'index': index,
                            'trigger_name': template_name,
                            'result': {'tag': True, 'result': "没有找到可删除的触发器原型"}
                        }

                    delete_result = cus_zabbix_api.def_delete_template_triggerprototype(triggerprototype_ids)
                    progress_callback(index, len(column_1_list), template_name, delete_result, "删除触发器原型")

                    return {
                        'index': index,
                        'trigger_name': template_name,
                        'result': delete_result
                    }

                except Exception as e:
                    return {
                        'index': index,
                        'trigger_name': template_name,
                        'result': {'tag': False, 'result': f"处理异常: {str(e)}"}
                    }


            # 使用线程池处理
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = []
                total_tasks = len(column_1_list)

                # 提交所有任务
                for i in range(len(column_1_list)):
                    future = executor.submit(process_triggerprototype, i)
                    futures.append(future)

                # 等待所有任务完成
                wait(futures)

            # 统计结果
            success_count = sum(1 for f in futures if f.result()['result']['tag'])
            print(f"\n操作完成: 成功 {success_count}/{total_tasks}，失败 {total_tasks - success_count}/{total_tasks}")

        # ![导出所有模板]
        elif args.export_configuration != 'export_configuration':
            # 准备输出文件
            zbx_version = cus_zabbix_api.def_check_zbx_version()['result']
            output_file = f'trans/{zbx_version}_所有模板.txt'

            # 清空或创建文件
            with open(output_file, 'w') as f:
                f.write("序号,模板ID,模板名称,数据源\n")  # 写入CSV头部

            # 获取所有模板信息
            templates = cus_zabbix_api.def_get_all_templateid()['result']
            template_ids = [t['templateid'] for t in templates]
            template_names = [t['host'] for t in templates]


            # 定义进度回调函数
            def progress_callback(index, total, template_name, template_id, result):
                """显示导出进度和结果"""
                if result['tag']:
                    status = f'\033[32m成功\033[0m'
                    details = f'数据源: \033[32m{result["result"]}\033[0m'
                else:
                    status = f'\033[31m失败\033[0m'
                    details = f'错误: \033[31m{result["result"]}\033[0m'

                print(f'({index}/{total}) 导出模板 [{status}]: \033[34m{template_name}\033[0m (ID: {template_id}) {details}')


            # 定义导出处理函数
            def export_template(template_id, index):
                """处理单个模板导出"""
                try:
                    result = cus_zabbix_api.def_export_configuration(template_id)

                    # 写入文件
                    with open(output_file, 'a') as f:
                        f.write(f"{index + 1},{template_id},{template_names[index]},{result['result'] if result['tag'] else '导出失败'}\n")

                    return {
                        'index': index,
                        'template_id': template_id,
                        'template_name': template_names[index],
                        'result': result
                    }
                except Exception as e:
                    return {
                        'index': index,
                        'template_id': template_id,
                        'template_name': template_names[index],
                        'result': {'tag': False, 'result': str(e)}
                    }


            # 使用线程池处理
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = []
                total = len(template_ids)

                # 提交所有导出任务
                for idx, template_id in enumerate(template_ids):
                    future = executor.submit(export_template, template_id, idx)
                    future.add_done_callback(
                        lambda f: progress_callback(
                            f.result()['index'] + 1,
                            total,
                            f.result()['template_name'],
                            f.result()['template_id'],
                            f.result()['result']
                        )
                    )
                    futures.append(future)

                # 等待所有任务完成
                wait(futures)

            # 统计结果
            success_count = sum(1 for f in futures if f.result()['result']['tag'])
            print(f"\n导出完成: 成功 \033[32m{success_count}\033[0m/{len(template_ids)}, 失败 \033[31m{len(template_ids) - success_count}\033[0m/{len(template_ids)}")
            print(f"结果已保存到: \033[34m{output_file}\033[0m")
        # ![导入所有模板]
        elif args.import_configuration != 'import_configuration':
            # 准备导入文件
            zbx_version = cus_zabbix_api.def_check_zbx_version()['result'][0:3]
            import_file = f'trans/{zbx_version}_所有模板.txt'

            # 版本适配检查
            version_adapters = {
                '5.0': cus_zabbix_api.def_import_configuration_5_0,
                '6.0': cus_zabbix_api.def_import_configuration_6_0,
                '6.4': cus_zabbix_api.def_import_configuration_6_4,
                '7.0': cus_zabbix_api.def_import_configuration_6_4
            }

            if zbx_version not in version_adapters:
                print(f"\033[31m错误: 当前Zabbix版本 '{zbx_version}' 未适配，无法导入配置\033[0m")
                exit(1)

            # 读取导入文件
            with open(import_file, 'r', encoding='utf-8') as f:
                all_data = [line.strip() for line in f.readlines()[1:]]  # 跳过标题行

            # 解析数据
            templates = []
            for line in all_data:
                parts = line.split(",", 3)
                if len(parts) == 4:
                    templates.append({
                        'index': parts[0],
                        'id': parts[1],
                        'name': parts[2],
                        'source': parts[3]
                    })


            # 定义进度回调函数
            def progress_callback(index, total, name, template_id, result, is_retry=False):
                """显示导入进度和结果"""
                operation = "重新导入" if is_retry else "导入"
                if result['result'] is True:
                    status = f'\033[32m成功\033[0m'
                    print(f'({index}/{total}) {operation}模板 [{status}]: \033[34m{name}\033[0m (ID: {template_id})')
                else:
                    status = f'\033[31m失败\033[0m'
                    print(f'({index}/{total}) {operation}模板 [{status}]: \033[34m{name}\033[0m (ID: {template_id})')
                    print(f"错误详情: \033[31m{result['result']}\033[0m")


            # 定义导入处理函数
            def import_template(template, adapter, is_retry=False):
                """处理单个模板导入"""
                try:
                    result = adapter(template['source'])
                    return {
                        'template': template,
                        'result': result,
                        'is_retry': is_retry,
                        'success': result['result'] is True
                    }
                except Exception as e:
                    return {
                        'template': template,
                        'result': {'result': str(e)},
                        'is_retry': is_retry,
                        'success': False
                    }


            # 首次导入
            failed_templates = []
            with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                futures = []
                for template in templates:
                    future = executor.submit(
                        import_template,
                        template,
                        version_adapters[zbx_version]
                    )
                    futures.append(future)

                for future in as_completed(futures):
                    res = future.result()
                    progress_callback(
                        int(res['template']['index']),
                        len(templates),
                        res['template']['name'],
                        res['template']['id'],
                        res['result'],
                        res['is_retry']
                    )
                    if not res['success']:
                        failed_templates.append(res['template'])

            # 重试失败的任务（最多重试3次）
            max_retries = 3
            for retry_count in range(max_retries):
                if not failed_templates:
                    break

                print(f"\n\033[33m开始第 {retry_count + 1} 次重试，剩余 {len(failed_templates)} 个模板\033[0m")

                retry_results = []
                with ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT) as executor:
                    futures = []
                    for template in failed_templates:
                        future = executor.submit(
                            import_template,
                            template,
                            version_adapters[zbx_version],
                            True
                        )
                        futures.append(future)

                    new_failed = []
                    for future in as_completed(futures):
                        res = future.result()
                        progress_callback(
                            int(res['template']['index']),
                            len(templates),
                            res['template']['name'],
                            res['template']['id'],
                            res['result'],
                            res['is_retry']
                        )
                        if not res['success']:
                            new_failed.append(res['template'])

                failed_templates = new_failed

            # 最终统计
            success_count = len(templates) - len(failed_templates)
            print(f"\n导入完成: 成功 \033[32m{success_count}\033[0m/{len(templates)}, 失败 \033[31m{len(failed_templates)}\033[0m/{len(templates)}")
            if failed_templates:
                print("\n以下模板导入失败:")
                for t in failed_templates:
                    print(f"  - {t['name']} (ID: {t['id']})")

