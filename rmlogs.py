#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
功能描述:
输入需要操作的日志目录
    如果文件名包含日期，仅进行压缩gzip
    如果文件名是catalina.out,进行分割,并仅进行压缩gzip
    其他文件忽略，不操作
"""
import re, os, time
import datetime


def gzip(name):
    fname = name
    os.popen("echo > " + fname)
    os.popen("cp " + fname + " " + fname + datetime.date.today())
    os.popen("gzip" + fname)


def compare_time(time_str, time_now):
    s_time = time.mktime(time.strptime(time_str, '%Y-%m-%d'))
    e_time = time.mktime(time.strptime(time_now, '%Y-%m-%d'))
    # print 's_time is:',s_time
    # print 'e_time is:',e_time
    return int(s_time) - int(e_time)

def getallfile(path):
    # 判断文件类型，返回当先文件夹
    allfile = []
    if os.path.isfile(path):
        allfile.append(path)
    elif os.path.isdir(path):
        allfilelist = os.listdir(path)
        for file in allfilelist:
            filepath = os.path.join(path, file)
            if os.path.isfile(filepath):
                allfile.append(filepath)
    return allfile


def match_date_str(str):
    date_reg_exp = re.compile('\d{4}[-]\d{2}[-]\d{2}')
    result = date_reg_exp.findall(str)
    if len(result) == 0:
        return False
    else:
        return True


# 处理日志文件的方法
# 转储，清空，压缩
def log_date_files(fname):
    # 包含log 和 日期的文件
    os.popen("gzip %s%s " % (fname, date_str))


def log_only_files(fname):
    # 仅包含log的文件
    date_str = datetime.date.today()
    os.popen("cp %s %s%s" % (fname, fname, date_str))
    os.popen("echo > %s " % fname)
    os.popen("gzip %s%s " % (fname, date_str))


def zip_date_files(fname):
    # 包含压缩 和 日期的文件
    pass


def zip_only_files(fname):
    # 仅包含压缩的文件
    pass


def file_type(ext_name):
    flag = 0
    #file_name, file_ext = os.path.splitext(ext_name)
    file_ext = ext_name.split(".")[-1]
    zip_list = ["zip", "gz", "rar", "tar"]
    log_list = ["log", "txt", "out"]

    for i in log_list:
        if i == file_ext:
            flag = 1
            return "log"

    for j in zip_list:
        if j == file_ext:
            flag = 1
            return "zip"
    if flag == 0:
        return "other"


if __name__ == '__main__':
    # path = []
    path = ["/nginx/logs/"]
    #    path =  ["/nginx/logs/halo/catalina.out"]
    date_reg_exp = re.compile('\d{4}[-]\d{2}[-]\d{2}')
    time_today = time.strftime("%Y-%m-%d", time.localtime())

    for p in path:
        names = getallfile(p)
        for name in names:
            # 得到文件名 filename, 不包含路径
            path_name = os.path.basename(name)
            file_name, file_ext = os.path.splitext(path_name)
            match_date = match_date_str(file_name)
            if file_type(name) == "log":
                if match_date:
                    # 包含log 和 日期的文件
                    print("文件类型\t日志文件\t包含LOG和日期\t:\t%s" % name)
                    log_date_files(name)
                else:
                    # 仅包含log的文件
                    print("文件类型\t日志文件\t仅包含LOG\t:\t%s" % name)
                    log_only_files(name)
            elif file_type(name) == "zip":
                if match_date:
                    # 包含压缩 和 日期的文件
                    print("文件类型\t压缩文件\t包含ZIP\t:\t%s" % name)
                else:
                    # 仅包含压缩的文件
                    print("文件类型\t压缩文件\t仅包含压缩后缀\t:\t%s" % name)
            else:
                # 忽略其他文件类型
                print("文件类型\tother\t仅包含压缩后缀\t:\t%s" % name)
