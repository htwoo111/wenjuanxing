# -*- coding: utf-8 -*

import requests
import re
import time
import random
import datetime
from settings import FORM_DATA, IP, URL


class WenJuanXing(object):
    def __init__(self, url):
        """
        url:要填写的问卷的url
        """
        self.wj_url = url
        self.post_url = None
        self.header = None
        self.cookie = None
        self.data = None

    def set_data(self):
        """
        生成问卷星提交表单
        """
        form_data = FORM_DATA  # 从设置中读取要提交表单的信息
        self.data = {
            "submitdata": form_data
        }

    def set_header(self):
        """
        随机生成ip，设置X-Forwarded-For
        ip需要控制ip段，不然生成的大部分是国外的
        :return:
        """
        ip = IP
        self.header = {
            'X-Forwarded-For': ip,
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }

    def get_ktimes(self):
        """
        随机生成一个ktimes,ktimes是构造post_url需要的参数，为一个整数
        :return:
        """
        return random.randint(5, 10)

    def get_response(self):
        """
        访问问卷网页，获取网页代码
        :return: get请求返回的response
        """
        response = requests.get(url=self.wj_url, headers=self.header)
        self.cookie = response.cookies
        return response

    def get_jqnonce(self, response):
        """
        通过正则表达式找出jqnonce,jqnonce是构造post_url需要的参数
        :param response: 访问问卷网页，返回的reaponse
        :return: 找到的jqnonce
        """
        jqnonce = re.search(r'.{8}-.{4}-.{4}-.{4}-.{12}', response.text)
        return jqnonce.group()

    def get_rn(self, response):
        """
        通过正则表达式找出rn,rn是构造post_url需要的参数
        :param response: 访问问卷网页，返回的reaponse
        :return: 找到的rn
        """
        rn = re.search(r'\d{9,10}\.\d{8}', response.text)
        return rn.group()

    def get_id(self, response):
        """
        通过正则表达式找出问卷id,问卷是构造post_url需要的参数
        :param response: 访问问卷网页，返回的reaponse
        :return: 找到的问卷id
        """
        id = re.search(r'\d{8}', response.url)
        return id.group()

    def get_jqsign(self, ktimes, jqnonce):
        """
        通过ktimes和jqnonce计算jqsign,jqsign是构造post_url需要的参数
        :param ktimes: ktimes
        :param jqnonce: jqnonce
        :return: 生成的jqsign
        """
        result = []
        b = ktimes % 10
        if b == 0:
            b = 1
        for char in list(jqnonce):
            f = ord(char) ^ b
            result.append(chr(f))
        return ''.join(result)

    def get_start_time(self, response):
        """
        通过正则表达式找出问卷starttime,问卷是构造post_url需要的参数
        :param response: 访问问卷网页，返回的reaponse
        :return: 找到的starttime
        """
        start_time = re.search(r'\d+?/\d+?/\d+?\s\d+?:\d{2}', response.text)
        return start_time.group()

    def set_post_url(self):
        """
        生成post_url
        :return:
        """
        self.set_header()  # 设置请求头，更换ip
        response = self.get_response()  # 访问问卷网页，获取response
        ktimes = self.get_ktimes()  # 获取ktimes
        jqnonce = self.get_jqnonce(response)  # 获取jqnonce
        rn = self.get_rn(response)  # 获取rn
        id = self.get_id(response)  # 获取问卷id
        jqsign = self.get_jqsign(ktimes, jqnonce)  # 生成jqsign
        start_time = self.get_start_time(response)  # 获取starttime
        time_stamp = '{}{}'.format(
            int(time.time()), random.randint(100, 200))  # 生成一个时间戳，最后三位为随机数
        url = 'https://www.wjx.cn/joinnew/processjq.ashx?submittype=1&curID={}&t={}&starttim' \
              'e={}&ktimes={}&rn={}&jqnonce={}&jqsign={}'.format(
                  id, time_stamp, start_time, ktimes, rn, jqnonce, jqsign)
        self.post_url = url  # 设置url
        # print("表单提交地址：{}".form5at(self.post_url))

    def post_data(self):
        """
        发送数据给服务器
        :return: 服务器返回的结果
        """
        self.set_data()
        response = requests.post(
            url=self.post_url, data=self.data, headers=self.header, cookies=self.cookie)
        return response

    def run(self):
        """
        填写一次问卷
        :return:
        """
        self.set_post_url()
        result = self.post_data()
        print("response_content:{}, status_code:{}".format(
            result.text, result.status_code))
        return result.text, result.status_code

    def mul_run(self, n):
        """
        填写多次问卷
        :return:
        """
        for i in range(n):
            time.sleep(0.1)
            response_text, response_status = self.run()
            print("response_content:{}, status_code:{}".format(
                response_text, response_status))


if __name__ == '__main__':
    url = URL
    w = WenJuanXing(url)
    now = datetime.datetime.now()
    print(now)
    w.run()
