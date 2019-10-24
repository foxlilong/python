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

def compare_time(time_str,time_now):
    s_time = time.mktime(time.strptime(time_str,'%Y-%m-%d'))
    e_time = time.mktime(time.strptime(time_now,'%Y-%m-%d'))
    #print 's_time is:',s_time
    #print 'e_time is:',e_time
    return int(s_time) - int(e_time)

#def is_valid_date(strdate):
#    '''判断是否是一个有效的日期字符串'''
#    try:
#        if ":" in strdate:
#            time.strptime(strdate, "%Y-%m-%d %H:%M:%S")
#        else:
#            time.strptime(strdate, "%Y-%m-%d")
#        return True
#    except:
#        return False
        
#def getallfile(path):
#    allfile = []
#    allfilelist=os.listdir(path)
#    for file in allfilelist:
#        filepath=os.path.join(path,file)
#        #判断是不是文件夹
#        if os.path.isfile(filepath):
##            getallfile(filepath)
#            allfile.append(filepath)
#    return allfile
    
def getallfile(path):
#判断文件类型
    allfile = []
    if os.path.isfile(path):
        allfile.append(path)
    elif os.path.isdir(path):
        allfilelist=os.listdir(path)
        for file in allfilelist:
            filepath=os.path.join(path,file)            
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

#处理不包含日志的文件
#转储，清空，压缩
def without_date_zip_files(fname):
    date_str = datetime.date.today()
    os.popen("cp %s %s%s" %(fname, fname, date_str))
    os.popen("echo > %s " %fname)
    os.popen("gzip %s%s " %(fname, date_str))

def file_type(ext_name):
    flag = 0
    file_name, file_ext = os.path.splitext(ext_name)
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
    if flag == 0 :
        return "other"

if __name__=='__main__':
    #path = []
    path =  ["/nginx/logs/halo/"] 
#    path =  ["/nginx/logs/halo/catalina.out"]
    date_reg_exp = re.compile('\d{4}[-]\d{2}[-]\d{2}')
    time_today = time.strftime("%Y-%m-%d",time.localtime())

    for p in path:
        names = getallfile(p)
        for name in names:
        #得到文件名 filename, 不包含路径
            path_name = os.path.basename(name)
            file_name, file_ext = os.path.splitext(path_name)
            match_date = match_date_str(file_name)
            if file_type(name) == "zip":
                if match_date:
                    print("zip 包含日期,name : %s" %name)
                else:
                    print("zip 不包含日期，name : %s" %name)
                    #处理不包含日期文件类型
                   # without_date_files(name)
            elif file_type(name) == "log":
                if match_date:
                    print("文件类型 date log, : %s" %name)
                else:
                    print("文件类型 no date log, : %s" %name)
                    without_date_zip_files(name)
            else:
                print("文件类型 %s, %s" %(file_type(name),name))
        

'''
        for root, dirs, files in os.walk(file_dir):
			names = os.listdir(p)
			#print names;
		for name in names:
			#gzip(name)
			matches_list=date_reg_exp.findall(name)
			if len(matches_list) > 0 :
				print matches_list[0]
			print ("path + name :%s%s "%(p , name))
			if name == "access.log":
				print name;
'''
#                os.system("cp %s%s %s%s%s" %( p , name, p, name, time_today))
#                os.system("echo > " + p + name)
#                os.system("gzip " + p + name + time_today)
			#if is_valid_date(matches_list[0]):
			#   print 1;




