#!/bin/bash
###
### hello to use the shell
###
### Usage:
###
###    sh update_config-entrypoint.sh [start|stop|restart|rm]
###
###
### Options:
###   help        Show this message.
###   init down cp start

# 设置了这个选项以后，包含管道命令的语句的返回值，会变成最后一个返回非零的管道命令的返回值。
set -o pipefail

# 执行的时候如果出现了返回值为非零将会继续执行下面的脚本
set +e

# Script trace mode
set -o xtrace

GV_VERSION=$(cat ./patch/.version)
GV_VERSION_DOCKER=$(cat ./patch/.version_docker)

help() {
	awk -F'### ' '/^###/ { print $2 }' "$0"
}

init() {
sed -i -e "/:centos-/s/:centos-.*/:centos-${GV_VERSION_DOCKER}/" docker-compose_v6_0_x_centos_mysql_local.yaml
chmod 755 -R ./
option=$(cat /etc/redhat-release | cut -c 22)
if [[ " " == "${option}" ]]; then
	option=$(cat /etc/redhat-release | cut -c 23)
fi
case ${option} in
    8)
    echo "Centos 8 catch!"
    if [ ! -d "/etc/yum.repos.d/bak/" ]; then
        yum install -y yum-utils \
            device-mapper-persistent-data \
            lvm2 --allowerasing
        yum-config-manager \
            --add-repo \
            https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
        yum -y install docker-ce docker-ce-cli containerd.io --allowerasing
        if [ $? -ne '0' ]; then
         rpm -qa | grep docker | xargs rpm -e --nodeps
         echo "YUM配置异常请重新执行，如继续报错请联系作者QQ1284524409"
         echo "YUM配置异常请联系作者QQ1284524409"
         exit 1
        fi
        yum -y install git rsyslog --allowerasing
    fi
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
        if [ $? -ne '0' ]; then
         rpm -qa | grep docker | xargs rpm -e --nodeps
         echo "YUM配置异常请重新执行，如继续报错请联系作者QQ1284524409"
         exit 1
        fi
        yum -y install git rsyslog
    ;;
    *)
    echo "Nothing to do"
    ;;
esac
if [ $? -ne '0' ]; then
 echo "YUM配置异常请联系作者QQ1284524409"
 exit 1
fi
service docker start
touch /etc/docker/daemon.json
cat > /etc/docker/daemon.json << EOF
{
  "registry-mirrors": ["https://xb10bnbv.mirror.aliyuncs.com"]
}
EOF
service docker restart
chmod 777 /var/run/docker.sock
if [ ! -f "/usr/local/bin/docker-compose" ]; then
    # curl -SL https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    \cp ./patch/docker-compose-linux-x86_64 /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi
systemctl enable docker
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

    if [[ "$1" == "cp" ]]; then
        option=$(echo ${GV_VERSION} | cut -c 1)
        case ${option} in
            5)
            echo "zabbix 5 LTSC!"
            ;;
            6)
            echo "zabbix 6 LTSC!"
            mkdir -p ./zbx_env/usr/share/zabbix/locale/zh_CN/LC_MESSAGES/
            \cp -rf ./patch/frontend_6.0.mo ./zbx_env/usr/share/zabbix/locale/zh_CN/LC_MESSAGES/frontend.mo
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
            chmod -R 777 /var/log/loki
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
            \cp ./patch/loki /etc/logrotate.d/loki
            # /usr/sbin/logrotate -f /etc/logrotate.d/loki
            ;;
            *)
            echo "Nothing to do"
            ;;
        esac
        exit 1
    fi

    if [[ "$1" == "start" ]]; then
        option=$(echo ${GV_VERSION_DOCKER} | cut -c 1)
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

    if [[ "$1" == "down" ]]; then
        sh ./patch/down_mysql.sh
        exit 1
    fi

    if [[ "$1" == "prxdown" ]]; then
        sh ./patch/down_mysql_proxy.sh
        exit 1
    fi

    if [[ "$1" == "init" ]]; then
        init
        exit 1
    fi
fi

#################################################
