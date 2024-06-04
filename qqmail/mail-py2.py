#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import getopt
import smtplib
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from subprocess import *

reload(sys)
sys.setdefaultencoding('utf8')

def sendqqmail(username, password, mailfrom, mailto, subject, content):
    gserver = 'smtp.qq.com'
    ##定义发邮件类型
    gport = 465
    try:
        msg = MIMEText(unicode(content).encode('utf-8'))
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
    except Exception,err:
        print "Send mail failed. Error: %s" % err


def main():
    _qqmailseq = ''
    _qqmailpwd = ''
    to = sys.argv[1]
    subject = sys.argv[2]
    content = sys.argv[3]
    ##定义QQ邮箱的账号和密码，你需要修改成你自己的账号和密码（请不要把真实的用户名和密码放到网上公开，否则你会死的很惨）
    sendqqmail(_qqmailseq, _qqmailpwd, _qqmailseq, to, subject, content)


if __name__ == "__main__":
    main()

#####脚本使用说明######
# 1. 首先定义好脚本中的邮箱账号和密码
# 2. 脚本执行命令为：python mail.py "邮箱账号" "邮件主题" "邮件内容"
