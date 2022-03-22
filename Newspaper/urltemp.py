# coding:utf-8
# author:zhangyang
# date:2020-9-24
# 此程序用于爬取人民日报下的数据资源。主页面需要提取包括1946年到2003年之间所有月份
# 次级页面是各个月份的所有报道
# 末级页面是报道内容
from datetime import datetime

import requests
from bs4 import BeautifulSoup

import pandas as pd
import time

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Referer': 'http://paper.people.com.cn/rmrb/paperindex.htm',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}
# http://paper.people.com.cn/rmrb/html/2020-09/24/nbs.D110000renmrb_01.htm
# http://paper.people.com.cn/rmrb/html/2020-09/23/nbs.D110000renmrb_01.htm
# http://paper.people.com.cn/rmrb/html/年(4位)-月（2位）/日（2位）/nbs.D110000renmrb_版面（2位）.htm
def href(date,page):
    """
    用于获取某天新闻联播各条新闻的链接
    :param date: 日期，形如20200101
    :param page: 日报版面，形如01版、02版
    :return: href_list: 返回新闻链接的列表
    """
    href_list = []

    seris_date = str(date)[0:4] + '-' + str(date)[4:6] + '/' + str(date)[6:8]
    u1 = 'http://paper.people.com.cn/rmrb/html/' + seris_date + '/'
# http://paper.people.com.cn/rmrb/html/2020-09/01/nw.D110000renmrb_20200901_3-01.htm
    index_url = u1 + 'nbs.D110000renmrb_' + page + '.htm'
    response = requests.get(index_url, headers=headers)

#    response = requests.get('http://paper.people.com.cn/rmrb/html/' + \
#                            str(date)[0:3] + '-' + str(date)[4:5] + '/' + str(date)[6:7] + '/nbs.D110000renmrb_' + '01'\
#                            '.htm', headers=headers)

    bs_obj = BeautifulSoup(response.text, 'lxml')
    bs_obj.encoding = 'gb18030'
#    lis = bs_obj.find_all('li')
    for ultag in bs_obj.find_all('ul', {'class': 'news-list'}):
        for litag in ultag.find_all('li'):
            href_list.append(u1+litag.find('a')['href'])
#             each.find('a')['href']
#             href_list.append(u1+i)

    return href_list #href_list

def news(url):
    print(url)
    response = requests.get(url, headers=headers, )
    bs_obj = BeautifulSoup(response.content.decode('utf-8'), 'lxml')

    text = bs_obj.find('div', {'class': 'article'}).text
    return text


def datelist(beginDate, endDate):
    # beginDate, endDate是形如‘20160601’的字符串或datetime格式
    date_l = [datetime.strftime(x, '%Y%m%d') for x in list(pd.date_range(start=beginDate, end=endDate))]
    return date_l


def save_text(date,page):
    """
    用于保存每天不同版面各条信息的tex文本
    :param date: 日期，形如20200101
    :param page: 日报版面，形如01版、02版
    :return: 无返回
    """

    f = open(str(date) + '_' + str(page)+'.txt', 'a', encoding='utf-8')
#    each = 'http://paper.people.com.cn/rmrb/html/2020-09/01/nw.D110000renmrb_20200901_2-01.htm'
    for each in href(date,page)[1:]:
        f.write(news(each))
        f.write('\n')
    f.close()


for date in datelist('20200901', '20200901'):
    for i in range(6):  # pages
        page = str(i+1) if i>9 else "0"+str(i+1)
        save_text(date,page)
        time.sleep(3)

