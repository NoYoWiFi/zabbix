**项目地址**  
[GitCode项目地址](https://gitcode.net/1284524409/zabbix/-/tree/zabbix_docker)

**效果图**
```  
[root@localhost zabbix_docker]# docker images  
REPOSITORY               TAG                 IMAGE ID       CREATED        SIZE  
zabbix-server-mysql      centos-6.0-latest   5bbe1784ca86   4 days ago     889MB  
zabbix-web-service       centos-6.0-latest   302c32090933   4 days ago     732MB  
zabbix-proxy-mysql       centos-6.0-latest   2af003bb178b   4 days ago     673MB  
zabbix-java-gateway      centos-6.0-latest   6825b642100d   4 days ago     720MB  
zabbix-snmptraps         centos-6.0-latest   d444eab79de1   4 days ago     601MB  
zabbix-agent2            centos-6.0-latest   ddb84f925c55   4 days ago     615MB  
mariadb                  10.5.19-focal       cfe0a83e48d5   8 days ago     392MB  
zabbix-web-nginx-mysql   centos-6.0-latest   64081ecac82f   6 weeks ago    774MB  
quay.io/centos/centos    stream8             6a97c47aacfc   3 months ago   513MB  
[root@localhost zabbix_docker]# [root@localhost zabbix_docker]# docker ps -a  
CONTAINER ID   IMAGE                                      COMMAND                  CREATED          STATUS                    PORTS                                                                            NAMES  
977e75774418   zabbix-web-nginx-mysql:centos-6.0-latest   "docker-entrypoint.sh"   15 minutes ago   Up 15 minutes (healthy)   0.0.0.0:80->8080/tcp, :::80->8080/tcp, 0.0.0.0:443->8443/tcp, :::443->8443/tcp   zabbix_docker-zabbix-web-nginx-mysql-1  
0770a23343e9   zabbix-server-mysql:centos-6.0-latest      "/usr/bin/tini -- /u…"   15 minutes ago   Up 15 minutes             0.0.0.0:10051->10051/tcp, :::10051->10051/tcp                                    zabbix_docker-zabbix-server-1  
98aecf59d879   zabbix-agent2:centos-6.0-latest            "/usr/bin/tini -- /u…"   15 minutes ago   Up 15 minutes             0.0.0.0:10050->10050/tcp, :::10050->10050/tcp, 31999/tcp                         zabbix_docker-zabbix-agent2-1  
ec9e9cd0ed74   zabbix-java-gateway:centos-6.0-latest      "docker-entrypoint.s…"   15 minutes ago   Up 15 minutes                                                                                              zabbix_docker-zabbix-java-gateway-1  
d0d7d7977b99   zabbix-snmptraps:centos-6.0-latest         "/usr/sbin/snmptrapd…"   15 minutes ago   Up 15 minutes             0.0.0.0:162->1162/udp, :::162->1162/udp                                          zabbix_docker-zabbix-snmptraps-1  
b72cdae7ba93   zabbix-web-service:centos-6.0-latest       "docker-entrypoint.s…"   15 minutes ago   Up 15 minutes                                                                                              zabbix_docker-zabbix-web-service-1  
0b8819153360   mariadb:10.5.19-focal                      "docker-entrypoint.s…"   15 minutes ago   Up 15 minutes             0.0.0.0:3306->3306/tcp, :::3306->3306/tcp                                        zabbix_docker-mysql-server-1  
[root@localhost zabbix_docker]#   
```  
  
**集成全中文模板**  
  
![](https://gitcode.net/1284524409/zabbix/-/raw/zabbix_docker/vx_images/8f09f045a9dc42a0bb47d97e3ec5963b.png)  
  
![](https://gitcode.net/1284524409/zabbix/-/raw/zabbix_docker/vx_images/ce76ece189844eaa94629d9c59beb845.png)

**执行如下命令进行git安装**

```
yum -y install git
```

**执行如下命令克隆docker安装中文版zabbix项目**

```
ZBX_SOURCES=https://gitcode.net/1284524409/zabbix.git
ZBX_VERSION=zabbix_docker
ZBX_NAME=zabbix_docker-6.0-latest
ZBX_DIR=/opt
cd ${ZBX_DIR}
git -c advice.detachedHead=false clone ${ZBX_SOURCES} --branch ${ZBX_VERSION} --depth 1 --single-branch ${ZBX_DIR}/${ZBX_NAME}
chmod 755 -R ${ZBX_DIR}/${ZBX_NAME}
cd ${ZBX_DIR}/${ZBX_NAME}
```

**执行如下命令安装docker服务**

```
# sh update_config-entrypoint_mysql.sh init
sh update_config-entrypoint_pgsql.sh init
```

**执行如下命令下载docker镜像**

```
sh update_config-entrypoint_mysql.sh down
# sh update_config-entrypoint_pgsql.sh down
```

**执行如下命令初始化配置文件**

```
sh update_config-entrypoint_mysql.sh cp
# sh update_config-entrypoint_pgsql.sh cp
```

**执行如下命令启动docker容器**

```
sh update_config-entrypoint_mysql.sh start
# sh update_config-entrypoint_pgsql.sh start
```

**打开网页输入服务器IP地址访问zabbix**
http://IP:8080 或 https://IP:8443
用户名: Admin
密码: zabbix

**打开网页输入服务器IP地址访问grafana**
https://IP:3000
用户名: admin
密码: admin

**将grafana界面设置成中文**
![](https://gitcode.net/1284524409/zabbix/-/raw/zabbix_docker/vx_images/2cc17fdd154217656975030bc6636523.png)

**启用zabbix插件
![](https://gitcode.net/1284524409/zabbix/-/raw/zabbix_docker/vx_images/844a584f0789fc28205b2b5a8302938c.png)

**连接zabbix数据库插件**
![](https://gitcode.net/1284524409/zabbix/-/raw/zabbix_docker/vx_images/c87b39af3050dac2ecb62c7365bc7a7b.png)

**新建zabbix数据库连接**
`https://zabbix-web-nginx-mysql:8443/api_jsonrpc.php`

![](https://gitcode.net/1284524409/zabbix/-/raw/zabbix_docker/vx_images/c68d9dbf98134214aa759dd25bbfbb2e.png)

**输入正确的用户名密码**
`Admin/zabbix`

![](https://gitcode.net/1284524409/zabbix/-/raw/zabbix_docker/vx_images/aa5fd658ee04a9dd7687e459b3064dbe.png)


**zabbix-server服务器同时优化成了rsyslog日志服务器，rsyslog日志端口为514**
日志存储路径为 /var/log/loki/

**grafana优化集成了zabbix与Loki插件**
请将任意.log后缀日志存入 /var/log/loki/即可连接到loki
URL为http://IP:3100
![](https://gitcode.net/1284524409/zabbix/-/raw/zabbix_docker/vx_images/c469826e35f6d0735418cbb9ca008b22.png)

**存储位置**

映射的卷位于当前文件夹的zbx_env目录

**zabbix-server配置文件位置**
`/opt/zabbix_docker-6.0-latest/env_vars/.env_srv`

**后期如果有新版本发布可以通过如下命令更新zabbix版本**

```
# sh update_config-entrypoint_mysql.sh stop
sh update_config-entrypoint_pgsql.sh stop

ZBX_SOURCES=https://gitcode.net/1284524409/zabbix.git
ZBX_VERSION=zabbix_docker
ZBX_NAME=zabbix_docker-6.0-latest
ZBX_DIR=/opt
git init
git remote add origin ${ZBX_SOURCES}
cd ${ZBX_DIR}/${ZBX_NAME}
git remote -v
git fetch --all
git reset --hard origin/${ZBX_VERSION}
git pull  ${ZBX_SOURCES} ${ZBX_VERSION}
chmod 755 -R ${ZBX_DIR}/${ZBX_NAME}
cd ${ZBX_DIR}/${ZBX_NAME}

# sh update_config-entrypoint_mysql.sh down
sh update_config-entrypoint_pgsql.sh down

# sh update_config-entrypoint_mysql.sh start
sh update_config-entrypoint_pgsql.sh start
```

`感谢打赏`    

| **微信** | **支付宝** |
| :--: | :--: |
| ![微信打赏](https://gitcode.net/1284524409/zabbix/-/raw/zabbix_docker/thanks_wx.jpg) | ![微信打赏](https://gitcode.net/1284524409/zabbix/-/raw/zabbix_docker/thanks_zfb.jpg) |

**全文完结**