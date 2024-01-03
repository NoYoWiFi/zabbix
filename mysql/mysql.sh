#/bin/bash
mariadb zabbix -e "DROP PROCEDURE partition_maintenance_all;" > /dev/null 2>&1
mariadb zabbix -e "DROP PROCEDURE partition_create;" > /dev/null 2>&1
mariadb zabbix -e "DROP PROCEDURE partition_drop;" > /dev/null 2>&1
mariadb zabbix -e "DROP PROCEDURE partition_drop_gt;" > /dev/null 2>&1
mariadb zabbix -e "DROP PROCEDURE partition_maintenance;" > /dev/null 2>&1
mariadb zabbix -e "DROP PROCEDURE partition_verify;" > /dev/null 2>&1
mariadb zabbix -e "DROP EVENT zbx_partitioning;" > /dev/null 2>&1
mariadb zabbix < ./zbx_db_partitiong.sql
# mariadb zabbix -e "CALL partition_maintenance_all('zabbix');"
lv_on=$(cat /etc/my.cnf |grep 'event_scheduler = ON')
echo $lv_on
if [[ x"$lv_on" != x ]]
then
    sed -i '/event_scheduler = ON/d' /etc/my.cnf
    sed -i '/max_connections = 2000/d' /etc/my.cnf
    sed -i '$d' /etc/my.cnf
fi
echo "[mysqld]" >> /etc/my.cnf
echo "event_scheduler = ON" >> /etc/my.cnf
echo "max_connections = 2000" >> /etc/my.cnf
systemctl restart mariadb
mariadb zabbix -e "ALTER TABLE zabbix.history ADD primary key (itemid,clock,ns);" > /dev/null 2>&1
mariadb zabbix -e "ALTER TABLE zabbix.history_log ADD primary key (itemid,clock,ns);" > /dev/null 2>&1
mariadb zabbix -e "ALTER TABLE zabbix.history_str ADD primary key (itemid,clock,ns);" > /dev/null 2>&1
mariadb zabbix -e "ALTER TABLE zabbix.history_text ADD primary key (itemid,clock,ns);" > /dev/null 2>&1
mariadb zabbix -e "ALTER TABLE zabbix.history_uint ADD primary key (itemid,clock,ns);" > /dev/null 2>&1
mariadb zabbix -e "ALTER TABLE zabbix.trends ADD primary key (itemid,clock);" > /dev/null 2>&1
mariadb zabbix -e "ALTER TABLE zabbix.trends_uint ADD primary key (itemid,clock);" > /dev/null 2>&1
mariadb zabbix -e "ALTER TABLE zabbix.proxy_history ADD primary key (id,itemid,clock,ns);" > /dev/null 2>&1
mariadb zabbix -e "ALTER TABLE zabbix.history DROP PRIMARY KEY,ADD primary key (itemid,clock,ns);" > /dev/null 2>&1
mariadb zabbix -e "ALTER TABLE zabbix.history_log DROP PRIMARY KEY,ADD primary key (itemid,clock,ns);" > /dev/null 2>&1
mariadb zabbix -e "ALTER TABLE zabbix.history_str DROP PRIMARY KEY,ADD primary key (itemid,clock,ns);" > /dev/null 2>&1
mariadb zabbix -e "ALTER TABLE zabbix.history_text DROP PRIMARY KEY,ADD primary key (itemid,clock,ns);" > /dev/null 2>&1
mariadb zabbix -e "ALTER TABLE zabbix.history_uint DROP PRIMARY KEY,ADD primary key (itemid,clock,ns);" > /dev/null 2>&1
mariadb zabbix -e "ALTER TABLE zabbix.trends DROP PRIMARY KEY,ADD primary key (itemid,clock);" > /dev/null 2>&1
mariadb zabbix -e "ALTER TABLE zabbix.trends_uint DROP PRIMARY KEY,ADD primary key (itemid,clock);" > /dev/null 2>&1
mariadb zabbix -e "ALTER TABLE zabbix.proxy_history DROP PRIMARY KEY,ADD primary key (id,itemid,clock,ns);" > /dev/null 2>&1

mariadb zabbix -e "SHOW VARIABLES LIKE 'event_scheduler'";
mariadb zabbix -e "CREATE EVENT zbx_partitioning ON SCHEDULE EVERY 12 HOUR DO CALL partition_maintenance_all('zabbix');"
mariadb zabbix -e "SELECT * FROM INFORMATION_SCHEMA.events\G"
mariadb zabbix -e "CALL partition_maintenance_all('zabbix');" > /dev/null 2>&1
mariadb zabbix -e "CALL partition_maintenance_all('zabbix');"
mariadb zabbix -e "show create table history\G"
mariadb zabbix -e "desc history"
#管理-一般-管家
# 历史记录
#  开启内部管家
#  覆盖监控项历史期间 √
#  数据存储期         7d
# 趋势
#  开启内部管家
#  覆盖监控项历史期间 √
#  数据存储期         365d

# --单独调用维护某个表创建、删除、增加分区存储过程
# 语法格式：
# CALL partition_maintenance('<zabbix_db_name>', '<table_name>', <days_to_keep_data>, <hourly_interval>, <num_future_intervals_to_create>)
# 说明：
# zabbix_db_name：数据库的名称
# table_name：要创建分区表的表名称
# days_to_keep_data：保存分区表数据的天数，超出这个天数的分区表将被删除，单位是天
# hourly_interval：每隔多少小时创建一个分区，单位是小时
# num_future_intervals_to_create：每次创建几个分区
# 案例：
# CALL partition_maintenance('zabbix', 'history', 28, 24, 14);  --对zabbix数据库的history表创建分区，数据保留28天，每隔24小时创建一个分区，每次创建14个分区
#--保留3天历史数据
# mariadb zabbix -e "CALL partition_drop('zabbix', 'history', $(date -d "-4 day" +%Y%m%d)2400);" 
# mariadb zabbix -e "CALL partition_drop('zabbix', 'history_log', $(date -d "-4 day" +%Y%m%d)2400);"
# mariadb zabbix -e "CALL partition_drop('zabbix', 'history_str', $(date -d "-4 day" +%Y%m%d)2400);"
# mariadb zabbix -e "CALL partition_drop('zabbix', 'history_text', $(date -d "-4 day" +%Y%m%d)2400);"
# mariadb zabbix -e "CALL partition_drop('zabbix', 'history_uint', $(date -d "-4 day" +%Y%m%d)2400);"
# mariadb zabbix -e "CALL partition_drop('zabbix', 'trends', $(date -d "-4 day" +%Y%m%d)2400);"
# mariadb zabbix -e "CALL partition_drop('zabbix', 'trends_uint', $(date -d "-4 day" +%Y%m%d)2400);"
# mariadb zabbix -e "CALL partition_drop('zabbix', 'proxy_history', $(date -d "-4 day" +%Y%m%d)2400);"
# 
# --调用维护预定义的表创建、删除、增加分区的存储过程
# CALL partition_maintenance_all('zabbix');

