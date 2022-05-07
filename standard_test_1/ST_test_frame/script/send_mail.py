import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication
from ST_test_frame.config import settings
from ST_test_frame.common.logs import Logs


class SendEmail():
    '''发送邮件模块。
    '''

    def __init__(self) -> None:
        self.sender = settings.MAIL_LIST[0]
        self.receiver = ''  #
        self.password = ''  #
        self.smtpserver = ''  #
        self.logger = Logs()

    def send_email(self):
        self.msg = MIMEMultipart()
        self.msg['Subject'] = Header('', 'utf-8')
        self.msg['Form'] = Header(self.sender, 'utf-8')
        self.msg['To'] = Header(self.receiver, 'utf-8')
        content_text = 'results of testcase'
        self.msg.attach(MIMEText(content_text, 'plain', 'utf-8'))

        html_file = ''  #
        with open(html_file, mode='rb') as f:
            attfile = f.read()
        attachment = MIMEApplication(attfile)
        attachment['Content-Type'] = 'app;ocation/octet-stream'
        attachment['Content-Disposition'] = 'attachment;filename={}'.format('')  #
        self.msg.attach(attachment)

        try:
            smtp = SMTP_SSL(self.smtpserver)
            smtp.login(self.sender, self.password)
            smtp.sendmail(self.sender, self.receiver, self.msg.as_string())
            smtp.quit()
            self.logger.info('send email success')
        except smtplib.SMTPException as e:
            self.logger.error(e)
        self.logger.logger.handlers.pop()
