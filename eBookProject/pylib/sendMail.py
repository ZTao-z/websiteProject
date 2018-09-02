# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def sendMsgByMail(receiverList, msg):
    # 第三方 SMTP 服务
    from_addr = "13424111354@163.com"
    password = "publicmail233"
    to_addr = receiverList
    smtp_server = "smtp.163.com"

    msg = MIMEText(msg, 'plain', 'utf-8')
    msg['From'] = _format_addr('肥宅工具箱 <%s>' % from_addr)
    msg['To'] = _format_addr('肥宅 <%s>' % to_addr)
    msg['Subject'] = Header('来自肥宅工具箱的通知', 'utf-8').encode()

    server = smtplib.SMTP()
    server.connect(smtp_server)
    server.starttls()
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
    return 1
