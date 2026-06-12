### 项目地址

|标题|链接  |
|--|--|
| centos_7_zabbix_5.0.x_mysql | [centos_7_zabbix_5.0.x_mysql](https://gitcode.com/fantasywith/zabbix/tree/centos_7_zabbix_5.0.x_mysql) |
| centos_7_zabbix_7.0.x_mysql | [centos_7_zabbix_7.0.x_mysql](https://gitcode.com/fantasywith/zabbix/tree/centos_7_zabbix_7.0.x_mysql) |
| centos_7_zabbix_7.0.x_pgsql | [centos_7_zabbix_7.0.x_pgsql](https://gitcode.com/fantasywith/zabbix/tree/centos_7_zabbix_7.0.x_pgsql) |
| rocky_8_zabbix_6.0.x_mysql | [rocky_8_zabbix_6.0.x_mysql](https://gitcode.com/fantasywith/zabbix/tree/rocky_8_zabbix_6.0.x_mysql) |
| rocky_8_zabbix_6.0.x_pgsql | [rocky_8_zabbix_6.0.x_pgsql](https://gitcode.com/fantasywith/zabbix/tree/rocky_8_zabbix_6.0.x_pgsql) |
| rocky_8_zabbix_7.0.x_mysql | [rocky_8_zabbix_7.0.x_mysql](https://gitcode.com/fantasywith/zabbix/tree/rocky_8_zabbix_7.0.x_mysql) |
| rocky_8_zabbix_7.0.x_pgsql | [rocky_8_zabbix_7.0.x_pgsql](https://gitcode.com/fantasywith/zabbix/tree/rocky_8_zabbix_7.0.x_pgsql) |
| rocky_9_zabbix_7.0.x_pgsql | [rocky_9_zabbix_7.0.x_pgsql](https://gitcode.com/fantasywith/zabbix/tree/rocky_9_zabbix_7.0.x_pgsql) |
| kylin_v10_zabbix_7.0.x_mysql | [kylin_v10_zabbix_7.0.x_mysql](https://gitcode.com/fantasywith/zabbix/tree/kylin_v10_zabbix_7.0.x_mysql) |
| kylin_v10_zabbix_7.0.x_pgsql | [kylin_v10_zabbix_7.0.x_pgsql](https://gitcode.com/fantasywith/zabbix/tree/kylin_v10_zabbix_7.0.x_pgsql) |
| zabbix_6.0.x_docker | [zabbix_6.0.x_docker](https://gitcode.com/fantasywith/zabbix/tree/zabbix_6.0.x_docker) |
| zabbix_6.0.x_dockerfile | [zabbix_6.0.x_dockerfile](https://gitcode.com/fantasywith/zabbix/tree/zabbix_6.0.x_dockerfile) |
| zabbix_7.0.x_docker | [zabbix_7.0.x_docker](https://gitcode.com/fantasywith/zabbix/tree/zabbix_7.0.x_docker) |
| zabbix_7.0.x_dockerfile | [zabbix_7.0.x_dockerfile](https://gitcode.com/fantasywith/zabbix/tree/zabbix_7.0.x_dockerfile) |
| zabbix_api | [zabbix_api](https://gitcode.com/fantasywith/zabbix/tree/zabbix_api) |
| zabbix_7.0.x_build | [zabbix_7.0.x_build](https://gitcode.com/fantasywith/zabbix/tree/zabbix_7.0.x_build) |

### 克隆项目文件
```
# **执行如下命令克隆 NoYoWiFi 编排好的 zabbix 项目**
ZBX_SOURCES=https://'public':'EnSy68rd-72hN-Lnn_zYVpFQ'@gitcode.com/fantasywith/zabbix.git
ZBX_BRANCH=zabbix_api
ZBX_TODIR=/opt/${ZBX_BRANCH}
cd ${ZBX_TODIR}
git -c advice.detachedHead=false clone ${ZBX_SOURCES} --branch ${ZBX_BRANCH} --depth 1 --single-branch ${ZBX_TODIR}/
chmod 755 -R ${ZBX_TODIR}/
cd ${ZBX_TODIR}/
```


**效果图**
![在这里插入图片描述](https://img-blog.csdnimg.cn/ba37dc5de24e4e12a31fe4564dd9f7e2.png)
**下载pycharm用于项目适配**
[PyCharm下载地址](https://www.jetbrains.com.cn/pycharm/download/?section=windows)

`注意下滑鼠标下载社区版`
![在这里插入图片描述](https://img-blog.csdnimg.cn/f6a81323b8764dfb9d3eb43f1badb327.png)

`打开软件后下载中文插件`

![在这里插入图片描述](https://img-blog.csdnimg.cn/3fec5ec9bcaf4b32a048c61a47862bd2.png)

**下载Git用于克隆GitHub项目**
[Git下载地址](https://registry.npmmirror.com/binary.html?path=git-for-windows/v2.42.0.windows.2/)
[具体操作可参考](https://blog.csdn.net/mengxiang_/article/details/128193219)

**下载Python用于用于项目适配**
[Python3.7.0下载地址](https://www.python.org/ftp/python/3.7.0/python-3.7.0-amd64.exe)
[具体操作可参考](https://blog.csdn.net/m0_70669967/article/details/127922676)

**下载FastGithub用于GitHub下载加速**
[FastGithub下载](https://gitcode.net/mirrors/xljiulang/fastgithub/-/releases/2.1.4?spm=1033.2243.3001.5876)
[具体操作可参考](https://blog.csdn.net/m0_67906358/article/details/128799651)

克隆GitHub项目
`https://gitcode.com/fantasywith/zabbix.git`
[具体操作可参考](https://blog.csdn.net/weixin_41675512/article/details/107773519)

**修改成正确的zabbix api地址与用户名密码，文件为zabbix_api.py**
`        self.url = 'http://172.169.10.2/zabbix/api_jsonrpc.php'  # 修改URL`
`                "user": "Admin",  # web页面登录用户名`
`                "password": "zabbix"  # web页面登录密码`

```
class ZabbixApi:
    def __init__(self):
        self.authID = None
        self.url = 'http://172.169.10.2/zabbix/api_jsonrpc.php'  # 修改URL
        self.header = {"Content-Type": "application/json"}
        self.session = requests.Session()
        self.session.mount(self.url, requests.adapters.HTTPAdapter(max_retries=3))
        self.def_login()
        self.gv_apiVersion = None

    def def_login(self):
        lv_data = json.dumps({
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": "Admin",  # web页面登录用户名
                "password": "zabbix"  # web页面登录密码
            },
```

**目前支持的参数有:**

```
PS D:\00_development\pycharm\zabbix_api> venv\Scripts\python.exe zabbix_api_base.py   
usage: zabbix_api_base.py [options]

zabbix api

optional arguments:
  -h, --help            show this help message and exit
  -create_hostgroup [无参数]
                        创建主机组
  -delete_hostgroup [无参数]
                        删除主机组
  -create_template [无参数]
                        创建模板
  -delete_template [无参数]
                        删除模板
  -massadd_template_groups [无参数]
                        模板添加主机组
  -massremove_template_groups [无参数]
                        模板删除主机组
  -massadd_template_macros [无参数]
                        模板添加用户宏
  -massremove_template_macros [无参数]
                        模板删除用户宏
  -massadd_template_templates_link [无参数]
                        模板关联模板
  -massremove_templateids_clear [无参数]
                        模板脱离模板清理监控项
  -massremove_templateids_link [无参数]
                        模板脱离模板保留监控项
  -update_tags [无参数]    模板更新替换所有标签
  -delete_tags [无参数]    模板删除标签
  -create_template_item [无参数]
                        模板创建监控项
  -delete_template_item [无参数]
                        模板删除监控项
  -update_template_item_tags [无参数]
                        模板更新监控项标签
  -delete_template_item_tags [无参数]
                        模板删除监控项标签
  -create_template_trigger [无参数]
                        模板创建触发器
  -delete_template_trigger [无参数]
                        模板删除触发器
  -update_template_trigger_tags [无参数]
                        模板更新触发器标签
  -delete_template_trigger_tags [无参数]
                        模板删除触发器标签
  -create_host [无参数]    创建主机
  -delete_host [无参数]    删除主机
  -massadd_host_interface [无参数]
                        主机创建接口
  -massremove_host_interface [无参数]
                        主机删除接口
  -massadd_host_template [无参数]
                        主机关联模板
  -massremove_host_templateids [无参数]
                        主机脱离模板保留监控项
  -massremove_host_templateids_clear [无参数]
                        主机脱离模板清理监控项
  -massadd_host_groups [无参数]
                        主机关联主机组
  -massremove_host_group [无参数]
                        主机脱离主机组
  -create_discoveryrule [无参数]
                        创建发现规则
  -delete_discoveryrule [无参数]
                        删除发现规则
  -create_itemprototype [无参数]
                        模板创建发现规则监控项
  -delete_itemprototype [无参数]
                        模板删除发现规则监控项
  -create_template_triggerprototype [无参数]
                        模板创建发现规则触发器
  -delete_template_triggerprototype [无参数]
                        模板删除发现规则触发器
  -export_configuration [无参数]
                        导出所有模板
  -import_configuration [无参数]
                        入所有模板
  -poedit_zabbix_ui_to_excel [无参数]
                        从poedit导出zabbix ui 6.0翻译文本到excel
  --v V
  -excel_zabbix_ui_to_poedit [无参数]
                        从excel导出zabbix ui 6.0翻译文本到poedit
  -xliff_zabbix_document_to_excel [无参数]
                        从xliff导出zabbix document 7.0翻译文本到excel
  -excel_zabbix_document_to_xliff [无参数]
                        从excel导出zabbix document 7.0翻译文本到xliff
  -v, --version         如有问题请联系作者QQ1284524409

None
PS D:\00_development\pycharm\zabbix_api> 


```

```
(venv) D:\00_development\pycharm\zabbix_api>venv\Scripts\python.exe zabbix_api_extend.py
usage: zabbix_api_extend.py [options]

zabbix api

optional arguments:
  -h, --help            show this help message and exit
  -get_item_history [无参数]
                        按主机名批量计算历史最小值、平均值、最大值
  -get_all_history [无参数]
                        按主机名批量导出历史数据
  -get_hostgroup_host [无参数]
                        为主机组批量获取主机名
  -get_host_key_item [无参数]
                        为所有主机获取数据
  -get_hostgroup_item [无参数]
                        为主机组批量获取主机监控项
  -stop_all_priority_trigger [无参数]
                        批量停止已启用触发器
  -start_all_priority_trigger [无参数]
                        批量启用已停止触发器
  -stop_all_unsupport_item [无参数]
                        批量停止不支持的监控项
  -start_all_unsupport_item [无参数]
                        批量启用不支持的监控项
  -massadd_host_template_base_20221003 [无参数]
                        主机组下所有主机附加模板
  -massupdate_host_template_base_20221003 [无参数]
                        主机组下所有主机更新模板
  -def_massremove_host_templateids_clear_base_20221003 [无参数]
                        主机组下所有主机脱离模板清理监控项
  -get_all_alert [无参数]  获取所有告警信息
  -get_all_problem [无参数]
                        获取所有问题信息
  -get_all_event [无参数]  获取所有事件信息
  -createfile [无参数]     生成配置文件
  -senddir [无参数]        下发文件
  -sendcfg [无参数]        配置代理
  -sendsj [无参数]         配置审计
  -v, --version         如有问题请联系作者QQ1284524409

(venv) D:\00_development\pycharm\zabbix_api>

```

```
(venv) D:\00_development\pycharm\zabbix_api>venv\Scripts\python.exe zabbix_api_chinese.py
usage: zabbix_api_chinese.py [options]

zabbix api

optional arguments:
  -h, --help            show this help message and exit
  -export_all_template_item_sheet19 [无参数]
                        仅作者用于导出英文所有模板监控项
  -trans_all_template_item_to_chinese_sheet20 [无参数]
                        请使用此选项翻译模板监控项
  -export_all_template_trigger_sheet21 [无参数]
                        仅作者用于导出英文所有模板触发器
  -trans_all_template_trigger_to_chinese_sheet22 [无参数]
                        请使用此选项翻译模板触发器
  -export_all_template_graph_sheet23 [无参数]
                        仅作者用于导出英文所有模板图表
  -trans_all_template_graph_to_chinese_sheet24 [无参数]
                        请使用此选项翻译模板图表
  -export_all_template_itemprototype_sheet25 [无参数]
                        仅作者用于导出英文所有模板监控项原型
  -trans_all_template_itemprototype_to_chinese_sheet26 [无参数]
                        请使用此选项翻译模板监控项原型
  -export_all_template_triggerprototype_sheet27 [无参数]
                        仅作者用于导出英文所有模板触发器类型
  -trans_all_template_triggerprototype_to_chinese_sheet28 [无参数]
                        请使用此选项翻译模板触发器类型
  -export_all_template_graphprototype_sheet29 [无参数]
                        仅作者用于导出英文所有模板图表原型
  -trans_all_template_graphprototype_to_chinese_sheet30 [无参数]
                        请使用此选项翻译模板图表原型
  -export_all_template_trigger_event_name_sheet37 [无参数]
                        仅作者用于导出英文所有模板触发器事件名称
  -trans_all_template_trigger_event_name_to_chinese_sheet37 [无参数]
                        请使用此选项翻译模板触发器事件名称
  -export_all_template_triggerprototype_name_sheet38 [无参数]
                        仅作者用于导出英文所有模板触发器原型事件名称
  -trans_all_template_triggerprototype_name_to_chinese_sheet38 [无参数]
                        请使用此选项翻译模板触发原型器事件名称
  -export_all_template_tag_name_sheet40 [无参数]
                        仅作者用于导出英文所有模板标签名称
  -trans_all_template_tag_name_to_chinese_sheet40 [无参数]
                        请使用此选项翻译模板标签名称
  -export_all_template_item_tag_name_sheet41 [无参数]
                        仅作者用于导出英文所有模板监控项标签名称
  -trans_all_template_item_tag_name_to_chinese_sheet41 [无参数]
                        请使用此选项翻译模板监控项标签名称
  -export_all_template_trigger_tag_name_sheet42 [无参数]
                        仅作者用于导出英文所有模板触发器标签名称
  -trans_all_template_trigger_tag_name_to_chinese_sheet42 [无参数]
                        请使用此选项翻译模板触发器标签名称
  -export_all_template_itemprototype_tag_sheet43 [无参数]
                        仅作者用于导出英文所有模板监控项原型标签
  -trans_all_template_itemprototype_tag_to_chinese_sheet43 [无参数]
                        请使用此选项翻译模板监控项原型标签
  -export_all_template_triggerprototype_tag_sheet44 [无参数]
                        仅作者用于导出英文所有模板监控项原型标签
  -trans_all_template_triggerprototype_tag_to_chinese_sheet44 [无参数]
                        请使用此选项翻译模板监控项原型标签
  -export_all_hostgroup_name_sheet45 [无参数]
                        仅作者用于导出英文主机组名称
  -trans_all_hostgroup_name_to_chinese_sheet45 [无参数]
                        请使用此选项翻译主机组名称
  -export_all_templategroup_name_sheet46 [无参数]
                        仅作者用于导出英文模板组名称
  -trans_all_templategroup_name_to_chinese_sheet46 [无参数]
                        请使用此选项翻译模板组名称
  -export_all_application_name_sheet47 [无参数]
                        仅作者用于导出英文模板应用集名称
  -trans_all_application_name_to_chinese_sheet47 [无参数]
                        请使用此选项翻译模板应用集名称
  -v, --version         如有问题请联系作者QQ1284524409

(venv) D:\00_development\pycharm\zabbix_api>

```

**Pycharm示例**

```
PS D:\00_development\pycharm\zabbix_api> .\venv\Scripts\python.exe .\zabbix_api_base.py -create_hostgroup
创建主机组: hostgroup1 失败! 原因: Host group "hostgroup1" already exists.
创建主机组: hostgroup2 失败! 原因: Host group "hostgroup2" already exists.
创建主机组: hostgroup3 失败! 原因: Host group "hostgroup3" already exists.
创建主机组: hostgroup4 失败! 原因: Host group "hostgroup4" already exists.
创建主机组: hostgroup5 失败! 原因: Host group "hostgroup5" already exists.
创建主机组: hostgroup6 失败! 原因: Host group "hostgroup6" already exists.
创建主机组: hostgroup7 失败! 原因: Host group "hostgroup7" already exists.
创建主机组: hostgroup8 失败! 原因: Host group "hostgroup8" already exists.
创建主机组: hostgroup9 失败! 原因: Host group "hostgroup9" already exists.
创建主机组: hostgroup10 失败! 原因: Host group "hostgroup10" already exists.
```

`交流群`  
  
| zabbix-答疑群                                                                                                | zabbix-汉化群                                                                                                  |  
|-----------------------------------------------------------------------------|---|  
| ![微信打赏](https://<br/>) |![微信打赏](https://gitcode.com/fantasywith/zabbix/-/raw/zabbix_api/vx_images/zabbix-hanhua.png)|  

**全文完结**

