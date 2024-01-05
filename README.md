==持续更新最新版本...==

# 编译构建方法
1. 下载zabbix dockerfile项目文件

[一键安装脚本](https://gitcode.net/1284524409/zabbix/-/archive/zabbix_dockerfile/zabbix-zabbix_dockerfile.tar.gz)

2. 执行命令全自动本地化部署

`汉化作者为官方zabbix docker镜像添加了如下内容`

==1) mysql分区 + 全官方模板汉化 + Web UI文本汉化 + grafana zabbix插件 + grafana loki插件 + https访问方式==

==2) PostgreSQL+ TimescaleDB分区 + 全官方模板汉化 + Web UI文本汉化 + grafana zabbix插件 + grafana loki插件 + https访问方式==

```shell
tar -zxvf zabbix_dockerfile.tar.gz
cd zabbix_rebuild
sh rebuild.sh
cd ../zbx
# sh update_config-entrypoint_pgsql.sh update
sh update_config-entrypoint_mysql.sh update

# sh down_pgsql.sh
sh down_mysql.sh

# sh update_config-entrypoint_pgsql.sh build1
sh update_config-entrypoint_mysql.sh build1

# sh update_config-entrypoint_pgsql.sh build2
sh update_config-entrypoint_mysql.sh build2

# sh update_config-entrypoint_pgsql.sh make
sh update_config-entrypoint_mysql.sh make
```

# 使用方法

```shell
docker images|grep none|awk '{print $3 }'|xargs docker rmi

# sh update_config-entrypoint_pgsql.sh cp
sh update_config-entrypoint_mysql.sh cp

# sh update_config-entrypoint_pgsql.sh start
sh update_config-entrypoint_mysql.sh start
```

**项目地址**  
[GitCode项目地址](https://gitcode.net/1284524409/zabbix/-/tree/zabbix_docker)

`感谢打赏`  
  
| 微信                        |支付宝|  
|---------------------------|---|  
|  ![微信打赏](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/thanks_wx.jpg) |![微信打赏](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/thanks_zfb.jpg)|  
  
  
**全文完结**