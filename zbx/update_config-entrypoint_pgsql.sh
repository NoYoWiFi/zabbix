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

GV_VERSION=$(cat ./patch/.version)
GV_VERSION_DOCKER=$(cat ./patch/.version_docker)
BUILD_CONFIG="./build.sh"
ZABBIX_BUILD_BASE="./Dockerfiles/build-base/centos/Dockerfile"
ZABBIX_BUILD_PGSQL="./Dockerfiles/build-pgsql/centos/Dockerfile"
ZABBIX_SERVER_PGSQL="./Dockerfiles/server-pgsql/centos/Dockerfile"
ZABBIX_PROXY_PGSQL="./Dockerfiles/proxy-pgsql/centos/Dockerfile"
ZABBIX_PROXY_PGSQL_ENTRYPOINT="./Dockerfiles/proxy-pgsql/centos/docker-entrypoint.sh"
ZABBIX_SERVER_PGSQL_ENTRYPOINT="./Dockerfiles/server-pgsql/centos/docker-entrypoint.sh"
WEB_NGINX_PGSQL="./Dockerfiles/web-nginx-pgsql/centos/Dockerfile"
WEB_NGINX_ENTRYPOINT="./Dockerfiles/web-nginx-pgsql/centos/docker-entrypoint.sh"
ZABBIX_AGENT2="./Dockerfiles/agent2/centos/Dockerfile"
ZABBIX_AGENT2_ENTRYPOINT="./Dockerfiles/agent2/centos/docker-entrypoint.sh"
ZABBIX_SNMPTRAPS="./Dockerfiles/snmptraps/centos/Dockerfile"
ZABBIX_JAVA_GATEWAY="./Dockerfiles/java-gateway/centos/Dockerfile"
ZABBIX_WEB_SERVICE="./Dockerfiles/web-service/centos/Dockerfile"

help() {
    awk -F'### ' '/^###/ { print $2 }' "$0"
}

init() {
sed -i -e "/:centos-/s/:centos-.*/:centos-${GV_VERSION_DOCKER}/" docker-compose_v6_0_x_centos_pgsql_local.yaml
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
        tar -zxvf ./patch/repos.tar.gz -C /etc/yum.repos.d/
    fi
    yum install -y yum-utils \
        device-mapper-persistent-data \
        lvm2
    yum-config-manager \
        --add-repo \
        https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
    yum -y install docker-ce docker-ce-cli containerd.io --allowerasing
    yum -y install git
    \cp ./trans/create_server_${GV_VERSION_DOCKER}_pgsql.sql.gz ./patch/create_server.sql.gz
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
        yum -y install git
        \cp ./trans/create_server_${GV_VERSION_DOCKER}_pgsql.sql.gz ./patch/create_server.sql.gz
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
service docker restart
chmod 777 /var/run/docker.sock
update_config_var $ZABBIX_BUILD_BASE "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
if [ ! -f "/usr/local/bin/docker-compose" ]; then
    # curl -SL https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    \cp ./patch/docker-compose-linux-x86_64 /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi
}

zabbix_build_base() {
sed -i -e "/^FROM quay/s/FROM .*/FROM rockylinux:8/" $ZABBIX_BUILD_BASE
update_config_var $ZABBIX_BUILD_BASE "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
if [ ! -f "./Dockerfiles/build-base/centos/go1.19.13.linux-amd64.tar.gz" ]; then
    \cp ./patch/go1.19.13.linux-amd64.tar.gz ./Dockerfiles/build-base/centos/
fi
if [ ! -f "./Dockerfiles/build-base/centos/repos.tar.gz" ]; then
    \cp ./patch/repos.tar.gz ./Dockerfiles/build-base/centos/
fi
sed -i -e "/^ADD/,+2d" "$ZABBIX_BUILD_BASE"
sed -i '/RUN/i ADD go1.19.13.linux-amd64.tar.gz /usr/local/\nADD repos.tar.gz /etc/yum.repos.d/\n' $ZABBIX_BUILD_BASE
sed -i -e "/^    case/,+24d" "$ZABBIX_BUILD_BASE"
}

zabbix_build_pgsql() {
sed -i -e "/^FROM quay/s/FROM .*/FROM rockylinux:8/" $ZABBIX_BUILD_PGSQL
update_config_var $ZABBIX_BUILD_PGSQL "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
sed -i -e "/^ADD/,+1d" "$ZABBIX_BUILD_PGSQL"
\cp ./patch/zabbix-${GV_VERSION}.tar.gz ./Dockerfiles/build-pgsql/centos/
\cp ./patch/mongodb_plugin.tar.gz ./Dockerfiles/build-pgsql/centos/
\cp ./patch/postgresql_plugin.tar.gz ./Dockerfiles/build-pgsql/centos/
#    \cp ./patch/create_server.sql.gz ./Dockerfiles/build-pgsql/centos/
\cp ./patch/create_server.sql.gz ./Dockerfiles/build-pgsql/centos/
\cp ./patch/NotoSansCJKjp-hinted.zip ./Dockerfiles/build-pgsql/centos/
sed -i -e "/^    go/d" "$ZABBIX_BUILD_PGSQL"
sed -i -e "/^ADD/,+1d" "$ZABBIX_BUILD_PGSQL"
sed -i -e "/^COPY create_server.sql.gz/d" "$ZABBIX_BUILD_PGSQL"
sed -i -e "/^    git -c/d" "$ZABBIX_BUILD_PGSQL"
sed -i "/RUN/i ADD zabbix-${GV_VERSION}.tar.gz /tmp/\nADD mongodb_plugin.tar.gz /tmp/\nADD postgresql_plugin.tar.gz /tmp/\n" $ZABBIX_BUILD_PGSQL
#sed -i '/RUN/i COPY create_server.sql.gz /tmp/\n' $ZABBIX_BUILD_PGSQL
sed -i '/RUN/i COPY create_server.sql.gz /tmp/\n' $ZABBIX_BUILD_PGSQL
sed -i '/    cp \/tmp\/create_server.sql.gz/d' $ZABBIX_BUILD_PGSQL
sed -i -e "/^ADD NotoSansCJKjp-hinted.zip/,+1d" "$ZABBIX_BUILD_PGSQL"
sed -i -e "/mkdir \/tmp\/fonts\//d" "$ZABBIX_BUILD_PGSQL"
sed -i '/RUN/i ADD NotoSansCJKjp-hinted.zip /tmp/fonts/\n' $ZABBIX_BUILD_PGSQL
#sed -i '/    strip \/tmp\/zabbix-\${ZBX_VERSION}\/src\/zabbix_agent\/zabbix_agentd \&\& \\/i\    cp /tmp/create_server.sql.gz database/postgresql/create_server.sql.gz && \\' $ZABBIX_BUILD_PGSQL
sed -i '/    strip \/tmp\/zabbix-\${ZBX_VERSION}\/src\/zabbix_agent\/zabbix_agentd \&\& \\/i\    cp /tmp/create_server.sql.gz database/postgresql/create_server.sql.gz && \\' $ZABBIX_BUILD_PGSQL
sed -i '/.\/configure \\/i\    go env -w GOPROXY=https://goproxy.cn && \\' $ZABBIX_BUILD_PGSQL
sed -i -e "/curl --silent/d" $ZABBIX_BUILD_PGSQL
}

zabbix_server_pgsql() {
if [ ! -f "./Dockerfiles/server-pgsql/centos/repos.tar.gz" ]; then
    \cp ./patch/repos.tar.gz ./Dockerfiles/server-pgsql/centos/
fi
if [ ! -f "./Dockerfiles/server-pgsql/centos/pip.sh" ]; then
    \cp ./patch/pip.sh ./Dockerfiles/server-pgsql/centos/
fi
if [ ! -f "./Dockerfiles/server-pgsql/centos/tcping-1.3.5-19.el8.x86_64.rpm" ]; then
    \cp ./patch/tcping-1.3.5-19.el8.x86_64.rpm ./Dockerfiles/server-pgsql/centos/
fi
\cp ./patch/timescaledb.sql ./Dockerfiles/server-pgsql/centos/
sed -i -e "/^FROM quay/s/FROM .*/FROM rockylinux:8/" $ZABBIX_SERVER_PGSQL
update_config_var $ZABBIX_SERVER_PGSQL "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
update_config_var $ZABBIX_SERVER_PGSQL "    rm -rf /var/cache/dnf /etc/udev/hwdb.bin /root/.pki" "    rm -rf /var/cache/dnf /etc/udev/hwdb.bin /root/.pki && \\"
sed -i -e "/^ADD/,+4d" "$ZABBIX_SERVER_PGSQL"
#3ADD
sed -i '/RUN set -eux /i ADD tcping-1.3.5-19.el8.x86_64.rpm /tmp/tcping-1.3.5-19.el8.x86_64.rpm\nADD pip.sh /tmp/pip.sh\nADD repos.tar.gz /etc/yum.repos.d/\nADD timescaledb.sql /usr/share/doc/zabbix-server-postgresql/timescaledb.sql\n' $ZABBIX_SERVER_PGSQL
#4ADD
#sed -i '/STOPSIGNAL SIGTERM/i ADD tcping-1.3.5-19.el8.x86_64.rpm /tmp/tcping-1.3.5-19.el8.x86_64.rpm\nADD pip.sh /tmp/pip.sh\nADD repos.tar.gz /etc/yum.repos.d/\nADD zbx_db_partitiong.sql /tmp/\n' $ZABBIX_SERVER_PGSQL
sed -i -e "/    rm -rf \/var\/cache\/dnf/d" "$ZABBIX_SERVER_PGSQL"
sed -i -e "/    sh \/tmp\/pip.sh/,+1d" "$ZABBIX_SERVER_PGSQL"
sed -i '/EXPOSE 10051/i\    rm -rf /var/cache/dnf /etc/udev/hwdb.bin /root/.pki && \\\n    sh /tmp/pip.sh\n' $ZABBIX_SERVER_PGSQL
}

zabbix_proxy_pgsql() {
\cp -vrf ./Dockerfiles/server-pgsql ./Dockerfiles/proxy-pgsql
if [ ! -f "./Dockerfiles/proxy-pgsql/centos/repos.tar.gz" ]; then
    \cp ./patch/repos.tar.gz ./Dockerfiles/proxy-pgsql/centos/
fi
if [ ! -f "./Dockerfiles/proxy-pgsql/centos/pip.sh" ]; then
    \cp ./patch/pip.sh ./Dockerfiles/proxy-pgsql/centos/
fi
if [ ! -f "./Dockerfiles/proxy-pgsql/centos/tcping-1.3.5-19.el8.x86_64.rpm" ]; then
    \cp ./patch/tcping-1.3.5-19.el8.x86_64.rpm ./Dockerfiles/proxy-pgsql/centos/
fi
\cp ./patch/timescaledb.sql ./Dockerfiles/proxy-pgsql/centos/
sed -i -e 's|Zabbix server|Zabbix proxy|g' $ZABBIX_PROXY_PGSQL
sed -i -e 's|zabbix_server|zabbix_proxy|g' $ZABBIX_PROXY_PGSQL
sed -i -e 's|create_server.sql.gz|create_proxy.sql.gz|g' $ZABBIX_PROXY_PGSQL
sed -i -e 's|zabbix-server-postgresql|zabbix-proxy-postgresql|g' $ZABBIX_PROXY_PGSQL
sed -i -e 's|, "/var/lib/zabbix/export"||g' $ZABBIX_PROXY_PGSQL
sed -i -e "/^FROM quay/s/FROM .*/FROM rockylinux:8/" $ZABBIX_PROXY_PGSQL

sed -i -e 's|zabbix-server-postgresql|zabbix-proxy-postgresql|g' $ZABBIX_PROXY_PGSQL_ENTRYPOINT
sed -i -e 's|Zabbix server|Zabbix proxy|g' $ZABBIX_PROXY_PGSQL_ENTRYPOINT
sed -i -e 's|zabbix_server|zabbix_proxy|g' $ZABBIX_PROXY_PGSQL_ENTRYPOINT

sed -i '368i\ ' $ZABBIX_PROXY_PGSQL_ENTRYPOINT
sed -i '368i\    fi' $ZABBIX_PROXY_PGSQL_ENTRYPOINT
sed -i '368i\        update_config_var $ZBX_CONFIG "HostnameItem" "${ZBX_HOSTNAMEITEM}"' $ZABBIX_PROXY_PGSQL_ENTRYPOINT
sed -i '368i\        update_config_var $ZBX_CONFIG "Hostname" "${ZBX_HOSTNAME:-"zabbix-proxy-pgsql"}"' $ZABBIX_PROXY_PGSQL_ENTRYPOINT
sed -i '368i\    else' $ZABBIX_PROXY_PGSQL_ENTRYPOINT
sed -i '368i\        update_config_var $ZBX_CONFIG "HostnameItem" "${ZBX_HOSTNAMEITEM}"' $ZABBIX_PROXY_PGSQL_ENTRYPOINT
sed -i '368i\        update_config_var $ZBX_CONFIG "Hostname" ""' $ZABBIX_PROXY_PGSQL_ENTRYPOINT
sed -i '368i\    if [ -z "${ZBX_HOSTNAME}" ] && [ -n "${ZBX_HOSTNAMEITEM}" ]; then' $ZABBIX_PROXY_PGSQL_ENTRYPOINT
sed -i '368i\    update_config_var $ZBX_CONFIG "Server" "${ZBX_SERVER_HOST}"' $ZABBIX_PROXY_PGSQL_ENTRYPOINT
sed -i '368i\    update_config_var $ZBX_CONFIG "ProxyMode" "${ZBX_PROXYMODE}"' $ZABBIX_PROXY_PGSQL_ENTRYPOINT

sed -i '418i\ ' $ZABBIX_PROXY_PGSQL_ENTRYPOINT
sed -i '418i\    update_config_var $ZBX_CONFIG "DataSenderFrequency" "${ZBX_DATASENDERFREQUENCY}"' $ZABBIX_PROXY_PGSQL_ENTRYPOINT
sed -i '418i\    update_config_var $ZBX_CONFIG "ProxyConfigFrequency" "${ZBX_PROXYCONFIGFREQUENCY}"' $ZABBIX_PROXY_PGSQL_ENTRYPOINT
sed -i '418i\    update_config_var $ZBX_CONFIG "ProxyOfflineBuffer" "${ZBX_PROXYOFFLINEBUFFER}"' $ZABBIX_PROXY_PGSQL_ENTRYPOINT
sed -i '418i\    update_config_var $ZBX_CONFIG "ProxyLocalBuffer" "${ZBX_PROXYLOCALBUFFER}"' $ZABBIX_PROXY_PGSQL_ENTRYPOINT

sed -i -e 's|prepare_server|prepare_proxy|g' $ZABBIX_PROXY_PGSQL_ENTRYPOINT


update_config_var $ZABBIX_PROXY_PGSQL "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
update_config_var $ZABBIX_PROXY_PGSQL "    rm -rf /var/cache/dnf /etc/udev/hwdb.bin /root/.pki" "    rm -rf /var/cache/dnf /etc/udev/hwdb.bin /root/.pki && \\"
sed -i -e "/^ADD/,+4d" "$ZABBIX_PROXY_PGSQL"
#3ADD
sed -i '/RUN set -eux /i ADD tcping-1.3.5-19.el8.x86_64.rpm /tmp/tcping-1.3.5-19.el8.x86_64.rpm\nADD pip.sh /tmp/pip.sh\nADD repos.tar.gz /etc/yum.repos.d/\nADD timescaledb.sql /usr/share/doc/zabbix-proxy-postgresql/timescaledb.sql\n' $ZABBIX_PROXY_PGSQL
#4ADD
#sed -i '/STOPSIGNAL SIGTERM/i ADD tcping-1.3.5-19.el8.x86_64.rpm /tmp/tcping-1.3.5-19.el8.x86_64.rpm\nADD pip.sh /tmp/pip.sh\nADD repos.tar.gz /etc/yum.repos.d/\nADD zbx_db_partitiong.sql /tmp/\n' $ZABBIX_PROXY_PGSQL
sed -i -e "/    rm -rf \/var\/cache\/dnf/d" "$ZABBIX_PROXY_PGSQL"
sed -i -e "/    sh \/tmp\/pip.sh/,+1d" "$ZABBIX_PROXY_PGSQL"
sed -i '/EXPOSE 10051/i\    rm -rf /var/cache/dnf /etc/udev/hwdb.bin /root/.pki && \\\n    sh /tmp/pip.sh\n' $ZABBIX_PROXY_PGSQL
}

zabbix_web_nginx_pgsql() {
if [ ! -f "./Dockerfiles/web-nginx-pgsql/centos/simkai.ttf" ]; then
    \cp ./patch/simkai.ttf ./Dockerfiles/web-nginx-pgsql/centos/
fi
if [ ! -f "./Dockerfiles/web-nginx-pgsql/centos/frontend_6.0.mo" ]; then
    \cp ./patch/frontend_6.0.mo ./Dockerfiles/web-nginx-pgsql/centos/
fi
if [ ! -f "./Dockerfiles/web-nginx-pgsql/centos/repos.tar.gz" ]; then
    \cp ./patch/repos.tar.gz ./Dockerfiles/web-nginx-pgsql/centos/
fi
if [ ! -f "./Dockerfiles/web-nginx-pgsql/centos/nginx.sh" ]; then
    \cp ./patch/nginx.sh ./Dockerfiles/web-nginx-pgsql/centos/
fi
sed -i -e "/^FROM quay/s/FROM .*/FROM rockylinux:8/" $WEB_NGINX_PGSQL
update_config_var $WEB_NGINX_PGSQL "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
sed -i -e "/^ADD/,+3d" "$WEB_NGINX_PGSQL"
sed -i '/STOPSIGNAL SIGTERM/i ADD repos.tar.gz /etc/yum.repos.d/\nADD simkai.ttf /usr/share/zabbix/assets/fonts/\nADD nginx.sh /tmp/nginx.sh\n' $WEB_NGINX_PGSQL
sed -i -e "/sh \/tmp\/nginx.sh/d" "$WEB_NGINX_ENTRYPOINT"
sed -i '/prepare_zbx_web_config$/a \sh /tmp/nginx.sh\' $WEB_NGINX_ENTRYPOINT
option=$(echo ${GV_VERSION} | cut -c 1)
case ${option} in
    5)
    echo "zabbix 5 LTSC!"
    sed -i '/.pki/ s/ \&\& \\//'  $WEB_NGINX_PGSQL
    sed -i '/.pki/ s/$/ \&\& \\/'  $WEB_NGINX_PGSQL
    sed -i "/ZBX_FONT_NAME/d" $WEB_NGINX_PGSQL
    sed -i '/.pki/a \    sed -i \"/ZBX_FONT_NAME/s/DejaVuSans/simkai/\" /usr/share/zabbix/include/defines.inc.php' $WEB_NGINX_PGSQL
    sed -i "/ZBX_GRAPH_FONT_NAME/d" Dockerfiles/web-nginx-pgsql/centos/Dockerfile
    sed -i '/.pki/a \    sed -i \"/ZBX_GRAPH_FONT_NAME/s/DejaVuSans/simkai/\" /usr/share/zabbix/include/defines.inc.php && \\' $WEB_NGINX_PGSQL
    ;;
    6)
    echo "zabbix 6 LTSC!"
    sed -i '/.pki/ s/ \&\& \\//'  $WEB_NGINX_PGSQL
    sed -i '/.pki/ s/$/ \&\& \\/'  $WEB_NGINX_PGSQL
    sed -i "/ZBX_FONT_NAME/d" $WEB_NGINX_PGSQL
    sed -i '/.pki/a \    sed -i \"/ZBX_FONT_NAME/s/DejaVuSans/simkai/\" /usr/share/zabbix/include/defines.inc.php' $WEB_NGINX_PGSQL
    sed -i "/ZBX_GRAPH_FONT_NAME/d" Dockerfiles/web-nginx-pgsql/centos/Dockerfile
    sed -i '/.pki/a \    sed -i \"/ZBX_GRAPH_FONT_NAME/s/DejaVuSans/simkai/\" /usr/share/zabbix/include/defines.inc.php && \\' $WEB_NGINX_PGSQL
    ;;
    *)
    echo "Nothing to do"
    ;;
esac
}

zabbix_agent2() {
if [ ! -f "./Dockerfiles/agent2/centos/repos.tar.gz" ]; then
    \cp ./patch/repos.tar.gz ./Dockerfiles/agent2/centos/
fi
update_config_var $ZABBIX_AGENT2 "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
sed -i -e "/^ADD/,+1d" "$ZABBIX_AGENT2"
sed -i '/allowerasing/d' $ZABBIX_AGENT2
sed -i '/best/a\        --allowerasing \\' $ZABBIX_AGENT2
sed -i -e "/^FROM quay/s/FROM .*/FROM rockylinux:8/" $ZABBIX_AGENT2
sed -i '/STOPSIGNAL SIGTERM/i ADD repos.tar.gz /etc/yum.repos.d/\n' $ZABBIX_AGENT2
update_config_var $ZABBIX_AGENT2_ENTRYPOINT "    update_config_var \$ZBX_AGENT_CONFIG \"Include\" \"/etc/zabbix/zabbix_agent2.d/plugins.d/*.conf\"" "#    update_config_var \$ZBX_AGENT_CONFIG \"Include\" \"/etc/zabbix/zabbix_agent2.d/plugins.d/*.conf\""
update_config_var $ZABBIX_AGENT2_ENTRYPOINT "    update_config_var \$ZBX_AGENT_CONFIG \"Include\" \"/etc/zabbix/zabbix_agentd.d/*.conf\" \"true\"" "#    update_config_var \$ZBX_AGENT_CONFIG \"Include\" \"/etc/zabbix/zabbix_agentd.d/*.conf\" \"true\""
}

zabbix_snmptraps() {
if [ ! -f "./Dockerfiles/snmptraps/centos/repos.tar.gz" ]; then
    \cp ./patch/repos.tar.gz ./Dockerfiles/snmptraps/centos/
fi
sed -i -e "/^FROM quay/s/FROM .*/FROM rockylinux:8/" $ZABBIX_SNMPTRAPS
update_config_var $ZABBIX_SNMPTRAPS "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
sed -i -e "/^ADD/,+1d" "$ZABBIX_SNMPTRAPS"
sed -i '/STOPSIGNAL SIGTERM/i ADD repos.tar.gz /etc/yum.repos.d/\n' $ZABBIX_SNMPTRAPS
}

zabbix_java_gateway() {
if [ ! -f "./Dockerfiles/java-gateway/centos/repos.tar.gz" ]; then
    \cp ./patch/repos.tar.gz ./Dockerfiles/java-gateway/centos/
fi
sed -i -e "/^FROM quay/s/FROM .*/FROM rockylinux:8/" $ZABBIX_JAVA_GATEWAY
update_config_var $ZABBIX_JAVA_GATEWAY "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
sed -i -e "/^ADD/,+1d" "$ZABBIX_JAVA_GATEWAY"
sed -i '/STOPSIGNAL SIGTERM/i ADD repos.tar.gz /etc/yum.repos.d/\n' $ZABBIX_JAVA_GATEWAY
}

zabbix_web_service() {
if [ ! -f "./Dockerfiles/web-service/centos/repos.tar.gz" ]; then
    \cp ./patch/repos.tar.gz ./Dockerfiles/web-service/centos/
fi
sed -i -e "/^FROM quay/s/FROM .*/FROM rockylinux:8/" $ZABBIX_WEB_SERVICE
update_config_var $ZABBIX_WEB_SERVICE "# syntax=docker/dockerfile:1" "## syntax=docker/dockerfile:1"
sed -i -e "/^ADD/,+1d" "$ZABBIX_WEB_SERVICE"
sed -i '/STOPSIGNAL SIGTERM/i ADD repos.tar.gz /etc/yum.repos.d/\n' $ZABBIX_WEB_SERVICE
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
        zabbix_build_pgsql
        zabbix_server_pgsql
        zabbix_proxy_pgsql
        zabbix_web_nginx_pgsql
        zabbix_agent2
        zabbix_snmptraps
        zabbix_java_gateway
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
        docker-compose -f docker-compose_v6_0_x_centos_pgsql_local.yaml --profile=build1 build
        exit 1
    fi
    
    if [[ "$1" == "build2" ]]; then
        docker-compose -f docker-compose_v6_0_x_centos_pgsql_local.yaml --profile=build2 build
        exit 1
    fi
    
    if [[ "$1" == "make" ]]; then
        option=$(echo ${GV_VERSION} | cut -c 1)
        case ${option} in
            5)
            echo "zabbix 5 LTSC!"
            docker-compose -f docker-compose_v6_0_x_centos_pgsql_local.yaml --profile=make5 build
            ;;
            6)
            echo "zabbix 6 LTSC!"
            docker-compose -f docker-compose_v6_0_x_centos_pgsql_local.yaml --profile=make6 build
            ;;
            *)
            echo "Nothing to do"
            ;;
        esac
        exit 1
    fi
    
    if [[ "$1" == "zabbix-web-nginx-pgsql" ]]; then
        docker-compose -f docker-compose_v6_0_x_centos_pgsql_local.yaml --profile=zabbix-web-nginx-pgsql build
        exit 1
    fi
    
    if [[ "$1" == "cp" ]]; then
        option=$(echo ${GV_VERSION} | cut -c 1)
        case ${option} in
            5)
            echo "zabbix 5 LTSC!"
            docker-compose -f docker-compose_v6_0_x_centos_pgsql_local.yaml --profile=start5 up -d
            ;;
            6)
            echo "zabbix 6 LTSC!"
            mkdir -p ./zbx_env/var/lib/postgresql/data
            chown -R 1000:1000 ./zbx_env/var/lib/postgresql/data
            mkdir -p ./zbx_env/usr/share/zabbix/locale/zh_CN/LC_MESSAGES/
            \cp -rf ./patch/frontend_6.0.mo ./zbx_env/usr/share/zabbix/locale/zh_CN/LC_MESSAGES/frontend.mo
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

            sed -i -e "/^\      __path__:/s/:.*/: \/var\/log\/loki\/\*log/" /etc/promtail/config.yml
            \cp ./patch/loki.conf /etc/rsyslog.d/
            mkdir -p ./zbx_env/usr/lib/zabbix/alertscripts
            \cp ./patch/echo.sh ./zbx_env/usr/lib/zabbix/alertscripts/
            chmod 755 ./zbx_env/usr/lib/zabbix/alertscripts/echo.sh
            sed -i -e "/^\#module(load=\"imudp\")/s/^#//" /etc/rsyslog.conf
            sed -i -e "/^\#input(type=\"imudp\"/s/^#//" /etc/rsyslog.conf
            sed -i -e "/^\#module(load=\"imtcp\")/s/^#//" /etc/rsyslog.conf
            sed -i -e "/^\#input(type=\"imtcp\"/s/^#//" /etc/rsyslog.conf
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
            docker-compose -f docker-compose_v6_0_x_centos_pgsql_local.yaml --profile=start5 up -d
            ;;
            6)
            echo "zabbix 6 LTSC!"
            docker-compose -f docker-compose_v6_0_x_centos_pgsql_local.yaml --profile=start6 up -d
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
            docker-compose -f docker-compose_v6_0_x_centos_pgsql_local.yaml --profile=prxstart5 up -d
            ;;
            6)
            echo "zabbix 6 LTSC!"
            docker-compose -f docker-compose_v6_0_x_centos_pgsql_local.yaml --profile=prxstart6 up -d
            ;;
            *)
            echo "Nothing to do"
            ;;
        esac
        exit 1
    fi

    if [[ "$1" == "stop" ]]; then
        docker-compose -f docker-compose_v6_0_x_centos_pgsql_local.yaml stop
        exit 1
    fi
    
    if [[ "$1" == "restart" ]]; then
        docker-compose -f docker-compose_v6_0_x_centos_pgsql_local.yaml restart
        exit 1
    fi
    
    if [[ "$1" == "rm" ]]; then
        docker-compose -f docker-compose_v6_0_x_centos_pgsql_local.yaml rm
        exit 1
    fi
	
    if [[ "$1" == "base" ]]; then
        docker build -t rockylinux:8 ./patch/Dockerfile_rockylinux
        docker save -o rockylinux8.tar.gz rockylinux:8
        docker rmi $(docker images |grep rockylinux | awk -F ' ' '{print $3}')
        docker load < rockylinux8.tar.gz
        rm -f rockylinux8.tar.gz
        exit 1
    fi
    
    if [[ "$1" == "buildpgsql" ]]; then
        docker build -t timescale/timescaledb:2.13.0-pg15 ./patch/Dockerfile_timescale
        docker save -o timescale.tar.gz timescale/timescaledb:2.13.0-pg15
        docker rmi $(docker images |grep timescale | awk -F ' ' '{print $3}')
        docker load < timescale.tar.gz
        rm -f timescale.tar.gz
        exit 1
    fi
fi

#################################################
