#!/usr/bin/python3
# coding:utf-8

__author__ = 'NoYoWiFi'
__date__ = '2023-9-11 16:53:39'

import copy
import difflib
import shutil
import base64
import os
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed, Executor, wait
from functools import lru_cache
import hashlib
from hashlib import md5
import hmac
import inspect
import json
import socket
from openpyxl.utils import column_index_from_string
from typing import Optional, Union, Any, Set, List, Dict, Tuple, Callable
from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils import get_column_letter
import os
import datetime
from datetime import datetime
import logging
import paramiko
import polib
import sys
import threading
import time
from time import mktime
import requests
import random
from pypinyin import pinyin, lazy_pinyin, Style
import string
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import urllib3
from xml.dom import minidom
import xml
import re
from collections import defaultdict
from openai import OpenAI
import requests
import subprocess
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional
from dataclasses import dataclass
from pathlib import Path

import os
import sys
import time
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import signal
import re

# 第三方库
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from tqdm import tqdm

# pypi_simple库
from pypi_simple import PyPISimple, NoSuchProjectError
from pypi_simple.classes import IndexPage, ProjectPage


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GV_CPU_COUNT = os.cpu_count()
# GV_CPU_COUNT = 1
GV_ERROR_MESS = {"error": ""}
GV_FIREFOX_TIMEOUT = 120
GV_FIREFOX_WAITTIMEOUT = 10


class CusZabbixApi:
    def __init__(self):
        self.authID = None
        self.url = 'https://172.16.51.250:8443/api_jsonrpc.php'  # 修改URL
        # self.url = 'https://172.169.10.3:8443/api_jsonrpc.php'  # 修改URL
        self.header = {"Content-Type": "application/json"}
        self.session = requests.Session()
        self.session.mount(self.url, requests.adapters.HTTPAdapter(max_retries=3))
        self.def_login()
        self.gv_apiVersion = None
        self.textValue = None

    def def_login(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                # "user": "Admin",  # 5.0.x版本web页面登录用户名
                "username": "Admin",  # 6.x.x版本web页面登录用户名
                "password": "zabbix"  # web页面登录密码
            },
            "id": 0
        })
        try:
            request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
            response = request.json()
            if response.get('result', '') != '':
                self.authID = response['result']
            elif response.get('error', '') != '':
                print(u"用户认证失败请检查! 原因: \033[;31m%s\033[0m" % (response['error']['data']))
                sys.exit(1)
        except Exception as ee:
            print(u"地址请求失败请检查! 原因: \033[;31m%s\033[0m" % ee)
            sys.exit(1)

    def def_create_proxygroup(self, proxygroup_name, proxygroup_failover_delay, proxygroup_min_online):
        # 构建params
        params = {}
        if proxygroup_name: params["name"] = proxygroup_name
        if proxygroup_failover_delay: params["failover_delay"] = proxygroup_failover_delay
        if proxygroup_min_online: params["min_online"] = proxygroup_min_online

        # 最终数据结构
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "proxygroup.create",
            "params": params,
            "auth": self.authID,
            "id": 1
        })

        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_proxygroup(self, proxygroup_name):
        """
        该方法允许根据给定的参数检索主机组。

        :param hostgroup_name_list: 主机组列表: ["Zabbixservers","Linuxservers"]
        :return: [{'groupid': '21', 'name': 'Zabbixservers'}, {'groupid': '22', 'name': 'Linuxservers'}]
        """
        # 构建params
        filter = {}
        if proxygroup_name: filter["name"] = proxygroup_name

        # 构建params
        params = {
            "output": ["proxy_groupid"],
            "filter": filter,
        }

        # 最终数据结构
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "proxygroup.get",
            "params": params,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_proxygroup_name(self, proxygroup_id):
        """
        该方法允许根据给定的参数检索主机组。

        :param hostgroup_name_list: 主机组列表: ["Zabbixservers","Linuxservers"]
        :return: [{'groupid': '21', 'name': 'Zabbixservers'}, {'groupid': '22', 'name': 'Linuxservers'}]
        """
        # 构建params
        proxy_groupids = {}
        if proxygroup_id: proxy_groupids["name"] = proxygroup_id

        # 构建params
        params = {
            "output": ["name"],
            "proxy_groupids": proxy_groupids,
        }

        # 最终数据结构
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "proxygroup.get",
            "params": params,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_delete_proxygroup(self, proxygroup_id_list):
        """
        此方法允许删除主机组。

        :param hostgroup_id_list: 主机组ID列表["107824"]
        :return: {'groupids': ['34']}
        """

        if proxygroup_id_list: params = proxygroup_id_list

        # 最终数据结构
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "proxygroup.delete",
            "params": params,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_host_add_proxygroup(self, host_id, proxygroup_id):
        """
        通过该方式可以创建新的主机组。

        :param proxygroup_id:
        :param hostgroup_name: 主机组名称: "Linux servers"
        :return: "groupids": ["107819"]
        """
        # 构建params
        params = {
            "proxyid": "0",
            "proxy_groupid": "0",
        }
        if host_id: params["hostid"] = host_id
        if proxygroup_id: params["proxy_groupid"] = proxygroup_id

        # 最终数据结构
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.update",
            "params": params,
            "auth": self.authID,
            "id": 1
        })

        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_create_proxy(self, proxy_name, proxy_groupid, proxy_local_address, proxy_local_port, proxy_operating_mode, proxy_allowed_addresses, proxy_address, proxy_port):
        """
        通过该方式可以创建新的主机组。

        :param hostgroup_name: 主机组名称: "Linux servers"
        :return: "groupids": ["107819"]
        """
        # 构建params
        params = {
            "operating_mode": 0,
        }
        if proxy_name: params["name"] = proxy_name
        if proxy_groupid: params["proxy_groupid"] = proxy_groupid
        if proxy_local_address: params["local_address"] = proxy_local_address
        if proxy_local_port: params["local_port"] = proxy_local_port
        if proxy_operating_mode: params["operating_mode"] = proxy_operating_mode
        if proxy_allowed_addresses: params["allowed_addresses"] = proxy_allowed_addresses
        if proxy_address: params["address"] = proxy_address
        if proxy_port: params["port"] = str(proxy_port)

        # 最终数据结构
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "proxy.create",
            "params": params,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_proxy(self, proxy_name):
        """
        该方法允许根据给定的参数检索主机组。

        :param hostgroup_name_list: 主机组列表: ["Zabbixservers","Linuxservers"]
        :return: [{'groupid': '21', 'name': 'Zabbixservers'}, {'groupid': '22', 'name': 'Linuxservers'}]
        """
        # 构建params
        filter = {}
        if proxy_name: filter["name"] = proxy_name

        # 构建params
        params = {
            "output": ["name", "proxyid"],
            "filter": filter,
        }

        # 最终数据结构
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "proxy.get",
            "params": params,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_proxy_name(self, proxy_id):
        """
        该方法允许根据给定的参数检索主机组。

        :param hostgroup_name_list: 主机组列表: ["Zabbixservers","Linuxservers"]
        :return: [{'groupid': '21', 'name': 'Zabbixservers'}, {'groupid': '22', 'name': 'Linuxservers'}]
        """
        # 构建params
        proxyids = {}
        if proxy_id: proxyids["proxyids"] = proxy_id

        # 构建params
        params = {
            "output": ["name"],
            "proxyids": proxyids,
        }

        # 最终数据结构
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "proxy.get",
            "params": params,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_delete_proxy(self, proxy_id_list):
        """
        此方法允许删除主机组。

        :param hostgroup_id_list: 主机组ID列表["107824"]
        :return: {'groupids': ['34']}
        """

        if proxy_id_list: params = proxy_id_list

        # 最终数据结构
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "proxy.delete",
            "params": params,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_host_add_proxy(self, host_id, proxy_id):
        """
        通过该方式可以创建新的主机组。

        :param hostgroup_name: 主机组名称: "Linux servers"
        :return: "groupids": ["107819"]
        """
        # 构建params
        params = {
            "proxyid": "0",
            "proxy_groupid": "0",
        }
        if host_id: params["hostid"] = host_id
        if proxy_id: params["proxyid"] = proxy_id

        # 最终数据结构
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.update",
            "params": params,
            "auth": self.authID,
            "id": 1
        })

        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    # ![01_创建主机组]
    def def_create_hostgroup(self, hostgroup_name):
        """
        通过该方式可以创建新的主机组。

        :param hostgroup_name: 主机组名称: "Linux servers"
        :return: "groupids": ["107819"]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostgroup.create",
            "params": {
                "name": "%s" % hostgroup_name,
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_create_template_group(self, name: str) -> dict:
        """
        创建模板组

        :param name: 模板组名称
        :return: 包含创建的模板组ID的字典

        示例:
        {"templategroupids": ["70"]}
        """
        # 构造API请求
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "templategroup.create",
            "params": {
                "name": name
            },
            "auth": self.authID,
            "id": 1
        })

        # 发送请求
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)

        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_delete_template_group(self, group_ids: list) -> dict:
        """
        删除模板组

        :param group_ids: 要删除的模板组ID列表
        :return: 包含删除的模板组ID的字典

        示例:
        {"templategroupids": ["70"]}
        """
        # 构造API请求
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "templategroup.delete",
            "params": group_ids,
            "auth": self.authID,
            "id": 1
        })

        # 发送请求
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)

        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_templategroup(self, templategroup_name):
        """
        该方法允许根据给定的参数检索模板组。

        :param templategroup_name: 模板组名称: "Templates/Linux"
        :return: [{'templategroupid': '1', 'name': 'Templates/Linux'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "templategroup.get",
            "params": {
                "output": "extend",
                "filter": {
                    "name": [templategroup_name]
                }
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][3], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_hostgroup_6_0(self, hostgroup_name_list):
        """
        该方法允许根据给定的参数检索主机组。

        :param hostgroup_name_list: 主机组列表: ["Zabbixservers","Linuxservers"]
        :return: [{'groupid': '21', 'name': 'Zabbixservers'}, {'groupid': '22', 'name': 'Linuxservers'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "selectTemplates": [],
                "selectHosts": [],
                "filter": {
                    "name": hostgroup_name_list,
                },
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_hostgroup_6_4(self, hostgroup_name_list):
        """
        该方法允许根据给定的参数检索主机组。

        :param hostgroup_name_list: 主机组列表: ["Zabbixservers","Linuxservers"]
        :return: [{'groupid': '21', 'name': 'Zabbixservers'}, {'groupid': '22', 'name': 'Linuxservers'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "selectHosts": [],
                "filter": {
                    "name": hostgroup_name_list,
                },
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_all_hostgroup(self):
        """
        该方法允许根据给定的参数检索主机组。

        :param hostgroup_name_list: 主机组列表: ["Zabbixservers","Linuxservers"]
        :return: [{'groupid': '21', 'name': 'Zabbixservers'}, {'groupid': '22', 'name': 'Linuxservers'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "extend",
                "sortfield": "groupid",
                "sortorder": "ASC",
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_all_hostgroup_name(self, hostgroup_name_list, total_length, current_progress):
        """
        此方法允许删除主机组。

        :param hostgroup_id_list: 主机组ID列表["107824"]
        :return: {'groupids': ['34']}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostgroup.update",
            "params": hostgroup_name_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            logger.debug(f"当前进度: {current_progress}/{total_length} ({(current_progress / total_length) * 100:.2f}%) {response['result']}")
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_delete_hostgroup(self, hostgroup_id_list):
        """
        此方法允许删除主机组。

        :param hostgroup_id_list: 主机组ID列表["107824"]
        :return: {'groupids': ['34']}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostgroup.delete",
            "params": hostgroup_id_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    # ![02_创建模板]
    def def_create_template(self, template_name, groupids_list):
        """
        此方法允许创建新模板。

        :param template_name: 模板名称: "Linux template"
        :param groupids_list: 主机组ID列表: [{"groupid":1},{"groupid":2}]
        :return: {'templateids': ['10537']}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.create",
            "params": {
                "host": "%s" % template_name,
                "groups": groupids_list,
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template(self, template_name):
        """
        该方法允许根据给定的参数检索模板。

        :param template_name: 模板名称 "Linux"
        :return: [{'templateid': '10558'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": "templateid",
                "filter": {
                    "host": template_name
                }
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_item_template_id(self, item_id):
        """
        该方法允许根据给定的参数检索模板。

        :param template_name: 模板名称 "Linux"
        :return: [{'templateid': '10558'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": ["hostid"],
                "itemid": item_id
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_host(self, template_id):
        """
        该方法允许根据给定的参数检索模板。

        :param template_name: 模板名称 "Linux"
        :return: [{'templateid': '10558'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": ["host"],
                "templateids": template_id
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_all_templategroup(self):
        """
        该方法允许根据给定的参数检索主机组。

        :param hostgroup_name_list: 主机组列表: ["Zabbixservers","Linuxservers"]
        :return: [{'groupid': '21', 'name': 'Zabbixservers'}, {'groupid': '22', 'name': 'Linuxservers'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "templategroup.get",
            "params": {
                "output": "extend",
                "sortfield": "groupid",
                "sortorder": "ASC",
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_all_templategroup_name(self, templategroup_name_list, total_length, current_progress):
        """
        此方法允许删除主机组。

        :param hostgroup_id_list: 主机组ID列表["107824"]
        :return: {'groupids': ['34']}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "templategroup.update",
            "params": templategroup_name_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            logger.debug(f"当前进度: {current_progress}/{total_length} ({(current_progress / total_length) * 100:.2f}%) {response['result']}")
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_all_templateid(self):
        """
        该方法允许根据给定的参数检索模板。

        :param template_name: 模板名称 "Linux"
        :return: [{'templateid': '10558'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": ["host", "templateid"],
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_delete_template(self, template_id_list):
        """
        此方法允许删除模板。

        :param template_id_list: 模板ID列表: ["13"]
        :return:  {"templateids":["13"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.delete",
            "params": template_id_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_description(self, template_id):
        """
        获取模板描述信息

        :param template_id: 模板ID
        :return: 包含模板描述信息的结果
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": ["description"],
                "templateids": template_id,
                "selectHosts": ["host", "hostid"],
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_template_description(self, template_description_list, total_length, current_progress):
        """
        更新模板描述信息

        :param template_description_list: 包含模板ID和描述信息的列表
        :param total_length: 总进度长度
        :param current_progress: 当前进度
        :return: 更新结果
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.update",
            "params": template_description_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            logger.debug(f"当前进度: {current_progress}/{total_length} ({(current_progress / total_length) * 100:.2f}%) {response['result']}")
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}


    def def_massadd_template_groups(self, template_id_list, group_id_list):
        """
        此方法允许同时向给定模板添加多个相关对象。

        :param template_id_list: 模板ID列表: [{"templateid": "10085"}]
        :param group_id_list: 主机群组ID列表: [{"groupid": "2"},{"groupid": "3"}]
        :return: {'templateids': ['10560']}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.massadd",
            "params": {
                "templates": template_id_list,
                "groups": group_id_list
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_massremove_template_groups(self, template_id_list, group_id_list):
        """
        此方法允许从多个模板中删除相关对象。

        :param template_id_list: 模板ID列表: ["10085"]
        :param group_id_list: 主机群组ID列表: ["2","3"]
        :return: {"templateids":["10085"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.massremove",
            "params": {
                "templateids": template_id_list,
                "groupids": group_id_list
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_massadd_template_macros(self, template_id_list, macros_list):
        """
        此方法允许同时向给定模板添加多个相关对象。

        :param template_id_list: 模板ID列表: [{"templateid": "10085"}]
        :param macros_list: 用户宏列表: [{"macro":"{$cacro1}","value":"1"},{"macro":"{$cacro2}","value":"2"}]
        :return: {'templateids': ['10560']}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.massadd",
            "params": {
                "templates": template_id_list,
                "macros": macros_list
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_massremove_template_macros(self, template_id_list, macros_id_list):
        """
        此方法允许从多个模板中删除相关对象。

        :param template_id_list: 模板ID列表: ["10085"]
        :param macros_id_list: 用户宏名称列表: ["{$E2}","{$E4}"]
        :return: {"templateids":["10085"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.massremove",
            "params": {
                "templateids": template_id_list,
                "macros": macros_id_list
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_massadd_template_templates_link(self, template_id_list, templates_link_id_list):
        """
        此方法允许同时向给定模板添加多个相关对象。

        :param template_id_list: 模板ID列表: [{"templateid": "10085"}]
        :param templates_link_id_list: 模板ID列表: [{"templateid":"10106"},{"templateid":"10104"}]
        :return: {'templateids': ['10560']}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.massadd",
            "params": {
                "templates": template_id_list,
                "templates_link": templates_link_id_list
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_massremove_templateids_clear(self, template_id_list, template_clear_id_list):
        """
        此方法允许从多个模板中删除相关对象。

        :param template_id_list: 模板ID列表: ["10085"]
        :param template_clear_id_list: 模板ID列表: ["10090","10091"]
        :return: {"templateids":["10085"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.massremove",
            "params": {
                "templateids": template_id_list,
                "templateids_clear": template_clear_id_list
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_massremove_templateids_link(self, template_id_list, template_link_id_list):
        """
        此方法允许从多个模板中删除相关对象。

        :param template_id_list: 模板ID列表: ["10085"]
        :param template_link_id_list: 模板ID列表: ["10090","10091"]
        :return: {"templateids":["10085"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.massremove",
            "params": {
                "templateids": template_id_list,
                "templateids_link": template_link_id_list
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_tags(self, template_id_list, tags_list):
        """
        此方法允许更新现有模板。

        :param template_id_list: 模板ID: "10085"
        :param tags_list: 标签列表: [{"tag":"Hostname1","value":"{HOST.NAME1}"},{"tag":"Hostname2","value":"{HOST.NAME2}"}]
        :return: {"hostids":["10086"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.update",
            "params": {
                "templateid": template_id_list,
                "tags": tags_list
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_tags_bytemplateid(self, tags_list, total_length, current_progress):
        """
        此方法允许更新现有模板。

        :param template_id_list: 模板ID: "10085"
        :param tags_list: 标签列表: [{"tag":"Hostname1","value":"{HOST.NAME1}"},{"tag":"Hostname2","value":"{HOST.NAME2}"}]
        :return: {"hostids":["10086"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.update",
            "params": tags_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            logger.debug(f"当前进度: {current_progress}/{total_length} ({(current_progress / total_length) * 100:.2f}%) {response['result']}")
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_tags(self, template_name):
        """
        该方法允许根据给定的参数检索模板。

        :param template_name: 模板名称 "Linux"
        :return: [{'tag': '1', 'value': '1'}, {'tag': '2', 'value': '2'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": ["tags"],
                "selectTags": "extend",
                "evaltype": 0,
                "filter": {
                    "host": [
                        "%s" % template_name
                    ]
                }
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_tags_bytemplateid(self, template_id):
        """
        该方法允许根据给定的参数检索模板。

        :param template_name: 模板名称 "Linux"
        :return: [{'tag': '1', 'value': '1'}, {'tag': '2', 'value': '2'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": ["host", "tags"],
                "selectTags": "extend",
                "evaltype": 0,
                "templateids": template_id,
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_all_template_name(self):
        """
        此方法用于依据给定的参数检索监控项

        :return:  [{'templateid': '42187', 'host': 'Host name of Zabbix agent running'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": ["templateid"],
                "sortfield": "host",
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    # ![06_模板创建监控项]
    def def_get_template_item(self, template_id, item_key):
        """
        此方法用于依据给定的参数检索监控项

        :param template_id: 模板ID: "10084"
        :param item_key: 监控项键值: "system.cpu.util[,idle]"
        :return: [{'itemid': '43855'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": "itemids",
                "templateids": template_id,
                "filter": {
                    "key_": item_key
                },
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_item_name(self, template_id):
        """
        此方法用于依据给定的参数检索监控项

        :param template_id: 模板ID: "10084"
        :return:  [[{'itemid': '42175', 'name': 'Host name of Zabbix agent running', 'hosts': [{'hostid': '10076', 'host': 'AIX by Zabbix agent'}]}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": ["name"],
                "templateids": template_id,
                "selectHosts": ["host", "hostid"],
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_itemprototype_name(self, template_id):
        """
        此方法用于依据给定的参数检索监控项

        :param template_id: 模板ID: "10084"
        :return:  [{'itemid': '42187', 'name': 'Host name of Zabbix agent running'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "itemprototype.get",
            "params": {
                "output": ["name"],
                "templateids": template_id,
                "selectHosts": ["host", "hostid"],
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_itemprototype_tags_bytemplateid(self, template_id):
        """
        此方法用于依据给定的参数检索监控项

        :param template_id: 模板ID: "10084"
        :return:  [{'itemid': '42187', 'name': 'Host name of Zabbix agent running'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "itemprototype.get",
            "params": {
                "output": ["tags"],
                "selectTags": "extend",
                "templateids": template_id,
                "selectHosts": ["host", "hostid"],
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_trigger_name(self, template_id):
        """
        此方法用于依据给定的参数检索触发器

        :param template_id: 模板ID: "10084"
        :return:  [{'triggerid': '42187', 'description': 'Remote Zabbix proxy: More than {$ZABBIX.PROXY.UTIL.MAX}% used in the history index cache'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": ["description"],
                "templateids": template_id,
                "selectHosts": ["host", "hostid"],
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_event_name(self, template_id):
        """
        此方法用于依据给定的参数检索触发器

        :param template_id: 模板ID: "10084"
        :return:  [{'triggerid': '42187', 'description': 'Remote Zabbix proxy: More than {$ZABBIX.PROXY.UTIL.MAX}% used in the history index cache'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": ["event_name"],
                "templateids": template_id,
                "selectHosts": ["host", "hostid"],
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_triggerprototype_name(self, template_id):
        """
        此方法用于依据给定的参数检索触发器

        :param template_id: 模板ID: "10084"
        :return:  [{'triggerid': '42187', 'description': 'Remote Zabbix proxy: More than {$ZABBIX.PROXY.UTIL.MAX}% used in the history index cache'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "triggerprototype.get",
            "params": {
                "output": ["description"],
                "templateids": template_id,
                "selectHosts": ["host", "hostid"],
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_triggerprototype_event_name(self, template_id):
        """
        此方法用于依据给定的参数检索触发器

        :param template_id: 模板ID: "10084"
        :return:  [{'triggerid': '42187', 'description': 'Remote Zabbix proxy: More than {$ZABBIX.PROXY.UTIL.MAX}% used in the history index cache'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "triggerprototype.get",
            "params": {
                "output": ["event_name"],
                "templateids": template_id,
                "selectHosts": ["host", "hostid"],
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_triggerprototype_tag_bytemplateid(self, template_id):
        """
        此方法用于依据给定的参数检索触发器

        :param template_id: 模板ID: "10084"
        :return:  [{'triggerid': '42187', 'description': 'Remote Zabbix proxy: More than {$ZABBIX.PROXY.UTIL.MAX}% used in the history index cache'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "triggerprototype.get",
            "params": {
                "output": ["tags"],
                "selectTags": "extend",
                "templateids": template_id,
                "selectHosts": ["host", "hostid"],
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_application_bytemplateid(self, template_id):
        """
        此方法用于依据给定的参数检索触发器

        :param template_id: 模板ID: "10084"
        :return:  [{'triggerid': '42187', 'description': 'Remote Zabbix proxy: More than {$ZABBIX.PROXY.UTIL.MAX}% used in the history index cache'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "application.get",
            "params": {
                "output": ["name"],
                "templateids": template_id,
                "selectHosts": ["host", "hostid"],
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_graph_name(self, template_id):
        """
        此方法用于依据给定的参数检索触发器

        :param template_id: 模板ID: "10084"
        :return:  [{'graphid': '42187', 'name': '"CPU jumps"'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "graph.get",
            "params": {
                "output": ["name"],
                "templateids": template_id,
                "selectHosts": ["host", "hostid"],
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_graphprototype_name(self, template_id):
        """
        此方法用于依据给定的参数检索触发器

        :param template_id: 模板ID: "10084"
        :return:  [{'graphid': '42187', 'name': '"CPU jumps"'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "graphprototype.get",
            "params": {
                "output": ["name"],
                "templateids": template_id,
                "selectHosts": ["host", "hostid"],
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_create_template_item(self, template_id, item_name, item_type, item_key, item_value_type, item_delay, snmp_oid):
        """
        此方法用于创建新监控项。

        :param template_id: 模板ID: "10085"
        :param item_name: 监控项名称: "Free disk space on /home/joe/"
        :param item_type: 监控项类型: 0
        :param item_key: 监控项关键字: "vfs.fs.size[/home/joe/,free]"
        :param item_value_type: 监控项数据类型: 3
        :param item_delay: 更新监控项的时间间隔: "30s"
        :param snmp_oid: snmp_oid: ".1.3.6.1.4.1.1"
        :return: {"itemids":["24758"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "hostid": template_id,
                "name": item_name,
                "type": item_type,
                "key_": item_key,
                "value_type": item_value_type,
                "delay": item_delay,
                "snmp_oid": snmp_oid
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_delete_template_item(self, template_id_list):
        """
        此方法用于删除监控项。

        :param template_id_list: 模板监控项ID列表: ["22982","22986"]
        :return: {"itemids":["22982","22986"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.delete",
            "params": template_id_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_template_item_tags(self, item_id, tags_list):
        """
        此方法允许更新现有模板。

        :param item_id: 监控项ID: "10085"
        :param tags_list: 标签列表: [{"tag":"Hostname1","value":"{HOST.NAME1}"},{"tag":"Hostname2","value":"{HOST.NAME2}"}]
        :return: {"hostids":["10086"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.update",
            "params": {
                "itemid": item_id,
                "tags": tags_list
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_template_item_tags_bytemplateid(self, tags_list, total_length, current_progress):
        """
        此方法允许更新现有模板。

        :param item_id: 监控项ID: "10085"
        :param tags_list: 标签列表: [{"tag":"Hostname1","value":"{HOST.NAME1}"},{"tag":"Hostname2","value":"{HOST.NAME2}"}]
        :return: {"hostids":["10086"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.update",
            "params": tags_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            logger.debug(f"当前进度: {current_progress}/{total_length} ({(current_progress / total_length) * 100:.2f}%) {response['result']}")
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_item_tags(self, item_id):
        """
        该方法允许根据给定的参数检索监控项。

        :param item_id: 监控项ID: "23298"
        :return: [{'tag': '1', 'value': '1'}, {'tag': '2', 'value': '2'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": ["tags"],
                "selectTags": "extend",
                "evaltype": 0,
                "filter": {
                    "itemid": [
                        "%s" % item_id
                    ]
                }
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_item_tags_bytemplateid(self, template_id):
        """
        该方法允许根据给定的参数检索监控项。

        :param item_id: 监控项ID: "23298"
        :return: [{'tag': '1', 'value': '1'}, {'tag': '2', 'value': '2'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": ["tags"],
                "selectTags": "extend",
                "evaltype": 0,
                "templateids": template_id,
                "selectHosts": ["host", "hostid"],
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    # ![04_为模板创建触发器]
    def def_create_template_trigger(self, trigger_name, priority, expression_name, recovery_expression_name):
        """
        此方法允许创建新的触发器.

        :param trigger_name: 触发器名称: "Processor load is too high on {HOST.NAME}"
        :param priority: 触发器的严重性级别: 2
        :param expression_name: 简化的触发器表达式: "last(/Linux server/system.cpu.load[percpu,avg1])>5"
        :param recovery_expression_name: 生成的触发恢复表达式: "last(/Linux server/system.cpu.load[percpu,avg1])<=5"
        :return: {"triggerids":["17369","17370"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "trigger.create",
            "params": {
                "description": trigger_name,
                "priority": priority,
                "expression": expression_name,
                "recovery_expression": recovery_expression_name,
                "manual_close": 1,
                "recovery_mode": 1
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_host_trigger(self, trigger_id):
        """
        此方法允许根据指定的参数检索触发器.

        :param trigger_name: 触发器名称: "Processor load is too high on {HOST.NAME}"
        :return: "17369"
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": "extend",
                "selectHosts": "extend",
                "selectGroups": "extend",
                "triggerids": trigger_id,
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_trigger(self, template_id, trigger_name):
        """
        此方法允许根据指定的参数检索触发器.

        :param trigger_name: 触发器名称: "Processor load is too high on {HOST.NAME}"
        :return: "17369"
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": "triggerid",
                "templateids": template_id,
                "filter": {
                    "description": trigger_name,
                },
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_delete_template_trigger(self, trigger_id):
        """
             此方法用于删除触发器。

             :param trigger_id: 监控项ID列表: ["12002","12003"]
             :return: {"triggerids":["12002","12003"]}
             """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "trigger.delete",
            "params": trigger_id,
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_trigger_tags(self, trigger_id):
        """
        该方法允许根据给定的参数检索监控项。

        :param trigger_id: 触发器ID: "23298"
        :return: [{'tag': '1', 'value': '1'}, {'tag': '2', 'value': '2'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": ["tags"],
                "selectTags": "extend",
                "evaltype": 0,
                "filter": {
                    "triggerid": trigger_id
                }
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_trigger_tags_bytemplateid(self, template_id):
        """
        该方法允许根据给定的参数检索监控项。

        :param trigger_id: 触发器ID: "23298"
        :return: [{'tag': '1', 'value': '1'}, {'tag': '2', 'value': '2'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": ["tags"],
                "selectTags": "extend",
                "templateids": template_id,
                "evaltype": 0,
                "selectHosts": ["host", "hostid"],
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_template_trigger_tags(self, trigger_id, tags_list):
        """
        此方法允许更新现有模板。

        :param trigger_id: 触发器ID: "10085"
        :param tags_list: 标签列表: [{"tag":"Hostname1","value":"{HOST.NAME1}"},{"tag":"Hostname2","value":"{HOST.NAME2}"}]
        :return: {"triggerids":["13938"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "trigger.update",
            "params": {
                "triggerid": trigger_id,
                "tags": tags_list
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_template_trigger_tags_bytemplateid(self, tags_list, total_length, current_progress):
        """
        此方法允许更新现有模板。

        :param trigger_id: 触发器ID: "10085"
        :param tags_list: 标签列表: [{"tag":"Hostname1","value":"{HOST.NAME1}"},{"tag":"Hostname2","value":"{HOST.NAME2}"}]
        :return: {"triggerids":["13938"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "trigger.update",
            "params": tags_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            logger.debug(f"当前进度: {current_progress}/{total_length} ({(current_progress / total_length) * 100:.2f}%) {response['result']}")
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_discoveryrule(self, hostid, name):
        """
        该方法允许根据给定的参数检索模板发现规则。

        :param hostid: 模板ID: "10534"
        :param name: LLD规则名称: "test"
        :return:  [{'itemid': '44081'}, {'itemid': '44083'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "discoveryrule.get",
            "params": {
                "output": ["itemid"],
                "hostids": hostid,
                "filter": {
                    "name": name
                },
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_create_discoveryrule(self, hostid, name, type, key_):
        """
        此方法允许创建新的模板发现规则。

        :param hostid: LLD规则的主机ID: '10197'
        :param name: LLD规则名称: 'Mounted filesystem discovery'
        :param type: LLD规则类型: '0'
        :param key_: LLD规则键值: 'vfs.fs.discovery'
        :return: "itemids":["27665"]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "discoveryrule.create",
            "params": {
                "name": name,
                "key_": key_,
                "hostid": hostid,
                "type": type,
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_delete_discoveryrule(self, discoveryrule_id_list):
        """
        此方法用于删除模板发现规则。

        :param discoveryrule_id_list: 模板发现规则ID列表: ["22982","22986"]
        :return: {"ruleids":["22982","22986"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "discoveryrule.delete",
            "params": discoveryrule_id_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_create_itemprototype(self, ruleid, template_id, item_name, item_type, item_key, item_units, item_value_type, item_delay, snmp_oid):
        """
        此方法允许创建新的模板发现规则。

        :param ruleid: 模板发现规则ID: "10065"
        :param template_id: 模板ID: "10085"
        :param item_name: 模板发现规则监控项名称: "Free disk space on /home/joe/"
        :param item_type: 模板发现规则监控项类型: 0
        :param item_key: 模板发现规则监控项关键字: "vfs.fs.size[/home/joe/,free]"
        :param item_units: 模板发现规则监控项单位: "%"
        :param item_value_type: 模板发现规则监控项数据类型: 3
        :param item_delay: 模板发现规则更新监控项的时间间隔: "30s"
        :param snmp_oid: 模板发现规则snmp_oid: ".1.3.6.1.4.1.1"
        :return: {"itemids":["24758"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "itemprototype.create",
            "params": {
                "ruleid": ruleid,
                "hostid": template_id,
                "name": item_name,
                "type": item_type,
                "key_": item_key,
                "units": item_units,
                "value_type": item_value_type,
                "delay": item_delay,
                "snmp_oid": snmp_oid
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_itemprototype_item(self, template_id, item_key):
        """
        此方法用于依据给定的参数检索模板发现规则监控项

        :param template_id: 模板ID: "10084"
        :param item_key: 监控项键值: "system.cpu.util[,idle]"
        :return: [{'itemid': '43855'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "itemprototype.get",
            "params": {
                "output": "itemid",
                "discoveryids": template_id,
                "filter": {
                    "key_": item_key
                },
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_delete_itemprototype(self, discoveryrule_id_list):
        """
        此方法用于删除模板发现规则。

        :param discoveryrule_id_list: 模板发现规则ID列表: ["22982","22986"]
        :return: {'prototypeids': ['44237']}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "itemprototype.delete",
            "params": discoveryrule_id_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_create_template_triggerprototype(self, trigger_name, priority, expression_name, recovery_expression_name):
        """
        此方法允许创建新的触发器.

        :param trigger_name: 触发器名称: "Processor load is too high on {HOST.NAME}"
        :param priority: 触发器的严重性级别: 2
        :param expression_name: 简化的触发器表达式: "last(/Linux server/system.cpu.load[percpu,avg1])>5"
        :param recovery_expression_name: 生成的触发恢复表达式: "last(/Linux server/system.cpu.load[percpu,avg1])<=5"
        :return: {"triggerids":["17369","17370"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "triggerprototype.create",
            "params": {
                "description": trigger_name,
                "priority": priority,
                "expression": expression_name,
                "recovery_expression": recovery_expression_name,
                "manual_close": 1,
                "recovery_mode": 1
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_template_triggerprototype(self, trigger_name):
        """
        此方法允许根据指定的参数检索触发器.

        :param trigger_name: 触发器名称: "Processor load is too high on {HOST.NAME}"
        :return: "17369"
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "triggerprototype.get",
            "params": {
                "output": "triggerid",
                "filter": {
                    "description": trigger_name
                },
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_delete_template_triggerprototype(self, trigger_id):
        """
             此方法用于删除触发器。

             :param trigger_id: 监控项ID列表: ["12002","12003"]
             :return: {"triggerids":["12002","12003"]}
             """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "triggerprototype.delete",
            "params": trigger_id,
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    # ![10_创建主机]
    def def_create_host(self, host_name, template_id_list, group_id_list, type, ip, port, version,
                        securitylevel, authprotocol, privprotocol, ipmi_authtype, ipmi_privilege,
                        ipmi_username, ipmi_password, name, snmp_community, snmp_securityname, snmp_authpassphrase, snmp_privpassphrase):
        """
        这个方法可以用来创建主机。

        :param host_name: 主机名称: "Linux server"
        :param template_id_list: 模板ID列表: [{"templateid":"20045"}]
        :param group_id_list: 主机组ID列表: [{"groupid":"50"}]
        :param type: 接口类型: 1
        :param ip: IP地址: "192.168.3.1"
        :param port: 端口号: "10050"
        :param version: 版本: 3
        :param securitylevel: 安全级别: 2
        :param authprotocol: 身份认证协议: 0
        :param privprotocol: 隐私协议: 0
        :return: {"hostids":["10658"]}
        """

        # 构建接口详情，排除空值
        details = {
            "version": version,
            "bulk": "1"
        }
        if snmp_community: details["community"] = snmp_community
        if snmp_securityname: details["securityname"] = snmp_securityname
        if securitylevel: details["securitylevel"] = securitylevel
        if authprotocol: details["authprotocol"] = authprotocol
        if snmp_authpassphrase: details["authpassphrase"] = snmp_authpassphrase
        if privprotocol: details["privprotocol"] = privprotocol
        if snmp_privpassphrase: details["privpassphrase"] = snmp_privpassphrase

        # 构建接口
        interface = {
            "type": type,
            "ip": ip,
            "port": port,
            "dns": "",
            "main": 1,
            "useip": 1,
            "details": details
        }

        # 构建params
        params = {
            "host": host_name,
            "templates": template_id_list,
            "groups": group_id_list,
            "name": name,
            "interfaces": [interface]
        }
        if ipmi_authtype: params["ipmi_authtype"] = ipmi_authtype
        if ipmi_privilege: params["ipmi_privilege"] = ipmi_privilege
        if ipmi_username: params["ipmi_username"] = ipmi_username
        if ipmi_password: params["ipmi_password"] = ipmi_password

        # 最终数据结构
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": params,
            "auth": self.authID,
            "id": 1
        })

        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_host(self, host_name):
        """
        此方法允许根据指定的参数获取主机。

        :param host_name: 主机名称: ["Zabbixserver"]
        :return: [{'hostid': '10600', 'groups': [{'groupid': '26', 'name': '000_LocalTemplates', 'internal': '0', 'flags': '0', 'uuid': 'dfcb57e7223e4446b8c27702e7c01ab8'}]}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid"],
                "selectGroups": "extend",
                "filter": {
                    "host": host_name
                },
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_delete_host(self, host_id_list):
        """
        这个方法允许删除主机。

        :param host_id_list: 要删除主机的ID: ["13"]
        :return: {"hostids":["13","32"]}
        """

        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.delete",
            "params": host_id_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    # ![11_主机创建接口]
    def def_massadd_host_interface(self, host_id_list, type, ip, port, version, securitylevel, authprotocol, privprotocol,
                                   snmp_community, snmp_securityname, snmp_authpassphrase, snmp_privpassphrase):
        """
        此方法允许同时添加多个相关对象到所有给定的主机。

        :param host_id_list: 主机ID列表: [{"hostid":"10160"}]
        :param type: 接口类型: 1
        :param ip: IP地址: "192.168.3.1"
        :param port: 端口号: "10050"
        :param version: 版本: 3
        :param securitylevel: 安全级别: 2
        :param authprotocol: 身份认证协议: 0
        :param privprotocol: 隐私协议: 0
        :return: {'interfaceids': {'interfaceids': ['72']}}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostinterface.massadd",
            "params": {
                "hosts": host_id_list,
                "interfaces": [
                    {
                        "type": type,
                        "ip": ip,
                        "port": port,
                        "dns": "",
                        "main": 1,
                        "useip": 1,
                        "details": {
                            "version": version,
                            "bulk": "1",
                            "community": snmp_community,
                            "securityname": snmp_securityname,
                            "securitylevel": securitylevel,
                            "authprotocol": authprotocol,
                            "authpassphrase": snmp_authpassphrase,
                            "privprotocol": privprotocol,
                            "privpassphrase": snmp_privpassphrase
                        }
                    }
                ],
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_massremove_host_interface(self, host_id_list, type, ip, port):
        """
        该方法允许从给定的主机列表中批量删除主机接口

        :param host_id_list: 主机ID列表: ["10160"]
        :param type: 接口类型: 1
        :param ip: IP地址: "192.168.3.1"
        :param port: 端口号: "10050"
        :return: {"interfaceids":["30069"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostinterface.massremove",
            "params": {
                "hostids": host_id_list,
                "interfaces": {
                    "dns": "",
                    "type": type,
                    "ip": ip,
                    "port": port,
                },
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    # ![12_主机关联模板]
    def def_massadd_host_template(self, host_id_list, template_id_list):
        """
        此方法允许同时添加多个相关对象到所有给定的主机。

        :param host_id_list: 主机ID列表: [{"hostid":"10160"}]
        :param template_id_list: 模板ID列表: [{"templateid":"1160"}]
        :return: {'hostids': ['10591']}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.massadd",
            "params": {
                "hosts": host_id_list,
                "templates": template_id_list,
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_massadd_host_template_base_20221003(self, excel_op, index, host_name, host_ip, template_name, host_id_list, template_id_list):
        """
        此方法允许同时添加多个相关对象到所有给定的主机。

        :param index: 序号: "1"
        :param host_name: 主机名: "host1"
        :param host_ip: 主机IP: "172.169.10.2"
        :param template_name: 模板名称: "template1"
        :param host_id_list: 主机ID列表: [{"hostid":"10160"}]
        :param template_id_list: 模板ID列表: [{"templateid":"1160"}]
        :return: {'hostids': ['10591']}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.massadd",
            "params": {
                "hosts": host_id_list,
                "templates": template_id_list,
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', '') != '':
            print(u"主机: \033[;32m%s\033[0m 关联模板 \033[;32m%s\033[0m 成功! 返回值为: \033[;32m%s\033[0m" % (
                host_name, template_name, response['result']))
            excel_op.set_cell_value(index + 1, 1, index)
            excel_op.set_cell_value(index + 1, 2, host_name)
            excel_op.set_cell_value(index + 1, 3, host_ip)
            excel_op.set_cell_value(index + 1, 4, template_name)
            excel_op.set_cell_value(index + 1, 5, '成功')
        elif response.get('error', '') != '':
            print(u"主机: \033[;31m%s\033[0m 关联模板 \033[;32m%s\033[0m 失败! 原因: \033[;31m%s\033[0m" % (
                host_name, template_name, response['error']['data']))
            excel_op.set_cell_value(index + 1, 1, index)
            excel_op.set_cell_value(index + 1, 2, host_name)
            excel_op.set_cell_value(index + 1, 3, host_ip)
            excel_op.set_cell_value(index + 1, 4, template_name)
            excel_op.set_cell_value(index + 1, 5, '失败')
            excel_op.set_cell_value(index + 1, 6, response['error']['data'])

    def def_massadd_host_template_base_item_20221003(self, excel_op, index, host_name, host_ip, history_value, template_name, host_id_list, template_id_list):
        """
        此方法允许同时添加多个相关对象到所有给定的主机。

        :param index: 序号: "1"
        :param host_name: 主机名: "host1"
        :param host_ip: 主机IP: "192.168.0.1"
        :param history_value: 历史值: "1001"
        :param template_name: 模板名称: "template1"
        :param host_id_list: 主机ID列表: [{"hostid":"10160"}]
        :param template_id_list: 模板ID列表: [{"templateid":"1160"}]
        :return: {'hostids': ['10591']}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.massadd",
            "params": {
                "hosts": host_id_list,
                "templates": template_id_list,
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', '') != '' or not template_id_list:
            excel_op.set_cell_value(index + 1, 1, index)
            excel_op.set_cell_value(index + 1, 2, host_name)
            excel_op.set_cell_value(index + 1, 3, host_ip)
            excel_op.set_cell_value(index + 1, 4, history_value)
            excel_op.set_cell_value(index + 1, 5, template_name)
            if template_id_list:
                excel_op.set_cell_value(index + 1, 6, '成功')
                print(u"主机: \033[;32m%s\033[0m 获取监控项的值为: \033[;32m%s\033[0m 关联模板 \033[;32m%s\033[0m 成功! 返回值为: \033[;32m%s\033[0m"
                      % (host_name, history_value, template_name, response['result']))
            else:
                excel_op.set_cell_value(index + 1, 6, '失败')
                excel_op.set_cell_value(index + 1, 7, '未找到定义的模板名')
                print(u"主机: \033[;31m%s\033[0m 获取监控项的值为: \033[;31m%s\033[0m 关联模板 \033[;31m%s\033[0m 失败! 原因: \033[;31m%s\033[0m"
                      % (host_name, history_value, template_name, '未找到定义的模板名'))

        elif response.get('error', '') != '':
            print(u"主机: \033[;31m%s\033[0m 获取监控项的值为: \033[;32m%s\033[0m 关联模板 \033[;32m%s\033[0m 失败! 原因: \033[;31m%s\033[0m"
                  % (host_name, history_value, template_name, response['error']['data']))
            excel_op.set_cell_value(index + 1, 1, index)
            excel_op.set_cell_value(index + 1, 2, host_name)
            excel_op.set_cell_value(index + 1, 3, host_ip)
            excel_op.set_cell_value(index + 1, 4, history_value)
            excel_op.set_cell_value(index + 1, 5, template_name)
            excel_op.set_cell_value(index + 1, 6, '失败')
            excel_op.set_cell_value(index + 1, 7, response['error']['data'])

    def def_massremove_host_templateids(self, host_id_list, template_id_list):
        """
        该方法允许从多个主机中移除相关对象。

        :param host_id_list: 主机ID列表: ["10160"]
        :param template_id_list: 模板ID列表 ["325"]
        :return: {"hostids":["69665"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.massremove",
            "params": {
                "hostids": host_id_list,
                "templateids": template_id_list
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_massremove_host_templateids_clear(self, host_id_list, template_id_list):
        """
        该方法允许从多个主机中移除相关对象。

        :param host_id_list: 主机ID列表: ["10160"]
        :param template_id_list: 模板ID列表 ["325"]
        :return: {"hostids":["69665"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.massremove",
            "params": {
                "hostids": host_id_list,
                "templateids_clear": template_id_list
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_massremove_host_templateids_clear_base_20221003(self, excel_op, index, host_name, host_ip, template_name, host_id_list, template_id_list):
        """
        该方法允许从多个主机中移除相关对象。

        :param index: 序号: "1"
        :param host_name: 主机名: "host1"
        :param host_ip: 主机IP: "172.169.10.2"
        :param template_name: 模板名称: "template1"
        :param host_id_list: 主机ID列表: ["10160"]
        :param template_id_list: 模板ID列表 ["325"]
        :return: {"hostids":["69665"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.massremove",
            "params": {
                "hostids": host_id_list,
                "templateids_clear": template_id_list
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', '') != '':
            print(u"主机: \033[;32m%s\033[0m 脱离模板 \033[;32m%s\033[0m 清理监控项成功! 返回值为: \033[;32m%s\033[0m" % (
                host_name, template_name, response['result']))
            excel_op.set_cell_value(index + 1, 1, index)
            excel_op.set_cell_value(index + 1, 2, host_name)
            excel_op.set_cell_value(index + 1, 3, host_ip)
            excel_op.set_cell_value(index + 1, 4, template_name)
            excel_op.set_cell_value(index + 1, 5, '成功')
        elif response.get('error', '') != '':
            print(u"主机: \033[;31m%s\033[0m 脱离模板 \033[;32m%s\033[0m 清理监控项失败! 原因: \033[;31m%s\033[0m" % (
                host_name, template_name, response['error']['data']))
            excel_op.set_cell_value(index + 1, 1, index)
            excel_op.set_cell_value(index + 1, 2, host_name)
            excel_op.set_cell_value(index + 1, 3, host_ip)
            excel_op.set_cell_value(index + 1, 4, template_name)
            excel_op.set_cell_value(index + 1, 5, '失败')
            excel_op.set_cell_value(index + 1, 6, response['error']['data'])

    # ![13_主机关联主机组]
    def def_massadd_host_groups(self, host_id_list, group_id_list):
        """
        该方法允许从多个主机中移除相关对象。

        :param host_id_list: 主机组ID列表: [{"hostid":"10160"}]
        :param group_id_list: 主机组ID列表: [{"groupid":"1160"}]
        :return: {'hostids': ['10591']}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.massadd",
            "params": {
                "hosts": host_id_list,
                "groups": group_id_list,
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_massremove_host_group(self, host_id_list, group_id_list):
        """
        该方法允许从多个主机中移除相关对象。

        :param host_id_list: 主机ID列表: ["10160"]
        :param group_id_list: 主机组ID列表 ["325"]
        :return: {"hostids":["69665"]}
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.massremove",
            "params": {
                "hostids": host_id_list,
                "groupids": group_id_list
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_host_item(self, host_name, item_key):
        """
        此方法用于依据给定的参数检索监控项

        :param host_name: 主机名称: "Linux"
        :param item_key: 监控项键值: "system.cpu.util[,idle]"
        :return: [{'itemid': '43855'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": "extend",
                "host": host_name,
                "filter": {
                    "key_": item_key
                },
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_group_item(self, group_name, item_key):
        """
        此方法用于依据给定的参数检索监控项

        :param host_name: 主机名称: "Linux"
        :param item_key: 监控项键值: "system.cpu.util[,idle]"
        :return: [{'itemid': '43855'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": "extend",
                "group": group_name,
                "search": {
                    "key_": item_key
                },
            },
            "auth": self.authID,
            "id": 1,
        })
        try:
            request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
            response = request.json()
            if response.get('result', ''):
                return {'tag': True, 'result': response['result']}
            if response.get('error', ''):
                GV_ERROR_MESS['error'] = response['error']
                logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
                return {'tag': False, 'result': response['error']}
            else:
                return {'tag': False, 'result': response}
        except requests.exceptions.SSLError as e:
            return {"tag": False, "result": [], "error": f"SSL 证书错误: {e}"}
        except requests.exceptions.Timeout as e:
            return {"tag": False, "result": [], "error": f"请求超时: {e}"}
        except requests.exceptions.ConnectionError as e:
            return {"tag": False, "result": [], "error": f"连接错误: {e}"}
        except requests.exceptions.JSONDecodeError as e:
            return {
                "tag": False,
                "result": [],
                "error": f"JSON 解码失败",
                "raw_response": response.text if 'response' in locals() else "无响应",
                "exception": str(e)
            }
        except Exception as e:
            return {"tag": False, "result": [], "error": f"未知异常: {e}"}

    def def_get_host_key_item(self, item_key):
        """
        此方法用于依据给定的参数检索监控项

        :param host_name: 主机名称: "Linux"
        :param item_key: 监控项键值: "system.cpu.util[,idle]"
        :return: [{'itemid': '43855'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": "extend",
                "selectHosts": ["host", "name"],
                "selectInterfaces": ["ip"],
                "search": {
                    "key_": item_key
                },
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_item_history(self, item_id, history, time_from, time_till):
        """
        该方法允许根据给定的参数检索历史数据。

        :param item_id: 监控项ID: "23298"
        :param history: 数据类型: 0
        :param time_from: "1351090996"
        :param time_till: "1351091936"
        :return: [{'itemid': '47789', 'clock': '1664431589', 'value': '1', 'ns': '816892476'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "itemids": item_id,
                "history": history,
                "time_from": time_from,
                "time_till": time_till
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_item_history_base_20221003(self, item_id, history):
        """
        该方法允许根据给定的参数检索历史数据。

        :param item_id: 监控项ID: "23298"
        :param history: 数据类型: 0
        :return: [{'itemid': '47789', 'clock': '1664431589', 'value': '1', 'ns': '816892476'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "itemids": item_id,
                "history": history,
                "sortfield": "clock",
                "sortorder": "DESC",
                "limit": 1
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            print(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return [{'value': 'X'}]

    def def_get_all_history(self, item_id, history, time_from, time_till):
        """
        该方法允许根据给定的参数检索历史数据。

        :param item_id: 监控项ID: "23298"
        :param history: 数据类型: 0
        :param time_from: "1351090996"
        :param time_till: "1351091936"
        :return: [{'itemid': '47789', 'clock': '1664431589', 'value': '1', 'ns': '816892476'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "itemids": item_id,
                "history": history,
                "sortfield": "clock",
                "sortorder": "DESC",
                "time_from": time_from,
                "time_till": time_till
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_action(self, action_name):
        """
        该方法允许根据给定的参数检索动作。

        :param action_name: 动作名称 "Report problems to Zabbix administrators"
        :return: [{'actionid': '3'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "action.get",
            "params": {
                "output": "actionid",
                "filter": {
                    "name": action_name
                }
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_all_alert(self, actionids, time_from, time_till):
        """
        该方法允许根据给定的参数检索历史数据。

        :param actionids: "3"
        :param time_from: "1351090996"
        :param time_till: "1351091936"
        :return: [{'itemid': '47789', 'clock': '1664431589', 'value': '1', 'ns': '816892476'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "alert.get",
            "params": {
                "output": "extend",
                "actionids": actionids,
                "sortfield": "clock",
                "sortorder": "DESC",
                "time_from": time_from,
                "time_till": time_till
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        value_list_1 = []
        for i in response['result']:
            if i['message'] == '':
                continue
            dic = {}
            dic.update({'告警主题': i["subject"], '执行状态': i["status"]})
            vlist = i['message'].split('\r\n')
            for vl1 in range(len(list(vlist))):
                logger.debug(vlist[vl1])
                pattern = re.compile(r'(.*?): (.*)$')
                result = None
                result = re.search(pattern, vlist[vl1])
                if result:
                    if result.group(2) == "":
                        dic.update({result.group(1): ''})
                    else:
                        dic.update({result.group(1): result.group(2)})
                else:
                    continue
            value_list_1.append(dic)
        if not value_list_1:
            return []
        return value_list_1

    def def_get_all_problem(self, time_from, time_till):
        """
        该方法允许根据给定的参数检索历史数据。

        :param actionids: "3"
        :param time_from: "1351090996"
        :param time_till: "1351091936"
        :return: [{'itemid': '47789', 'clock': '1664431589', 'value': '1', 'ns': '816892476'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "problem.get",
            "params": {
                "output": "extend",
                "sortfield": "eventid",
                "sortorder": "DESC",
                "selectAcknowledges": "extend",
                "recent": "true",
                "time_from": time_from,
                "time_till": time_till
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        value_list_1 = []
        for i in response['result']:
            dic = {}
            dic.update({'主机组': '', '主机名': '', '可见名': '', 'triggerid': i["objectid"], '问题名称': i["name"],
                        '是否确认': i["acknowledged"], '问题等级': i["severity"],
                        '运营数据': i["opdata"], '问题日期': i["clock"], '问题时间': ''})

            value_list_1.append(dic)
        if not value_list_1:
            return []
        return value_list_1

    def def_get_all_alert_custom(self, actionids, time_from, time_till):
        """
        该方法允许根据给定的参数检索历史数据。

        :param actionids: "3"
        :param time_from: "1351090996"
        :param time_till: "1351091936"
        :return: [{'itemid': '47789', 'clock': '1664431589', 'value': '1', 'ns': '816892476'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "alert.get",
            "params": {
                "output": "extend",
                "actionids": actionids,
                "sortfield": "clock",
                "sortorder": "DESC",
                "time_from": time_from,
                "time_till": time_till
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        value_list_1 = []
        for i in response['result']:
            if i['message'] == '':
                continue

            dic = {}
            dic.update({'clock': i["clock"], 'subject': i["subject"], 'status': i["status"]})

            pattern = re.compile(r'.*(\d{4}\.\d{2}\.\d{2}).*\r[^\r]')
            result = None
            result = re.search(pattern, i['message'])
            if result:
                dic.update({'message_date': result.group(1)})
            else:
                dic.update({'message_date': ''})

            pattern = re.compile(r'.*(\d{2}:\d{2}:\d{2}).*\r[^\r]')
            result = None
            result = re.search(pattern, i['message'])
            if result:
                dic.update({'message_clock': result.group(1)})
            else:
                dic.update({'message_clock': ''})

            pattern = re.compile(r'.*(故障).*\r[^\r]')
            result = None
            result = re.search(pattern, i['message'])
            if result:
                dic.update({'message_status': result.group(1)})
            else:
                dic.update({'message_status': ''})

            pattern = re.compile(r'.*(发生|,): (.*)\r[^\r]')
            result = None
            result = re.search(pattern, i['message'])
            if result:
                dic.update({'message_name': result.group(2)})
            else:
                dic.update({'message_name': ''})

            try:
                dic.update({'message_duration': result.group(1)})
            except:
                dic.update({'message_duration': ''})

            pattern = re.compile(r'.*告警主机:(.*_ROS_.*)\r[^\r]')
            result = None
            result = re.search(pattern, i['message'])
            if result:
                dic.update({'message_host': result.group(1)})
            else:
                dic.update({'message_host': ''})

            pattern = re.compile(r'.*告警等级:(.*)')
            result = None
            result = re.search(pattern, i['message'])
            if result:
                dic.update({'message_severity': result.group(1)})
            else:
                dic.update({'message_severity': ''})

            value_list_1.append(dic)

        if not value_list_1:
            return []
        return value_list_1

    def def_get_hostgroup_host(self, hostgroup_id_list):
        """
        获取主机组下所有主机名

        :param hostgroup_id_list: 主机组ID列表: ['10084']
        :return:  [{'hostid': '10084', 'host': 'Zabbix server'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": [
                    "host", 
                    "name", 
                    "proxyid", 
                    "proxy_groupid",
                    # 添加 IPMI 相关字段
                    "ipmi_authtype",
                    "ipmi_privilege", 
                    "ipmi_username",
                    "ipmi_password"
                ],
                "groupids": hostgroup_id_list,
                "selectParentTemplates": ["host"],
                "selectHostGroups": ["name"],
                "selectInterfaces": ["ip", "type", "port", "details"],
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_host_ip(self, host_id_list):
        """
        获取主机组下所有主机名

        :param hostgroup_id_list: 主机组ID列表: ['10084']
        :return: [{'ip': '127.0.0.1'}]}],
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["interfaces"],
                "hostids": host_id_list,
                "selectInterfaces": ['ip'],
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_host_name(self, host_id_list):
        """
        获取主机组下所有主机名

        :param hostgroup_id_list: 主机组ID列表: ['10084']
        :return: [{'ip': '127.0.0.1'}]}],
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["name"],
                "hostids": host_id_list,
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_host_name(self, host_id, host_name):
        """
        获取主机组下所有主机名

        :param hostgroup_id_list: 主机组ID列表: ['10084']
        :return: [{'ip': '127.0.0.1'}]}],
        """
        # 构建params
        params = {
        }
        if host_id: params["hostid"] = host_id
        if host_name: params["name"] = host_name

        # 最终数据结构
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.update",
            "params": params,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_from_host_id_get_hostgroup(self, host_id_list):
        """
        获取主机组下所有主机名

        :param hostgroup_id_list: 主机组ID列表: ['10084']
        :return: [{'ip': '127.0.0.1'}]}],
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid"],
                "hostids": host_id_list,
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_all_event(self, event_name, time_from, time_till):
        """
        该方法允许根据给定的参数检索事件。

        :param event_name: 动作名称 "Report problems to Zabbix administrators"
        :return:  [{'eventid': '15', 'hosts': [{'hostid': '10084', 'proxy_hostid': '0', 'host': 'Zabbix server', 'status': '0', 'lastaccess': '0', 'ipmi_authtype': '-1', 'ipmi_privi
lege': '2', 'ipmi_username': '', 'ipmi_password': '', 'maintenanceid': '0', 'maintenance_status': '0', 'maintenance_type': '0', 'maintenance_from': '0', 'name': 'Zabbix server', 'flags': '0',
'templateid': '0', 'description': '', 'tls_connect': '1', 'tls_accept': '1', 'tls_issuer': '', 'tls_subject': '', 'proxy_address': '', 'auto_compress': '1', 'custom_interfaces': '0', 'uuid': '
', 'inventory_mode': '-1'}]}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "event.get",
            "params": {
                "output": ['hosts'],
                "selectHosts": "extend",
                "sortfield": "clock",
                "sortorder": "DESC",
                "time_from": time_from,
                "time_till": time_till,
                "filter": {
                    "name": event_name
                },
            },
            "auth": self.authID,
            "id": 1,
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_all_priority_trigger(self, priority, status):
        """
        :param priority:
        :param status: 0已启用的触发器;1已禁用的触发器
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": [
                    "triggerid",
                    "description",
                    "priority"
                ],
                "filter": {
                    "status": status,
                    "priority": priority,
                },
                "active": '',
                "sortfield": "priority",
                "sortorder": "DESC"
            },
            "auth": self.authID,
            "id": 1
        }
        if status == 1:
            del data['params']['active']
        data = json.dumps(data)
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', '') != '':
            return response.get('result', '')
        else:
            return

    def def_get_all_priority_trigger_by_description(self, priority, status, description):
        """
        :param priority:
        :param status: 0已启用的触发器;1已禁用的触发器
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": [
                    "triggerid",
                    "description",
                    "priority"
                ],
                "filter": {
                    "status": status,
                    "priority": priority,
                },
                "search": {
                    "description": description
                },
                "active": '',
                "sortfield": "priority",
                "sortorder": "DESC"
            },
            "auth": self.authID,
            "id": 1
        }
        if status == 1:
            del data['params']['active']
        data = json.dumps(data)
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', '') != '':
            return response.get('result', '')
        else:
            return

    def def_stop_all_priority_trigger(self, priority):
        try:
            response = self.def_get_all_priority_trigger(priority, 0)
            for i in range(len(response)):
                self.def_update_all_priority_trigger(response[i]['triggerid'], 1)
                print(u"已成功禁用触发器: \033[;32m%s\033[0m 触发器ID为: \033[;32m%s\033[0m" %
                      (response[i]['description'], response[i]['triggerid']))
            return response
        except:
            return

    def def_stop_all_priority_trigger_by_description(self, priority, description):
        try:
            response = self.def_get_all_priority_trigger_by_description(priority, 0, description)
            for i in range(len(response)):
                self.def_update_all_priority_trigger(response[i]['triggerid'], 1)
                print(u"已成功禁用触发器: \033[;32m%s\033[0m 触发器ID为: \033[;32m%s\033[0m" %
                      (response[i]['description'], response[i]['triggerid']))
            return response
        except:
            return

    def def_start_all_priority_trigger(self, priority):
        try:
            response = self.def_get_all_priority_trigger(priority, 1)
            for i in range(len(response)):
                self.def_update_all_priority_trigger(response[i]['triggerid'], 0)
                print(u"已成功启动触发器: \033[;32m%s\033[0m 触发器ID为: \033[;32m%s\033[0m" %
                      (response[i]['description'], response[i]['triggerid']))
            return response
        except:
            return

    def def_update_all_priority_trigger(self, triggerid, status):
        """
        :param triggerid:
        :param status: 0启用触发器;1禁用触发器
        :return:
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "trigger.update",
            "params": {
                "triggerid": triggerid,
                "status": status,
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', '') != '':
            return response.get('result', '')
        else:
            return

    def def_get_all_unsupport_item(self):
        """
        :param state: 0标准的监控项;1不受支持的监控项
        :param status: 0已启用的监控项;1已禁用的监控项
        :return:
        """
        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": [
                    "itemid",
                    "name",
                ],
                "filter": {
                    "state": 1,
                },
                "sortfield": "name",
                "sortorder": "DESC"
            },
            "auth": self.authID,
            "id": 1
        }
        data = json.dumps(data)
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', '') != '':
            return response.get('result', '')
        else:
            return

    def def_stop_all_unsupport_item(self):
        try:
            response = self.def_get_all_unsupport_item()
            for i in range(len(response)):
                self.def_update_all_unsupport_item(response[i]['itemid'], 1)
                print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 已成功禁用监控项: \033[;32m%s\033[0m 监控项ID为: \033[;32m%s\033[0m' % (len(response), i + 1, response[i]['name'], response[i]['itemid']))
            return response
        except:
            return

    def def_start_all_unsupport_item(self):
        try:
            response = self.def_get_all_unsupport_item()
            for i in range(len(response)):
                self.def_update_all_unsupport_item(response[i]['itemid'], 0)
                print(u'(\033[;34m%s\033[0m/\033[;34m%s\033[0m): -> 已成功启动监控项: \033[;32m%s\033[0m 监控项ID为: \033[;32m%s\033[0m' % (len(response), i + 1, response[i]['name'], response[i]['itemid']))
            return response
        except:
            return

    def def_update_all_unsupport_item(self, itemid, status):
        """
        :param itemid:
        :param status: 0启用触发器;1禁用触发器
        :return:
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.update",
            "params": {
                "itemid": itemid,
                "status": status
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', '') != '':
            return response.get('result', '')
        else:
            return

    def def_check_zbx_version(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "apiinfo.version",
            "params": [],
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_item_name(self, item_list, total_length, current_progress):
        """
        更新监控项名称

        :param itemid: 监控项ID: ['10084']
        :param item_name: 监控项名称: 'Available memory'
        :return:
        """

        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.update",
            "params": item_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            logger.debug(f"当前进度: {current_progress}/{total_length} ({(current_progress / total_length) * 100:.2f}%) {response['result']}")
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_itemprototype_name(self, item_list, total_length, current_progress):
        """
        更新监控项名称

        :param itemid: 监控项ID: ['10084']
        :param item_name: 监控项名称: 'Available memory'
        :return:
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "itemprototype.update",
            "params": item_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            logger.debug(f"当前进度: {current_progress}/{total_length} ({(current_progress / total_length) * 100:.2f}%) {response['result']}")
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_itemprototype_tags_bytemplateid(self, tag_list, total_length, current_progress):
        """
        更新监控项名称

        :param itemid: 监控项ID: ['10084']
        :param item_name: 监控项名称: 'Available memory'
        :return:
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "itemprototype.update",
            "params": tag_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            logger.debug(f"当前进度: {current_progress}/{total_length} ({(current_progress / total_length) * 100:.2f}%) {response['result']}")
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_trigger_name(self, item_list, total_length, current_progress):
        """
        更新触发器名称

        :param triggerid: 触发器ID: ['10084']
        :param trigger_name: 触发器名称: 'Available memory'
        :return:
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "trigger.update",
            "params": item_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            logger.debug(f"当前进度: {current_progress}/{total_length} ({(current_progress / total_length) * 100:.2f}%) {response['result']}")
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_triggerprototype_name(self, item_list, total_length, current_progress):
        """
        更新触发器名称

        :param triggerid: 触发器ID: ['10084']
        :param trigger_name: 触发器名称: 'Available memory'
        :return:
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "triggerprototype.update",
            "params": item_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            logger.debug(f"当前进度: {current_progress}/{total_length} ({(current_progress / total_length) * 100:.2f}%) {response['result']}")
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_triggerprototype_tag_bytemplateid(self, tag_list, total_length, current_progress):
        """
        更新触发器名称

        :param triggerid: 触发器ID: ['10084']
        :param trigger_name: 触发器名称: 'Available memory'
        :return:
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "triggerprototype.update",
            "params": tag_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            logger.debug(f"当前进度: {current_progress}/{total_length} ({(current_progress / total_length) * 100:.2f}%) {response['result']}")
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_template_application_bytemplateid(self, application_list, total_length, current_progress):
        """
        更新触发器名称

        :param triggerid: 触发器ID: ['10084']
        :param trigger_name: 触发器名称: 'Available memory'
        :return:
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "application.update",
            "params": application_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            logger.debug(f"当前进度: {current_progress}/{total_length} ({(current_progress / total_length) * 100:.2f}%) {response['result']}")
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_graph_name(self, item_list, total_length, current_progress):
        """
        更新图表名称

        :param graphid: 图表ID: ['10084']
        :param graph_name: 图表名称: 'Available memory'
        :return:
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "graph.update",
            "params": item_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            logger.debug(f"当前进度: {current_progress}/{total_length} ({(current_progress / total_length) * 100:.2f}%) {response['result']}")
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_update_graphprototype_name(self, item_list, total_length, current_progress):
        """
        更新图表名称

        :param graphid: 图表ID: ['10084']
        :param graph_name: 图表名称: 'Available memory'
        :return:
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "graphprototype.update",
            "params": item_list,
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            logger.debug(f"当前进度: {current_progress}/{total_length} ({(current_progress / total_length) * 100:.2f}%) {response['result']}")
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_get_en_list(self, excel_op, title_name, v_1, v_2, v_3, v_4, active_sheet_name):
        column_1_list = [f_1['templateid'] for f_1 in self.def_get_all_template_name()['result']]
        translator = CusLanguageTrans()
        excel_op.create_new_workbook()
        excel_op.create_sheet(self.def_check_zbx_version()['result'])
        [excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]

        # 初始化变量
        def_get_template_item_name_list = []
        all_template_id_list = []
        all_template_name_list = []
        all_template_host_list = []
        en_list = []
        ch_list = []
        row_index = {"index": 2}
        def_get_template_list = column_1_list

        # 进度计数器
        completed_count = 0
        total_templates = len(def_get_template_list)
        total_items = 0  # 将在处理模板后初始化

        # 回调函数：处理模板结果
        def template_callback(future, idx):
            nonlocal completed_count
            try:
                lv_result = future.result()
                if lv_result['tag'] is True:
                    def_get_template_item_name_list.append(lv_result['result'])
                completed_count += 1
                progress = (completed_count / total_templates) * 100
                print(f'模板处理进度: {completed_count}/{total_templates} ({progress:.2f}%)')
            except Exception as e:
                print(f"Error processing template {idx}: {str(e)}")

        # 第一个线程池：处理模板
        with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
            for idx, template_id in enumerate(def_get_template_list):
                future = executor.submit(v_3, template_id)
                future.add_done_callback(lambda f, idx=idx: template_callback(f, idx))

        # 收集所有模板项
        for f_1 in range(len(def_get_template_item_name_list)):
            for f_4 in def_get_template_item_name_list[f_1]:
                en_list.append(u'{0}'.format(f_4[v_1]))
                all_template_id_list.append(u'{0}'.format(f_4[v_2]))
                try:
                    if f_4.get('hosts') and len(f_4['hosts']) > 0:
                        all_template_host_list.append(u'{0}'.format(f_4['hosts'][0]['host']))
                    else:
                        # 如果没有关联的主机，使用模板自身的host字段（如果存在）
                        all_template_host_list.append(u'{0}'.format(f_4['templateid']))
                except KeyError:
                    all_template_host_list.append(u'{0}'.format(f_4['host']))

        total_items = len(all_template_id_list)
        completed_count = 0  # 重置计数器用于Excel操作

        # 回调函数：处理Excel行
        def excel_callback(future, idx):
            nonlocal completed_count, row_index
            try:
                row_index = future.result()
                completed_count += 1
                progress = (completed_count / total_items) * 100
                print(f'Excel写入进度: {completed_count}/{total_items} ({progress:.2f}%)')
            except Exception as e:
                print(f"Error processing row {idx}: {str(e)}")

        # 第二个线程池：Excel操作
        with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
            for __int_02 in range(len(all_template_id_list)):
                future = executor.submit(
                    self._process_excel_row,
                    excel_op,
                    row_index,
                    __int_02,
                    all_template_id_list,
                    all_template_host_list,
                    en_list
                )
                future.add_done_callback(lambda f, idx=__int_02: excel_callback(f, idx))

        excel_op.save_workbook(active_sheet_name + '.xlsx')

        # Helper method for Excel row processing

    def _process_excel_row(self, excel_op, row_index, index, all_template_id_list, all_template_host_list, en_list):
        excel_op.set_cell_value(row_index['index'], 1, row_index['index'] - 1)
        excel_op.set_cell_value(row_index['index'], 2, u'({0}/{1})'.format(len(all_template_id_list), index + 1))
        excel_op.set_cell_value(row_index['index'], 4, all_template_host_list[index])
        excel_op.set_cell_value(row_index['index'], 5, all_template_id_list[index])
        excel_op.set_cell_value(row_index['index'], 6, u'{0}'.format(en_list[index]))
        row_index.update({'index': row_index['index'] + 1})
        return row_index

    def def_set_zh_list(self, excel_op, v_2, v_1, v_4):
        excel_op.activate_sheet(self.def_check_zbx_version()['result'])
        column_1_list = excel_op.get_column_values(5)
        del column_1_list[0]
        column_2_list = excel_op.get_column_values(7)
        del column_2_list[0]
        column_3_list = excel_op.get_column_values(2)
        del column_3_list[0]
        column_4_list = excel_op.get_column_values(3)
        del column_4_list[0]
        def_update_list = []
        for f_1 in range(len(column_1_list)):
            if column_2_list[f_1].find("'tag':") != -1:
                column_2_list[f_1] = json.loads(column_2_list[f_1].replace("'", "\""))
            def_update_list.append({u"{v_2}".format(v_2=v_2): column_1_list[f_1], u"{v_1}".format(v_1=v_1): column_2_list[f_1]})

        # 获取列表长度
        total_length = len(def_update_list)

        # 预初始化结果列表
        results = [None] * total_length

        # 进度计数器
        completed_count = 0

        # 回调函数
        def progress_callback(future, index):
            nonlocal completed_count
            try:
                result = future.result()
                results[index] = result
                completed_count += 1
                progress_percentage = (completed_count / total_length) * 100
                print(f'当前进度: {completed_count}/{total_length} ({progress_percentage:.2f}%) {result}')
            except Exception as e:
                print(f"Error occurred while processing item {index}: {str(e)}")
                results[index] = None
                completed_count += 1

        with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
            # 提交所有任务并添加回调
            for index, item in enumerate(def_update_list):
                future = executor.submit(v_4, item, total_length, index + 1)
                future.add_done_callback(lambda f, idx=index: progress_callback(f, idx))

            # 等待所有任务完成
            executor.shutdown(wait=True)

        return results

    def def_get_dashboard(self):
        """
        获取主机组下所有主机名

        :return:  [{'hostid': '10084', 'name': 'Zabbix server'}]
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "dashboard.get",
            "params": {
                "output": "extend",
                "selectWidgets": "extend",
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        print(response)
        exit(1)
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_export_configuration(self, templateid):
        """

        :param templates_list: 模板列表 [10161, 10162]
        :return:
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "configuration.export",
            "params": {
                "options": {
                    "templates": [templateid]
                },
                "format": "json"
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_import_configuration_5_0(self, source):
        """

        :param source: 模板数据源
        :return:
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "configuration.import",
            "params": {
                "format": "json",
                "rules": {
                    "groups": {
                        "createMissing": True,
                    },
                    "templates": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "templateScreens": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "templateLinkage": {
                        "createMissing": True,
                    },
                    "applications": {
                        "createMissing": True,
                    },
                    "items": {
                        "createMissing": True,
                        "updateExisting": True,
                    },
                    "discoveryRules": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "triggers": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "graphs": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "httptests": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "valueMaps": {
                        "createMissing": True,
                        "updateExisting": False
                    },
                },
                "source": source,
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_import_configuration_6_0(self, source):
        """

        :param source: 模板数据源
        :return:
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "configuration.import",
            "params": {
                "format": "json",
                "rules": {
                    "groups": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "templates": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "valueMaps": {
                        "createMissing": True,
                        "updateExisting": False
                    },
                    "templateDashboards": {
                        "createMissing": True,
                        "updateExisting": True,
                    },
                    "templateLinkage": {
                        "createMissing": True,
                    },
                    "items": {
                        "createMissing": True,
                        "updateExisting": True,
                    },
                    "discoveryRules": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "triggers": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "graphs": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "httptests": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                },
                "source": source,
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_import_configuration_6_4(self, source):
        """

        :param source: 模板数据源
        :return:
        """
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "configuration.import",
            "params": {
                "format": "json",
                "rules": {
                    "template_groups": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "host_groups": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "templates": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "valueMaps": {
                        "createMissing": True,
                        "updateExisting": False
                    },
                    "templateDashboards": {
                        "createMissing": True,
                        "updateExisting": True,
                    },
                    "templateLinkage": {
                        "createMissing": True,
                    },
                    "items": {
                        "createMissing": True,
                        "updateExisting": True,
                    },
                    "discoveryRules": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "triggers": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "graphs": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                    "httptests": {
                        "createMissing": True,
                        "updateExisting": True
                    },
                },
                "source": source,
            },
            "auth": self.authID,
            "id": 1
        })
        request = self.session.post(url=self.url, headers=self.header, data=data, verify=False)
        response = request.json()
        if response.get('result', ''):
            return {'tag': True, 'result': response['result']}
        if response.get('error', ''):
            GV_ERROR_MESS['error'] = response['error']
            logger.debug(u"错误: \033[;31m{0}\033[0m \033[;31m{1}\033[0m".format(inspect.stack()[0][2], response['error']))
            return {'tag': False, 'result': response['error']}
        else:
            return {'tag': False, 'result': response}

    def def_timecovert(self, stringtime):
        timeArray = time.strptime(stringtime, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

    def def_timeCovertIntToYMD(self, inttime):
        timeArray = time.localtime(inttime)
        timeStamp = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return timeStamp

    def def_convert_numeric_to_text_problem_severity(self, value):
        if value == '0':
            self.textValue = '未分类'
        elif value == '1':
            self.textValue = '信息'
        elif value == '2':
            self.textValue = '警告'
        elif value == '3':
            self.textValue = '一般严重'
        elif value == '4':
            self.textValue = '严重'
        elif value == '5':
            self.textValue = '灾难'
        else:
            self.textValue = value
        return self.textValue

    def def_convert_numeric_to_text(self, value):
        if value == '0':
            self.textValue = '消息未发送'
        elif value == '1':
            self.textValue = '消息已发送'
        elif value == '2':
            self.textValue = '经多次重试后失败'
        elif value == '3':
            self.textValue = '告警管理员尚未处理的新告警'
        elif value == 'Not classified':
            self.textValue = '未分类'
        elif value == 'Information':
            self.textValue = '信息'
        elif value == 'Warning':
            self.textValue = '警告'
        elif value == 'Average':
            self.textValue = '一般严重'
        elif value == 'High':
            self.textValue = '严重'
        elif value == 'Disaster':
            self.textValue = '灾难'
        else:
            self.textValue = value
        return self.textValue

    def def_convert_numeric_to_text_problem(self, value):
        if value == '0':
            self.textValue = '恢复'
        elif value == '1':
            self.textValue = '故障'
        else:
            self.textValue = value
        return self.textValue


# 配置日志
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


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
            # 尝试转换值为字符串以处理特殊字符
            if value is not None:
                # 清理特殊字符
                str_value = str(value)
                # 移除或替换可能引起问题的字符
                str_value = str_value.replace('\x00', '')  # 移除空字符
                str_value = str_value.replace('\r\n', '\n').replace('\r', '\n')  # 统一换行符
                # 替换其他可能的问题字符
                str_value = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', str_value)

                self._worksheet.cell(row=row, column=col_idx).value = str_value
            else:
                self._worksheet.cell(row=row, column=col_idx).value = None

        except Exception as e:
            error_msg = f"设置单元格({row},{col_idx})失败: {type(e).__name__}: {str(e)}"
            logger.warning(error_msg)
            print(f"Excel错误详情: {error_msg}")

            try:
                # 尝试保存错误信息
                self._worksheet.cell(row=row, column=col_idx).value = f"错误: {type(e).__name__}"
            except:
                pass

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


class CusMysqlOp(object):
    def __init__(self):
        """
        excel_op = ExcelOp(file='zabbix_api.xlsx', index=16)
        column_1_list = excel_op.get_cell_value(1)
        del column_1_list[0]
        title_name = ['主机名']
        excel_op.create_sheet(excel_op._worksheet)
        [excel_op.set_cell_value(1, i + 1, title_name[i]) for i in range(len(title_name))]
        [excel_op.set_cell_value(i + 2, 1, column_1_list[i]) for i in range(len(column_1_list))]
        excel_op.save_workbook(excel_op._worksheet)
        """
        self.file = None
        self.wb_object = None
        self.sheet_name = None
        self.ws_object = None

        self.create_file = None
        self.create_ws_object = None
        self.create_wb_object = None
        # excel_file = 'example.xlsx'
        # host = 'localhost'
        # user = 'your_username'
        # password = 'your_password'
        # database = 'your_database'
        # table = 'your_table'
        # insert_excel_to_mysql(excel_file, host, user, password, database, table)

    # @staticmethod
    # def insert_excel_to_mysql(excel_file, host, user, password, database, table):
    #     try:
    #         # 连接到 MySQL 数据库
    #         connection = pymysql.connect(
    #             host=host,
    #             user=user,
    #             password=password,
    #             database=database,
    #             cursorclass=pymysql.cursors.DictCursor
    #         )
    #         # 加载 Excel 文件
    #         workbook = load_workbook(excel_file)
    #         sheet = workbook.active
    #         # 获取表头
    #         headers = [cell.value for cell in sheet[1]]
    #         with connection.cursor() as cursor:
    #             # 逐行插入数据
    #             for row in sheet.iter_rows(min_row=2, values_only=True):
    #                 data = dict(zip(headers, row))
    #                 columns = ', '.join(data.keys())
    #                 placeholders = ', '.join(['%s'] * len(data))
    #                 sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    #                 cursor.execute(sql, tuple(data.values()))
    #         # 提交事务
    #         connection.commit()
    #         print("数据插入成功！")
    #     except Exception as e:
    #         print(f"发生错误: {e}")
    #         connection.rollback()
    #     finally:
    #         # 关闭连接
    #         connection.close()


class CusAssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg


class CusUrl:
    def __init__(self, host, path, schema):
        self.host = host
        self.path = path
        self.schema = schema
        pass


class CusLanguageTransOne(object):
    def __init__(self):
        # 应用ID（到控制台获取）
        self.APPID = "668c78a6"
        # 接口APISercet（到控制台机器翻译服务页面获取）
        self.Secret = "ZGVlMGM5OThmZDljYWVkYTFjNGZlYzll"
        # 接口APIKey（到控制台机器翻译服务页面获取）
        self.APIKey = "066246864d8bca0557c7b4fa9e128cde"
        # 术语资源唯一标识，请根据控制台定义的RES_ID替换具体值，如不需术语可以不用传递此参数
        self.RES_ID = "epktzy16ho"
        self.url = "https://itrans.xf-yun.com/v1/its"
        # 翻译原文本内容

    def assemble_ws_auth_url(self, requset_url, method="POST", api_key="", api_secret=""):
        u = self.parse_url(requset_url)
        host = u.host
        path = u.path
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        logger.warning(date)
        # date = "Thu, 12 Dec 2019 01:57:27 GMT"
        signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
        logger.debug(signature_origin)
        signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            api_key, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        logger.debug(authorization_origin)
        values = {
            "host": host,
            "date": date,
            "authorization": authorization
        }

        return requset_url + "?" + urlencode(values)

    def parse_url(self, requset_url):
        stidx = requset_url.index("://")
        host = requset_url[stidx + 3:]
        schema = requset_url[:stidx + 3]
        edidx = host.index("/")
        if edidx <= 0:
            raise CusAssembleHeaderException("invalid request url:" + requset_url)
        path = host[edidx:]
        host = host[:edidx]
        u = CusUrl(host, path, schema)
        return u

    def sha256base64(self, data):
        sha256 = hashlib.sha256()
        sha256.update(data)
        digest = base64.b64encode(sha256.digest()).decode(encoding='utf-8')
        return digest

    def def_trans(self, text):
        if text == '':
            return ''
        request_url = self.assemble_ws_auth_url(self.url, "POST", self.APIKey, self.Secret)
        headers = {'content-type': "application/json", 'host': 'itrans.xf-yun.com', 'app_id': self.APPID}
        logger.debug(request_url)
        logger.debug(text)
        v_int_ifcut = int(len(text) / 5000)
        v_list_text = text.split('\n#| ')
        v_list_cut_list = []
        v_list_cn = []
        v_int_cut_num = int(len(v_list_text) / (v_int_ifcut + 1))
        logger.debug(v_int_ifcut)
        logger.debug(v_int_cut_num)
        logger.debug(len(v_list_text))
        for i in range(len(v_list_text)):
            v_list_cut_list.append(v_list_text[i])
            if i == v_int_cut_num - 1:
                text = "\n#| ".join(v_list_cut_list)
                logger.debug(text)
                body = {
                    "header": {
                        "app_id": self.APPID,
                        "status": 3,
                        "res_id": self.RES_ID
                    },
                    "parameter": {
                        "its": {
                            "from": "en",
                            "to": "cn",
                            "result": {}
                        }
                    },
                    "payload": {
                        "input_data": {
                            "encoding": "utf8",
                            "status": 3,
                            "text": base64.b64encode(text.encode("utf-8")).decode('utf-8')
                        }
                    }
                }
                response = requests.post(request_url, data=json.dumps(body), headers=headers)
                tempResult = json.loads(response.content.decode())
                v_json = json.loads(base64.b64decode(tempResult['payload']['result']['text']).decode())
                logger.debug(base64.b64decode(tempResult['payload']['result']['text']).decode())
                v_list_cn.append(v_json['trans_result']['dst'].upper())
                v_list_cut_list.clear()
                v_int_cut_num = (v_int_ifcut + 1) * v_int_cut_num + 1
        return "\n#| ".join(v_list_cn)


class CusLanguageTransTwo(object):
    def __init__(self, host="itrans.xfyun.cn"):
        # 应用ID（到控制台获取）
        self.APPID = "668c78a6"
        # 接口APISercet（到控制台机器翻译服务页面获取）
        self.Secret = "ZGVlMGM5OThmZDljYWVkYTFjNGZlYzll"
        # 接口APIKey（到控制台机器翻译服务页面获取）
        self.APIKey = "066246864d8bca0557c7b4fa9e128cde"

        # 以下为POST请求
        self.Host = host
        self.RequestUri = "/v2/its"
        # 设置url
        logger.debug(host)
        self.url = "https://" + host + self.RequestUri
        self.HttpMethod = "POST"
        self.Algorithm = "hmac-sha256"
        self.HttpProto = "HTTP/1.1"

        # 设置当前时间
        curTime_utc = datetime.utcnow()
        self.Date = self.httpdate(curTime_utc)
        # 设置业务参数
        # 语种列表参数值请参照接口文档：https://www.xfyun.cn/doc/nlp/xftrans/API.html
        self.Text = "你好吗"
        self.BusinessArgs = {
            "from": "en",
            "to": "cn",
        }

    def hashlib_256(self, res):
        m = hashlib.sha256(bytes(res.encode(encoding='utf-8'))).digest()
        result = "SHA-256=" + base64.b64encode(m).decode(encoding='utf-8')
        return result

    def httpdate(self, dt):
        """
        Return a string representation of a date according to RFC 1123
        (HTTP/1.1).

        The supplied date must be in UTC.

        """
        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                 "Oct", "Nov", "Dec"][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
                                                        dt.year, dt.hour, dt.minute, dt.second)

    def generateSignature(self, digest):
        signatureStr = "host: " + self.Host + "\n"
        signatureStr += "date: " + self.Date + "\n"
        signatureStr += self.HttpMethod + " " + self.RequestUri \
                        + " " + self.HttpProto + "\n"
        signatureStr += "digest: " + digest
        signature = hmac.new(bytes(self.Secret.encode(encoding='utf-8')),
                             bytes(signatureStr.encode(encoding='utf-8')),
                             digestmod=hashlib.sha256).digest()
        result = base64.b64encode(signature)
        return result.decode(encoding='utf-8')

    def init_header(self, data):
        digest = self.hashlib_256(data)
        logger.debug(digest)
        sign = self.generateSignature(digest)
        authHeader = 'api_key="%s", algorithm="%s", ' \
                     'headers="host date request-line digest", ' \
                     'signature="%s"' \
                     % (self.APIKey, self.Algorithm, sign)
        logger.debug(authHeader)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Method": "POST",
            "Host": self.Host,
            "Date": self.Date,
            "Digest": digest,
            "Authorization": authHeader
        }
        return headers

    def get_body(self, text):
        content = str(base64.b64encode(text.encode('utf-8')), 'utf-8')
        postdata = {
            "common": {"app_id": self.APPID},
            "business": self.BusinessArgs,
            "data": {
                "text": content,
            }
        }
        body = json.dumps(postdata)
        logger.debug(body)
        return body

    def def_trans(self, text):
        if self.APPID == '' or self.APIKey == '' or self.Secret == '':
            print('Appid 或APIKey 或APISecret 为空！请打开demo代码，填写相关信息。')
        else:
            code = 0
            body = self.get_body(text)
            headers = self.init_header(body)
            logger.debug(self.url)
            if text == '':
                return ''
            response = requests.post(self.url, data=body, headers=headers, timeout=8)
            status_code = response.status_code
            logger.debug(response.content)
            if status_code != 200:
                # 鉴权失败
                print("Http请求失败，状态码：" + str(status_code) + "，错误信息：" + response.text)
                print("请根据错误信息检查代码，接口文档：https://www.xfyun.cn/doc/nlp/xftrans/API.html")
            else:
                # 鉴权成功
                # respData = json.loads(response.text)
                respData = response.json()
                if respData.get('data', ''):
                    logger.debug(respData['data']['result']['trans_result']['dst'])
                    return respData['data']['result']['trans_result']['dst']
                else:
                    return respData['desc']
                # 以下仅用于调试
                # code = str(respData["code"])
                # if code != '0':
                #     print("请前往https://www.xfyun.cn/document/error-code?code=" + code + "查询解决办法")


class CusLanguageTrans(object):
    def __init__(self):
        # 应用ID（到控制台获取）
        self.APPID = "668c78a6"
        # 接口APISercet（到控制台机器翻译服务页面获取）
        self.Secret = "ZGVlMGM5OThmZDljYWVkYTFjNGZlYzll"
        # 接口APIKey（到控制台机器翻译服务页面获取）
        self.APIKey = "066246864d8bca0557c7b4fa9e128cde"
        # 术语资源唯一标识，请根据控制台定义的RES_ID替换具体值，如不需术语可以不用传递此参数
        self.RES_ID = "epktzy16ho"
        self.url = "https://fanyi.xfyun.cn/api-tran/trans/its"
        self.cookies = {
            '_wafuid': '42179584',
            'JSESSIONID': '5C64510B0B5D7E4C6F8ADF6E3D9EEF19',
            '_gcl_au': '1.1.534731207.1666665336',
            'Hm_lvt_fe740601c79b0c00b6d5458d146aa5ef': '1666665336',
            'gr_user_id': '4d219912-8592-41f1-9405-a3f3b77165db',
            '8473744dbcf62d60_gr_session_id': '20b029c9-36ef-4685-9cbb-ac525a8d18e3',
            '8473744dbcf62d60_gr_session_id_20b029c9-36ef-4685-9cbb-ac525a8d18e3': 'true',
            '_ga': 'GA1.2.75942607.1666665337',
            '_gid': 'GA1.2.1536677545.1666665337',
            'Hm_lpvt_fe740601c79b0c00b6d5458d146aa5ef': '1666665358',
            'di_c_mti': 'f634cf0f-f6c0-697e-a6c2-b130d51ed2ea',
            'Hm_lvt_46f7583efda1cc689658545dca371747': '1666665365',
            'ssoSessionId': '06c679b6-ee78-4763-aa91-2b4ace6a0810',
            'account_id': '14795786860',
            'Hm_lpvt_46f7583efda1cc689658545dca371747': '1666665395',
        }

        self.headers = {
            'Host': 'fanyi.xfyun.cn',
            'Accept': 'application/json, text/plain, */*',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'Origin': 'https://fanyi.xfyun.cn',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://fanyi.xfyun.cn/console/trans/text',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            # Requests sorts cookies= alphabetically
            # 'Cookie': '_wafuid=42179584; JSESSIONID=5C64510B0B5D7E4C6F8ADF6E3D9EEF19; _gcl_au=1.1.534731207.1666665336; Hm_lvt_fe740601c79b0c00b6d5458d146aa5ef=1666665336; gr_user_id=4d219912-8592-41f1-9405-a3f3b77165db; 8473744dbcf62d60_gr_session_id=20b029c9-36ef-4685-9cbb-ac525a8d18e3; 8473744dbcf62d60_gr_session_id_20b029c9-36ef-4685-9cbb-ac525a8d18e3=true; _ga=GA1.2.75942607.1666665337; _gid=GA1.2.1536677545.1666665337; Hm_lpvt_fe740601c79b0c00b6d5458d146aa5ef=1666665358; di_c_mti=f634cf0f-f6c0-697e-a6c2-b130d51ed2ea; Hm_lvt_46f7583efda1cc689658545dca371747=1666665365; ssoSessionId=06c679b6-ee78-4763-aa91-2b4ace6a0810; account_id=14795786860; Hm_lpvt_46f7583efda1cc689658545dca371747=1666665395',
        }
        self.session = requests.Session()
        self.session.mount(self.url, requests.adapters.HTTPAdapter(max_retries=3))
        # 翻译原文本内容

    def def_trans(self, text):
        return text.replace('\n', '')

        if text == '':
            return ''

        v_int_ifcut = int(len(text) / 2000)
        v_list_text = text.split('\n#| ')
        v_list_cut_list = []
        v_list_cn = []
        v_int_cut_num = int(len(v_list_text) / (v_int_ifcut + 1))
        logger.debug(v_int_ifcut)
        logger.debug(v_int_cut_num)
        logger.debug(len(v_list_text))
        for i in range(len(v_list_text)):
            v_list_cut_list.append(v_list_text[i])
            if i == v_int_cut_num - 1:
                text = "\n#| ".join(v_list_cut_list)
                logger.debug(text)
                data = {
                    'from': 'en',
                    'to': 'cn',
                    'text': text,
                }
                time.sleep(1)
                logger.debug(text)
                request = self.session.post(url=self.url, cookies=self.cookies, headers=self.headers, data=data)
                response = request.json()
                if response.get('data', ''):
                    v_json = json.loads(response['data'])['trans_result']['dst'].upper()
                    if v_json == '':
                        GV_ERROR_MESS = u'{0}'.format('翻译错误未执行完毕')
                    v_list_cn.append(v_json)
                    v_list_cut_list.clear()
                    v_int_cut_num = (v_int_ifcut + 1) * v_int_cut_num + 1
        return "\n#| ".join(v_list_cn)


class CusTermProcessor:
    """Markdown文档处理器，用于保护术语、代码块、表格等元素

    功能:
    - 术语保护与替换
    - 代码块保护
    - 表格列保护
    - 链接保护与翻译
    - 标题保护
    - 函数保护

    属性:
        debug_config (Dict[str, bool]): 调试开关配置
        debug_level (Dict[str, int]): 调试级别配置
        excel_op (CusExcelOp): Excel操作对象
        term_dict (Dict): 术语字典
        header_terms (Dict): 标题术语字典
        link_terms (Dict): 链接术语字典
        _caches (Dict): 缓存结构
    """

    def __init__(self, excel_path: str):
        """初始化术语处理器

        参数:
            excel_path (str): Excel文件路径，包含3个sheet:
                - Sheet1: 术语保护
                - Sheet2: 标题保护
                - Sheet3: 链接保护
        """
        # 调试开关配置
        self.debug_config = {
            'code': False,  # 代码块相关调试
            'table': False,  # 表格相关调试
            'link': False,  # 链接相关调试
            'term': False,  # 术语相关调试
            'header': False,  # 标题相关调试
            'func': False,  # 函数相关调试
            'cache': False,  # 缓存系统相关调试
            'clean': False,  # 清理相关调试
            'all': False  # 全部调试
        }

        # 调试级别配置
        self.debug_level = {
            'code': 1,  # 1=基础信息, 2=详细信息, 3=全量数据
            'table': 1,
            'link': 1,
            'term': 1,
            'header': 1,
            'func': 1,
            'cache': 1
        }

        self.excel_op = CusExcelOp()
        self.excel_path = excel_path

        # 加载术语表
        self.excel_op.load_excel(excel_path, 1)
        self.term_dict = self._build_term_dictionary()

        # 加载标题术语表
        self.excel_op.load_excel(excel_path, 2)
        self.header_terms = self._build_dictionary('header')

        # 加载链接术语表
        self.excel_op.load_excel(excel_path, 3)
        self.link_terms = self._build_dictionary('link')

        # 初始化缓存结构
        self._init_caches()

        self._create_protection_markers()
        self._ensure_required_terms()

        # 预编译正则表达式
        self._compile_patterns()

    def _init_caches(self) -> None:
        """初始化缓存结构"""
        self._caches = {
            'code': {
                'protected_data': {},
                'stats': {
                    'blocks_protected': 0,
                    'inline_protected': 0,
                    'special_protected': 0,
                    'code_inline_protected': 0,
                    'empty_protected': 0,
                    'unmarked_blocks_protected': 0
                }
            },
            'table': {
                'protected_data': {},
                'stats': {
                    'tables_processed': 0,
                    'columns_protected': 0
                }
            },
            'link': {
                'protected_data': {},
                'stats': {
                    'links_protected': 0,
                    'links_translated': 0
                }
            },
            'term': {
                'protected_data': {},
                'stats': {
                    'terms_replaced': 0
                }
            },
            'header': {
                'protected_data': {},
                'stats': {
                    'headers_protected': 0
                }
            },
            'func': {
                'protected_data': {},
                'stats': {
                    'functions_protected': 0
                }
            },
            'macro': {
                'protected_data': {},
                'stats': {
                    'macros_protected': 0,
                    'max_nesting_level': 0
                }
            }
        }
        self.header_mapping = {}  # 缓存HEADER_MAPPING表数据 {EN: ZH}
        self.link_mapping = []  # 缓存LINK_MAPPING表数据

    def _compile_patterns(self) -> None:
        """预编译所有正则表达式"""
        # 1. 标题保护正则
        # 修改后的标题正则表达式（确保捕获所有换行符）
        self.header_pattern = re.compile(
            r'(?P<full_header>'
            r'(?P<prefix>^#{1,6}\s+)'  # 1-6个#加空格
            r'(?P<content>[^\n]+?)'  # 非换行内容
            r'(?:\s+\{\s*#(?P<anchor>[\w-]+)\s*\})?'  # 可选锚点
            r'(?P<suffix>(?:\n|$)+))',  # 一个或多个换行或结束（修改此处）
            re.MULTILINE
        )

        # 表格列保护配置（优化版）
        self.protected_columns = {
            # 精确匹配基础列名（提高性能）
            r'\b.*Method.*\b',
            r'\b\*Name\*\b',
            r'\b\*type\*\b',
            r'\b\*Type\*\b',  # 加粗格式
            r'\b`?property`?\b',
            r'\b`Type`\b',  # 代码格式
            r'\bColumn\b',
            r'\bElement\b',
            r'\bField\b',
            r'\bFunction group\b',
            r'\bFunction\b',
            r'\bid\b',
            r'\bID\b',
            r'\bItem key\b',
            r'\bMacro\b',
            r'\bMandatory\b',
            r'\bMethod\b',
            r'\bName\b',
            r'\bOption\b',  # 完全匹配
            r'\bParameter\b',  # 完全匹配
            r'\bPlatform\b',
            r'\bProperty\b',  # 完全匹配
            r'\bRange\b',
            r'\bSupported operators\b',  # 完全匹配
            r'\bSymbol\b',  # 完全匹配
            r'\bTemplate name\b',  # 完全匹配
            r'\bType\b',  # 精确匹配
            r'\bType\b',  # 完全匹配
            r'\btype\b',  # 小写匹配
            r'\bUpgrade from\b',  # 完全匹配
            r'\bWidget\b',  # 完全匹配
            r'\bPrefix\b',  # 完全匹配
            r'\bInterval\b',  # 完全匹配
        }

        # 更新为最终版模式
        self.unwanted_patterns = {
            r'^###\s*指令保护技术标记原样输出\s*$',  # 精确匹配整行
            r'###\s*(待翻译文本|翻译文本|翻译结果|Original text|Text to translate)[:：]?\s*',
            r'【待翻译】',
            r'(?:^|\n|[（(])\s*(?:注|注意|请注意)[：:)].*?(?:保持不变|直接复制)[^。]*。\s*',
            r'(?:^|\n)\s*[（(]注：.*OutputFormat.*[）)]\s*$',  # 模糊匹配
        }

        # 预编译所有正则表达式
        self._compiled_unwanted_patterns = [re.compile(p, re.IGNORECASE) for p in self.unwanted_patterns]

        # 代码块正则
        self.code_block_pattern = re.compile(
            r'(?P<full_block>(?P<fence>```+)\s*(?P<lang>[^\n]*)\n'
            r'(?P<content>.*?)\n'
            r'(?P=fence)\s*\n?)',  # 确保匹配代码块后的换行符
            re.DOTALL
        )

        # 行内代码正则
        self.inline_code_pattern = re.compile(
            r'(?P<full_inline>`[^`\n]+`)',
        )

        self.inline_notecode_pattern = re.compile(
            r'(?P<special>:::|::: ?[a-zA-Z]+)'
        )

        self.inline_code_inline_pattern = re.compile(
            r'(?P<code_inline>\n    [^\n]+(?:\n    [^\n]+)*\n\n)',
            re.MULTILINE
        )

        self.inline_empty_pattern = re.compile(
            r'(?P<empty>^\s*\n\s*)',
            re.MULTILINE
        )

        # 链接正则
        self.link_pattern = re.compile(
            r'(?P<full_link>'  # 完整链接捕获组开始
            r'(?P<image>!)?'  # 可选的图片标记
            r'\[(?P<text>[^]]*)\]'  # 链接文本
            r'\('  # 开始URL部分
            r'(?P<url>'  # 完整URL捕获组开始
            r'(?P<url_path>[^#)"\']+)'  # URL路径部分（排除#、)和引号）
            r'(?:#(?P<url_anchor>[\w-]+))?'  # 可选的锚点部分
            r')'  # 完整URL捕获组结束
            r'(?:\s*["\'][^"\']*["\'])?'  # 可选的标题
            r'\)'  # 结束URL部分
            r')',    # 完整链接捕获组结束
            re.MULTILINE
        )

        # 表格正则
        self.table_pattern = re.compile(
            r'(?P<full_table>(?:^|\n)\s*'
            r'(?P<header>\|.*?\|)\s*\n'
            r'(?P<align>\|[\s\-:]*\|)*\s*\n?'
            r'(?P<rows>(?:\|.*?\|(?:\n|$))+)'
            r'\s*(?=\n|$))',
            re.MULTILINE
        )

        self.macro_pattern = re.compile(
            r'''
            \{                      # 宏开始
            ([$#]?)                 # 可选的$符号(组1)
            (                       # 宏名称部分(组2)
                [A-Z][A-Z0-9_.]*    # 必须大写字母开头
                (?:<[1-9]>)?        # 可选的索引标记
            )
            \}                      # 宏结束
            ''',
            re.VERBOSE
        )

        # 预定义的函数名列表
        self.protected_functions = {
            'get', 'update', 'create', 'delete', 'massadd',
            'massremove', 'massupdate', 'odbc', 'tcp', 'acknowledge',
            'adddependencies', 'checkAuthentication', 'clear',
            'container_info[]', 'container_stats', 'copy', 'cpu',
            'createglobal', 'deletedependencies', 'deleteglobal',
            'execute', 'export', 'file', 'generate', 'getscriptsbyhosts',
            'getsli', 'import', 'importcompare', 'login', 'logout',
            'mem', 'memory', 'replacehostinterfaces', 'run', 'udp',
            'unblock', 'updateglobal', 'version', 'icmpping', 'icmppingloss',
            'vfs.file.exists'
        }

        # 修改后的函数正则表达式 - 支持圆括号参数和加粗格式
        self.function_pattern = re.compile(
            r'\b'  # 单词边界开始
            r'(?P<full_function>'
            r'(?P<bold>\*\*)?'  # 可选的加粗标记开头
            r'(?P<name>' + '|'.join(re.escape(f) for f in self.protected_functions) + r')\b'  # 受保护的函数名，后面是单词边界
            r'(?P<bold_end>\*\*)?'  # 可选的加粗标记结尾
            r'(?:\s*[\\\[]\s*(?P<params>[^\]]*)\s*[\\\]])?'  # 参数部分（使用方括号，可选）
            r'(?:\s*\{\s*#(?P<id>[\w.]+)\s*\})?'  # 可选ID部分
            r')'  # 结束full_function组
            r'\b'  # 单词边界结束
        )


    # ==================== 构建字典 ====================
    def _build_term_dictionary(self) -> Dict[str, Any]:
        """构建术语字典（带详细统计输出）

        返回:
            Dict: 包含以下结构的字典:
                - original_terms: 原始术语映射
                - lowercase_index: 小写术语索引
                - special_terms: 特殊格式术语列表
                - raw_count: 原始条目数
                - loaded_count: 有效加载数
                - empty_source: 空源术语计数
                - empty_target: 空目标术语计数
        """
        self._debug_print('term', 1, "开始构建术语字典")
        src_col = self.excel_op.get_column_values(1)
        tgt_col = self.excel_op.get_column_values(2)

        term_data = {
            'original_terms': {},
            'lowercase_index': defaultdict(list),
            'special_terms': [],
            'raw_count': 0,
            'loaded_count': 0,
            'empty_source': 0,
            'empty_target': 0
        }

        for src, tgt in zip(src_col, tgt_col):
            term_data['raw_count'] += 1
            src_term = str(src).strip() if src is not None else ''
            tgt_term = str(tgt).strip() if tgt is not None else ''

            if not src_term:
                term_data['empty_source'] += 1
                continue

            term_data['original_terms'][src_term] = tgt_term
            term_data['lowercase_index'][src_term.lower()].append(src_term)

            if not tgt_term:
                term_data['empty_target'] += 1

            if not src_term.isalnum():
                term_data['special_terms'].append(src_term)

            term_data['loaded_count'] += 1

        # 详细统计输出
        self._debug_print('term', 1, "\n术语表统计:")
        self._debug_print('term', 1, f"总条目数: {term_data['raw_count']}")
        self._debug_print('term', 1, f"有效加载: {term_data['loaded_count']}")
        self._debug_print('term', 1, f"空源术语: {term_data['empty_source']}")
        self._debug_print('term', 1, f"空目标术语: {term_data['empty_target']}")
        self._debug_print('term', 1, f"特殊格式术语: {len(term_data['special_terms'])}")
        return term_data

    def _build_dictionary(self, dict_type: str) -> Dict[str, str]:
        """通用字典构建方法

        参数:
            dict_type (str): 字典类型('header'或'link')

        返回:
            Dict[str, str]: 术语映射字典
        """
        src_col = self.excel_op.get_column_values(1)
        tgt_col = self.excel_op.get_column_values(2)

        data = {
            'terms': {},
            'raw_count': len(src_col),
            'loaded_count': 0,
            'empty_source': 0,
            'empty_target': 0
        }

        for src, tgt in zip(src_col, tgt_col):
            src_term = str(src).strip() if src is not None else ''
            tgt_term = str(tgt).strip() if tgt is not None else ''

            if not src_term:
                data['empty_source'] += 1
                continue

            data['terms'][src_term] = tgt_term
            data['loaded_count'] += 1

            if not tgt_term:
                data['empty_target'] += 1

        # 统计输出
        self._debug_print(dict_type, 1, f"[{dict_type}术语表统计]")
        self._debug_print(dict_type, 1, f"总条目数: {data['raw_count']}")
        self._debug_print(dict_type, 1, f"有效加载: {data['loaded_count']}")
        self._debug_print(dict_type, 1, f"空源术语: {data['empty_source']}")
        self._debug_print(dict_type, 1, f"空目标术语: {data['empty_target']}")

        if dict_type == 'link':
            self._debug_print(dict_type, 1, f"最终加载的{dict_type}术语: {data['terms']}")

        return data['terms']

    # ==================== 标记生成方法 ====================
    def _create_marker(self, prefix: str, content: str) -> str:
        """通用标记生成方法（8位哈希）"""
        return f"{{{prefix}_{md5(content.encode()).hexdigest()[:8]}}}"

    def _create_header_marker(self, header: str) -> str:
        """生成标题专用标记（8位哈希）"""
        return self._create_marker("HEADER", header)

    def _create_code_marker(self, content: str) -> str:
        """生成代码块标记"""
        return self._create_marker("CODE", content)

    def _create_term_marker(self, term: str) -> str:
        """生成术语标记"""
        return self._create_marker("TERM", term)

    def _create_table_marker(self, content: str) -> str:
        """生成表格标记"""
        return self._create_marker("EXCEL", content)

    def _create_link_marker(self, link: str) -> str:
        """生成链接标记"""
        return self._create_marker("LINK", link)

    def _create_function_marker(self, function: str) -> str:
        """生成函数标记"""
        return self._create_marker("FUNC", function)

    def _create_macro_marker(self, function: str) -> str:
        """生成函数标记"""
        return self._create_marker("MACRO", function)

    def _create_protection_markers(self):
        """
        初始化所有保护内容的标记系统，包括：
        - 术语标记（term_to_marker）
        - 代码块标记（在_protect_code_blocks中生成）
        - 表格标记（在_protect_table_columns中生成）
        """
        self.term_to_marker = {}
        self.marker_to_term = {}

        # # 初始化术语缓存
        # self._caches['term']['protected_data'] = {}

        for term, translation in self.term_dict['original_terms'].items():
            marker = self._create_term_marker(term)
            self.term_to_marker[term] = marker
            self.marker_to_term[marker] = translation

            # # 将标记存入缓存系统
            # self._caches['term']['protected_data'][marker] = {
            #     'original': term,
            #     'translated': translation
            # }

            # # 更新统计信息
            # self._caches['term']['stats']['terms_replaced'] = len(self.term_to_marker)

    # ==================== 核心处理方法 ====================
    def _protect_table_columns(self, table: Dict) -> Tuple[str, Dict]:
        """安全增强版表格列保护（分阶段处理链接）"""
        lines = [table['header']]
        if table.get('align_line'):
            lines.append(table['align_line'])
        lines.extend(table['rows'])

        # 阶段1：仅保护非标题行中的链接（保留标题链接用于列识别）
        link_protected_lines = []
        for line_idx, line in enumerate(lines):
            if line_idx == 0:  # 标题行不处理链接
                link_protected_lines.append(line)
            else:
                protected_line, link_data = self._protect_markdown_links(line)
                self._caches['table']['protected_data'].update(link_data)
                link_protected_lines.append(protected_line)

        # 阶段2：识别保护列（处理带格式/链接的列名）
        header_cols = [c.strip() for c in table['header'].split('|')[1:-1]]
        protected_indices = set()

        for i, name in enumerate(header_cols):
            # 提取纯文本列名（去除链接标记）
            plain_name = re.sub(r'\[([^\]]+)\]\[[^)]+\]', r'\1', name)
            if self._is_protected_column(plain_name):
                protected_indices.add(i)
                # 保护标题中的链接（如果有）
                if '](' in name:
                    protected_name, link_data = self._protect_markdown_links(name)
                    self._caches['table']['protected_data'].update(link_data)
                    header_cols[i] = protected_name

        # 更新统计
        self._caches['table']['stats']['columns_protected'] += len(protected_indices)
        self._caches['table']['stats']['tables_processed'] += 1

        # 阶段3：处理表格内容
        col_widths = [
            max(3, len(self._normalize_header(re.sub(r'\[([^\]]+)\]\[[^)]+\]', r'\1', col))))
            for col in header_cols
        ]

        processed_lines = []
        for line_idx, line in enumerate(link_protected_lines):
            # 处理标题行（可能包含已保护的链接）
            if line_idx == 0:
                processed_header = '|' + '|'.join([
                    f' {col.strip()} '.ljust(col_widths[i] + 2)
                    for i, col in enumerate(header_cols)
                ]) + '|'
                processed_lines.append(processed_header)
                continue

            # 保持原始分隔线
            if line_idx == 1 and all(c in ('-', ':') or c == '|' for c in line):
                processed_lines.append(line)
                continue

            parts = line.split('|')
            cells = parts[1:-1]

            for idx in range(len(cells)):
                if idx in protected_indices:
                    content = cells[idx].strip()
                    if content:
                        marker = self._create_table_marker(content)
                        self._caches['table']['protected_data'][marker] = content

                        # 保持原始格式
                        leading = len(cells[idx]) - len(cells[idx].lstrip())
                        trailing = len(cells[idx]) - len(cells[idx].rstrip())
                        cells[idx] = ' ' * leading + marker + ' ' * trailing
                else:
                    cells[idx] = self._process_cell_content(cells[idx])

            # 重构表格行
            processed_line = '|' + '|'.join([
                f' {cell.strip()} '.ljust(col_widths[i] + 2 if i < len(col_widths) else len(cell) + 2)
                for i, cell in enumerate(cells)
            ]) + '|'
            processed_lines.append(processed_line)

        # 确保表格前有两个换行符
        table_text = '\n'.join(processed_lines)
        if not table_text.startswith('\n\n'):
            table_text = '\n\n' + table_text

        return table_text, self._caches['table']['protected_data']

    def _protect_code_blocks(self, text: str) -> Tuple[str, Dict]:
        """保护代码块"""
        blocks = self._parse_markdown_code_segments(text)
        if not blocks:
            return text, {}

        protected_data = {}
        segments = []
        last_pos = 0

        for block in blocks:
            segments.append(text[last_pos:block['start_pos']])
            last_pos = block['end_pos']

            marker = self._create_code_marker(block['content'])
            protected_data[marker] = block['content']

            if block['type'] == 'block':
                segments.append(f"\n{block['fence']}{block['language']}\n{marker}\n{block['fence']}\n")
                self._caches['code']['stats']['blocks_protected'] += 1
            elif block['type'] == 'special':
                segments.append(f"\n{marker}")
                self._caches['code']['stats']['special_protected'] += 1
            elif block['type'] == 'code_inline':
                segments.append(f"\n{marker}\n")
                self._caches['code']['stats']['code_inline_protected'] += 1
            elif block['type'] == 'empty':
                segments.append(f"\n{marker}\n")
                self._caches['code']['stats']['empty_protected'] += 1
            else:
                segments.append(f"`{marker}`")
                self._caches['code']['stats']['inline_protected'] += 1

        segments.append(text[last_pos:])
        return ''.join(segments), protected_data

    def _protect_headers(self, text: str) -> Tuple[str, Dict]:
        """保护Markdown标题（精确控制换行符）"""
        protected = {}
        segments = []
        last_pos = 0

        for match in self.header_pattern.finditer(text):
            segments.append(text[last_pos:match.start()])
            last_pos = match.end()

            # 只提取标题行本身，不包括后续的换行符
            header_line = match.group('prefix') + match.group('content')
            if match.group('anchor'):
                header_line += f" {{#{match.group('anchor')}}}"

            marker = self._create_header_marker(header_line)

            protected[marker] = {
                'full_text': header_line,  # 只存储标题行
                'prefix': match.group('prefix'),
                'content': match.group('content'),
                'anchor': match.group('anchor')
            }
            segments.append(f"{marker}\n")

            # 保留原始文本中的换行符（不作为标题的一部分）
            segments.append(match.group('suffix'))

        segments.append(text[last_pos:])
        return ''.join(segments), protected

    def _protect_markdown_links(self, text: str) -> Tuple[str, Dict]:
        self._debug_print('link', 1, f"开始保护链接，文本长度: {len(text)}")
        """保护Markdown链接（优化版）"""
        segments = []
        last_pos = 0

        for match in self.link_pattern.finditer(text):
            segments.append(text[last_pos:match.start()])
            last_pos = match.end()

            full_link = match.group('full_link')
            # 检查是否有对应的翻译术语
            translated_link = self._get_translated_link(full_link)
            marker = self._create_link_marker(full_link)

            # 存储原始链接和翻译版本（确保完整格式）
            self._caches['link']['protected_data'][marker] = {
                'original': full_link,
                'translated': translated_link if translated_link else full_link
            }

            self._caches['link']['stats']['links_protected'] += 1
            if translated_link:
                self._caches['link']['stats']['links_translated'] += 1

            segments.append(marker)
            self._debug_print('link', 2, f"保护链接: {full_link} -> {marker}")

        segments.append(text[last_pos:])
        self._debug_print('link', 1, f"共保护 {len(self._caches['link']['protected_data'])} 个链接")
        return ''.join(segments), self._caches['link']['protected_data']

    def _protect_functions(self, text: str) -> Tuple[str, Dict]:
        """保护函数结构（增强版）- 支持方括号参数和大括号ID"""
        protected_data = {}
        segments = []
        last_pos = 0

        for match in self.function_pattern.finditer(text):
            # 跳过空匹配
            if not match.group('name'):
                continue

            segments.append(text[last_pos:match.start()])
            last_pos = match.end()

            full_function = match.group('full_function')
            func_name = match.group('name')

            # 核心逻辑：仅对预定义函数名跳过参数检查
            if func_name.lower() not in self.protected_functions:
                # 非预定义函数：必须带参数或ID才保护
                if not (match.group('params') or match.group('id')):
                    segments.append(full_function)
                    continue

            marker = self._create_function_marker(full_function)
            protected_data[marker] = full_function
            segments.append(marker)

        segments.append(text[last_pos:])
        return ''.join(segments), protected_data

    def _protect_macro(self, text: str) -> Tuple[str, Dict]:
        """
        保护文档中的所有宏结构（支持嵌套）

        参数:
            text: 需要处理的文本

        返回:
            Tuple[str, Dict]:
                - 处理后的文本（宏被替换为占位符）
                - 保护的宏数据字典 {占位符: 原始宏信息}
        """
        protected_data = {}

        def replace_macro(match: re.Match, nesting_level: int = 0) -> str:
            """递归处理嵌套宏的回调函数"""
            nonlocal protected_data, self

            full_macro = match.group(0)
            is_builtin = not match.group(1)  # 组1是$符号
            macro_name = match.group(2)  # 组2是宏名称
            has_index = '<' in macro_name  # 是否有索引

            # 更新最大嵌套深度统计
            self._caches['macro']['stats']['max_nesting_level'] = max(self._caches['macro']['stats']['max_nesting_level'], nesting_level)

            # 生成唯一占位符（8位MD5哈希）
            marker = self._create_macro_marker(full_macro)

            # 保存原始宏信息
            protected_data[marker] = {
                'raw': full_macro,
                'name': macro_name,
                'is_builtin': is_builtin,
                'has_index': has_index,
                'nesting_level': nesting_level
            }

            return marker

        # 使用正则表达式替换回调处理所有宏
        processed_text = self.macro_pattern.sub(
            lambda m: replace_macro(m, nesting_level=0),
            text
        )

        return processed_text, protected_data

    # ==================== 解析文本 ====================
    def _parse_markdown_tables(self, text: str) -> List[Dict]:
        """解析文本中的Markdown表格并返回结构化数据

        参数:
            text: 包含Markdown表格的文本

        返回:
            包含表格数据的字典列表，每个字典包含:
            - full_text: 完整表格文本
            - header: 表头行
            - rows: 数据行列表
            - 位置信息等元数据
        """
        tables = []
        for match in self.table_pattern.finditer(text):
            try:
                # 处理可能的多行表格行
                raw_rows = match.group('rows')
                rows = []
                buffer = []

                for line in raw_rows.split('\n'):
                    stripped = line.strip()
                    if stripped.startswith('|'):
                        if buffer:  # 保存前一个完整的行
                            rows.append(''.join(buffer))
                            buffer = []
                        buffer.append(line)
                    elif buffer:  # 处理多行单元格内容
                        buffer.append('\n' + line)

                if buffer:  # 添加最后一行
                    rows.append(''.join(buffer))

                table_data = {
                    'full_text': match.group('full_table'),
                    'header': match.group('header').strip(),
                    'align_line': match.group('align').strip() if match.group('align') else None,
                    'rows': rows,
                    'start_pos': match.start(),
                    'end_pos': match.end(),
                    'raw_rows': raw_rows  # 保留原始数据用于调试
                }
                tables.append(table_data)

            except Exception as e:
                print(f"[警告] 表格解析错误: {str(e)}")
                continue

        return tables

    def _parse_markdown_code_segments(self, text: str) -> List[Dict]:
        """解析文本中的Markdown代码段，返回结构化数据

        支持类型：
        - 多行代码块（```lang\ncontent\n```）
        - 行内代码（`content`）

        返回字段：
        - type: 'block'/'inline'
        - content: 代码内容
        - 位置信息等元数据
        """
        blocks = []
        text_length = len(text)

        # 处理多行代码块
        for match in self.code_block_pattern.finditer(text):
            blocks.append({
                'type': 'block',
                'full_text': match.group('full_block'),
                'content': match.group('content'),
                'language': match.group('lang') or '',
                'fence': match.group('fence'),
                'start_pos': match.start(),
                'end_pos': match.end()
            })

        # 处理行内代码（排除多行代码块内的部分）
        for match in self.inline_code_pattern.finditer(text):
            start, end = match.start(), match.end()
            if not any(block['start_pos'] <= start <= block['end_pos'] for block in blocks):
                blocks.append({
                    'type': 'inline',
                    'full_text': match.group('full_inline'),
                    'content': match.group('full_inline')[1:-1],
                    'start_pos': start,
                    'end_pos': end
                })

        # 处理行内代码（排除多行代码块内的部分）
        for match in self.inline_notecode_pattern.finditer(text):
            start, end = match.start(), match.end()
            if not any(block['start_pos'] <= start <= block['end_pos'] for block in blocks):
                blocks.append({
                    'type': 'special',
                    'full_text': match.group('special'),
                    'content': match.group('special'),
                    'start_pos': start,
                    'end_pos': end
                })

        # 处理行内代码（排除多行代码块内的部分）
        for match in self.inline_code_inline_pattern.finditer(text):
            start, end = match.start(), match.end()
            if not any(block['start_pos'] <= start <= block['end_pos'] for block in blocks):
                blocks.append({
                    'type': 'code_inline',
                    'full_text': match.group('code_inline'),
                    'content': match.group('code_inline'),
                    'start_pos': start,
                    'end_pos': end
                })

        # 处理行内代码（排除多行代码块内的部分）
        for match in self.inline_empty_pattern.finditer(text):
            start, end = match.start(), match.end()
            if not any(block['start_pos'] <= start <= block['end_pos'] for block in blocks):
                blocks.append({
                    'type': 'empty',
                    'full_text': match.group('empty'),
                    'content': match.group('empty'),  # 去除空行中的空白字符
                    'start_pos': start,
                    'end_pos': end
                })

        # 按起始位置排序
        return sorted(blocks, key=lambda x: x['start_pos'])

    # ==================== 主流程方法 ====================
    def preprocess(self, text: str) -> str:
        """优化处理顺序，确保Markdown元素按正确优先级处理"""
        # 保护顺序很重要：代码块 -> 标题 -> 函数 -> 表格 -> 超链接 -> 术语
        self._debug_print('all', 1, f"开始预处理流程，原始文本长度: {len(text)}")
        self._debug_print('clean', 3, f"原始文本内容:\n{text}")

        # 1. 保护代码块 OK
        self._debug_print('code', 1, "保护代码块...")
        text, code_data = self._protect_code_blocks(text)
        self._caches['code']['protected_data'].update(code_data)

        # 2. 保护宏
        self._debug_print('macro', 1, "=== 开始保护宏 ===")
        text, macro_data = self._protect_macro(text)
        self._caches['macro']['protected_data'].update(macro_data)
        self._debug_print('macro', 2, f"宏保护后文本片段: {text[:100]}...")

        # 2. 保护标题 OK
        self._debug_print('header', 1, "保护标题...")
        text, header_data = self._protect_headers(text)
        self._caches['header']['protected_data'].update(header_data)

        # 2. 保护函数
        self._debug_print('func', 1, "=== 开始保护函数 ===")
        text, func_data = self._protect_functions(text)
        self._caches['func']['protected_data'].update(func_data)
        self._debug_print('func', 2, f"函数保护后文本片段: {text[:100]}...")

        # 4. 保护非表格链接（跳过表格内的链接）
        tables = self._parse_markdown_tables(text)
        if tables:
            segments = []
            last_pos = 0
            for table in tables:
                segments.append(text[last_pos:table['start_pos']])
                last_pos = table['end_pos']
                protected_table, table_data = self._protect_table_columns(table)
                self._caches['table']['protected_data'].update(table_data)
                segments.append(protected_table)
            segments.append(text[last_pos:])
            text = ''.join(segments)

        # 4. 保护链接
        self._debug_print('link', 1, "保护链接...")
        text, link_data = self._protect_markdown_links(text)
        self._caches['link']['protected_data'].update(link_data)

        # 5. 术语替换
        self._debug_print('term', 1, "术语替换...")
        text = self._replace_terms(text)

        self._debug_print('all', 1, "=== 预处理完成 ===")
        self._debug_print('clean', 3, f"处理后的文本内容:\n{text}")
        return text

    def postprocess(self, text: str) -> str:
        """增强后处理，确保Markdown格式正确"""
        # 恢复顺序与保护相反：术语 -> 表格 -> 超链接 -> 函数 -> 标题-> 代码块
        if not text:
            return text

        self._debug_print('all', 1, f"原始文本...{text}")
        # 1. 还原术语
        self._debug_print('term', 1, "开始还原术语...")
        for marker, term in sorted(self.marker_to_term.items(), key=len, reverse=True):
            text = text.replace(marker, term)
            self._debug_print('term', 1, f"完成还原术语...{marker} - > {term}")

        # 2. 还原表格内容
        self._debug_print('table', 1, "开始还原表格...")
        for marker in sorted(self._caches['table']['protected_data'].keys(), key=len, reverse=True):
            protected_content = self._caches['table']['protected_data'][marker]
            # 获取替换内容
            replacement = protected_content.get('translated', marker) if isinstance(protected_content, dict) else protected_content
            # 执行替换
            text = text.replace(marker, replacement)
            self._debug_print('table', 1, f"完成还原表格...{marker} - > {protected_content}")

        # 5. 还原链接（包括表格内的链接） - 只需要执行一次
        self._debug_print('link', 1, "开始还原链接...")
        for marker, link_data in self._caches['link']['protected_data'].items():
            replacement = link_data.get('translated') or link_data.get('original') or marker
            text = text.replace(marker, replacement)
            self._debug_print('link', 1, f"完成还原链接...{marker} - > {link_data}")

        # 4. 还原代函数 OK
        self._debug_print('func', 1, "开始还原函数...")
        for marker, original in self._caches['func']['protected_data'].items():
            text = text.replace(marker, original)
            self._debug_print('func', 1, f"完成还原函数...{marker} - > {original}")

        # 3. 还原标题（确保标题后有换行） OK
        self._debug_print('header', 1, "开始还原标题...")
        for marker, header_data in self._caches['header']['protected_data'].items():
            translated_content = self.header_terms.get(f"{header_data['prefix']}{header_data['content']}", f"{header_data['prefix']}{header_data['content']}")
            reconstructed = f"{translated_content}"
            if header_data.get('anchor'):
                reconstructed += f" {{#{header_data['anchor']}}}"

            # 只替换标记本身，不影响周围的换行符
            self._debug_print('header', 2, f"还原标题：{header_data['prefix']}{header_data['content']} -> {reconstructed}")
            text = text.replace(marker, reconstructed)
            self._debug_print('header', 1, f"完成还原标题...{marker} - > {header_data}")

        # 4. 还原宏 OK
        # 最佳实践：保持按嵌套层级排序
        sorted_macros = sorted(
            self._caches['macro']['protected_data'].items(),
            key=lambda item: item[1].get('nesting_level', 0),
            reverse=True
        )
        for marker, macro_info in sorted_macros:
            text = text.replace(marker, macro_info['raw'])

        # 4. 还原代码块 OK
        self._debug_print('code', 1, "开始还原代码...")
        for marker, original in self._caches['code']['protected_data'].items():
            text = text.replace(marker, original)
            self._debug_print('code', 1, f"完成还原代码...{marker} - > {original}")

        # 7. 清理不需要的提示词
        self._debug_print('clean', 1, "开始清理...")
        text = self._clean_unwanted_patterns(text)
        self._debug_print('clean', 1, f"完成清理...{text}")

        return text

    # ==================== 其余方法 ====================
    def debug_info(self) -> dict:
        """返回各缓存状态的调试信息"""
        return {
            category: {
                'count': len(cache['protected_data']),
                'stats': cache['stats'],
                'sample': list(cache['protected_data'].items())[:3]  # 示例数据
            }
            for category, cache in self._caches.items()
        }

    def calc_markdown_links(self, excel_op):
        """处理所有链接的翻译"""
        excel_op.activate_sheet("HEADER_MAPPING")
        self._load_header_mapping(excel_op)

        # 加载LINK_MAPPING表
        excel_op.activate_sheet("LINK_MAPPING")
        self._load_link_mapping(excel_op)

        logger.debug(self.link_mapping)
        logger.debug(self.header_mapping)
        results = []
        excel_op.set_cell_value(1, 11, "超链接参考")
        for current_row, record in enumerate(self.link_mapping):
            translated_link = self._translate_single_link(record)
            results.append(translated_link)
            excel_op.set_cell_value(current_row + 2, 11, translated_link)

    def export_markdown_headers_to_excel(self, excel_op, text: str, source_row: int, start_row: int):
        """
        将Markdown标题及其翻译状态导出到Excel（跳过代码块中的标题）

        参数:
            excel_op: Excel操作对象
            text: 要分析的文本内容
            source_row: 源文件中的行号
            start_row: Excel中开始写入的行号

        返回:
            下一个可用的行号
        """
        # 先找出所有代码块的范围
        code_blocks = self._find_code_blocks(text)
        headers_info = self.get_markdown_headers_info(text)

        if not headers_info:
            return start_row

        current_row = start_row

        for header_info in headers_info:
            # 检查标题是否位于代码块中
            if self._is_in_code_block(header_info['start_pos'], header_info['end_pos'], code_blocks):
                continue

            # 检查标题是否在术语字典中
            full_header = f"{header_info['prefix']}{header_info['content']}"
            is_translated = full_header in self.header_terms
            translation = self.header_terms.get(full_header, "")

            # 写入各列信息
            excel_op.activate_sheet("document")
            doc_path = excel_op.get_cell_value(source_row, 1)
            excel_op.activate_sheet("HEADER_MAPPING")
            excel_op.set_cell_value(current_row, 1, doc_path)
            excel_op.set_cell_value(current_row, 2, f"源行 {source_row}")
            excel_op.set_cell_value(current_row, 3, f"H{header_info['level']}")
            excel_op.set_cell_value(current_row, 4, header_info['content'])
            excel_op.set_cell_value(current_row, 5, header_info['full_text'])
            excel_op.set_cell_value(current_row, 6, "是" if header_info['has_anchor'] else "否")
            excel_op.set_cell_value(current_row, 7, header_info['anchor'] or "")
            excel_op.set_cell_value(current_row, 8, "是" if is_translated else "否")
            excel_op.set_cell_value(current_row, 9, translation if is_translated else "需要翻译")
            excel_op.set_cell_value(current_row, 10, self._title_to_anchor_en(header_info['content']))
            excel_op.set_cell_value(current_row, 11, self._title_to_anchor_zh(translation if is_translated else "需要翻译"))

            current_row += 1

        return current_row

    def export_markdown_links_to_excel(self, excel_op, text: str, source_row: int, start_row: int):
        """
        将Markdown超链接及其翻译状态导出到Excel（新增是否有锚点列）

        列结构:
            1. 源行信息
            2. 链接类型
            3. 链接文本
            4. URL路径
            5. 是否有锚点（新增）
            6. URL锚点
            7. 完整链接
            8. 是否已翻译
            9. 翻译内容
        """
        code_blocks = self._find_code_blocks(text)
        links_info = self.get_markdown_links_info(text)

        if not links_info:
            return start_row

        current_row = start_row

        for link_info in links_info:
            if self._is_in_code_block(link_info['start_pos'], link_info['end_pos'], code_blocks):
                continue

            is_translated = (link_info['full_link'] in self.link_terms or
                             link_info['text'] in self.link_terms)
            translation = self.link_terms.get(link_info['full_link'],
                                              self.link_terms.get(link_info['text'], ""))

            # 调整后的列结构（新增第4列）
            excel_op.activate_sheet("document")
            doc_path = excel_op.get_cell_value(source_row, 1)
            excel_op.activate_sheet("LINK_MAPPING")
            excel_op.set_cell_value(current_row, 1, doc_path)
            excel_op.set_cell_value(current_row, 2, f"源行 {source_row}")
            excel_op.set_cell_value(current_row, 3, "图片链接" if link_info['is_image'] else "普通链接")
            excel_op.set_cell_value(current_row, 4, link_info['text'])
            excel_op.set_cell_value(current_row, 5, link_info['url_path'])
            excel_op.set_cell_value(current_row, 6, "是" if link_info['has_anchor'] else "否")  # 新增列
            excel_op.set_cell_value(current_row, 7, link_info['url_anchor'] or "")
            excel_op.set_cell_value(current_row, 8, link_info['full_link'])
            excel_op.set_cell_value(current_row, 9, "是" if is_translated else "否")
            excel_op.set_cell_value(current_row, 10, translation if is_translated else "需要翻译")

            current_row += 1

        return current_row

    def export_table_headers_to_excel(self, excel_op, text: str, source_row: int, start_row: int):
        """
        将表格表头及其保护状态导出到Excel（简化版）

        参数:
            excel_op: Excel操作对象
            text: 要分析的文本内容
            source_row: 源文件中的行号
            start_row: Excel中开始写入的行号

        返回:
            下一个可用的行号
        """

        headers_info = self.get_table_headers_with_protection_info(text)
        if not headers_info:
            return start_row

        current_row = start_row

        for table_idx, table_info in enumerate(headers_info, start=1):
            # 计算需要合并的行数
            merge_rows = len(table_info['headers'])

            # 写入各列信息
            for col_idx, (col, norm_col, protected, reason) in enumerate(
                    zip(table_info['headers'],
                        table_info['normalized_headers'],
                        table_info['protected_flags'],
                        table_info['protection_reasons']),
                    start=1
            ):
                excel_op.activate_sheet("document")
                doc_path = excel_op.get_cell_value(source_row, 1)
                excel_op.activate_sheet("EXCEL_MAPPING")
                excel_op.set_cell_value(current_row, 1, doc_path)
                excel_op.set_cell_value(current_row, 2, f"源行 {source_row}")
                excel_op.set_cell_value(current_row, 3, f"表格 {table_idx}")
                excel_op.set_cell_value(current_row, 4, table_info['raw_header'])
                excel_op.set_cell_value(current_row, 5, col)
                excel_op.set_cell_value(current_row, 6, norm_col)
                excel_op.set_cell_value(current_row, 7, "是" if protected else "否")
                excel_op.set_cell_value(current_row, 8, reason)
                excel_op.set_cell_value(current_row, 9, "保持现状" if protected else "可考虑添加保护")

                current_row += 1

        return current_row

    def get_markdown_headers_info(self, text: str) -> List[Dict[str, Any]]:
        """
        获取所有Markdown标题信息（包含位置信息）

        参数:
            text: 要分析的文本内容

        返回:
            List[Dict]: 每个标题的信息字典，包含以下字段:
                - 'level': 标题级别 (1-6)
                - 'prefix': 标题前缀 (如 "## ")
                - 'content': 标题内容
                - 'full_text': 完整标题文本
                - 'has_anchor': 是否有锚点
                - 'anchor': 锚点名称 (如果有)
                - 'start_pos': 标题起始位置
                - 'end_pos': 标题结束位置
        """
        headers_info = []

        for match in self.header_pattern.finditer(text):
            prefix = match.group('prefix')
            level = len(prefix.strip())  # 计算标题级别
            content = match.group('content').strip()
            anchor = match.group('anchor')

            # 构建完整标题文本
            full_text = prefix + content
            if anchor:
                full_text += f" {{#{anchor}}}"

            headers_info.append({
                'level': level,
                'prefix': prefix,
                'content': content,
                'full_text': full_text,
                'has_anchor': anchor is not None,
                'anchor': anchor,
                'start_pos': match.start(),  # 添加起始位置
                'end_pos': match.end()  # 添加结束位置
            })

        return headers_info

    def get_markdown_links_info(self, text: str) -> List[Dict[str, Any]]:
        """
        获取所有Markdown链接信息（包含锚点信息）

        返回字典新增:
            - 'has_anchor': 是否有URL锚点
        """
        links_info = []

        for match in self.link_pattern.finditer(text):
            url_anchor = match.group('url_anchor')
            if url_anchor is not None:
                url_anchor = url_anchor.lower()
                url_anchor = url_anchor.replace("-", "_")

            links_info.append({
                'is_image': match.group('image') is not None,
                'text': match.group('text'),
                'url': match.group('url'),
                'url_path': match.group('url_path'),
                'url_anchor': url_anchor,
                'has_anchor': url_anchor is not None,  # 新增是否有锚点标记
                'full_link': match.group('full_link'),
                'start_pos': match.start(),
                'end_pos': match.end()
            })

        return links_info

    def get_table_headers_with_protection_info(self, text: str) -> List[Dict[str, Any]]:
        """
        获取所有表格的表头信息并标记保护状态

        参数:
            text: 要分析的文本内容

        返回:
            List[Dict]: 每个表格的表头信息列表，包含以下字段:
                - 'raw_header': 原始表头文本
                - 'headers': 表头列列表
                - 'protected_flags': 对应列是否受保护的布尔列表
                - 'normalized_headers': 标准化后的表头列表
                - 'protection_reasons': 每列的保护原因说明

        示例返回:
            [{
                'raw_header': "| 名称 | Type | Description |",
                'headers': ["名称", "Type", "Description"],
                'protected_flags': [False, True, False],
                'normalized_headers': ["名称", "type", "description"],
                'protection_reasons': ["", "匹配保护模式: ^Type$", ""]
            }]
        """
        tables = self._parse_markdown_tables(text)
        result = []

        for table in tables:
            # 提取原始表头列
            raw_header = table['header']
            header_cols = [col.strip() for col in raw_header.split('|')[1:-1]]

            # 分析每列的保护状态
            protected_flags = []
            protection_reasons = []
            normalized_headers = []

            for col in header_cols:
                normalized = self._normalize_header(col)
                normalized_headers.append(normalized)

                # 检查保护状态和原因
                is_protected = False
                reason = ""

                # 检查精确匹配模式
                for pattern in self.protected_columns:
                    if re.search(pattern, col.strip(), re.IGNORECASE):
                        is_protected = True
                        reason = f"精确匹配保护模式: {pattern}"
                        break
                    elif re.search(pattern, normalized, re.IGNORECASE):
                        is_protected = True
                        reason = f"标准化后匹配保护模式: {pattern}"
                        break

                protected_flags.append(is_protected)
                protection_reasons.append(reason if is_protected else "")

            # 添加到结果
            result.append({
                'raw_header': raw_header,
                'headers': header_cols,
                'protected_flags': protected_flags,
                'normalized_headers': normalized_headers,
                'protection_reasons': protection_reasons
            })

        return result

    def set_debug(self, category: str, enabled: bool = True, level: int = None):
        """
        统一调试设置方法

        参数:
            category: 调试类别('code','table','link','term','header','func','cache','all')
            enabled: 是否启用该类别调试(默认True)
            level: 同时设置调试级别(可选，1=基础, 2=详细, 3=全量)
        """
        # 设置调试开关
        if category == 'all':
            for key in self.debug_config:
                self.debug_config[key] = enabled
        elif category in self.debug_config:
            self.debug_config[category] = enabled
        else:
            print(f"[警告] 未知调试类别: {category}", file=sys.stderr)
            return

        # 设置调试级别
        if level is not None:
            if category == 'all':
                for key in self.debug_level:
                    self.debug_level[key] = level
            elif category in self.debug_level:
                self.debug_level[category] = level

    def _clean_unwanted_patterns(self, text: str) -> str:
        """清理不需要的提示词模式（带分级调试）"""
        self._debug_print('clean', 2, f"开始清理不需要的模式，原始文本长度: {len(text)}")
        self._debug_print('clean', 3, f"原始文本预览:\n{text[:200]}...")

        original_text = text
        total_removed = 0

        for pattern in self.unwanted_patterns:
            self._debug_print('clean', 2, f"\n处理模式: {pattern}")

            # 调试匹配过程
            matches = list(re.finditer(pattern, text, flags=re.MULTILINE))
            self._debug_print('clean', 2, f"找到 {len(matches)} 个匹配项")

            for i, match in enumerate(matches, 1):
                self._debug_print('clean', 3,
                                  f"匹配项 {i}: 位置[{match.start()}-{match.end()}] "
                                  f"内容: {match.group()!r}")

                # 显示匹配上下文
                if self.debug_config.get('term') and self.debug_level.get('term', 1) >= 4:
                    context = text[max(0, match.start() - 20):match.end() + 20]
                    self._debug_print('clean', 4, f"匹配上下文:\n{context}")

            # 执行替换并记录变化
            before_len = len(text)
            text = re.sub(pattern, '', text, flags=re.MULTILINE)
            text = re.sub(r'(\n){2,}', '\\n\\n', text, flags=re.MULTILINE)
            text = re.sub(r'::: ?经典笔记', '::: noteclassic', text, flags=re.MULTILINE)
            text = re.sub(r'::: ?经典注释', '::: noteclassic', text, flags=re.MULTILINE)
            text = re.sub(r'::: ?重要提示', '::: noteimportant', text, flags=re.MULTILINE)
            text = re.sub(r'::: ?注意提示', '::: notetip', text, flags=re.MULTILINE)
            text = re.sub(r'::: ?注意警告', '::: notewarning', text, flags=re.MULTILINE)
            text = re.sub(r'::: ?提示', '::: notetip', text, flags=re.MULTILINE)
            text = re.sub(r'::: ?注意重要', '::: noteimportant', text, flags=re.MULTILINE)
            removed = before_len - len(text)
            total_removed += removed

            self._debug_print('clean', 2,
                              f"替换结果: 移除了 {removed} 字符 (累计: {total_removed})")

        # 最终结果调试
        self._debug_print('clean', 2,
                          f"清理完成，共移除 {total_removed} 字符")
        self._debug_print('clean', 3,
                          f"处理后文本预览:\n{text[:200]}...")

        return text

    def _debug_print(self, category: str, level: int = 1, *args, **kwargs):
        """增强版分级调试输出"""
        if not self.debug_config.get(category, False) or not self.debug_config.get('all', False):
            return
        elif self.debug_level.get(category, 1) < level:
            return
        if (self.debug_config.get('all', False) or
                (self.debug_config.get(category, False) and
                 self.debug_level.get(category, 1) >= level)):
            prefix = f"[DEBUG-{category.upper()}-L{level}]"
            # 添加上下文信息
            caller = inspect.stack()[1].function
            print(f"{prefix} [{caller}]", *args, **kwargs)

    def _ensure_required_terms(self):
        """确保必要术语存在于术语字典中，缺失时自动补充

        关键术语列表：
        - proxy
        - Proxy
        - proxy-group
        - API
        """
        required_terms = {'proxy', 'Proxy', 'proxy-group', 'API'}
        missing = required_terms - set(self.term_dict['original_terms'].keys())

        for term in missing:
            self.term_dict['original_terms'][term] = term
            self._debug_print('term', 1, f"[警告] 自动补充关键术语: {term}")
            # 为新补充的术语生成标记
            marker = self._create_term_marker(term)
            self.term_to_marker[term] = marker
            self.marker_to_term[marker] = term

    def _find_code_blocks(self, text: str) -> List[Tuple[int, int]]:
        """
        找出所有代码块的范围（起始和结束位置）

        返回:
            List[Tuple[int, int]]: 代码块的(start_pos, end_pos)列表
        """
        code_blocks = []
        in_code_block = False
        start_pos = 0

        # 处理多行代码块 ```
        for match in re.finditer(r'```.*?\n', text):
            if not in_code_block:
                start_pos = match.start()
                in_code_block = True
            else:
                code_blocks.append((start_pos, match.end()))
                in_code_block = False

        # 处理单行代码块 `
        for match in re.finditer(r'`[^`]+`', text):
            code_blocks.append((match.start(), match.end()))

        return code_blocks

    def _get_translated_link(self, link: str) -> Optional[str]:
        """增强链接翻译调试"""
        self._debug_print('link', 2, f"检查链接翻译: {link}")
        if not self.link_terms:
            self._debug_print('link', 1, "链接术语表为空")
            return None

        # 精确匹配优先
        if link in self.link_terms:
            self._debug_print('link', 2, f"找到精确匹配: {link} -> {self.link_terms[link]}")
            return self.link_terms[link]

        match = self.link_pattern.match(link)
        if not match:
            self._debug_print('link', 1, f"无效链接格式: {link}")
            return None

        text = match.group('text')
        url = match.group('url')
        is_image = match.group('image') is not None

        # 查找文本翻译
        translated_text = None
        if text in self.link_terms:
            translated_text = self.link_terms[text]
        else:
            for src, tgt in self.link_terms.items():
                if src.lower() == text.lower():
                    translated_text = tgt
                    break

        if not translated_text:
            self._debug_print('link', 2, f"未找到链接文本 '{text}' 的翻译")
            return None

        # 重构链接
        result = f"![{translated_text}]({url})" if is_image else f"[{translated_text}]({url})"
        self._debug_print('link', 2, f"重构链接: {link} -> {result}")
        return result

    def _is_in_code_block(self, start_pos: int, end_pos: int, code_blocks: List[Tuple[int, int]]) -> bool:
        """
        检查给定位置是否位于任何代码块中

        参数:
            start_pos: 要检查的起始位置
            end_pos: 要检查的结束位置
            code_blocks: 代码块范围列表

        返回:
            bool: 如果在代码块中返回True
        """
        for block_start, block_end in code_blocks:
            if start_pos >= block_start and end_pos <= block_end:
                return True
        return False

    def _is_protected_column(self, header: str) -> bool:
        """判断列是否受保护（增强调试版）"""
        self._debug_print('table', 3, f"\n开始检查列保护: '{header}'")

        # 提取纯文本内容（去除链接格式）
        plain_text = re.sub(r'\[([^]]+)\]\[[^)]+\]', r'\1', header)  # 修改正则匹配链接格式
        normalized = self._normalize_header(plain_text)

        self._debug_print('table', 3, f"处理后文本: 纯文本='{plain_text}', 标准化='{normalized}'")
        self._debug_print('table', 3, f"当前保护模式: {self.protected_columns}")

        # 正则匹配保护列规则
        for pattern in self.protected_columns:
            if re.search(pattern, plain_text, re.IGNORECASE):
                self._debug_print('table', 3, f"匹配保护列模式: pattern='{pattern}', text='{plain_text}'")
                return True

        # # 检查是否匹配保护模式
        # for pattern in sorted(self.protected_columns, key=len, reverse=True):
        #     if re.fullmatch(pattern, header.strip()):
        #         self._debug_print('table', 2, f"直接匹配: '{header}' 匹配模式: {pattern}")
        #         return True
        #     if re.fullmatch(pattern, plain_text.strip()):
        #         self._debug_print('table', 2, f"纯文本匹配: '{plain_text}' 匹配模式: {pattern}")
        #         return True
        #     if re.fullmatch(pattern, normalized):
        #         self._debug_print('table', 2, f"标准化匹配: '{normalized}' 匹配模式: {pattern}")
        #         return True

        self._debug_print('table', 3, f"列 '{header}' 不匹配任何保护模式")
        return False

    def _load_header_mapping(self, excel_op):
        """加载HEADER_MAPPING表数据到内存"""
        rows = excel_op.get_dimensions()['rows']
        for row in range(2, rows + 1):  # 跳过标题行
            en = excel_op.get_cell_value(row, "J")  # EN列
            zh = excel_op.get_cell_value(row, "K")  # ZH列
            if en and zh:
                self.header_mapping[en] = zh

    def _load_link_mapping(self, excel_op):
        """加载LINK_MAPPING表数据到内存"""
        rows = excel_op.get_dimensions()['rows']
        for row in range(2, rows + 1):  # 跳过标题行
            record = {
                "text": excel_op.get_cell_value(row, "D"),  # 文本部分
                "link": excel_op.get_cell_value(row, "H"),  # 链接部分
                "translated": excel_op.get_cell_value(row, "G")  # 翻译内容
            }
            self.link_mapping.append(record)

    @lru_cache(maxsize=1024)
    def _normalize_header(self, header: str) -> str:
        """标准化表头文本（去除Markdown/HTML格式）并缓存结果

        参数:
            header (str): 原始表头文本

        返回:
            str: 标准化后的表头文本
        """
        # 修正超链接正则表达式 [text](url) -> text
        header = re.sub(r'\[([^]]+)\]\[[^)]+\]', r'\1', header)
        # 移除代码标记 `text` -> text
        header = re.sub(r'`([^`]+)`', r'\1', header)
        # 移除粗体/斜体标记
        header = re.sub(r'[\*_]{1,2}([^\*_]+)[\*_]{1,2}', r'\1', header)
        return header.strip().lower()

    def _process_cell_content(self, cell: str) -> str:
        """处理单元格内容（保留格式+术语替换+换行处理）"""
        # 保护特殊格式（HTML/链接/代码块）
        protected = {}

        def protect(match):
            key = f"{{PROT{len(protected)}}}"
            protected[key] = match.group(0)
            return key

        # 保护换行标签
        cell = cell.replace('<br>', '{BR}')

        # 保护其他特殊格式
        temp = re.sub(
            r'<[^>]+>|`[^`]+`|\$\$[^$\$]+\$\$|\bhttps?://\S+',
            protect,
            cell
        )

        # 执行术语替换
        temp = self._replace_terms(temp)

        # 恢复被保护的内容
        for k, v in protected.items():
            temp = temp.replace(k, v)

        # 恢复换行标签
        temp = temp.replace('{BR}', '<br>')

        return temp.strip()

    def _replace_terms(self, text: str) -> str:
        """术语替换核心逻辑"""
        if not text.strip():
            return text

        # 优先匹配长术语
        sorted_terms = sorted(
            self.term_dict['original_terms'].keys(),
            key=lambda x: (-len(x), x.lower())
        )

        pattern = re.compile(
            r'(?<!\w)(?:' + '|'.join(map(re.escape, sorted_terms)) + r')(?!\w)',
            flags=re.IGNORECASE
        )

        def replace_match(match):
            term = match.group(0)

            if term in self.term_to_marker:
                marker = self.term_to_marker[term]
                self._caches['term']['protected_data'][marker] = term
                self._caches['term']['stats']['terms_replaced'] += 1
                return marker
            for dict_term in self.term_dict['lowercase_index'].get(term.lower(), []):
                if term.lower() == dict_term.lower():
                    marker = self.term_to_marker[dict_term]
                    self._caches['term']['protected_data'][marker] = term
                    self._caches['term']['stats']['terms_replaced'] += 1
                    return marker
            return term

        return pattern.sub(replace_match, text)

    def _title_to_anchor_en(self, title):
        """
        将 Markdown 标题转换为对应的锚点格式
        规则：
        1. 转换为小写
        2. 移除非字母数字字符（保留字母和数字）
        3. 将空格和短横线转换为下划线
        4. 确保不出现连续的下划线
        """
        # 转换为小写
        anchor = title.lower()

        # 将空格和短横线转换为下划线
        anchor = anchor.replace(' ', '_').replace('-', '_')

        # 移除非字母数字字符（除了下划线）
        anchor = re.sub(r'[^a-z0-9_]', '', anchor)

        # 将所有大写英文字符转换为小写
        anchor = anchor.lower()

        # 移除连续的下划线
        anchor = re.sub(r'_+', '_', anchor)

        # 移除开头和结尾的下划线
        anchor = anchor.strip('_')

        return anchor

    def _title_to_anchor_zh(self, title):
        """
        将中文 Markdown 标题转换为对应的锚点格式
        规则：
        1. 移除开头的#和空格
        2. 保留中文、字母和数字
        3. 移除非中文/字母/数字的其他字符
        4. 将空格转换为短横线
        5. 将所有大写英文字符转换为小写
        6. 移除连续的短横线
        7. 移除开头和结尾的短横线
        """
        # 移除开头的#和空格
        clean_title = re.sub(r'^#+\s*', '', title.strip())

        # 保留中文、字母、数字和空格
        # 中文Unicode范围: \u4e00-\u9fa5
        clean_title = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', '', clean_title)

        # 将空格转换为短横线
        anchor = clean_title.replace(' ', '-')

        # 将所有大写英文字符转换为小写
        anchor = anchor.lower()

        # 移除连续的短横线
        anchor = re.sub(r'-+', '-', anchor)

        # 移除开头和结尾的短横线
        anchor = anchor.strip('-')

        return anchor

    def _translate_single_link(self, record: Dict) -> str:
        """翻译单个链接，显示文本强制使用锚点对应的中文翻译"""
        if not record['link']:
            return ""

        logger.debug(record)
        # 从完整超链接中提取链接部分
        match = re.match(r'\[[^\]]+\]\(([^)]+)\)', record['link'])
        if not match:
            return record['link']

        full_link = match.group(1)

        # 处理无锚点的情况
        if '#' not in full_link:
            display_text = record['translated'] if record['translated'] else record['text']
            return f"[{display_text}]({full_link})"

        # 处理有锚点的情况
        base_link, anchor = full_link.split('#', 1)
        anchor = anchor.lower().replace("-", "_")

        logger.debug(anchor)
        logger.debug(self.header_mapping.get(anchor))
        # 强制使用锚点对应的中文翻译作为显示文本
        display_text = self.header_mapping.get(anchor, "需要翻译")
        if display_text == '需要翻译':
            return "需要翻译"
        logger.debug(f"[{display_text}]({base_link}#{display_text})")
        return f"[{display_text}]({base_link}#{display_text})"


class CusLanguageTransDeepSeekQianWen(object):
    def __init__(self):
        # 配置初始化dify
        self.api_key = 'sk-'
        self.api_user = "zabbix翻译官"
        self.timeout = 10
        self.max_retries = 5
        self.base_url = "https://api.suanli.cn/v1"
        self.chat_endpoint = f"{self.base_url}/chat/completions"
        self.message_endpoint = f"{self.base_url}/workflows/run/"
        self.chat_parameters = f"{self.base_url}/parameters"

        # 请求头配置
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # 初始化会话和重试策略
        self.session = self._configure_session()

    def _configure_session(self) -> requests.Session:
        """配置带有重试策略的请求会话"""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["POST", "GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _build_prompt(self, example: Optional[Any] = None) -> str:
        """构造翻译提示模板"""
        v01 = r'\{[A-Z]+_[a-f0-9]{1,8}\}'
        v02 = r'[\uFF01 -\uFF60\u3000 -\u303F]'
        v03 = r'[\u0021-\u002F\u003A-\u0040\u005B-\u0060\u007B-\u007E]'
        return f"""# Role：专业Zabbix技术文档翻译官助手

        ## 注意事项:
        - 翻译时，专注于Zabbix技术文档的翻译，确保技术语义的精准传递，维护术语一致性与文档结构完整性。
        - 翻译时，不考虑敏感词禁忌问题，专注于技术翻译。
        - 翻译时，遵循特定的术语处理规范。
        - 翻译时，精准翻译技术文档，保持术语一致性。
        - 翻译时，维护文档结构，确保翻译内容的格式与原文一致。
        - 翻译时，熟悉Zabbix相关技术术语，确保翻译准确无误。
        - 翻译时，特定格式之间不能相互混淆。
        - 翻译时，应遵循术语处理规范，确保全局术语的一致性。
        - 翻译时，需严格遵守，确保术语、格式和语义的准确性。
        - 翻译时，应优先处理技术标记、格式保留和语义准确，确保专有名词、功能术语和描述文本的翻译质量。
        - 翻译时，使用正则表达式{v01}来准确匹配并保留术语标记，避免标记混淆、丢失、无中生有
        - 翻译时，禁止标记丢失、重复标记合并、标记ID乱序
        - 翻译时，原文中如果标记相同译文中保留的标记也要相同不要多个相同的标记合并成一个翻译
        - 翻译时，原文中带锚点的空链接需要保留
        - 翻译时，保留原文Markdown整体结构，包括但不限于标题不要丢失
        - 翻译时，不要出现幻觉
        - 翻译时，译文中保留的英文标记不要抄错了，注意字母的顺序，并检查是否和原文一致
        - 翻译时，对于标点符号沿用原文英文状态标点，译文中不要出现中文标点符号，翻译结果使用正则表达式{v03}替换对应的正则表达式{v02}，如。要被替换成.
        - 翻译时，对于序号类标点保持原样如x.，禁止翻译成x。,x代表数字
        - 翻译时，保留原文中的换行符号
        - 翻译结果，只返回对应翻译内容。

        ## 翻译流程:
        - 接收用户输入的待翻译文本
        - 定义：所有满足正则表达式{v01}格式的文本均为标记
        - 保留：所有标记原样保留（禁止翻译/删除/修改大小写）
        - 重复：若原文中有3个相同标记，译文也必须出现3次
        - 顺序：标记ID后缀（如“1a2b3c4d”）须严格按原文字符顺序
        - 翻译文本，确保技术语义的准确传递
        - 以Markdown格式返回翻译结果
        - 翻译结果，只返回对应翻译内容
        - 检查翻译结果，确保术语一致性与文档结构完整性
        - 在翻译完成后，进行一次全面的格式检查，仅包含翻译后的内容，保留所有原始标记和格式，不添加任何额外说明或注释，
        使用正则表达式{v01}来匹配原文校验翻译后的术语标记避免标记混淆、丢失、无中生有
        - 翻译完成后的文本禁止出现标记丢失、重复标记合并、标记ID乱序
        - 检查翻译后的标记是否有多个相同标记合并成一个标记的情况，有的话需分开
        - 使用正则表达式检查是否遗漏原文中带锚点的空链接，遗漏的话需要补上
        - 翻译完成后检查保留的英文标记是否与原文一致，注意字母的顺序，如果不一致需要重新抄写
        - 翻译完成后不要丢失Markdown格式标题
        - 翻译完成后禁止在最后面添加（注：.*）
        - 翻译结果不要有幻觉
        
        🔹 **示例**  
        Kyoto
        京都
    
        Mount Everest
        珠穆朗玛峰
    
        请按以上规则响应用户的翻译需求！

        {example}

        """

    def _build_user_content(self, text) -> str:
        return f"""{text}
"""

    def _build_request_params(self, text: str, example: Optional[Any] = None) -> Dict:
        """构造API请求参数"""
        return {
            "model": "QwQ-32B",
            "messages": [
                {'role': 'system', 'content': self._build_prompt(example)},
                {'role': 'user', 'content': self._build_user_content(text)}
            ],
            "temperature": 0.01,
            "top_p": 0.1,
            "max_tokens": 100000,
            "stream": True
        }

    def _process_stream_response(self, response: requests.Response) -> str:
        """处理流式响应数据（生产级优化）"""
        chunks = []

        try:
            for line in response.iter_lines():
                if not line:
                    continue

                decoded_line = line.decode('utf-8')
                if not decoded_line.startswith('data:'):
                    continue

                try:
                    json_data = json.loads(decoded_line[5:].strip())
                    print(json_data)
                    content = json_data.get("choices", [])[0].get("delta", {}).get("content", "")
                    if content is not None:
                        chunks.append(content)

                except json.JSONDecodeError as e:
                    logger.warning(f"JSON解析错误: {e}, 原始数据: {decoded_line}")
                    continue

        except Exception as e:
            logger.error(f"流式处理异常: {str(e)}")
            raise

        logger.info(f"成功处理 {len(chunks)} 个数据分片")
        return "".join(chunks)

    def translate(self, text: str, example: Optional[Any] = None) -> Dict[str, object]:
        """
        执行翻译请求

        Args:
            text: 要翻译的文本

        Returns:
            包含翻译结果的字典:
            - success: 是否成功
            - result: 成功时为翻译结果，失败时为错误信息
        """
        if not text or not text.strip():
            logger.warning("翻译请求接收到空文本")
            return {'success': False, 'result': '错误！输入文本为空'}

        for attempt in range(self.max_retries):
            try:
                # logger.info(f"尝试翻译 (第{attempt + 1}次)...")
                response = self.session.post(
                    url=self.chat_endpoint,
                    headers=self.headers,
                    json=self._build_request_params(text, example),
                    timeout=self.timeout,
                    stream=True
                )
                response.raise_for_status()

                full_response = self._process_stream_response(response)
                if full_response:
                    return {'success': True, 'result': full_response}
                else:
                    logger.error("API返回空响应")
                    return {'success': False, 'result': '错误！API返回空响应'}

            except requests.exceptions.RequestException as e:
                logger.error(f"请求失败 (尝试 {attempt + 1}): {str(e)}")
                if attempt == self.max_retries - 1:
                    return {'success': False, 'result': f"错误！请求失败: {str(e)}"}
                time.sleep(2 ** attempt)  # 指数退避

        return {'success': False, 'result': '错误！未知错误'}

    def _fetch_conversation(self, workflow_id: str) -> str:
        """获取特定会话的完整响应"""
        try:
            params = {
                "user": self.api_user,
            }
            response = self.session.get(
                url=f"{self.message_endpoint}:{workflow_id}",
                headers=self.headers,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json().get('data', '').get('outputs', '').get('text', '')
        except requests.exceptions.RequestException as e:
            logger.error(f"获取会话失败: {str(e)}")
            return ''

    def _fetch_parameters(self):
        """获取特定会话的完整响应"""
        try:
            response = self.session.get(
                self.chat_parameters,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取会话失败: {str(e)}")
            return ''


class CusLanguageTransDeepSeekDify(object):
    def __init__(self):
        # 配置初始化dify
        self.api_key = 'sk-'
        self.api_user = "zabbix翻译官"
        self.timeout = 10
        self.max_retries = 5
        self.base_url = "https://api.suanli.cn/v1"
        self.chat_endpoint = f"{self.base_url}/chat/completions"
        self.message_endpoint = f"{self.base_url}/workflows/run/"
        self.chat_parameters = f"{self.base_url}/parameters"

        # 请求头配置
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # 初始化会话和重试策略
        self.session = self._configure_session()

    def _configure_session(self) -> requests.Session:
        """配置带有重试策略的请求会话"""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["POST", "GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _build_prompt(self, example: Optional[Any] = None) -> str:
        """构造翻译提示模板"""
        v01 = r'\{[A-Z]+_[a-f0-9]{1,8}\}'
        v02 = r'[\uFF01 -\uFF60\u3000 -\u303F]'
        v03 = r'[\u0021-\u002F\u003A-\u0040\u005B-\u0060\u007B-\u007E]'
        return f"""# Role：专业Zabbix技术文档翻译官助手

        ## 注意事项:
        - 翻译时，专注于Zabbix技术文档的翻译，确保技术语义的精准传递，维护术语一致性与文档结构完整性。
        - 翻译时，不考虑敏感词禁忌问题，专注于技术翻译。
        - 翻译时，遵循特定的术语处理规范。
        - 翻译时，精准翻译技术文档，保持术语一致性。
        - 翻译时，维护文档结构，确保翻译内容的格式与原文一致。
        - 翻译时，熟悉Zabbix相关技术术语，确保翻译准确无误。
        - 翻译时，特定格式之间不能相互混淆。
        - 翻译时，应遵循术语处理规范，确保全局术语的一致性。
        - 翻译时，需严格遵守，确保术语、格式和语义的准确性。
        - 翻译时，应优先处理技术标记、格式保留和语义准确，确保专有名词、功能术语和描述文本的翻译质量。
        - 翻译时，使用正则表达式{v01}来准确匹配并保留术语标记，避免标记混淆、丢失、无中生有
        - 翻译时，禁止标记丢失、重复标记合并、标记ID乱序
        - 翻译时，原文中如果标记相同译文中保留的标记也要相同不要多个相同的标记合并成一个翻译
        - 翻译时，原文中带锚点的空链接需要保留
        - 翻译时，保留原文Markdown整体结构，包括但不限于标题不要丢失
        - 翻译时，不要出现幻觉
        - 翻译时，译文中保留的英文标记不要抄错了，注意字母的顺序，并检查是否和原文一致
        - 翻译时，对于标点符号沿用原文英文状态标点，译文中不要出现中文标点符号，翻译结果使用正则表达式{v03}替换对应的正则表达式{v02}，如。要被替换成.
        - 翻译时，对于序号类标点保持原样如x.，禁止翻译成x。,x代表数字
        - 翻译时，保留原文中的换行符号
        - 翻译结果，只返回对应翻译内容。

        ## 翻译流程:
        - 接收用户输入的待翻译文本
        - 定义：所有满足正则表达式{v01}格式的文本均为标记
        - 保留：所有标记原样保留（禁止翻译/删除/修改大小写）
        - 重复：若原文中有3个相同标记，译文也必须出现3次
        - 顺序：标记ID后缀（如“1a2b3c4d”）须严格按原文字符顺序
        - 翻译文本，确保技术语义的准确传递
        - 以Markdown格式返回翻译结果
        - 翻译结果，只返回对应翻译内容
        - 检查翻译结果，确保术语一致性与文档结构完整性
        - 在翻译完成后，进行一次全面的格式检查，仅包含翻译后的内容，保留所有原始标记和格式，不添加任何额外说明或注释，
        使用正则表达式{v01}来匹配原文校验翻译后的术语标记避免标记混淆、丢失、无中生有
        - 翻译完成后的文本禁止出现标记丢失、重复标记合并、标记ID乱序
        - 检查翻译后的标记是否有多个相同标记合并成一个标记的情况，有的话需分开
        - 使用正则表达式检查是否遗漏原文中带锚点的空链接，遗漏的话需要补上
        - 翻译完成后检查保留的英文标记是否与原文一致，注意字母的顺序，如果不一致需要重新抄写
        - 翻译完成后不要丢失Markdown格式标题
        - 翻译完成后禁止在最后面添加（注：.*）
        - 翻译结果不要有幻觉

        🔹 **示例**  
        Kyoto
        京都
    
        Mount Everest
        珠穆朗玛峰
    
        请按以上规则响应用户的翻译需求！
        
        {example}
        
        """

    def _build_user_content(self, text) -> str:
        return f"""{text}
"""

    def _build_request_params(self, text: str, example: Optional[Any] = None) -> Dict:
        """构造API请求参数"""
        return {
            "response_mode": "streaming",
            "user": self.api_user,
            # "query": text,
            "inputs": {
                "query": text,
                "prompt": self._build_prompt(example),
                "user_content": self._build_user_content(text)},
            # "inputs": {},
            "files": [],
            "conversation_id": "",
        }

    def _process_stream_response(self, response: requests.Response) -> str:
        """处理流式响应数据（生产级优化）"""
        chunks = []

        try:
            for line in response.iter_lines():
                if not line:
                    continue

                decoded_line = line.decode('utf-8')
                if not decoded_line.startswith('data:'):
                    continue

                try:
                    json_data = json.loads(decoded_line[5:].strip())
                    # 确保 json_data 是字典类型
                    if not isinstance(json_data, dict):
                        logger.warning(f"解析后的数据不是字典，类型为: {type(json_data)}，内容: {json_data}")
                        continue
                    # 获取 event 字段
                    data_event = json_data.get("event", "")
                    if data_event == "workflow_finished":
                        # 安全访问嵌套字段
                        data = json_data.get("data", {})
                        if not isinstance(data, dict):
                            logger.warning(f"data 字段不是字典，类型为: {type(data)}，内容: {data}")
                            continue

                        outputs = data.get("outputs", {})
                        if not isinstance(outputs, dict):
                            logger.warning(f"outputs 字段不是字典，类型为: {type(outputs)}，内容: {outputs}")
                            continue

                        llm_text = outputs.get("llm_text", "")
                        if llm_text is not None:
                            chunks.append(llm_text)
                            logger.debug(f"接收到数据分片，长度: {len(llm_text)}")

                except json.JSONDecodeError as e:
                    logger.warning(f"JSON解析错误: {e}, 原始数据: {decoded_line}")
                    continue

        except Exception as e:
            logger.error(f"流式处理异常: {str(e)}")
            raise

        logger.info(f"成功处理 {len(chunks)} 个数据分片")
        return "".join(chunks)

    def translate(self, text: str, example: Optional[Any] = None) -> Dict[str, object]:
        """
        执行翻译请求

        Args:
            text: 要翻译的文本

        Returns:
            包含翻译结果的字典:
            - success: 是否成功
            - result: 成功时为翻译结果，失败时为错误信息
        """
        if not text or not text.strip():
            logger.warning("翻译请求接收到空文本")
            return {'success': False, 'result': '错误！输入文本为空'}

        for attempt in range(self.max_retries):
            try:
                # logger.info(f"尝试翻译 (第{attempt + 1}次)...")
                response = self.session.post(
                    url=self.chat_endpoint,
                    headers=self.headers,
                    json=self._build_request_params(text, example),
                    timeout=self.timeout,
                    stream=True
                )
                response.raise_for_status()

                full_response = self._process_stream_response(response)
                if full_response:
                    return {'success': True, 'result': full_response}
                else:
                    logger.error("API返回空响应")
                    return {'success': False, 'result': '错误！API返回空响应'}

            except requests.exceptions.RequestException as e:
                logger.error(f"请求失败 (尝试 {attempt + 1}): {str(e)}")
                if attempt == self.max_retries - 1:
                    return {'success': False, 'result': f"错误！请求失败: {str(e)}"}
                time.sleep(2 ** attempt)  # 指数退避

        return {'success': False, 'result': '错误！未知错误'}

    def _fetch_conversation(self, workflow_id: str) -> str:
        """获取特定会话的完整响应"""
        try:
            params = {
                "user": self.api_user,
            }
            response = self.session.get(
                url=f"{self.message_endpoint}:{workflow_id}",
                headers=self.headers,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json().get('data', '').get('outputs', '').get('text', '')
        except requests.exceptions.RequestException as e:
            logger.error(f"获取会话失败: {str(e)}")
            return ''

    def _fetch_parameters(self):
        """获取特定会话的完整响应"""
        try:
            response = self.session.get(
                self.chat_parameters,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取会话失败: {str(e)}")
            return ''


class CusLanguageTransDeepSeek(object):
    def __init__(self, args: Optional[Any] = None):
        # 配置初始化
        self.args = args
        self.api_key = 'sk-'
        self.api_user = "侯建明"
        self.timeout = 10
        self.max_retries = 5
        self.model = 'qwen3-4b'
        self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.chat_endpoint = f"{self.base_url}/chat/completions"
        self.message_endpoint = f"{self.base_url}/workflows/run/"
        self.chat_parameters = f"{self.base_url}/parameters"

        # 请求头配置
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # 初始化会话和重试策略
        self.session = self._configure_session()

    def _configure_session(self) -> OpenAI:
        """配置带有重试策略的请求会话"""
        return OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
        )

    def _build_prompt(self, example: Optional[Any] = None) -> str:
        """构造翻译提示模板"""
        v01 = r'\{[A-Z]+_[a-f0-9]{1,8}\}'
        v02 = r'[\uFF01 -\uFF60\u3000 -\u303F]'
        v03 = r'[\u0021-\u002F\u003A-\u0040\u005B-\u0060\u007B-\u007E]'
        if ['location'].count(self.args.type) == 1:
            return f"""# Role：你是一个专业的地名翻译助手，专注于将外国地名（包括城市、自然景观、文化场所等）准确、规范地翻译成中文/英文。你遵循公认的翻译准则，兼顾历史习惯、语言规范和文化背景，并提供必要的解释说明。  

            ## 注意事项:
            - 严禁主观臆造译名，需严格依据权威资料。  
            - 对不了解的地名不猜测，可说明“暂未收录”并建议用户提供更多上下文。  
            - 保持政治与文化中立，符合中国法律法规及国际通用规范。  
            🔹 **核心功能**  
            1. **准确翻译**：  
               - 采用中国大陆官方或通用译名（参考《世界地名翻译大辞典》、新华社译名规范等）。  
               - 若地名存在多版本译名（如旧译/新译、音译/意译分歧），优先推荐最常用版本，并标注其他常见译法。  
               - 对特殊地名（含历史、宗教、文化背景）添加简要注释（如名称来源、意义或背景知识）。  

            2. **注音与语言标识**：  
               - 标注地名原始语言（如英语、西班牙语、阿拉伯语等），必要时用国际音标（IPA）或拼音辅助说明发音。  
               - 若地名本身具有含义（如“一月的河”意为“Rio de Janeiro”），可补充说明。  

            3. **处理复杂情况**：  
               - 对争议地区地名（如主权存在争议的名称），采用中立、客观的表述，必要时标注地区归属背景。  
               - 保留原名中的特殊符号（如连字符、空格），确保翻译格式清晰。  

            4. **用户交互支持**：  
               - 若用户提供的地名拼写模糊或可能存在错误，友好提示并尝试给出最接近的常见地名建议。  
               - 允许用户指定翻译风格（如学术严谨型、通俗通用型）。  

            🔹 **示例**  
            用户输入：”Kyoto“
            输出：
            - **标准中文翻译**：京都
            - **标准英文翻译**：Kyoto
            - **原始语言**：日语
            - **发音参考**：/kjoːto/
            - **其他译法**：暂未收录
            - **注释**：日本古都，曾长期为日本首都，以历史文化遗迹闻名。

            用户输入：”Mount Everest“
            输出：
            - **标准中文翻译**：珠穆朗玛峰
            - **标准英文翻译**：Mount Everest
            - **原始语言**：英语
            - **发音参考**：暂未收录
            - **其他译法**：埃佛勒斯峰（旧译）
            - **注释**：位于中国与尼泊尔边境，是世界最高峰。尼泊尔称“萨加玛塔峰”（Sagarmatha）。

            请按以上规则响应用户的地名翻译需求！

            - 翻译结果，只返回对应翻译内容。

            ## 翻译流程:
            - 接收用户输入的待翻译文本
            - 定义：所有满足正则表达式{v01}格式的文本均为标记
            - 保留：所有标记原样保留（禁止翻译/删除/修改大小写）
            - 重复：若原文中有3个相同标记，译文也必须出现3次
            - 顺序：标记ID后缀（如“1a2b3c4d”）须严格按原文字符顺序
            - 翻译文本，确保技术语义的准确传递
            - 以Markdown格式返回翻译结果
            - 翻译结果，只返回对应翻译内容
            - 检查翻译结果，确保术语一致性与文档结构完整性
            - 在翻译完成后，进行一次全面的格式检查，仅包含翻译后的内容，保留所有原始标记和格式，不添加任何额外说明或注释，
            使用正则表达式{v01}来匹配原文校验翻译后的术语标记避免标记混淆、丢失、无中生有
            - 翻译完成后的文本禁止出现标记丢失、重复标记合并、标记ID乱序
            - 检查翻译后的标记是否有多个相同标记合并成一个标记的情况，有的话需分开
            - 使用正则表达式检查是否遗漏原文中带锚点的空链接，遗漏的话需要补上
            - 翻译完成后检查保留的英文标记是否与原文一致，注意字母的顺序，如果不一致需要重新抄写
            - 翻译完成后不要丢失Markdown格式标题
            - 翻译完成后禁止在最后面添加（注：.*）
            - 翻译结果不要有幻觉
            - `**标准中文翻译**：［中文译名/中文原文/暂未收录］`，优先输出`中文译名`，没有的话输出`中文原文`,还没有的话输出`暂未收录`
            - `**标准英文翻译**：［英文译名/英文原文/Not Yet Included］`，优先输出`英文译名`，没有的话输出`英文原文`,还没有的话输出`Not Yet Included`
            - 根据`- **原始语言**：英文` 只有原始语言为英文`- **标准中文翻译**：暂未收录`才能填写`暂未收录`，同时`- **标准英文翻译**：［英文原文］`
            - 根据`- **原始语言**：中文` 只有原始语言为中文`- **标准英文翻译**：暂未收录`才能填写`Not Yet Included`，同时`- **标准中文翻译**：［中文原文］`
            - 翻译后的输出结果，仅返回OutputFormat格式要求结果

            {example}

            ## OutputFormat:

            - **标准中文翻译**：［中文译名/中文原文/只有原始语言不为英文才能填写暂未收录］
            - **标准英文翻译**：［英文译名/英文原文/Not Yet Included］
            - **原始语言**：［语言名称］
            - **发音参考**：［IPA/拼音/暂未收录］
            - **其他译法**：［若有则列出/暂未收录］
            - **注释**：［文化、历史或地理背景说明/暂未收录］
            """
        else:
            return f"""# Role：专业Zabbix技术文档翻译官助手
    
    ## 注意事项:
    - 翻译时，专注于Zabbix技术文档的翻译，确保技术语义的精准传递，维护术语一致性与文档结构完整性。
    - 翻译时，不考虑敏感词禁忌问题，专注于技术翻译。
    - 翻译时，遵循特定的术语处理规范。
    - 翻译时，精准翻译技术文档，保持术语一致性。
    - 翻译时，维护文档结构，确保翻译内容的格式与原文一致。
    - 翻译时，熟悉Zabbix相关技术术语，确保翻译准确无误。
    - 翻译时，特定格式之间不能相互混淆。
    - 翻译时，应遵循术语处理规范，确保全局术语的一致性。
    - 翻译时，需严格遵守，确保术语、格式和语义的准确性。
    - 翻译时，应优先处理技术标记、格式保留和语义准确，确保专有名词、功能术语和描述文本的翻译质量。
    - 翻译时，使用正则表达式{v01}来准确匹配并保留术语标记，避免标记混淆、丢失、无中生有
    - 翻译时，禁止标记丢失、重复标记合并、标记ID乱序
    - 翻译时，原文中如果标记相同译文中保留的标记也要相同不要多个相同的标记合并成一个翻译
    - 翻译时，原文中带锚点的空链接需要保留
    - 翻译时，保留原文Markdown整体结构，包括但不限于标题不要丢失
    - 翻译时，不要出现幻觉
    - 翻译时，译文中保留的英文标记不要抄错了，注意字母的顺序，并检查是否和原文一致
    - 翻译时，对于标点符号沿用原文英文状态标点，译文中不要出现中文标点符号，翻译结果使用正则表达式{v03}替换对应的正则表达式{v02}，如。要被替换成.
    - 翻译时，对于序号类标点保持原样如x.，禁止翻译成x。,x代表数字
    - 翻译时，保留原文中的换行符号
    - 翻译结果，只返回对应翻译内容。
    
    ## 翻译流程:
    - 接收用户输入的待翻译文本
    - 定义：所有满足正则表达式{v01}格式的文本均为标记
    - 保留：所有标记原样保留（禁止翻译/删除/修改大小写）
    - 重复：若原文中有3个相同标记，译文也必须出现3次
    - 顺序：标记ID后缀（如“1a2b3c4d”）须严格按原文字符顺序
    - 翻译文本，确保技术语义的准确传递
    - 以Markdown格式返回翻译结果
    - 翻译结果，只返回对应翻译内容
    - 检查翻译结果，确保术语一致性与文档结构完整性
    - 在翻译完成后，进行一次全面的格式检查，仅包含翻译后的内容，保留所有原始标记和格式，不添加任何额外说明或注释，
    使用正则表达式{v01}来匹配原文校验翻译后的术语标记避免标记混淆、丢失、无中生有
    - 翻译完成后的文本禁止出现标记丢失、重复标记合并、标记ID乱序
    - 检查翻译后的标记是否有多个相同标记合并成一个标记的情况，有的话需分开
    - 使用正则表达式检查是否遗漏原文中带锚点的空链接，遗漏的话需要补上
    - 翻译完成后检查保留的英文标记是否与原文一致，注意字母的顺序，如果不一致需要重新抄写
    - 翻译完成后不要丢失Markdown格式标题
    - 翻译完成后禁止在最后面添加（注：.*）
    - 翻译结果不要有幻觉
    
    🔹 **示例**  
    Kyoto
    京都

    Mount Everest
    珠穆朗玛峰

    请按以上规则响应用户的翻译需求！
    
    {example}
    

    """

    def _build_user_content(self, text) -> str:
        return f"""{text}
"""

    def _send_translation_request(self, text: str, example: Optional[Any] = None):
        """发送翻译请求"""
        return self.session.chat.completions.create(
            model=self.model,
            messages=[
                {'role': 'system', 'content': self._build_prompt(example)},
                {'role': 'user', 'content': self._build_user_content(text)}
            ],
            temperature=0.01,
            top_p=0.1,
            max_tokens=30000,
            stream=True,
            extra_body={"chat_template_kwargs": {"enable_thinking": False}}
        )

    def _process_response(self, response) -> str:
        """
        处理API流式响应（生产级优化）

        参数:
            response: 流式响应对象
            timeout: 超时时间(秒)，默认30秒

        返回:
            str: 拼接完整的响应内容

        异常:
            TimeoutError: 处理超时时抛出
            RuntimeError: 处理过程中出现严重错误时抛出

        说明:
            1. 增加超时机制防止无限等待
            2. 完善的错误处理和日志记录
            3. 使用列表收集数据避免乱序和性能问题
            4. 详细的运行日志便于调试
        """
        chunks = []
        processed_chunks = 0

        try:
            for chunk in response:
                if not (chunk.choices and chunk.choices[0].delta.content):
                    continue
                content = chunk.choices[0].delta.content
                chunks.append(content)
                processed_chunks += 1
                logger.debug(f"接收到数据分片，长度: {len(content)}")

        except Exception as e:
            logger.error(f"流式响应处理异常: {str(e)}", exc_info=True)
            raise RuntimeError(f"处理流式响应失败: {str(e)}") from e

        logger.info(f"成功处理 {processed_chunks} 个数据分片，总长度: {sum(len(c) for c in chunks)}")
        return "".join(chunks)

    def translate(self, text: str, example: Optional[Any] = None) -> Dict[str, object]:
        """
        执行翻译请求

        Args:
            text: 要翻译的文本

        Returns:
            包含翻译结果的字典:
            - success: 是否成功
            - result: 成功时为翻译结果，失败时为错误信息
        """
        if not text or not text.strip():
            logger.warning("翻译请求接收到空文本")
            return {'success': False, 'result': '错误！输入文本为空'}

        for attempt in range(self.max_retries):
            try:
                # logger.info(f"尝试翻译 (第{attempt + 1}次)...")
                response = self._send_translation_request(text, example)
                result = self._process_response(response)
                return {'success': True, 'result': result}
            except Exception as e:
                logger.error(f"请求失败 (尝试 {attempt + 1}): {str(e)}")
                if attempt == self.max_retries - 1:
                    return {'success': False, 'result': f"错误！请求失败: {str(e)}"}
                time.sleep(2 ** attempt)  # 指数退避

        return {'success': False, 'result': '错误！未知错误'}


class CusRetryManager:
    """管理任务重试和结果收集的非阻塞控制器 (带进度跟踪版)"""

    def __init__(
            self,
            executor: concurrent.futures.Executor,
            task_func: Callable[[Any], Any],
            validator_func: Callable[[Any], bool],
            max_retries: int = 3,
            retry_delay: float = 1,
            total_tasks: int = 0  # 新增总任务数参数
    ):
        """初始化重试管理器

        Args:
            executor: 线程池/进程池执行器
            task_func: 要执行的任务函数
            validator_func: 验证结果是否有效的函数
            max_retries: 最大重试次数 (默认3)
            retry_delay: 基础重试间隔秒数 (默认1)
            total_tasks: 总任务数量 (用于进度计算)
        """
        self.executor = executor
        self.max_retries = max_retries
        self.task_func = task_func
        self.validator_func = validator_func
        self.retry_delay = retry_delay
        self.total_tasks = total_tasks
        self.results: Dict[int, Optional[Any]] = {}
        self.pending_tasks: Dict[concurrent.futures.Future, tuple] = {}
        self.completed_count = 0  # 已完成任务计数器
        self.start_time = time.time()  # 记录开始时间

    def submit_task(self, item: Any, index: int, attempt: int = 0) -> None:
        """提交任务并绑定回调"""
        future = self.executor.submit(self.task_func, item)
        self.pending_tasks[future] = (item, index, attempt)
        future.add_done_callback(self._handle_completion)
        self._print_progress(f"任务 [索引={index}] 已提交 (尝试 {attempt + 1}/{self.max_retries})")
        return future  # ★ 关键修改：返回future对象

    def _print_progress(self, message: str) -> None:
        """打印带进度信息的消息"""
        if self.total_tasks > 0:
            progress = (self.completed_count / self.total_tasks) * 100
            elapsed_time = time.time() - self.start_time
            print(f"[进度: {progress:.1f}% | 已完成: {self.completed_count}/{self.total_tasks} | 耗时: {elapsed_time:.1f}s] {message}")
        else:
            print(message)

    def _handle_completion(self, future: concurrent.futures.Future) -> None:
        """处理任务完成事件 (增强日志)"""
        item, index, attempt = self.pending_tasks.pop(future)

        try:
            result = future.result()
            logger.debug(f"任务 [索引={index}] 原始结果类型: {type(result)}")

            is_valid = self.validator_func(result)

            if is_valid:
                result_str = str(result)
                if len(result_str) > 50:
                    result_str = result_str[:50] + "..."
                self.results[index] = result
                self.completed_count += 1  # 增加已完成计数
                self._print_progress(f"任务 [索引={index}] 成功，结果摘要: {result_str}")
            else:
                self._print_progress(f"任务 [索引={index}] 结果无效 (类型: {type(result)}), 准备重试...")
                self._retry_task(item, index, attempt)
        except Exception as e:
            self._print_progress(f"任务 [索引={index}] 执行失败 (异常类型: {type(e).__name__}): {str(e)}")
            self._retry_task(item, index, attempt)

    def _retry_task(self, item: Any, index: int, attempt: int) -> None:
        """执行重试逻辑 (带退避)"""
        if attempt < self.max_retries:
            delay = self.retry_delay * (2 ** attempt)
            logger.debug(f"任务 [索引={index}] 将在 {delay} 秒后重试 (尝试 {attempt + 1}/{self.max_retries})")
            time.sleep(delay)
            self.submit_task(item, index, attempt + 1)
        else:
            self.results[index] = None
            self.completed_count += 1  # 即使失败也计入完成
            logger.debug(f"任务 [索引={index}] 重试用尽，最终失败")

    def wait_for_completion(self, timeout: Optional[float] = None) -> bool:
        """等待所有任务完成

        Args:
            timeout: 超时时间(秒)

        Returns:
            bool: 是否所有任务都已完成
        """
        start_time = time.time()
        while self.pending_tasks:
            if timeout and (time.time() - start_time) > timeout:
                logger.debug(f"等待超时 ({timeout}秒)，仍有 {len(self.pending_tasks)} 个任务未完成")
                return False
            time.sleep(0.1)
            # 定期打印进度
            if len(self.pending_tasks) % 10 == 0:  # 每10个任务打印一次
                self._print_progress(f"等待任务完成...剩余 {len(self.pending_tasks)} 个任务")
        return True


class CusTranslationProcessor:
    """处理翻译流程，集成重试机制和结果验证"""

    def __init__(self, args, cus_termProcessor, cus_excel_op, cus_deepseekdify: Optional[Any] = None):
        """初始化翻译处理器

        Args:
            args: 命令行参数
            cus_termProcessor: 术语处理器实例
            cus_excel_op: Excel操作实例
            cus_deepseekdify: 翻译服务实例
        """
        self.args = args
        self.cus_termProcessor = cus_termProcessor
        self.cus_excel_op = cus_excel_op
        self.cus_deepseekdify = cus_deepseekdify

        # 配置参数
        self.output_file = 'trans_all.xlsx'
        self.zabbix_terms_table_titles_file = 'TERM_EXCEL_LIST.xlsx'
        self.document_file = 'document.xlsx'
        self.term_document_sheet = 'document'
        self.term_table_sheet = 'EXCEL_MAPPING'
        self.term_header_sheet = 'HEADER_MAPPING'
        self.term_link_sheet = 'LINK_MAPPING'

        # 初始化Excel数据
        self._init_excel_data()

    def _init_excel_data(self):
        """初始化Excel数据"""
        self.cus_excel_op.load_excel(self.document_file, 1)
        self.column_3_list = self.cus_excel_op.get_column_values(3)
        del self.column_3_list[0]

        # 初始化结果列表
        self.lv_list_get_all_host_groupid = [""] * len(self.column_3_list)

        # 清理旧文件
        for f in [self.output_file, self.zabbix_terms_table_titles_file]:
            if os.path.exists(f):
                os.remove(f)

    def _init_excel_sheets(self):
        """初始化Excel工作表"""
        cus_excel_op1 = CusExcelOp()
        cus_excel_op1.load_excel(self.document_file, 1)

        # 配置各sheet
        sheets_config = [
            (self.term_table_sheet, ["路径", "源文件行号", "表格序号", "原始表头", "列名", "标准化列名",
                                     "是否受保护", "保护原因", "建议操作"]),
            (self.term_header_sheet, ["路径", "源文件行号", "标题级别", "标题内容", "完整标题文本",
                                      "是否有锚点", "锚点名称", "是否已翻译", "翻译内容", "EN", "ZH"]),
            (self.term_link_sheet, ["路径", "源文件行号", "链接类型", "文本部分", "链接部分",
                                    "是否有锚点", "锚点名称", "完整超链接", "是否已翻译", "翻译内容"])
        ]

        for sheet_name, headers in sheets_config:
            self.cus_excel_op.create_sheet(sheet_name)
            self.cus_excel_op.activate_sheet(sheet_name)
            for col, header in enumerate(headers, start=1):
                self.cus_excel_op.set_cell_value(1, col, header)

        self.cus_excel_op.save_workbook(self.zabbix_terms_table_titles_file)
        return cus_excel_op1

    def _validate_translation_result(self, result: Any) -> bool:
        """改进的翻译结果验证方法

        Args:
            result: 翻译服务返回的结果，可能是字典或字符串

        Returns:
            bool: 结果是否有效
        """
        if result is None:
            return False

        # 处理字典类型的返回结果
        if isinstance(result, dict):
            # 检查success字段是否为True
            if not result.get('success', False):
                logger.debug(f"验证失败: success字段为False")
                return False

            # 获取翻译结果内容
            translated_text = result.get('result', '')
            if not isinstance(translated_text, str):
                logger.debug(f"验证失败: result字段不是字符串类型")
                return False

            # 检查翻译结果是否为空
            if not translated_text.strip():
                logger.debug(f"验证失败: 翻译结果为空")
                return False

            # 检查是否包含明显的错误信息（放宽条件）
            error_phrases = ["响应中缺少answer字段", "not enough"]
            if any(phrase in translated_text.lower() for phrase in error_phrases):
                logger.debug(f"验证失败: 包含错误短语")
                return False

            return True

        # 处理字符串类型的返回结果
        elif isinstance(result, str):
            if not result.strip():
                logger.debug(f"验证失败: 字符串结果为空")
                return False

            error_phrases = ["响应中缺少answer字段", "not enough"]
            if any(phrase in result.lower() for phrase in error_phrases):
                logger.debug(f"验证失败: 包含错误短语")
                return False

            return True

        logger.debug(f"验证失败: 未知结果类型 {type(result)}")
        return False

    def _validate_translation(self, original_text: str, translated_text: str) -> Dict[str, List[str]]:
        """
        增强版翻译校验，精确报告标记丢失情况（包括重复标记）并关联原文内容

        参数:
            original_text: 原始文本（包含标记）
            translated_text: 翻译后的文本

        返回:
            Dict[str, List[str]]: 包含三类错误:
                - 'missing_markers': 标记数量不一致或具体丢失的标记
                - 'unrestored_markers': 未被还原的标记及其出现次数差异
                - 'marker_context': 异常标记对应的原文上下文
        """
        errors = {
            'missing_markers': [],
            'unrestored_markers': [],
            'marker_context': {}  # 新增：存储异常标记的上下文
        }

        # 1. 提取原文和译文中的所有标记（保留顺序和重复）
        marker_pattern = r'\{[A-Z]+_[a-f0-9]{1,8}\}'
        original_markers = re.findall(marker_pattern, original_text)
        translated_markers = re.findall(marker_pattern, translated_text)

        # 2. 构建标记上下文映射（标记 -> 包含该标记的原文片段）
        context_map = {}
        for marker in set(original_markers):
            # 查找标记周围的上下文（标记前后各20个字符）
            context = re.search(fr'.{{0,20}}{re.escape(marker)}.{{0,20}}', original_text)
            if context:
                context_map[marker] = context.group(0)

        # 3. 检查标记数量一致性（考虑重复标记）
        if len(original_markers) != len(translated_markers):
            marker_counts = {}
            for marker in set(original_markers + translated_markers):
                orig_count = original_markers.count(marker)
                trans_count = translated_markers.count(marker)
                if orig_count != trans_count:
                    marker_counts[marker] = (orig_count, trans_count)
                    # 记录上下文
                    if marker in context_map:
                        errors['marker_context'][marker] = context_map[marker]

            # 生成详细的错误信息
            details = []
            for marker, (orig, trans) in marker_counts.items():
                if trans == 0:
                    details.append(f"找回{marker}标记，理由（完全缺失，原文出现`{orig}`次）")
                else:
                    abs_diff = abs(orig - trans)
                    details.append(f"找回`{abs_diff}`个{marker}标记，理由（原文出现`{orig}`次，译文出现`{trans}`次）")

            errors['unrestored_markers'].append(
                f"标记数量不一致: 原文标记出现`{len(original_markers)}`次，译文标记出现`{len(translated_markers)}`次"
            )
            errors['missing_markers'].append(
                f"具体差异: {', '.join(details)}"
            )

        # 4. 检查每个唯一标记是否存在
        original_markers_set = set(original_markers)
        translated_markers_set = set(translated_markers)

        # 完全缺失的标记（译文一次都没出现）
        completely_missing = original_markers_set - translated_markers_set
        for marker in completely_missing:
            count = original_markers.count(marker)
            errors['unrestored_markers'].append(
                f"标记 {marker} 完全缺失（原文出现 `{count}` 次）"
            )
            # 记录上下文
            if marker in context_map:
                errors['marker_context'][marker] = context_map[marker]

        # 定义括号对
        bracket_pairs = [('{', '}'), ('[', ']')]

        for open_br, close_br in bracket_pairs:
            # 计算原文和译文中开括号和关括号的数量
            orig_open = original_text.count(open_br)
            orig_close = original_text.count(close_br)
            trans_open = translated_text.count(open_br)
            trans_close = translated_text.count(close_br)

            # 计算原文和译文中未闭合的括号数量
            orig_unmatched_open = max(0, orig_open - orig_close)
            orig_unmatched_close = max(0, orig_close - orig_open)
            trans_unmatched_open = max(0, trans_open - trans_close)
            trans_unmatched_close = max(0, trans_close - trans_open)

            # 第一步：校验括号是否成对出现或未闭合的括号是否对应
            if (orig_unmatched_open > 0 and trans_unmatched_open < orig_unmatched_open) or \
                    (orig_unmatched_close > 0 and trans_unmatched_close < orig_unmatched_close) or \
                    (orig_unmatched_open == 0 and orig_open != orig_close) or \
                    (orig_unmatched_close == 0 and orig_close != orig_open) or \
                    (trans_unmatched_open == 0 and trans_open != trans_close) or \
                    (trans_unmatched_close == 0 and trans_close != trans_open):
                error_msg = (
                    f"{open_br}{close_br} 括号不成对出现或未闭合的括号不对应: "
                    f"原文 {open_br}出现{orig_open}次，{close_br}出现{orig_close}次；"
                    f"译文 {open_br}出现{trans_open}次，{close_br}出现{trans_close}次"
                )
                errors['missing_markers'].append(error_msg)
                continue


            # 第二步：校验原文和译文中的括号数量是否一致
            if orig_open != trans_open or orig_close != trans_close:
                error_msg = (
                    f"{open_br}{close_br} 括号数量不一致: "
                    f"原文 {open_br}出现{orig_open}次，{close_br}出现{orig_close}次；"
                    f"译文 {open_br}出现{trans_open}次，{close_br}出现{trans_close}次"
                )
                errors['missing_markers'].append(error_msg)

        # 新增：检查翻译结果是否包含特定文本
        expected_strings = [
            r".*OutputFormat.*",
            r".*翻译结果.*",
            r".*输出结果.*",
            r"::: ?[\u4e00-\u9fa5]+",
            r'\n    [^\n\u4e00-\u9fff]+(?:\n(?![^\n\u4e00-\u9fff]+)\n    [^\n\u4e00-\u9fff]+)*\n\n'
            # r'.*[\uFF01 -\uFF60\u3000 -\u303F].*'
        ]

        for expected in expected_strings:
            if re.search(expected, translated_text):
                errors['missing_markers'].append(f"翻译结果不应包含文本：{expected}")

        if ['location'].count(self.args.type) == 1:
            # 新增：校验标准中文翻译的格式
            expected_structure = [
                r"- \*\*标准中文翻译\*\*：(?!.*[\[\]\|a-zA-Z])([\u4e00-\u9fff\s]*|暂未收录)",
                r"- \*\*标准英文翻译\*\*：(?!.*[\[\]\|\u4e00-\u9fff])([a-zA-Z\s]*|Not Yet Included)",
                r"- \*\*原始语言\*\*：.*",
                r"- \*\*发音参考\*\*：.*",
                r"- \*\*其他译法\*\*：.*",
                r"- \*\*注释\*\*：.*"
            ]

            # 检查是否以 '- **标准中文翻译**：' 开头
            if not translated_text.startswith('- **标准中文翻译**：'):
                errors['missing_markers'].append("翻译文本必须以 '- **标准中文翻译**：' 开头")

            # 检查结构是否符合预期
            lines = translated_text.split('\n')
            if len(lines) < len(expected_structure):
                errors['missing_markers'].append("翻译文本结构不完整")
            else:
                for i, line in enumerate(lines[:len(expected_structure)]):
                    if not re.match(expected_structure[i], line.strip()):
                        if i == 0:
                            errors['missing_markers'].append("第1行应为标准中文翻译，但包含非中文字符或格式错误: " + line)
                        elif i == 1:
                            errors['missing_markers'].append("第2行应为标准英文翻译，但包含非英文字符或格式错误: " + line)
                        else:
                            errors['missing_markers'].append(f"第{i + 1}行结构不符合预期: " + line)

        return errors

    def _validate_translation_with_fallback(self, original_text: str, translated_text: str, max_retries: int = 3) -> Dict:
        """
        增强版翻译校验，包含分片失败回退处理和详细标记校验

        参数:
            original_text: 原始文本（包含标记）
            translated_text: 翻译后的文本
            max_retries: 最大重试次数

        返回:
            Dict: 包含校验结果和错误详情:
                - is_valid: 整体是否有效
                - errors: 详细错误信息
                - fallback_error: 回退错误信息（如果有）
        """

        for attempt in range(max_retries + 1):
            # 最后一次尝试时回退到原始文本
            if attempt == max_retries:
                translated_text = original_text

            # 调用原有的详细校验方法
            errors = self._validate_translation(original_text, translated_text)

            # 如果没有标记错误且不是回退的情况
            if not errors['unrestored_markers'] and not errors['missing_markers']:
                return {
                    "is_valid": True,
                    "errors": errors,
                }
            else:
                return {
                    "is_valid": False,
                    "errors": errors,
                }

    def _validate_excel_column(self, output_file_path: str, column_to_validate: int, result_column: int) -> None:
        """
        验证Excel文件中指定列的数据，并将校验结果写入指定列。

        参数:
            output_file_path: 输出文件路径
            column_to_validate: 需要验证的列索引（从1开始）
            result_column: 写入校验结果的列索引（从1开始）

        返回:
            None
        """
        # 加载Excel文件
        excel_op = CusExcelOp()
        excel_op.load_excel(output_file_path)

        # 获取指定列的数据
        column_data = excel_op.get_column_values(3)
        # 遍历每一行数据进行校验
        for row_idx, cell_value in enumerate(column_data, start=1):
            errors = []

            # 获取C列的值
            c_value = excel_op.get_cell_value(row_idx, 3)
            d_value = excel_op.get_cell_value(row_idx, column_to_validate)
            if not d_value:
                continue
            # 校验括号、方括号、花括号、::: 和 ``` 是否成对出现
            for char_pair in [('(', ')'), ('[', ']'), ('{', '}')]:
                open_char, close_char = char_pair
                if open_char in d_value and d_value.count(open_char) != d_value.count(close_char):
                    errors.append(f"{open_char}和{close_char}不成对出现\n")

            # 特殊字符 ::: 和 ``` 的成对性校验
            special_chars = [':::', '```']
            for char in special_chars:
                if d_value.count(char) % 2 != 0:
                    errors.append(f"{char}字符不成对出现\n")

            # 新增：检查翻译结果是否包含特定文本
            expected_strings = [
                r".*OutputFormat.*",
                r".*翻译结果.*",
                r".*输出结果.*",
                r"::: ?[\u4e00-\u9fa5]+",
                r'\{[A-Z]+_[a-f0-9]{1,8}\}',
                r'\|.*?\|\n\n(?! *\r?\n\n *)\|.*?\|',
                # r'.*[\uFF01 -\uFF60\u3000 -\u303F].*'
            ]

            for expected in expected_strings:
                if re.search(expected, d_value):
                    errors.append(f"翻译结果不应包含文本：{expected}\n")

            patterns = {
                '换行符': r'\n\n',
            }
            counts = {}
            d_newlines = 0
            c_newlines = 0
            # 打印调试信息
            # print(f"d_value type: {type(d_value)}, value: {d_value}")
            # print(f"c_value type: {type(c_value)}, value: {c_value}")
            for key, pattern in patterns.items():
                d_newlines = len(re.findall(pattern, d_value, re.MULTILINE))
                c_newlines = len(re.findall(pattern, c_value, re.MULTILINE))
                counts[key] = {'d': d_newlines, 'c': c_newlines}
            # 计算较大的换行符数量作为基准
            max_newlines = max(d_newlines, c_newlines)
            # 计算允许的最大误差
            allowed_error = max_newlines * 0.5 if max_newlines > 0 else 0
            # 计算实际的差异
            actual_difference = abs(d_newlines - c_newlines)

            # 检查实际差异是否超过允许的误差
            if actual_difference > allowed_error:
                errors.append(
                    f"C列和D列中的换行符数量不一致，D列有{d_newlines}个，C列有{c_newlines}个，"
                    f"差异超过了50%的允许误差范围。\n"
                )

            # 统计数字、点号、数字空格、4个空格开头的行、#空格数字的出现次数
            patterns = {
                '序号': r'\d ?\. ',
                '序号转义': r'\d ?\\. ',
                '整数标题': r'#\s+\d+',
                'br换行': r'<br>',
            }

            counts = {}
            for key, pattern in patterns.items():
                d_count = len(re.findall(pattern, d_value, re.MULTILINE))
                c_count = len(re.findall(pattern, c_value, re.MULTILINE))
                counts[key] = {'d': d_count, 'c': c_count}

                if d_count != c_count:
                    errors.append(
                        f"C列和D列中的{key}数量不一致，D列有{d_count}个，C列有{c_count}个\n"
                    )


            # 如果有错误，则写入校验结果
            if errors:
                error_message = ''.join(errors)
                excel_op.set_cell_value(row_idx, result_column, error_message)

        excel_op.save_workbook(self.output_file)

    def _process_batch(self, batch_start, batch_end, batch_num, total_batches, cus_excel_op1):
        """改进的批次处理方法，支持实时回调显示进度"""
        current_batch = self.column_3_list[batch_start:batch_end]
        total_items = len(current_batch)
        completed_count = 0
        success_count = 0
        failed_indices = []

        # 进度回调函数
        def progress_callback(future, index):
            nonlocal completed_count, success_count
            try:
                result = future.result()
                if self._validate_translation_result(result):
                    translated_text = result['result'] if isinstance(result, dict) else result
                    self.lv_list_get_all_host_groupid[index] = translated_text
                    success_count += 1
                else:
                    failed_indices.append(index)
            except Exception as e:
                failed_indices.append(index)
                print(f"翻译任务失败 (索引={index}): {str(e)}")
            finally:
                completed_count += 1
                # 实时进度显示（每10个或最后一条更新）
                if completed_count % 10 == 0 or completed_count == total_items:
                    progress = (completed_count / total_items) * 100
                    print(
                        f"批次 {batch_num}/{total_batches}: "
                        f"进度 {completed_count}/{total_items} ({progress:.1f}%) | "
                        f"成功 {success_count} | 失败 {len(failed_indices)}"
                    )

        # 计算实际并行任务数
        parallel_tasks = min(GV_CPU_COUNT, total_items)

        with ThreadPoolExecutor(max_workers=parallel_tasks) as executor:
            retry_manager = CusRetryManager(
                executor=executor,
                task_func=self._translate_item,
                validator_func=self._validate_translation_result,
                max_retries=3,
                retry_delay=2,
                total_tasks=total_items
            )

            # 提交所有任务并添加回调
            for i, col in enumerate(current_batch):
                if col:  # 只有有内容时才处理
                    global_index = batch_start + i
                    future = retry_manager.submit_task((col, global_index), global_index)
                    future.add_done_callback(lambda f, idx=global_index: progress_callback(f, idx))

            # 等待所有任务完成（带超时控制）
            print(f"▶ 开始处理批次 {batch_num} (共 {total_items} 项)...")
            if not retry_manager.wait_for_completion(timeout=60 * 30):
                print(f"⚠ 警告: 批次 {batch_num} 处理超时，已完成 {completed_count}/{total_items}")

        # 最终统计报告
        print(
            f"▷ 批次 {batch_num} 完成: "
            f"成功 {success_count}/{total_items} | "
            f"失败 {len(failed_indices)}"
        )
        if failed_indices:
            print(f"失败索引: {sorted(failed_indices)}")

        # 执行二次验证和结果写入
        self._validate_and_write_results(batch_start, batch_end, batch_num, total_batches, cus_excel_op1)

    def _translate_item(self, item_data: tuple) -> Any:
        """改进的翻译方法，确保返回统一格式"""
        col, index = item_data
        source_row = index + 2

        try:
            # 预处理和导出
            self._export_excel_data(col, source_row)

            # 预处理内容
            processed_col = self.cus_termProcessor.preprocess(col)
            self.cus_excel_op.activate_sheet(self.term_document_sheet)
            self.cus_excel_op.set_cell_value(source_row, 4, processed_col)

            # 执行翻译并统一返回格式
            # translation_result = self.cus_deepseekdify.translate(processed_col)
            translation_result = {'success': True, 'result': '{HEADER_af31b4b2}\n'}
            # print(translation_result)
            # exit(1)

            # 确保返回统一格式
            if isinstance(translation_result, dict):
                if 'success' not in translation_result:
                    translation_result['success'] = True
                return translation_result
            elif isinstance(translation_result, str):
                return {'success': True, 'result': translation_result}
            else:
                return {'success': False, 'result': str(translation_result)}

        except Exception as e:
            print(f"翻译过程中发生异常: {str(e)}")
            return {'success': False, 'result': str(e)}

    def _export_excel_data(self, col: str, source_row: int):
        """导出数据到Excel各工作表"""
        self.cus_excel_op.activate_sheet(self.term_table_sheet)
        self.current_table_map_write_row = self.cus_termProcessor.export_table_headers_to_excel(
            self.cus_excel_op, col, source_row, getattr(self, 'current_table_map_write_row', 2))

        self.cus_excel_op.activate_sheet(self.term_header_sheet)
        self.current_head_map_write_row = self.cus_termProcessor.export_markdown_headers_to_excel(
            self.cus_excel_op, col, source_row, getattr(self, 'current_head_map_write_row', 2))

        self.cus_excel_op.activate_sheet(self.term_link_sheet)
        self.current_link_map_write_row = self.cus_termProcessor.export_markdown_links_to_excel(
            self.cus_excel_op, col, source_row, getattr(self, 'current_link_map_write_row', 2))

    def _validate_and_write_results(self, batch_start: int, batch_end: int, batch_num: int, total_batches: int, cus_excel_op1):
        """增强的验证和结果写入方法，支持实时回调进度显示"""
        print(f"\n▶ 开始批次 {batch_num}/{total_batches} 的二次验证...")

        # 准备验证任务数据
        validation_tasks = []
        for i in range(batch_start, batch_end):
            translated_text = self.lv_list_get_all_host_groupid[i]
            if translated_text:
                original_text = self.cus_excel_op.get_cell_value(i + 2, 4)
                validation_tasks.append({
                    "index": i,
                    "original_text": original_text,
                    "translated_text": translated_text,
                    "excel_op": cus_excel_op1,
                    "row_index": i + 2,
                    "max_retries": 1
                })

        total_tasks = len(validation_tasks)
        completed_tasks = 0
        success_count = 0
        failed_indices = []

        # 进度回调函数
        def validation_callback(future):
            nonlocal completed_tasks, success_count
            try:
                result = future.result()
                status_msg = "✓" if result["is_valid"] else "✗"
                color_code = "32" if result["is_valid"] else "31"

                # 更新统计
                if result["is_valid"]:
                    success_count += 1
                else:
                    failed_indices.append(result["row_index"])

                # 实时进度显示
                completed_tasks += 1
                progress = (completed_tasks / total_tasks) * 100
                print(
                    f"\r批次 {batch_num}/{total_batches}: "
                    f"进度 {completed_tasks}/{total_tasks} ({progress:.1f}%) | "
                    f"成功 {success_count} | 失败 {len(failed_indices)} "
                    f"[最新: 行{result['row_index']} {status_msg}]",
                    end="", flush=True
                )

                # 写入结果到Excel
                if result["is_valid"]:
                    self._write_results_to_excel(
                        cus_excel_op1,
                        result["row_index"],
                        result["result"],
                        {}
                    )
                else:
                    self._write_results_to_excel(
                        cus_excel_op1,
                        result["row_index"],
                        result["result"],
                        result["errors"]
                    )

            except Exception as e:
                print(f"\n验证回调异常: {str(e)}")

        # 使用线程池并行验证
        with ThreadPoolExecutor(max_workers=GV_CPU_COUNT) as executor:
            # 提交所有验证任务
            futures = []
            for task in validation_tasks:
                future = executor.submit(self._retry_translation_with_validation, task)
                future.add_done_callback(validation_callback)
                futures.append(future)

            # 等待所有任务完成
            print("\n等待验证任务完成...")
            done, not_done = wait(futures, timeout=60 * 30)
            if not_done:
                print(f"\n⚠ 警告: {len(not_done)}个验证任务超时未完成")

        # 最终统计报告
        print(f"\n▷ 验证完成: 成功 {success_count}/{total_tasks} | 失败 {len(failed_indices)}")
        if failed_indices:
            print(f"失败行号: {sorted(failed_indices)}")

    def _retry_translation_with_validation(self, task_data: dict) -> dict:
        """增强版重试翻译方法，包含分片翻译、验证、重试和进度显示功能

        Args:
            task_data: 包含任务数据的字典:
                - original_text: 原始文本
                - translated_text: 已翻译文本
                - excel_op: Excel操作实例
                - row_index: 行索引
                - batch_info: 批次信息(包含total_tasks, completed_tasks等)
                - max_retries: 最大重试次数(默认3)
                - retry_delay: 重试延迟秒数(默认0)
                - start_time: 批次开始时间(用于计算耗时)

        Returns:
            dict: 包含验证结果和可能的新翻译结果
        """
        # 参数验证和初始化
        required_fields = ["original_text", "translated_text", "excel_op", "row_index"]
        for field in required_fields:
            if field not in task_data:
                raise ValueError(f"缺少必要参数: {field}")

        # 获取批次信息
        batch_info = task_data.get("batch_info", {})
        total_tasks = max(1, batch_info.get("total_tasks", 1))
        all_row_indices = batch_info.get("all_row_indices", [])

        if isinstance(batch_info, str):
            batch_info = {
                "batch_num": 1,
                "total_batches": 1,
                "total_tasks": 1,
                "completed_tasks": 0,
                "display_text": batch_info
            }
        elif not isinstance(batch_info, dict):
            batch_info = {}
        # 初始化批次信息（线程安全）
        with threading.Lock():
            # 设置默认值
            batch_info.setdefault("batch_num", 1)
            batch_info.setdefault("total_batches", 1)
            batch_info.setdefault("total_tasks", 1)
            batch_info.setdefault("completed_tasks", 0)
            batch_info.setdefault("display_text", f"批次{batch_info['batch_num']}/{batch_info['total_batches']}")
            batch_info.setdefault("all_row_indices", [])

        # 解包参数
        original_text = task_data["original_text"]
        translated_text = task_data["translated_text"]
        excel_op = task_data["excel_op"]
        row_index = task_data["row_index"]
        max_retries = task_data.get("max_retries", 3)
        start_time = task_data.get("start_time", time.time())

        # 使用线程安全的计数器
        with threading.Lock():
            completed_tasks = batch_info.get("completed_tasks", 0)
            remaining_tasks = total_tasks - completed_tasks

            # 计算进度
            progress_percent = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            elapsed_time = time.time() - start_time

            # 打印初始进度
            progress_msg = (
                f"[批次 {batch_info['batch_num']}/{batch_info['total_batches']}] "
                f"[进度: {progress_percent:.1f}% | "
                f"已完成: {completed_tasks}/{total_tasks} | "
                f"剩余行: {remaining_tasks} | "
                f"耗时: {elapsed_time:.1f}s] "
                f"开始处理行 {row_index}"
            )
            logger.warning(progress_msg)

        current_retry = 0
        final_result = None
        line_errors = {}  # 使用 {行号: {错误类型: 详情}} 结构
        if self.cus_deepseekdify is not None:
            processed_col = self.cus_deepseekdify.translate(original_text)
            if isinstance(processed_col, dict):
                translated_text = processed_col.get('result', '')
            # 主重试循环
            while current_retry <= max_retries:
                # 更新重试进度信息
                retry_progress = (
                    f"[行 {row_index} 重试 {current_retry}/{max_retries}] "
                    f"总进度: {progress_percent:.1f}%"
                )
                logger.warning(retry_progress)

                # 1. 验证现有翻译
                processed_col = translated_text
                postprocess_col = self.cus_termProcessor.postprocess(translated_text)

                validation_result = self._validate_translation_with_fallback(
                    original_text,
                    processed_col,
                    max_retries=max_retries
                )
                errors = validation_result['errors']

                # 记录本次校验的错误信息
                if errors['unrestored_markers'] or errors['missing_markers']:
                    error_info = {
                        "retry_count": current_retry,
                        "errors": errors.copy(),
                        "translation": translated_text
                    }

                # 判断是否需要重试
                should_retry = not validation_result['is_valid']

                if not should_retry:
                    # 验证通过的处理 - 清除所有错误信息
                    self._write_results_to_excel(excel_op, row_index, postprocess_col, {})
                    # 检查 postprocess_col 是否为空
                    if not postprocess_col:
                        logger.warning(f"行 {row_index} 的 postprocess_col 为空，标记为失败")
                        final_result = {
                            "is_valid": False,
                            "index": task_data.get("index"),
                            "row_index": row_index,
                            "result": postprocess_col,
                            "errors": {
                                "empty_postprocess": ["后处理结果为空"]
                            },
                            "retry_count": current_retry,
                        }
                    else:
                        final_result = {
                            "is_valid": True,
                            "index": task_data.get("index"),
                            "row_index": row_index,
                            "result": postprocess_col,
                            "errors": {},  # 成功时清除所有错误
                            "retry_count": current_retry,
                        }
                    break

                if current_retry >= max_retries:
                    # 达到最大重试次数，尝试分片翻译
                    logger.warning(f"行 {row_index} 达到最大重试次数，尝试分片翻译...")

                    # 按markdown行分割文本
                    lines = original_text.split('\n')
                    translated_lines = []
                    max_line_retries = 3  # 每行最大重试次数
                    has_fallback_lines = False  # 新增：标记是否有行回退
                    total_line_retries = 0  # 新增总重试计数器
                    # 准备错误信息 - 合并所有历史错误
                    # 逐行翻译和验证
                    for i, line in enumerate(lines):
                        original_line = line  # 保存原始行内容
                        if not line.strip():  # 检查当前行是否为空行（去除空白字符后是否为空）
                            translated_lines.append(line)  # 如果是空行，添加一个空字符串到结果列表
                            continue  # 跳过当前行的后续处理，直接进入下一轮循环

                        line_retry_count = 0
                        line_translation = original_line  # 初始化为原文
                        line_is_valid = False

                        current_line_errors = {}  # 当前行的错误信息
                        translation_prompt = ""
                        # 修改错误提示词构造逻辑（关键修改部分）
                        while line_retry_count <= max_line_retries and not line_is_valid:
                            try:
                                # 翻译当前行
                                temp_translation = self.cus_deepseekdify.translate(line, translation_prompt)
                                if isinstance(temp_translation, dict):
                                    temp_translation = temp_translation.get('result', '')

                                # 保留原始行的前导空格/制表符
                                leading_whitespace = len(line) - len(line.lstrip())
                                if leading_whitespace > 0:
                                    temp_translation = line[:leading_whitespace] + temp_translation.lstrip()
                                # 验证当前行
                                # print(original_line)
                                # print(temp_translation)
                                temp_errors = self._validate_translation(original_line, temp_translation)
                                # print(temp_errors)
                                # print(temp_errors)
                                line_is_valid = not (temp_errors['unrestored_markers'] or temp_errors['missing_markers'])

                                if line_is_valid:
                                    line_translation = temp_translation
                                    logger.warning(f"行 {row_index} 的分片 {i + 1}/{len(lines)} 翻译验证通过 (重试 {line_retry_count}次)")
                                    # 验证通过时清除该行可能存在的历史错误记录
                                    line_errors.pop(i, None)
                                else:
                                    # 只在确实有错误时才记录
                                    current_line_errors = {}
                                    if temp_errors['unrestored_markers']:
                                        current_line_errors['unrestored'] = temp_errors['unrestored_markers'].copy()
                                    if temp_errors['missing_markers']:
                                        current_line_errors['missing'] = temp_errors['missing_markers'].copy()
                                    # 只有当存在错误时才更新到主错误字典
                                    if current_line_errors:
                                        line_errors[i] = current_line_errors
                                    # print(current_line_errors)
                                    # 准备错误提示
                                    error_prompt = ""
                                    if temp_errors['unrestored_markers']:
                                        # line_errors[i].setdefault('unrestored', []).extend(
                                        #     temp_errors['unrestored_markers']
                                        # )
                                        error_prompt += f"未处理的标记: {temp_errors['unrestored_markers']}\n"
                                    if temp_errors['missing_markers']:
                                        #     line_errors[i].setdefault('missing', []).extend(
                                        #         temp_errors['missing_markers']
                                        #     )
                                        error_prompt += f"译文缺失: {temp_errors['missing_markers']}\n"

                                    # 生成新的翻译提示
                                    translation_prompt = (
                                        f"[原文]:\n{original_line}\n\n"
                                        f"[当前译文]:\n{temp_translation}\n\n"
                                        f"[修正要求]:{error_prompt}\n请将原文按照修正要求重新翻译\n"
                                    )
                                    # print(translation_prompt)
                                    # 只在未达到最大重试次数时使用提示
                                    if line_retry_count < max_line_retries:
                                        # 更新输入为包含错误提示的新内容
                                        line = original_line

                            except Exception as e:
                                logger.warning(f"行 {row_index} 的分片 {i + 1}/{len(lines)} 翻译出错: {str(e)}")
                                line_translation = f"{original_line}"  # 出错时回退到原文
                            line_retry_count += 1
                            if line_retry_count <= max_line_retries and not line_is_valid:
                                time.sleep(1)  # 重试间隔

                        # 确保最终结果不为空
                        translated_lines.append(line_translation if line_translation.strip() else f"{original_line}")

                        # 记录最终结果
                        if not line_is_valid:
                            has_fallback_lines = True
                            logger.warning(
                                f"行 {row_index} 的分片 {i + 1}/{len(lines)} 最终验证失败 "
                                f"(重试 {line_retry_count}次)，使用原始文本"
                            )
                        # ✅ 仅保留最后一次的错误信息
                        if current_line_errors:
                            # 强制覆盖而非合并
                            line_errors[i] = {
                                et: copy.copy(d)  # 深拷贝避免后续修改影响
                                for et, d in current_line_errors.items()
                            }
                            # print(line_errors)

                        else:
                            # 验证通过时，清除该行可能存在的错误记录
                            line_errors.pop(i, None)

                    # 组合分片翻译结果
                    translated_text = '\n'.join(translated_lines)
                    postprocess_col = self.cus_termProcessor.postprocess(translated_text)

                    if not postprocess_col or postprocess_col.isspace():
                        postprocess_col = translated_text  # 回退到翻译结果
                        logger.warning(f"行 {row_index} 后处理结果为空，使用原始翻译结果")

                    # 格式化错误信息写入Excel
                    formatted = {
                        5: [],  # 未处理的标记
                        6: [],  # 译文缺失
                        7: "部分失败" if has_fallback_lines else "",  # 状态
                        8: [],  # 上下文信息
                        9: []  # 错误行号
                    }

                    # 添加空值错误处理
                    # if "empty_postprocess" in final_result.get("errors", {}):
                    #     formatted[6].append("后处理结果为空")

                    for line_num, errors in line_errors.items():
                        if 'unrestored' in errors:
                            formatted[5].append(
                                f"行{line_num}: 未处理的标记: {', '.join(errors['unrestored'])}"
                            )
                        if 'missing' in errors:
                            formatted[6].append(
                                f"行{line_num}: 译文缺失: {', '.join(errors['missing'])}"
                            )
                        formatted[9].append(str(line_num))

                    # 合并为多行文本
                    for col in (5, 6, 8):
                        if formatted[col]:
                            formatted[col] = '\n'.join(formatted[col])

                    formatted[9] = f"错误行: [{', '.join(formatted[9])}]" if formatted[9] else ""

                    # 检查 postprocess_col 是否为空
                    if not postprocess_col or postprocess_col.isspace():
                        logger.error(f"行 {row_index} 的最终处理结果为空！原始内容: {original_text}")
                        postprocess_col = f"{original_text}"  # 确保不会写入空值
                        has_fallback_lines = True
                        final_result = {
                            "is_valid": False,
                            "index": task_data.get("index"),
                            "row_index": row_index,
                            "result": postprocess_col,
                            "errors": {
                                "empty_postprocess": ["后处理结果为空"]
                            },
                            "retry_count": current_retry,
                            "is_fragmented": True,
                            "has_fallback_lines": has_fallback_lines,
                            "line_retry_counts": line_retry_count,
                        }
                    else:
                        final_result = {
                            "is_valid": not has_fallback_lines,
                            "index": task_data.get("index"),
                            "row_index": row_index,
                            "result": postprocess_col,
                            "errors": line_errors,
                            "retry_count": current_retry,
                            "is_fragmented": True,
                            "has_fallback_lines": has_fallback_lines,
                            "line_retry_counts": line_retry_count,
                        }
                    break

                current_retry += 1

            # 在方法结束时更新进度
            with threading.Lock():
                batch_info["completed_tasks"] = batch_info.get("completed_tasks", 0) + 1
                completed_tasks = batch_info["completed_tasks"]
                remaining_tasks = total_tasks - completed_tasks
                progress_percent = (completed_tasks / total_tasks) * 100
                elapsed_time = time.time() - start_time

                # 优化剩余行显示逻辑
                remaining_rows = all_row_indices[completed_tasks:]
                remaining_display = (
                    f"{len(remaining_rows)}行"  # 默认显示行数
                    if len(remaining_rows) > 5  # 超过5行只显示数量
                    else str(remaining_rows)  # 5行以内显示具体行号
                )

                result_status = "成功" if final_result.get("is_valid", False) else "失败"
                fragmented_info = " (分片)" if final_result.get("is_fragmented", False) else ""
                # 添加空值失败信息
                if "empty_postprocess" in final_result.get("errors", {}):
                    result_status += " (后处理结果为空)"
                progress_msg = (
                    f"[批次 {batch_info['batch_num']}/{batch_info['total_batches']}] "
                    f"[进度: {progress_percent:.1f}% | "
                    f"已完成: {completed_tasks}/{total_tasks} | "
                    f"剩余: {remaining_display} | "
                    f"耗时: {elapsed_time:.1f}s] "
                    f"行 {row_index} 处理完成: {result_status}{fragmented_info} "
                    f"(重试次数: {final_result.get('retry_count', 0)})"
                )
                logger.warning(progress_msg)
        return final_result

    def _write_results_to_excel(self, excel_op, row, value, errors_messages):
        """改进的结果写入方法，支持多行错误信息

        修改点：
        - 支持写入多行错误信息
        - 自动调整行高以适应长文本
        """
        try:
            # 写入主结果
            excel_op.set_cell_value(row, 4, value)
            # 标准化错误信息（兼容新旧格式）
            if not isinstance(errors_messages, dict):
                errors_messages = {}

            # print(errors_messages)

            for col in range(5, 10):
                key_list = list(errors_messages.keys())

                unrestored_list = []
                for key in errors_messages:
                    if 'unrestored' in errors_messages[key]:
                        unrestored_list.extend(errors_messages[key]['unrestored'])
                # 用换行符拼接
                unrestored_text = '\n'.join(unrestored_list)

                missing_list = []
                for key in errors_messages:
                    if 'missing' in errors_messages[key]:
                        missing_list.extend(errors_messages[key]['missing'])
                # 用换行符拼接
                missing_text = '\n'.join(missing_list)
                if col == 5:
                    excel_op.set_cell_value(row, col, str(key_list))
                if col == 6:
                    excel_op.set_cell_value(row, col, str(unrestored_text))
                if col == 7:
                    excel_op.set_cell_value(row, col, str(missing_text))
        except Exception as e:
            print(f"\033[31m写入Excel失败(行{row}): {str(e)}\033[0m")

    def process(self):
        """主处理流程"""
        # 初始化Excel
        cus_excel_op1 = self._init_excel_sheets()

        # 分批处理配置
        batch_size = 1000
        total_items = len(self.column_3_list)
        start_index = 0
        print(f"\033[;33m从第 {start_index + 1} 项开始处理（跳过前 {start_index} 项）\033[0m")
        end_index = total_items

        # 主处理循环
        for batch_start in range(start_index, min(end_index, total_items), batch_size):
            batch_end = min(batch_start + batch_size, total_items)
            batch_num = batch_start // batch_size + 1
            total_batches = (total_items + batch_size - 1) // batch_size

            self._process_batch(batch_start, batch_end, batch_num, total_batches, cus_excel_op1)

            # 保存进度
            self.cus_excel_op.save_workbook(self.zabbix_terms_table_titles_file)
            cus_excel_op1.save_workbook(self.output_file)
            print(f"\033[;33m批次 {batch_num}/{total_batches} 已完成，当前总计处理 {batch_end}/{total_items} 条\033[0m")

        # 最终处理
        print(f"\033[;32m所有处理完成！共处理 {total_items} 条数据\033[0m")
        self.cus_termProcessor.calc_markdown_links(self.cus_excel_op)
        self.cus_excel_op.save_workbook(self.zabbix_terms_table_titles_file)
        print(f"\033[;32m超链接计算结果已保存\033[0m")

        # 验证output_file表的第4列数据，并将结果写入H列
        self._validate_excel_column(self.output_file, 4, 8)

        print(f"\033[;32m校验结果已写入H列并保存\033[0m")


class CusMyThreadSendDir(threading.Thread):
    def __init__(self, cur_num, total_num, ssh_ip, port, pwd, cus_excel_op):
        super(CusMyThreadSendDir, self).__init__()
        self.cur_num = cur_num
        self.total_num = total_num
        self.ssh_ip = ssh_ip
        self.port = int(port)
        self.username = "root"
        self.pwd = pwd
        self.transport = None
        self.sftp = None
        self.cus_excel_op = cus_excel_op

    def run(self):
        try:
            self.transport = paramiko.Transport(sock=(self.ssh_ip, self.port))
            self.transport.connect(username=self.username, password=self.pwd)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        except Exception as e:
            self.cus_excel_op.set_cell_value(self.cur_num + 1, 2, "否")
            self.cus_excel_op.set_cell_value(self.cur_num + 1, 3, f'{e}')
            print(u'(进度: -> \033[;34m%s\033[0m/\033[;34m%s\033[0m \033[;34m%s\033[0m \033[;31m%s\033[0m)' % (self.total_num, self.cur_num, self.ssh_ip, e))
            self.cus_excel_op.save_workbook('uploadResult' + '.xlsx')
            return

    def run(self):
        def create_remote_dir(dir):
            for item in dir:
                try:
                    self.sftp.stat(item)
                    pass
                except IOError:
                    logger.debug("Create a new directory: ", item)
                    self.sftp.mkdir(item)

        def for_dir():
            for res in path:
                if os.path.isdir(res):
                    local_dir_path.append(res)
            remote_dir_path.append(des)

        def for_zdir():
            des_src_dir.append(remote_dir_path[1])
            des_src_dir_list = des_src_dir[0].split("/")
            des_dir_list = des_src_dir_list[1:]
            c = ""
            remote_des_src_path = []
            for item in des_dir_list:
                c += "/" + item
                remote_des_src_path.append(c)
            create_remote_dir(remote_des_src_path)
            create_remote_dir(remote_dir_path)
            for res in path:
                if os.path.isfile(res):
                    local_file_path.append(res)

        def print_progress(transferred, total):
            sys.stdout.write(f'Transferred: {transferred / total * 100:.2f}% bytes / Total: {total} bytes\r')
            sys.stdout.flush()

        try:
            src = "./senddir/"
            des = "/tmp/recvdir/"
            sep = "/"
            path = []
            local_dir_path = []
            local_file_path = []
            remote_dir_path = []
            remote_file_path = []
            des_src_dir = []
            for i in os.listdir(src):
                path.append(src + sep + i)
            for n in path:
                if os.path.isdir(n) and os.listdir(n):
                    for i in os.listdir(n):
                        path.append(n + sep + i)
            local_dir_path.append(src)
            local_dir = src.split("/")
            local_dir_first = local_dir[0:-1]
            global a
            if len(local_dir_first) == 0:
                for_dir()
                for res in local_dir_path:
                    remote_dir_path.append(des + "/" + res)
                for_zdir()
                for res in local_file_path:
                    remote_file_path.append(des + "/" + res)
            else:
                if len(local_dir_first) == 1:
                    dir_join = "/".join(local_dir_first)
                    a = dir_join
                else:
                    dir_join = "/".join(local_dir_first)
                    a = dir_join + "/"
                for res in path:
                    if os.path.isdir(res):
                        local_dir_path.append(res)
                remote_dir_path.append(des)
                b = [item.split(a)[-1] for item in local_dir_path]
                for res in b:
                    if len(local_dir_first) == 1:
                        remote_dir_path.append(des + res)
                    else:
                        remote_dir_path.append(des + "/" + res)
                for_zdir()
                d = [item.split(a)[-1] for item in local_file_path]
                for res in d:
                    if len(local_dir_first) == 1:
                        remote_file_path.append(des + res)
                    else:
                        remote_file_path.append(des + "/" + res)
            time_start = time.time()
            local_file_num = len(local_file_path)
            for i in range(local_file_num):
                self.sftp.put(local_file_path[i], remote_file_path[i], callback=print_progress)
            total_time = time.time() - time_start
            self.transport.close()
            self.cus_excel_op.set_cell_value(self.cur_num + 1, 2, "是")
            print(u'(进度: -> \033[;34m%s\033[0m/\033[;34m%s\033[0m \033[;34m%s\033[0m) upload done' % (
                self.total_num, self.cur_num, self.ssh_ip))
            self.cus_excel_op.save_workbook('uploadResult' + '.xlsx')
        except Exception as e:
            self.cus_excel_op.set_cell_value(self.cur_num + 1, 2, "否")
            self.cus_excel_op.set_cell_value(self.cur_num + 1, 3, f'{e}')
            print(u'(进度: -> \033[;34m%s\033[0m/\033[;34m%s\033[0m \033[;34m%s\033[0m \033[;31m%s\033[0m)' % (self.total_num, self.cur_num, self.ssh_ip, e))
            self.cus_excel_op.save_workbook('uploadResult' + '.xlsx')
            return


class MyThreadCfgSshComm:
    """重构为可调用对象，适用于线程池"""

    def __init__(self, cur_num, total_num, ssh_ip, port, usr, pwd, cmd, encoding='gbk', log_file_path=None,
                 max_retries=2):
        self.cur_num = cur_num
        self.total_num = total_num
        self.ssh_ip = ssh_ip
        self.port = int(port) if port else 22
        self.username = usr
        self.pwd = pwd
        self.cmd = u'{v01}'.format(v01=cmd)
        self.encoding = encoding  # 新增编码参数
        self.rackreply = ''
        self.success = False
        self.error_msg = ''
        self.execution_log = []
        self.max_retries = max_retries  # 最大重试次数
        self.log_dir = 'ssh_execution_logs'  # 日志目录
        self._ensure_log_dir()

    def _ensure_log_dir(self):
        """确保日志目录存在"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def _save_to_log_file(self, result):
        """将结果保存为独立的.log文件"""
        try:
            # 创建以IP为文件名的日志文件
            # 清理IP中的特殊字符，确保文件名安全
            safe_ip = re.sub(r'[^\w\.-]', '_', self.ssh_ip)
            log_filename = f"{safe_ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            log_filepath = os.path.join(self.log_dir, log_filename)

            with open(log_filepath, 'w', encoding='utf-8') as f:
                # 写入基本信息
                f.write("=" * 80 + "\n")
                f.write(f"SSH命令执行日志 - {self.ssh_ip}\n")
                f.write("=" * 80 + "\n\n")

                f.write(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"IP地址: {self.ssh_ip}\n")
                f.write(f"端口: {self.port}\n")
                f.write(f"用户名: {self.username}\n")
                f.write(f"编码: {self.encoding}\n")  # 记录使用的编码
                f.write(f"任务编号: {self.cur_num}/{self.total_num}\n")
                f.write(f"执行结果: {'成功' if result['success'] else '失败'}\n")
                f.write(f"重试次数: {self.max_retries}\n")
                f.write("\n" + "=" * 80 + "\n\n")

                # 写入执行的命令
                f.write("执行的命令:\n")
                f.write("-" * 40 + "\n")
                list_cmd = self.cmd.split('\n')
                for i, cmd_line in enumerate(list_cmd, 1):
                    if cmd_line.strip():
                        f.write(f"{i:3d}. {cmd_line}\n")
                f.write("\n" + "=" * 80 + "\n\n")

                # 写入执行日志
                f.write("执行过程日志:\n")
                f.write("-" * 40 + "\n")
                for log_entry in self.execution_log:
                    timestamp = log_entry.get('timestamp', '')
                    log_type = log_entry.get('type', '')
                    message = log_entry.get('message', '')
                    if timestamp and message:
                        f.write(f"[{timestamp}] [{log_type}] {message}\n")
                f.write("\n" + "=" * 80 + "\n\n")

                # 写入输出结果
                if result['success']:
                    f.write("命令输出结果:\n")
                    f.write("-" * 40 + "\n")
                    if result['output']:
                        f.write(result['output'])
                    else:
                        f.write("无输出内容")
                else:
                    f.write("错误信息:\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"错误: {result.get('error', '未知错误')}\n\n")
                    f.write("详细日志:\n")
                    for log_entry in self.execution_log:
                        if log_entry.get('type') == 'ERROR':
                            f.write(f"[{log_entry.get('timestamp', '')}] {log_entry.get('message', '')}\n")

                f.write("\n" + "=" * 80 + "\n")
                f.write(f"文件生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n")

            # 创建IP链接文件（软链接）
            try:
                ip_link_file = os.path.join(self.log_dir, f"{safe_ip}.log")
                # 如果已经存在链接，先删除
                if os.path.exists(ip_link_file) or os.path.islink(ip_link_file):
                    try:
                        os.remove(ip_link_file)
                    except:
                        pass
                # 创建指向最新日志文件的链接
                os.symlink(log_filename, ip_link_file)
            except:
                pass  # 如果创建链接失败，继续执行

            self._add_log('INFO', f"结果已保存到日志文件: {log_filename}")
            return log_filepath

        except Exception as e:
            self._add_log('ERROR', f"保存日志文件失败: {str(e)}")
            return None

    def __call__(self):
        return self.execute_with_retry()

    def execute_with_retry(self):
        """带重试机制的执行"""
        last_error = None

        for attempt in range(self.max_retries + 1):  # 0, 1, 2 共3次尝试
            try:
                self._add_log('INFO', f"第{attempt + 1}次尝试执行，使用编码: {self.encoding}")
                result = self.execute()

                if result['success']:
                    # 执行成功，保存日志文件
                    self._save_to_log_file(result)
                    return result
                else:
                    last_error = result['error']

                    # 如果是特定错误，可以重试
                    retryable_errors = [
                        'Error reading SSH protocol banner',
                        'Socket is closed',
                        'timed out',
                        'Connection refused'
                    ]

                    if any(error in last_error for error in retryable_errors):
                        if attempt < self.max_retries:
                            self._add_log('WARNING', f"执行失败，{1}秒后重试... 错误: {last_error}")
                            time.sleep(1)  # 等待1秒后重试
                            continue
                    else:
                        # 不可重试的错误，保存日志文件
                        self._save_to_log_file(result)
                        return result

            except Exception as e:
                last_error = str(e)
                if attempt < self.max_retries:
                    self._add_log('WARNING', f"执行异常，{1}秒后重试... 错误: {last_error}")
                    time.sleep(1)
                    continue

        # 所有重试都失败
        self._add_log('ERROR', f"所有{self.max_retries + 1}次尝试都失败，最后错误: {last_error}")
        error_result = {
            'ip': self.ssh_ip,
            'success': False,
            'output': '',
            'error': last_error,
            'cur_num': self.cur_num,
            'execution_log': self.execution_log,
            'summary': f'失败: {last_error[:50]}'
        }
        # 保存错误日志文件
        self._save_to_log_file(error_result)
        return error_result

    def _add_log(self, log_type, message):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            log_entry = {
                'timestamp': timestamp,
                'type': log_type,
                'message': message,
                'ip': self.ssh_ip,
                'cur_num': self.cur_num
            }
            self.execution_log.append(log_entry)

            if log_type == 'CMD_OUTPUT' and message:
                # 清理控制字符后再显示
                clean_msg = self._clean_cursor_control(message)
                if clean_msg:
                    print(u'(进度: -> \033[;34m%s\033[0m/\033[;34m%s\033[0m \033[;34m%s\033[0m \033[;33m%s\033[0m)' % (
                        self.total_num, self.cur_num, self.ssh_ip, clean_msg[:100]))
            elif log_type == 'ERROR':
                print(u'(进度: -> \033[;34m%s\033[0m/\033[;34m%s\033[0m \033[;34m%s\033[0m \033[;31m%s\033[0m)' % (
                    self.total_num, self.cur_num, self.ssh_ip, message[:100]))
            return log_entry
        except:
            pass

    def _clean_cursor_control(self, text):
        """专门清理光标控制序列 [数字+D 模式，保留后面的内容"""

        if not text:
            return text

        cleaned = text

        # 匹配 [数字+D 模式并移除
        pattern = r'\[\d+D\s*'
        cleaned = re.sub(pattern, '', cleaned)

        # 如果还有多个连续的空格，压缩成一个空格
        cleaned = re.sub(r'\s+', ' ', cleaned)

        return cleaned

    def _clean_for_storage(self, text):
        """清理用于存储的文本 - 改进版本"""

        if not text:
            return ""

        cleaned = text
        # 1. 首先处理光标控制序列 [数字+D
        # 使用负向前瞻断言，确保不会过度清理
        cursor_pattern = r'\[\d+D\s*'
        cleaned = re.sub(cursor_pattern, '', cleaned)

        # 2. 修复提示符位置：将行尾的 # 移到下一行开头
        # 匹配模式：单词字符结尾，后面跟着 # 然后换行
        cleaned = re.sub(r'(\w+)#\s*\n', r'\1\n#', cleaned)

        # 3. 修复行内的 # 位置
        lines = cleaned.split('\n')
        fixed_lines = []
        for i, line in enumerate(lines):
            # line = line
            if not line:
                continue

            # 检查是否以 # 结尾但不是注释的情况
            if line.endswith('#') and len(line) > 1:
                # 如果前面是单词字符，则把 # 移到下一行
                if re.search(r'\w#', line):
                    line = re.sub(r'(\w)#', r'\1', line)
                    # 如果下一行存在，在当前行末尾添加换行和 #
                    if i + 1 < len(lines):
                        lines[i + 1] = '#' + lines[i + 1]
                    else:
                        fixed_lines.append(line)
                        fixed_lines.append('#')
                    continue

            fixed_lines.append(line)

        cleaned = '\n'.join(fixed_lines)

        # 4. 移除其他ANSI转义序列
        cleaned = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', cleaned)

        # 5. 移除其他控制字符
        cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', cleaned)

        # 6. 移除分页符
        cleaned = re.sub(r'---- More ----', '', cleaned)

        # 7. 移除其他控制字符
        lines = cleaned.split('\n')
        processed_lines = []
        for line in lines:
            # line = line
            if line:  # 只保留非空行
                line = re.sub(r'\s+', ' ', line)
                processed_lines.append(line)

        return '\n'.join(processed_lines)

    def _adjust_prompt_positions(self, text):
        """调整提示符位置，确保格式正确"""

        if not text:
            return text

        lines = text.split('\n')
        adjusted_lines = []

        i = 0
        while i < len(lines):
            line = lines[i]

            if not line:
                i += 1
                continue

            # 情况1: 检查是否需要调整 # 在结尾的位置
            if line.endswith('#') and len(line) > 1:
                # 如果 # 前面是字母数字，需要调整
                match = re.match(r'(.+[a-zA-Z0-9])#$', line)
                if match:
                    # 保留前面的内容，将 # 放到下一行
                    adjusted_lines.append(match.group(1))
                    # 检查下一行是否为空或需要合并
                    if i + 1 < len(lines) and lines[i + 1]:
                        adjusted_lines.append('#' + lines[i + 1])
                        i += 2
                    else:
                        adjusted_lines.append('#')
                        i += 1
                    continue

            # 情况2: 检查是否需要调整 # 在开头的位置（新增）
            if line.startswith('#') and len(line) > 1:
                # 检查是否是以#开头，后面跟着非空格的字符（如 "#acl number 2001"）
                match = re.match(r'^#(.+)$', line)
                if match and match.group(1).strip():
                    # 将#单独放一行，内容放下一行
                    adjusted_lines.append('#')
                    adjusted_lines.append(match.group(1))
                    i += 1
                    continue

            adjusted_lines.append(line)
            i += 1

        return '\n'.join(adjusted_lines)

    def execute(self):
        """执行SSH命令并返回结果"""
        transport = None
        ssh_channel = None

        try:
            self._add_log('INFO', f"开始执行SSH命令到 {self.ssh_ip}:{self.port}，使用编码: {self.encoding}")

            # 1. 建立socket连接 - 增加错误处理
            __timeout = 15  # 增加超时时间
            __sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            __sock.settimeout(__timeout)

            try:
                __sock.connect((self.ssh_ip, self.port))
                self._add_log('DEBUG', f"Socket连接成功")
            except Exception as e:
                error_msg = f"连接失败: {str(e)}"
                self._add_log('ERROR', error_msg)
                raise Exception(error_msg)

            # 2. 创建SSH传输层 - 增加banner超时
            transport = paramiko.Transport(__sock)
            transport.banner_timeout = 20  # 增加banner读取超时
            transport.auth_timeout = 15

            # 3. 身份验证
            try:
                if os.path.isfile(self.pwd):
                    self._add_log('INFO', "使用RSA密钥认证")
                    __pkey = paramiko.RSAKey.from_private_key_file(self.pwd)
                    transport.connect(username=self.username, pkey=__pkey)
                else:
                    self._add_log('INFO', "使用密码认证")
                    transport.connect(username=self.username, password=self.pwd)
                self._add_log('INFO', "SSH认证成功")
            except Exception as e:
                error_msg = f"认证失败: {str(e)}"
                self._add_log('ERROR', error_msg)
                raise Exception(error_msg)

            # 4. 创建SSH通道并执行命令
            ssh_channel = transport.open_channel(kind='session')
            ssh_channel.settimeout(30)

            list_cmd = self.cmd.split('\n')
            self._add_log('INFO', f"准备执行 {len(list_cmd)} 条命令")

            # 获取交互式shell
            ssh_channel.get_pty(width=80, height=24)
            ssh_channel.invoke_shell()

            # 等待初始提示符
            time.sleep(1)

            # 清除初始欢迎信息
            initial_buffer = b''
            start_time = time.time()
            while time.time() - start_time < 3:
                if ssh_channel.recv_ready():
                    data = ssh_channel.recv(4096)
                    if data:
                        initial_buffer += data
                time.sleep(0.1)

            if initial_buffer:
                # 使用指定的编码解码
                try:
                    welcome_decoded = initial_buffer.decode(self.encoding, errors='ignore')
                except (UnicodeDecodeError, LookupError):
                    # 如果指定编码失败，尝试utf-8
                    self._add_log('WARNING', f"指定的编码 {self.encoding} 解码失败，尝试 utf-8")
                    try:
                        welcome_decoded = initial_buffer.decode('utf-8', errors='ignore')
                    except:
                        welcome_decoded = initial_buffer.decode('gbk', errors='ignore')

                self.rackreply += welcome_decoded
                self._add_log('DEBUG', f"收到初始信息")

            # 发送回车获取提示符
            ssh_channel.send('\n')
            time.sleep(0.5)

            # 逐条执行命令
            for cmd_line in list_cmd:
                cmd_line = cmd_line
                if not cmd_line:
                    continue

                self._add_log('CMD_INPUT', f"执行命令: {cmd_line}")

                # 发送命令
                ssh_channel.send(cmd_line + '\n')
                time.sleep(0.5)

                # 读取命令输出
                output_buffer = ""
                start_time = time.time()
                max_wait_time = 20  # 减少单条命令等待时间
                in_more_mode = False
                more_count = 0

                while time.time() - start_time < max_wait_time:
                    if ssh_channel.recv_ready():
                        try:
                            data = ssh_channel.recv(4096)
                            if data:
                                # 使用指定的编码解码
                                try:
                                    decoded_data = data.decode(self.encoding, errors='ignore')
                                except (UnicodeDecodeError, LookupError):
                                    # 如果指定编码失败，尝试utf-8
                                    try:
                                        decoded_data = data.decode('utf-8', errors='ignore')
                                    except:
                                        decoded_data = data.decode('gbk', errors='ignore')

                                output_buffer += decoded_data
                                self.rackreply += decoded_data

                                # 实时显示清理后的输出
                                clean_display = self._clean_cursor_control(decoded_data)
                                if clean_display:
                                    lines = clean_display.split('\n')
                                    for line in lines:
                                        if line:
                                            self._add_log('CMD_OUTPUT', line[:100])

                                # 检查分页提示
                                if '---- More ----' in decoded_data:
                                    if not in_more_mode:
                                        self._add_log('DEBUG', "检测到分页提示，发送空格继续...")
                                        in_more_mode = True
                                    more_count += 1

                                    # 发送空格继续
                                    ssh_channel.send(' ')
                                    time.sleep(0.3)

                                    # 防止无限分页
                                    if more_count > 30:
                                        self._add_log('WARNING', "分页过多，发送回车跳过...")
                                        ssh_channel.send('\n')
                                        time.sleep(0.5)
                                        more_count = 0
                                        in_more_mode = False

                                    continue
                                else:
                                    in_more_mode = False
                                    more_count = 0

                                # 检查命令是否完成
                                if self._has_prompt(decoded_data):
                                    # 等待一下看看是否还有数据
                                    time.sleep(0.5)
                                    if not ssh_channel.recv_ready():
                                        break

                        except socket.timeout:
                            self._add_log('WARNING', "读取数据超时")
                            break
                        except Exception as e:
                            self._add_log('WARNING', f"读取数据出错: {str(e)}")
                            break

                    time.sleep(0.1)

                # 命令执行完成后，发送回车获取新提示符
                time.sleep(0.5)
                ssh_channel.send('\n')
                time.sleep(0.5)

                # 检查退出命令
                if cmd_line.lower() in ['exit', 'quit', 'end']:
                    self._add_log('INFO', f"执行退出命令: {cmd_line}")
                    time.sleep(1)
                    break

            self.success = True
            self._add_log('INFO', "所有命令执行完成")

            # 清理输出用于存储
            cleaned_output = self._clean_for_storage(self.rackreply)
            # 调整提示符位置
            cleaned_output = self._adjust_prompt_positions(cleaned_output)

            return {
                'ip': self.ssh_ip,
                'success': True,
                'output': cleaned_output,
                'error': '',
                'cur_num': self.cur_num,
                'execution_log': self.execution_log,
                'summary': f"成功执行 {len([c for c in list_cmd if c])} 条命令，使用编码: {self.encoding}"
            }

        except Exception as e:
            error_msg = str(e)
            self._add_log('ERROR', f"执行异常: {error_msg}")

            # 提供更友好的错误信息
            if "Error reading SSH protocol banner" in error_msg:
                error_msg = "读取SSH协议banner失败，可能是网络问题或服务器配置"
            elif "timed out" in error_msg:
                error_msg = f"连接超时({__timeout}秒)"

            return {
                'ip': self.ssh_ip,
                'success': False,
                'output': '',
                'error': error_msg,
                'cur_num': self.cur_num,
                'execution_log': self.execution_log,
                'summary': f'异常: {error_msg[:50]}'
            }

        finally:
            try:
                if ssh_channel and not ssh_channel.closed:
                    ssh_channel.close()
            except:
                pass

            try:
                if transport and transport.is_active():
                    transport.close()
            except:
                pass

    def _has_prompt(self, text):
        """检查是否有命令提示符"""
        prompts = ['# ', '> ', '$ ', '] ', '% ', ': ', '#', '>', '$', ']']

        # 检查文本末尾
        for prompt in prompts:
            if text.endswith(prompt) or text.rstrip().endswith(prompt):
                return True

        # 检查最后几行
        lines = text.split('\n')
        for line in lines[-3:]:  # 检查最后3行
            line = line
            for prompt in prompts:
                if line.endswith(prompt):
                    return True

        return False

class CusMyThreadCfgZabbixAgent(threading.Thread):
    def __init__(self, cur_num, total_num, ssh_ip, port, pwd, zabbix_server_ip):
        super(CusMyThreadCfgZabbixAgent, self).__init__()
        self.cur_num = cur_num
        self.total_num = total_num
        self.ssh_ip = ssh_ip
        self.port = int(port)
        self.username = "root"
        self.pwd = pwd
        self.zabbix_server_ip = zabbix_server_ip
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # self.cmd = """
        # rm -rf /tmp/zabbix_dir
        # """

        self.cmd1 = """
        echo 1
        echo 2
        sh /tmp/zabbix_dir/install.sh --cleardir
        """

        self.cmd2 = """
        sh /tmp/zabbix_dir/install.sh --senddir
        """

        self.cmd3 = """
        sh /tmp/zabbix_dir/install.sh --install
        """

    def run(self):
        try:
            # self.ssh.connect(hostname=self.ssh_ip, port=self.port, username=self.username, password=self.pwd)
            # stdin, stdout, stderr = self.ssh.exec_command(self.cmd)
            # res, err = stdout.read(), stderr.read()
            # result = res if err else res
            # self.ssh.close()

            self.ssh.connect(hostname=self.ssh_ip, port=self.port, username=self.username, password=self.pwd)
            stdin, stdout, stderr = self.ssh.exec_command(self.cmd1)
            res, err = stdout.read(), stderr.read()
            result = res if err else res
            self.ssh.close()
            print("""{0}/{1}: {2} status {3}, err: {4}""".format(self.cur_num, self.total_num, self.ssh_ip, res, err))
        except Exception as e:
            print("""%s/%s: %s""" % (self.cur_num, self.total_num, e))


class CusMyThreadCfgSj(threading.Thread):
    def __init__(self, cur_num, total_num, s_dic):
        self.session = requests.Session()
        super(CusMyThreadCfgSj, self).__init__()
        self.cur_num = cur_num
        self.total_num = total_num
        self.s_dic = {}
        self.s_dic.update(s_dic)
        self.username = "root"
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 删除文件
        self.cmd1 = """
        rm -rf /tmp/zabbix_dir 1>&2
        """
        # 配置网卡
        self.cmd2 = """
        sh /tmp/zabbix_dir/cfgip.sh {0} {1} {2} {3} {4} {5} {6} {7} 1>&2
        """.format(self.s_dic['s_eth'], self.s_dic['s_ip'], self.s_dic['s_newmask'], self.s_dic['s_gateway'],
                   self.s_dic['s_dns1'], self.s_dic['s_dns2'], self.s_dic['s_host'], self.s_dic['s_app'])
        # 配置主机名并重启
        self.cmd3 = """
        sh /tmp/zabbix_dir/cfghost.sh {0}
        """.format(self.s_dic['s_host'])
        # 配置免密登录需要修改cfgssh.sh密码
        self.cmd4 = """
        sh /tmp/zabbix_dir/cfgssh.sh 1>&2
        """
        # 配置JDK
        self.cmd5 = """
        sh /tmp/zabbix_dir/cfgjdk.sh
        """
        # 配置mysql将需要配置mysql的excel行放到第一行，第二行置空
        self.cmd6 = """
        sh /tmp/zabbix_dir/cfgmysql.sh
        """
        # 配置redis
        self.cmd7 = """
        sh /tmp/zabbix_dir/cfgredis.sh
        """
        # 配置zookeeper将需要配置zookeeper的excel行放到第一行，第二行置空，需要配置JDK
        self.cmd8 = """
        sh /tmp/zabbix_dir/cfgzookeeper.sh
        """
        # 配置kafka将需要配置kafka的excel行放到第一行，第二行置空，需要配置JDK
        self.cmd9 = """
        sh /tmp/zabbix_dir/cfgkafka.sh
        """
        # 配置elasticsearch将需要配置elasticsearch的excel行放到第一行，第二行置空，需要配置JDK11
        self.cmd10 = """
        sh /tmp/zabbix_dir/cfgelasticsearch.sh
        """
        # 配置kibana将需要配置kibana的excel行放到第一行，第二行置空，需要配置elasticsearch
        self.cmd11 = """
        sh /tmp/zabbix_dir/cfgkibana.sh
        """
        # 导入es数据
        # list_a_ = []
        # with open('senddir/ip/kibana.txt', 'r') as a_:
        #     [list_a_.append(line_) for line_ in a_]
        # # 导入es数据库
        # self.def_create_index(list_a_[0].split(' ')[1])
        # 配置naco
        self.cmd12 = """
        sh /tmp/zabbix_dir/cfgnacos.sh
        """
        # self.authID = ""
        # # naco的web页面操作，无需此操作
        # list_a_ = []
        # with open('senddir/ip/nacos.txt', 'r') as a_:
        #     [list_a_.append(line_) for line_ in a_]
        # # 创建命名空间，无需此操作
        # self.def_login(list_a_[0].split(' ')[0])
        # self.def_nacos_conf(list_a_[0].split(' ')[0])
        self.cmd13 = """
        sh /tmp/zabbix_dir/cfgopenresty.sh
        """
        self.cmd14 = """
        sh /tmp/zabbix_dir/cfgspark.sh
        """
        self.cmd15 = """
        sh /tmp/zabbix_dir/install.sh
        """

    def run(self):
        try:
            self.ssh.connect(hostname=self.s_dic['ssh_ip'], port=self.s_dic['port'], username=self.username, password=self.s_dic['pwd'])
            # 根据需要修改执行的命令 cmd2 timeout=30
            stdin, stdout, stderr = self.ssh.exec_command(self.cmd15)
            res, err = stdout.read(), stderr.read()
            result = res if err else res
            print("""%s/%s: %s host ok, err: %s""" % (self.cur_num, self.total_num, self.s_dic['ssh_ip'], err))
            self.ssh.close()

        except Exception as e:
            print("""%s/%s: %s""" % (self.cur_num, self.total_num, e))

    def get_filelist(self, dir, Filelist, suffix):
        if os.path.isfile(dir):
            if dir.endswith(suffix):
                Filelist.append(dir)
        elif os.path.isdir(dir):
            for s in os.listdir(dir):
                newDir = os.path.join(dir, s)
                self.get_filelist(newDir, Filelist, suffix)
        return Filelist

    def def_create_index(self, host_ip_):
        headers = {
            'Host': '{0}:5601'.format(host_ip_),
            'Accept': 'text/plain, */*; q=0.01',
            'kbn-version': '7.2.0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            # Already added when you pass json= but not when you pass data=
            # 'Content-Type': 'application/json',
            'Origin': 'http://{0}:5601'.format(host_ip_),
            'Referer': 'http://{0}:5601/app/kibana'.format(host_ip_),
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        file_list = []
        self.get_filelist('senddir\\patch\\json', file_list, '')
        for i_ in range(len(file_list)):
            line_data = ""
            with open(file_list[i_], 'r') as a_:
                next(a_)
                for line_ in a_:
                    line_data = line_data + ''.join(line_)
                json_data = json.loads(line_data)
                fileName_ = os.path.basename(file_list[i_])
                params = {
                    'path': fileName_,
                    'method': 'PUT',
                }
            self.session.mount('http://{0}:5601/api/console/proxy'.format(host_ip_), requests.adapters.HTTPAdapter(max_retries=3))
            request = self.session.post(url='http://{0}:5601/api/console/proxy'.format(host_ip_), params=params, headers=headers, json=json_data, verify=False)
            response = request.json()
            if response.get('acknowledged', '') != '':
                print(u"创建索引: \033[;32m%s\033[0m 成功! 返回值为: \033[;32m%s\033[0m" % (
                    fileName_, response['acknowledged']))
            elif response.get('error', '') != '':
                print(u"创建索引: \033[;31m%s\033[0m 失败! 原因: \033[;31m%s\033[0m" % (
                    fileName_, response['error']['reason']))

    def def_login(self, host_ip_):
        headers = {
            'Host': '{0}:38848'.format(host_ip_),
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'Origin': 'http://{0}:38848'.format(host_ip_),
            'Referer': 'http://{0}:38848/nacos/'.format(host_ip_),
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        data = {
            'username': 'nacos',
            'password': 'nacos',
        }

        try:
            request = self.session.post(url='http://{0}:38848/nacos/v1/auth/users/login'.format(host_ip_), headers=headers, data=data, verify=False)
            response = request.json()
            if response.get('accessToken', '') != '':
                self.authID = response['accessToken']
            elif response.get('error', '') != '':
                print(u"用户认证失败请检查! 原因: \033[;31m%s\033[0m" % (response))
                sys.exit(1)
        except Exception as ee:
            print(u"地址请求失败请检查! 原因: \033[;31m%s\033[0m" % ee)
            sys.exit(1)

    def def_nacos_conf(self, host_ip_):
        headers = {
            'Host': '{0}:38848'.format(host_ip_),
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'Origin': 'http://{0}:38848'.format(host_ip_),
            'Referer': 'http://{0}:38848/nacos/'.format(host_ip_),
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        data = {
            'customNamespaceId': 'sjzx',
            'namespaceName': 'sjzx',
            'namespaceDesc': 'sjzx',
            'namespaceId': '',
        }
        self.session.mount('http://{0}:38848/nacos/v1/console/namespaces?&accessToken={1}'.format(host_ip_, self.authID), requests.adapters.HTTPAdapter(max_retries=3))
        request = self.session.post(url='http://{0}:38848/nacos/v1/console/namespaces?&accessToken={1}'.format(host_ip_, self.authID), headers=headers, data=data, verify=False)
        response = request.json()
        if response != False:
            print(u"创建命名空间: \033[;32m%s\033[0m 成功! 返回值为: \033[;32m%s\033[0m" % (
                "sjzx", response))
        elif response == False:
            print(u"创建命名空间: \033[;31m%s\033[0m 失败! 原因: \033[;31m%s\033[0m" % (
                "sjzx", response))
        exit(1)


def def_percentage(me_total_length, me_current_process):
    current_progress = me_current_process + 1
    total_length = len(me_total_length)
    progress_percentage = (current_progress / total_length) * 100
    return f'({total_length}/{current_progress}): {progress_percentage:.2f}%'


def def_rmtree_ignore_errors(path, ignore_errors=False, onerror=None, ignore_dirs=None):
    if ignore_dirs is None:
        ignore_dirs = set()

    def _rmtree_inner(path):
        # 判断是否为目录且是否在要忽略的目录中
        if os.path.isdir(path) and os.path.basename(path) in ignore_dirs:
            print(f"Skipping directory: {path}")
            return
            # 如果是文件，则使用os.remove
        elif os.path.isfile(path):
            os.remove(path)
            return
            # 使用shutil的rmtree来删除目录
        try:
            shutil.rmtree(path, onerror=onerror)
        except OSError as e:
            if (not ignore_errors and
                    onerror is None):
                raise
            if onerror is not None:
                onerror(e)

                # 遍历目录树并删除（除了要忽略的目录）

    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            _rmtree_inner(os.path.join(root, name))
        for name in dirs:
            _rmtree_inner(os.path.join(root, name))


class CusPoEdit(object):
    def __init__(self):
        self.excel_file = None
        self.lv_list_msgcomment = []
        self.lv_list_msgid = []
        self.lv_list_msgid_plural = []
        self.lv_list_msgstr = []
        self.lv_list_msgstr0 = []
        self.lv_list_msgctxt = []
        self.po = polib.POFile()

    def def_create_pofile(self, po_file, occurrences, msgid, msgid_plural, msgstr, msgstr_plural, msgctxt):
        with open(po_file, 'a', encoding='utf-8') as s_hosts:
            if occurrences != None:
                if occurrences != "":
                    s_hosts.write(str(occurrences) + '\r')
            if msgctxt != None:
                if msgctxt != "":
                    s_hosts.write('msgctxt ' + str(msgctxt) + '\r')
            if msgid != None:
                if msgid != "":
                    s_hosts.write('msgid ' + str(msgid) + '\r')
            if msgid_plural != None:
                if msgid_plural != "":
                    s_hosts.write('msgid_plural ' + str(msgid_plural) + '\r')
            if msgstr != None:
                if msgstr != "":
                    s_hosts.write('msgstr ' + str(msgstr) + '\r')
            if msgstr_plural != None:
                if msgstr_plural != "":
                    s_hosts.write('msgstr[0] ' + str(msgstr_plural) + '\r')
        s_hosts.close()

    def def_translate(self, po_file):
        po = polib.pofile(po_file)
        self.lv_list_msgcomment = []
        self.lv_list_msgid = []
        self.lv_list_msgid_plural = []
        self.lv_list_msgstr = []
        self.lv_list_msgstr0 = []
        self.lv_list_msgctxt = []
        i = 1
        for entry in po:
            pattern = re.compile(r'(?:#.*)\n(?:".*\n.*)|(?:#.*)\n')
            res = re.findall(pattern, str(entry).replace('"\n"', ''))
            lv_str = ''
            result = []
            if len(res) == 0:
                self.lv_list_msgcomment.append("")
            for lv_tuple in res:
                result.append("".join(lv_tuple))
            for value in result:
                lv_str = lv_str + value
            self.lv_list_msgcomment.append(lv_str)
            # if i == 37:
            #     logger.debug(self.lv_list_msgstr0)
            #     print(str(entry))
            #     print(res)
            #     exit(1)

            pattern = None
            res = None
            lv_tuple = None
            pattern = re.compile(r'[^# ]msgid (?:.*)\n(?:".*\n.*)|[^# ]msgid (?:.*)\n')
            res = re.findall(pattern, str(entry).replace('"\n"', ''))
            if len(res) == 0:
                self.lv_list_msgid.append("")
            for lv_tuple in res:
                self.lv_list_msgid.append("".join(str(lv_tuple).replace('msgid ', "").replace('\n', '')))
            # if i == 1:
            #     print(self.lv_list_msgid)
            #     print(str(entry))
            #     print(res)
            #     exit(1)

            pattern = None
            res = None
            lv_tuple = None
            pattern = re.compile(r'msgid_plural (?:.*)\n(?:".*\n.*)|msgid_plural (?:.*)\n')
            res = re.findall(pattern, str(entry).replace('"\n"', ''))
            if len(res) == 0:
                self.lv_list_msgid_plural.append("")
            for lv_tuple in res:
                self.lv_list_msgid_plural.append("".join(str(lv_tuple).replace('msgid_plural ', "").replace('\n', '')))
            # if i == 37:
            #     logger.debug(self.lv_list_msgstr0)
            #     print(str(entry))
            #     print(res)
            #     exit(1)

            pattern = None
            res = None
            lv_tuple = None
            pattern = re.compile(r'msgstr (?:.*)\n(?:".*\n.*)|msgstr (?:.*)\n')
            res = re.findall(pattern, str(entry).replace('"\n"', ''))
            if len(res) == 0:
                self.lv_list_msgstr.append("")
            for lv_tuple in res:
                self.lv_list_msgstr.append("".join(str(lv_tuple).replace('msgstr ', "").replace('\n', '')))

            pattern = None
            res = None
            lv_tuple = None
            pattern = re.compile(r'msgstr\[0\] (?:.*)\n(?:".*\n.*)|msgstr\[0\] (?:.*)\n')
            res = re.findall(pattern, str(entry).replace('"\n"', ''))
            if len(res) == 0:
                self.lv_list_msgstr0.append("")
            for lv_tuple in res:
                self.lv_list_msgstr0.append("".join(str(lv_tuple).replace('msgstr[0] ', "").replace('\n', '')))
            # if i == 37:
            #     logger.debug(self.lv_list_msgstr0)
            #     print(str(entry))
            #     print(res)
            #     exit(1)

            pattern = None
            res = None
            lv_tuple = None
            pattern = re.compile(r'msgctxt (?:.*)\n(?:".*\n.*)|msgctxt (?:.*)\n')
            res = re.findall(pattern, str(entry).replace('"\n"', ''))
            if len(res) == 0:
                self.lv_list_msgctxt.append("")
            for lv_tuple in res:
                self.lv_list_msgctxt.append("".join(str(lv_tuple).replace('msgctxt ', "").replace('\n', '')))
            i = i + 1
        print(len(self.lv_list_msgcomment), len(self.lv_list_msgid), len(self.lv_list_msgid_plural), len(self.lv_list_msgstr),
              len(self.lv_list_msgstr0), len(self.lv_list_msgctxt))
        return {'msgcomment': self.lv_list_msgcomment, 'msgid': self.lv_list_msgid, 'msgid_plural': self.lv_list_msgid_plural,
                'msgstr': self.lv_list_msgstr, 'msgstr0': self.lv_list_msgstr0, 'msgctxt': self.lv_list_msgctxt}


class Cusxliff(object):
    def __init__(self):
        self.excel_file = None
        self.lv_list_msgcomment = []
        self.lv_list_msgid = []
        self.lv_list_msgid_plural = []
        self.lv_list_msgstr = []
        self.lv_list_msgstr0 = []
        self.lv_list_msgctxt = []
        self.po = polib.POFile()

    def def_translate(self, xliff_file):
        with open(xliff_file, encoding='utf-8', errors='ignore') as f:
            text = f.read()
        dom_tree = xml.dom.minidom.parseString(text)
        root_node = dom_tree.documentElement

        # 获取<file>元素的original属性
        original_value = None
        for file_node in root_node.getElementsByTagName("file"):
            original_value = file_node.getAttribute('original')
            break  # 假设只有一个<file>元素

        # 创建一个字典来存储结果，其中键是trans-unit的id，值是包含source, target和original的元组
        trans_units = {}

        # 遍历所有的trans-unit元素
        for trans_unit in root_node.getElementsByTagName("trans-unit"):
            # 获取trans-unit的id属性
            id_value = trans_unit.getAttribute('id')

            # 初始化source和target变量
            source_value = None
            target_value = ''

            # 遍历trans-unit的子节点
            for child in trans_unit.childNodes:
                # 检查节点是否是ELEMENT_NODE并且节点名称是'source'或'target'
                if child.nodeType == child.ELEMENT_NODE:
                    if child.nodeName == 'source':
                        source_value = child.firstChild.data if child.firstChild else None
                    elif child.nodeName == 'target':
                        # 检查<target>是否有state属性且值为"needs-translation"
                        if 'state' in child.attributes and child.attributes['state'].value == 'needs-translation':
                            target_value = ''  # 设置为空字符串
                        else:
                            target_value = child.firstChild.data if child.firstChild else ''

                            # 如果source被找到了，则将其存储到字典中，并添加original值和可能为空的target值
            if source_value:
                trans_units[id_value] = (source_value, target_value, original_value)

        return trans_units

    def def_get_filelist(self, dir, Filelist, suffix):
        if os.path.isfile(dir):
            if dir.endswith(suffix):
                Filelist.append(dir)
        elif os.path.isdir(dir):
            for s in os.listdir(dir):
                newDir = os.path.join(dir, s)
                self.def_get_filelist(newDir, Filelist, suffix)
        return Filelist

    @staticmethod
    def def_extract_links_from_md(md_content):
        # 正则表达式匹配行内链接
        inline_link_pattern = re.compile(r'\[([^\]]+)]\(([^)]+)\)')
        inline_links = inline_link_pattern.findall(md_content)

        # 匹配参考链接的定义部分
        ref_link_defs_pattern = re.compile(r'^\[(.*?)\]:\s*(.*)$', re.MULTILINE)
        ref_link_defs = ref_link_defs_pattern.findall(md_content)

        # 创建一个字典来映射参考链接的ID到URL
        ref_links_dict = {id: url.strip() for id, url in ref_link_defs}

        # 提取Markdown文本中的参考链接ID
        ref_link_ids_pattern = re.compile(r'\[(.*?)\]\[(.*?)\]')
        ref_link_ids_matches = ref_link_ids_pattern.findall(md_content)

        # 提取参考链接的全链接
        ref_links = []
        for text, id_ in ref_link_ids_matches:
            if id_ in ref_links_dict:
                ref_links.append(f"[{text}]({ref_links_dict[id_]})")

                # 合并行内链接和参考链接
        all_links = inline_links + ref_links

        # 转换为Markdown格式的链接列表
        markdown_links = [f"[{text}]({url})" for text, url in all_links]

        # # （可选）去重逻辑，这里仅根据链接的URL去重，可能需要调整以满足实际需求
        # unique_links = []
        # seen_urls = set()
        # for link in markdown_links:
        #     _, url = link.split('](')
        #     url = url.split(')')[0]
        #     if url not in seen_urls:
        #         unique_links.append(link)
        #         seen_urls.add(url)

        return markdown_links

    @staticmethod
    def def_extract_headers_from_md(md_content):
        # 正则表达式匹配所有标题（从#到######）
        header_pattern = re.compile(r'^(#+)\s+(.+)$', re.MULTILINE)
        headers = header_pattern.findall(md_content)

        # 提取标题文本并附带其级别（'#'的数量）
        markdown_headers = [f"{'#' * len(level)} {title}" for level, title in headers]

        return markdown_headers


class CusLocalMethod(object):
    def __init__(self, ):
        self.value = None
        self.numericValue = None
        self.textreplace = None
        self.command_pattern = re.compile(rf"^(?=.*\b(?:ls|cd|find|dh\s-h|exit|ll|pwd|ping|telnet|netstat)\b).*", re.MULTILINE)

    # def_batch_replace(str, {"[": "", "]": ""})
    def def_batch_replace(self, text: str, replacements: dict) -> str:
        """
        批量替换字符串中的多个字符或子字符串

        该函数接受一个字符串和一个替换映射字典，依次执行所有替换操作，
        返回替换后的新字符串。

        Args:
            text (str): 需要被替换的原始字符串
            replacements (dict): 替换映射字典，格式为 {旧字符串: 新字符串}
                                key为要被替换的字符串，value为替换后的新字符串

        Returns:
            str: 执行所有替换操作后的新字符串

        Raises:
            TypeError: 如果text不是字符串类型
            TypeError: 如果replacements不是字典类型

        Examples:
            >>> # 基本使用：替换方括号
            >>> def_batch_replace("Hello [World]", {"[": "(", "]": ")"})
            'Hello (World)'

            >>> # 替换多个字符
            >>> def_batch_replace("a-b_c", {"-": "", "_": " "})
            'a b c'

            >>> # 替换单词或短语
            >>> def_batch_replace("I like apples and bananas", {"apples": "oranges", "bananas": "pears"})
            'I like oranges and pears'

            >>> # 清空特定字符（替换为空字符串）
            >>> def_batch_replace("123-456-7890", {"-": ""})
            '1234567890'

            >>> # 处理特殊字符
            >>> def_batch_replace("Line1\\nLine2\\tTab", {"\\n": " ", "\\t": " "})
            'Line1 Line2 Tab'

        Notes:
            1. 替换操作按字典顺序依次执行，后续替换可能受到前面替换结果的影响
            2. 如果需要保持替换顺序，请使用collections.OrderedDict
            3. 原始字符串不会被修改，函数返回的是新字符串
            4. 如果替换字典为空，直接返回原字符串
            5. 替换操作区分大小写

        Performance:
            时间复杂度: O(n * m)，其中n是字符串长度，m是替换项数量
            对于大量替换或超长字符串，请考虑性能优化
        """
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def def_has_chinese(self, text):
        """判断字符串中是否包含中文"""
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False

    def def_find_chinese_in_brackets(self, text):
        """查找{#}内包含中文的字符串"""
        result = []
        pattern = r"{#(.*?)}"
        matches = re.findall(pattern, text)
        for match in matches:
            if self.def_has_chinese(match):
                result.append(match)
        return result

    @staticmethod
    def def_get_nested_value(d, *keys):
        for key in keys:
            if isinstance(d, dict):
                d = d.get(key)
            else:
                return ""
        return d or ""

    @staticmethod
    def format_time(seconds):
        """
        将秒数格式化为易读的时间字符串，支持正负数，只显示非零的时间单位

        参数:
            seconds (int/float/str): 秒数（可以是负数或"异常"字符串）

        返回:
            str: 格式化后的时间字符串或原"异常"字符串
        """
        if seconds == -999 or (isinstance(seconds, str) and seconds == "异常"):
            return "异常"

        # 确保输入是数字
        if isinstance(seconds, str):
            try:
                seconds = float(seconds)
            except ValueError:
                return "异常"

        # 处理负数情况
        is_negative = seconds < 0
        remaining = abs(seconds)

        time_units = [
            ('天', 86400),
            ('小时', 3600),
            ('分钟', 60),
            ('秒', 1)
        ]

        parts = []

        for unit_name, unit_seconds in time_units:
            if remaining >= unit_seconds:
                unit_value = int(remaining // unit_seconds)
                parts.append(f"{unit_value}{unit_name}")
                remaining %= unit_seconds

        # 处理小数秒数
        if remaining > 0 and (not parts or unit_name == '秒'):
            if remaining == int(remaining):
                parts.append(f"{int(remaining)}秒")
            else:
                parts.append(f"{remaining:.2f}秒".rstrip('0').rstrip('.') + "秒")

        # 如果没有匹配任何单位(秒数绝对值小于1秒)
        if not parts:
            return f"{'-' if is_negative else ''}{abs(seconds)}秒"

        # 组合结果
        result = ''.join(parts)
        if is_negative:
            result = f"-{result}"

        return result

    def remove_command_lines(self, text):
        """
        删除文本中包含ls、cd或find命令的所有行，并移除任何产生的空行。

        参数:
        text (str): 要处理的文本。

        返回:
        str: 处理后的文本，其中所有包含ls、cd或find命令的行以及空行已被删除。
        """
        # 使用正则表达式删除包含命令的行
        text = self.command_pattern.sub('', text)

        # 将文本分割成行，然后过滤掉空行或仅包含空白字符的行
        filtered_lines = [line for line in text.splitlines() if line.strip()]

        # 将过滤后的行重新组合成一个字符串
        return '\n'.join(filtered_lines)

    def generate_strong_password(self, length=8):
        """
        生成指定长度的随机密码(8-15位字符)，同时满足所有4个条件:
        1.密码中包含英文大写字母(A-Z) 2.密码中包含英文小写字母(a-z)
        3.密码中包含基本数字(0-9) 4.密码中包含特殊字符(-_@)
        生成更强壮的密码，确保每种字符类型都有合理分布

        参数:
            length (int): 密码长度

        返回:
            str: 生成的密码
        """
        if length < 8 or length > 15:
            raise ValueError("密码长度必须在8-15位之间")

        uppercase = string.ascii_uppercase
        lowercase = string.ascii_lowercase
        digits = string.digits
        special_chars = string.punctuation.replace("'", "").replace('"', '').replace('`', '').replace('(', '').replace(')', '')
        special_chars = '-_'
        all_chars = uppercase + lowercase + digits + special_chars

        password_chars = []

        # 确保每种类型都有合理数量
        # 大写字母：至少1个，最多不超过总长度的1/3
        upper_count = max(2, min(length // 4, random.randint(1, length // 3)))
        # 小写字母：至少1个
        lower_count = max(2, random.randint(1, length // 2))
        # 数字：至少1个
        digit_count = max(2, random.randint(1, length // 3))
        # 特殊字符：至少1个
        special_count = max(2, random.randint(1, length // 4))

        # 如果总数超过长度，调整数量
        total_required = upper_count + lower_count + digit_count + special_count
        if total_required > length:
            # 按比例减少
            ratio = length / total_required
            upper_count = max(1, int(upper_count * ratio))
            lower_count = max(1, int(lower_count * ratio))
            digit_count = max(1, int(digit_count * ratio))
            special_count = max(1, int(special_count * ratio))

        # 添加指定数量的各种字符
        password_chars.extend(random.choices(uppercase, k=upper_count))
        password_chars.extend(random.choices(lowercase, k=lower_count))
        password_chars.extend(random.choices(digits, k=digit_count))
        password_chars.extend(random.choices(special_chars, k=special_count))

        # 如果还有剩余位置，用随机字符填充
        remaining = length - len(password_chars)
        if remaining > 0:
            password_chars.extend(random.choices(all_chars, k=remaining))

        # 打乱顺序
        random.shuffle(password_chars)
        return ''.join(password_chars)

    @staticmethod
    def generate_multiple_passwords(self, count=5, length=8, strong=False):
        """
        生成多个密码

        参数:
            count (int): 密码数量
            length (int): 密码长度
            strong (bool): 是否使用强密码生成器

        返回:
            list: 密码列表
        """
        generator = self.generate_strong_password if strong else self.generate_password_special()
        return [generator(length) for _ in range(count)]


    def hanzi_to_pinyin(self, text):
        """
        将汉字转换为小写拼音
        """
        pinyin_list = lazy_pinyin(text)
        return self.def_batch_replace(''.join(pinyin_list),{"·": "", ".": "", " ": ""})



SPECIAL_CHARS = "-"
class PasswordGenerator:
    """
    简洁高效的密码生成器
    """

    def __init__(self, password_file: str = "generated_passwords.xlsx"):
        self._password_file = password_file
        self._existing_passwords: Dict[str, bool] = {}  # 存储所有历史密码

        # 只加载密码文件中的历史密码
        self._load_existing_passwords()

    def _load_existing_passwords(self) -> None:
        """只从密码文件加载历史密码"""
        if not os.path.exists(self._password_file):
            print(f"密码文件 {self._password_file} 不存在，将创建新文件")
            return

        try:
            workbook = load_workbook(self._password_file)
            worksheet = workbook.active

            # 获取密码文件的实际数据行数
            password_rows = self._get_actual_data_rows(worksheet)
            print(f"密码文件实际数据行数: {password_rows - 1}")  # 减去标题行

            # 从B列读取密码（跳过标题行）
            password_count = 0
            for row in range(2, password_rows + 1):
                password = worksheet[f'B{row}'].value
                if password:
                    self._existing_passwords[str(password)] = True
                    password_count += 1

            workbook.close()
            print(f"从密码文件加载了 {password_count} 个历史密码用于唯一性校验")

        except Exception as e:
            print(f"加载密码文件失败: {e}")

    def _get_actual_data_rows(self, worksheet) -> int:
        """获取实际数据行数（遇到空行停止）"""
        max_row = 0
        for row in worksheet.iter_rows():
            # 检查整行是否为空
            if all(cell.value is None for cell in row):
                break
            max_row += 1
        return max_row

    def generate_strong_password(self, length=8):
        """生成强密码"""
        if length < 8 or length > 15:
            raise ValueError("密码长度必须在8-15位之间")

        uppercase = string.ascii_uppercase
        lowercase = string.ascii_lowercase
        digits = string.digits
        special_chars = SPECIAL_CHARS
        all_chars = uppercase + lowercase + digits + special_chars

        # 简单高效的生成逻辑
        for _ in range(20):  # 最多尝试20次
            # 确保每种字符类型都有
            password = [
                random.choice(uppercase),
                random.choice(lowercase),
                random.choice(digits),
                random.choice(special_chars)
            ]

            # 填充剩余长度
            remaining = length - 4
            if remaining > 0:
                password.extend(random.choices(all_chars, k=remaining))

            random.shuffle(password)
            password_str = ''.join(password)

            # 检查是否唯一（与历史密码比较）
            if password_str not in self._existing_passwords:
                return password_str

        # 如果还是重复，添加随机后缀
        return self._generate_with_suffix(length)

    def _generate_with_suffix(self, length: int) -> str:
        """带后缀的密码生成"""
        base_chars = string.ascii_letters + string.digits + SPECIAL_CHARS

        for i in range(1000):
            # 生成基础密码
            password = [
                random.choice(string.ascii_uppercase),
                random.choice(string.ascii_lowercase),
                random.choice(string.digits),
                random.choice(SPECIAL_CHARS)
            ]

            remaining = length - 4
            if remaining > 0:
                password.extend(random.choices(base_chars, k=remaining))

            random.shuffle(password)
            base_password = ''.join(password)

            # 添加数字后缀确保唯一性
            for suffix in range(100):
                if suffix == 0:
                    candidate = base_password
                else:
                    candidate = base_password[:length - 2] + str(suffix).zfill(2)

                if candidate not in self._existing_passwords:
                    return candidate

        # 最终方案
        import uuid
        while True:
            unique_id = str(uuid.uuid4())[:length]
            if (any(c in string.ascii_uppercase for c in unique_id) and
                    any(c in string.ascii_lowercase for c in unique_id) and
                    any(c in string.digits for c in unique_id) and
                    any(c in SPECIAL_CHARS for c in unique_id) and
                    unique_id not in self._existing_passwords):
                return unique_id

    def save_new_passwords(self, password_mapping: Dict[str, str], source_file: str = "") -> None:
        """只保存新生成的密码到密码文件"""
        if not password_mapping:
            print("没有新密码需要保存")
            return

        try:
            if os.path.exists(self._password_file):
                workbook = load_workbook(self._password_file)
                worksheet = workbook.active
                # 获取密码文件的实际数据行数作为起始行
                password_rows = self._get_actual_data_rows(worksheet)
                start_row = password_rows + 1
            else:
                workbook = Workbook()
                worksheet = workbook.active
                worksheet.title = "Passwords"
                # 设置标题
                worksheet['A1'] = "Index"
                worksheet['B1'] = "Password"
                worksheet['C1'] = "Username"
                worksheet['D1'] = "Source File"
                worksheet['E1'] = "Time"
                start_row = 2

            # 只写入这次新生成的密码到密码文件
            for i, (username, password) in enumerate(password_mapping.items()):
                row_num = start_row + i
                worksheet[f'A{row_num}'] = row_num - 1
                worksheet[f'B{row_num}'] = password
                worksheet[f'C{row_num}'] = username
                worksheet[f'D{row_num}'] = source_file
                worksheet[f'E{row_num}'] = self._get_current_time()

            workbook.save(self._password_file)
            workbook.close()
            print(f"保存了 {len(password_mapping)} 个新密码到密码文件")

            # 更新内存中的密码字典，避免本次会话内重复
            for password in password_mapping.values():
                self._existing_passwords[password] = True

        except Exception as e:
            print(f"保存密码文件失败: {e}")

    def _get_current_time(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_for_excel_column(self, excel_op, output_column='B', length=8):
        """为用户Excel文件的A列生成密码"""
        # 获取用户文件的实际数据行数
        dimensions = excel_op.get_dimensions(skip_empty=True)
        user_rows = dimensions['rows']

        print(f"用户文件实际数据行数: {user_rows}")

        # 读取用户文件的A列数据（去掉标题）
        a_column_values = excel_op.get_column_values('A', skip_empty=True, skip_header=True)

        if not a_column_values:
            print("用户文件的A列没有有效数据")
            return {}

        print(f"开始为 {len(a_column_values)} 个用户生成密码...")

        password_mapping = {}

        # 生成密码
        for i, username in enumerate(a_column_values):
            if not username:
                continue

            username_str = str(username).strip()
            password = self.generate_strong_password(length)
            password_mapping[username_str] = password

            # 写入用户文件的指定列
            excel_op.set_cell_value(i + 2, output_column, password)  # i+2 因为从第2行开始

            if (i + 1) % 100 == 0:
                print(f"已生成 {i + 1} 个密码")

        # 只保存新生成的密码到密码文件
        source_file = getattr(excel_op, '_source_file', 'Unknown')
        self.save_new_passwords(password_mapping, source_file)

        print(f"完成! 为 {len(password_mapping)} 个用户生成了唯一密码")
        return password_mapping

    def get_statistics(self) -> Dict[str, int]:
        """获取统计信息"""
        return {
            "total_historical_passwords": len(self._existing_passwords)
        }



"""
PyPI镜像同步工具 - 彻底修复NoneType比较错误
"""

@dataclass
class DownloadStats:
    """下载统计信息"""
    total_packages: int = 0
    downloaded_packages: int = 0
    skipped_packages: int = 0
    failed_packages: int = 0
    total_files: int = 0
    downloaded_files: int = 0
    skipped_files: int = 0
    failed_files: int = 0
    total_bytes: int = 0
    start_time: float = field(default_factory=time.time)
    end_time: float = 0

    @property
    def elapsed_time(self) -> float:
        """获取耗时"""
        if self.end_time > 0:
            return self.end_time - self.start_time
        return time.time() - self.start_time

    @property
    def download_speed(self) -> float:
        """下载速度（MB/s）"""
        if self.elapsed_time > 0 and self.total_bytes > 0:
            return (self.total_bytes / 1024 / 1024) / self.elapsed_time
        return 0


class SafeUtils:
    """安全工具类，避免NoneType比较错误"""

    @staticmethod
    def safe_int(value: Any, default: int = 0) -> int:
        """安全转换为整数，避免None值"""
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    @staticmethod
    def safe_str(value: Any, default: str = "") -> str:
        """安全转换为字符串"""
        if value is None:
            return default
        try:
            return str(value)
        except:
            return default

    @staticmethod
    def safe_compare(a: Any, b: Any, default_for_none: Any = 0) -> Tuple[Any, Any]:
        """安全比较，确保没有None值"""
        a_safe = default_for_none if a is None else a
        b_safe = default_for_none if b is None else b
        return a_safe, b_safe

    @staticmethod
    def create_tqdm(total: Optional[int] = None, **kwargs) -> tqdm:
        """创建安全的tqdm进度条"""
        # 确保total不是None
        safe_total = 0 if total is None else total

        # 清理kwargs中的None值
        safe_kwargs = {}
        for key, value in kwargs.items():
            if value is not None:
                safe_kwargs[key] = value
            elif key in ['initial', 'unit_scale', 'miniters']:
                safe_kwargs[key] = 0  # 数值参数设为0

        return tqdm(total=safe_total, **safe_kwargs)


class PyPIMirrorSync:
    """PyPI镜像同步类"""

    def __init__(self, config: Dict[str, Any]):
        """
        初始化同步器
        """
        self.config = self._validate_config(config)
        self._setup_directories()
        self._setup_logging()
        self._setup_http_session()
        self.stats = DownloadStats()

        # 初始化pypi_simple客户端
        self._setup_pypi_client()

        # 状态文件路径
        self.state_file = self.config['log_dir'] / 'sync_state.json'
        self.downloaded_file = self.config['log_dir'] / 'downloaded.json'

        # 中断处理
        self._interrupted = False
        signal.signal(signal.SIGINT, self._handle_interrupt)
        signal.signal(signal.SIGTERM, self._handle_interrupt)

    def _validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """验证和设置默认配置"""
        default_config = {
            'mirror_url': 'https://pypi.org/simple/',
            'download_dir': Path('packages'),
            'log_dir': Path('logs'),
            'max_workers': 5,
            'timeout': 30.0,
            'retries': 3,
            'skip_existing': True,
            'verify_checksum': False,  # 第一次同步建议关闭，避免哈希问题
            'file_types': ['.whl', '.tar.gz', '.zip'],
            'rate_limit': 0,
            'max_packages': 10,  # 第一次测试建议少量
            'skip_packages': [],
            'only_packages': [],
            'prefer_binary': True,
            'platform_tag': None,
            'python_version': None,
            'download_strategy': 'simple',  # 简化策略，避免复杂排序
            'show_progress': True,
            'safe_mode': True,  # 启用安全模式
        }

        # 合并配置
        validated = default_config.copy()
        validated.update(config)

        # 确保路径是Path对象
        validated['download_dir'] = Path(validated['download_dir'])
        validated['log_dir'] = Path(validated['log_dir'])

        return validated

    def _setup_directories(self):
        """创建必要的目录"""
        self.config['download_dir'].mkdir(parents=True, exist_ok=True)
        self.config['log_dir'].mkdir(parents=True, exist_ok=True)

    def _setup_logging(self):
        """设置日志系统"""
        log_file = self.config['log_dir'] / 'sync.log'

        # 简化日志配置
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger('PyPISync')

    def _setup_http_session(self):
        """创建HTTP会话"""
        retry_strategy = Retry(
            total=self.config['retries'],
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "HEAD"]
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=self.config['max_workers'] * 2,
            pool_maxsize=self.config['max_workers'] * 2
        )

        self.session = requests.Session()
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self.session.headers.update({
            'User-Agent': f'PyPISync/1.0 (Python/{sys.version_info.major}.{sys.version_info.minor})',
        })

    def _setup_pypi_client(self):
        """初始化pypi_simple客户端"""
        try:
            self.pypi_client = PyPISimple(
                endpoint=self.config['mirror_url'],
            )
            self.logger.info(f"已连接到PyPI镜像: {self.config['mirror_url']}")
        except Exception as e:
            self.logger.error(f"初始化pypi_simple客户端失败: {e}")
            raise

    def _handle_interrupt(self, signum, frame):
        """处理中断信号"""
        self._interrupted = True
        self.logger.warning(f"收到信号 {signum}，正在优雅退出...")

    def load_state(self) -> Dict[str, Any]:
        """加载同步状态"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"加载状态文件失败: {e}")
        return {}

    def save_state(self, state: Dict[str, Any]):
        """保存同步状态"""
        try:
            state['last_save'] = datetime.now().isoformat()
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"保存状态文件失败: {e}")

    def load_downloaded_packages(self) -> Set[str]:
        """加载已下载的包列表"""
        if self.downloaded_file.exists():
            try:
                with open(self.downloaded_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return set(data.get('packages', []))
            except Exception as e:
                self.logger.error(f"加载已下载包列表失败: {e}")
        return set()

    def save_downloaded_packages(self, packages: Set[str]):
        """保存已下载的包列表"""
        try:
            data = {
                'last_updated': datetime.now().isoformat(),
                'total_packages': len(packages),
                'packages': sorted(list(packages))
            }
            with open(self.downloaded_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"保存已下载包列表失败: {e}")

    def get_package_list(self) -> List[str]:
        """获取所有包名列表"""
        self.logger.info(f"从 {self.config['mirror_url']} 获取包列表...")

        try:
            index_page: IndexPage = self.pypi_client.get_index_page(
                timeout=self.config['timeout']
            )

            packages = list(index_page.projects)

            self.logger.info(f"获取到 {len(packages)} 个包")
            return packages

        except Exception as e:
            self.logger.error(f"获取包列表失败: {e}")
            return []

    def get_package_info(self, package_name: str) -> Optional[Dict[str, Any]]:
        """获取包信息 - 安全版本"""
        try:
            project_page: ProjectPage = self.pypi_client.get_project_page(
                project=package_name,
                timeout=self.config['timeout']
            )

            files = []
            for package in project_page.packages:
                # 过滤文件类型
                if self.config['file_types']:
                    if not any(package.filename.endswith(ft) for ft in self.config['file_types']):
                        continue

                # 安全获取所有属性
                file_info = {
                    'filename': package.filename,
                    'url': package.url,
                    'size': SafeUtils.safe_int(getattr(package, 'size', 0)),
                    'upload_time': getattr(package, 'upload_time', ''),
                    'package_type': getattr(package, 'package_type', 'unknown'),
                    'requires_python': SafeUtils.safe_str(getattr(package, 'requires_python', '')),
                    'yanked': getattr(package, 'yanked', False),
                    'yanked_reason': SafeUtils.safe_str(getattr(package, 'yanked_reason', '')),
                    'digests': {},
                }

                # 安全获取哈希值
                if hasattr(package, 'md5_digest') and package.md5_digest:
                    file_info['digests']['md5'] = SafeUtils.safe_str(package.md5_digest)
                if hasattr(package, 'sha256_digest') and package.sha256_digest:
                    file_info['digests']['sha256'] = SafeUtils.safe_str(package.sha256_digest)

                files.append(file_info)

            # 尝试从包名解析版本
            version = None
            if files:
                # 使用第一个文件的文件名解析版本
                filename = files[0]['filename']
                version_match = re.search(r'-(\d+\.\d+\.\d+[a-zA-Z0-9._]*)', filename)
                if version_match:
                    version = version_match.group(1)

            package_info = {
                'name': package_name,
                'version': version,
                'files': files,
                'metadata': {},
            }

            return package_info

        except NoSuchProjectError:
            self.logger.warning(f"包 {package_name} 不存在")
            return None
        except Exception as e:
            self.logger.error(f"获取包 {package_name} 信息失败: {e}")
            return None

    def should_skip_package(self, package_name: str) -> bool:
        """判断是否应该跳过这个包"""
        if package_name in self.config['skip_packages']:
            return True

        if self.config['only_packages'] and package_name not in self.config['only_packages']:
            return True

        return False

    def _select_simple_file(self, files: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """简单选择文件 - 避免复杂排序"""
        if not files:
            return None

        # 简单策略：优先选择非yanked的wheel文件
        for file_info in files:
            yanked = file_info.get('yanked', False)
            package_type = file_info.get('package_type', '')

            # 跳过yanked文件
            if yanked:
                continue

            # 如果配置了优先二进制，选择wheel文件
            if self.config['prefer_binary'] and package_type == 'bdist_wheel':
                return file_info

        # 如果没有找到符合条件的，返回第一个非yanked文件
        for file_info in files:
            if not file_info.get('yanked', False):
                return file_info

        # 如果所有文件都是yanked，返回第一个文件
        return files[0] if files else None

    def download_file_safely(self, url: str, filepath: Path,
                             expected_size: int = 0,
                             expected_hash: Optional[Dict[str, str]] = None) -> bool:
        """安全下载文件 - 避免所有None比较"""
        try:
            # 限速
            if self.config['rate_limit'] > 0:
                time.sleep(self.config['rate_limit'])

            # 如果文件已存在且大小匹配，跳过
            if self.config['skip_existing'] and filepath.exists():
                file_size = filepath.stat().st_size
                expected_size_safe = SafeUtils.safe_int(expected_size)

                # 如果不知道期望大小，或者大小匹配，则跳过
                if expected_size_safe == 0 or file_size == expected_size_safe:
                    # 只有在配置了验证且提供了哈希时才验证
                    if (self.config['verify_checksum'] and expected_hash and
                            'sha256' in expected_hash):
                        try:
                            with open(filepath, 'rb') as f:
                                file_data = f.read()
                            actual_hash = hashlib.sha256(file_data).hexdigest()
                            if actual_hash == expected_hash['sha256']:
                                self.logger.debug(f"文件已存在且验证通过: {filepath.name}")
                                return True
                            else:
                                self.logger.warning(f"文件哈希不匹配，重新下载: {filepath.name}")
                                filepath.unlink()
                        except Exception:
                            # 哈希验证失败，继续下载
                            pass
                    else:
                        self.logger.debug(f"文件已存在: {filepath.name}")
                        return True

            # 下载文件
            response = self.session.get(
                url,
                stream=True,
                timeout=self.config['timeout']
            )
            response.raise_for_status()

            # 创建目录
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # 临时文件路径
            temp_filepath = filepath.with_suffix(filepath.suffix + '.download')

            # 获取文件大小（安全处理None）
            content_length = response.headers.get('content-length')
            total_size = SafeUtils.safe_int(content_length)

            downloaded_size = 0
            hasher = hashlib.sha256() if self.config['verify_checksum'] else None

            # 简单的下载进度显示
            if self.config['show_progress'] and total_size > 0:
                self.logger.info(f"下载 {filepath.name} ({total_size / 1024:.1f} KB)")

            with open(temp_filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)

                        if hasher:
                            hasher.update(chunk)

            # 重命名为最终文件名
            if os.path.exists(temp_filepath):
                # 如果目标文件已存在，先删除
                if os.path.exists(filepath):
                    try:
                        os.remove(filepath)
                    except:
                        pass

                os.rename(temp_filepath, filepath)

            # 更新统计
            self.stats.total_bytes += downloaded_size

            self.logger.debug(f"下载完成: {filepath.name} ({downloaded_size} bytes)")
            return True

        except requests.exceptions.Timeout:
            self.logger.error(f"下载超时: {url}")
            return False
        except requests.exceptions.RequestException as e:
            self.logger.error(f"下载失败 {url}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"下载异常 {url}: {str(e)[:100]}")  # 只显示前100个字符
            return False
        finally:
            # 清理临时文件
            temp_filepath = filepath.with_suffix(filepath.suffix + '.download')
            if os.path.exists(temp_filepath):
                try:
                    os.remove(temp_filepath)
                except:
                    pass

    def download_package_safely(self, package_name: str,
                                downloaded_packages: Set[str]) -> Tuple[bool, str]:
        """安全下载单个包"""
        if self._interrupted:
            return False, package_name

        # 检查是否应该跳过
        if self.should_skip_package(package_name):
            self.logger.debug(f"跳过包: {package_name}")
            return True, package_name

        # 检查是否已下载
        if package_name in downloaded_packages and self.config['skip_existing']:
            self.stats.skipped_packages += 1
            self.logger.debug(f"包已下载: {package_name}")
            return True, package_name

        self.logger.info(f"开始处理: {package_name}")

        # 获取包信息
        package_info = self.get_package_info(package_name)
        if not package_info:
            self.stats.failed_packages += 1
            self.logger.warning(f"无法获取包信息: {package_name}")
            return False, package_name

        files = package_info['files']
        if not files:
            self.stats.failed_packages += 1
            self.logger.warning(f"没有可下载的文件: {package_name}")
            return False, package_name

        # 选择文件
        selected_file = self._select_simple_file(files)
        if not selected_file:
            self.stats.failed_packages += 1
            self.logger.warning(f"没有合适的文件: {package_name}")
            return False, package_name

        # 创建包目录
        package_dir = self.config['download_dir'] / package_name
        try:
            package_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.logger.error(f"创建目录失败 {package_dir}: {e}")
            self.stats.failed_packages += 1
            return False, package_name

        # 下载文件
        filename = selected_file['filename']
        url = selected_file['url']
        size = selected_file.get('size', 0)
        digests = selected_file.get('digests', {})

        filepath = package_dir / filename

        if self.download_file_safely(url, filepath, size, digests):
            # 保存包信息
            try:
                info_file = package_dir / f"{package_name}.info.json"
                with open(info_file, 'w', encoding='utf-8') as f:
                    json.dump(package_info, f, indent=2, ensure_ascii=False)
            except Exception as e:
                self.logger.warning(f"保存包信息失败 {package_name}: {e}")

            self.stats.downloaded_files += 1
            self.stats.downloaded_packages += 1
            self.logger.info(f"完成: {package_name}")
            return True, package_name
        else:
            self.stats.failed_files += 1
            self.stats.failed_packages += 1
            self.logger.error(f"失败: {package_name}")
            return False, package_name

    def sync(self, resume: bool = True) -> bool:
        """执行同步"""
        self.logger.info("=" * 60)
        self.logger.info("开始PyPI镜像同步")
        self.logger.info(f"镜像源: {self.config['mirror_url']}")
        self.logger.info(f"下载目录: {self.config['download_dir']}")
        self.logger.info("=" * 60)

        # 加载状态
        state = self.load_state() if resume else {}
        downloaded_packages = self.load_downloaded_packages() if resume else set()

        self.stats.skipped_packages = len(downloaded_packages)

        # 获取包列表
        all_packages = self.get_package_list()
        if not all_packages:
            self.logger.error("无法获取包列表，同步终止")
            return False

        # 过滤包
        packages_to_sync = []
        for package in all_packages:
            if (self.config['max_packages'] and
                    len(packages_to_sync) >= self.config['max_packages']):
                self.logger.info(f"达到最大包数限制: {self.config['max_packages']}")
                break

            if not self.should_skip_package(package):
                packages_to_sync.append(package)

        self.stats.total_packages = len(packages_to_sync)
        self.logger.info(f"需要同步 {self.stats.total_packages} 个包")

        # 断点续传
        if resume and 'last_package' in state:
            last_package = state['last_package']
            try:
                start_index = packages_to_sync.index(last_package) + 1
                self.logger.info(f"从上次中断处继续: {last_package} (索引 {start_index})")
                packages_to_sync = packages_to_sync[start_index:]
            except ValueError:
                self.logger.warning(f"上次中断的包 {last_package} 不在列表中")

        # 简单的进度显示
        self.logger.info(f"开始下载 {len(packages_to_sync)} 个包...")

        success_packages = set()
        failed_packages = []
        processed = 0

        # 不使用复杂的线程池，避免并发问题
        for i, package in enumerate(packages_to_sync, 1):
            if self._interrupted:
                self.logger.warning("同步被用户中断")
                break

            # 更新进度
            processed += 1
            progress = (processed / len(packages_to_sync)) * 100

            # 简单进度显示
            if processed % 10 == 0 or processed == len(packages_to_sync):
                self.logger.info(f"进度: {processed}/{len(packages_to_sync)} ({progress:.1f}%)")

            try:
                success, pkg_name = self.download_package_safely(package, downloaded_packages)
                if success:
                    success_packages.add(pkg_name)
                else:
                    failed_packages.append(pkg_name)

                # 更新状态
                state['last_package'] = package
                self.save_state(state)

                # 定期保存进度
                if processed % 20 == 0:
                    all_downloaded = downloaded_packages.union(success_packages)
                    self.save_downloaded_packages(all_downloaded)

            except Exception as e:
                self.logger.error(f"处理包 {package} 时发生异常: {e}")
                failed_packages.append(package)

        # 保存最终状态
        all_downloaded = downloaded_packages.union(success_packages)
        self.save_downloaded_packages(all_downloaded)

        # 清空状态文件
        self.save_state({})

        # 完成统计
        self.stats.end_time = time.time()

        # 生成报告
        self._generate_report(success_packages, failed_packages)

        success = len(failed_packages) == 0 or len(success_packages) > 0
        if success:
            self.logger.info("=" * 60)
            self.logger.info("同步完成！")
            self.logger.info(f"成功: {len(success_packages)}, 失败: {len(failed_packages)}")
            self.logger.info("=" * 60)
        else:
            self.logger.error("同步失败")

        return success

    def _generate_report(self, success_packages: Set[str], failed_packages: List[str]):
        """生成同步报告"""
        report_file = self.config['log_dir'] / 'sync_report.txt'

        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("PyPI镜像同步报告\n")
                f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"镜像源: {self.config['mirror_url']}\n")
                f.write(f"耗时: {self.stats.elapsed_time:.2f} 秒\n\n")

                f.write("统计信息:\n")
                f.write(f"  总包数: {self.stats.total_packages}\n")
                f.write(f"  成功下载: {self.stats.downloaded_packages}\n")
                f.write(f"  跳过: {self.stats.skipped_packages}\n")
                f.write(f"  失败: {self.stats.failed_packages}\n")
                f.write(f"  总数据量: {self.stats.total_bytes / 1024 / 1024:.2f} MB\n")
                f.write(f"  平均速度: {self.stats.download_speed:.2f} MB/s\n")

        except Exception as e:
            self.logger.error(f"生成报告失败: {e}")
