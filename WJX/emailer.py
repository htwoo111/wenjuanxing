# -*- coding: utf-8 -*
from datetime import datetime
import smtplib
# 在设置邮件的主题、内容时需要用到的模块
from email.mime.text import MIMEText
from email.header import Header
from settings import SENDER, SMTP_PASSWORD, RECEIVER



class Emailer(object):
    def __init__(self, title, content):
        # self.title = input('请输入标题：')
        # self.content = input('请输入邮件内容：')
        self.title = title
        self.content = content

    def send(self):
        # 163邮箱的服务器地址，如果需要实现用其它邮箱实现发送
        # 邮件，这里需要改为其它邮箱的服务器地址
        mail_server = "smtp.163.com"

        # 163邮箱的端口
        # mail_port = 25

        # 163邮箱的用户名
        # mail_user = SENDER    #这里设置自己的邮箱的用户名

        # 163邮箱的密码，注意：不是登录密码，而是授权密码
        # 授权密码的设置步骤:登录--》设置--》POP3/SMTP/IMAP--》客户端授权密码
        # 设置了授权密码后，记得回到POP3/SMTP/IMAP中把最上面两个的勾打上
        # password = SMTP_PASSWORD    #自己设置的授权密码

        # 设置邮件收件人, 可以设置多个收信人
        # receiver = RECEIVER

        # 创建邮件,设置邮件的格式
        message = MIMEText(self.content, 'plain', 'utf8')
        # 设置主题,下面的必须为Subject，不能自己随意更改
        # 以下的三个内容必须设置，否则容易出现554的错误
       # message["Subject"] = self.title
        message['Subject'] = Header(self.title, 'utf-8')
        # 设置发件人
        message["From"] = SENDER
        # 设置收件人
        message["To"] = RECEIVER

        # 连接服务器，通过smtplib.SMTP()连接
        # 第一个参数是邮箱服务器地址，第二个参数是邮箱服务器的端口
        conneServer = smtplib.SMTP_SSL(mail_server, 465)
        # 登录邮箱
        conneServer.login(SENDER, SMTP_PASSWORD)
        # 发送邮件
        conneServer.sendmail(SENDER, RECEIVER, message.as_string())

        # 发送完后必须关闭,否则浪费空间资源
        conneServer.close()

    def run(self):
        print('-'*25 + '开始发送邮件' + '-'*25)
        print('发送邮件到：{}'.format(RECEIVER))
        print('title:{}'.format(self.title))
        print('content:')
        print('\t{}'.format(self.content))
        self.send()
        print('-'*25 + '发送成功' + '-'*25)


if __name__ == '__main__':
    # 抽取要复习的项目
    now = datetime.now()  # 获取当前时间

    # 邮件的title
    title = '复习 : {}'.format('xxx')
    # 邮件内容
    content = '''
            time : {} \n
            复习 : {}
            '''.format(now, 'xxx')
    # 通过邮件通知
    emailer = Emailer(title, content)
    emailer.run()
