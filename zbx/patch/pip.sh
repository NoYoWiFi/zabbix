#/bin/bash
set -eux && \
INSTALL_PKGS="python3 \
        python3-pip" && \
microdnf -y install \
    --disablerepo "*" \
    --enablerepo "baseos" \
    --enablerepo "appstream" \
    --enablerepo "crb" \
    --enablerepo="epel" \
    --setopt=install_weak_deps=0 \
    --setopt=keepcache=0 \
    --best \
    --nodocs ${INSTALL_PKGS}
mkdir ~/.pip
touch ~/.pip/pip.conf
cat > ~/.pip/pip.conf << EOF
[global]
cache-dir = ~/.pip/
index-url = https://mirrors.aliyun.com/pypi/simple/

[install]

trusted-host = https://mirrors.aliyun.com
disable-pip-version-check = true
timeout = 6000

EOF
python3 -m pip install --upgrade pip
pip3 install paramiko openpyxl
pip3 install cryptography==3.4.8
pip3 install alibabacloud_dysmsapi20170525
rpm -ivh /tmp/tcping-1.3.5-19.el8.x86_64.rpm