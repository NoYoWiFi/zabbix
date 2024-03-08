#/bin/bash
#zabbix数据库history表清空
#zabbix数据库密码
DPassword="Passw0rd@123"
shellFolder=$(dirname $(readlink -f "$0"))
systemctl stop zabbix-server > $shellFolder/error 2>&1
if [ $? -ne '0' ]; then
 cat $shellFolder/error
 exit 1
fi
echo "zabbix-server stop success"
mysql -e "use zabbix;truncate table history;"
mysql -e "use zabbix;truncate table history_uint;"
mysql -e "use zabbix;truncate table trends;"
mysql -e "use zabbix;truncate table trends_uint;"
mysqldump -uroot zabbix > /tmp/zabbix.sql
mysql -e "drop database zabbix;"
mysql -e "create database zabbix character set utf8 collate utf8_bin;"
mysql -e "grant all privileges on zabbix.* to'zabbix'@'localhost' identified by '$DPassword';"
mysql -e "grant all privileges on zabbix.* to'zabbix'@'%' identified by '$DPassword';"
mysql -e "flush privileges;"
systemctl stop mariadb > $shellFolder/error 2>&1
if [ $? -ne '0' ]; then
 cat $shellFolder/error
 exit 1
fi
echo "mariadb stop success"
rm -rf /var/lib/mysql/ib*
systemctl start mariadb
mysql -uroot zabbix< /tmp/zabbix.sql
systemctl start zabbix-server
