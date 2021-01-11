import requests
import re
import time
import json

s = requests.Session()
start = time.time()
data = {
    '_eventId': 'submit',
    'geolocation': ''
}

data['username'] = input('input SID: ')
data['password'] = input('input passwd: ')

r = s.get(
    'https://cas.sustech.edu.cn/cas/login?service=https%3A%2F%2Ftis.sustech.edu.cn%2FcasLogin')
# 记得写账号和密码
data['execution'] = re.findall('on" value="(.+?)"', r.text)[0]
# 进入教务系统
r = s.post(
    'https://cas.sustech.edu.cn/cas/login?service=https%3A%2F%2Ftis.sustech.edu.cn%2FcasLogin', data)

file = open("lesson_list.json", "r", encoding='utf-8')

lesson_list = json.load(file)
for i in range(10):
    print(time.time()-start)
    for select_headers in lesson_list:
        r = s.post('https://tis.sustech.edu.cn/Xsxk/addGouwuche', select_headers)
        select_return = r.json()
        print(select_return['message'], select_return['jg'])
    if i == 9:
        flag = input('continue? y/n: ')
        if flag == 'y':
            i = 0
