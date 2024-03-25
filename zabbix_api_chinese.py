#!/usr/bin/python3
# coding:utf-8

import argparse
import base64
import datetime
from datetime import datetime
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='zabbix  api ', usage='%(prog)s [options]')
    # ![]
    ######################################################################################################
    parser.add_argument('-export_all_template_item_sheet19', nargs='?', metavar='无参数', dest='export_all_template_item_sheet19', default='export_all_template_item_sheet19',
                        help=u"翻译所有模板监控项")
    parser.add_argument('-trans_template_item_to_chinese_sheet19', nargs='?', metavar='无参数', dest='trans_template_item_to_chinese_sheet19', default='trans_template_item_to_chinese_sheet19',
                        help=u"翻译模板监控项")
    parser.add_argument('-trans_all_template_item_to_chinese_sheet20', nargs='?', metavar='无参数', dest='trans_all_template_item_to_chinese_sheet20', default='trans_all_template_item_to_chinese_sheet20',
                        help=u"还原模板监控项")
    ######################################################################################################
    parser.add_argument('-export_all_template_trigger_sheet21', nargs='?', metavar='无参数', dest='export_all_template_trigger_sheet21', default='export_all_template_trigger_sheet21',
                        help=u"翻译所有模板触发器")
    parser.add_argument('-trans_template_trigger_to_chinese_sheet21', nargs='?', metavar='无参数', dest='trans_template_trigger_to_chinese_sheet21', default='trans_template_trigger_to_chinese_sheet21',
                        help=u"翻译模板触发器")
    parser.add_argument('-trans_all_template_trigger_to_chinese_sheet22', nargs='?', metavar='无参数', dest='trans_all_template_trigger_to_chinese_sheet22', default='trans_all_template_trigger_to_chinese_sheet22',
                        help=u"还原模板触发器")
    ######################################################################################################
    parser.add_argument('-export_all_template_graph_sheet23', nargs='?', metavar='无参数', dest='export_all_template_graph_sheet23', default='export_all_template_graph_sheet23',
                        help=u"翻译所有模板图表")
    parser.add_argument('-trans_template_graph_to_chinese_sheet23', nargs='?', metavar='无参数', dest='trans_template_graph_to_chinese_sheet23', default='trans_template_graph_to_chinese_sheet23',
                        help=u"翻译模板图表")
    parser.add_argument('-trans_all_template_graph_to_chinese_sheet24', nargs='?', metavar='无参数', dest='trans_all_template_graph_to_chinese_sheet24', default='trans_all_template_graph_to_chinese_sheet24',
                        help=u"还原模板图表")
    #########################################################################################################
    parser.add_argument('-export_all_template_itemprototype_sheet25', nargs='?', metavar='无参数', dest='export_all_template_itemprototype_sheet25', default='export_all_template_itemprototype_sheet25',
                        help=u"翻译所有模板监控项原型")
    parser.add_argument('-trans_template_itemprototype_to_chinese_sheet25', nargs='?', metavar='无参数', dest='trans_template_itemprototype_to_chinese_sheet25', default='trans_template_itemprototype_to_chinese_sheet25',
                        help=u"翻译模板监控项原型")
    parser.add_argument('-trans_all_template_itemprototype_to_chinese_sheet26', nargs='?', metavar='无参数', dest='trans_all_template_itemprototype_to_chinese_sheet26', default='trans_all_template_itemprototype_to_chinese_sheet26',
                        help=u"还原模板监控项原型")
    #########################################################################################################
    parser.add_argument('-export_all_template_triggerprototype_sheet27', nargs='?', metavar='无参数', dest='export_all_template_triggerprototype_sheet27', default='export_all_template_triggerprototype_sheet27',
                        help=u"翻译所有模板触发器类型")
    parser.add_argument('-trans_template_triggerprototype_to_chinese_sheet27', nargs='?', metavar='无参数', dest='trans_template_triggerprototype_to_chinese_sheet27', default='trans_template_triggerprototype_to_chinese_sheet27',
                        help=u"翻译模板触发器类型")
    parser.add_argument('-trans_all_template_triggerprototype_to_chinese_sheet28', nargs='?', metavar='无参数', dest='trans_all_template_triggerprototype_to_chinese_sheet28', default='trans_all_template_triggerprototype_to_chinese_sheet28',
                        help=u"还原模板触发器类型")
    #########################################################################################################
    parser.add_argument('-export_all_template_graphprototype_sheet29', nargs='?', metavar='无参数', dest='export_all_template_graphprototype_sheet29', default='export_all_template_graphprototype_sheet29',
                        help=u"翻译所有模板图表原型")
    parser.add_argument('-trans_template_graphprototype_to_chinese_sheet29', nargs='?', metavar='无参数', dest='trans_template_graphprototype_to_chinese_sheet29', default='trans_template_graphprototype_to_chinese_sheet29',
                        help=u"翻译模板图表原型")
    parser.add_argument('-trans_all_template_graphprototype_to_chinese_sheet30', nargs='?', metavar='无参数', dest='trans_all_template_graphprototype_to_chinese_sheet30', default='trans_all_template_graphprototype_to_chinese_sheet30',
                        help=u"还原模板图表原型")
    ######################################################################################################
    parser.add_argument('-export_all_template_trigger_event_name_sheet37', nargs='?', metavar='无参数', dest='export_all_template_trigger_event_name_sheet37', default='export_all_template_trigger_event_name_sheet37',
                        help=u"翻译所有模板触发器事件名称")
    parser.add_argument('-trans_all_template_trigger_event_name_to_chinese_sheet37', nargs='?', metavar='无参数', dest='trans_all_template_trigger_event_name_to_chinese_sheet37', default='trans_all_template_trigger_event_name_to_chinese_sheet37',
                        help=u"还原模板触发器事件名称")
    ######################################################################################################
    parser.add_argument('-export_all_template_triggerprototype_name_sheet38', nargs='?', metavar='无参数', dest='export_all_template_triggerprototype_name_sheet38', default='export_all_template_triggerprototype_name_sheet38',
                        help=u"翻译所有模板触发器原型事件名称")
    parser.add_argument('-trans_all_template_triggerprototype_name_to_chinese_sheet38', nargs='?', metavar='无参数', dest='trans_all_template_triggerprototype_name_to_chinese_sheet38', default='trans_all_template_triggerprototype_name_to_chinese_sheet38',
                        help=u"还原模板触发原型器事件名称")
    ######################################################################################################
    parser.add_argument('-export_all_template_tag_name_sheet40', nargs='?', metavar='无参数', dest='export_all_template_tag_name_sheet40', default='export_all_template_tag_name_sheet40',
                        help=u"翻译所有模板标签名称")
    parser.add_argument('-trans_all_template_tag_name_to_chinese_sheet40', nargs='?', metavar='无参数', dest='trans_all_template_tag_name_to_chinese_sheet40', default='trans_all_template_tag_name_to_chinese_sheet40',
                        help=u"还原模板标签名称")
    ######################################################################################################
    parser.add_argument('-export_all_template_item_tag_name_sheet41', nargs='?', metavar='无参数', dest='export_all_template_item_tag_name_sheet41', default='export_all_template_item_tag_name_sheet41',
                        help=u"翻译所有模板监控项标签名称")
    parser.add_argument('-trans_all_template_item_tag_name_to_chinese_sheet41', nargs='?', metavar='无参数', dest='trans_all_template_item_tag_name_to_chinese_sheet41', default='trans_all_template_item_tag_name_to_chinese_sheet41',
                        help=u"还原模板监控项标签名称")
    ######################################################################################################
    parser.add_argument('-export_all_template_trigger_tag_name_sheet42', nargs='?', metavar='无参数', dest='export_all_template_trigger_tag_name_sheet42', default='export_all_template_trigger_tag_name_sheet42',
                        help=u"翻译所有模板触发器标签名称")
    parser.add_argument('-trans_all_template_trigger_tag_name_to_chinese_sheet42', nargs='?', metavar='无参数', dest='trans_all_template_trigger_tag_name_to_chinese_sheet42', default='trans_all_template_trigger_tag_name_to_chinese_sheet42',
                        help=u"还原模板触发器标签名称")
    ######################################################################################################
    parser.add_argument('-export_all_template_itemprototype_tag_sheet43', nargs='?', metavar='无参数', dest='export_all_template_itemprototype_tag_sheet43', default='export_all_template_itemprototype_tag_sheet43',
                        help=u"翻译所有模板监控项原型标签")
    parser.add_argument('-trans_all_template_itemprototype_tag_to_chinese_sheet43', nargs='?', metavar='无参数', dest='trans_all_template_itemprototype_tag_to_chinese_sheet43', default='trans_all_template_itemprototype_tag_to_chinese_sheet43',
                        help=u"还原模板监控项原型标签")
    #########################################################################################################
    parser.add_argument('-export_all_template_triggerprototype_tag_sheet44', nargs='?', metavar='无参数', dest='export_all_template_triggerprototype_tag_sheet44', default='export_all_template_triggerprototype_tag_sheet44',
                        help=u"翻译所有模板监控项原型标签")
    parser.add_argument('-trans_all_template_triggerprototype_tag_to_chinese_sheet44', nargs='?', metavar='无参数', dest='trans_all_template_triggerprototype_tag_to_chinese_sheet44', default='trans_all_template_triggerprototype_tag_to_chinese_sheet44',
                        help=u"还原模板监控项原型标签")
    ######################################################################################################
    parser.add_argument('-export_all_hostgroup_name_sheet45', nargs='?', metavar='无参数', dest='export_all_hostgroup_name_sheet45', default='export_all_hostgroup_name_sheet45',
                        help=u"翻译主机组名称")
    parser.add_argument('-trans_all_hostgroup_name_to_chinese_sheet45', nargs='?', metavar='无参数', dest='trans_all_hostgroup_name_to_chinese_sheet45', default='trans_all_hostgroup_name_to_chinese_sheet45',
                        help=u"还原主机组名称")
    ######################################################################################################
    parser.add_argument('-export_all_templategroup_name_sheet46', nargs='?', metavar='无参数', dest='export_all_templategroup_name_sheet46', default='export_all_templategroup_name_sheet46',
                        help=u"翻译模板组名称")
    parser.add_argument('-trans_all_templategroup_name_to_chinese_sheet46', nargs='?', metavar='无参数', dest='trans_all_templategroup_name_to_chinese_sheet46', default='trans_all_templategroup_name_to_chinese_sheet46',
                        help=u"还原模板组名称")
    ######################################################################################################
    parser.add_argument('-export_all_application_name_sheet47', nargs='?', metavar='无参数', dest='export_all_application_name_sheet47', default='export_all_application_name_sheet47',
                        help=u"翻译模板应用集名称")
    parser.add_argument('-trans_all_application_name_to_chinese_sheet47', nargs='?', metavar='无参数', dest='trans_all_application_name_to_chinese_sheet47', default='trans_all_application_name_to_chinese_sheet47',
                        help=u"还原模板应用集名称")
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
        # ![19_翻译模板监控项]
        if args.export_all_template_item_sheet19 != 'export_all_template_item_sheet19':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=19)
            title_name = ['序号', '模板序号', '监控项序号', '模板名称', '监控项ID', '英文名称', '中文名称', '原因']
            v_1 = 'name'
            v_2 = 'itemid'
            v_3 = cus_zabbix_api.def_get_template_item_name
            v_4 = cus_zabbix_api.def_update_item_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![19_翻译模板监控项]
        elif args.trans_template_item_to_chinese_sheet19 != 'trans_template_item_to_chinese_sheet19':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=19)
            title_name = ['序号', '模板序号', '监控项序号', '模板名称', '监控项ID', '英文名称', '中文名称', '原因']
            v_1 = 'name'
            v_2 = 'itemid'
            v_3 = cus_zabbix_api.def_get_template_item_name
            v_4 = cus_zabbix_api.def_update_item_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![20_还原模板监控项]
        elif args.trans_all_template_item_to_chinese_sheet20 != 'trans_all_template_item_to_chinese_sheet20':
            cus_excel_op.def_load_excel(file='./trans/19_翻译模板监控项_.xlsx', index=1)
            v_1 = 'name'
            v_2 = 'itemid'
            v_4 = cus_zabbix_api.def_update_item_name
            cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![21_翻译模板触发器]
        elif args.export_all_template_trigger_sheet21 != 'export_all_template_trigger_sheet21':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=21)
            title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
            v_1 = 'description'
            v_2 = 'triggerid'
            v_3 = cus_zabbix_api.def_get_template_trigger_name
            v_4 = cus_zabbix_api.def_update_trigger_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![21_翻译模板触发器]
        elif args.trans_template_trigger_to_chinese_sheet21 != 'trans_template_trigger_to_chinese_sheet21':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=21)
            title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
            v_1 = 'description'
            v_2 = 'triggerid'
            v_3 = cus_zabbix_api.def_get_template_trigger_name
            v_4 = cus_zabbix_api.def_update_trigger_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![22_还原模板触发器]
        ######################################################################################################
        elif args.trans_all_template_trigger_to_chinese_sheet22 != 'trans_all_template_trigger_to_chinese_sheet22':
            cus_excel_op.def_load_excel(file='./trans/21_翻译模板触发器_.xlsx', index=1)
            v_1 = 'description'
            v_2 = 'triggerid'
            v_4 = cus_zabbix_api.def_update_trigger_name
            cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        # ![23_翻译模板图形]
        if args.export_all_template_graph_sheet23 != 'export_all_template_graph_sheet23':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=23)
            title_name = ['序号', '模板序号', '图表序号', '模板名称', '图表ID', '英文名称', '中文名称', '原因']
            v_1 = 'name'
            v_2 = 'graphid'
            v_3 = cus_zabbix_api.def_get_template_graph_name
            v_4 = cus_zabbix_api.def_update_graph_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![23_翻译模板图形]
        elif args.trans_template_graph_to_chinese_sheet23 != 'trans_template_graph_to_chinese_sheet23':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=23)
            title_name = ['序号', '模板序号', '图表序号', '模板名称', '图表ID', '英文名称', '中文名称', '原因']
            v_1 = 'name'
            v_2 = 'graphid'
            v_3 = cus_zabbix_api.def_get_template_graph_name
            v_4 = cus_zabbix_api.def_update_graph_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![24_还原模板图形]
        elif args.trans_all_template_graph_to_chinese_sheet24 != 'trans_all_template_graph_to_chinese_sheet24':
            cus_excel_op.def_load_excel(file='./trans/23_翻译模板图形_.xlsx', index=1)
            v_1 = 'name'
            v_2 = 'graphid'
            v_4 = cus_zabbix_api.def_update_graph_name
            cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![25_翻译模板监控项原型]
        elif args.export_all_template_itemprototype_sheet25 != 'export_all_template_itemprototype_sheet25':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=25)
            title_name = ['序号', '模板序号', '监控项序号', '模板名称', '监控项ID', '英文名称', '中文名称', '原因']
            v_1 = 'name'
            v_2 = 'itemid'
            v_3 = cus_zabbix_api.def_get_template_itemprototype_name
            v_4 = cus_zabbix_api.def_update_itemprototype_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![25_翻译模板监控项原型]
        elif args.trans_template_itemprototype_to_chinese_sheet25 != 'trans_template_itemprototype_to_chinese_sheet25':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=25)
            title_name = ['序号', '模板序号', '监控项序号', '模板名称', '监控项ID', '英文名称', '中文名称', '原因']
            v_1 = 'name'
            v_2 = 'itemid'
            v_3 = cus_zabbix_api.def_get_template_itemprototype_name
            v_4 = cus_zabbix_api.def_update_itemprototype_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![26_还原模板监控项原型]
        elif args.trans_all_template_itemprototype_to_chinese_sheet26 != 'trans_all_template_itemprototype_to_chinese_sheet26':
            cus_excel_op.def_load_excel(file='./trans/25_翻译模板监控项原型_.xlsx', index=1)
            v_1 = 'name'
            v_2 = 'itemid'
            v_4 = cus_zabbix_api.def_update_itemprototype_name
            cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![27_翻译模板触发器类型]
        elif args.export_all_template_triggerprototype_sheet27 != 'export_all_template_triggerprototype_sheet27':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=27)
            title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
            v_1 = 'description'
            v_2 = 'triggerid'
            v_3 = cus_zabbix_api.def_get_template_triggerprototype_name
            v_4 = cus_zabbix_api.def_update_triggerprototype_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![27_翻译模板触发器类型]
        elif args.trans_template_triggerprototype_to_chinese_sheet27 != 'trans_template_triggerprototype_to_chinese_sheet27':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=27)
            title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
            v_1 = 'description'
            v_2 = 'triggerid'
            v_3 = cus_zabbix_api.def_get_template_triggerprototype_name
            v_4 = cus_zabbix_api.def_update_triggerprototype_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![28_还原模板触发器类型]
        elif args.trans_all_template_triggerprototype_to_chinese_sheet28 != 'trans_all_template_triggerprototype_to_chinese_sheet28':
            cus_excel_op.def_load_excel(file='./trans/27_翻译模板触发器类型_.xlsx', index=1)
            v_1 = 'description'
            v_2 = 'triggerid'
            v_4 = cus_zabbix_api.def_update_triggerprototype_name
            cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![29_翻译模板图形原型]
        elif args.export_all_template_graphprototype_sheet29 != 'export_all_template_graphprototype_sheet29':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=29)
            title_name = ['序号', '模板序号', '图表序号', '模板名称', '图表ID', '英文名称', '中文名称', '原因']
            v_1 = 'name'
            v_2 = 'graphid'
            v_3 = cus_zabbix_api.def_get_template_graphprototype_name
            v_4 = cus_zabbix_api.def_update_graphprototype_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![29_翻译模板图形原型]
        elif args.trans_template_graphprototype_to_chinese_sheet29 != 'trans_template_graphprototype_to_chinese_sheet29':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=29)
            title_name = ['序号', '模板序号', '图表序号', '模板名称', '图表ID', '英文名称', '中文名称', '原因']
            v_1 = 'name'
            v_2 = 'graphid'
            v_3 = cus_zabbix_api.def_get_template_graphprototype_name
            v_4 = cus_zabbix_api.def_update_graphprototype_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![30_还原模板图形原型]
        elif args.trans_all_template_graphprototype_to_chinese_sheet30 != 'trans_all_template_graphprototype_to_chinese_sheet30':
            cus_excel_op.def_load_excel(file='./trans/29_翻译模板图形原型_.xlsx', index=1)
            v_1 = 'name'
            v_2 = 'graphid'
            v_4 = cus_zabbix_api.def_update_graphprototype_name
            cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![37_翻译模板触发器事件名称]
        elif args.export_all_template_trigger_event_name_sheet37 != 'export_all_template_trigger_event_name_sheet37':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=37)
            title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
            v_1 = 'event_name'
            v_2 = 'triggerid'
            v_3 = cus_zabbix_api.def_get_template_event_name
            v_4 = cus_zabbix_api.def_update_trigger_name
            cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![37_还原模板触发器类型]
        elif args.trans_all_template_trigger_event_name_to_chinese_sheet37 != 'trans_all_template_trigger_event_name_to_chinese_sheet37':
            cus_excel_op.def_load_excel(file='./trans/37_翻译模板触发器事件名称_.xlsx', index=1)
            v_1 = 'event_name'
            v_2 = 'triggerid'
            v_4 = cus_zabbix_api.def_update_trigger_name
            cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![38_翻译模板原型触发器事件名称]
        elif args.export_all_template_triggerprototype_name_sheet38 != 'export_all_template_triggerprototype_name_sheet38':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=38)
                title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
                v_1 = 'event_name'
                v_2 = 'triggerid'
                v_3 = cus_zabbix_api.def_get_template_triggerprototype_event_name
                v_4 = cus_zabbix_api.def_update_triggerprototype_name
                cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![38_还原模板触原型发器类型]
        elif args.trans_all_template_triggerprototype_name_to_chinese_sheet38 != 'trans_all_template_triggerprototype_name_to_chinese_sheet38':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.def_load_excel(file='./trans/38_翻译模板原型触发器事件名称_.xlsx', index=1)
                v_1 = 'event_name'
                v_2 = 'triggerid'
                v_4 = cus_zabbix_api.def_update_triggerprototype_name
                cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![40_翻译所有模板标签名称]
        elif args.export_all_template_tag_name_sheet40 != 'export_all_template_tag_name_sheet40':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=40)
                title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
                v_1 = 'tags'
                v_2 = 'templateid'
                v_3 = cus_zabbix_api.def_get_template_tags_bytemplateid
                v_4 = cus_zabbix_api.def_update_tags_bytemplateid
                cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![40_还原模板标签名称]
        elif args.trans_all_template_tag_name_to_chinese_sheet40 != 'trans_all_template_tag_name_to_chinese_sheet40':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.def_load_excel(file='./trans/40_翻译所有模板标签名称_.xlsx', index=1)
                v_1 = 'tags'
                v_2 = 'templateid'
                v_4 = cus_zabbix_api.def_update_tags_bytemplateid
                cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![41_翻译所有模板监控项标签名称]
        elif args.export_all_template_item_tag_name_sheet41 != 'export_all_template_item_tag_name_sheet41':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=41)
                title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
                v_1 = 'tags'
                v_2 = 'itemid'
                v_3 = cus_zabbix_api.def_get_template_item_tags_bytemplateid
                v_4 = cus_zabbix_api.def_update_template_item_tags_bytemplateid
                cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![41_还原模板监控项标签名称]
        elif args.trans_all_template_item_tag_name_to_chinese_sheet41 != 'trans_all_template_item_tag_name_to_chinese_sheet41':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.def_load_excel(file='./trans/41_翻译所有模板监控项标签名称_.xlsx', index=1)
                v_1 = 'tags'
                v_2 = 'itemid'
                v_4 = cus_zabbix_api.def_update_template_item_tags_bytemplateid
                cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![42_翻译所有模板触发器标签名称]
        elif args.export_all_template_trigger_tag_name_sheet42 != 'export_all_template_trigger_tag_name_sheet42':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=42)
                title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
                v_1 = 'tags'
                v_2 = 'triggerid'
                v_3 = cus_zabbix_api.def_get_template_trigger_tags_bytemplateid
                v_4 = cus_zabbix_api.def_update_template_trigger_tags_bytemplateid
                cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![42_还原模板触发器标签名称]
        elif args.trans_all_template_trigger_tag_name_to_chinese_sheet42 != 'trans_all_template_trigger_tag_name_to_chinese_sheet42':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.def_load_excel(file='./trans/42_翻译所有模板触发器标签名称_.xlsx', index=1)
                v_1 = 'tags'
                v_2 = 'triggerid'
                v_4 = cus_zabbix_api.def_update_template_trigger_tags_bytemplateid
                cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![43_翻译模板监控项原型标签]
        elif args.export_all_template_itemprototype_tag_sheet43 != 'export_all_template_itemprototype_tag_sheet43':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=43)
                title_name = ['序号', '模板序号', '监控项序号', '模板名称', '监控项ID', '英文名称', '中文名称', '原因']
                v_1 = 'tags'
                v_2 = 'itemid'
                v_3 = cus_zabbix_api.def_get_template_itemprototype_tags_bytemplateid
                v_4 = cus_zabbix_api.def_update_itemprototype_tags_bytemplateid
                cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![43_还原模板监控项原型标签]
        elif args.trans_all_template_itemprototype_tag_to_chinese_sheet43 != 'trans_all_template_itemprototype_tag_to_chinese_sheet43':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.def_load_excel(file='./trans/43_翻译模板监控项原型标签_.xlsx', index=1)
                title_name = ['序号', '模板序号', '监控项序号', '模板名称', '监控项ID', '英文名称', '中文名称', '原因']
                v_1 = 'tags'
                v_2 = 'itemid'
                v_4 = cus_zabbix_api.def_update_itemprototype_tags_bytemplateid
                cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![44_翻译模板原型触发器标签]
        elif args.export_all_template_triggerprototype_tag_sheet44 != 'export_all_template_triggerprototype_tag_sheet44':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=44)
                title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
                v_1 = 'tags'
                v_2 = 'triggerid'
                v_3 = cus_zabbix_api.def_get_template_triggerprototype_tag_bytemplateid
                v_4 = cus_zabbix_api.def_update_triggerprototype_tag_bytemplateid
                cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)
        # ![44_还原模板原型触发器标签]
        elif args.trans_all_template_triggerprototype_tag_to_chinese_sheet44 != 'trans_all_template_triggerprototype_tag_to_chinese_sheet44':
            lv_dic_zbx_version = {'6.0': '6.0',
                                  '6.4': '6.4'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.def_load_excel(file='./trans/44_翻译模板原型触发器标签_.xlsx', index=1)
                v_1 = 'tags'
                v_2 = 'triggerid'
                v_4 = cus_zabbix_api.def_update_triggerprototype_tag_bytemplateid
                cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![45_翻译主机组名称]
        elif args.export_all_hostgroup_name_sheet45 != 'export_all_hostgroup_name_sheet45':
            cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=45)
            title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
            v_3 = cus_zabbix_api.def_get_all_hostgroup()
            row_index = {"index": 2}
            cus_excel_op.def_creat_excel()
            cus_excel_op.def_create_sheet(cus_zabbix_api.def_check_zbx_version()['result']),
            lv_result = None
            if v_3['tag'] is True:
                for f_1 in range(len(v_3['result'])):
                    [cus_excel_op.def_set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))],
                    cus_excel_op.def_set_cell_value(row_index['index'], 1, row_index['index'] - 1),
                    cus_excel_op.def_set_cell_value(row_index['index'], 2, u'({0}/{1})'.format(len(v_3['result']), f_1 + 1)),
                    cus_excel_op.def_set_cell_value(row_index['index'], 3, ""),
                    cus_excel_op.def_set_cell_value(row_index['index'], 4, ""),
                    cus_excel_op.def_set_cell_value(row_index['index'], 5, v_3['result'][f_1]['groupid']),
                    cus_excel_op.def_set_cell_value(row_index['index'], 6, v_3['result'][f_1]['name']),
                    cus_excel_op.def_set_cell_value(row_index['index'], 7, v_3['result'][f_1]['name']),
                    GV_ERROR_MESS.update(error=''),
                    print(u'(\033[;34m{0}\033[0m/\033[;34m{1}\033[0m)|\033[;34m{2}\033[0m > \033[;34m{3}'.format(len(v_3['result']), f_1 + 1, v_3['result'][f_1]['groupid'], v_3['result'][f_1]['name'])),
                    row_index.update(index=row_index['index'] + 1),
            cus_excel_op.def_save_create_xlsx(cus_excel_op.sheet_name + '.xlsx')

        # ![45_还原主机组名称]
        elif args.trans_all_hostgroup_name_to_chinese_sheet45 != 'trans_all_hostgroup_name_to_chinese_sheet45':
            cus_excel_op.def_load_excel(file='./trans/45_翻译主机组名称_.xlsx', index=1)
            v_1 = 'name'
            v_2 = 'groupid'
            v_4 = cus_zabbix_api.def_update_all_hostgroup_name
            cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![46_翻译模板组名称]
        elif args.export_all_templategroup_name_sheet46 != 'export_all_templategroup_name_sheet46':
            lv_dic_zbx_version = {'6.4': '6.4'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=46)
                title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
                v_3 = cus_zabbix_api.def_get_all_templategroup()
                row_index = {"index": 2}
                cus_excel_op.def_creat_excel()
                cus_excel_op.def_create_sheet(cus_zabbix_api.def_check_zbx_version()['result']),
                lv_result = None
                if v_3['tag'] is True:
                    for f_1 in range(len(v_3['result'])):
                        [cus_excel_op.def_set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))],
                        cus_excel_op.def_set_cell_value(row_index['index'], 1, row_index['index'] - 1),
                        cus_excel_op.def_set_cell_value(row_index['index'], 2, u'({0}/{1})'.format(len(v_3['result']), f_1 + 1)),
                        cus_excel_op.def_set_cell_value(row_index['index'], 3, ""),
                        cus_excel_op.def_set_cell_value(row_index['index'], 4, ""),
                        cus_excel_op.def_set_cell_value(row_index['index'], 5, v_3['result'][f_1]['groupid']),
                        cus_excel_op.def_set_cell_value(row_index['index'], 6, v_3['result'][f_1]['name']),
                        cus_excel_op.def_set_cell_value(row_index['index'], 7, v_3['result'][f_1]['name']),
                        GV_ERROR_MESS.update(error=''),
                        print(u'(\033[;34m{0}\033[0m/\033[;34m{1}\033[0m)|\033[;34m{2}\033[0m > \033[;34m{3}'.format(len(v_3['result']), f_1 + 1, v_3['result'][f_1]['groupid'], v_3['result'][f_1]['name'])),
                        row_index.update(index=row_index['index'] + 1),
                cus_excel_op.def_save_create_xlsx(cus_excel_op.sheet_name + '.xlsx')

        # ![46_还原模板组名称]
        elif args.trans_all_templategroup_name_to_chinese_sheet46 != 'trans_all_templategroup_name_to_chinese_sheet46':
            lv_dic_zbx_version = {'6.4': '6.4'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.def_load_excel(file='./trans/46_翻译模板组名称_.xlsx', index=1)
                v_1 = 'name'
                v_2 = 'groupid'
                v_4 = cus_zabbix_api.def_update_all_templategroup_name
                cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)
        ######################################################################################################
        # ![47_翻译模板应用集名称]
        elif args.export_all_application_name_sheet47 != 'export_all_application_name_sheet47':
            lv_dic_zbx_version = {'5.0': '5.0'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.def_load_excel(file='zabbix_api.xlsx', index=47)
                title_name = ['序号', '模板序号', '触发器序号', '模板名称', '触发器ID', '英文名称', '中文名称', '原因']
                v_1 = 'name'
                v_2 = 'applicationid'
                v_3 = cus_zabbix_api.def_get_template_application_bytemplateid
                v_4 = cus_zabbix_api.def_update_template_application_bytemplateid
                cus_zabbix_api.def_get_en_list(cus_excel_op, title_name, v_1, v_2, v_3, v_4)

        # ![47_还原模板组名称]
        elif args.trans_all_application_name_to_chinese_sheet47 != 'trans_all_application_name_to_chinese_sheet47':
            lv_dic_zbx_version = {'5.0': '5.0'}
            if lv_dic_zbx_version.get(cus_zabbix_api.def_check_zbx_version()['result'][0:3], None):
                cus_excel_op.def_load_excel(file='./trans/47_翻译模板应用集名称_.xlsx', index=1)
                v_1 = 'name'
                v_2 = 'applicationid'
                v_4 = cus_zabbix_api.def_update_template_application_bytemplateid
                cus_zabbix_api.def_set_zh_list(cus_excel_op, v_2, v_1, v_4)


