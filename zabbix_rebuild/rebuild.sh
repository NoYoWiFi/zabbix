#/bin/bash
# 设置了这个选项以后，包含管道命令的语句的返回值，会变成最后一个返回非零的管道命令的返回值。
set -o pipefail

# 执行的时候如果出现了返回值为非零将会继续执行下面的脚本
set +e

# Script trace mode
set -o xtrace
shellFolder=$(dirname $(readlink -f "$0"))
ZBX_VERSION=$(cat .version)
function check_ip_status()
{
    ping -c 3 -i 0.2 -W 3 $1 &> /dev/null
    if [ $? -eq 0 ];then
        return 0
    else
        return -1
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
    yum install -y yum-utils \
        device-mapper-persistent-data \
        lvm2 --allowerasing
    if [ $? -ne '0' ]; then
     echo "YUM ERROR!! EXIT!!"
     exit 1
    fi
    yum-config-manager \
        --add-repo \
        https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
    yum -y install docker-ce docker-ce-cli containerd.io --allowerasing
    yum -y install git
fi
chmod 755 -R ../fastgithub_linux-x64/
yum -y install libicu
ps -ef | grep fast | awk -F ' ' '{print $2}' | xargs kill -9
/bin/bash -c "nohup ../fastgithub_linux-x64/fastgithub >/dev/null 2>&1 & " && echo 1
sleep 10
git config --global http.sslVerify false
export http_proxy="http://127.0.0.1:38457"
export https_proxy="https://127.0.0.1:38457"
# 取消http代理
# git config --global --unset http.proxy
# 取消https代理 
# git config --global --unset https.proxy
git config --global http.proxy "http://127.0.0.1:38457"
git config --global https.proxy "https://127.0.0.1:38457"

cd /tmp
# ZBX_SOURCES=https://gitcode.net/mirrors/zabbix/zabbix.git
ZBX_SOURCES=https://github.com/zabbix/zabbix.git
git -c advice.detachedHead=false clone ${ZBX_SOURCES} --branch ${ZBX_VERSION} --depth 1 --single-branch /tmp/zabbix-${ZBX_VERSION}
if [ $? -ne '0' ]; then
 exit 1
fi
tar -zcf zabbix-${ZBX_VERSION}.tar.gz zabbix-${ZBX_VERSION}/
cd /tmp
\cp zabbix-${ZBX_VERSION}.tar.gz ${shellFolder}/
# ZBX_SOURCES=https://gitcode.net/mirrors/zabbix/zabbix-docker.git
ZBX_SOURCES=https://github.com/zabbix/zabbix-docker.git
git -c advice.detachedHead=false clone ${ZBX_SOURCES} --branch ${ZBX_VERSION:0:3} --depth 1 --single-branch /tmp/zabbix-docker-${ZBX_VERSION}
if [ $? -ne '0' ]; then
 exit 1
fi
tar -zcf zabbix-docker-${ZBX_VERSION}.tar.gz zabbix-docker-${ZBX_VERSION}/
cd /tmp
\cp zabbix-docker-${ZBX_VERSION}.tar.gz ${shellFolder}/
cd /tmp
ZBX_SOURCES=https://git.zabbix.com/scm/ap/mongodb.git
git -c advice.detachedHead=false clone ${ZBX_SOURCES} --branch ${ZBX_VERSION} --depth 1 --single-branch /tmp/mongodb_plugin
if [ $? -ne '0' ]; then
 exit 1
fi
tar -zcf mongodb_plugin.tar.gz mongodb_plugin/
cd /tmp
\cp mongodb_plugin.tar.gz ${shellFolder}/
cd /tmp
ZBX_SOURCES=https://git.zabbix.com/scm/ap/postgresql.git
git -c advice.detachedHead=false clone ${ZBX_SOURCES} --branch ${ZBX_VERSION} --depth 1 --single-branch /tmp/postgresql_plugin
if [ $? -ne '0' ]; then
 exit 1
fi
tar -zcf postgresql_plugin.tar.gz postgresql_plugin/
cd /tmp
\cp postgresql_plugin.tar.gz ${shellFolder}/
cd ${shellFolder}/
ZBX_VERSION=$(cat .version)
mkdir -p /opt/zbx/
tar -zxf ./zabbix-docker-${ZBX_VERSION}.tar.gz -C /opt/zbx/ --strip-components 1
\cp -vrf ../zbx/ /opt/
cat /opt/zbx/patch/go1.19.13.linux-amd64.tar.gz_* > /opt/zbx/patch/go1.19.13.linux-amd64.tar.gz
cat /opt/zbx/patch/NotoSansCJKjp-hinted.zip_* > /opt/zbx/patch/NotoSansCJKjp-hinted.zip
\cp .version /opt/zbx/patch/
\cp zabbix-${ZBX_VERSION}.tar.gz /opt/zbx/patch/
\cp postgresql_plugin.tar.gz /opt/zbx/patch/
\cp mongodb_plugin.tar.gz /opt/zbx/patch/
chmod 755 -R /opt/zbx/
cd /opt/zbx/

