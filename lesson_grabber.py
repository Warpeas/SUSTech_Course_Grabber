import requests
import re
import json
from threading import Thread, Lock
import time
from prettytable import PrettyTable

login_url = "https://cas.sustech.edu.cn/cas/login?service=https%3A%2F%2Ftis.sustech.edu.cn%2Fcas"

STOP = 0
RUN = 1


class form_data:
    def __init__(self):
        self.dict = {
            'p_pylx': "1",
            "p_sfgldjr": "0",
            "p_sfredis": "0",
            "p_sfsyxkgwc": "0",
            # 'p_xn': 2020-2021, # 学年
            # 'p_xq': 2,  # 学期
            # 'p_xnxq': 2020-20212, # 学年学期
            # 'p_dqxn': 2020-2021, # 当前学年
            # 'p_dqxq': 2, # 当前学期
            # 'p_dqxnxq': 2020-20212, # 当前学年学期
            # 'p_xkfsdm': 'bxxk', # 选课方式代码
            # 'p_xiaoqu': '', # 校区
            # 'p_kkyx': '', # 开课院系代码
            # 'p_id': '', # 课程id
            'p_sfhlctkc': 0,  # 忽略冲突课程
            'p_sfhllrlkc': 0,  # 忽略零余量课程
            # 'p_kxsj_xqj': '',  # 空闲时间-星期几
            # 'p_kxsj_ksjc': '',  # 空闲时间-开始节次
            # 'p_kxsj_jsjc': '',  # 空闲时间-结束节次
            # 'p_kcdm_js': '', # 课程代码-js
            # 'p_kcdm_cxrw': '', #课程代码-查询
            "p_sfxsgwckb": "1",
            'pageNum': 1,
            'pageSize': 12,
        }
        month = time.localtime().tm_mon
        cYear = time.localtime().tm_year
        xn = ""
        xq = ""
        if month > 8 and month <= 12:
            xq = "1"
            xn = str(cYear)+"-"+str(cYear+1)
        elif month >= 1 and month < 7:
            xq = "2"
            xn = str(cYear-1) + "-" + str(cYear)
        else:
            xq = "3"
            xn = str(cYear-1) + "-" + str(cYear)
        xnxq = xn+xq
        dqxn = xn
        dqxq = xq
        dqxnxq = xnxq
        self.dict['xn'] = xn
        self.dict['xq'] = xq
        self.dict['xnxq'] = xnxq
        self.dict['dqxn'] = dqxn
        self.dict['dqxq'] = dqxq
        self.dict['dqxnxq'] = dqxnxq

    def search(self):
        print("选择课程种类")
        print("通识必修 0")
        print("通识选修 1")
        print("培养方案内 2")
        print("非培养方案 3")
        print("重修选课 4")
        t = input("选择 ")
        if t == "0":
            self.search_course_type("bxxk")
        elif t == "1":
            self.search_course_type("xxxk")
        elif t == "2":
            self.search_course_type("kzyxk")
        elif t == "3":
            self.search_course_type("zynknjxk")
        elif t == "4":
            self.search_course_type("cxxk")
        else:
            self.search_course_type("bxxk")
        name = input("课程名称: ")
        self.search_course_name(name)
        ic = input("忽略冲突课程？y/n ")
        if ic == "y":
            self.search_course_ignore_conflict()
        else:
            self.search_course_no_ignore_conflict()

    def search_course_name(self, name):
        self.dict['p_gjz'] = name

    def search_course_teacher(self, teacher):
        self.dict['p_skjs'] = teacher

    def search_course_type(self, type):
        #   名称    代码
        #   通识必修课  bxxk
        #   通识选修课    xxxk
        #   培养方案内课程    kzyxk
        #   非培养方案内课程    zynknjxk
        #   重修选课    cxxk
        self.dict['p_xkfsdm'] = type

    def search_course_language(self, language):
        # 语言 代码
        # 中文 1
        # 英语 2
        # 双语 3
        # 其他 6
        self.dict['p_skyy'] = language

    def search_course_ignore_conflict(self):
        self.dict['p_sfhlctkc'] = 1

    def search_course_no_ignore_conflict(self):
        self.dict['p_sfhlctkc'] = 0

    def search_course_ignore_full(self):
        self.dict['p_sfhllrlkc'] = 1

    def search_course_no_ignore_full(self):
        self.dict['p_sfhllrlkc'] = 0

    def search_next_page(self):
        self.dict['pageNum'] += 1

    def select_course_name(self, name):
        self.dict['p_gjz'] = name

    def select_course_type(self, type):
        #   名称    代码
        #   通识必修课  bxxk
        #   通识选修课    xxxk
        #   培养方案内课程    kzyxk
        #   非培养方案内课程    zynknjxk
        #   重修选课    cxxk
        self.dict['p_xkfsdm'] = type

    def select_course_id(self, id):
        self.dict['p_id'] = id

    def select_course(self):
        self.dict['p_xktjz'] = 'rwtjzyx'
        # self.dict['p_pylx'] = 1

    @staticmethod
    def parse(course_data, course_type):
        course = form_data()
        course.select_course()
        course.select_course_name(course_data['rwmc'])
        course.select_course_id(course_data['id'])
        course.select_course_type(course_type)
        return course


class grabber:
    def __init__(self):
        self.s = requests.Session()
        self.status = RUN
        self.course_list = []

    def account(self, username, password):
        self.username = username
        self.password = password

    def load_course(self):
        file = open("lesson_list.json", "r")
        self.course_list = json.load(file)
        if len(self.course_list) == 0:
            print("no course")
            return False
        self.lock = Lock()
        self.lock.acquire()
        self.grab_thread = Thread(target=grab_thread, args=(self,))
        self.grab_thread.setDaemon(True)
        self.grab_thread.start()
        return True

    def dump_course(self):
        json.dump(obj=self.course_list, ensure_ascii=False,
                  fp=open("lesson_list.json", "w"))

    def login(self):
        try:
            r = self.s.get(url=login_url, timeout=5)
        except:
            return False
        if len(re.findall('on" value="(.+?)"', r.text)) == 0:
            return

        data = {
            'username': self.username,
            'password': self.password,
            '_eventId': 'submit',
            'geolocation': ''
        }
        data['execution'] = re.findall('on" value="(.+?)"', r.text)[0]
        # 登录
        try:
            r = self.s.post(url=login_url, data=data)
        except:
            return False
        return True

    def search(self, query_data):
        print(query_data)
        # r = self.s.get('https://tis.sustech.edu.cn/Xsxk/query/1')
        r = self.s.post(
            'https://tis.sustech.edu.cn/Xsxk/queryKxrw', query_data)
        print(r.text)
        query_json = r.json()
        print(query_json)
        js = json.dumps(query_json['yxkcList'],
                        indent=4, separators=(',', ':'))
        header = 'name teacher time'.split(' ')
        row = []
        ids = []
        for course in query_json["kxrwList"]["list"]:
            row.append([course["rwmc"], course["dgjsmc"], course["pkjgmx"]])
            ids.append(course["id"])
        pt = PrettyTable()
        pt._set_field_names(header)
        pt.add_row(row=row)

        print(js)

    def start_grab(self):
        self.lock.release()

    def pause_grab(self):
        self.lock.acquire()

    def stop_grab(self):
        self.status = STOP
        try:
            self.lock.release()
        except:
            return


def grab_thread(grabber: grabber):
    while grabber.status == RUN:
        if len(grabber.course_list) == 0:
            return

        # try:
        #     grabber.login()
        # except:
        #     print("login failed, retrying")
        #     continue

        grabber.lock.acquire()
        for course in grabber.course_list:
            print("正在尝试抢", course["课程名称"])
            try:
                r = grabber.s.post(
                    'https://tis.sustech.edu.cn/Xsxk/addGouwuche', course)
            except:
                continue
            else:
                # TODO: Handle login time exceed
                response = r.json()
                print(response['message'], response['jg'])
                if response['jg'] == "1":
                    print("抢到", course["课程名称"])
                    grabber.course_list.remove(course)
        grabber.lock.release()
        time.sleep(1)
