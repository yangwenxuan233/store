import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication


# 调用时传入参数为同一路径下的文件名称 如test.html
def send_email(name):
    smtpserver = 'smtp.qq.com'  # qq邮箱服务器
    sender = '00000000000@qq.com'  # 发送人
    password = 'xxxxxxxxxxxxxxxx'  # 16位授权码
    receiver = '000000000000@qq.com'  # 接收人
    mail_title = '这是标题'  # 邮件标题

    # 构造邮件对象
    msg = MIMEMultipart()
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = Header(sender, "utf-8")
    msg["To"] = Header(receiver, "utf-8")
    # 将文本信息添加到邮件正文
    msg_content = "这是正文"
    msg.attach(MIMEText(msg_content, 'plain', 'utf-8'))

    # 构造附件对象
    htmlfile = name
    with open(htmlfile, mode='rb') as f:
        attfile = f.read()
    attachment = MIMEApplication(attfile)
    # 配置附件参数
    attachment["Content-Type"] = 'application/octet-stream'
    attachment["Content-Disposition"] = 'attachment;filename="%s"' % name
    # 将附件添加到邮件中
    msg.attach(attachment)

    # 发送邮件
    try:
        smtp = SMTP_SSL(smtpserver)  # ssl登录连接到邮件服务器 需要手动开启SMTP服务
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("无法发送邮件")
