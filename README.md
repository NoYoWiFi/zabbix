==持续更新最新版本...==
# 全自动安装方法
1. 下载一键安装脚本
[一键安装脚本](https://gitcode.net/1284524409/zabbix/-/archive/rocky_8_zabbix_6.0.x_mysql/zabbix-rocky_8_zabbix_6.0.x_mysql.tar.gz)
2. 执行命令全自动安装zabbix-server
```
tar -zxvf zabbix-rocky_8_zabbix_6.0.x_mysql.tar.gz
cd zabbix-rocky_8_zabbix_6.0.x_mysql
sh autosetup.sh install
```
3. 执行命令全自动安装zabbix-proxy
```
tar -zxvf zabbix-rocky_8_zabbix_6.0.x_mysql.tar.gz
cd zabbix-rocky_8_zabbix_6.0.x_mysql
sh autosetup.sh proxy
```
4. [Rocky8.9系统下载](https://mirrors.aliyun.com/rockylinux/8/isos/x86_64/)
5. [Rocky系统bug报告](https://bugs.rockylinux.org/my_view_page.php?refresh=true)
# 手动安装方法
1. 操作系统：Rocky8
2. 数据库版本
```shell
[root@localhost /]# rpm -qa | grep MariaDB
MariaDB-common-11.1.2-1.el8.x86_64
MariaDB-shared-11.1.2-1.el8.x86_64
MariaDB-client-11.1.2-1.el8.x86_64
MariaDB-server-compat-11.1.2-1.el8.noarch
MariaDB-client-compat-11.1.2-1.el8.noarch
MariaDB-server-11.1.2-1.el8.x86_64
[root@localhost /]# 
```
3. zabbix 版本
```shell
[root@localhost /]# rpm -qa | grep zabbix
zabbix-web-deps-6.0.25-release1.el8.noarch
zabbix-server-mysql-6.0.25-release1.el8.x86_64
zabbix-sender-6.0.25-release1.el8.x86_64
zabbix-get-6.0.25-release1.el8.x86_64
zabbix-agent2-plugin-mongodb-6.0.25-release1.el8.x86_64
zabbix-web-6.0.25-release1.el8.noarch
zabbix-web-mysql-6.0.25-release1.el8.noarch
zabbix-nginx-conf-6.0.25-release1.el8.noarch
zabbix-proxy-mysql-6.0.25-release1.el8.x86_64
zabbix-agent2-6.0.25-release1.el8.x86_64
zabbix-sql-scripts-6.0.25-release1.el8.noarch
zabbix-selinux-policy-6.0.25-release1.el8.x86_64
zabbix-js-6.0.25-release1.el8.x86_64
zabbix-agent2-plugin-postgresql-6.0.25-release2.el8.x86_64
zabbix-java-gateway-6.0.25-release1.el8.x86_64
zabbix-web-service-6.0.25-release1.el8.x86_64
zabbix-release-6.0-4.el8.noarch
[root@localhost /]# 
```
4. 设置yum 
```shell
sed -e 's|^mirrorlist=|#mirrorlist=|g' \
    -e 's|^#baseurl=http://dl.rockylinux.org/$contentdir|baseurl=https://mirrors.aliyun.com/rockylinux|g' \
    -i.bak \
    /etc/yum.repos.d/Rocky-*.repo

yum clean all
yum makecache
yum -y install wget
```
5. 安装MariaDB
```shell
cat > /etc/yum.repos.d/MariaDB.repo << EOF
# MariaDB 10.11.2 CentOS repository list - created 2023-03-24 01:38 UTC
# https://mariadb.org/download/
[mariadb]
name = MariaDB
# rpm.mariadb.org is a dynamic mirror if your preferred mirror goes offline. See https://mariadb.org/mirrorbits/ for details.
# baseurl = https://rpm.mariadb.org/10.11.3/centos/\$releasever/\$basearch
baseurl = https://mirrors.aliyun.com/mariadb/yum/11.1/rhel/\$releasever/\$basearch
# gpgkey = https://rpm.mariadb.org/RPM-GPG-KEY-MariaDB
gpgkey = https://mirrors.aliyun.com/mariadb/yum/RPM-GPG-KEY-MariaDB
gpgcheck = 1
EOF
yum module disable mysql mariadb -y
sudo dnf -y install MariaDB-server MariaDB-client
systemctl start mariadb
```

6. 安装snmp及部分插件
```shell
yum -y install nano net-snmp* net-tools unzip glibc-langpack-zh.x86_64 langpacks-zh_CN.noarch sysstat iotop rsyslog
```

7. 安装zabbix
```shell
wget -P /tmp/ https://repo.zabbix.com/zabbix/6.0/rhel/8/x86_64/zabbix-release-latest.el8.noarch.rpm
rpm -ivhU --force /tmp/zabbix-release-latest.el8.noarch.rpm
sed -i -e "/^enabled=0/s/=.*/=1/" /etc/yum.repos.d/zabbix.repo
cat > /tmp/packages  << EOF
zabbix-agent2
zabbix-agent2-plugin-mongodb
zabbix-agent2-plugin-postgresql
zabbix-get
zabbix-java-gateway
zabbix-js
zabbix-nginx-conf
zabbix-proxy-mysql
zabbix-selinux-policy
zabbix-sender
zabbix-server-mysql
zabbix-sql-scripts
zabbix-web
zabbix-web-deps
zabbix-web-mysql
zabbix-web-service
EOF
cat /tmp/packages | xargs yum -y install
```
8. 创建zabbix数据库导入create_server_6.0-latest汉化模板
```shell
DPassword="123.com"
mariadb -e "create database zabbix character set utf8mb4 collate utf8mb4_bin;"
mariadb -e "grant all privileges on zabbix.* to'zabbix'@'localhost' identified by '$DPassword';"
mariadb -e "grant all privileges on zabbix.* to'zabbix'@'%' identified by '$DPassword';"
mariadb -e "set character_set_server=utf8mb4;"
mariadb -e "flush privileges;"
cd /tmp
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/patch/my.cnf
\cp /tmp/my.cnf /etc/
touch /var/log/mariadb.log
cd /tmp
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/mysql/create_server_6.0-latest.sql.gz
\cp /tmp/create_server_6.0-latest.sql.gz /usr/share/zabbix-sql-scripts/mysql/
chmod 766 /usr/share/zabbix-sql-scripts/mysql/create_server_6.0-latest.sql.gz
zcat /usr/share/zabbix-sql-scripts/mysql/create_server_6.0-latest.sql.gz | mariadb -h 127.0.0.1 -uzabbix -p$DPassword zabbix;
```
9. 关闭防火墙与selinux
```shell
setenforce 0
service firewalld stop
chkconfig firewalld off
sed -i "/SELINUX=enforcing/s/SELINUX=enforcing/SELINUX=disabled/" /etc/selinux/config
```
10. 配置nginx
```shell
cd /tmp
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/patch/nginx.conf
\cp /tmp/nginx.conf /etc/nginx/nginx.conf
cd /tmp
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/patch/zabbix.conf
\cp /tmp/zabbix.conf /etc/nginx/conf.d
DPassword="123.com"
cd /tmp
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/patch/zabbix.conf.php
\cp /tmp/zabbix.conf.php /etc/zabbix/web/
sed -i "/123.com/s/123.com/$DPassword/" /etc/zabbix/web/zabbix.conf.php
```
11. 为nginx配置https访问
```shell
mkdir -p /etc/pki/nginx
cd /tmp
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/patch/server.pem
\cp /tmp/server.pem /etc/pki/nginx/
sed -i -e "/listen/d" /etc/nginx/conf.d/zabbix.conf
sed -i -e "/server {/a\ \tlisten 8080;\n\tlisten 8443 ssl;" /etc/nginx/conf.d/zabbix.conf
sed -i -e "/ssl_/d" /etc/nginx/conf.d/zabbix.conf
sed -i -e "/if /,+2d" /etc/nginx/conf.d/zabbix.conf
sed -i -e "/8443 ssl/a\ \tssl_certificate \"/etc/pki/nginx/server.pem\";\n\
\tssl_certificate_key \"/etc/pki/nginx/server.pem\";\n\
\tssl_session_cache shared:SSL:1m;\n\
\tssl_session_timeout  10m;\n\
#\tssl_ciphers PROFILE=SYSTEM;\n\
\tssl_prefer_server_ciphers on;\n\
\tif (\$server_port = 8080) {\n\
\t\trewrite ^(\.\*)\$ https://\$host:8443\$1 permanent;\n\
\t}\
" /etc/nginx/conf.d/zabbix.conf
```
12. 配置php-fpm
```shell
cd /tmp
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/php-fpm.d/zabbix.conf
\cp /tmp/zabbix.conf /etc/php-fpm.d/
```
13. 配置snmptrap
```shell
cd /tmp
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/snmptrap/zabbix_trap_receiver.pl
\cp /tmp/zabbix_trap_receiver.pl /usr/bin/
chmod a+x /usr/bin/zabbix_trap_receiver.pl
sed -i "/# authCommunity   log,execute,net public/s/# authCommunity   log,execute,net public/authCommunity   log,execute,net public/" /etc/snmp/snmptrapd.conf
sed -i "/zabbix_trap_receiver.pl/d" /etc/snmp/snmptrapd.conf
echo "perl do \"/usr/bin/zabbix_trap_receiver.pl\"" >> /etc/snmp/snmptrapd.conf
```
14. 配置SNMPv3登录权限
```
systemctl start snmpd
sed -i -e "/rouser/d" /etc/snmp/snmpd.conf
sed -i -e "/zabbix/d" /var/lib/net-snmp/snmpd.conf
systemctl stop snmpd
net-snmp-create-v3-user -ro -A Admin@zabbix -a MD5 -X Admin@zabbix -x DES zabbix
```
15. 汉化web ui图形界面并解决web乱码问题
```shell
cd /tmp
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/patch/frontend_6.0.mo
\cp /tmp/frontend_6.0.mo /usr/share/zabbix/locale/zh_CN/LC_MESSAGES/frontend.mo
cd /tmp
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/patch/simkai.ttf
\cp /tmp/simkai.ttf /usr/share/zabbix/assets/fonts
sed -i "/ZBX_GRAPH_FONT_NAME/s/graphfont/simkai/" /usr/share/zabbix/include/defines.inc.php
sed -i "/ZBX_FONT_NAME/s/graphfont/simkai/" /usr/share/zabbix/include/defines.inc.php
```
16. 解除打开文件数限制
```shell
cd /tmp
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/patch/limits.conf
\cp /tmp/limits.conf /etc/security/
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/patch/sysctl.conf
\cp /tmp/sysctl.conf /etc/

sed -i -e "/^DefaultLimitCORE=/s/=.*/=infinity/" /etc/systemd/system.conf
sed -i -e "/^#DefaultLimitNOFILE=/s/=.*/=100000/" /etc/systemd/system.conf
sed -i -e "/^#DefaultLimitNPROC=/s/=.*/=100000/" /etc/systemd/system.conf
# sed -i -e "/^LimitNOFILE=/s/=.*/=655350/" /usr/lib/systemd/system/mariadb.service

sed -i -e "/^\#DefaultLimitNOFILE=/s/^#//" /etc/systemd/system.conf
sed -i -e "/^\#DefaultLimitNPROC=/s/^#//" /etc/systemd/system.conf


sed -i -e "/^#DefaultLimitCORE=/s/=.*/=infinity/" /etc/systemd/user.conf
sed -i -e "/^#DefaultLimitNOFILE=/s/=.*/=100000/" /etc/systemd/user.conf
sed -i -e "/^#DefaultLimitNPROC=/s/=.*/=100000/" /etc/systemd/user.conf

sed -i -e "/^\#DefaultLimitCORE=/s/^#//" /etc/systemd/user.conf
sed -i -e "/^\#DefaultLimitNOFILE=/s/^#//" /etc/systemd/user.conf
sed -i -e "/^\#DefaultLimitNPROC=/s/^#//" /etc/systemd/user.conf
```
17. 优化zabbix_agent2.conf配置文件
```shell
sed -i -e "/^\# Timeout/s/=.*/=30/" /etc/zabbix/zabbix_agent2.conf
sed -i -e "/^Timeout/s/=.*/=30/" /etc/zabbix/zabbix_agent2.conf
sed -i -e "/^\# Timeout/s/^# //" /etc/zabbix/zabbix_agent2.conf
```
18. 优化zabbix_server.conf配置文件
```shell
DPassword="123.com"
sed -i "/# DBHost=localhost/s/# DBHost=localhost/DBHost=localhost/" /etc/zabbix/zabbix_server.conf
sed -i "/# DBPassword=/s/# DBPassword=/DBPassword=$DPassword/" /etc/zabbix/zabbix_server.conf
sed -i "/# DBPort=/s/# DBPort=/DBPort=5432/" /etc/zabbix/zabbix_server.conf
sed -i "/# ListenIP=0.0.0.0/s/# ListenIP=0.0.0.0/ListenIP=0.0.0.0/" /etc/zabbix/zabbix_server.conf
sed -i "/# JavaGateway=/s/# JavaGateway=/JavaGateway=127.0.0.1/" /etc/zabbix/zabbix_server.conf
sed -i "/# JavaGatewayPort=10052/s/# JavaGatewayPort=10052/JavaGatewayPort=10052/" /etc/zabbix/zabbix_server.conf
sed -i "/# StartJavaPollers=0/s/# StartJavaPollers=0/StartJavaPollers=5/" /etc/zabbix/zabbix_server.conf

sed -i "/# SNMPTrapperFile=\/tmp\/zabbix_traps.tmp/s/# SNMPTrapperFile=\/tmp\/zabbix_traps.tmp/SNMPTrapperFile=\/tmp\/zabbix_traps.tmp/" /etc/zabbix/zabbix_server.conf
sed -i "/^SNMPTrapperFile=\/var\/log\/snmptrap\/snmptrap.log/s/SNMPTrapperFile=\/var\/log\/snmptrap\/snmptrap.log/# SNMPTrapperFile=\/var\/log\/snmptrap\/snmptrap.log/" /etc/zabbix/zabbix_server.conf
sed -i "/# AllowUnsupportedDBVersions=0/s/# AllowUnsupportedDBVersions=0/AllowUnsupportedDBVersions=1/" /etc/zabbix/zabbix_server.conf

# sed -i "/date\.timezon/s/\; php_value\[date\.timezone\] = Europe\/Riga/php_value[date.timezone] = Asia\/Shanghai/" /etc/opt/rh/rh-php72/php-fpm.d/zabbix.conf
# cp /usr/share/doc/zabbix-agent-*/userparameter_mysql.conf /etc/zabbix/zabbix_agentd.d/

#[zabbix-server]
sed -i -e "/^\# DebugLevel/s/=.*/=1/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartPollers/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartProxyPollers/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartPreprocessors/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartSNMPTrapper/s/=.*/=1/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartPollersUnreachable/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartTrappers/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartVMwareCollectors/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartPingers/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartDiscoverers/s/=.*/=3/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartHTTPPollers/s/=.*/=3/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartTimers/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartEscalators/s/=.*/=2/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartAlerters/s/=.*/=5/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# MaxHousekeeperDelete/s/=.*/=0/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# CacheSize/s/=.*/=2G/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartHistoryPollers/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# HistoryCacheSize/s/=.*/=2G/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# HistoryIndexCacheSize/s/=.*/=2G/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# HousekeepingFrequency/s/=.*/=0/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# TrendCacheSize/s/=.*/=2G/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# TrendFunctionCacheSize/s/=.*/=512M/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# ValueCacheSize/s/=.*/=64G/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# VMwareCacheSize/s/=.*/=2G/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartIPMIPollers/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartLLDProcessors/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# Timeout/s/=.*/=30/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# UnreachableDelay/s/=.*/=90/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# UnreachablePeriod/s/=.*/=270/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# UnavailableDelay/s/=.*/=360/" /etc/zabbix/zabbix_server.conf

sed -i -e "/^DebugLevel/s/=.*/=1/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^StartPollers/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^StartProxyPollers/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^StartPreprocessors/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^StartSNMPTrapper/s/=.*/=1/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^StartPollersUnreachable/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^StartTrappers/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^StartVMwareCollectors/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^StartPingers/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^StartDiscoverers/s/=.*/=3/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^StartHTTPPollers/s/=.*/=3/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^StartTimers/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^StartEscalators/s/=.*/=2/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^StartAlerters/s/=.*/=5/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^MaxHousekeeperDelete/s/=.*/=0/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^CacheSize/s/=.*/=2G/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^StartHistoryPollers/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^HistoryCacheSize/s/=.*/=2G/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^HistoryIndexCacheSize/s/=.*/=2G/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^HousekeepingFrequency/s/=.*/=0/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^TrendCacheSize/s/=.*/=2G/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^TrendFunctionCacheSize/s/=.*/=512M/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^ValueCacheSize/s/=.*/=64G/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^VMwareCacheSize/s/=.*/=2G/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^StartIPMIPollers/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^StartLLDProcessors/s/=.*/=100/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^Timeout/s/=.*/=30/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^UnreachableDelay/s/=.*/=90/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^UnreachablePeriod/s/=.*/=270/" /etc/zabbix/zabbix_server.conf
sed -i -e "/^UnavailableDelay/s/=.*/=360/" /etc/zabbix/zabbix_server.conf

sed -i -e "/^\# DebugLevel/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartPollers/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartProxyPollers/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartPreprocessors/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartSNMPTrapper/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartPollersUnreachable/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartTrappers/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartVMwareCollectors/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartPingers/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartDiscoverers/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartHTTPPollers/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartTimers/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartEscalators/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartAlerters/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# MaxHousekeeperDelete/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# CacheSize/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartHistoryPollers/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# HistoryCacheSize/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# HistoryIndexCacheSize/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# HousekeepingFrequency/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# TrendCacheSize/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# TrendFunctionCacheSize/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# ValueCacheSize/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# VMwareCacheSize/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartIPMIPollers/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# StartLLDProcessors/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# Timeout/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# UnreachableDelay/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# UnreachablePeriod/s/^# //" /etc/zabbix/zabbix_server.conf
sed -i -e "/^\# UnavailableDelay/s/^# //" /etc/zabbix/zabbix_server.conf
```
19. 安装grafana zabbix图形界面
```shell
# wget -P /tmp/ https://mirrors.huaweicloud.com/grafana/10.2.3/grafana-enterprise-10.2.3-1.x86_64.rpm
cd /tmp/
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/grafana/grafana-enterprise-10.1.0-1.x86_64_00.rpm
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/grafana/grafana-enterprise-10.1.0-1.x86_64_01.rpm
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/grafana/grafana-enterprise-10.1.0-1.x86_64_02.rpm
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/grafana/grafana-enterprise-10.1.0-1.x86_64_03.rpm
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/grafana/grafana-enterprise-10.1.0-1.x86_64_04.rpm
cat ./grafana-enterprise-10.1.0-1.x86_64.rpm_0* > ./grafana-enterprise-10.1.0-1.x86_64.rpm
yum -y install /tmp/grafana-enterprise-10.1.0-1.x86_64.rpm
# wget -P /tmp/ https://github.com/grafana/grafana-zabbix/releases/download/v4.4.4/alexanderzobnin-zabbix-app-4.4.4.linux_amd64.zip
cd /tmp/
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/grafana/alexanderzobnin-zabbix-app-4.4.1.linux_amd64.zip
unzip -qo /tmp/alexanderzobnin-zabbix-app-*.zip -d /var/lib/grafana/plugins
chown grafana:grafana -R /var/lib/grafana/plugins/*
```
20. 为grafana配置https访问
```shell
sed -i -e "/^;protocol =/s/=.*/= https/" /etc/grafana/grafana.ini
sed -i -e "/^;cert_file =/s/=.*/= \/etc\/grafana\/ssl\/server.pem/" /etc/grafana/grafana.ini
sed -i -e "/^;cert_key =/s/=.*/= \/etc\/grafana\/ssl\/server.pem/" /etc/grafana/grafana.ini

sed -i -e "/^;protocol =/s/^;//" /etc/grafana/grafana.ini
sed -i -e "/^;cert_file =/s/^;//" /etc/grafana/grafana.ini
sed -i -e "/^;cert_key =/s/^;//" /etc/grafana/grafana.ini
mkdir -p /etc/grafana/ssl
cd /tmp/
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/patch/server.pem
\cp /tmp/server.pem /etc/grafana/ssl
```
21. 配置日志服务rsyslog
```shell
cd /tmp/
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/patch/loki.conf
\cp /tmp/loki.conf /etc/rsyslog.d/
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/patch/loki
\cp /tmp/loki /etc/logrotate.d/loki
sed -i -e "/^\# module(load=\"imudp\")/s/^# //" /etc/rsyslog.conf
sed -i -e "/^\# input(type=\"imudp\"/s/^# //" /etc/rsyslog.conf
sed -i -e "/^\# module(load=\"imtcp\")/s/^# //" /etc/rsyslog.conf
sed -i -e "/^\# input(type=\"imtcp\"/s/^# //" /etc/rsyslog.conf
sed -i -e "/^\module(load=\"builtin:omfile\"/s/^\(.*\)$/# \1/" /etc/rsyslog.conf
systemctl restart rsyslog
```
22. 安装grafana loki日志分析服务
```shell
cd /tmp/
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/grafana/loki-2.8.4.x86_64.rpm
yum -y install /tmp/loki-2.8.4.x86_64.rpm
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/grafana/promtail-2.8.4.x86_64.rpm
yum -y install /tmp/promtail-2.8.4.x86_64.rpm
mkdir -p /var/log/loki
chmod 755 /var/log/loki
cd /tmp/
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/patch/echo.sh
\cp /tmp/echo.sh /usr/lib/zabbix/alertscripts/
chmod +x /usr/lib/zabbix/alertscripts/echo.sh
chown zabbix:zabbix /usr/lib/zabbix/alertscripts/echo.sh
touch /var/log/loki/alert.log
chmod 666 /var/log/loki/alert.log
sed -i -e "/^\      __path__:/s/:.*/: \/var\/log\/loki\/\*log/" /etc/promtail/config.yml

```

23. 为mysql分区
```shell
cd /tmp/
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/mysql/mysql.sh
curl -# -O https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/mysql/zbx_db_partitiong.sql
sh mysql.sh
```
24. 配置开机启动服务
```shell
sysctl -p 
systemctl daemon-reload
systemctl daemon-reexec
chown root:zabbix /usr/sbin/fping
chmod 755 /usr/sbin/fping
chmod +s /usr/sbin/fping
systemctl start zabbix-agent2
systemctl enable zabbix-agent2
systemctl start zabbix-java-gateway
systemctl enable zabbix-java-gateway
systemctl start zabbix-proxy
systemctl enable zabbix-proxy
systemctl start php-fpm
systemctl enable php-fpm
systemctl start nginx
systemctl enable nginx
systemctl enable mariadb
systemctl restart mariadb
systemctl daemon-reload
systemctl restart grafana-server
systemctl enable grafana-server.service
systemctl restart loki
systemctl enable loki.service
systemctl restart promtail
systemctl enable promtail.service
systemctl start snmptrapd
systemctl enable snmptrapd
systemctl start snmpd
systemctl enable snmpd
systemctl start zabbix-server
systemctl enable zabbix-server
netstat -nltp | grep '10050\|10051\|10052\|3306\|80\|3000'
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
![](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/vx_images/2cc17fdd154217656975030bc6636523.png)

**启用zabbix插件
![](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/vx_images/844a584f0789fc28205b2b5a8302938c.png)

**连接zabbix数据库插件**
![](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/vx_images/c87b39af3050dac2ecb62c7365bc7a7b.png)

**新建zabbix数据库连接**
`https://zabbix-web-nginx-mysql:8443/api_jsonrpc.php`

![](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/vx_images/c68d9dbf98134214aa759dd25bbfbb2e.png)

**输入正确的用户名密码**
`Admin/zabbix`

![](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/vx_images/aa5fd658ee04a9dd7687e459b3064dbe.png)


**zabbix-server服务器同时优化成了rsyslog日志服务器，rsyslog日志端口为514**
日志存储路径为 /var/log/loki/

**grafana优化集成了zabbix与Loki插件**
请将任意.log后缀日志存入 /var/log/loki/即可连接到loki
URL为http://IP:3100
![在这里插入图片描述](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/vx_images/c469826e35f6d0735418cbb9ca008b22.png)


`感谢打赏`  
  
| 微信                        |支付宝|  
|---------------------------|---|  
|  ![微信打赏](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/thanks_wx.jpg) |![微信打赏](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/thanks_zfb.jpg)|  
  
  
**全文完结**