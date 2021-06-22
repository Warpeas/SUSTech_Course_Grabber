from lesson_grabber import form_data, grabber, STOP, RUN
import getpass
import json
import datetime
import time
from encrypt import *

grabber = grabber()

try:
    f = open('user.info', 'r')
except:
    while True:
        username = input('SID: ')
        password = getpass.getpass()
        grabber.account(username, password)
        print("try login")
        if grabber.login():
            print("login success")
            break
        else:
            print("login failed")
    flag = input("Do you want to save password? y/n ")
    if flag == "y":
        with open('user.info', 'w') as f:
            print(des_encrypt(username+"-"+password), file=f, end="")
else:
    user_info = des_decrypt(f.read())
    user_info = user_info.split("-")
    # print(user_info)
    username = user_info[0]
    password = user_info[1]
    grabber.account(username, password)
    print("try login")
    if grabber.login():
        print("login success")
    else:
        print("login failed")
        exit()

if grabber.load_course():
    print("course loaded")
else:
    exit()

start_time = datetime.time(12, 55, 0, 0)
end_time = datetime.time(13, 3, 0, 0)
while True:
    current_time = datetime.datetime.now().time()
    print("current time", current_time.strftime('%H:%M:%S'))
    if current_time.__le__(start_time) and grabber.status == STOP:
        grabber.start_grab()
    elif current_time.__le__(end_time) and grabber.status == RUN:
        grabber.pause_grab()
    time.sleep(60)
