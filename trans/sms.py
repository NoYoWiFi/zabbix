#!/usr/bin/env python3
# coding=utf-8

import sys
import logging
import json
import datetime

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

# 创建一个日志器
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

# 创建日志格式器
formatter = logging.Formatter(fmt="%(asctime)s [ %(filename)s ]  %(lineno)d line | [ %(levelname)s ] | [%(message)s]",
                              datefmt="%Y/%m/%d/%X")

# 创建一个输出到控制台的处理器
console_handler = logging.StreamHandler()

# 创建一个输出到文件的处理器
file_handler = logging.FileHandler("/var/log/loki/sms.log", encoding="utf-8")

# 添加控制台处理器并设置格式
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 添加文件处理器并设置格式
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 替换为你的阿里云 Access Key ID 和 Access Key Secret
access_key_id = 'xxx'
access_key_secret = 'xxx'

# 替换为你的短信签名名称、模板CODE和接收短信的手机号码
sign_name = 'xxx'    
template_code = 'xxx'
phone_numbers = sys.argv[1]

msg_title = sys.argv[2]
# 从命令行参数中获取 JSON 格式的消息内容
message = sys.argv[3]

var_str_01 = "{" + "\"" + "title" + "\""+ ":" + "\"" + u'{var_01}'.format(var_01=msg_title) + "\""
var_str_02 = "\"" + "datetime" + "\""+ ":" + "\"" + str(datetime.date.today()) + "\""
var_str_03 = "\"" + "name" + "\""+ ":" + "\"" + "名称" + "\""
var_str_04 = "\"" + "info" + "\""+ ":" + "\"" + u'{var_01}'.format(var_01=message) + "\"" + "}"
var_json_05 = var_str_01 + "," + var_str_02 + "," + var_str_03 + "," + var_str_04
# var_json_06 = {"title":"故障: Linux: Zabbix客户端代理不可用达(10s)","datetime":"2024.03.02 22:25:26","name":"Zabbix server 127.0.0.1","info":"zabbix[host,agent,available]:not available (0)"}
# print(var_json_05)

logger.info("PhoneNumber: " + phone_numbers)
logger.info("Title: " + msg_title)
logger.info("Info: " + str(message))

# 初始化 Aliyun SDK
config = open_api_models.Config(
    access_key_id=access_key_id,
    access_key_secret=access_key_secret
)
config.endpoint = 'dysmsapi.aliyuncs.com'
client = Dysmsapi20170525Client(config)

# exit(1)
# 构造发送短信请求
send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
    phone_numbers=phone_numbers,
    sign_name=sign_name,
    template_code=template_code,
    template_param=str(var_json_05)
)

# Zabbix运维数据中心 A warning has occurred ${title} Time：${datetime} Host：${name} Info：${info}
# Zabbix运维数据中心 A warning has occurred ${title} Time：${datetime} Host：${name} Info：${info}
# '{"name": "Alice", "age": 25}'
# {"title":"{EVENT.NAME}","datetime":"{EVENT.DATE} {EVENT.TIME}","name":"{HOST.NAME} {HOST.IP}","info":"{ITEM.KEY1}:{ITEM.VALUE1}"}
# print(json.loads('{"name": "Alice", "age": 25}'))
# print(json.loads("{\"info\": \"{var_01}\"}".format(var_01=str(message))))
# print(message)
# print(json.loads('{"info": "var_01"}'))
try:
    # 发送短信
    a = client.send_sms_with_options(send_sms_request, util_models.RuntimeOptions())
    print(a)
except Exception as error:
    # 输出错误信息
    logger.error("SMS sending error: " + str(error.message))
    logger.error("Diagnostic address: " + error.data.get("Recommend"))
    UtilClient.assert_as_string(error.message)
