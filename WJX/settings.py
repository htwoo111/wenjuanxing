# -*- coding: utf-8 -*

import random
from datetime import datetime

# form_data: 1$xxx} 1：表示第一个题目，xxx：表示选项(如果是选择题的话1表示第一个选项)
form_data = "1$xxx}2$xxx

# 设置IP，防止验证码出现
# 随机IP，
# IP = '{}.{}.{}.{}'.format(112, random.randint(
            # 64, 68), random.randint(0, 255), random.randint(0, 255))
# 设置东莞的IP
# DG_IP_LIST = ['125.93.72.235', '59.36.181.171', '218.16.72.192', '219.130.31.64', '116.4.246.88']
# IP = random.choice(DG_IP_LIST)
# 设置自己的IP
FAKE_IP_LIST = ['110.134.110.203', '111.91.111.156', '111.91.44.15']
IP = random.choice(MY_IP_LIST)


# 设置要填写的问卷星的网站
URL = 'https://www.wjx.top/m/xxxxxxxx.aspx'

# 设置问卷星开始的时间
# START_TIME = datetime(年，月，日，时，分，秒)
START_TIME = str(datetime(2019,10,24,10,25))[:-7]

# 设置日记
LOG_FILE = 'wenjunaxing.log'

# 设置邮箱信息
SENDER = "xxx@xxx.com"
SMTP_PASSWORD = 'xxx'
RECEIVER = 'xxx@xxx.com'