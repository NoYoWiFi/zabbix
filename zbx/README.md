==持续更新最新版本...==

# 编译构建方法
1. 下载zabbix dockerfile项目文件

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
ZBX_BRANCH=zabbix_6.0.x_dockerfile
ZBX_TODIR=/opt/${ZBX_BRANCH}
cd ${ZBX_TODIR}
git -c advice.detachedHead=false clone ${ZBX_SOURCES} --branch ${ZBX_BRANCH} --depth 1 --single-branch ${ZBX_TODIR}/
chmod 755 -R ${ZBX_TODIR}/
cd ${ZBX_TODIR}/
```

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
# sh update_config-entrypoint_pgsql.sh prxstart
sh update_config-entrypoint_mysql.sh start
# sh update_config-entrypoint_mysql.sh prxstart
```

**项目地址**  
[GitCode项目地址](https://gitcode.com/fantasywith/zabbix/tree/zabbix_docker)

`交流群`  
  
| zabbix-答疑群                                                                                                | zabbix-汉化群                                                                                                  |  
|---------------------------|---|  
|  ![微信打赏](https://gitcode.com/fantasywith/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/vx_images/zabbix-dayi.png) |![微信打赏](https://gitcode.com/fantasywith/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/vx_images/zabbix-hanhua.png)|  
  
  
**全文完结**