from lesson_grabber import form_data, grabber
import getpass
import json
from encrypt import *
import time

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

# 首先构筑搜索信息包
search_form = form_data()
control = ""
while True:
    # 新搜索
    search_form.construct_search_form()

    while True:
        # 搜索请求
        total_num, lessons = grabber.search(search_form.dict)
        print("previous page P --", search_form.current_pageNum(), "-- next page N")
        print("add course to grabber list #idx")
        print("new search S")
        print("exit E")
        control = input("input command: ").lower()
        if control.isdigit():
            lesson = lessons[int(control)]
            if lesson not in grabber.course_list:
                grabber.course_list.append(lessons[int(control)])
        elif control == "s":
            break
        elif control == "n":
            if search_form.current_pageNum() * search_form.current_pageSize() < total_num:
                search_form.search_next_page()
            else:
                print("last page")
                time.sleep(0.1)
        elif control == "p":
            search_form.search_previous_page()
        elif control == "e":
            break
        else:
            print("Invalid command")

    if control == "e":
        break

print(grabber.course_list)
grabber.dump_course()
print("course list saved, exiting")
