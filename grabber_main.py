from lesson_grabber import Form_data, Grabber
import getpass
import json
from encrypt import *

grabber = Grabber()

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
while True:
    print("Start Grab 1")
    print("Pause Grab 2")
    print("Stop Grab 3")
    a = input("Choose: ")
    if a == "1":
        grabber.start_grab()
    elif a == "2":
        grabber.pause_grab()
    elif a == "3":
        grabber.stop_grab()
        grabber.dump_course()
        break
