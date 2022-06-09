#-- coding:UTF-8 --
import os
import sys
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'housesystem.settings')
django.setup()
import random
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from user.models import Order, User
from index.models import *
# from .models import *
import datetime


def send(to, text):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = '1728999839@qq.com'  # 用户名
    mail_pass = "kvqbwapmiqdsegaa"  # 口令

    sender = '1728999839@qq.com'  # 发送邮箱
    receivers = [to]  # 接收邮件

    message = MIMEText(text, 'plain', 'utf-8')
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

    begin = begin.date()
    end = end.date()

    today = datetime.date.today()
    month = datetime.timedelta(days=30)
    week = datetime.timedelta(weeks=1)
    zero = datetime.timedelta(days=0)
    print("begin: ", end="")
    print(begin)
    print("end: ", end="")
    print(end)
    if end-begin >= month:
        temp = begin
        while temp <= end:
            if zero < temp-today <= week:
                return True, temp
            temp += month
    return False, today


def everyday(time):
    while True:
        orders = Order.objects.all()
        print('##########')
        print('start:')
        print('##########')
        for order in orders:
            if order.Pay == 0:
                flag, ddl = check(order.OrderDate, order.DueDate)
                if flag:
                    user = User.objects.get(UserID=order.UserID)
                    text = "亲爱的用户，你有一单长租的月租尚未支付，请在" + str(ddl) + "之前提交，谢谢。"
                    send(user.Email, text)
                else:
                    print('skip')
        # send('1728999839@qq.com')
        # sleep(60*60*24)  # seconds
        sleep(time)


def main():
    time = datetime.date.today()
    month = datetime.timedelta(days=30)
    week = datetime.timedelta(weeks=1)
    time2 = datetime.date(2022, 6, 23)
    print(time)
    print(time + month)
    print(time + month - week)
    print(time2 - time)
    gap = time2 - time
    print(gap.days > 16)
    strcode = ''
    for i in range(6):
        strcode += str(int(random.Random().random() * 10))
    code = random.Random().random() * 10
    code = int(code)
    print(code)
    print(strcode)
    # sendcode('1728999839@qq.com')


    '''pics = Picture.objects.all()
    for pic in pics:
        pic.PicPath = pic.PicPath + '.png'
        pic.save()'''

def switch(city):
    lay = city.split('/')
    if lay[1] == '直辖市':
        city = lay[0][:-1] + lay[2][:-1]
    else:
        city = lay[1][:-1] + lay[2][:-1]
    print(city)


if __name__ == '__main__':
    # Thread(target=).start()

    day = 60*60*24  # 一天一次
    everyday(time=day)
    '''ip = '43.138.67.29:8090'
    pics = Picture.objects.all()
    for pic in pics:
        string = pic.PicPath.split('/')
        pic.PicPath = string[0] + '/' + string[1] + '/' + ip + '/' + string[3] + '/' + string[4]
        print(pic.PicPath)
        pic.save()'''





