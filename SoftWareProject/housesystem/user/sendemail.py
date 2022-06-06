import random
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.header import Header
#from .models import *
import datetime


def send(to):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = '1728999839@qq.com'  # 用户名
    mail_pass = "kvqbwapmiqdsegaa"  # 口令

    sender = '1728999839@qq.com'  # 发送邮箱
    receivers = [to]  # 接收邮件

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
        print("邮件发送成功", end='至:')
        print(to)
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


def sendcode(to):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = '1728999839@qq.com'  # 用户名
    mail_pass = "kvqbwapmiqdsegaa"  # 口令

    sender = '1728999839@qq.com'  # 发送邮箱
    receivers = [to]  # 接收邮件

    strcode = ''
    for i in range(6):
        strcode += str(int(random.Random().random() * 10))
    message = MIMEText('验证码:'+strcode, 'plain', 'utf-8')
    message['From'] = Header("青年租房网", 'utf-8')
    message['To'] = Header("亲爱的用户", 'utf-8')

    subject = '青年租房网注册验证码'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功", end='至:')
        print(to)
        return strcode
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
        false = 'X'
        return false


def check(begin, end):
    today = datetime.date.today()
    month = datetime.timedelta(days=30)
    week = datetime.timedelta(weeks=1)
    zero = datetime.timedelta(days=0)
    if end-begin >= month:
        temp = begin
        while temp <= end:
            if zero < temp-today <= week:
                ture = True
                return ture
            temp += month
    false = False
    return false


def everyday():
    while True:
        orders = Order.objects.all()
        for order in orders:
            if order.Pay == 0:
                if check(order.OrderDate, order.DueDate):
                    user = User.objects.get(UserID=order.UserID)
                    # send(user.Email)
                    print(user.Email)
        # send('1728999839@qq.com')
        sleep(60*60*24)  # seconds


if __name__ == '__main__':
    # Thread(target=send).start()
    # everyday()
    time = datetime.date.today()
    month = datetime.timedelta(days=30)
    week = datetime.timedelta(weeks=1)
    time2 = datetime.date(2022, 6, 23)
    print(time)
    print(time + month)
    print(time + month - week)
    print(time2 - time)
    gap = time2 - time
    print(gap.days>16)
    strcode = ''
    for i in range(6):
        strcode += str(int(random.Random().random() * 10))
    code = random.Random().random() * 10
    code = int(code)
    print(code)
    print(strcode)
    sendcode('1728999839@qq.com')