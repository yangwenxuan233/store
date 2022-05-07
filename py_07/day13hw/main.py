'''
    报告：
        1.加载器：加载所有测试用例并得到所有用例
        2.使用运行器运行这些测试用例并生成报告
    任务2：
        减乘除：进行测试（）
        实现报告的邮件发送
'''
import HTMLTestRunner
import unittest
import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication


def run_case(path, case, name):
    # 1.加载所有用例
    tests = unittest.defaultTestLoader.discover(path, case)
    # 2.使用运行器
    runner = HTMLTestRunner.HTMLTestRunner(
        title="这是一份计算器的测试报告",
        description="这只是"+name+"运算的测试报告",
        verbosity=1,
        stream=open("Calc"+name+".html", mode="wb")
    )

    # 3.运行所有用例
    runner.run(tests)


# 4.实现邮件发送
def send_email(name):
    smtpserver = 'smtp.qq.com'
    sender = '1282398184@qq.com'
    password = 'pbcqpkvgbkdfbaai'
    receiver = '1282398184@qq.com'
    mail_title = '计算器测试用例执行结果'

    # 构造邮件对象
    msg = MIMEMultipart()
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = Header(sender, "utf-8")
    msg["To"] = Header(receiver, "utf-8")
    msg_content = "计算器测试用例执行结果见附件"
    msg.attach(MIMEText(msg_content, 'plain', 'utf-8'))

    # 添加附件
    htmlfile = 'Calc'+name+'.html'
    with open(htmlfile, mode='rb') as f:
        attfile = f.read()
    attachment = MIMEApplication(attfile)
    attachment["Content-Type"] = 'application/octet-stream'
    attachment["Content-Disposition"] = 'attachment;filename="%s.html"' % name
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


# run_case(r"D:\pscode\demo\day13hw", "testMul.py", "mul")
# run_case(r"D:\pscode\demo\day13hw", "testDev.py", "dev")
# run_case(r"D:\pscode\demo\day13hw", "testAdd.py", "add")
# run_case(r"D:\pscode\demo\day13hw", "testSub.py", "sub")

# send_email("add")
# send_email("sub")
# send_email("mul")
# send_email("dev")
