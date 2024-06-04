#!/usr/bin/env python
import os
import sys
import getopt
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
from subprocess import *
import re


def sendqqmail(username, password, mailfrom, mailto, subject, content):
    gserver = 'smtp.qq.com'
    ##定义发邮件类型
    gport = 465
    try:
        msg = MIMEText(content,"plain","utf-8")
        msg['from'] = mailfrom
        msg['to'] = mailto
        msg['Reply-To'] = mailfrom
        msg['Subject'] = subject
        # ssl连接，把下面改为smtp = smtplib.SMTP_SSL(gserver, gport)
        smtp = smtplib.SMTP_SSL(gserver, gport)
        smtp.set_debuglevel(0)
        smtp.ehlo()
        smtp.login(username, password)
        smtp.sendmail(mailfrom, mailto, msg.as_string())
        smtp.close()
    except Exception as err:
        print("Send mail failed. Error: %s" % err)


def main():
    _qqmailseq = ''
    _qqmailpwd = ''
    to = sys.argv[1].split(';')
    subject = sys.argv[2]
    content = sys.argv[3]
    ##定义QQ邮箱的账号和密码，你需要修改成你自己的账号和密码（请不要把真实的用户名和密码放到网上公开，否则你会死的很惨）
    for i in range(len(to)):
        sendqqmail(_qqmailseq, _qqmailpwd, _qqmailseq, to[i], subject, content)


if __name__ == "__main__":
    main()

#####脚本使用说明######
# 1. 首先定义好脚本中的邮箱账号和密码
# 2. 脚本执行命令为：python mail.py "邮箱账号" "邮件主题" "邮件内容"
