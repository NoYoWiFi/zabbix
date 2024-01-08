#!/bin/sh
#export QT_DEBUG_PLUGINS=1
\chmod 755 ./sqldrivers/libqsqlmysql.so
rm -rf /etc/ld.so.conf.d/qtlib.conf
rm -rf /lib64/qtlib
\cp -vrf ./qtlib.conf /etc/ld.so.conf.d/
\cp -vrf ./qtlib /lib64/
\cp -vrf ./qml/* ./
\cp -vrf ./plugins/* ./
\chmod 755 ./autosetup
ldconfig
rpm -ivhU ./pip/rpm/python2-*
shellFolder=$(dirname $(readlink -f "$0"))
cd $shellFolder/pip
rpm -ivhU unzip-6.0-19.el7.x86_64.rpm
cd $shellFolder/pip
unzip -o setuptools-41.0.1.zip
cd setuptools-41.0.1
python2 setup.py install --prefix=/usr/
cd $shellFolder/pip
tar -zxvf xlrd-1.2.0.tar.gz
cd xlrd-1.2.0
python2 setup.py install --prefix=/usr/
cd $shellFolder/pip
tar -zxvf xlwt-1.3.0.tar.gz
cd xlwt-1.3.0
python2 setup.py install --prefix=/usr/
cd $shellFolder/pip
tar -zxvf future-0.18.2.tar.gz
cd future-0.18.2
python2 setup.py install --prefix=/usr/
cd $shellFolder/pip
tar -zxvf pip-19.3.1.tar.gz
cd pip-19.3.1
python2 setup.py install --prefix=/usr/
cd $shellFolder/pip
tar -zxvf pycparser-2.19.tar.gz
cd pycparser-2.19
python2 setup.py install --prefix=/usr/
cd $shellFolder/pip
pip install cffi-*.whl
pip install six-*.whl
pip install bcrypt-*.whl
pip install PyNaCl-*.whl
pip install enum34-*.whl
pip install ipaddress-*.whl
pip install cryptography-*.whl
pip install paramiko-*.whl
pip install PyMySQL-*.whl
