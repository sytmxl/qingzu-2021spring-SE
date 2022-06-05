from threading import Thread
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send():
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "1728999839@qq.com"  # 用户名
    mail_pass = "kvqbwapmiqdsegaa"  # 口令

    sender = '1728999839@qq.com'    # 发送邮箱
    receivers = ['1728999839@qq.com']  # 接收邮件

    message = MIMEText('请及时支付租金', 'plain', 'utf-8')
    message['From'] = Header("青年租房网", 'utf-8')
    message['To'] = Header("亲爱的租客", 'utf-8')

    subject = '青年租房网租金支付提示'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

def everyday():
    while True:
        send()
        sleep(5)    # seconds


if __name__ == '__main__':
    # Thread(target=send).start()
    everyday()
