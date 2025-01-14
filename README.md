


**zabbix 版本**

`6.0.x`

`7.0.x`
# 全自动安装方法
1. 下载一键安装包

### 项目地址

|标题|链接  |
|--|--|
| centos_7_zabbix_5.0.x_mysql | [centos_7_zabbix_5.0.x_mysql](https://github.com/NoYoWiFi/zabbix/tree/centos_7_zabbix_5.0.x_mysql) |
| centos_7_zabbix_7.0.x_mysql | [centos_7_zabbix_7.0.x_mysql](https://github.com/NoYoWiFi/zabbix/tree/centos_7_zabbix_7.0.x_mysql) |
| centos_7_zabbix_7.0.x_pgsql | [centos_7_zabbix_7.0.x_pgsql](https://github.com/NoYoWiFi/zabbix/tree/centos_7_zabbix_7.0.x_pgsql) |
| rocky_8_zabbix_6.0.x_mysql | [rocky_8_zabbix_6.0.x_mysql](https://github.com/NoYoWiFi/zabbix/tree/rocky_8_zabbix_6.0.x_mysql) |
| rocky_8_zabbix_6.0.x_pgsql | [rocky_8_zabbix_6.0.x_pgsql](https://github.com/NoYoWiFi/zabbix/tree/rocky_8_zabbix_6.0.x_pgsql) |
| rocky_8_zabbix_7.0.x_mysql | [rocky_8_zabbix_7.0.x_mysql](https://github.com/NoYoWiFi/zabbix/tree/rocky_8_zabbix_7.0.x_mysql) |
| rocky_8_zabbix_7.0.x_pgsql | [rocky_8_zabbix_7.0.x_pgsql](https://github.com/NoYoWiFi/zabbix/tree/rocky_8_zabbix_7.0.x_pgsql) |
| zabbix_6.0.x_docker | [zabbix_6.0.x_docker](https://github.com/NoYoWiFi/zabbix/tree/zabbix_6.0.x_docker) |
| zabbix_6.0.x_dockerfile | [zabbix_6.0.x_dockerfile](https://github.com/NoYoWiFi/zabbix/tree/zabbix_6.0.x_dockerfile) |
| zabbix_7.0.x_docker | [zabbix_7.0.x_docker](https://github.com/NoYoWiFi/zabbix/tree/zabbix_7.0.x_docker) |
| zabbix_7.0.x_dockerfile | [zabbix_7.0.x_dockerfile](https://github.com/NoYoWiFi/zabbix/tree/zabbix_7.0.x_dockerfile) |
| zabbix_api | [zabbix_api](https://github.com/NoYoWiFi/zabbix/tree/zabbix_api) |
| zabbix_7.0.x_build | [zabbix_7.0.x_build](https://github.com/NoYoWiFi/zabbix/tree/zabbix_7.0.x_build) |

### 克隆项目文件
```
# **执行如下命令克隆 NoYoWiFi 编排好的 zabbix 项目**
ZBX_SOURCES=https://'zabbix':'k_LC6VHmJzNyB_3SBgtz'@gitcode.net/1284524409/zabbix.git
ZBX_BRANCH=zabbix_7.0.x_docker
ZBX_TODIR=/opt/${ZBX_BRANCH}
cd ${ZBX_TODIR}
git -c advice.detachedHead=false clone ${ZBX_SOURCES} --branch ${ZBX_BRANCH} --depth 1 --single-branch ${ZBX_TODIR}/
chmod 755 -R ${ZBX_TODIR}/
cd ${ZBX_TODIR}/
```
**效果图**
```
[root@localhost zabbix_docker]# docker images  
REPOSITORY               TAG                 IMAGE ID       CREATED        SIZE  
zabbix-server-mysql      centos-7.0-latest   5bbe1784ca86   4 days ago     889MB  
zabbix-web-service       centos-7.0-latest   302c32090933   4 days ago     732MB  
zabbix-proxy-mysql       centos-7.0-latest   2af003bb178b   4 days ago     673MB  
zabbix-java-gateway      centos-7.0-latest   6825b642100d   4 days ago     720MB  
zabbix-snmptraps         centos-7.0-latest   d444eab79de1   4 days ago     601MB  
zabbix-agent2            centos-7.0-latest   ddb84f925c55   4 days ago     615MB  
mariadb                  10.5.19-focal       cfe0a83e48d5   8 days ago     392MB  
zabbix-web-nginx-mysql   centos-7.0-latest   64081ecac82f   6 weeks ago    774MB  
quay.io/centos/centos    stream8             6a97c47aacfc   3 months ago   513MB  
[root@localhost zabbix_docker]# [root@localhost zabbix_docker]# docker ps -a  
CONTAINER ID   IMAGE                                      COMMAND                  CREATED          STATUS                    PORTS                                                                            NAMES  
977e75774418   zabbix-web-nginx-mysql:centos-7.0-latest   "docker-entrypoint.sh"   15 minutes ago   Up 15 minutes (healthy)   0.0.0.0:80->8080/tcp, :::80->8080/tcp, 0.0.0.0:443->8443/tcp, :::443->8443/tcp   zabbix_docker-zabbix-web-nginx-mysql-1  
0770a23343e9   zabbix-server-mysql:centos-7.0-latest      "/usr/bin/tini -- /u…"   15 minutes ago   Up 15 minutes             0.0.0.0:10051->10051/tcp, :::10051->10051/tcp                                    zabbix_docker-zabbix-server-1  
98aecf59d879   zabbix-agent2:centos-7.0-latest            "/usr/bin/tini -- /u…"   15 minutes ago   Up 15 minutes             0.0.0.0:10050->10050/tcp, :::10050->10050/tcp, 31999/tcp                         zabbix_docker-zabbix-agent2-1  
ec9e9cd0ed74   zabbix-java-gateway:centos-7.0-latest      "docker-entrypoint.s…"   15 minutes ago   Up 15 minutes                                                                                              zabbix_docker-zabbix-java-gateway-1  
d0d7d7977b99   zabbix-snmptraps:centos-7.0-latest         "/usr/sbin/snmptrapd…"   15 minutes ago   Up 15 minutes             0.0.0.0:162->1162/udp, :::162->1162/udp                                          zabbix_docker-zabbix-snmptraps-1  
b72cdae7ba93   zabbix-web-service:centos-7.0-latest       "docker-entrypoint.s…"   15 minutes ago   Up 15 minutes                                                                                              zabbix_docker-zabbix-web-service-1  
0b8819153360   mariadb:10.5.19-focal                      "docker-entrypoint.s…"   15 minutes ago   Up 15 minutes             0.0.0.0:3306->3306/tcp, :::3306->3306/tcp                                        zabbix_docker-mysql-server-1  
[root@localhost zabbix_docker]#   
```
  
**集成全中文模板**  
  
![](https://img-blog.csdnimg.cn/img_convert/55715daf2df3eaa7a6e90c92d82309d0.png)  
  
![](https://img-blog.csdnimg.cn/img_convert/6359aa9e90881fe33fbb2f9ecfa21b9e.png)
`[Rocky8|centos7|centos8]`

**执行如下命令进行git安装**

```
yum -y install git
```

**执行如下命令克隆docker安装中文版zabbix项目**

```
ZBX_SOURCES=https://gitcode.net/1284524409/zabbix.git
ZBX_VERSION=zabbix_7.0.x_docker
ZBX_NAME=zabbix_docker-7.0-latest
ZBX_DIR=/opt
cd ${ZBX_DIR}
git -c advice.detachedHead=false clone ${ZBX_SOURCES} --branch ${ZBX_VERSION} --depth 1 --single-branch ${ZBX_DIR}/${ZBX_NAME}
chmod 755 -R ${ZBX_DIR}/${ZBX_NAME}
cd ${ZBX_DIR}/${ZBX_NAME}
```

**执行如下命令安装docker服务**

```
sh update_config-entrypoint_mysql.sh init
# sh update_config-entrypoint_pgsql.sh init
```

**执行如下命令下载docker镜像**

```
sh update_config-entrypoint_mysql.sh down
# sh update_config-entrypoint_mysql.sh down_proxy
# sh update_config-entrypoint_pgsql.sh down
# sh update_config-entrypoint_pgsql.sh down_proxy
```

**执行如下命令初始化配置文件**

```
sh update_config-entrypoint_mysql.sh cp
# sh update_config-entrypoint_mysql.sh cp_proxy
# sh update_config-entrypoint_pgsql.sh cp
# sh update_config-entrypoint_pgsql.sh cp_proxy
```

**执行如下命令启动docker容器**

```
sh update_config-entrypoint_mysql.sh start
# sh update_config-entrypoint_mysql.sh start_proxy
# sh update_config-entrypoint_pgsql.sh start
# sh update_config-entrypoint_pgsql.sh start_proxy
```

`[Ubuntu]`

`ubunt系统请参考如下命令手动执行`

```
root@ubuntu:/opt/zabbix_docker-7.0-latest# cat /etc/os-release | grep "Ubuntu "
PRETTY_NAME="Ubuntu 23.10"
ubuntu@ubuntu:~$ sudo sed -i 's/https:\/\/mirrors.aliyun.com/http:\/\/mirrors.cloud.aliyuncs.com/g' /etc/apt/sources.list
ubuntu@ubuntu:~$ sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
ubuntu@ubuntu:~$ curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | apt-key add -
ubuntu@ubuntu:~$ sudo passwd root
New password: 
Retype new password: 
passwd: password updated successfully
ubuntu@ubuntu:~$ su
Password: 
root@ubuntu:/home/ubuntu# curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | apt-key add -
Warning: apt-key is deprecated. Manage keyring files in trusted.gpg.d instead (see apt-key(8)).
OK
root@ubuntu:/home/ubuntu# add-apt-repository "deb [arch=amd64] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
root@ubuntu:/home/ubuntu# apt-get -y install docker-ce
root@ubuntu:/home/ubuntu# service docker start
root@ubuntu:/home/ubuntu# apt install git
root@ubuntu:/home/ubuntu# ZBX_SOURCES=https://gitcode.net/1284524409/zabbix.git
root@ubuntu:/home/ubuntu# ZBX_VERSION=zabbix_7.0.x_docker
root@ubuntu:/home/ubuntu# ZBX_NAME=zabbix_docker-7.0-latest
root@ubuntu:/home/ubuntu# ZBX_DIR=/opt
root@ubuntu:/home/ubuntu# cd ${ZBX_DIR}
root@ubuntu:/opt# git -c advice.detachedHead=false clone ${ZBX_SOURCES} --branch ${ZBX_VERSION} --depth 1 --single-branch ${ZBX_DIR}/${ZBX_NAME}
root@ubuntu:/opt# chmod 755 -R ${ZBX_DIR}/${ZBX_NAME}
root@ubuntu:/opt# cd ${ZBX_DIR}/${ZBX_NAME}
root@ubuntu:/opt/zabbix_docker-7.0-latest# ls -al /bin/sh
lrwxrwxrwx 1 root root 4 Jul 11  2023 /bin/sh -> dash
root@ubuntu:/opt/zabbix_docker-7.0-latest# sudo ln -fs /bin/bash /bin/sh
root@ubuntu:/opt/zabbix_docker-7.0-latest# ls -al /bin/sh
lrwxrwxrwx 1 root root 9 Jan 12 05:42 /bin/sh -> /bin/bash
root@ubuntu:/opt/zabbix_docker-7.0-latest# sh update_config-entrypoint_mysql.sh init
root@ubuntu:/opt/zabbix_docker-7.0-latest# sh update_config-entrypoint_mysql.sh down
root@ubuntu:/opt/zabbix_docker-7.0-latest# sh update_config-entrypoint_mysql.sh cp
root@ubuntu:/opt/zabbix_docker-7.0-latest# sh update_config-entrypoint_mysql.sh start
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
![](https://img-blog.csdnimg.cn/img_convert/3898d7faa3de8bc6dd1c00fb7e9f0806.png)

**启用zabbix插件
![](https://img-blog.csdnimg.cn/img_convert/f2fb7adc82f693acb60cc2f795a6597f.png)

**连接zabbix数据库插件**
![](https://img-blog.csdnimg.cn/img_convert/01bb2a2a4918bc5dd2d371a329efd46c.png)

**新建zabbix数据库连接**
`https://zabbix-web-nginx-mysql:8443/api_jsonrpc.php`

![](https://img-blog.csdnimg.cn/img_convert/55e97ccad77c7c88301574f638d6d0b7.png)

**输入正确的用户名密码**
`Admin/zabbix`

![](https://img-blog.csdnimg.cn/img_convert/c2eff0bfc204f6866d83b63e42652671.png)


**zabbix-server服务器同时优化成了rsyslog日志服务器，rsyslog日志端口为514**
日志存储路径为 /var/log/loki/

**grafana优化集成了zabbix与Loki插件**
请将任意.log后缀日志存入 /var/log/loki/即可连接到loki
URL为http://IP:3100
![](https://img-blog.csdnimg.cn/img_convert/4f4cb7f444a94411cc7619ad4b9fb316.png)

**存储位置**

映射的卷位于当前文件夹的zbx_env目录

**zabbix-server配置文件位置**
`/opt/zabbix_docker-7.0-latest/env_vars/.env_srv`

**后期如果有新版本发布可以通过如下命令更新zabbix版本**

```
sh update_config-entrypoint_mysql.sh stop
# sh update_config-entrypoint_pgsql.sh stop

ZBX_SOURCES=https://gitcode.net/1284524409/zabbix.git
ZBX_VERSION=zabbix_7.0.x_docker
ZBX_NAME=zabbix_docker-7.0-latest
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

sh update_config-entrypoint_mysql.sh down
# sh update_config-entrypoint_pgsql.sh down

sh update_config-entrypoint_mysql.sh start
# sh update_config-entrypoint_pgsql.sh start
```



`交流群`  
  
| zabbix-答疑群                                                                                                | zabbix-汉化群                                                                                                  |  
|:------------------------------------------------------------------------------------------:| :--: |
| ![微信打赏](https://img-blog.csdnimg.cn/img_convert/22d15cdf72b989f4bf132adbc705fcad.png) | ![微信打赏](https://img-blog.csdnimg.cn/img_convert/221620e1baaca5ce5fdbc7fc09bb675b.png) |

**全文完结** |
