**zabbix 版本**

`6.0.27`

**项目地址**  
[GitCode项目地址](https://gitcode.net/1284524409/zabbix/-/tree/zabbix_docker)

**效果图**
```  
[root@localhost zbx]# docker images;
REPOSITORY                                                     TAG                                   IMAGE ID       CREATED          SIZE
zabbix-web-nginx-pgsql                                         rocky-6.0-latest                      b67b259b0a8b   7 minutes ago    441MB
zabbix-server-pgsql                                            rocky-6.0-latest                      d89d656e4dd2   7 minutes ago    431MB
zabbix-proxy-pgsql                                             rocky-6.0-latest                      1eabdf15a0a0   7 minutes ago    425MB
zabbix-web-service                                             rocky-6.0-latest                      0b5517385135   8 minutes ago    473MB
zabbix-java-gateway                                            rocky-6.0-latest                      787d686971f9   26 minutes ago   460MB
zabbix-agent2                                                  rocky-6.0-latest                      27d8d0a3e994   26 minutes ago   307MB
zabbix-build-pgsql                                             rocky-6.0-latest                      dc70e7fdf506   2 hours ago      2.07GB
zabbix-server-mysql                                            rocky-6.0-latest                      0ecb5beeb87f   3 hours ago      512MB
zabbix-proxy-mysql                                             rocky-6.0-latest                      90d6b14d4fe1   3 hours ago      496MB
zabbix-web-nginx-mysql                                         rocky-6.0-latest                      f76d91be3616   8 hours ago      515MB
zabbix-snmptraps                                               rocky-6.0-latest                      7123f3cc0a20   24 hours ago     286MB
zabbix-build-mysql                                             rocky-6.0-latest                      a070dc2c9bc1   31 hours ago     2.07GB
zabbix-build-base                                              rocky-6.0-latest                      9c35feed350f   32 hours ago     1.39GB
mariadb                                                        11.2.3                                7d65ebbd4dce   47 hours ago     405MB
timescale/timescaledb                                          2.13.0-pg16                           37796458a471   3 weeks ago      284MB
grafana/grafana-enterprise                                     10.0.11                               55a918349323   4 weeks ago      351MB
grafana/loki                                                   2.9.4                                 652b79950756   5 weeks ago      74.6MB
grafana/promtail                                               2.9.4                                 1c7475004f2f   5 weeks ago      198MB
rockylinux                                                     8                                     c24baca6f6df   8 weeks ago      228MB

```  
  
**集成全中文模板**  
  
![](https://gitcode.net/1284524409/zabbix/-/raw/zabbix_docker/vx_images/8f09f045a9dc42a0bb47d97e3ec5963b.png)  
  
![](https://gitcode.net/1284524409/zabbix/-/raw/zabbix_docker/vx_images/ce76ece189844eaa94629d9c59beb845.png)

`[Rocky8|centos7|centos8]`

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
# sh update_config-entrypoint_mysql.sh prxdown
# sh update_config-entrypoint_pgsql.sh down
# sh update_config-entrypoint_pgsql.sh prxdown
```

**执行如下命令初始化配置文件**

```
sh update_config-entrypoint_mysql.sh cp
# sh update_config-entrypoint_pgsql.sh cp
```

**执行如下命令启动docker容器**

```
sh update_config-entrypoint_mysql.sh start
# sh update_config-entrypoint_mysql.sh prxstart
# sh update_config-entrypoint_pgsql.sh start
# sh update_config-entrypoint_pgsql.sh prxstart
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
sh update_config-entrypoint_mysql.sh stop
# sh update_config-entrypoint_pgsql.sh stop

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

sh update_config-entrypoint_mysql.sh down
# sh update_config-entrypoint_pgsql.sh down

sh update_config-entrypoint_mysql.sh start
# sh update_config-entrypoint_pgsql.sh start
```

`[Ubuntu]`

`ubunt系统请参考如下命令手动执行`

```
root@ubuntu:/opt/zabbix_docker-6.0-latest# cat /etc/os-release | grep "Ubuntu "
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
root@ubuntu:/home/ubuntu# ZBX_VERSION=zabbix_docker
root@ubuntu:/home/ubuntu# ZBX_NAME=zabbix_docker-6.0-latest
root@ubuntu:/home/ubuntu# ZBX_DIR=/opt
root@ubuntu:/home/ubuntu# cd ${ZBX_DIR}
root@ubuntu:/opt# git -c advice.detachedHead=false clone ${ZBX_SOURCES} --branch ${ZBX_VERSION} --depth 1 --single-branch ${ZBX_DIR}/${ZBX_NAME}
root@ubuntu:/opt# chmod 755 -R ${ZBX_DIR}/${ZBX_NAME}
root@ubuntu:/opt# cd ${ZBX_DIR}/${ZBX_NAME}
root@ubuntu:/opt/zabbix_docker-6.0-latest# ls -al /bin/sh
lrwxrwxrwx 1 root root 4 Jul 11  2023 /bin/sh -> dash
root@ubuntu:/opt/zabbix_docker-6.0-latest# sudo ln -fs /bin/bash /bin/sh
root@ubuntu:/opt/zabbix_docker-6.0-latest# ls -al /bin/sh
lrwxrwxrwx 1 root root 9 Jan 12 05:42 /bin/sh -> /bin/bash
root@ubuntu:/opt/zabbix_docker-6.0-latest# sh update_config-entrypoint_mysql.sh init
root@ubuntu:/opt/zabbix_docker-6.0-latest# sh update_config-entrypoint_mysql.sh down
root@ubuntu:/opt/zabbix_docker-6.0-latest# sh update_config-entrypoint_mysql.sh cp
root@ubuntu:/opt/zabbix_docker-6.0-latest# sh update_config-entrypoint_mysql.sh start
```

`交流群`  
  
| zabbix-答疑群                                                                                                | zabbix-汉化群                                                                                                  |  
|:------------------------------------------------------------------------------------------:| :--: |
| ![微信打赏](https://gitcode.net/1284524409/zabbix/-/raw/zabbix_docker/vx_images/zabbix-dayi.png) | ![微信打赏](https://gitcode.net/1284524409/zabbix/-/raw/zabbix_docker/vx_images/zabbix-hanhua.png) |

**全文完结**