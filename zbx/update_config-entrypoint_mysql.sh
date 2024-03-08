#!/bin/bash
###
### hello to use the shell
###
### Usage:
###
###    sh update_config-entrypoint.sh [update]
###
###
### Options:
###   update      Config dockerfiles
###   help        Show this message.
###   update base build1 build12 make cp start
# 设置了这个选项以后，包含管道命令的语句的返回值，会变成最后一个返回非零的管道命令的返回值。
set -o pipefail

# 执行的时候如果出现了返回值为非零将会继续执行下面的脚本
set +e

# Script trace mode
set -o xtrace

GV_ENV_SHELL="./patch/.env_shell"
source ./patch/getEnv.sh
GV_VERSION=${GV_ARR_ENV[GV_ZABBIX_VERSION]}
GV_VERSION_DOCKER=${GV_ARR_ENV[GV_ZABBIX_POSTFIX]}
BUILD_CONFIG="./build.sh"
ZABBIX_BUILD_BASE="./Dockerfiles/build-base/centos/Dockerfile"
ZABBIX_BUILD_MYSQL="./Dockerfiles/build-mysql/centos/Dockerfile"
ZABBIX_SERVER_MYSQL="./Dockerfiles/server-mysql/centos/Dockerfile"
ZABBIX_SERVER_MYSQL_ENTRYPOINT="./Dockerfiles/server-mysql/centos/docker-entrypoint.sh"
WEB_NGINX_MYSQL="./Dockerfiles/web-nginx-mysql/centos/Dockerfile"
WEB_NGINX_MYSQL_NGINX_CONF="./Dockerfiles/web-nginx-mysql/centos/conf/etc/zabbix/nginx.conf"
WEB_NGINX_ENTRYPOINT="./Dockerfiles/web-nginx-mysql/centos/docker-entrypoint.sh"
ZABBIX_AGENT2="./Dockerfiles/agent2/centos/Dockerfile"
ZABBIX_AGENT2_ENTRYPOINT="./Dockerfiles/agent2/centos/docker-entrypoint.sh"
ZABBIX_SNMPTRAPS="./Dockerfiles/snmptraps/centos/Dockerfile"
ZABBIX_JAVA_GATEWAY="./Dockerfiles/java-gateway/centos/Dockerfile"
ZABBIX_PROXY_MYSQL="./Dockerfiles/proxy-mysql/centos/Dockerfile"
ZABBIX_PROXY_MYSQL_ENTRYPOINT="./Dockerfiles/proxy-mysql/centos/docker-entrypoint.sh"
ZABBIX_WEB_SERVICE="./Dockerfiles/web-service/centos/Dockerfile"

help() {
    awk -F'### ' '/^###/ { print $2 }' "$0"
}

init() {
sed -i -e "/:centos-/s/:centos-.*/:centos-${GV_VERSION_DOCKER}/" docker-compose_v6_0_x_centos_mysql_local.yaml
sed -i -e "/version=\${version:-/s/-.*/-\"${GV_VERSION_DOCKER}\"}/" $BUILD_CONFIG
chmod 755 -R ./
option=$(cat /etc/redhat-release | cut -c 22)
if [[ " " == "${option}" ]]; then
	option=$(cat /etc/redhat-release | cut -c 23)
fi
if [[ "." == "${option}" ]]; then
	option=$(cat /etc/redhat-release | cut -c 21)
fi
case ${option} in
    8)
    echo "Centos 8 catch!"
    if [ ! -d "/etc/yum.repos.d/bak/" ]; then
        mkdir /etc/yum.repos.d/bak/
        mv /etc/yum.repos.d/* /etc/yum.repos.d/bak/
        tar -zxvf ./patch/rockylinux_8/repos.tar.gz -C /etc/yum.repos.d/
    fi
    yum install -y yum-utils \
        device-mapper-persistent-data \
        lvm2
    yum-config-manager \
        --add-repo \
        https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
    yum -y install docker-ce docker-ce-cli containerd.io --allowerasing
    yum -y install git rsyslog
    \cp ./trans/create_server_${GV_VERSION_DOCKER}_mysql.sql.gz ./patch/create_server.sql.gz
    ;;
    7)
    echo "Centos 7 catch!"
        yum install -y yum-utils \
            device-mapper-persistent-data \
            lvm2
        yum-config-manager \
            --add-repo \
            https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
        yum -y install docker-ce docker-ce-cli containerd.io
        yum -y install git rsyslog
        \cp ./trans/create_server_${GV_VERSION_DOCKER}_mysql.sql.gz ./patch/create_server.sql.gz
    ;;
    *)
    echo "Nothing to do"
    ;;
esac
service docker start
mkdir /etc/docker
touch /etc/docker/daemon.json
cat > /etc/docker/daemon.json << EOF
{
  "registry-mirrors": ["https://xb10bnbv.mirror.aliyuncs.com"]
}
EOF
PS_DOCKER=$(ps -ef | grep docker | grep -vE grep | grep -oE '.sock')
if [${PS_DOCKER} = ""]; then
    service docker restart
fi
chmod 777 /var/run/docker.sock
update_config_var $ZABBIX_BUILD_BASE "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
if [ ! -f "/usr/local/bin/docker-compose" ]; then
    # curl -SL https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    \cp ./patch/docker-compose-linux-x86_64 /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi
}

zabbix_build_base() {
sed -i -e "/^FROM quay/s/FROM .*/FROM ${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE]}/" $ZABBIX_BUILD_BASE
update_config_var $ZABBIX_BUILD_BASE "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
if [ ! -f "./Dockerfiles/build-base/centos/go1.19.13.linux-amd64.tar.gz" ]; then
    \cp ./patch/go1.19.13.linux-amd64.tar.gz ./Dockerfiles/build-base/centos/
fi
sed -i -e "/^ADD/,+1d" "$ZABBIX_BUILD_BASE"
sed -i '/RUN/i ADD go1.19.13.linux-amd64.tar.gz /usr/local/\n' $ZABBIX_BUILD_BASE
sed -i -e "/^    case/,+24d" "$ZABBIX_BUILD_BASE"
}

zabbix_build_mysql() {
sed -i -e "/^FROM quay/s/FROM .*/FROM ${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE]}/" $ZABBIX_BUILD_MYSQL
update_config_var $ZABBIX_BUILD_MYSQL "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
sed -i -e "/^ADD/,+1d" "$ZABBIX_BUILD_MYSQL"
\cp ./patch/zabbix-${GV_VERSION}.tar.gz ./Dockerfiles/build-mysql/centos/
\cp ./patch/mongodb_plugin.tar.gz ./Dockerfiles/build-mysql/centos/
\cp ./patch/postgresql_plugin.tar.gz ./Dockerfiles/build-mysql/centos/
\cp ./patch/create_server.sql.gz ./Dockerfiles/build-mysql/centos/
\cp ./patch/NotoSansCJKjp-hinted.zip ./Dockerfiles/build-mysql/centos/
sed -i -e "/^    go/d" "$ZABBIX_BUILD_MYSQL"
sed -i -e "/^ADD/,+1d" "$ZABBIX_BUILD_MYSQL"
sed -i -e "/^ADD/,+1d" "$ZABBIX_BUILD_MYSQL"
sed -i -e "/^    git -c/d" "$ZABBIX_BUILD_MYSQL"
sed -i "/RUN/i ADD zabbix-${GV_VERSION}.tar.gz /tmp/\nADD mongodb_plugin.tar.gz /tmp/\nADD postgresql_plugin.tar.gz /tmp/\n" $ZABBIX_BUILD_MYSQL
sed -i '/RUN/i ADD create_server.sql.gz /tmp/\n' $ZABBIX_BUILD_MYSQL
sed -i -e "/^ADD NotoSansCJKjp-hinted.zip/,+1d" "$ZABBIX_BUILD_MYSQL"
sed -i -e "/mkdir \/tmp\/fonts\//d" "$ZABBIX_BUILD_MYSQL"
sed -i '/RUN/i ADD NotoSansCJKjp-hinted.zip /tmp/fonts/\n' $ZABBIX_BUILD_MYSQL
sed -i '/    cp \/tmp\/create_server.sql.gz/d' $ZABBIX_BUILD_MYSQL
sed -i '/    strip \/tmp\/zabbix-\${ZBX_VERSION}\/src\/zabbix_agent\/zabbix_agentd \&\& \\/i\    cp /tmp/create_server.sql.gz database/mysql/create_server.sql.gz && \\' $ZABBIX_BUILD_MYSQL
sed -i '/.\/configure \\/i\    export GOPROXY=https://goproxy.cn && \\\n    go env -w GOPROXY=https://goproxy.cn && \\' $ZABBIX_BUILD_MYSQL
sed -i -e "/curl --tlsv1/d" $ZABBIX_BUILD_MYSQL
}

zabbix_server_mysql() {
if [ ! -f "./Dockerfiles/server-mysql/centos/zbx_db_partitiong.sql" ]; then
    \cp ./patch/zbx_db_partitiong.sql ./Dockerfiles/server-mysql/centos/
fi
if [ ! -f "./Dockerfiles/server-mysql/centos/pip.sh" ]; then
    \cp ./patch/pip.sh ./Dockerfiles/server-mysql/centos/
fi
if [ ! -f "./Dockerfiles/server-mysql/centos/tcping-1.3.5-19.el8.x86_64.rpm" ]; then
    \cp ./patch/tcping-1.3.5-19.el8.x86_64.rpm ./Dockerfiles/server-mysql/centos/
fi
sed -i -e "/^FROM quay/s/FROM .*/FROM ${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE]}/" $ZABBIX_SERVER_MYSQL
update_config_var $ZABBIX_SERVER_MYSQL "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
sed -i -e "/^ADD/,+3d" "$ZABBIX_SERVER_MYSQL"
sed -i '/STOPSIGNAL SIGTERM/i ADD tcping-1.3.5-19.el8.x86_64.rpm /tmp/tcping-1.3.5-19.el8.x86_64.rpm\nADD pip.sh /tmp/pip.sh\nADD zbx_db_partitiong.sql /opt/\n' $ZABBIX_SERVER_MYSQL
sed -i -e "/    microdnf -y clean all/d" "$ZABBIX_SERVER_MYSQL"
sed -i -e "/    sh \/tmp\/pip.sh/,+1d" "$ZABBIX_SERVER_MYSQL"
sed -i '/EXPOSE 10051/i\    microdnf -y clean all && \\\n    sh /tmp/pip.sh\n' $ZABBIX_SERVER_MYSQL
sed -i -e "/microdnf download libcurl/s/^/#/" $ZABBIX_SERVER_MYSQL
sed -i -e "/rpm -Uvh --nodeps --replacefiles/s/^/#/" $ZABBIX_SERVER_MYSQL
sed -i -e "/microdnf remove -y libcurl-minimal/s/^/#/" $ZABBIX_SERVER_MYSQL
sed -i -e "/rm -rf \"\*curl/s/^/#/" $ZABBIX_SERVER_MYSQL
# exec_sql_file
sed -i -e "275,301{/^    mysql --silent/,+16d}" $ZABBIX_SERVER_MYSQL_ENTRYPOINT
var_value_01="    mysql --silent --skip-column-names \\"
var_value_02="                --default-character-set=utf8mb4 \\"
var_value_03="                -h \${DB_SERVER_HOST} -P \${DB_SERVER_PORT} \\"
var_value_04="                -u \${DB_SERVER_ROOT_USER} \$ssl_opts \\"
var_value_05="                \${DB_SERVER_DBNAME} < /opt/zbx_db_partitiong.sql"
var_value_06="    mysql_query \"use zabbix;ALTER TABLE zabbix.history DROP PRIMARY KEY,ADD primary key (itemid,clock,ns);\" 1>/dev/null"
var_value_06_1="    mysql_query \"use zabbix;ALTER TABLE zabbix.history_log DROP PRIMARY KEY,ADD primary key (itemid,clock,ns);\" 1>/dev/null"
var_value_06_2="    mysql_query \"use zabbix;ALTER TABLE zabbix.history_str DROP PRIMARY KEY,ADD primary key (itemid,clock,ns);\" 1>/dev/null"
var_value_06_3="    mysql_query \"use zabbix;ALTER TABLE zabbix.history_text DROP PRIMARY KEY,ADD primary key (itemid,clock,ns);\" 1>/dev/null"
var_value_06_4="    mysql_query \"use zabbix;ALTER TABLE zabbix.history_uint DROP PRIMARY KEY,ADD primary key (itemid,clock,ns);\" 1>/dev/null"
var_value_06_5="    mysql_query \"use zabbix;ALTER TABLE zabbix.trends DROP PRIMARY KEY,ADD primary key (itemid,clock);\" 1>/dev/null"
var_value_06_6="    mysql_query \"use zabbix;ALTER TABLE zabbix.trends_uint DROP PRIMARY KEY,ADD primary key (itemid,clock);\" 1>/dev/null"
var_value_06_7="    mysql_query \"use zabbix;ALTER TABLE zabbix.proxy_history DROP PRIMARY KEY,ADD primary key (id,itemid,clock,ns);\" 1>/dev/null"

var_value_07="    mysql_query \"use zabbix;SHOW VARIABLES LIKE 'event_scheduler';\" 1>/dev/null"
var_value_08="    mysql_query \"use zabbix;CREATE EVENT zbx_partitioning ON SCHEDULE EVERY 12 HOUR DO CALL partition_maintenance_all('zabbix');\" 1>/dev/null"
var_value_09="    mysql_query \"use zabbix;SELECT * FROM INFORMATION_SCHEMA.events\G\" 1>/dev/null"
var_value_10="    mysql_query \"use zabbix;CALL partition_maintenance_all('zabbix');\" 1>/dev/null"
var_value_01=$(escape_spec_char "$var_value_01")
var_value_02=$(escape_spec_char "$var_value_02")
var_value_03=$(escape_spec_char "$var_value_03")
var_value_04=$(escape_spec_char "$var_value_04")
var_value_05=$(escape_spec_char "$var_value_05")
var_value_06=$(escape_spec_char "$var_value_06")
var_value_06_1=$(escape_spec_char "$var_value_06_1")
var_value_06_2=$(escape_spec_char "$var_value_06_2")
var_value_06_3=$(escape_spec_char "$var_value_06_3")
var_value_06_4=$(escape_spec_char "$var_value_06_4")
var_value_06_5=$(escape_spec_char "$var_value_06_5")
var_value_06_6=$(escape_spec_char "$var_value_06_6")
var_value_06_7=$(escape_spec_char "$var_value_06_7")
var_value_07=$(escape_spec_char "$var_value_07")
var_value_08=$(escape_spec_char "$var_value_08")
var_value_09=$(escape_spec_char "$var_value_09")
var_value_10=$(escape_spec_char "$var_value_10")
# exec_sql_file
NUMINDEX=$(sed -n -e '257,301{/unset MYSQL_PWD/=}' $ZABBIX_SERVER_MYSQL_ENTRYPOINT)
sed -i "${NUMINDEX}i\\$var_value_10" $ZABBIX_SERVER_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_09" $ZABBIX_SERVER_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_08" $ZABBIX_SERVER_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_07" $ZABBIX_SERVER_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_06_7" $ZABBIX_SERVER_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_06_6" $ZABBIX_SERVER_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_06_5" $ZABBIX_SERVER_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_06_4" $ZABBIX_SERVER_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_06_3" $ZABBIX_SERVER_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_06_2" $ZABBIX_SERVER_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_06_1" $ZABBIX_SERVER_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_06" $ZABBIX_SERVER_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_05" $ZABBIX_SERVER_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_04" $ZABBIX_SERVER_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_03" $ZABBIX_SERVER_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_02" $ZABBIX_SERVER_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_01" $ZABBIX_SERVER_MYSQL_ENTRYPOINT
}

zabbix_proxy_mysql() {
if [ ! -f "./Dockerfiles/proxy-mysql/centos/zbx_db_partitiong.sql" ]; then
    \cp ./patch/zbx_db_partitiong.sql ./Dockerfiles/proxy-mysql/centos/
fi
if [ ! -f "./Dockerfiles/proxy-mysql/centos/pip.sh" ]; then
    \cp ./patch/pip.sh ./Dockerfiles/proxy-mysql/centos/
fi
if [ ! -f "./Dockerfiles/proxy-mysql/centos/tcping-1.3.5-19.el8.x86_64.rpm" ]; then
    \cp ./patch/tcping-1.3.5-19.el8.x86_64.rpm ./Dockerfiles/proxy-mysql/centos/
fi
sed -i -e "/^FROM quay/s/FROM .*/FROM ${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE]}/" $ZABBIX_PROXY_MYSQL
update_config_var $ZABBIX_PROXY_MYSQL "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
sed -i -e "/^ADD/,+3d" "$ZABBIX_PROXY_MYSQL"
sed -i '/STOPSIGNAL SIGTERM/i ADD tcping-1.3.5-19.el8.x86_64.rpm /tmp/tcping-1.3.5-19.el8.x86_64.rpm\nADD pip.sh /tmp/pip.sh\nADD zbx_db_partitiong.sql /opt/\n' $ZABBIX_PROXY_MYSQL
sed -i -e "/    microdnf -y clean all/d" "$ZABBIX_PROXY_MYSQL"
sed -i -e "/    sh \/tmp\/pip.sh/,+1d" "$ZABBIX_PROXY_MYSQL"
sed -i '/EXPOSE 10051/i\    microdnf -y clean all && \\\n    sh /tmp/pip.sh\n' $ZABBIX_PROXY_MYSQL
sed -i -e "/microdnf download libcurl/s/^/#/" $ZABBIX_SERVER_MYSQL
sed -i -e "/rpm -Uvh --nodeps --replacefiles/s/^/#/" $ZABBIX_SERVER_MYSQL
sed -i -e "/microdnf remove -y libcurl-minimal/s/^/#/" $ZABBIX_SERVER_MYSQL
sed -i -e "/rm -rf \"\*curl/s/^/#/" $ZABBIX_SERVER_MYSQL
# exec_sql_file
sed -i -e "275,301{/^    mysql --silent/,+16d}" $ZABBIX_PROXY_MYSQL_ENTRYPOINT
var_value_01="    mysql --silent --skip-column-names \\"
var_value_02="                --default-character-set=utf8mb4 \\"
var_value_03="                -h \${DB_SERVER_HOST} -P \${DB_SERVER_PORT} \\"
var_value_04="                -u \${DB_SERVER_ROOT_USER} \$ssl_opts \\"
var_value_05="                \${DB_SERVER_DBNAME} < /opt/zbx_db_partitiong.sql"
var_value_06="    mysql_query \"use zabbix;ALTER TABLE zabbix.history DROP PRIMARY KEY,ADD primary key (itemid,clock,ns);\" 1>/dev/null"
var_value_06_1="    mysql_query \"use zabbix;ALTER TABLE zabbix.history_log DROP PRIMARY KEY,ADD primary key (itemid,clock,ns);\" 1>/dev/null"
var_value_06_2="    mysql_query \"use zabbix;ALTER TABLE zabbix.history_str DROP PRIMARY KEY,ADD primary key (itemid,clock,ns);\" 1>/dev/null"
var_value_06_3="    mysql_query \"use zabbix;ALTER TABLE zabbix.history_text DROP PRIMARY KEY,ADD primary key (itemid,clock,ns);\" 1>/dev/null"
var_value_06_4="    mysql_query \"use zabbix;ALTER TABLE zabbix.history_uint DROP PRIMARY KEY,ADD primary key (itemid,clock,ns);\" 1>/dev/null"
var_value_06_5="    mysql_query \"use zabbix;ALTER TABLE zabbix.trends DROP PRIMARY KEY,ADD primary key (itemid,clock);\" 1>/dev/null"
var_value_06_6="    mysql_query \"use zabbix;ALTER TABLE zabbix.trends_uint DROP PRIMARY KEY,ADD primary key (itemid,clock);\" 1>/dev/null"
var_value_06_7="    mysql_query \"use zabbix;ALTER TABLE zabbix.proxy_history DROP PRIMARY KEY,ADD primary key (id,itemid,clock,ns);\" 1>/dev/null"

var_value_07="    mysql_query \"use zabbix;SHOW VARIABLES LIKE 'event_scheduler';\" 1>/dev/null"
var_value_08="    mysql_query \"use zabbix;CREATE EVENT zbx_partitioning ON SCHEDULE EVERY 12 HOUR DO CALL partition_maintenance_all('zabbix');\" 1>/dev/null"
var_value_09="    mysql_query \"use zabbix;SELECT * FROM INFORMATION_SCHEMA.events\G\" 1>/dev/null"
var_value_10="    mysql_query \"use zabbix;CALL partition_maintenance_all('zabbix');\" 1>/dev/null"
var_value_01=$(escape_spec_char "$var_value_01")
var_value_02=$(escape_spec_char "$var_value_02")
var_value_03=$(escape_spec_char "$var_value_03")
var_value_04=$(escape_spec_char "$var_value_04")
var_value_05=$(escape_spec_char "$var_value_05")
var_value_06=$(escape_spec_char "$var_value_06")
var_value_06_1=$(escape_spec_char "$var_value_06_1")
var_value_06_2=$(escape_spec_char "$var_value_06_2")
var_value_06_3=$(escape_spec_char "$var_value_06_3")
var_value_06_4=$(escape_spec_char "$var_value_06_4")
var_value_06_5=$(escape_spec_char "$var_value_06_5")
var_value_06_6=$(escape_spec_char "$var_value_06_6")
var_value_06_7=$(escape_spec_char "$var_value_06_7")
var_value_07=$(escape_spec_char "$var_value_07")
var_value_08=$(escape_spec_char "$var_value_08")
var_value_09=$(escape_spec_char "$var_value_09")
var_value_10=$(escape_spec_char "$var_value_10")
# exec_sql_file
NUMINDEX=$(sed -n -e '264,301{/unset MYSQL_PWD/=}' $ZABBIX_PROXY_MYSQL_ENTRYPOINT)
sed -i "${NUMINDEX}i\\$var_value_10" $ZABBIX_PROXY_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_09" $ZABBIX_PROXY_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_08" $ZABBIX_PROXY_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_07" $ZABBIX_PROXY_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_06_7" $ZABBIX_PROXY_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_06_6" $ZABBIX_PROXY_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_06_5" $ZABBIX_PROXY_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_06_4" $ZABBIX_PROXY_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_06_3" $ZABBIX_PROXY_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_06_2" $ZABBIX_PROXY_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_06_1" $ZABBIX_PROXY_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_06" $ZABBIX_PROXY_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_05" $ZABBIX_PROXY_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_04" $ZABBIX_PROXY_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_03" $ZABBIX_PROXY_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_02" $ZABBIX_PROXY_MYSQL_ENTRYPOINT
sed -i "${NUMINDEX}i\\$var_value_01" $ZABBIX_PROXY_MYSQL_ENTRYPOINT
}

zabbix_web_nginx_mysql() {
if [ ! -f "./Dockerfiles/web-nginx-mysql/centos/simkai.ttf" ]; then
    \cp ./patch/simkai.ttf ./Dockerfiles/web-nginx-mysql/centos/
fi
if [ ! -f "./Dockerfiles/web-nginx-mysql/centos/${GV_ARR_ENV[GV_WEB_UI_FILE_NAME]}" ]; then
    \cp ./patch/${GV_ARR_ENV[GV_WEB_UI_FILE_NAME]} ./Dockerfiles/web-nginx-mysql/centos/
fi
if [ ! -f "./Dockerfiles/web-nginx-mysql/centos/nginx.sh" ]; then
    \cp ./patch/nginx.sh ./Dockerfiles/web-nginx-mysql/centos/
fi
sed -i -e "/^FROM quay/s/FROM .*/FROM ${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE]}/" $WEB_NGINX_MYSQL
update_config_var $WEB_NGINX_MYSQL "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
sed -i -e "/^ADD/,+1d" $WEB_NGINX_MYSQL
sed -i -e "/^            curl-minimal/s/            curl-minimal/#            curl-minimal/" $WEB_NGINX_MYSQL
sed -i -e "/--nodocs \${INSTALL_PKGS}/s/--nodocs \${INSTALL_PKGS}/--nodocs \${INSTALL_PKGS} tzdata/" $WEB_NGINX_MYSQL
sed -i '/STOPSIGNAL SIGTERM/i ADD simkai.ttf /usr/share/zabbix/assets/fonts/\n' $WEB_NGINX_MYSQL
#sed -i '/STOPSIGNAL SIGTERM/i ADD simkai.ttf /usr/share/zabbix/assets/fonts/\nADD nginx.sh /tmp/nginx.sh\n' $WEB_NGINX_MYSQL
# sed -i -e "/    sh \/tmp\/nginx.sh/d" $WEB_NGINX_MYSQL
# sed -i -e "/    microdnf -y clean all/d" $WEB_NGINX_MYSQL
# sed -i '/EXPOSE 8080/i\    microdnf -y clean all && \\\n    sh /tmp/nginx.sh\n' $WEB_NGINX_MYSQL
sed -i -e "/listen/d" ${WEB_NGINX_MYSQL_NGINX_CONF}
sed -i -e "/server {/a\ \tlisten 8080;\n\tlisten [::]:8080;\n\tlisten 8443 ssl;" ${WEB_NGINX_MYSQL_NGINX_CONF}
sed -i -e "/ssl_/d" ${WEB_NGINX_MYSQL_NGINX_CONF}
sed -i -e "/if /,+2d" ${WEB_NGINX_MYSQL_NGINX_CONF}
sed -i -e "/8443 ssl/a\ \tssl_certificate \"/etc/ssl/nginx/server.pem\";\n\
\tssl_certificate_key \"/etc/ssl/nginx/server.pem\";\n\
\tssl_session_cache shared:SSL:1m;\n\
\tssl_session_timeout  10m;\n\
\tssl_ciphers PROFILE=SYSTEM;\n\
\tssl_prefer_server_ciphers on;\n\
\tif (\$server_port = 8080) {\n\
\t\trewrite ^(\.\*)\$ https://\$host:8443\$1 permanent;\n\
\t}\
" ${WEB_NGINX_MYSQL_NGINX_CONF}

option=$(echo ${GV_VERSION} | cut -c 1)
case ${option} in
    5)
    echo "zabbix 5 LTSC!"
    sed -i '/.pki/ s/ \&\& \\//'  $WEB_NGINX_MYSQL
    sed -i '/.pki/ s/$/ \&\& \\/'  $WEB_NGINX_MYSQL
    sed -i "/ZBX_FONT_NAME/d" $WEB_NGINX_MYSQL
    sed -i '/.pki/a \    sed -i \"/ZBX_FONT_NAME/s/DejaVuSans/simkai/\" /usr/share/zabbix/include/defines.inc.php' $WEB_NGINX_MYSQL
    sed -i "/ZBX_GRAPH_FONT_NAME/d" Dockerfiles/web-nginx-mysql/centos/Dockerfile
    sed -i '/.pki/a \    sed -i \"/ZBX_GRAPH_FONT_NAME/s/DejaVuSans/simkai/\" /usr/share/zabbix/include/defines.inc.php && \\' $WEB_NGINX_MYSQL
    ;;
    6)
    echo "zabbix 6 LTSC!"
    sed -i '/.pki/ s/ \&\& \\//'  $WEB_NGINX_MYSQL
    sed -i '/.pki/ s/$/ \&\& \\/'  $WEB_NGINX_MYSQL
    sed -i "/ZBX_FONT_NAME/d" $WEB_NGINX_MYSQL
    sed -i '/.pki/a \    sed -i \"/ZBX_FONT_NAME/s/DejaVuSans/simkai/\" /usr/share/zabbix/include/defines.inc.php' $WEB_NGINX_MYSQL
    sed -i "/ZBX_GRAPH_FONT_NAME/d" Dockerfiles/web-nginx-mysql/centos/Dockerfile
    sed -i '/.pki/a \    sed -i \"/ZBX_GRAPH_FONT_NAME/s/DejaVuSans/simkai/\" /usr/share/zabbix/include/defines.inc.php && \\' $WEB_NGINX_MYSQL
    ;;
    *)
    echo "Nothing to do"
    ;;
esac
}

zabbix_agent2() {
update_config_var $ZABBIX_AGENT2 "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
sed -i '/allowerasing/d' $ZABBIX_AGENT2
sed -i -e "/^FROM quay/s/FROM .*/FROM ${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE]}/" $ZABBIX_AGENT2
sed -i -e "/libcurl-minimal/s/^/#/" $ZABBIX_AGENT2
update_config_var $ZABBIX_AGENT2_ENTRYPOINT "    update_config_var \$ZBX_AGENT_CONFIG \"Include\" \"/etc/zabbix/zabbix_agent2.d/plugins.d/*.conf\"" "#    update_config_var \$ZBX_AGENT_CONFIG \"Include\" \"/etc/zabbix/zabbix_agent2.d/plugins.d/*.conf\""
update_config_var $ZABBIX_AGENT2_ENTRYPOINT "    update_config_var \$ZBX_AGENT_CONFIG \"Include\" \"/etc/zabbix/zabbix_agentd.d/*.conf\" \"true\"" "#    update_config_var \$ZBX_AGENT_CONFIG \"Include\" \"/etc/zabbix/zabbix_agentd.d/*.conf\" \"true\""
}

zabbix_snmptraps() {
sed -i -e "/^FROM quay/s/FROM .*/FROM ${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE]}/" $ZABBIX_SNMPTRAPS
update_config_var $ZABBIX_SNMPTRAPS "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
}

zabbix_java_gateway() {
sed -i -e "/^FROM quay/s/FROM .*/FROM ${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE]}/" $ZABBIX_JAVA_GATEWAY
update_config_var $ZABBIX_JAVA_GATEWAY "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
}

zabbix_web_service() {
sed -i -e "/^FROM quay/s/FROM .*/FROM ${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE]}/" $ZABBIX_WEB_SERVICE
update_config_var $ZABBIX_WEB_SERVICE "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
}

escape_spec_char() {
    local var_value=$1

    var_value="${var_value//\\/\\\\}"
    var_value="${var_value//[$'\n']/}"
    var_value="${var_value//\//\\/}"
    var_value="${var_value//./\\.}"
    var_value="${var_value//\*/\\*}"
    var_value="${var_value//^/\\^}"
    var_value="${var_value//\$/\\\$}"
    var_value="${var_value//\&/\\\&}"
    var_value="${var_value//\[/\\[}"
    var_value="${var_value//\]/\\]}"

    echo "$var_value"
}

update_config_var() {
    local config_path=$1
    local var_name=$2
    local var_value=$3
    

    if [ ! -f "$config_path" ]; then
        echo "**** Configuration file '$config_path' does not exist"
        return
    fi

    # Remove configuration parameter definition in case of unset parameter value
    if [ -z "$var_value" ]; then
        sed -i -e "/^$var_name=/d" "$config_path"
        echo "removed"
        return
    fi

    # Remove value from configuration parameter in case of double quoted parameter value
    if [ "$var_value" == '""' ]; then
        sed -i -e "/^$var_name=/s/=.*/=/" "$config_path"
        echo "undefined"
        return
    fi

    # Escaping characters in parameter value and name
    var_value=$(escape_spec_char "$var_value")
    var_name=$(escape_spec_char "$var_name")
    
    if [ "$(grep -E "^$var_name =" $config_path)" ] && [ "$is_multiple" != "true" ]; then
        sed -i -e "/^$var_name =/s/=.*/= $var_value/" "$config_path"
        echo "updated $var_name = $var_value "
    fi
    
    if [ "$(grep -E "^$var_name" $config_path)" ] && [ "$is_multiple" != "true" ]; then
        sed -i -e "/^$var_name/s/$var_name/$var_value/" "$config_path"
        echo "updated $var_name -> $var_value "
    fi
}


#################################################
if [ $# -eq 0 ]; then
    help
    exit 1
elif [ $# -ge 1 ]; then
    if [[ $1 == "help" ]]; then
    #    echo "**** Configuration file '$config_path' does not exist"
        help
        exit 1
    fi
    
    if [[ "$1" == "update" ]]; then
        init
        zabbix_build_base
        zabbix_build_mysql
        zabbix_server_mysql
        zabbix_web_nginx_mysql
        zabbix_agent2
        zabbix_snmptraps
        zabbix_java_gateway
        zabbix_proxy_mysql
        option=$(echo ${GV_VERSION} | cut -c 1)
        case ${option} in
            5)
            echo "zabbix 5 LTSC!"
            ;;
            6)
            echo "zabbix 6 LTSC!"
            zabbix_web_service
            ;;
            *)
            echo "Nothing to do"
            ;;
        esac
        exit 1
    fi
    
    if [[ "$1" == "build1" ]]; then
        docker-compose -f docker-compose_v6_0_x_centos_mysql_local.yaml --profile=build1 build
        exit 1
    fi
    
    if [[ "$1" == "build2" ]]; then
        docker-compose -f docker-compose_v6_0_x_centos_mysql_local.yaml --profile=build2 build
        exit 1
    fi
    
    if [[ "$1" == "make" ]]; then
        option=$(echo ${GV_VERSION} | cut -c 1)
        case ${option} in
            5)
            echo "zabbix 5 LTSC!"
            docker-compose -f docker-compose_v6_0_x_centos_mysql_local.yaml --profile=make5 build
            ;;
            6)
            echo "zabbix 6 LTSC!"
            docker-compose -f docker-compose_v6_0_x_centos_mysql_local.yaml --profile=make6 build
            ;;
            *)
            echo "Nothing to do"
            ;;
        esac
        exit 1
    fi
    
    if [[ "$1" == "zabbix-web-nginx-mysql" ]]; then
        docker-compose -f docker-compose_v6_0_x_centos_mysql_local.yaml --profile=zabbix-web-nginx-mysql build
        exit 1
    fi
    
    if [[ "$1" == "cp" ]]; then
        option=$(echo ${GV_VERSION} | cut -c 1)
        case ${option} in
            5)
            echo "zabbix 5 LTSC!"
            docker-compose -f docker-compose_v6_0_x_centos_mysql_local.yaml --profile=start5 up -d
            ;;
            6)
            echo "zabbix 6 LTSC!"
            mkdir -p ./zbx_env/usr/share/zabbix/locale/zh_CN/LC_MESSAGES/
            \cp -rf ./patch/${GV_ARR_ENV[GV_WEB_UI_FILE_NAME]} ./zbx_env/usr/share/zabbix/locale/zh_CN/LC_MESSAGES/frontend.mo
#            mkdir -p ./zbx_env/etc/mysql/conf.d
            mkdir -p ./zbx_env/etc/mysql
            \cp -rf ./patch/my.cnf ./zbx_env/etc/mysql/my.cnf
            mkdir -p ./zbx_env/etc/ssl/nginx
            \cp -rf ./patch/server.pem ./zbx_env/etc/ssl/nginx/
            \cp ./patch/docker-compose-linux-x86_64 /usr/local/bin/docker-compose
            mkdir -p ./zbx_env/data/ssl
            \cp -rf ./patch/server.pem ./zbx_env/data/ssl/
            mkdir -p ./zbx_env/data/plugins
            tar -zxf ./patch/alexanderzobnin-zabbix-app-*.tar.gz -C ./zbx_env/data/plugins
            mkdir -p ./zbx_env/loki/config
            \cp -rf ./patch/loki-config.yaml ./zbx_env/loki/config
            mkdir -p ./zbx_env/promtail/config
            \cp -rf ./patch/promtail-config.yaml ./zbx_env/promtail/config
            mkdir -p /var/log/loki
            touch /var/log/loki/alert.log
            echo "test" > /var/log/loki/alert.log
            chmod 777 -R /var/log/loki
            \cp ./patch/loki.conf /etc/rsyslog.d/
            mkdir -p ./zbx_env/usr/lib/zabbix/alertscripts
            \cp ./patch/echo.sh ./zbx_env/usr/lib/zabbix/alertscripts/
            chmod 755 ./zbx_env/usr/lib/zabbix/alertscripts/echo.sh
            sed -i -e "/^\#module(load=\"imudp\")/s/^#//" /etc/rsyslog.conf
            sed -i -e "/^\#input(type=\"imudp\"/s/^#//" /etc/rsyslog.conf
            sed -i -e "/^\#module(load=\"imtcp\")/s/^#//" /etc/rsyslog.conf
            sed -i -e "/^\#input(type=\"imtcp\"/s/^#//" /etc/rsyslog.conf
            sed -i -e "/^\#\$ModLoad imudp/s/^#//" /etc/rsyslog.conf
            sed -i -e "/^\#\$UDPServerRun 514/s/^#//" /etc/rsyslog.conf
            sed -i -e "/^\#\$ModLoad imtcp/s/^#//" /etc/rsyslog.conf
            sed -i -e "/^\#\$InputTCPServerRun 514/s/^#//" /etc/rsyslog.conf
            sed -i -e "/^\module(load=\"builtin:omfile\"/s/^\(.*\)$/# \1/" /etc/rsyslog.conf
            systemctl restart rsyslog
            ;;
            *)
            echo "Nothing to do"
            ;;
        esac
        exit 1
    fi
    
    if [[ "$1" == "start" ]]; then
        option=$(echo ${GV_VERSION} | cut -c 1)
        case ${option} in
            5)
            echo "zabbix 5 LTSC!"
            docker-compose -f docker-compose_v6_0_x_centos_mysql_local.yaml --profile=start5 up -d
            ;;
            6)
            echo "zabbix 6 LTSC!"
            docker-compose -f docker-compose_v6_0_x_centos_mysql_local.yaml --profile=start6 up -d
            ;;
            *)
            echo "Nothing to do"
            ;;
        esac
        exit 1
    fi

    if [[ "$1" == "prxstart" ]]; then
        option=$(echo ${GV_VERSION} | cut -c 1)
        case ${option} in
            5)
            echo "zabbix 5 LTSC!"
            docker-compose -f docker-compose_v6_0_x_centos_mysql_local.yaml --profile=prxstart5 up -d
            ;;
            6)
            echo "zabbix 6 LTSC!"
            docker-compose -f docker-compose_v6_0_x_centos_mysql_local.yaml --profile=prxstart6 up -d
            ;;
            *)
            echo "Nothing to do"
            ;;
        esac
        exit 1
    fi
    
    if [[ "$1" == "stop" ]]; then
        docker-compose -f docker-compose_v6_0_x_centos_mysql_local.yaml stop
        exit 1
    fi
    
    if [[ "$1" == "restart" ]]; then
        docker-compose -f docker-compose_v6_0_x_centos_mysql_local.yaml restart
        exit 1
    fi
    
    if [[ "$1" == "rm" ]]; then
        docker-compose -f docker-compose_v6_0_x_centos_mysql_local.yaml rm
        exit 1
    fi
	
    if [[ "$1" == "base" ]]; then
        docker build -t ${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE]} ./patch/Dockerfile_rockylinux
        docker save -o rockylinux9.tar.gz ${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE]}
        docker rmi $(docker images |grep rockylinux | awk -F ' ' '{print $3}')
        docker load < rockylinux9.tar.gz
        rm -f rockylinux9.tar.gz
        exit 1
    fi
    
    if [[ "$1" == "buildmariadb" ]]; then
        docker build -t mariadb:${GV_ARR_ENV[GV_MARIADB_VERSION]} ./patch/Dockerfile_mariadb
        docker save -o mariadb.tar.gz mariadb:${GV_ARR_ENV[GV_MARIADB_VERSION]}
        docker rmi $(docker images |grep mariadb | awk -F ' ' '{print $3}')
        docker load < mariadb.tar.gz
        rm -f mariadb.tar.gz
        exit 1
    fi
fi

#################################################
