import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import pandas as pd
import time

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Referer': 'http://tv.cctv.com/lm/xwlb/',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}


def href(date):
    """
    用于获取某天新闻联播各条新闻的链接
    :param date: 日期，形如20190101
    :return: href_list: 返回新闻链接的列表
    """
    href_list = []

    response = requests.get('http://tv.cctv.com/lm/xwlb/day/' + str(date) + '.shtml', headers=headers)
    bs_obj = BeautifulSoup(response.text, 'lxml')
    lis = bs_obj.find_all('li')
    for each in lis:
        href_list.append(each.find('a')['href'])
    return href_list


def news(url):
    print(url)
    response = requests.get(url, headers=headers, )
    bs_obj = BeautifulSoup(response.content.decode('utf-8'), 'lxml')
    if 'news.cctv.com' in url:
        text = bs_obj.find('div', {'id': 'content_body'}).text
    else:
        text = bs_obj.find('div', {'class': 'cnt_bd'}).text
    return text


def datelist(beginDate, endDate):
    # beginDate, endDate是形如‘20160601’的字符串或datetime格式
    date_l = [datetime.strftime(x, '%Y%m%d') for x in list(pd.date_range(start=beginDate, end=endDate))]
    return date_l


def save_text(date):
    f = open(str(date) + '.txt', 'a', encoding='utf-8')
    for each in href(date)[1:]:
        f.write(news(each))
        f.write('\n')
    f.close()


for date in datelist('20200924', '20200924'):
    save_text(date)
    time.sleep(3)