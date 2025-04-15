#/bin/bash
_alertscripts="/usr/lib/zabbix/alertscripts"
read -p "please input qqmailseq:" _qqmailseq
read -p "please input qqmailpwd:" _qqmailpwd
\cp mail-py3.py ${_alertscripts}/
sed -i "/_qqmailseq = '.*'/s/_qqmailseq = '.*'/_qqmailseq = '${_qqmailseq}'/" ${_alertscripts}/mail-py3.py
sed -i "/_qqmailpwd = '.*'/s/_qqmailpwd = '.*'/_qqmailpwd = '${_qqmailpwd}'/" ${_alertscripts}/mail-py3.py
chmod 644 ${_alertscripts}/mail-py3.py
chown zabbix:zabbix ${_alertscripts}/mail-py3.py



