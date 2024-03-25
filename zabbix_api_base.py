#!/usr/bin/python3
# coding:utf-8

import argparse
from collections import defaultdict
import base64
import datetime
from datetime import datetime
import hashlib
import hmac
import inspect
import json
import openpyxl
import os
from concurrent.futures import ThreadPoolExecutor
import re
import sys
import time
from time import mktime
import requests
from requests.adapters import HTTPAdapter
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import zabbix_api
from zabbix_api import CusZabbixApi
from zabbix_api import CusExcelOp
from zabbix_api import CusPoEdit
from zabbix_api import GV_CPU_COUNT

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='zabbix  api ', usage='%(prog)s [options]')
    # ![01_创建主机组]
    parser.add_argument('-create_hostgroup', nargs='?', metavar='无参数', dest='create_hostgroup', default='create_hostgroup',
                        help=u"创建主机组")
    parser.add_argument('-delete_hostgroup', nargs='?', metavar='无参数', dest='delete_hostgroup', default='delete_hostgroup',
                        help=u"删除主机组")
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
    parser.add_argument('-excel_zabbix_ui_to_poedit', nargs='?', metavar='无参数', dest='excel_zabbix_ui_to_poedit', default='excel_zabbix_ui_to_poedit',
                        help=u"从excel导出zabbix ui 6.0翻译文本到poedit")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 如有问题请联系作者QQ1284524409',
                        help=u"如有问题请联系作者QQ1284524409")

    args = parser.parse_args()
    cus_excel_op = CusExcelOp()

    if len(sys.argv) == 1:
        print(parser.print_help())
        # ![导出po到excel]
    elif args.poedit_zabbix_ui_to_excel != 'poedit_zabbix_ui_to_excel':
        title_name = ['注释', 'msgid', 'msgid_plural', 'msgstr', 'msgstr0', 'msgctxt']
        cus_excel_op.def_creat_excel()
        cus_excel_op.def_create_sheet("frontend")
        [cus_excel_op.def_set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]

        cus_poEdit = CusPoEdit()
        res_poreturn = cus_poEdit.def_translate("frontend.po")

        for i in range(len(res_poreturn['msgcomment'])):
            for x in range(1, 7):
                if x == 1:
                    cus_excel_op.def_set_cell_value(i + 2, x, res_poreturn['msgcomment'][i])
                elif x == 2:
                    cus_excel_op.def_set_cell_value(i + 2, x, res_poreturn['msgid'][i])
                elif x == 3:
                    cus_excel_op.def_set_cell_value(i + 2, x, res_poreturn['msgid_plural'][i])
                elif x == 4:
                    cus_excel_op.def_set_cell_value(i + 2, x, res_poreturn['msgstr'][i])
                elif x == 5:
                    cus_excel_op.def_set_cell_value(i + 2, x, res_poreturn['msgstr0'][i])
                elif x == 6:
                    cus_excel_op.def_set_cell_value(i + 2, x, res_poreturn['msgctxt'][i])
            i = i + 1
        cus_excel_op.def_save_create_xlsx('frontend.xlsx')
    elif args.excel_zabbix_ui_to_poedit != 'excel_zabbix_ui_to_poedit':
        cus_poEdit = CusPoEdit()
        for var_i in range(1,4):
            cus_excel_op.def_load_excel(file='trans/frontend_.xlsx', index=var_i)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = []
            column_3_list = []
            column_4_list = []
            column_5_list = []
            column_6_list = []
            with open('frontend_{0}.po'.format(cus_excel_op.sheet_name), 'w', encoding='utf-8') as s_hosts:
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
""".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), cus_excel_op.sheet_name,
                   time.mktime(time.strptime(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()), "%a %b %d %H:%M:%S %Y"))))
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.def_get_cell_value(i + 2, 2))
                column_3_list.append(cus_excel_op.def_get_cell_value(i + 2, 3))
                column_4_list.append(cus_excel_op.def_get_cell_value(i + 2, 4))
                column_5_list.append(cus_excel_op.def_get_cell_value(i + 2, 5))
                column_6_list.append(cus_excel_op.def_get_cell_value(i + 2, 6))
                cus_poEdit.def_create_pofile('frontend_{0}.po'.format(cus_excel_op.sheet_name), column_1_list[i], column_2_list[i], column_3_list[i],
                                             column_4_list[i], column_5_list[i], column_6_list[i])
            print(len(column_2_list))
    else:
        cus_zabbix_api = CusZabbixApi()
        # ![01_创建主机组]
        if args.create_hostgroup != 'create_hostgroup':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=1)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            # 去重
            unit_column_1_list = list(set(column_1_list))
            # 使用index保持不乱序
            unit_column_1_list.sort(key=column_1_list.index)
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_sum_v01 = 0
            for lv_result in executor.map(cus_zabbix_api.def_create_hostgroup, unit_column_1_list):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 创建主机组: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(unit_column_1_list), lv_sum_v01 + 1, unit_column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 创建主机组: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(unit_column_1_list), lv_sum_v01 + 1, unit_column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1
        elif args.delete_hostgroup != 'delete_hostgroup':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=1)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            # 去重
            unit_column_1_list = list(set(column_1_list))
            # 使用index保持不乱序
            unit_column_1_list.sort(key=column_1_list.index)

            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_sum_v01 = 0
            lv_list_all_hostgroupid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_hostgroup_6_0, unit_column_1_list):
                if lv_result['tag'] is True:
                    lv_list_all_hostgroupid.append([lv_result['result'][0]['groupid']])
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 获取主机组ID: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(unit_column_1_list), lv_sum_v01 + 1, unit_column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1
            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_delete_hostgroup, lv_list_all_hostgroupid):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 删除主机组: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(unit_column_1_list), lv_sum_v01 + 1, unit_column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 删除主机组: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(unit_column_1_list), lv_sum_v01 + 1, unit_column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1
        # ![02_创建模板]
        elif args.create_template != 'create_template':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=2)
            column_1_list = cus_excel_op.def_get_col_value(1)
            column_2_list = cus_excel_op.def_get_col_value(2)
            del column_1_list[0]
            del column_2_list[0]
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_all_hostgroupid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_hostgroup_6_0, column_2_list):
                if lv_result['tag'] is True:
                    lv_list_all_hostgroupid.append([{"groupid": int(lv_result['result'][0]['groupid'])}])
                else:
                    lv_list_all_hostgroupid.append([{"groupid": []}])
            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_create_template, column_1_list, lv_list_all_hostgroupid):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 创建模板: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 创建模板: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1

        elif args.delete_template != 'delete_template':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=2)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]

            lv_result = None
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_templateid = []
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append([lv_result['result'][0]['templateid']])
                else:
                    lv_list_get_all_templateid.append([])
            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_delete_template, lv_list_get_all_templateid):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 删除模板: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 删除模板: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1
        # ![02_模板添加主机组]
        elif args.massadd_template_groups != 'massadd_template_groups':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=2)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = cus_excel_op.def_get_col_value(2)
            del column_2_list[0]
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_templateid = []
            lv_list_get_all_hostgroupid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append([lv_result['result'][0]])
                else:
                    lv_list_get_all_templateid.append([])
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_hostgroup_6_0, column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_hostgroupid.append([{'groupid': lv_result['result'][0]['groupid']}])
                else:
                    lv_list_get_all_hostgroupid.append([{'groupid': ''}])
            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_massadd_template_groups, lv_list_get_all_templateid, lv_list_get_all_hostgroupid):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板添加主机组: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板添加主机组: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1

        elif args.massremove_template_groups != 'massremove_template_groups':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=2)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = cus_excel_op.def_get_col_value(2)
            del column_2_list[0]
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_templateid = []
            lv_list_get_all_hostgroupid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append([lv_result['result'][0]['templateid']])
                else:
                    lv_list_get_all_templateid.append([])
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_hostgroup_6_0, column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_hostgroupid.append([lv_result['result'][0]['groupid']])
                else:
                    lv_list_get_all_hostgroupid.append([])

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_massremove_template_groups, lv_list_get_all_templateid, lv_list_get_all_hostgroupid):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板移除主机组: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板移除主机组: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1
        # ![03_模板添加用户宏]
        elif args.massadd_template_macros != 'massadd_template_macros':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=3)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = cus_excel_op.def_get_col_value(2)
            del column_2_list[0]
            column_3_list = cus_excel_op.def_get_col_value(3)
            del column_3_list[0]
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_templateid = []
            lv_list_get_all_macro = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append([lv_result['result'][0]])
                else:
                    lv_list_get_all_templateid.append([])
            lv_int_i = None
            for lv_int_i in range(len(column_2_list)):
                lv_list_get_all_macro.append([{"macro": cus_excel_op.def_get_cell_value(lv_int_i + 2, 2), "value": str(cus_excel_op.def_get_cell_value(lv_int_i + 2, 3))}])

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_massadd_template_macros, lv_list_get_all_templateid, lv_list_get_all_macro):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板添加用户宏: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板添加用户宏: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1

        elif args.massremove_template_macros != 'massremove_template_macros':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=3)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = cus_excel_op.def_get_col_value(2)
            del column_2_list[0]
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_templateid = []
            lv_list_get_all_macro = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append([lv_result['result'][0]['templateid']])
                else:
                    lv_list_get_all_templateid.append([])
            lv_int_i = None
            for lv_int_i in range(len(column_2_list)):
                lv_list_get_all_macro.append([cus_excel_op.def_get_cell_value(lv_int_i + 2, 2)])

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_massremove_template_macros, lv_list_get_all_templateid, lv_list_get_all_macro):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板删除用户宏: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板删除用户宏: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1

        # ![04_模板关联模板]
        elif args.massadd_template_templates_link != 'massadd_template_templates_link':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=4)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = cus_excel_op.def_get_col_value(2)
            del column_2_list[0]
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_templateid = []
            lv_list_get_all_link_templateid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append([lv_result['result'][0]])
                else:
                    lv_list_get_all_templateid.append([])
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_link_templateid.append([lv_result['result'][0]])
                else:
                    lv_list_get_all_link_templateid.append([])

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_massadd_template_templates_link, lv_list_get_all_templateid, lv_list_get_all_link_templateid):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板关联模板: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板关联模板: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1

        elif args.massremove_templateids_clear != 'massremove_templateids_clear':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=4)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = cus_excel_op.def_get_col_value(2)
            del column_2_list[0]
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_templateid = []
            lv_list_get_all_link_templateid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append([lv_result['result'][0]['templateid']])
                else:
                    lv_list_get_all_templateid.append([])
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_link_templateid.append([lv_result['result'][0]['templateid']])
                else:
                    lv_list_get_all_link_templateid.append([])

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_massremove_templateids_clear, lv_list_get_all_templateid, lv_list_get_all_link_templateid):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板脱离模板清理主机监控项: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板脱离模板清理主机监控项: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1

        elif args.massremove_templateids_link != 'massremove_templateids_link':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=4)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = cus_excel_op.def_get_col_value(2)
            del column_2_list[0]
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_templateid = []
            lv_list_get_all_link_templateid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append([lv_result['result'][0]['templateid']])
                else:
                    lv_list_get_all_templateid.append([])
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_link_templateid.append([lv_result['result'][0]['templateid']])
                else:
                    lv_list_get_all_link_templateid.append([])

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_massremove_templateids_link, lv_list_get_all_templateid, lv_list_get_all_link_templateid):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板脱离模板保留主机监控项: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板脱离模板保留主机监控项: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1

        # ![05_模板更新标签]
        elif args.update_tags != 'update_tags':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=5)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            # 去重
            unit_column_1_list = list(set(column_1_list))
            # 使用index保持不乱序
            unit_column_1_list.sort(key=column_1_list.index)

            lv_list_get_all_tag = []
            lv_list_tmp_get_all_tag = []
            for o in range(len(column_1_list)):
                for i in range(len(unit_column_1_list)):
                    if column_1_list[o] == unit_column_1_list[i]:
                        lv_list_tmp_get_all_tag.append({unit_column_1_list[i]: {
                            "tag": cus_excel_op.def_get_cell_value(o + 2, 2), "value": cus_excel_op.def_get_cell_value(o + 2, 3)
                        }})
            dict4 = {}
            for i in range(len(lv_list_tmp_get_all_tag)):
                for key in lv_list_tmp_get_all_tag[i].keys():
                    if key in unit_column_1_list:
                        dict4.setdefault(key, []).append(lv_list_tmp_get_all_tag[i][key])
                    # else:
                    #     dict4[key] = lv_list_tmp_get_all_tag[i][key]
            lv_list_get_all_tag = list(dict4.values())

            column_2_list = cus_excel_op.def_get_col_value(2)
            del column_2_list[0]
            column_3_list = cus_excel_op.def_get_col_value(3)
            del column_3_list[0]
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_templateid = []
            lv_list_get_all_macro = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, unit_column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append(lv_result['result'][0]['templateid'])
                else:
                    lv_list_get_all_templateid.append('')

            lv_int_i = None
            for lv_int_i in range(len(column_2_list)):
                lv_list_get_all_macro.append([{"tag": cus_excel_op.def_get_cell_value(lv_int_i + 2, 2), "value": str(cus_excel_op.def_get_cell_value(lv_int_i + 2, 3))}])

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_update_tags, lv_list_get_all_templateid, lv_list_get_all_tag):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板更新标签: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(unit_column_1_list), lv_sum_v01 + 1, unit_column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板更新标签: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(unit_column_1_list), lv_sum_v01 + 1, unit_column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1

        elif args.delete_tags != 'delete_tags':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=5)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            # 去重
            unit_column_1_list = list(set(column_1_list))
            # 使用index保持不乱序
            unit_column_1_list.sort(key=column_1_list.index)

            lv_list_get_all_tag = []
            lv_list_tmp_get_all_tag = []
            for o in range(len(column_1_list)):
                for i in range(len(unit_column_1_list)):
                    if column_1_list[o] == unit_column_1_list[i]:
                        lv_list_tmp_get_all_tag.append({unit_column_1_list[i]: {
                            "tag": cus_excel_op.def_get_cell_value(o + 2, 2), "value": cus_excel_op.def_get_cell_value(o + 2, 3)
                        }})
            dict4 = {}
            for i in range(len(lv_list_tmp_get_all_tag)):
                for key in lv_list_tmp_get_all_tag[i].keys():
                    if key in unit_column_1_list:
                        dict4.setdefault(key, []).append(lv_list_tmp_get_all_tag[i][key])
                    # else:
                    #     dict4[key] = lv_list_tmp_get_all_tag[i][key]
            lv_list_get_all_pre_delete_tag = list(dict4.values())

            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_templateid = []
            lv_list_all_old_tag = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template_tags, unit_column_1_list):
                if lv_result['tag'] is True:
                    lv_list_all_old_tag.append(lv_result['result'][0]['tags'])
                else:
                    lv_list_all_old_tag.append('')
            for i in range(len(lv_list_all_old_tag)):
                for o in lv_list_get_all_pre_delete_tag[i]:
                    try:
                        lv_list_all_old_tag[i].remove(o)
                    except:
                        continue
            lv_list_get_all_templateid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, unit_column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append(lv_result['result'][0]['templateid'])
                else:
                    lv_list_get_all_templateid.append('')

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_update_tags, lv_list_get_all_templateid, lv_list_all_old_tag):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板移除标签: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(unit_column_1_list), lv_sum_v01 + 1, unit_column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板移除标签: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(unit_column_1_list), lv_sum_v01 + 1, unit_column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1

        # ![06_模板创建监控项]
        elif args.create_template_item != 'create_template_item':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=6)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = []
            column_3_list = []
            column_4_list = []
            column_5_list = []
            column_6_list = []
            column_7_list = []
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.def_get_cell_value(i + 2, 2))
                column_3_list.append(cus_excel_op.def_get_cell_value(i + 2, 3))
                column_4_list.append(cus_excel_op.def_get_cell_value(i + 2, 4))
                column_5_list.append(cus_excel_op.def_get_cell_value(i + 2, 5))
                column_6_list.append(cus_excel_op.def_get_cell_value(i + 2, 6))
                column_7_list.append(cus_excel_op.def_get_cell_value(i + 2, 7))
            i = None
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_templateid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append(lv_result['result'][0]['templateid'])
                else:
                    lv_list_get_all_templateid.append('')

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_create_template_item, lv_list_get_all_templateid,
                                          column_2_list, column_3_list, column_4_list, column_5_list, column_6_list, column_7_list):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板创建监控项: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板创建监控项: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1

        elif args.delete_template_item != 'delete_template_item':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=6)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_4_list = []
            for i in range(len(column_1_list)):
                column_4_list.append(cus_excel_op.def_get_cell_value(i + 2, 4))
            i = None

            lv_list_get_all_templateid = []
            lv_result = None
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append(lv_result['result'][0]['templateid'])
                else:
                    lv_list_get_all_templateid.append('')

            lv_list_get_all_template_itemid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template_item, lv_list_get_all_templateid, column_4_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_template_itemid.append([lv_result['result'][0]['itemid']])
                else:
                    lv_list_get_all_template_itemid.append([])

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_delete_template_item, lv_list_get_all_template_itemid):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板删除监控项: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板删除监控项: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1

        # ![07_模板更新监控项标签]
        elif args.update_template_item_tags != 'update_template_item_tags':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=7)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = []
            column_3_list = []
            column_4_list = []
            column_5_list = []
            column_6_list = []
            column_7_list = []
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.def_get_cell_value(i + 2, 2))
                column_3_list.append(cus_excel_op.def_get_cell_value(i + 2, 3))
                column_4_list.append(cus_excel_op.def_get_cell_value(i + 2, 4))
                column_5_list.append(cus_excel_op.def_get_cell_value(i + 2, 1) + '_' +
                                     cus_excel_op.def_get_cell_value(i + 2, 2))
            i = None
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_templateid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append(lv_result['result'][0]['templateid'])
                else:
                    lv_list_get_all_templateid.append('')

            lv_list_get_all_template_itemid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template_item, lv_list_get_all_templateid, column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_template_itemid.append(lv_result['result'][0]['itemid'])
                else:
                    lv_list_get_all_template_itemid.append('')

            # 去重
            unit_column_1_list = list(set(column_5_list))
            # 使用index保持不乱序
            unit_column_1_list.sort(key=column_5_list.index)

            lv_list_get_all_tag = []
            lv_list_tmp_get_all_tag = []
            for o in range(len(column_5_list)):
                for i in range(len(unit_column_1_list)):
                    if column_5_list[o] == unit_column_1_list[i]:
                        lv_list_tmp_get_all_tag.append({unit_column_1_list[i]: {
                            "tag": cus_excel_op.def_get_cell_value(o + 2, 3), "value": cus_excel_op.def_get_cell_value(o + 2, 4)
                        }})

            dict4 = {}
            for i in range(len(lv_list_tmp_get_all_tag)):
                for key in lv_list_tmp_get_all_tag[i].keys():
                    if key in unit_column_1_list:
                        dict4.setdefault(key, []).append(lv_list_tmp_get_all_tag[i][key])
                    # else:
                    #     dict4[key] = lv_list_tmp_get_all_tag[i][key]
            lv_list_get_all_pre_delete_tag = list(dict4.values())

            unit_column_2_list = list(set(lv_list_get_all_template_itemid))
            # 使用index保持不乱序
            unit_column_2_list.sort(key=lv_list_get_all_template_itemid.index)

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_update_template_item_tags, unit_column_2_list, lv_list_get_all_pre_delete_tag):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板更新监控项标签: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板更新监控项标签: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1

        elif args.delete_template_item_tags != 'delete_template_item_tags':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=7)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = []
            column_3_list = []
            column_4_list = []
            column_5_list = []
            column_6_list = []
            column_7_list = []
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.def_get_cell_value(i + 2, 2))
                column_3_list.append(cus_excel_op.def_get_cell_value(i + 2, 3))
                column_4_list.append(cus_excel_op.def_get_cell_value(i + 2, 4))
                column_5_list.append(cus_excel_op.def_get_cell_value(i + 2, 1) + '_' +
                                     cus_excel_op.def_get_cell_value(i + 2, 2))
            i = None

            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_templateid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append(lv_result['result'][0]['templateid'])
                else:
                    lv_list_get_all_templateid.append('')

            lv_list_get_all_template_itemid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template_item, lv_list_get_all_templateid, column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_template_itemid.append(lv_result['result'][0]['itemid'])
                else:
                    lv_list_get_all_template_itemid.append('')

            # 去重
            unit_column_1_list = list(set(column_5_list))
            # 使用index保持不乱序
            unit_column_1_list.sort(key=column_5_list.index)

            lv_list_get_all_tag = []
            lv_list_tmp_get_all_tag = []
            for o in range(len(column_5_list)):
                for i in range(len(unit_column_1_list)):
                    if column_5_list[o] == unit_column_1_list[i]:
                        lv_list_tmp_get_all_tag.append({unit_column_1_list[i]: {
                            "tag": cus_excel_op.def_get_cell_value(o + 2, 3), "value": cus_excel_op.def_get_cell_value(o + 2, 4)
                        }})

            dict4 = {}
            for i in range(len(lv_list_tmp_get_all_tag)):
                for key in lv_list_tmp_get_all_tag[i].keys():
                    if key in unit_column_1_list:
                        dict4.setdefault(key, []).append(lv_list_tmp_get_all_tag[i][key])
                    # else:
                    #     dict4[key] = lv_list_tmp_get_all_tag[i][key]
            lv_list_get_all_pre_delete_tag = list(dict4.values())

            unit_column_2_list = list(set(lv_list_get_all_template_itemid))
            # 使用index保持不乱序
            unit_column_2_list.sort(key=lv_list_get_all_template_itemid.index)

            lv_list_get_all_template_item_tags = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template_item_tags, unit_column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_template_item_tags.append(lv_result['result'][0]['tags'])
                else:
                    lv_list_get_all_template_item_tags.append('')

            for i in range(len(lv_list_get_all_template_item_tags)):
                for o in lv_list_get_all_pre_delete_tag[i]:
                    try:
                        lv_list_get_all_template_item_tags[i].remove(o)
                    except:
                        continue

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_update_template_item_tags, unit_column_2_list, lv_list_get_all_template_item_tags):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板移除监控项标签: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板移除监控项标签: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1
        # ![08_模板创建触发器]
        elif args.create_template_trigger != 'create_template_trigger':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=8)

            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = []
            column_3_list = []
            column_4_list = []
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.def_get_cell_value(i + 2, 2))
                column_3_list.append(cus_excel_op.def_get_cell_value(i + 2, 3))
                column_4_list.append(cus_excel_op.def_get_cell_value(i + 2, 4))

            lv_sum_v01 = 0
            lv_result = None
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            for lv_result in executor.map(cus_zabbix_api.def_create_template_trigger, column_1_list, column_2_list, column_3_list, column_4_list):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板创建触发器: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板创建触发器: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1
        elif args.delete_template_trigger != 'delete_template_trigger':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=8)

            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_5_list = []
            for i in range(len(column_1_list)):
                column_5_list.append(cus_excel_op.def_get_cell_value(i + 2, 5))

            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_templateid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_5_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append(lv_result['result'][0]['templateid'])
                else:
                    lv_list_get_all_templateid.append('')

            lv_list_get_all_template_trigger = []
            lv_result = None
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            for lv_result in executor.map(cus_zabbix_api.def_get_template_trigger, lv_list_get_all_templateid, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_template_trigger.append([lv_result['result'][0]['triggerid']])
                else:
                    lv_list_get_all_template_trigger.append([])

            lv_sum_v01 = 0
            lv_result = None
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            for lv_result in executor.map(cus_zabbix_api.def_delete_template_trigger, lv_list_get_all_template_trigger):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板删除触发器: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板删除触发器: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1
        # ![09_模板更新触发器标签]
        elif args.update_template_trigger_tags != 'update_template_trigger_tags':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=9)

            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = []
            column_3_list = []
            column_4_list = []
            column_5_list = []
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.def_get_cell_value(i + 2, 2))
                column_3_list.append(cus_excel_op.def_get_cell_value(i + 2, 3))
                column_4_list.append(cus_excel_op.def_get_cell_value(i + 2, 4))
                column_5_list.append(cus_excel_op.def_get_cell_value(i + 2, 1) + '_' +
                                     cus_excel_op.def_get_cell_value(i + 2, 2))
            i = None
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_templateid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append(lv_result['result'][0]['templateid'])
                else:
                    lv_list_get_all_templateid.append('')

            lv_list_get_all_template_itemid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template_trigger, lv_list_get_all_templateid, column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_template_itemid.append(lv_result['result'][0]['triggerid'])
                else:
                    lv_list_get_all_template_itemid.append('')

            # 去重
            unit_column_1_list = list(set(column_5_list))
            # 使用index保持不乱序
            unit_column_1_list.sort(key=column_5_list.index)

            lv_list_get_all_tag = []
            lv_list_tmp_get_all_tag = []
            for o in range(len(column_5_list)):
                for i in range(len(unit_column_1_list)):
                    if column_5_list[o] == unit_column_1_list[i]:
                        lv_list_tmp_get_all_tag.append({unit_column_1_list[i]: {
                            "tag": cus_excel_op.def_get_cell_value(o + 2, 3), "value": cus_excel_op.def_get_cell_value(o + 2, 4)
                        }})

            dict4 = {}
            for i in range(len(lv_list_tmp_get_all_tag)):
                for key in lv_list_tmp_get_all_tag[i].keys():
                    if key in unit_column_1_list:
                        dict4.setdefault(key, []).append(lv_list_tmp_get_all_tag[i][key])
                    # else:
                    #     dict4[key] = lv_list_tmp_get_all_tag[i][key]
            lv_list_get_all_pre_delete_tag = list(dict4.values())

            unit_column_2_list = list(set(lv_list_get_all_template_itemid))
            # 使用index保持不乱序
            unit_column_2_list.sort(key=lv_list_get_all_template_itemid.index)

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_update_template_trigger_tags, unit_column_2_list, lv_list_get_all_pre_delete_tag):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板更新触发器标签: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(unit_column_2_list), lv_sum_v01 + 1, unit_column_2_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板更新触发器标签: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(unit_column_2_list), lv_sum_v01 + 1, unit_column_2_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1
        elif args.delete_template_trigger_tags != 'delete_template_trigger_tags':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=9)

            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = []
            column_3_list = []
            column_4_list = []
            column_5_list = []
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.def_get_cell_value(i + 2, 2))
                column_3_list.append(cus_excel_op.def_get_cell_value(i + 2, 3))
                column_4_list.append(cus_excel_op.def_get_cell_value(i + 2, 4))
                column_5_list.append(cus_excel_op.def_get_cell_value(i + 2, 1) + '_' +
                                     cus_excel_op.def_get_cell_value(i + 2, 2))
            i = None

            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_templateid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append(lv_result['result'][0]['templateid'])
                else:
                    lv_list_get_all_templateid.append('')

            lv_list_get_all_template_itemid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template_trigger, lv_list_get_all_templateid, column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_template_itemid.append(lv_result['result'][0]['triggerid'])
                else:
                    lv_list_get_all_template_itemid.append('')

            # 去重
            unit_column_1_list = list(set(column_5_list))
            # 使用index保持不乱序
            unit_column_1_list.sort(key=column_5_list.index)

            lv_list_get_all_tag = []
            lv_list_tmp_get_all_tag = []
            for o in range(len(column_5_list)):
                for i in range(len(unit_column_1_list)):
                    if column_5_list[o] == unit_column_1_list[i]:
                        lv_list_tmp_get_all_tag.append({unit_column_1_list[i]: {
                            "tag": cus_excel_op.def_get_cell_value(o + 2, 3), "value": cus_excel_op.def_get_cell_value(o + 2, 4)
                        }})

            dict4 = {}
            for i in range(len(lv_list_tmp_get_all_tag)):
                for key in lv_list_tmp_get_all_tag[i].keys():
                    if key in unit_column_1_list:
                        dict4.setdefault(key, []).append(lv_list_tmp_get_all_tag[i][key])
                    # else:
                    #     dict4[key] = lv_list_tmp_get_all_tag[i][key]
            lv_list_get_all_pre_delete_tag = list(dict4.values())

            unit_column_2_list = list(set(lv_list_get_all_template_itemid))
            # 使用index保持不乱序
            unit_column_2_list.sort(key=lv_list_get_all_template_itemid.index)

            lv_list_get_all_template_item_tags = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template_trigger_tags, unit_column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_template_item_tags.append(lv_result['result'][0]['tags'])
                else:
                    lv_list_get_all_template_item_tags.append('')

            for i in range(len(lv_list_get_all_template_item_tags)):
                for o in lv_list_get_all_pre_delete_tag[i]:
                    try:
                        lv_list_get_all_template_item_tags[i].remove(o)
                    except:
                        continue

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_update_template_trigger_tags, unit_column_2_list, lv_list_get_all_template_item_tags):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 模板移除触发器标签: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(unit_column_2_list), lv_sum_v01 + 1, unit_column_2_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 模板移除触发器标签: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(unit_column_2_list), lv_sum_v01 + 1, unit_column_2_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1
        # ![10_创建主机]
        elif args.create_host != 'create_host':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=10)
            column_1_list = cus_excel_op.def_get_col_value(1)
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
            column_14_list = []
            column_15_list = []
            column_16_list = []
            column_17_list = []
            column_18_list = []
            column_19_list = []
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.def_get_cell_value(i + 2, 2))
                column_3_list.append(cus_excel_op.def_get_cell_value(i + 2, 3))
                column_4_list.append(cus_excel_op.def_get_cell_value(i + 2, 4))
                column_5_list.append(cus_excel_op.def_get_cell_value(i + 2, 5))
                column_6_list.append(cus_excel_op.def_get_cell_value(i + 2, 6))
                column_6_list.append(cus_excel_op.def_get_cell_value(i + 2, 6))
                column_7_list.append(cus_excel_op.def_get_cell_value(i + 2, 7))
                column_8_list.append(cus_excel_op.def_get_cell_value(i + 2, 8))
                column_9_list.append(cus_excel_op.def_get_cell_value(i + 2, 9))
                column_10_list.append(cus_excel_op.def_get_cell_value(i + 2, 10))
                column_11_list.append(cus_excel_op.def_get_cell_value(i + 2, 11))
                column_12_list.append(cus_excel_op.def_get_cell_value(i + 2, 12))
                column_13_list.append(cus_excel_op.def_get_cell_value(i + 2, 13))
                column_14_list.append(cus_excel_op.def_get_cell_value(i + 2, 14))
                column_15_list.append(cus_excel_op.def_get_cell_value(i + 2, 15))
                column_16_list.append(cus_excel_op.def_get_cell_value(i + 2, 16))
                column_17_list.append(cus_excel_op.def_get_cell_value(i + 2, 17))
                column_18_list.append(cus_excel_op.def_get_cell_value(i + 2, 18))
                column_19_list.append(cus_excel_op.def_get_cell_value(i + 2, 19))

            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_templateid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append([{"templateid": int(lv_result['result'][0]['templateid'])}])
                else:
                    lv_list_get_all_templateid.append([])

            lv_dic_zbx_version = {'6.0': cus_zabbix_api.def_get_hostgroup_6_0,
                                  '6.4': cus_zabbix_api.def_get_hostgroup_6_4}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
                lv_list_get_all_groupid = []
                lv_result = None
                for lv_result in executor.map(lv_dic_zbx_version[cus_zabbix_api.def_check_zbx_version()['result'][0:3]], column_3_list):
                    if lv_result['tag'] is True:
                        lv_list_get_all_groupid.append([{"groupid": int(lv_result['result'][0]['groupid'])}])
                    else:
                        lv_list_get_all_groupid.append([])

                lv_sum_v01 = 0
                lv_result = None
                for lv_result in executor.map(cus_zabbix_api.def_create_host, column_1_list, lv_list_get_all_templateid, lv_list_get_all_groupid, column_4_list,
                                              column_5_list, column_6_list, column_7_list, column_8_list, column_9_list, column_10_list, column_11_list,
                                              column_12_list, column_13_list, column_14_list, column_15_list, column_16_list, column_17_list, column_18_list,
                                              column_19_list):
                    if lv_result['tag'] is True:
                        print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 创建主机: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                              % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                    else:
                        print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 创建主机: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                              % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                    lv_sum_v01 = lv_sum_v01 + 1
        elif args.delete_host != 'delete_host':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=10)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_hostid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_host, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_hostid.append([lv_result['result'][0]['hostid']])
                else:
                    lv_list_get_all_hostid.append([])

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_delete_host, lv_list_get_all_hostid):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 删除主机: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 删除主机: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1
        # ![11_主机创建接口]
        elif args.massadd_host_interface != 'massadd_host_interface':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=11)
            column_1_list = cus_excel_op.def_get_col_value(1)
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
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.def_get_cell_value(i + 2, 2))
                column_3_list.append(cus_excel_op.def_get_cell_value(i + 2, 3))
                column_4_list.append(cus_excel_op.def_get_cell_value(i + 2, 4))
                column_5_list.append(cus_excel_op.def_get_cell_value(i + 2, 5))
                column_6_list.append(cus_excel_op.def_get_cell_value(i + 2, 6))
                column_6_list.append(cus_excel_op.def_get_cell_value(i + 2, 6))
                column_7_list.append(cus_excel_op.def_get_cell_value(i + 2, 7))
                column_8_list.append(cus_excel_op.def_get_cell_value(i + 2, 8))
                column_9_list.append(cus_excel_op.def_get_cell_value(i + 2, 9))
                column_10_list.append(cus_excel_op.def_get_cell_value(i + 2, 10))
                column_11_list.append(cus_excel_op.def_get_cell_value(i + 2, 10))
                column_12_list.append(cus_excel_op.def_get_cell_value(i + 2, 10))

            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_hostid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_host, column_3_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_hostid.append([{"hostid": int(lv_result['result'][0]['hostid'])}])
                else:
                    lv_list_get_all_hostid.append([])

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_massadd_host_interface, lv_list_get_all_hostid, column_2_list,
                                          column_3_list, column_4_list, column_5_list, column_6_list, column_7_list, column_8_list,
                                          column_9_list, column_10_list, column_11_list, column_12_list):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 主机创建接口: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 主机创建接口: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1
        elif args.massremove_host_interface != 'massremove_host_interface':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=11)

            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = []
            column_3_list = []
            column_4_list = []
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.def_get_cell_value(i + 2, 2))
                column_3_list.append(cus_excel_op.def_get_cell_value(i + 2, 3))
                column_4_list.append(cus_excel_op.def_get_cell_value(i + 2, 4))

            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_hostid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_host, column_3_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_hostid.append([lv_result['result'][0]['hostid']])
                else:
                    lv_list_get_all_hostid.append([])

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_massremove_host_interface, lv_list_get_all_hostid, column_2_list,
                                          column_3_list, column_4_list):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 删除主机接口: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 删除主机接口: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1
        # ![12_主机关联模板]
        elif args.massadd_host_template != 'massadd_host_template':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=12)

            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = []
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.def_get_cell_value(i + 2, 2))

            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_hostid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_host, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_hostid.append([{"hostid": int(lv_result['result'][0]['hostid'])}])
                else:
                    lv_list_get_all_hostid.append([])

            lv_list_get_all_templateid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append([{"templateid": int(lv_result['result'][0]['templateid'])}])
                else:
                    lv_list_get_all_templateid.append([])

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_massadd_host_template, lv_list_get_all_hostid, lv_list_get_all_templateid):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 主机关联模板: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 主机关联模板: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1
        elif args.massremove_host_templateids != 'massremove_host_templateids':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=12)

            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = []
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.def_get_cell_value(i + 2, 2))

            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_hostid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_host, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_hostid.append([lv_result['result'][0]['hostid']])
                else:
                    lv_list_get_all_hostid.append([])

            lv_list_get_all_templateid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append([lv_result['result'][0]['templateid']])
                else:
                    lv_list_get_all_templateid.append([])

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_massremove_host_templateids, lv_list_get_all_hostid, lv_list_get_all_templateid):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 主机脱离模板保留监控项: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 主机脱离模板保留监控项: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1
        elif args.massremove_host_templateids_clear != 'massremove_host_templateids_clear':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=12)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = []
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.def_get_cell_value(i + 2, 2))

            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_hostid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_host, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_hostid.append([lv_result['result'][0]['hostid']])
                else:
                    lv_list_get_all_hostid.append([])

            lv_list_get_all_templateid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_template, column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_templateid.append([lv_result['result'][0]['templateid']])
                else:
                    lv_list_get_all_templateid.append([])

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_massremove_host_templateids_clear, lv_list_get_all_hostid, lv_list_get_all_templateid):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 主机脱离模板删除监控项: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 主机脱离模板删除监控项: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1
        # ![13_主机关联主机组]
        elif args.massadd_host_groups != 'massadd_host_groups':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=13)

            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = []
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.def_get_cell_value(i + 2, 2))

            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_hostid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_host, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_hostid.append([{"hostid": int(lv_result['result'][0]['hostid'])}])
                else:
                    lv_list_get_all_hostid.append([])

            lv_list_get_all_groupid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_hostgroup_6_0, column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_groupid.append([{"groupid": int(lv_result['result'][0]['groupid'])}])
                else:
                    lv_list_get_all_groupid.append([])

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_massadd_host_groups, lv_list_get_all_hostid, lv_list_get_all_groupid):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 主机关联主机组: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 主机关联主机组: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1
        elif args.massremove_host_group != 'massremove_host_group':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=13)

            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            column_2_list = []
            for i in range(len(column_1_list)):
                column_2_list.append(cus_excel_op.def_get_cell_value(i + 2, 2))

            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            lv_list_get_all_hostid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_host, column_1_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_hostid.append([lv_result['result'][0]['hostid']])
                else:
                    lv_list_get_all_hostid.append([])

            lv_list_get_all_groupid = []
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_get_hostgroup_6_0, column_2_list):
                if lv_result['tag'] is True:
                    lv_list_get_all_groupid.append([lv_result['result'][0]['groupid']])
                else:
                    lv_list_get_all_groupid.append([])

            lv_sum_v01 = 0
            lv_result = None
            for lv_result in executor.map(cus_zabbix_api.def_massremove_host_group, lv_list_get_all_hostid, lv_list_get_all_groupid):
                if lv_result['tag'] is True:
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 主机脱离主机组: \033[;32m%s\033[0m 成功 返回值为: \033[;32m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                else:
                    print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 主机脱离主机组: \033[;31m%s\033[0m 失败 返回值为: \033[;31m%s\033[0m'
                          % (len(column_1_list), lv_sum_v01 + 1, column_1_list[lv_sum_v01], lv_result['result']))
                lv_sum_v01 = lv_sum_v01 + 1
        # ![31_发现规则]
        elif args.create_discoveryrule != 'create_discoveryrule':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=31)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            [
                (
                    cus_zabbix_api.def_create_discoveryrule(
                        "".join([o['templateid'] for o in cus_zabbix_api.def_get_template(cus_excel_op.def_get_cell_value(i + 2, 1))]),
                        cus_excel_op.def_get_cell_value(i + 2, 2),
                        cus_excel_op.def_get_cell_value(i + 2, 3),
                        cus_excel_op.def_get_cell_value(i + 2, 4),
                    ),
                )
                for i in range(len(column_1_list))
            ]
        elif args.delete_discoveryrule != 'delete_discoveryrule':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=31)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            [
                (
                    cus_zabbix_api.def_delete_discoveryrule(
                        [
                            o['itemid'] for o in cus_zabbix_api.def_get_discoveryrule(
                            "".join([o['templateid'] for o in cus_zabbix_api.def_get_template(cus_excel_op.def_get_cell_value(i + 2, 1))]),
                            cus_excel_op.def_get_cell_value(i + 2, 2))
                        ]
                    )
                )
                for i in range(len(column_1_list))
            ]
        # ![32_模板创建监控项原型]
        elif args.create_itemprototype != 'create_itemprototype':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=32)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            # 去重
            unit_column_1_list = list(set(column_1_list))
            # 使用index保持不乱序
            unit_column_1_list.sort(key=column_1_list.index)
            [
                [
                    (
                        cus_zabbix_api.def_create_itemprototype(
                            ",".join([i_01['itemid'] for i_01 in cus_zabbix_api.def_get_discoveryrule(
                                "".join([i_02['templateid'] for i_02 in cus_zabbix_api.def_get_template(cus_excel_op.def_get_cell_value(o + 2, 1))]),
                                cus_excel_op.def_get_cell_value(o + 2, 2))]),
                            ','.join([u['templateid'] for u in cus_zabbix_api.def_get_template(unit_column_1_list[i])]),
                            cus_excel_op.def_get_cell_value(o + 2, 3), cus_excel_op.def_get_cell_value(o + 2, 4),
                            cus_excel_op.def_get_cell_value(o + 2, 5), cus_excel_op.def_get_cell_value(o + 2, 6),
                            cus_excel_op.def_get_cell_value(o + 2, 7), cus_excel_op.def_get_cell_value(o + 2, 8),
                            cus_excel_op.def_get_cell_value(o + 2, 9))
                        ,)
                    for o in range(len(column_1_list)) if column_1_list[o] == unit_column_1_list[i]
                ]
                for i in range(len(unit_column_1_list))
            ]
        elif args.delete_itemprototype != 'delete_itemprototype':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=32)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            # 去重
            unit_column_1_list = list(set(column_1_list))
            # 使用index保持不乱序
            unit_column_1_list.sort(key=column_1_list.index)
            [
                [
                    [
                        cus_zabbix_api.def_delete_itemprototype(([x['itemid']]), ) for x in cus_zabbix_api.def_get_itemprototype_item(
                        ",".join([i_01['itemid'] for i_01 in cus_zabbix_api.def_get_discoveryrule(
                            "".join([i_02['templateid'] for i_02 in cus_zabbix_api.def_get_template(cus_excel_op.def_get_cell_value(o + 2, 1))]),
                            cus_excel_op.def_get_cell_value(o + 2, 2))]),
                        cus_excel_op.def_get_cell_value(o + 2, 5))
                    ]
                    for o in range(len(column_1_list)) if column_1_list[o] == unit_column_1_list[i]
                ]
                for i in range(len(unit_column_1_list))
            ]

        # ![33_模板创建触发器]
        elif args.create_template_triggerprototype != 'create_template_triggerprototype':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=33)
            column_1_list = cus_excel_op.def_get_col_value(1)
            del column_1_list[0]
            [(cus_zabbix_api.def_create_template_triggerprototype(cus_excel_op.def_get_cell_value(i + 2, 1), cus_excel_op.def_get_cell_value(i + 2, 2),
                                                                  cus_excel_op.def_get_cell_value(i + 2, 3), cus_excel_op.def_get_cell_value(i + 2, 4)),)
             for i in range(len(column_1_list))]
        elif args.delete_template_triggerprototype != 'delete_template_triggerprototype':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=33)
            column_1_list = cus_excel_op.def_get_col_value(3)
            del column_1_list[0]
            [(cus_zabbix_api.def_delete_template_triggerprototype([cus_zabbix_api.def_get_template_triggerprototype(cus_excel_op.def_get_cell_value(i + 2, 1))]),)
             for i in range(len(column_1_list))]

        # ![导出所有模板]
        elif args.export_configuration != 'export_configuration':
            title_name = ['序号', '模板名称', '模板ID', '数据源']
            result = cus_zabbix_api.def_get_all_templateid()['result']
            with open('trans/{v01}_所有模板.txt'.format(v01=cus_zabbix_api.def_check_zbx_version()['result']), 'a+') as s_template:
                s_template.truncate(0)
            s_template.close()
            lv_all_templateIndex = []
            lv_all_templateID = []
            lv_all_templateName = []
            lv_all_templateSource = []
            executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
            for i in range(len(result)):
                lv_all_templateIndex.append(str(i + 1))
                lv_all_templateID.append(result[i]['templateid'])
                lv_all_templateName.append(result[i]['host'])
            lv_sum_v01 = 0
            for lv_result in executor.map(cus_zabbix_api.def_export_configuration, lv_all_templateID):
                with open('trans/{v01}_所有模板.txt'.format(v01=cus_zabbix_api.def_check_zbx_version()['result']), 'a') as s_template:
                    s_template.write(str(lv_sum_v01 + 1) + ',')
                    s_template.write(lv_all_templateID[lv_sum_v01] + ',')
                    s_template.write(lv_all_templateName[lv_sum_v01] + ',')
                    s_template.write(lv_result['result'] + ' \n')
                    print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 导出模板成功: \033[;32m%s\033[0m 模板ID为: \033[;32m%s\033[0m'
                          % (len(lv_all_templateID), lv_sum_v01 + 1, lv_all_templateName[lv_sum_v01], lv_all_templateID[lv_sum_v01]))
                s_template.close()
                lv_sum_v01 = lv_sum_v01 + 1
        # ![导入所有模板]
        elif args.import_configuration != 'import_configuration':
            with open('trans/{v01}_所有模板.txt'.format(v01=cus_zabbix_api.def_check_zbx_version()['result'][0:3]), 'r+', encoding='utf-8') as f:
                one_object_list = {}
                lv_all_templateIndex = []
                lv_all_templateID = []
                lv_all_templateName = []
                lv_all_templateSource = []
                errorlist = []
                all_data = f.readlines()
                f.close()
                for i in range(len(all_data)):
                    temp_list = all_data[i].split(",", 3)
                    lv_all_templateIndex.append(temp_list[0])
                    lv_all_templateID.append(temp_list[1])
                    lv_all_templateName.append(temp_list[2])
                    lv_all_templateSource.append(temp_list[3])
                executor = ThreadPoolExecutor(zabbix_api.GV_CPU_COUNT)
                lv_sum_v01 = 0
                lv_dic_zbx_version = {'5.0': cus_zabbix_api.def_import_configuration_5_0,
                                      '6.0': cus_zabbix_api.def_import_configuration_6_0,
                                      '6.4': cus_zabbix_api.def_import_configuration_6_4}
                if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                    sucessnum = 0
                    for lv_result in executor.map(lv_dic_zbx_version[cus_zabbix_api.def_check_zbx_version()['result'][0:3]], lv_all_templateSource):
                        if lv_result['result'] is True:
                            print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 导入模板成功: \033[;32m%s\033[0m 模板ID为: \033[;32m%s\033[0m'
                                  % (len(lv_all_templateID), sucessnum + 1, lv_all_templateName[lv_sum_v01], lv_all_templateID[lv_sum_v01]))
                            lv_sum_v01 = lv_sum_v01 + 1
                            sucessnum = sucessnum + 1
                        else:
                            errorlist.append(lv_sum_v01 + 1)
                            print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 导入模板失败: \033[;31m%s\033[0m 模板ID为: \033[;31m%s\033[0m 稍后将再次尝试导入'
                                  % (len(lv_all_templateID), sucessnum + 1, lv_all_templateName[lv_sum_v01], lv_all_templateID[lv_sum_v01]))
                            lv_sum_v01 = lv_sum_v01 + 1
                else:
                    print(u"当前zabbix server版本\"{v01}\"未适配不能提供汉化".format(v01=cus_zabbix_api.def_check_zbx_version()['result']))
                    exit(1)
                lv_sum_v01 = 0
                while len(errorlist) > 0:
                    one_object_list = {}
                    lv_all_templateIndex1 = []
                    lv_all_templateID1 = []
                    lv_all_templateName1 = []
                    lv_all_templateSource1 = []
                    for lv_tmp_i in range(len(errorlist)):
                        all_data02 = all_data[errorlist[lv_tmp_i] - 1]
                        temp_list = all_data02.split(",", 3)
                        lv_all_templateIndex1.append(temp_list[0])
                        lv_all_templateID1.append(temp_list[1])
                        lv_all_templateName1.append(temp_list[2])
                        lv_all_templateSource1.append(temp_list[3])
                    if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                        for lv_result in executor.map(lv_dic_zbx_version[cus_zabbix_api.def_check_zbx_version()['result'][0:3]], lv_all_templateSource1):
                            if lv_result['result'] is True:
                                print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 重新导入模板成功: \033[;32m%s\033[0m 模板ID为: \033[;32m%s\033[0m'
                                      % (len(lv_all_templateID), sucessnum + 1, lv_all_templateName1[lv_sum_v01], lv_all_templateID1[lv_sum_v01]))
                                lv_sum_v01 = lv_sum_v01 + 1
                                sucessnum = sucessnum + 1
                                del errorlist[0]
                            else:
                                print(u'(\033[;31m%s\033[0m/\033[;31m%s\033[0m): -> 重新导入模板失败: \033[;31m%s\033[0m 模板ID为: \033[;31m%s\033[0m 稍后将再次尝试导入'
                                      % (len(lv_all_templateID), sucessnum + 1, lv_all_templateName1[lv_sum_v01], lv_all_templateID1[lv_sum_v01]))
                                del errorlist[0]
                                errorlist.append(int(lv_all_templateIndex1[lv_sum_v01]))
                                lv_sum_v01 = lv_sum_v01 + 1
                    else:
                        print(u"当前zabbix server版本\"{v01}\"未适配不能提供汉化".format(v01=cus_zabbix_api.def_check_zbx_version()['result']))
                        exit(1)


