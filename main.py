import requests
import re
import time
import json
import getpass

s = requests.Session()
start = time.time()
data = {
    '_eventId': 'submit',
    'geolocation': ''
}

data['username'] = input('input SID: ')
data['password'] = getpass.getpass()

r = s.get(
    'https://cas.sustech.edu.cn/cas/login?service=https%3A%2F%2Ftis.sustech.edu.cn%2Fcas')
data['execution'] = re.findall('on" value="(.+?)"', r.text)[0]
# 进入教务系统
r = s.post(url='https://cas.sustech.edu.cn/cas/login?service=https%3A%2F%2Ftis.sustech.edu.cn%2Fcas', data=data)
file = open("lesson_list.json", "r", encoding='utf-8')
r = s.get(
    'https://cas.sustech.edu.cn/cas/login?service=https%3A%2F%2Ftis.sustech.edu.cn%2Fcas')
print(re.findall('on" value="(.+?)"', r.text))
lesson_list = json.load(file)
i = 0
while True:
    print(time.time()-start)
    for select_headers in lesson_list:
        r = s.post('https://tis.sustech.edu.cn/Xsxk/addGouwuche',
                   select_headers)
        # print(r.text)
        select_return = r.json()
        print(select_return['message'], select_return['jg'])
    i += 1
    if i == 10:
        flag = input('continue? y/n: ')
        if flag == 'y':
            i = 0
        else:
            exit(0)
