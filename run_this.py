import shutil
import traceback
import zipfile
from time import sleep

import requests
import json
import os
import winreg

def get_data_from_cookie(Cookie,path_base):
    path = path_base + "/data/"

    if not os.path.exists(path):
        os.mkdir(path)

    # 自由选课
    post_header = {'Host': 'jwcxk2.aufe.edu.cn', 'Connection': 'keep-alive', 'Content-Length': '27', 'Accept': '*/*',
                   'X-Requested-With': 'XMLHttpRequest',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Origin': 'http://jwcxk2.aufe.edu.cn',
                   'Referer': 'http://jwcxk2.aufe.edu.cn/student/courseSelect/freeCourse/index?fajhh=4092',
                   'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', "Cookie": Cookie}
    post_data = {'searchtj': '',
                 'xq': '0',
                 'jc': '0',
                 'kclbdm': ''}
    url = "http://jwcxk2.aufe.edu.cn/student/courseSelect/freeCourse/courseList"
    text_url = requests.post(url, headers=post_header, data=post_data).json()
    with open("{}自由选课.json".format(path), "w", encoding='utf-8') as f:
        json.dump(text_url, f)
        print_way_1("自由选课.json保存文件完成...")
        f.close()
    # 选课结果
    post_header = {'Host': 'jwcxk2.aufe.edu.cn', 'Connection': 'keep-alive', 'Accept': '*/*',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest',
                   'Referer': 'http://jwcxk2.aufe.edu.cn/student/courseSelect/courseSelectResult/index',
                   'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', "Cookie": Cookie}
    url = "http://jwcxk2.aufe.edu.cn/student/courseSelect/thisSemesterCurriculum/callback"
    text_url = requests.get(url, headers=post_header).json()
    with open("{}选课结果.json".format(path), "w", encoding='utf-8') as f:
        json.dump(text_url, f)
        print_way_1("选课结果.json保存文件完成...")
        f.close()
    sleep(5)
    # 培养方案完成情况
    post_header = {'Host': 'jwcxk2.aufe.edu.cn', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                   'Referer': 'http://jwcxk2.aufe.edu.cn/student/integratedQuery/planCompletion/index',
                   'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', "Cookie": Cookie}
    url = "http://jwcxk2.aufe.edu.cn/student/integratedQuery/planCompletion/index"

    text_url = requests.get(url, headers=post_header).text
    pyfa = text_url.split('var zNodes = ')[1].split(";\r\n\t$(document).ready(function() {\r\n\t\tconsole.log(zNodes)")[0]
    pyfa = json.loads(pyfa)
    with open("{}培养方案完成情况.json".format(path), "w", encoding='utf-8') as f:
        json.dump(pyfa, f)
        print_way_1("培养方案完成情况.json保存文件完成...")
        f.close()
    # 方案成绩
    post_header = {'Host': 'jwcxk2.aufe.edu.cn', 'Connection': 'keep-alive', 'Accept': '*/*',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                   'X-Requested-With': 'XMLHttpRequest',
                   'Referer': 'http://jwcxk2.aufe.edu.cn/student/integratedQuery/scoreQuery/schemeScores/index',
                   'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', "Cookie": Cookie}
    url = "http://jwcxk2.aufe.edu.cn/student/integratedQuery/scoreQuery/schemeScores/callback"

    text_url = requests.get(url, headers=post_header).json()
    with open("{}方案成绩.json".format(path), "w", encoding='utf-8') as f:
        json.dump(text_url, f)
        print_way_1("方案成绩.json保存文件完成...")
        f.close()
    # 学籍信息
    post_header = {'Host': 'jwcxk2.aufe.edu.cn', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                   'Referer': 'http://jwcxk2.aufe.edu.cn/student/integratedQuery/scoreQuery/schemeScores/index',
                   'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', "Cookie": Cookie}
    url = "http://jwcxk2.aufe.edu.cn/student/rollManagement/rollInfo/index"
    zp_url = "http://jwcxk2.aufe.edu.cn/student/rollInfo/img"

    image = requests.get(zp_url, headers=post_header)
    with open("{}image.jpg".format(path), 'wb') as f:
        f.write(image.content)
        print_way_1("image.jpg保存文件完成...")
        f.close()

    text_url = requests.get(url, headers=post_header).text
    with open("{}学籍信息.html".format(path), "w", encoding='utf-8') as f:
        f.write(text_url)
        print_way_1("学籍信息.html保存文件完成...")
        f.close()

def process_data_from_json(path_base):
    path_r = path_base + "/data/"
    path_w = path_base + "/Processing_data/"

    if not os.path.exists(path_w):
        os.mkdir(path_w)

    with open("{}培养方案完成情况.json".format(path_r), 'r') as load_f:
        pyfa = json.load(load_f)
        load_f.close()
    peiyangfanan_list = []
    for i in pyfa:
        if "]" in i["name"].split(" &nbsp;")[1]:
            if "))" not in i["name"].split(" &nbsp;")[1]:
                # [PDA1131001]马克思主义基本原理概论
                id_0 = "id:" + i["id"] + "#"
                kcm = "课程名:" + i["name"].split(" &nbsp;")[1].split("]")[1].split("[")[0] + "#"
                temp = id_0 + "课程序号:" + i["flagId"] + "#" + "flagType:" + i["flagType"] + "#" + kcm
            else:
                # [PDA1131004]中国近现代史纲要[3学分](必修,87.0(20190627))
                id_0 = "id:" + i["id"] + "#"
                kcm = "课程名:" + i["name"].split(" &nbsp;")[1].split("]")[1].split("[")[0] + "#"
                xf = "学分:" + i["name"].split(" &nbsp;")[1].split("]")[1].split("[")[1].split("学分")[0] + "#"
                fs = "分数:" + i["name"].split(" &nbsp;")[1].split(",")[1].split("(")[0] + "#"
                rq = "日期:" + i["name"].split(" &nbsp;")[1].split("(")[2].split("))")[0] + "#"
                temp = id_0 + "课程序号:" + i["flagId"] + "#" + "flagType:" + i["flagType"] + "#" + kcm + xf + fs + rq
        else:
            # 分类教育(最低修读学分:15,通过学分:0.0,已修课程门数:0,已及格课程门数:0,未及格课程门数:0,必修课缺修门数:0)
            # 'id': '11'
            id_0 = "id:" + i["id"] + "#"
            lbmc = "类别名称:" + i["name"].split(" &nbsp;")[1].split("(")[0] + "#"
            zdxdxf = "最低修读学分:" + i["name"].split(" &nbsp;")[1].split("最低修读学分:")[1].split(",")[0] + "#"
            tgxf = "通过学分:" + i["name"].split(" &nbsp;")[1].split("通过学分:")[1].split(",")[0] + "#"
            yxkcms = "已修课程门数:" + i["name"].split(" &nbsp;")[1].split("已修课程门数:")[1].split(",")[0] + "#"
            yjgkcms = "已及格课程门数:" + i["name"].split(" &nbsp;")[1].split("已及格课程门数:")[1].split(",")[0] + "#"
            wjgkcms = "未及格课程门数:" + i["name"].split(" &nbsp;")[1].split("未及格课程门数:")[1].split(",")[0] + "#"
            bxkqxms = "必修课缺修门数:" + i["name"].split(" &nbsp;")[1].split("必修课缺修门数:")[1].split(")")[0] + "#"
            temp = id_0 + "flagId:" + i["flagId"] + "#" + "flagType:" + i[
                "flagType"] + "#" + lbmc + zdxdxf + tgxf + yxkcms + yjgkcms + wjgkcms + bxkqxms
        peiyangfanan_list.append(temp)

    with open("{}培养方案数据.txt".format(path_w), "w", encoding="utf-8") as f:
        for i in peiyangfanan_list:
            f.write(i)
            f.write("\n")
        print_way_1("培养方案数据.txt保存文件完成...")
        f.close()
    with open("{}方案成绩.json".format(path_r), 'r') as load_f:
        facj = json.load(load_f)
        load_f.close()
    with open("{}学生方案情况.txt".format(path_w), "w", encoding="utf-8")as f:
        for i in facj:
            xuehao = "学号:" + str(i["cjList"][0]["id"]["studentId"]) + "#"
            banji = "班级:" + str(i["cjList"][0]["classNo"]) + "#"
            yxxf = "已修读课程总学分:" + str(i["yxxf"]) + "#"
            zms = "已修读课程门数:" + str(i["zms"]) + "#"
            tgms = "通过课程门数:" + str(i["tgms"]) + "#"
            cjbh = "培养方案代号:" + str(i["cjbh"]) + "#"
            cjlx = "培养方案名称:" + str(i["cjlx"]) + "#"
            temp_str = xuehao + banji + cjlx + cjbh + yxxf + zms + tgms
            # print_way_1(temp_str)
            f.write(temp_str)
            f.write("\n")
        print_way_1("学生方案情况.txt保存文件完成...")
        f.close()

    with open("{}方案成绩.json".format(path_r), 'r') as load_f:
        facj = json.load(load_f)
        load_f.close()
    with open("{}学生方案成绩情况.txt".format(path_w), "w", encoding="utf-8")as f:
        for i in facj:
            for o in i["cjList"]:
                courseNumber = "课程号:" + str(o['id']['courseNumber']) + "#"
                coureSequenceNumber = "课序号:" + str(o["id"]["coureSequenceNumber"]) + "#"
                courseName = "课程名称:" + str(o['courseName']) + "#"
                courseAttributeName = "课程属性:" + str(o['courseAttributeName']) + "#"
                credit = "学分:" + str(o['credit']) + "#"
                cj = "成绩:" + str(o['cj']) + "#"
                englishCourseName = "英文课程名:" + str("".join(o['englishCourseName'].split("\r\n"))) + "#"
                temp_str = courseNumber + coureSequenceNumber + courseName + courseAttributeName + credit + cj + englishCourseName
                # print_way_1(temp_str)
                f.write(temp_str)
                f.write("\n")
        print_way_1("学生方案成绩情况.txt保存文件完成...")
        f.close()
    with open("{}自由选课.json".format(path_r), 'r') as f:
        zyxk = json.load(f)
        f.close()
    rwRxkZlList = json.loads(zyxk["rwRxkZlList"])
    with open("{}自由选课数据.txt".format(path_w), "w", encoding="utf-8")as f:
        for i in rwRxkZlList:
            kcm = "课程名:" + str(i["kcm"]) + "#"
            kch = "课程号:" + str(i["kch"]) + "#"
            kxh = "课序号:" + str(i["kxh"]) + "#"

            xf = "学分:" + str(i["xf"]) + "#"
            skjs = "上课教师:" + str(i["skjs"]) + "#"
            kslxmc = "考试类型:" + str(i["kslxmc"]) + "#"
            kkxsjc = "开课院系:" + str(i["kkxsjc"]) + "#"

            shangkedeshumue = "一周上课的次数:" + str(len(i["sjdd"])) + "#"
            skxq = "0_星期几上课:" + str(i["sjdd"][0]["skxq"]) + "#"
            skjc = "0_第几节课:" + str(i["sjdd"][0]["skjc"]) + "#"
            skzc = "0_上课的周:" + str(i["sjdd"][0]["skzc"]) + "#"
            cxjc = "0_上课持续的时间节:" + str(i["sjdd"][0]["cxjc"]) + "#"

            if len(i["sjdd"]) > 1:
                for o in range(1, len(i["sjdd"])):
                    skxq += str(o) + "_星期几上课:" + str(i["sjdd"][o]["skxq"]) + "#"
                    skjc += str(o) + "_第几节课:" + str(i["sjdd"][o]["skjc"]) + "#"
                    skzc += str(o) + "_上课的周:" + str(i["sjdd"][o]["skzc"]) + "#"
                    cxjc += str(o) + "_上课持续的时间节:" + str(i["sjdd"][o]["cxjc"]) + "#"

            bkskrl = "课程容量:" + str(i["bkskrl"]) + "#"
            bkskyl = "容量剩余:" + str(i["bkskyl"]) + "#"

            zxjxjhh = "教学计划年份:" + str(i["zxjxjhh"]) + "#"

            temp_str = kcm + kch + kxh + xf + skjs + bkskrl + bkskyl + kslxmc + kkxsjc + zxjxjhh \
                       + shangkedeshumue + skxq + skjc + skzc + cxjc
            # print_way_1(temp_str)
            f.write(temp_str)
            f.write("\n")
        print_way_1("自由选课数据.txt保存文件完成...")
        f.close()
    with open("{}自由选课.json".format(path_r), 'r') as f:
        zyxk = json.load(f)
        f.close()
    yxkclist = json.loads(zyxk["yxkclist"])
    with open("{}选课结果数据.txt".format(path_w), "w", encoding="utf-8")as f:
        for i in yxkclist:
            attendClassTeacher = "教师:" + str(i["attendClassTeacher"]) + "#"
            courseName = "课程名称:" + str(i["courseName"]) + "#"
            examTypeName = "考试类型:" + str(i["examTypeName"]) + "#"
            coureNumber = "课程号:" + str(i["id"]["coureNumber"]) + "#"
            coureSequenceNumber = "课序号:" + str(i["id"]["coureSequenceNumber"]) + "#"
            unit = "学分:" + str(i["unit"]) + "#"
            coursePropertiesName = "课程属性:" + str(i["coursePropertiesName"]) + "#"
            selectCourseStatusName = "选课状态:" + str(i["selectCourseStatusName"]) + "#"

            executiveEducationPlanNumber = "0_教学计划年份:" + str(
                i["timeAndPlaceList"][0]["executiveEducationPlanNumber"]) + "#"

            shangkedeshumue = "一周上课的次数:" + str(len(i["timeAndPlaceList"])) + "#"

            classDay = "0_星期几上课:" + str(i["timeAndPlaceList"][0]["classDay"]) + "#"
            classSessions = "0_第几节课:" + str(i["timeAndPlaceList"][0]["classSessions"]) + "#"
            classWeek = "0_上课的周:" + str(i["timeAndPlaceList"][0]["classWeek"]) + "#"
            continuingSession = "0_上课持续的时间节:" + str(i["timeAndPlaceList"][0]["continuingSession"]) + "#"

            if len(i["timeAndPlaceList"]) > 1:
                for o in range(1, len(i["timeAndPlaceList"])):
                    classDay += str(o) + "_星期几上课:" + str(i["timeAndPlaceList"][o]["classDay"]) + "#"
                    classSessions += str(o) + "_第几节课:" + str(i["timeAndPlaceList"][o]["classSessions"]) + "#"
                    classWeek += str(o) + "_上课的周:" + str(i["timeAndPlaceList"][o]["classWeek"]) + "#"
                    continuingSession += str(o) + "_上课持续的时间节:" + str(
                        i["timeAndPlaceList"][o]["continuingSession"]) + "#"

            temp_str = courseName + attendClassTeacher + examTypeName \
                       + coureNumber + coureSequenceNumber + unit \
                       + coursePropertiesName + selectCourseStatusName + executiveEducationPlanNumber \
                       + shangkedeshumue + classDay + classSessions + continuingSession + classWeek
            # print_way_1(temp_str)
            f.write(temp_str)
            f.write("\n")
        print_way_1("选课结果数据.txt保存文件完成...")
        f.close()
    with open("{}选课结果.json".format(path_r), 'r') as load_f:
        xkjg = json.load(load_f)
        load_f.close()
    dateList = xkjg["dateList"][0]
    with open("{}本学期信息数据.txt".format(path_w), "w", encoding="utf-8")as f:
        programPlanName = "培养方案名称:" + str(dateList["programPlanName"]) + "#"  # 培养方案名称
        programPlanCode = "培养方案代号:" + str(dateList["programPlanCode"]) + "#"  # 培养方案代号
        totalUnits = "本学期已经选课的学分:" + str(dateList["totalUnits"]) + "#"  # 已经选课的学分
        temp_str = programPlanName + programPlanCode + totalUnits
        # print_way_1(temp_str)
        f.write(temp_str)
        f.write("\n")
        print_way_1("本学期信息数据.txt保存文件完成...")
        f.close()

def request_test(Cookie_test):
    # 培养方案完成情况
    post_header_test = {'Host': 'jwcxk2.aufe.edu.cn', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'Referer': 'http://jwcxk2.aufe.edu.cn/student/integratedQuery/planCompletion/index',
                        'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9',
                        "Cookie": str(Cookie_test)}
    url_test = "http://jwcxk2.aufe.edu.cn/student/integratedQuery/planCompletion/index"

    try:
        text_url = requests.get(url_test, headers=post_header_test)

        if "忘记密码了" in text_url.text:
            return 1
    except requests.exceptions.ContentDecodingError:
        return 1
    except requests.exceptions.ConnectionError:
        return 2
    except:
        traceback.print_exc(file=open("xxxxxxxxx.txt", "w"))
        return 3
    return 4

def print_way_1(temp):
    print(temp)

def get_cookie_temp():
    print_way_1("请填写登录后的 cookie:(复制粘贴到此处)")
    cookie = input()
    return cookie

# 获取登录信息 Cookie
def first_get_cookie(path_base):
    print_way_1("请连接 vpn 登录教务处,并填写登录后的 cookie")
    print_way_1("获取 cookie 不会的可以参照下面的链接:")
    print_way_1("https://jingyan.baidu.com/article/48a420571d8770a924250496.html")
    print_way_1("形如：")
    print_way_1("JSESSIONID=abcsOddTd0s4U4BddMZmx; selectionBar=1445673")
    print_way_1("请填写登录后的 cookie:(复制粘贴到此处)")
    cookie = input()
    # print(cookie)

    print_way_1('请耐心等待，大约20s')
    t = request_test(cookie)
    # print(t)
    if t == 1:
        os.system("cls")
        print_way_1("请填写符合规定 且 正确的cookie")
        first_get_cookie(path_base)
    elif t == 2:
        os.system("cls")
        print_way_1("请连接 vpn ,或者等待vpn连接稳定后按回车键继续")
        first_get_cookie(path_base)
    elif t == 3:
        os.system("cls")
        print_way_1("遇到未知错误,请联系作者，或者关闭软件，重启电脑后重试")
        os.system("pause")
    elif t == 4:
        print_way_1("cookie 填写正确")
        with open("{}\cookie.txt".format(path_base), "w", encoding="utf-8")as f:
            f.write(str(cookie))
            f.close()

def makdir_base_path():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    path_base = '{}\教务处选课系统'.format(winreg.QueryValueEx(key, "Desktop")[0])
    if not os.path.exists(path_base):
        os.mkdir(path_base)
    return path_base

def zip_ya(startdir):
    startdir = startdir  #要压缩的文件夹路径
    file_news = startdir.split("教务处选课系统")[0] +'教务处选课系统.zip' # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir,'') #这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''#这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename),fpath+filename)
    z.close()

def get_tjxk_txt_to_path(path):
    path_base = path

    with open("{}/Processing_data/培养方案数据.txt".format(path_base), "r", encoding="utf-8")as f:
        pyfasj = f.readlines()
        f.close()

    with open("{}/Processing_data/自由选课数据.txt".format(path_base), "r", encoding="utf-8")as f:
        zyxksj = f.readlines()
        f.close()

    # 规避已选课程的上课时间
    with open("{}/Processing_data/选课结果数据.txt".format(path_base), "r", encoding="utf-8")as f:
        xkjgsj = f.readlines()
        f.close()

    flag = 0
    kcz = ""
    kch_xuyao_map = {}
    for i in pyfasj:
        if "#flagType:001" in i or "#flagType:002" in i:
            flag = 0
        if flag == 1 and "日期:" not in i:
            try:
                kch_xuyao_map[kcz].append(i)
            except:
                kch_xuyao_map[kcz] = [i]
        if "最低修读学分:" in i and "flagType:002" in i:
            flag = 0
            tgxf = float(i.split("通过学分:")[1].split("#")[0])
            zdxdxf = float(i.split("最低修读学分:")[1].split("#")[0])
            if tgxf < zdxdxf or (zdxdxf == 0 and tgxf < 1):
                flag = 1
                kcz = i
            else:
                kcz = ""
                flag = 0
    # print(len(kch_kexuan_map))
    # print(kch_kexuan_map)

    kch_kexuan_map = {}
    for i in kch_xuyao_map:
        # print(i.split("\n")[0])
        temp_kexuan_list = []
        for o in kch_xuyao_map[i]:
            temp_kexuan_list.append(str(o.split("课程序号:")[1].split("#")[0]))
            # print("\t",o.split("\n")[0])
        for kch in temp_kexuan_list:
            for kc in zyxksj:
                if kch in kc:
                    try:
                        kch_kexuan_map[i].append(kc.split("\n")[0])
                    except:
                        kch_kexuan_map[i] = [kc.split("\n")[0]]
                    # print(kc.split("\n")[0])

    # print(len(kch_kexuan_map))
    # print(kch_kexuan_map)

    # 一周上课的次数:1#0_星期几上课:3#0_第几节课:1#0_上课的周:111111111111111111000000#0_上课持续的时间节:2#
    def zyxk_kch_to_sjxl(kc):
        temp_str = [["0" * 10 * 7] * 24][0]
        for i in [kc]:
            yzskcs_len = int(i.split("一周上课的次数:")[1].split("#")[0])
            ##一周上课的次数:1#0_星期几上课:3#0_第几节课:1#0_上课的周:111111111111111111000000#0_上课持续的时间节:2#
            for o in range(yzskcs_len):
                num = -1
                skdz_str_list = list(str(i.split("{}_上课的周:".format(o))[1].split("#")[0]))
                for skdz in skdz_str_list:
                    num += 1
                    # print(num)
                    if skdz == "1":
                        xqjsk = int(i.split("{}_星期几上课:".format(o))[1].split("#")[0])
                        djjk = int(i.split("{}_第几节课:".format(o))[1].split("#")[0])
                        skcxsj = int(i.split("{}_上课持续的时间节:".format(o))[1].split("#")[0])
                        temp_str[num] = temp_str_he_bin(temp_str[num], week_to_sjxl(xqjsk, djjk, skcxsj))
                    # print(temp_str)
        return "".join(temp_str)

    def week_to_sjxl(xqjsk_t, djjk_t, skcxsj_t):
        temp_str = list("0" * 10 * 7)
        xqjsk = int(xqjsk_t) - 1
        djjk = int(djjk_t) - 1
        skcxsj = int(skcxsj_t)
        for i in range(skcxsj):
            temp_str[(xqjsk * 10 + djjk + i)] = "1"
        return "".join(temp_str)

    def temp_str_he_bin(str1, str2):
        temp_str = list(str1)
        num = -1
        for i in str2:
            num += 1
            if i == "1":
                temp_str[num] = "1"
        return "".join(temp_str)

    def xkjgsj_to_sjxl_week_list(xkjgsj):
        temp_str = [["0" * 10 * 7] * 24][0]
        for i in xkjgsj:
            yzskcs_len = int(i.split("一周上课的次数:")[1].split("#")[0])
            ##一周上课的次数:1#0_星期几上课:3#0_第几节课:1#0_上课的周:111111111111111111000000#0_上课持续的时间节:2#
            for o in range(yzskcs_len):
                num = -1
                skdz_str_list = list(str(i.split("{}_上课的周:".format(o))[1].split("#")[0]))
                for skdz in skdz_str_list:
                    num += 1
                    # print(num)
                    if skdz == "1":
                        xqjsk = int(i.split("{}_星期几上课:".format(o))[1].split("#")[0])
                        djjk = int(i.split("{}_第几节课:".format(o))[1].split("#")[0])
                        skcxsj = int(i.split("{}_上课持续的时间节:".format(o))[1].split("#")[0])
                        temp_str[num] = temp_str_he_bin(temp_str[num], week_to_sjxl(xqjsk, djjk, skcxsj))
                    # print(temp_str)
        return "".join(temp_str)

    xksjxl = xkjgsj_to_sjxl_week_list(xkjgsj)

    def kch_sjxl_in_xksjxl(kch_sjxl, xksjxl):
        temp_sjxl = list(kch_sjxl)
        num = -1
        for i in xksjxl:
            num += 1
            if temp_sjxl[num] == "1" and i == "1":
                return True
        return False

    with open("{}/推荐选的课.txt".format(path_base), "w", encoding="utf-8")as f:
        shi_jian_yun_xu_kch = []
        for i in kch_kexuan_map:
            # print(i.split("\n")[0])
            f.write(i.split("\n")[0])
            f.write("\n")
            for o in kch_kexuan_map[i]:
                if not kch_sjxl_in_xksjxl(zyxk_kch_to_sjxl(o), xksjxl):
                    # print("\t",o.split("#开课院系:")[0])
                    f.write("\t" + o.split("#开课院系:")[0])
                    f.write("\n")
        print("没有余量推荐选的课.txt 已经完成")
        f.close()

    with open("{}/有课程余量推荐选的课.txt".format(path_base), "w", encoding="utf-8")as f:
        shi_jian_yun_xu_kch = []
        for i in kch_kexuan_map:
            # print(i.split("\n")[0])
            f.write(i.split("\n")[0])
            f.write("\n")
            for o in kch_kexuan_map[i]:
                if not kch_sjxl_in_xksjxl(zyxk_kch_to_sjxl(o), xksjxl):
                    # kcrl = int(o.split("课程容量:")[1].split("#")[0])
                    rlsy = int(o.split("容量剩余:")[1].split("#")[0])
                    # print("\t",o.split("#开课院系:")[0])
                    if rlsy > 0:
                        f.write("\t" + o.split("#开课院系:")[0])
                        f.write("\n")
        print("有课程余量推荐选的课.txt 已经完成")
        f.close()

path_base = makdir_base_path()

try:
    first_get_cookie(path_base)
    with open("{}\cookie.txt".format(path_base), "r", encoding="utf-8")as f:
        Cookie = f.readline()
        f.close()
    get_data_from_cookie(Cookie,path_base)
    # 处理数据
    try:
        process_data_from_json(path_base)
        print_way_1("获取和处理数据已经完成\n")
    except:
        print_way_1("！！！处理文件时发生了异常，请联系作者，并将{}处的压缩包附带发送".format(path_base))
        print_way_1("！！！此软件的作者：wp\nQQ：983214439")
        zip_ya(path_base)
        os.system("pause")

    # 生成推荐课程
    try:
        os.system("cls")
        print_way_1("---------")
        print_way_1("| 此软件的作者：wp\n| QQ：983214439")
        print_way_1("| 这个版本的选课推荐是按照没有修满的课程组，再根据时间是否有冲突分成 有课程余量推荐选的课 和 推荐选的课")
        print_way_1("| 选课的时候如果不退现在已经选的课，请按照目录下 有课程余量推荐选的课 进教务系统进行选课")
        print_way_1("| 此软件暂不提供自动选课功能，需要你手动根据上面提到的步骤进行选课")
        print_way_1("---------")
        get_tjxk_txt_to_path(path_base)
        zip_ya(path_base)
        print_way_1("\n教务处选课系统，已经完成，请查看{}文件夹\n".format(path_base))
        print_way_1("感谢你的使用，敬请期待新的功能")
        os.system("pause")
    except:
        print_way_1("！！！生成推荐课程时发生了异常，请联系作者，并将{}处的压缩包附带发送".format(path_base))
        print_way_1("！！！此软件的作者：wp\nQQ：983214439")
        zip_ya(path_base)
        os.system("pause")

except:
    traceback.print_exc(file=open("{}/log.txt".format(path_base), "a+"))
    print_way_1("！！！处理文件时发生了异常，请联系作者，并将{}处的压缩包附带发送".format(path_base))
    print_way_1("！！！此软件的作者：wp\nQQ：983214439")
    zip_ya(path_base)
    os.system("pause")
#pyinstaller -F -i jwc.ico run_this.py