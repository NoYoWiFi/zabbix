#/bin/bash
# 设置了这个选项以后，包含管道命令的语句的返回值，会变成最后一个返回非零的管道命令的返回值。
set -o pipefail

# 执行的时候如果出现了返回值为非零将会继续执行下面的脚本
set +e

# Script trace mode
set -o xtrace
#zabbix数据库密码
DPassword="123.com"
shellFolder=$(dirname $(readlink -f "$0"))
case ${1} in
    "trans")
        echo "trans"
        ;;
    "install")
        echo "install"
        ;;
    "proxy")
        echo "proxy"
        ;;
    *)
        echo "sh autosetup.sh [trans|install|proxy]"
        echo "Nothing to do"
        exit 1
        ;;
esac
function check_ip_status()
{
    ping -c 3 -i 0.2 -W 3 $1 &> /dev/null
    if [ $? -eq 0 ];then
        return 0
    else
        return 1
    fi
}
if [ -d "/etc/yum.repos.d/bak/" ];then
    echo "repo file ERROR"
    rm -f /etc/yum.repos.d/Rocky-Media.repo
    mv -vf /etc/yum.repos.d/bak/* /etc/yum.repos.d/
    rm -rf /etc/yum.repos.d/bak/
	\cp Rocky-AppStream.repo /etc/yum.repos.d/
	\cp Rocky-BaseOS.repo /etc/yum.repos.d/
fi
check_ip_status www.baidu.com
if [ $? -ne 0 ];then
    echo "No network, need ISO mount /media"
    if [ ! -d "/media/BaseOS/Packages/" ];then
        exit 1
    fi
    mkdir -p /etc/yum.repos.d/bak
    mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/bak
    \cp Rocky-Media.repo /etc/yum.repos.d/
else
	\cp Rocky-AppStream.repo /etc/yum.repos.d/
	\cp Rocky-BaseOS.repo /etc/yum.repos.d/
    touch /etc/yum.repos.d/MariaDB.repo
    cat > /etc/yum.repos.d/MariaDB.repo << EOF
# https://mariadb.org/download/
[mariadb]
name = MariaDB
# rpm.mariadb.org is a dynamic mirror if your preferred mirror goes offline. See https://mariadb.org/mirrorbits/ for details.
baseurl = https://mirrors.aliyun.com/mariadb/yum/11.2/rhel/\$releasever/\$basearch
# gpgkey = https://rpm.mariadb.org/RPM-GPG-KEY-MariaDB
gpgkey = https://mirrors.aliyun.com/mariadb/yum/RPM-GPG-KEY-MariaDB
gpgcheck = 1
EOF
    yum module disable mysql mariadb -y
    sudo dnf -y install MariaDB-server MariaDB-client
    if [ $? -ne '0' ]; then
     echo "ERROR!"
     exit 1
    fi
fi
#![配置时区]
timedatectl set-timezone Asia/Shanghai
chronyc -a makestep
#![安装php8.x]
dnf module reset php -y
dnf module enable php:8.0 -y
#![安装snmp及部分插件]
yum -y install nano net-snmp* net-tools unzip glibc-langpack-zh.x86_64 langpacks-zh_CN.noarch sysstat iotop rsyslog iperf3
#![安装grafana zabbix图形界面]
cat ./grafana/grafana-enterprise-* > ./grafana/grafana-enterprise.x86_64.rpm
yum -y install grafana/*.rpm
#![安装grafana zabbix插件]
unzip -qo ./grafana/alexanderzobnin-zabbix-app-*.zip -d /var/lib/grafana/plugins
chown grafana:grafana -R /var/lib/grafana/plugins/*
#![安装zabbix]
case ${1} in
    "proxy")
        echo "proxy"
        yum -y install packages/zabbix-agent2* packages/MariaDB* packages/tcping* packages/zabbix-get* packages/zabbix-java-gateway* \
        packages/zabbix-proxy-mysql* packages/zabbix-release* packages/zabbix-selinux-policy* \
        packages/zabbix-sender* packages/zabbix-sql-scripts* packages/fping*
        if [ $? -ne '0' ]; then
         echo "ERROR!"
         exit 1
        fi
        ;;
    *)
        yum -y install packages/*
        if [ $? -ne '0' ]; then
         echo "ERROR!"
         exit 1
        fi
        ;;
esac
systemctl start mariadb
if [ $? -ne '0' ]; then
 echo "ERROR!"
 exit 1
fi
#![创建zabbix数据库导入create_server_6.0-latest汉化模板]
mariadb -e "create database zabbix character set utf8mb4 collate utf8mb4_bin;"
mariadb -e "grant all privileges on zabbix.* to'zabbix'@'localhost' identified by '$DPassword';"
mariadb -e "grant all privileges on zabbix.* to'zabbix'@'%' identified by '$DPassword';"
mariadb -e "set character_set_server=utf8mb4;"
mariadb -e "flush privileges;"
# chmod 766 /usr/share/zabbix-sql-scripts/mysql/server.sql.gz
# zcat /usr/share/zabbix-sql-scripts/mysql/server.sql.gz | mariadb -h 127.0.0.1 -uzabbix -p$DPassword zabbix;
\cp ./patch/my.cnf /etc/
touch /var/log/mariadb.log
case ${1} in
    "trans")
        echo "trans"
        chmod 766 /usr/share/zabbix-sql-scripts/mysql/server.sql.gz
        zcat /usr/share/zabbix-sql-scripts/mysql/server.sql.gz | mariadb -h 127.0.0.1 -uzabbix -p$DPassword zabbix;
        ;;
    "install")
        echo "install"
        \cp mysql/create_server_6.0-latest_mysql.sql.gz /usr/share/zabbix-sql-scripts/mysql/
        chmod 766 /usr/share/zabbix-sql-scripts/mysql/create_server_6.0-latest_mysql.sql.gz
        zcat /usr/share/zabbix-sql-scripts/mysql/create_server_6.0-latest_mysql.sql.gz | mariadb -h 127.0.0.1 -uzabbix -p$DPassword zabbix;
        ;;
    "proxy")
        echo "proxy"
        chmod 766 /usr/share/zabbix-sql-scripts/mysql/proxy.sql
        cat /usr/share/zabbix-sql-scripts/mysql/proxy.sql | mariadb -h 127.0.0.1 -uzabbix -p$DPassword zabbix;
        ;;
    *)
        echo "Nothing to do"
        ;;
esac
#![关闭防火墙与selinux]
setenforce 0
service firewalld stop
chkconfig firewalld off
sed -i "/SELINUX=enforcing/s/SELINUX=enforcing/SELINUX=disabled/" /etc/selinux/config
sed -i -e "/zbx-agent2/d" /etc/hosts
echo "127.0.0.1 zbx-agent2" >> /etc/hosts
case ${1} in
    "proxy")
        echo "proxy"
        ;;
    *)
        #![配置nginx]
        \cp ./patch/nginx.conf /etc/nginx/nginx.conf
        \cp ./patch/zabbix.conf /etc/nginx/conf.d
        \cp ./patch/zabbix.conf.php /etc/zabbix/web/
        sed -i "/123.com/s/123.com/$DPassword/" /etc/zabbix/web/zabbix.conf.php
        #![为nginx配置https访问]
        mkdir -p /etc/pki/nginx
        \cp ./patch/server.pem /etc/pki/nginx/
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
        #![配置php-fpm]
        \cp ./php-fpm.d/zabbix.conf /etc/php-fpm.d/
        # sed -i "/date\.timezon/s/\; php_value\[date\.timezone\] = Europe\/Riga/php_value[date.timezone] = Asia\/Shanghai/" /etc/opt/rh/rh-php72/php-fpm.d/zabbix.conf
        ;;
esac
#![配置snmptrap]
\cp ./snmptrap/zabbix_trap_receiver.pl /usr/bin/
chmod a+x /usr/bin/zabbix_trap_receiver.pl
sed -i "/# authCommunity   log,execute,net public/s/# authCommunity   log,execute,net public/authCommunity   log,execute,net public/" /etc/snmp/snmptrapd.conf
sed -i "/zabbix_trap_receiver.pl/d" /etc/snmp/snmptrapd.conf
echo "perl do \"/usr/bin/zabbix_trap_receiver.pl\"" >> /etc/snmp/snmptrapd.conf
#![创建SNMP V3用户]
sed -i -e "/rouser/d" /etc/snmp/snmpd.conf
sed -i -e "/zabbix/d" /var/lib/net-snmp/snmpd.conf
net-snmp-create-v3-user -ro -A Admin@zabbix -a MD5 -X Admin@zabbix -x DES zabbix
case ${1} in
    "proxy")
        echo "proxy"
        ;;
    *)
        #![汉化web ui图形界面并解决web乱码问题]
        \cp patch/frontend_6.0.mo /usr/share/zabbix/locale/zh_CN/LC_MESSAGES/frontend.mo
        \cp ./patch/simkai.ttf /usr/share/zabbix/assets/fonts
        sed -i "/ZBX_GRAPH_FONT_NAME/s/graphfont/simkai/" /usr/share/zabbix/include/defines.inc.php
        sed -i "/ZBX_FONT_NAME/s/graphfont/simkai/" /usr/share/zabbix/include/defines.inc.php
        ;;
esac
#![解除打开文件数限制]
\cp ./patch/limits.conf /etc/security/
\cp ./patch/sysctl.conf /etc/
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

case ${1} in
    "proxy")
        echo "proxy"
        ZABBIX_CONFIG="/etc/zabbix/zabbix_proxy.conf"
        sed -i "/DBName=zabbix_proxy/s/DBName=.*/DBName=zabbix/" ${ZABBIX_CONFIG}
        ;;
    *)
        #![为grafana配置https访问]
        sed -i -e "/^;protocol =/s/=.*/= https/" /etc/grafana/grafana.ini
        sed -i -e "/^;cert_file =/s/=.*/= \/etc\/grafana\/ssl\/server.pem/" /etc/grafana/grafana.ini
        sed -i -e "/^;cert_key =/s/=.*/= \/etc\/grafana\/ssl\/server.pem/" /etc/grafana/grafana.ini
        sed -i -e "/^;protocol =/s/^;//" /etc/grafana/grafana.ini
        sed -i -e "/^;cert_file =/s/^;//" /etc/grafana/grafana.ini
        sed -i -e "/^;cert_key =/s/^;//" /etc/grafana/grafana.ini
        mkdir -p /etc/grafana/ssl
        \cp ./patch/server.pem /etc/grafana/ssl
        ZABBIX_CONFIG="/etc/zabbix/zabbix_server.conf"
        ;;
esac
#![优化zabbix_agent2.conf配置文件]
sed -i -e "/^\# Timeout/s/=.*/=30/" /etc/zabbix/zabbix_agent2.conf
sed -i -e "/^Timeout/s/=.*/=30/" /etc/zabbix/zabbix_agent2.conf
sed -i -e "/^\# Timeout/s/^# //" /etc/zabbix/zabbix_agent2.conf
# cp /usr/share/doc/zabbix-agent-*/userparameter_mysql.conf /etc/zabbix/zabbix_agentd.d/
#![优化zabbix_server.conf配置文件]
sed -i "/# DBHost=localhost/s/# DBHost=localhost/DBHost=localhost/" ${ZABBIX_CONFIG}
sed -i "/# DBPassword=/s/# DBPassword=/DBPassword=$DPassword/" ${ZABBIX_CONFIG}
sed -i "/# DBPort=/s/# DBPort=/DBPort=5432/" ${ZABBIX_CONFIG}
sed -i "/# ListenIP=0.0.0.0/s/# ListenIP=0.0.0.0/ListenIP=0.0.0.0/" ${ZABBIX_CONFIG}
sed -i "/# JavaGateway=/s/# JavaGateway=/JavaGateway=127.0.0.1/" ${ZABBIX_CONFIG}
sed -i "/# JavaGatewayPort=10052/s/# JavaGatewayPort=10052/JavaGatewayPort=10052/" ${ZABBIX_CONFIG}
sed -i "/# StartJavaPollers=0/s/# StartJavaPollers=0/StartJavaPollers=5/" ${ZABBIX_CONFIG}
sed -i "/# SNMPTrapperFile=\/tmp\/zabbix_traps.tmp/s/# SNMPTrapperFile=\/tmp\/zabbix_traps.tmp/SNMPTrapperFile=\/tmp\/zabbix_traps.tmp/" ${ZABBIX_CONFIG}
sed -i "/^SNMPTrapperFile=\/var\/log\/snmptrap\/snmptrap.log/s/SNMPTrapperFile=\/var\/log\/snmptrap\/snmptrap.log/# SNMPTrapperFile=\/var\/log\/snmptrap\/snmptrap.log/" ${ZABBIX_CONFIG}
sed -i "/# AllowUnsupportedDBVersions=0/s/# AllowUnsupportedDBVersions=0/AllowUnsupportedDBVersions=1/" ${ZABBIX_CONFIG}
sed -i -e "/^\# DebugLevel/s/=.*/=1/" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartPollers/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartProxyPollers/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartPreprocessors/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartSNMPTrapper/s/=.*/=1/" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartPollersUnreachable/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartTrappers/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartVMwareCollectors/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartPingers/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartDiscoverers/s/=.*/=50/" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartHTTPPollers/s/=.*/=3/" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartTimers/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartEscalators/s/=.*/=2/" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartAlerters/s/=.*/=5/" ${ZABBIX_CONFIG}
sed -i -e "/^\# MaxHousekeeperDelete/s/=.*/=0/" ${ZABBIX_CONFIG}
sed -i -e "/^\# CacheSize/s/=.*/=2G/" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartHistoryPollers/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^\# HistoryCacheSize/s/=.*/=2G/" ${ZABBIX_CONFIG}
sed -i -e "/^\# HistoryIndexCacheSize/s/=.*/=2G/" ${ZABBIX_CONFIG}
sed -i -e "/^\# HousekeepingFrequency/s/=.*/=0/" ${ZABBIX_CONFIG}
sed -i -e "/^\# TrendCacheSize/s/=.*/=2G/" ${ZABBIX_CONFIG}
sed -i -e "/^\# TrendFunctionCacheSize/s/=.*/=512M/" ${ZABBIX_CONFIG}
sed -i -e "/^\# ValueCacheSize/s/=.*/=64G/" ${ZABBIX_CONFIG}
sed -i -e "/^\# VMwareCacheSize/s/=.*/=2G/" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartIPMIPollers/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartLLDProcessors/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^\# Timeout/s/=.*/=30/" ${ZABBIX_CONFIG}
sed -i -e "/^\# UnreachableDelay/s/=.*/=90/" ${ZABBIX_CONFIG}
sed -i -e "/^\# UnreachablePeriod/s/=.*/=270/" ${ZABBIX_CONFIG}
sed -i -e "/^\# UnavailableDelay/s/=.*/=360/" ${ZABBIX_CONFIG}

sed -i -e "/^DebugLevel/s/=.*/=1/" ${ZABBIX_CONFIG}
sed -i -e "/^StartPollers/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^StartProxyPollers/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^StartPreprocessors/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^StartSNMPTrapper/s/=.*/=1/" ${ZABBIX_CONFIG}
sed -i -e "/^StartPollersUnreachable/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^StartTrappers/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^StartVMwareCollectors/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^StartPingers/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^StartDiscoverers/s/=.*/=50/" ${ZABBIX_CONFIG}
sed -i -e "/^StartHTTPPollers/s/=.*/=3/" ${ZABBIX_CONFIG}
sed -i -e "/^StartTimers/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^StartEscalators/s/=.*/=2/" ${ZABBIX_CONFIG}
sed -i -e "/^StartAlerters/s/=.*/=5/" ${ZABBIX_CONFIG}
sed -i -e "/^MaxHousekeeperDelete/s/=.*/=0/" ${ZABBIX_CONFIG}
sed -i -e "/^CacheSize/s/=.*/=2G/" ${ZABBIX_CONFIG}
sed -i -e "/^StartHistoryPollers/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^HistoryCacheSize/s/=.*/=2G/" ${ZABBIX_CONFIG}
sed -i -e "/^HistoryIndexCacheSize/s/=.*/=2G/" ${ZABBIX_CONFIG}
sed -i -e "/^HousekeepingFrequency/s/=.*/=0/" ${ZABBIX_CONFIG}
sed -i -e "/^TrendCacheSize/s/=.*/=2G/" ${ZABBIX_CONFIG}
sed -i -e "/^TrendFunctionCacheSize/s/=.*/=512M/" ${ZABBIX_CONFIG}
sed -i -e "/^ValueCacheSize/s/=.*/=64G/" ${ZABBIX_CONFIG}
sed -i -e "/^VMwareCacheSize/s/=.*/=2G/" ${ZABBIX_CONFIG}
sed -i -e "/^StartIPMIPollers/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^StartLLDProcessors/s/=.*/=100/" ${ZABBIX_CONFIG}
sed -i -e "/^Timeout/s/=.*/=30/" ${ZABBIX_CONFIG}
sed -i -e "/^UnreachableDelay/s/=.*/=90/" ${ZABBIX_CONFIG}
sed -i -e "/^UnreachablePeriod/s/=.*/=270/" ${ZABBIX_CONFIG}
sed -i -e "/^UnavailableDelay/s/=.*/=360/" ${ZABBIX_CONFIG}

sed -i -e "/^\# DebugLevel/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartPollers/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartProxyPollers/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartPreprocessors/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartSNMPTrapper/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartPollersUnreachable/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartTrappers/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartVMwareCollectors/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartPingers/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartDiscoverers/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartHTTPPollers/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartTimers/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartEscalators/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartAlerters/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# MaxHousekeeperDelete/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# CacheSize/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartHistoryPollers/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# HistoryCacheSize/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# HistoryIndexCacheSize/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# HousekeepingFrequency/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# TrendCacheSize/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# TrendFunctionCacheSize/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# ValueCacheSize/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# VMwareCacheSize/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartIPMIPollers/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# StartLLDProcessors/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# Timeout/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# UnreachableDelay/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# UnreachablePeriod/s/^# //" ${ZABBIX_CONFIG}
sed -i -e "/^\# UnavailableDelay/s/^# //" ${ZABBIX_CONFIG}
#![配置日志服务rsyslog]
systemctl start rsyslog
\cp ./patch/loki.conf /etc/rsyslog.d/
\cp ./patch/loki /etc/logrotate.d/loki
sed -i -e "/^\#module(load=\"imudp\")/s/^#//" /etc/rsyslog.conf
sed -i -e "/^\#input(type=\"imudp\"/s/^#//" /etc/rsyslog.conf
sed -i -e "/^\#module(load=\"imtcp\")/s/^#//" /etc/rsyslog.conf
sed -i -e "/^\#input(type=\"imtcp\"/s/^#//" /etc/rsyslog.conf
sed -i -e "/^\module(load=\"builtin:omfile\"/s/^\(.*\)$/# \1/" /etc/rsyslog.conf
systemctl restart rsyslog
case ${1} in
    "proxy")
        #![安装grafana loki日志分析服务]
        mkdir -p /var/log/loki
        chmod 755 /var/log/loki
        touch /var/log/loki/alert.log
        chmod 666 /var/log/loki/alert.log
        sed -i -e "/^\      __path__:/s/:.*/: \/var\/log\/loki\/\*log/" /etc/promtail/config.yml
        ;;
    *)
        #![安装grafana loki日志分析服务]
        mkdir -p /var/log/loki
        chmod 755 /var/log/loki
        \cp ./patch/echo.sh /usr/lib/zabbix/alertscripts/
        chmod +x /usr/lib/zabbix/alertscripts/echo.sh
        chown zabbix:zabbix /usr/lib/zabbix/alertscripts/echo.sh
        touch /var/log/loki/alert.log
        chmod 666 /var/log/loki/alert.log
        sed -i -e "/^\      __path__:/s/:.*/: \/var\/log\/loki\/\*log/" /etc/promtail/config.yml
        ;;
esac
#![配置开机启动服务]
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
cd ${shellFolder}/mysql
case ${1} in
    "install")
        chmod a+rw -R /var/log/loki/
        systemctl start php-fpm
        systemctl enable php-fpm
        systemctl start nginx
        systemctl enable nginx
        systemctl start zabbix-server
        systemctl enable zabbix-server
        sh mysql.sh
        ;;
    "proxy")
        systemctl start zabbix-proxy
        systemctl enable zabbix-proxy
        sh mysql.sh
        ;;
    "trans")
        systemctl start php-fpm
        systemctl enable php-fpm
        systemctl start nginx
        systemctl enable nginx
        systemctl disable zabbix-server
        ;;
    *)
        echo "Nothing to do"
        ;;
esac
netstat -nltp | grep '10050\|10051\|10052\|3306\|8443\|3000'
# rm -rf ${shellFolder}*
