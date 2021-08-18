import HTMLTestRunner_cn
import unittest
import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication


def run_case(path, name):
    # 1.加载所有用例
    tests = unittest.defaultTestLoader.discover(path, pattern="Test*.py")

    runner = HTMLTestRunner_cn.HTMLTestRunner(
        title="这是一个新浪微博app的测试报告",
        description="这是一个登陆模块的测试报告",
        verbosity=1,
        stream=open(name + ".html", mode="wb")
    )

    runner.run(tests)


def send_email(name):
    smtpserver = 'smtp.qq.com'
    sender = '1282398184@qq.com'
    password = 'pbcqpkvgbkdfbaai'
    receiver = '2431320433@qq.com'  # '1282398184@qq.com'  '2431320433@qq.com'
    mail_title = '微博app测试用例执行结果'

    # 构造邮件对象
    msg = MIMEMultipart()
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = Header(sender, "utf-8")
    msg["To"] = Header(receiver, "utf-8")
    msg_content = "这是一份测试用例执行报告"
    msg.attach(MIMEText(msg_content, 'plain', 'utf-8'))

    # 添加附件
    htmlfile = name
    with open(htmlfile, mode='rb') as f:
        attfile = f.read()
    attachment = MIMEApplication(attfile)
    attachment["Content-Type"] = 'application/octet-stream'
    attachment["Content-Disposition"] = 'attachment;filename="%s"' % name
    msg.attach(attachment)

    # 发送邮件
    try:
        smtp = SMTP_SSL(smtpserver)  # ssl登录连接到邮件服务器
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("无法发送邮件")


# run_case(r"D:\pycode\autotest\autoweb06", "login")
send_email("login.html")
