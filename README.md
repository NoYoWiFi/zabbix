==持续更新最新版本...==
# 安装部署方法
1. 下载zabbix dockerfile项目文件
[一键安装脚本](https://gitcode.net/1284524409/zabbix/-/archive/zabbix_dockerfile/zabbix_dockerfile.tar.gz)
2. 执行命令全自动本地化部署
```
tar -zxvf zabbix_dockerfile.tar.gz
cd zabbix_rebuild
sh rebuild.sh
cd ../zbx
# update_config-entrypoint_pgsql.sh update
update_config-entrypoint_mysql.sh update

# update_config-entrypoint_pgsql.sh build1
update_config-entrypoint_mysql.sh build1

# update_config-entrypoint_pgsql.sh build2
update_config-entrypoint_mysql.sh build2

# update_config-entrypoint_pgsql.sh make
update_config-entrypoint_mysql.sh make
```

`感谢打赏`  
  
| 微信                        |支付宝|  
|---------------------------|---|  
|  ![微信打赏](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/thanks_wx.jpg) |![微信打赏](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/thanks_zfb.jpg)|  
  
  
**全文完结**