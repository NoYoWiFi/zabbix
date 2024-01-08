#!/bin/bash
shellFolder=$(dirname $(readlink -f "$0"))
cd $shellFolder/pip
rpm -ivhU unzip-6.0-19.el7.x86_64.rpm
cd $shellFolder/pip
unzip setuptools-41.0.1.zip
cd setuptools-41.0.1
python setup.py install
cd $shellFolder/pip
tar -zxvf xlrd-1.2.0.tar.gz
cd xlrd-1.2.0
python setup.py install
cd $shellFolder/pip
tar -zxvf future-0.18.2.tar.gz
cd future-0.18.2
python setup.py install
cd $shellFolder/pip
tar -zxvf pip-19.3.1.tar.gz
cd pip-19.3.1
python setup.py install
cd $shellFolder/pip
tar -zxvf pycparser-2.19.tar.gz
cd pycparser-2.19
python setup.py install
cd $shellFolder/pip
pip install cffi-1.13.2-cp27-cp27mu-manylinux1_x86_64.whl
pip install six-1.12.0-py2.py3-none-any.whl
pip install bcrypt-3.1.7-cp27-cp27mu-manylinux1_x86_64.whl
pip install PyNaCl-1.3.0-cp27-cp27mu-manylinux1_x86_64.whl
pip install enum34-1.1.6-py2-none-any.whl
pip install ipaddress-1.0.23-py2.py3-none-any.whl
pip install cryptography-2.8-cp27-cp27mu-manylinux1_x86_64.whl
pip install paramiko-2.6.0-py2.py3-none-any.whl




