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

GV_ENV_SHELL="./patch/.env_shell"
source ./patch/getEnv.sh
GV_VERSION=${GV_ARR_ENV[GV_ZABBIX_VERSION]}
GV_VERSION_DOCKER=${GV_ARR_ENV[GV_ZABBIX_POSTFIX]}


# 初始化option变量
option=""

# 首先尝试从os-release获取信息
if [ -f /etc/os-release ]; then
    . /etc/os-release
    
    case "$ID" in
        centos|rhel|rocky|almalinux)
            # RHEL系列，获取主版本号
            option=$(echo "$VERSION_ID" | cut -d. -f1)
            ;;
        ubuntu|debian)
            # Debian/Ubuntu系列
            option=$(echo "$VERSION_ID" | cut -d. -f1)
            ;;
        fedora)
            option="$VERSION_ID"
            ;;
        *)
            # 其他发行版，尝试提取数字
            option=$(echo "$VERSION_ID" | grep -oE '^[0-9]+')
            ;;
    esac
fi

help() {
	awk -F'### ' '/^###/ { print $2 }' "$0"
}

init() {
sed -i -e "/:centos-/s/:centos-.*/:centos-${GV_VERSION_DOCKER}/" docker-compose_v6_0_x_centos_mysql_local.yaml
chmod 755 -R ./
#!/bin/bash

# 如果os-release没获取到，尝试其他方法
if [ -z "$option" ]; then
    # 尝试redhat-release
    if [ -f /etc/redhat-release ]; then
        option=$(cat /etc/redhat-release | grep -oE '[0-9]+' | head -1)
    fi
    
    # 尝试lsb-release
    if [ -z "$option" ] && command -v lsb_release >/dev/null 2>&1; then
        option=$(lsb_release -rs | cut -d. -f1)
    fi
fi

# 最终判断
if [ -n "$option" ]; then
    echo "Detected system version: $option"
    echo "Successfully processed the file."
    # 执行你的后续操作
else
    echo "An error occurred: Unable to detect system version"
    exit 1
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
        if [[ "22.03" == "$(cat /etc/os-release 2>/dev/null | grep -Eo 'VERSION_ID="([^"]*)"' | cut -d'"' -f2)" ]]; then
            echo "Successfully processed the file."
            sed -i "/\$releasever/s/\$releasever/7/" /etc/yum.repos.d/docker-ce.repo
        else
            echo "An error occurred: No such file or directory."
        fi
        yum -y install docker-ce docker-ce-cli containerd.io
        if [ $? -ne '0' ]; then
         rpm -qa | grep docker | xargs rpm -e --nodeps
         echo "YUM配置异常请重新执行，如继续报错请联系作者QQ1284524409"
         exit 1
        fi
        yum -y install git rsyslog
    ;;
    20)
    echo "UOS Server 20 catch!"
    if [ ! -d "/etc/yum.repos.d/bak/" ]; then
        yum install -y yum-utils \
            device-mapper-persistent-data \
            lvm2 --allowerasing
        yum-config-manager \
            --add-repo \
            https://repo.huaweicloud.com/docker-ce/linux/centos/docker-ce.repo
		# 编码函数
		encode_to_base64() {
			echo -n "$1" | base64 -w 0
		}

		# 解码并执行 sed
		apply_sed() {
			local pattern="$1"
			local replacement="$2"
			local file="$3"
			
			# 编码模式和替换文本
			encoded_pattern=$(encode_to_base64 "$pattern")
			encoded_replacement=$(encode_to_base64 "$replacement")
			
			# 解码后执行 sed
			decoded_pattern=$(echo "$encoded_pattern" | base64 -d)
			decoded_replacement=$(echo "$encoded_replacement" | base64 -d)
			
			sed -i "s/${decoded_pattern}/${decoded_replacement}/g" "$file"
		}

		# 使用示例
		config_path='/etc/yum.repos.d/'

		# 1. 替换域名（完全不用担心特殊字符）
		apply_sed 'download.docker.com' 'repo.huaweicloud.com\/docker-ce' "${config_path}"/*.repo

		# 2. 修改 gpgcheck
		apply_sed 'gpgcheck=1' 'gpgcheck=0' "${config_path}"/*.repo

		# 3. 替换 $releasever（$ 符号不再需要转义）
		apply_sed '$releasever' '8' "${config_path}"/*.repo
		
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
    *)
    echo "Nothing to do"
	exit 1
    ;;
esac
if [ $? -ne '0' ]; then
 echo "YUM配置异常请联系作者QQ1284524409"
 exit 1
fi
service docker start
touch /etc/docker/daemon.json
cat > /etc/docker/daemon.json << EOF
{"registry-mirrors": ["https://dockerpull.com"]}
EOF
service docker restart
if [ ! -f "/usr/local/bin/docker-compose" ]; then
    # curl -SL https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    cat ./patch/docker-compose-linux-x86_64_* > ./patch/docker-compose-linux-x86_64
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
        case ${option} in
            5)
            echo "zabbix 5 LTSC!"
            ;;
            6|7|20)
            echo "zabbix 6 LTSC!"
            mkdir -p ./zbx_env/usr/share/zabbix/locale/zh_CN/LC_MESSAGES/
            \cp -rf ./patch/${GV_ARR_ENV[GV_WEB_UI_FILE_NAME]} ./zbx_env/usr/share/zabbix/locale/zh_CN/LC_MESSAGES/frontend.mo
#            mkdir -p ./zbx_env/etc/mysql/conf.d
            mkdir -p ./zbx_env/usr/share/doc/zabbix-server-mysql/
            \cp -f ./trans/${GV_ARR_ENV[GV_SQL_MYSQL_FILE_NAME]} ./zbx_env/usr/share/doc/zabbix-server-mysql/create.sql.gz
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
            sed -i -e "/^\#\$ModLoad imudp/s/^#//" /etc/rsyslog.conf
            sed -i -e "/^\#\$UDPServerRun 514/s/^#//" /etc/rsyslog.conf
            sed -i -e "/^\#\$ModLoad imtcp/s/^#//" /etc/rsyslog.conf
            sed -i -e "/^\#\$InputTCPServerRun 514/s/^#//" /etc/rsyslog.conf
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

    if [[ "$1" == "cp_proxy" ]]; then
        option=$(echo ${GV_VERSION} | cut -c 1)
        case ${option} in
            5)
            echo "zabbix 5 LTSC!"
            ;;
            6|7|20)
            echo "zabbix 6 LTSC!"
            mkdir -p ./zbx_env/etc/mysql
            \cp -rf ./patch/my.cnf ./zbx_env/etc/mysql/my.cnf
            \cp ./patch/docker-compose-linux-x86_64 /usr/local/bin/docker-compose
            mkdir -p /var/log/loki
            touch /var/log/loki/alert.log
            echo "test" > /var/log/loki/alert.log
            mkdir -p ./zbx_env/usr/lib/zabbix/alertscripts
            \cp ./patch/echo.sh ./zbx_env/usr/lib/zabbix/alertscripts/
            chmod 755 ./zbx_env/usr/lib/zabbix/alertscripts/echo.sh
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
            6|7|20)
            echo "zabbix 6 LTSC!"
            docker-compose -f docker-compose_v6_0_x_centos_mysql_local.yaml --profile=start6 up -d
            ;;
            *)
            echo "Nothing to do"
            ;;
        esac
        exit 1
    fi

    if [[ "$1" == "start_proxy" ]]; then
        option=$(echo ${GV_VERSION} | cut -c 1)
        case ${option} in
            5)
            echo "zabbix 5 LTSC!"
            docker-compose -f docker-compose_v6_0_x_centos_mysql_local.yaml --profile=prxstart5 up -d
            ;;
            6|7|20)
            echo "zabbix 6 LTSC!"
            docker-compose -f docker-compose_v6_0_x_centos_mysql_local.yaml --profile=prxstart6 up -d
            ;;
            *)
            echo "Nothing to do"
            ;;
        esac
        exit 1
    fi

    if [[ "$1" == "start_agent2" ]]; then
        docker-compose -f docker-compose_v6_0_x_centos_mysql_local.yaml --profile=start_agent2 up -d

        exit 1
    fi

    if [[ "$1" == "stop" ]]; then
        docker-compose -f compose_zabbix_components.yaml stop
        exit 1
    fi

    if [[ "$1" == "restart" ]]; then
        docker-compose -f compose_zabbix_components.yaml stop
        docker-compose -f docker-compose_v6_0_x_centos_mysql_local.yaml start
        exit 1
    fi

    if [[ "$1" == "down" ]]; then
        sh ./patch/down_mysql.sh
        exit 1
    fi

    if [[ "$1" == "down_proxy" ]]; then
        sh ./patch/down_mysql_proxy.sh
        exit 1
    fi
    
    if [[ "$1" == "down_agent2" ]]; then
        sh ./patch/down_agent2.sh
        exit 1
    fi

    if [[ "$1" == "rm" ]]; then
        docker-compose -f compose_zabbix_components.yaml rm
        exit 1
    fi

    if [[ "$1" == "init" ]]; then
        init
        exit 1
    fi
fi

#################################################
