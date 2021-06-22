from lesson_grabber import form_data, grabber, STOP, RUN, READY
import getpass
import json
import datetime
import time
from encrypt import *
from threading import Thread


def auto_control():
    start_time = datetime.time(12, 57, 0, 0)
    end_time = datetime.time(13, 3, 0, 0)
    while not grabber.is_end():
        current_time = datetime.datetime.now().time()
        if current_time > start_time and current_time < end_time and grabber.status != RUN:
            grabber.start_grab()
        elif current_time > end_time and grabber.status != STOP:
            grabber.pause_grab()
        else:
            # print("current time", current_time.strftime('%H:%M:%S'))
            time.sleep(60)


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
    print("course loaded, you can also add new courses by search")
else:
    print("no course in list, please start search")

auto_controller = Thread(target=auto_control)
auto_controller.setDaemon(True)
auto_controller.start()

# 首先构筑搜索信息包
search_form = form_data()
control = ""
search_form.construct_search_package()

while True:
    # 搜索请求
    total_num, lessons = grabber.search(search_form.dict)
    print("previous page P --|",
          search_form.current_pageNum(), "|-- next page N")
    print("#"*40)
    print("add course to grabber's course list #idx")
    print("new search S | grabber status G | exit E")
    control = input("input command: ").lower()
    if control.isdigit():
        lesson = lessons[int(control)]
        if lesson not in grabber.course_list:
            if grabber.is_end():
                grabber.ready_grab()
            grabber.course_list.append(lessons[int(control)])
    elif control == "s":
        search_form.new_search()
    elif control == "n":
        if search_form.current_pageNum() * search_form.current_pageSize() < total_num:
            search_form.search_next_page()
        else:
            print("last page")
            time.sleep(0.1)
    elif control == "p":
        search_form.search_previous_page()
    elif control == "e":
        grabber.dump_course()
        print("course list saved, exiting")
        exit(0)
    elif control == "g":
        if grabber.is_end():
            print("no course in list, grabber is stopped")
        else:
            while True:
                grabber.print_course_list()
                control = input("do you want to remove course? #/n: ")
                if control.isdigit() and int(control) < len(grabber.course_list):
                    grabber.course_list.remove(int(control))
                else:
                    break
    else:
        print("Invalid command")
