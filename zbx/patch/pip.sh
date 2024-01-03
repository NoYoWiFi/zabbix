#/bin/bash
yum -y install python3
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
pip3 install  paramiko openpyxl
pip3 install  cryptography==3.4.8
rpm -ivh /tmp/tcping-1.3.5-19.el8.x86_64.rpm