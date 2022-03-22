import requests
import sys
import io
import time
import json

# 登录时需要POST的数据
data = {'loginName': '60918',
        'pwd': 'dcc001da682622dd35440f27cb241246',
        #      dcc001da682622dd35440f27cb241246
        'platformType': '3',
        'clientVersion': '0.1'}

# 设置请求头
headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}

# 登录时表单提交到的地址（用开发者工具可以看到）
url_basic = 'http://10.44.202.52/manage/login/login'
t = int(round(time.time() * 1000))
login_url = url_basic + '?t=' + str(t)
# 1598947290419

# 构造Session
session = requests.Session()
# 在session中发送登录请求，此后这个session里就存储了cookie
# 可以用print(session.cookies.get_dict())查看
resp = session.post(login_url, data)
print(session.cookies.get_dict())
# 登录后才能访问的网页

t = int(round(time.time() * 1000))
headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'token': '100159894150397800',
    'Referer': 'http://10.44.202.52/center/pattendanceRecord?defMoment=&month=08&year=2020',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

params = (
    ('t', str(t)),
    ('month', '08'),
    ('year', '2020'),
)

# 发送访问请求
resp = session.get('http://10.44.202.52/manage/pAttendanceRecord/web', headers=headers, params=params, verify=False)

res = json.loads(resp.text).get('obj')
print(res)
