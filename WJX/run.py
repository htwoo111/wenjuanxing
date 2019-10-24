# -*- coding: utf-8 -*
from emailer import Emailer
from datetime import datetime
from main_program import WenJuanXing
from my_logger import logger
from settings import URL, START_TIME


def fill_form(url):
    """
    填写问卷星
    """
    w = WenJuanXing(url)
    try:
        # 接收提交表单后的结果
        response_text, response_status = w.run()
        return response_text, response_status
    except Exception as e:
        LOGGER.debug(e)
        print('main.py raise a error: {}'.format(e))
        return None

def send_email(title, content):
    email = Emailer(title, content)
    email.run()

def main():
    # 获取当前时间
    now = str(datetime.now())[:-7]
    print('当前时间是：{}'.format(now))
    ret = fill_form(URL)
    # 判断是否程序出错
    if ret:
        title = '问卷星填写结果'
        content = '当前时间：{}\nresponse text:{}\nresponse status code:{}'.format(now, *ret)
        send_email(title, content)

if __name__ == '__main__':
    main()
