#!/usr/bin/python3
# coding:utf-8

import argparse
import base64
import datetime
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, wait
from zabbix_api import GV_CPU_COUNT
import hashlib
import hmac
import inspect
import json
import openpyxl
import re
import sys
import time
from time import mktime
import requests
from requests.adapters import HTTPAdapter
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from zabbix_api import CusZabbixApi
from zabbix_api import CusExcelOp
from zabbix_api import GV_ERROR_MESS
from zabbix_api import CusLocalMethod


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='zabbix  api ', usage='%(prog)s [options]')
    # ![]
    ######################################################################################################
    parser.add_argument('-export_all_template_item_sheet19', nargs='?', metavar='无参数', dest='export_all_template_item_sheet19', default='export_all_template_item_sheet19',
                        help=u"仅作者用于导出英文所有模板监控项")
    parser.add_argument('-trans_all_template_item_to_chinese_sheet20', nargs='?', metavar='无参数', dest='trans_all_template_item_to_chinese_sheet20', default='trans_all_template_item_to_chinese_sheet20',
                        help=u"请使用此选项翻译模板监控项")
    ######################################################################################################
    parser.add_argument('-export_all_template_trigger_sheet21', nargs='?', metavar='无参数', dest='export_all_template_trigger_sheet21', default='export_all_template_trigger_sheet21',
                        help=u"仅作者用于导出英文所有模板触发器")
    parser.add_argument('-trans_all_template_trigger_to_chinese_sheet22', nargs='?', metavar='无参数', dest='trans_all_template_trigger_to_chinese_sheet22', default='trans_all_template_trigger_to_chinese_sheet22',
                        help=u"请使用此选项翻译模板触发器")
    ######################################################################################################
    parser.add_argument('-export_all_template_graph_sheet23', nargs='?', metavar='无参数', dest='export_all_template_graph_sheet23', default='export_all_template_graph_sheet23',
                        help=u"仅作者用于导出英文所有模板图表")
    parser.add_argument('-trans_all_template_graph_to_chinese_sheet24', nargs='?', metavar='无参数', dest='trans_all_template_graph_to_chinese_sheet24', default='trans_all_template_graph_to_chinese_sheet24',
                        help=u"请使用此选项翻译模板图表")
    #########################################################################################################
    parser.add_argument('-export_all_template_itemprototype_sheet25', nargs='?', metavar='无参数', dest='export_all_template_itemprototype_sheet25', default='export_all_template_itemprototype_sheet25',
                        help=u"仅作者用于导出英文所有模板监控项原型")
    parser.add_argument('-trans_all_template_itemprototype_to_chinese_sheet26', nargs='?', metavar='无参数', dest='trans_all_template_itemprototype_to_chinese_sheet26', default='trans_all_template_itemprototype_to_chinese_sheet26',
                        help=u"请使用此选项翻译模板监控项原型")
    #########################################################################################################
    parser.add_argument('-export_all_template_triggerprototype_sheet27', nargs='?', metavar='无参数', dest='export_all_template_triggerprototype_sheet27', default='export_all_template_triggerprototype_sheet27',
                        help=u"仅作者用于导出英文所有模板触发器类型")
    parser.add_argument('-trans_all_template_triggerprototype_to_chinese_sheet28', nargs='?', metavar='无参数', dest='trans_all_template_triggerprototype_to_chinese_sheet28', default='trans_all_template_triggerprototype_to_chinese_sheet28',
                        help=u"请使用此选项翻译模板触发器类型")
    #########################################################################################################
    parser.add_argument('-export_all_template_graphprototype_sheet29', nargs='?', metavar='无参数', dest='export_all_template_graphprototype_sheet29', default='export_all_template_graphprototype_sheet29',
                        help=u"仅作者用于导出英文所有模板图表原型")
    parser.add_argument('-trans_all_template_graphprototype_to_chinese_sheet30', nargs='?', metavar='无参数', dest='trans_all_template_graphprototype_to_chinese_sheet30', default='trans_all_template_graphprototype_to_chinese_sheet30',
                        help=u"请使用此选项翻译模板图表原型")
    ######################################################################################################
    parser.add_argument('-export_all_template_trigger_event_name_sheet37', nargs='?', metavar='无参数', dest='export_all_template_trigger_event_name_sheet37', default='export_all_template_trigger_event_name_sheet37',
                        help=u"仅作者用于导出英文所有模板触发器事件名称")
    parser.add_argument('-trans_all_template_trigger_event_name_to_chinese_sheet37', nargs='?', metavar='无参数', dest='trans_all_template_trigger_event_name_to_chinese_sheet37', default='trans_all_template_trigger_event_name_to_chinese_sheet37',
                        help=u"请使用此选项翻译模板触发器事件名称")
    ######################################################################################################
    parser.add_argument('-export_all_template_triggerprototype_name_sheet38', nargs='?', metavar='无参数', dest='export_all_template_triggerprototype_name_sheet38', default='export_all_template_triggerprototype_name_sheet38',
                        help=u"仅作者用于导出英文所有模板触发器原型事件名称")
    parser.add_argument('-trans_all_template_triggerprototype_name_to_chinese_sheet38', nargs='?', metavar='无参数', dest='trans_all_template_triggerprototype_name_to_chinese_sheet38', default='trans_all_template_triggerprototype_name_to_chinese_sheet38',
                        help=u"请使用此选项翻译模板触发原型器事件名称")
    ######################################################################################################
    parser.add_argument('-export_all_template_tag_name_sheet40', nargs='?', metavar='无参数', dest='export_all_template_tag_name_sheet40', default='export_all_template_tag_name_sheet40',
                        help=u"仅作者用于导出英文所有模板标签名称")
    parser.add_argument('-trans_all_template_tag_name_to_chinese_sheet40', nargs='?', metavar='无参数', dest='trans_all_template_tag_name_to_chinese_sheet40', default='trans_all_template_tag_name_to_chinese_sheet40',
                        help=u"请使用此选项翻译模板标签名称")
    ######################################################################################################
    parser.add_argument('-export_all_template_item_tag_name_sheet41', nargs='?', metavar='无参数', dest='export_all_template_item_tag_name_sheet41', default='export_all_template_item_tag_name_sheet41',
                        help=u"仅作者用于导出英文所有模板监控项标签名称")
    parser.add_argument('-trans_all_template_item_tag_name_to_chinese_sheet41', nargs='?', metavar='无参数', dest='trans_all_template_item_tag_name_to_chinese_sheet41', default='trans_all_template_item_tag_name_to_chinese_sheet41',
                        help=u"请使用此选项翻译模板监控项标签名称")
    ######################################################################################################
    parser.add_argument('-export_all_template_trigger_tag_name_sheet42', nargs='?', metavar='无参数', dest='export_all_template_trigger_tag_name_sheet42', default='export_all_template_trigger_tag_name_sheet42',
                        help=u"仅作者用于导出英文所有模板触发器标签名称")
    parser.add_argument('-trans_all_template_trigger_tag_name_to_chinese_sheet42', nargs='?', metavar='无参数', dest='trans_all_template_trigger_tag_name_to_chinese_sheet42', default='trans_all_template_trigger_tag_name_to_chinese_sheet42',
                        help=u"请使用此选项翻译模板触发器标签名称")
    ######################################################################################################
    parser.add_argument('-export_all_template_itemprototype_tag_sheet43', nargs='?', metavar='无参数', dest='export_all_template_itemprototype_tag_sheet43', default='export_all_template_itemprototype_tag_sheet43',
                        help=u"仅作者用于导出英文所有模板监控项原型标签")
    parser.add_argument('-trans_all_template_itemprototype_tag_to_chinese_sheet43', nargs='?', metavar='无参数', dest='trans_all_template_itemprototype_tag_to_chinese_sheet43', default='trans_all_template_itemprototype_tag_to_chinese_sheet43',
                        help=u"请使用此选项翻译模板监控项原型标签")
    #########################################################################################################
    parser.add_argument('-export_all_template_triggerprototype_tag_sheet44', nargs='?', metavar='无参数', dest='export_all_template_triggerprototype_tag_sheet44', default='export_all_template_triggerprototype_tag_sheet44',
                        help=u"仅作者用于导出英文所有模板监控项原型标签")
    parser.add_argument('-trans_all_template_triggerprototype_tag_to_chinese_sheet44', nargs='?', metavar='无参数', dest='trans_all_template_triggerprototype_tag_to_chinese_sheet44', default='trans_all_template_triggerprototype_tag_to_chinese_sheet44',
                        help=u"请使用此选项翻译模板监控项原型标签")
    ######################################################################################################
    parser.add_argument('-export_all_hostgroup_name_sheet45', nargs='?', metavar='无参数', dest='export_all_hostgroup_name_sheet45', default='export_all_hostgroup_name_sheet45',
                        help=u"仅作者用于导出英文主机组名称")
    parser.add_argument('-trans_all_hostgroup_name_to_chinese_sheet45', nargs='?', metavar='无参数', dest='trans_all_hostgroup_name_to_chinese_sheet45', default='trans_all_hostgroup_name_to_chinese_sheet45',
                        help=u"请使用此选项翻译主机组名称")
    ######################################################################################################
    parser.add_argument('-export_all_templategroup_name_sheet46', nargs='?', metavar='无参数', dest='export_all_templategroup_name_sheet46', default='export_all_templategroup_name_sheet46',
                        help=u"仅作者用于导出英文模板组名称")
    parser.add_argument('-trans_all_templategroup_name_to_chinese_sheet46', nargs='?', metavar='无参数', dest='trans_all_templategroup_name_to_chinese_sheet46', default='trans_all_templategroup_name_to_chinese_sheet46',
                        help=u"请使用此选项翻译模板组名称")
    ######################################################################################################
    parser.add_argument('-export_all_application_name_sheet47', nargs='?', metavar='无参数', dest='export_all_application_name_sheet47', default='export_all_application_name_sheet47',
                        help=u"仅作者用于导出英文模板应用集名称")
    parser.add_argument('-trans_all_application_name_to_chinese_sheet47', nargs='?', metavar='无参数', dest='trans_all_application_name_to_chinese_sheet47', default='trans_all_application_name_to_chinese_sheet47',
                        help=u"请使用此选项翻译模板应用集名称")
    # 在 #![] 标记区域添加以下两个参数
    ######################################################################################################
    parser.add_argument('-export_all_template_description_sheet56', nargs='?', metavar='无参数', dest='export_all_template_description_sheet56', default='export_all_template_description_sheet56',
                        help=u"仅作者用于导出英文所有模板描述信息")
    parser.add_argument('-trans_all_template_description_to_chinese_sheet56', nargs='?', metavar='无参数', dest='trans_all_template_description_to_chinese_sheet56', default='trans_all_template_description_to_chinese_sheet56',
                        help=u"请使用此选项翻译模板描述信息")
    ######################################################################################################

    ######################################################################################################
    parser.add_argument('-find_chinese_in_brackets', nargs='?', metavar='无参数', dest='find_chinese_in_brackets', default='find_chinese_in_brackets',
                        help=u"校验宏是否是中文字符串")
    ######################################################################################################
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 如有问题请联系作者QQ1284524409',
                        help=u"如有问题请联系作者QQ1284524409")
    ######################################################################################################
    if len(sys.argv) == 1:
        print(parser.print_help())
    else:
        args = parser.parse_args()
        cus_zabbix_api = CusZabbixApi()
        cus_excel_op = CusExcelOp()
        cus_local_method = CusLocalMethod()
        # ![19_仅作者用于导出英文所有模板监控项]
        if args.export_all_template_item_sheet19 != 'export_all_template_item_sheet19':
            cus_excel_op.load_excel('zabbix_api.xlsx', 19)
            active_sheet_name = cus_excel_op.get_active_sheet_name()
            title_name = ['序号', '模板序号', '监控项序号', '模板名称', '监控项ID', '英文名称', '中文名称', '原因']
            v_1 = 'name'
            v_2 = 'itemid'
            v_3 = cus_zabbix_api.def_get_template_item_name
            v_4 = cus_zabbix_api.def_update_item_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4, active_sheet_name)
        # ![20_请使用此选项翻译模板监控项]
        elif args.trans_all_template_item_to_chinese_sheet20 != 'trans_all_template_item_to_chinese_sheet20':
            cus_excel_op.load_excel('./trans/19_翻译模板监控项_.xlsm', 1)
            v_1 = 'name'
            v_2 = 'itemid'
            v_4 = cus_zabbix_api.def_update_item_name
            cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![21_仅作者用于导出英文所有模板触发器]
        elif args.export_all_template_trigger_sheet21 != 'export_all_template_trigger_sheet21':
            cus_excel_op.load_excel('zabbix_api.xlsx', 21)
            active_sheet_name = cus_excel_op.get_active_sheet_name()
            title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
            v_1 = 'description'
            v_2 = 'triggerid'
            v_3 = cus_zabbix_api.def_get_template_trigger_name
            v_4 = cus_zabbix_api.def_update_trigger_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4, active_sheet_name)
        # ![22_请使用此选项翻译模板触发器]
        ######################################################################################################
        elif args.trans_all_template_trigger_to_chinese_sheet22 != 'trans_all_template_trigger_to_chinese_sheet22':
            cus_excel_op.load_excel('./trans/21_翻译模板触发器_.xlsx', 1)
            v_1 = 'description'
            v_2 = 'triggerid'
            v_4 = cus_zabbix_api.def_update_trigger_name
            cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        # ![23_仅作者用于导出英文所有模板图形]
        if args.export_all_template_graph_sheet23 != 'export_all_template_graph_sheet23':
            cus_excel_op.load_excel('zabbix_api.xlsx', 23)
            active_sheet_name = cus_excel_op.get_active_sheet_name()
            title_name = ['序号', '模板序号', '图表序号', '模板名称', '图表ID', '英文名称', '中文名称', '原因']
            v_1 = 'name'
            v_2 = 'graphid'
            v_3 = cus_zabbix_api.def_get_template_graph_name
            v_4 = cus_zabbix_api.def_update_graph_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4, active_sheet_name)
        # ![24_请使用此选项翻译模板图形]
        elif args.trans_all_template_graph_to_chinese_sheet24 != 'trans_all_template_graph_to_chinese_sheet24':
            cus_excel_op.load_excel('./trans/23_翻译模板图形_.xlsx', 1)
            v_1 = 'name'
            v_2 = 'graphid'
            v_4 = cus_zabbix_api.def_update_graph_name
            cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![25_仅作者用于导出英文所有模板监控项原型]
        elif args.export_all_template_itemprototype_sheet25 != 'export_all_template_itemprototype_sheet25':
            cus_excel_op.load_excel('zabbix_api.xlsx', 25)
            active_sheet_name = cus_excel_op.get_active_sheet_name()
            title_name = ['序号', '模板序号', '监控项序号', '模板名称', '监控项ID', '英文名称', '中文名称', '原因']
            v_1 = 'name'
            v_2 = 'itemid'
            v_3 = cus_zabbix_api.def_get_template_itemprototype_name
            v_4 = cus_zabbix_api.def_update_itemprototype_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4, active_sheet_name)
        # ![26_请使用此选项翻译模板监控项原型]
        elif args.trans_all_template_itemprototype_to_chinese_sheet26 != 'trans_all_template_itemprototype_to_chinese_sheet26':
            cus_excel_op.load_excel('./trans/25_翻译模板监控项原型_.xlsx', 1)
            v_1 = 'name'
            v_2 = 'itemid'
            v_4 = cus_zabbix_api.def_update_itemprototype_name
            cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![27_仅作者用于导出英文所有模板触发器类型]
        elif args.export_all_template_triggerprototype_sheet27 != 'export_all_template_triggerprototype_sheet27':
            cus_excel_op.load_excel('zabbix_api.xlsx', 27)
            active_sheet_name = cus_excel_op.get_active_sheet_name()
            title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
            v_1 = 'description'
            v_2 = 'triggerid'
            v_3 = cus_zabbix_api.def_get_template_triggerprototype_name
            v_4 = cus_zabbix_api.def_update_triggerprototype_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4, active_sheet_name)
        # ![28_请使用此选项翻译模板触发器类型]
        elif args.trans_all_template_triggerprototype_to_chinese_sheet28 != 'trans_all_template_triggerprototype_to_chinese_sheet28':
            cus_excel_op.load_excel('./trans/27_翻译模板触发器类型_.xlsx', 1)
            v_1 = 'description'
            v_2 = 'triggerid'
            v_4 = cus_zabbix_api.def_update_triggerprototype_name
            cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![29_仅作者用于导出英文所有模板图形原型]
        elif args.export_all_template_graphprototype_sheet29 != 'export_all_template_graphprototype_sheet29':
            cus_excel_op.load_excel('zabbix_api.xlsx', 29)
            active_sheet_name = cus_excel_op.get_active_sheet_name()
            title_name = ['序号', '模板序号', '图表序号', '模板名称', '图表ID', '英文名称', '中文名称', '原因']
            v_1 = 'name'
            v_2 = 'graphid'
            v_3 = cus_zabbix_api.def_get_template_graphprototype_name
            v_4 = cus_zabbix_api.def_update_graphprototype_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4, active_sheet_name)
        # ![30_请使用此选项翻译模板图形原型]
        elif args.trans_all_template_graphprototype_to_chinese_sheet30 != 'trans_all_template_graphprototype_to_chinese_sheet30':
            cus_excel_op.load_excel('./trans/29_翻译模板图形原型_.xlsx', 1)
            v_1 = 'name'
            v_2 = 'graphid'
            v_4 = cus_zabbix_api.def_update_graphprototype_name
            cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![37_仅作者用于导出英文所有模板触发器事件名称]
        elif args.export_all_template_trigger_event_name_sheet37 != 'export_all_template_trigger_event_name_sheet37':
            cus_excel_op.load_excel('zabbix_api.xlsx', 37)
            active_sheet_name = cus_excel_op.get_active_sheet_name()
            title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
            v_1 = 'event_name'
            v_2 = 'triggerid'
            v_3 = cus_zabbix_api.def_get_template_event_name
            v_4 = cus_zabbix_api.def_update_trigger_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4, active_sheet_name)
        # ![37_翻译模板触发器事件名称]
        elif args.trans_all_template_trigger_event_name_to_chinese_sheet37 != 'trans_all_template_trigger_event_name_to_chinese_sheet37':
            cus_excel_op.load_excel('./trans/37_翻译模板触发器事件名称_.xlsx', 1)
            v_1 = 'event_name'
            v_2 = 'triggerid'
            v_4 = cus_zabbix_api.def_update_trigger_name
            cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![38_翻译模板原型触发器事件名称]
        elif args.export_all_template_triggerprototype_name_sheet38 != 'export_all_template_triggerprototype_name_sheet38':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4',
                                  '7.0': '7.0'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.load_excel('zabbix_api.xlsx', 38)
                active_sheet_name = cus_excel_op.get_active_sheet_name()
                title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
                v_1 = 'event_name'
                v_2 = 'triggerid'
                v_3 = cus_zabbix_api.def_get_template_triggerprototype_event_name
                v_4 = cus_zabbix_api.def_update_triggerprototype_name
                cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4, active_sheet_name)
        # ![38_请使用此选项翻译模板触原型发器类型]
        elif args.trans_all_template_triggerprototype_name_to_chinese_sheet38 != 'trans_all_template_triggerprototype_name_to_chinese_sheet38':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4',
                                  '7.0': '7.0'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.load_excel('./trans/38_翻译模板原型触发器事件名称_.xlsx', 1)
                v_1 = 'event_name'
                v_2 = 'triggerid'
                v_4 = cus_zabbix_api.def_update_triggerprototype_name
                cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![40_仅作者用于导出英文所有所有模板标签名称]
        elif args.export_all_template_tag_name_sheet40 != 'export_all_template_tag_name_sheet40':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4',
                                  '7.0': '7.0',}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.load_excel('zabbix_api.xlsx', 40)
                active_sheet_name = cus_excel_op.get_active_sheet_name()
                title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
                v_1 = 'tags'
                v_2 = 'templateid'
                v_3 = cus_zabbix_api.def_get_template_tags_bytemplateid
                v_4 = cus_zabbix_api.def_update_tags_bytemplateid
                cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4, active_sheet_name)
        # ![40_请使用此选项翻译模板标签名称]
        elif args.trans_all_template_tag_name_to_chinese_sheet40 != 'trans_all_template_tag_name_to_chinese_sheet40':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4',
                                  '7.0': '7.0',}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.load_excel('./trans/40_翻译所有模板标签名称_.xlsx', 1)
                v_1 = 'tags'
                v_2 = 'templateid'
                v_4 = cus_zabbix_api.def_update_tags_bytemplateid
                cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![41_仅作者用于导出英文所有所有模板监控项标签名称]
        elif args.export_all_template_item_tag_name_sheet41 != 'export_all_template_item_tag_name_sheet41':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4',
                                  '7.0': '7.0',}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.load_excel('zabbix_api.xlsx', 41)
                active_sheet_name = cus_excel_op.get_active_sheet_name()
                title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
                v_1 = 'tags'
                v_2 = 'itemid'
                v_3 = cus_zabbix_api.def_get_template_item_tags_bytemplateid
                v_4 = cus_zabbix_api.def_update_template_item_tags_bytemplateid
                cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4, active_sheet_name)
        # ![41_请使用此选项翻译模板监控项标签名称]
        elif args.trans_all_template_item_tag_name_to_chinese_sheet41 != 'trans_all_template_item_tag_name_to_chinese_sheet41':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4',
                                  '7.0': '7.0',}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.load_excel('./trans/41_翻译所有模板监控项标签名称_.xlsx', 1)
                v_1 = 'tags'
                v_2 = 'itemid'
                v_4 = cus_zabbix_api.def_update_template_item_tags_bytemplateid
                cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![42_仅作者用于导出英文所有所有模板触发器标签名称]
        elif args.export_all_template_trigger_tag_name_sheet42 != 'export_all_template_trigger_tag_name_sheet42':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4',
                                  '7.0': '7.0',}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.load_excel('zabbix_api.xlsx', 42)
                active_sheet_name = cus_excel_op.get_active_sheet_name()
                title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
                v_1 = 'tags'
                v_2 = 'triggerid'
                v_3 = cus_zabbix_api.def_get_template_trigger_tags_bytemplateid
                v_4 = cus_zabbix_api.def_update_template_trigger_tags_bytemplateid
                cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4, active_sheet_name)
        # ![42_请使用此选项翻译模板触发器标签名称]
        elif args.trans_all_template_trigger_tag_name_to_chinese_sheet42 != 'trans_all_template_trigger_tag_name_to_chinese_sheet42':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4',
                                  '7.0': '7.0',}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.load_excel('./trans/42_翻译所有模板触发器标签名称_.xlsx', 1)
                v_1 = 'tags'
                v_2 = 'triggerid'
                v_4 = cus_zabbix_api.def_update_template_trigger_tags_bytemplateid
                cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![43_仅作者用于导出英文所有模板监控项原型标签]
        elif args.export_all_template_itemprototype_tag_sheet43 != 'export_all_template_itemprototype_tag_sheet43':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4',
                                  '7.0': '7.0',}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.load_excel('zabbix_api.xlsx', 43)
                active_sheet_name = cus_excel_op.get_active_sheet_name()
                title_name = ['序号', '模板序号', '监控项序号', '模板名称', '监控项ID', '英文名称', '中文名称', '原因']
                v_1 = 'tags'
                v_2 = 'itemid'
                v_3 = cus_zabbix_api.def_get_template_itemprototype_tags_bytemplateid
                v_4 = cus_zabbix_api.def_update_itemprototype_tags_bytemplateid
                cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4, active_sheet_name)
        # ![43_请使用此选项翻译模板监控项原型标签]
        elif args.trans_all_template_itemprototype_tag_to_chinese_sheet43 != 'trans_all_template_itemprototype_tag_to_chinese_sheet43':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4',
                                  '7.0': '7.0',}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.load_excel('./trans/43_翻译模板监控项原型标签_.xlsx', 1)
                title_name = ['序号', '模板序号', '监控项序号', '模板名称', '监控项ID', '英文名称', '中文名称', '原因']
                v_1 = 'tags'
                v_2 = 'itemid'
                v_4 = cus_zabbix_api.def_update_itemprototype_tags_bytemplateid
                cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![44_仅作者用于导出英文所有模板原型触发器标签]
        elif args.export_all_template_triggerprototype_tag_sheet44 != 'export_all_template_triggerprototype_tag_sheet44':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4',
                                  '7.0': '7.0',}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.load_excel('zabbix_api.xlsx', 44)
                active_sheet_name = cus_excel_op.get_active_sheet_name()
                title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
                v_1 = 'tags'
                v_2 = 'triggerid'
                v_3 = cus_zabbix_api.def_get_template_triggerprototype_tag_bytemplateid
                v_4 = cus_zabbix_api.def_update_triggerprototype_tag_bytemplateid
                cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4, active_sheet_name)
        # ![44_请使用此选项翻译模板原型触发器标签]
        elif args.trans_all_template_triggerprototype_tag_to_chinese_sheet44 != 'trans_all_template_triggerprototype_tag_to_chinese_sheet44':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4',
                                  '7.0': '7.0',}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.load_excel('./trans/44_翻译模板原型触发器标签_.xlsx', 1)
                v_1 = 'tags'
                v_2 = 'triggerid'
                v_4 = cus_zabbix_api.def_update_triggerprototype_tag_bytemplateid
                cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![45_仅作者用于导出英文所有主机组名称]
        elif args.export_all_hostgroup_name_sheet45 != 'export_all_hostgroup_name_sheet45':
            cus_excel_op.load_excel('zabbix_api.xlsx', 45)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
            v_3 = cus_zabbix_api.def_get_all_hostgroup()
            row_index = {"index": 2}
            cus_excel_op.create_new_workbook()
            cus_excel_op.create_sheet(cus_zabbix_api.def_check_zbx_version()['result']),
            lv_result = None
            if v_3['tag'] is True:
                for f_1 in range(len(v_3['result'])):
                    [cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))],
                    cus_excel_op.set_cell_value(row_index['index'], 1, row_index['index'] - 1),
                    cus_excel_op.set_cell_value(row_index['index'], 2, u'({0}/{1})'.format(len(v_3['result']), f_1 + 1)),
                    cus_excel_op.set_cell_value(row_index['index'], 3, ""),
                    cus_excel_op.set_cell_value(row_index['index'], 4, ""),
                    cus_excel_op.set_cell_value(row_index['index'], 5, v_3['result'][f_1]['groupid']),
                    cus_excel_op.set_cell_value(row_index['index'], 6, v_3['result'][f_1]['name']),
                    cus_excel_op.set_cell_value(row_index['index'], 7, v_3['result'][f_1]['name']),
                    GV_ERROR_MESS.update(error=''),
                    print(u'(\033[;34m{0}\033[0m/\033[;34m{1}\033[0m)|\033[;34m{2}\033[0m > \033[;34m{3}'.format(len(v_3['result']), f_1 + 1, v_3['result'][f_1]['groupid'], v_3['result'][f_1]['name'])),
                    row_index.update(index=row_index['index'] + 1),
            cus_excel_op.save_workbook(first_active_sheet_name + '.xlsx')

        # ![45_请使用此选项翻译主机组名称]
        elif args.trans_all_hostgroup_name_to_chinese_sheet45 != 'trans_all_hostgroup_name_to_chinese_sheet45':
            cus_excel_op.load_excel('./trans/45_翻译主机组名称_.xlsx', 1)
            v_1 = 'name'
            v_2 = 'groupid'
            v_4 = cus_zabbix_api.def_update_all_hostgroup_name
            cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![46_仅作者用于导出英文所有模板组名称]
        elif args.export_all_templategroup_name_sheet46 != 'export_all_templategroup_name_sheet46':
            lv_dic_zbx_version = {'6.4': '6.4',
                                  '7.0': '7.0',}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.load_excel('zabbix_api.xlsx', 46)
                first_active_sheet_name = cus_excel_op.get_active_sheet_name()
                title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
                v_3 = cus_zabbix_api.def_get_all_templategroup()
                row_index = {"index": 2}
                cus_excel_op.create_new_workbook()
                cus_excel_op.create_sheet(cus_zabbix_api.def_check_zbx_version()['result']),
                lv_result = None
                if v_3['tag'] is True:
                    for f_1 in range(len(v_3['result'])):
                        [cus_excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))],
                        cus_excel_op.set_cell_value(row_index['index'], 1, row_index['index'] - 1),
                        cus_excel_op.set_cell_value(row_index['index'], 2, u'({0}/{1})'.format(len(v_3['result']), f_1 + 1)),
                        cus_excel_op.set_cell_value(row_index['index'], 3, ""),
                        cus_excel_op.set_cell_value(row_index['index'], 4, ""),
                        cus_excel_op.set_cell_value(row_index['index'], 5, v_3['result'][f_1]['groupid']),
                        cus_excel_op.set_cell_value(row_index['index'], 6, v_3['result'][f_1]['name']),
                        cus_excel_op.set_cell_value(row_index['index'], 7, v_3['result'][f_1]['name']),
                        GV_ERROR_MESS.update(error=''),
                        print(u'(\033[;34m{0}\033[0m/\033[;34m{1}\033[0m)|\033[;34m{2}\033[0m > \033[;34m{3}'.format(len(v_3['result']), f_1 + 1, v_3['result'][f_1]['groupid'], v_3['result'][f_1]['name'])),
                        row_index.update(index=row_index['index'] + 1),
                cus_excel_op.save_workbook(first_active_sheet_name + '.xlsx')

        # ![46_请使用此选项翻译模板组名称]
        elif args.trans_all_templategroup_name_to_chinese_sheet46 != 'trans_all_templategroup_name_to_chinese_sheet46':
            lv_dic_zbx_version = {'6.4': '6.4',
                                  '7.0': '7.0'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.load_excel('./trans/46_翻译模板组名称_.xlsx', 1)
                v_1 = 'name'
                v_2 = 'groupid'
                v_4 = cus_zabbix_api.def_update_all_templategroup_name
                cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![47_仅作者用于导出英文所有模板应用集名称]
        elif args.export_all_application_name_sheet47 != 'export_all_application_name_sheet47':
            lv_dic_zbx_version = {'5.0': '5.0'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.load_excel('zabbix_api.xlsx', 47)
                active_sheet_name = cus_excel_op.get_active_sheet_name()
                title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
                v_1 = 'name'
                v_2 = 'applicationid'
                v_3 = cus_zabbix_api.def_get_template_application_bytemplateid
                v_4 = cus_zabbix_api.def_update_template_application_bytemplateid
                cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4, active_sheet_name)

        # ![47_请使用此选项翻译模板组名称]
        elif args.trans_all_application_name_to_chinese_sheet47 != 'trans_all_application_name_to_chinese_sheet47':
            lv_dic_zbx_version = {'5.0': '5.0'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.load_excel('./trans/47_翻译模板应用集名称_.xlsx', 1)
                v_1 = 'name'
                v_2 = 'applicationid'
                v_4 = cus_zabbix_api.def_update_template_application_bytemplateid
                cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![48_仅作者用于导出英文所有模板描述信息]
        elif args.export_all_template_description_sheet56 != 'export_all_template_description_sheet56':
            cus_excel_op.load_excel('zabbix_api.xlsx', 56)
            active_sheet_name = cus_excel_op.get_active_sheet_name()
            title_name = ['序号', '模板序号', '描述序号', '模板名称', '模板ID', '英文描述', '中文描述', '原因']
            v_1 = 'description'
            v_2 = 'templateid'
            v_3 = cus_zabbix_api.def_get_template_description  # 需要在CusZabbixApi类中实现该方法
            v_4 = cus_zabbix_api.def_update_template_description  # 需要在CusZabbixApi类中实现该方法
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4, active_sheet_name)
        # ![48_请使用此选项翻译模板描述信息]
        elif args.trans_all_template_description_to_chinese_sheet56 != 'trans_all_template_description_to_chinese_sheet56':
            cus_excel_op.load_excel('./trans/48_翻译模板描述信息_.xlsx', 1)
            v_1 = 'description'
            v_2 = 'templateid'
            v_4 = cus_zabbix_api.def_update_template_description  # 需要在CusZabbixApi类中实现该方法
            cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################

        elif args.find_chinese_in_brackets != 'find_chinese_in_brackets':
            # 1. 加载Excel数据
            cus_excel_op.load_excel('find_chinese_in_brackets.xlsx', 1)
            first_active_sheet_name = cus_excel_op.get_active_sheet_name()
            column_1_list = cus_excel_op.get_column_values(1)
            del column_1_list[0]

            # 2. 准备结果表格
            title_name = ['行号', '宏值', '结果']
            cus_excel_op.create_new_workbook()
            cus_excel_op.create_sheet(first_active_sheet_name)
            for i, title in enumerate(title_name):
                cus_excel_op.set_cell_value(1, i + 1, title)


            # 3. 定义回调函数
            def process_result_callback(future, index):
                """处理结果的回调函数"""
                try:
                    result = future.result()
                    # 写入Excel
                    row = index + 2  # 第1行是标题，数据从第2行开始
                    cus_excel_op.set_cell_value(row, 1, row - 1)  # 行号
                    cus_excel_op.set_cell_value(row, 2, column_1_list[index])  # 原始宏值
                    cus_excel_op.set_cell_value(row, 3, str(result))  # 处理结果

                    # 更新进度
                    current_progress = index + 1
                    progress_percentage = (current_progress / len(column_1_list)) * 100
                    print(f'处理进度: {current_progress}/{len(column_1_list)} ({progress_percentage:.2f}%) | 行 {row - 1}: {result}')

                except Exception as e:
                    print(f'处理第 {index + 1} 行时发生错误: {str(e)}')
                    cus_excel_op.set_cell_value(index + 2, 3, f'错误: {str(e)}')


            # 4. 使用进度条装饰器
            def progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
                """进度条显示函数"""
                percent = ("{0:.1f}").format(100 * (iteration / float(total)))
                filled_length = int(length * iteration // total)
                bar = fill * filled_length + '-' * (length - filled_length)
                print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
                if iteration == total:
                    print()


            # 5. 并行处理数据
            print(f"\n开始处理 {len(column_1_list)} 条数据...")
            with ThreadPoolExecutor(GV_CPU_COUNT) as executor:
                futures = []
                for idx, macro_value in enumerate(column_1_list):
                    future = executor.submit(cus_local_method.def_find_chinese_in_brackets, macro_value)
                    future.add_done_callback(lambda f, i=idx: process_result_callback(f, i))
                    futures.append(future)
                    # 显示进度条
                    progress_bar(idx + 1, len(column_1_list), prefix='进度:', suffix='完成')

                # 等待所有任务完成
                wait(futures)

            # 6. 保存结果
            result_file = "find_chinese_in_brackets_result.xlsx"
            cus_excel_op.save_workbook(result_file)
            print(f"\n处理完成，结果已保存到: {result_file}")


