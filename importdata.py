#!/bin/python
#coding=utf-8

import pymysql
import sys

# 使用方法：
# python3 importdata.py filename
# filename为要导入的文件名称，importdata.py为脚本名称
# 注意：需要 pip3 install pymysql 安装pymsql库 
# Auther:qitan


# 请输入的相关信息
host = ""
user = ""
password = "" 
database = ""
table = ""
selectziduan = [] # 请输入要导入的列，例如[1,2,5]表示仅仅导入第1列、第2列和第5列数据；默认为全部字段数据

# 连接数据库
def dbCon():
    if not host or not user or not password or not database:
        print('请打开脚本，输入要导入的数据库信息！')
    db = pymysql.connect(host,user,password,database)
    db.set_charset('utf8')
    return db
  
# 获取要导入的字段
def getZiduan():
    db = dbCon()
    dbc = db.cursor()
    dbc.execute("desc {};".format(table))
    zdlist = dbc.fetchall()
    global selectziduan

    if not selectziduan:
        selectziduan = list(range(1,len(zdlist)+1))
    
    ziduan = ''
    j = 0
    
    for i in range(len(selectziduan)):
        j += 1
        if j != len(selectziduan):
            ziduan += zdlist[selectziduan[i]-1][0]+','
        else:
            ziduan += zdlist[selectziduan[i]-1][0]

    #else:
    #    for i in zdlist:
    #        j += 1
    #        if j != len(zdlist):
    #            ziduan += i[0]+','
    #        else:
    #            ziduan += i[0]
    
    db.close()
    return ziduan

# 执行导入语句
def dbExecute(sql):
    db = dbCon()
    dbc = db.cursor()
    try:
        dbc.execute(sql)
        db.commit()
        print('导入数据成功')
    except BaseException as e:
        db.rollback()
        print('导入数据失败，报错信息：\n\n',e)
        print('\n\nSQL语句为：\n\n',sql)
        dbc.execute("desc {};".format(table))
        print("\n数据结构为:\n",dbc.fetchall())
    db.close()

# 读取导入文件的数据
def readFile(file_path):
    ziduan = getZiduan()
    sql_lines=''
    with open(file_path,'r') as f:
        next(f)
        for line in f.readlines():
            
            # 如果导入的数据为全量数据，但是仅仅想导入其中几列请去掉注释
           # if selectziduan:
           #     t = []
           #     for i in range(len(selectziduan)):
           #         t.append(line.strip('\n').split(',')[selectziduan[i]-1])
           #     line = tuple(t)
           # else:

            line = tuple(line.strip('\n').split(','))
            sql = 'insert into {} ({}) values {};'.format(table,ziduan,line)
            sql_lines = sql_lines + sql
    return(sql_lines)

if __name__ == '__main__':
    inputfile = sys.argv[1]
    if inputfile[-4:] != '.csv':
        print("请使用一个.csv的文件")
    else:
        sql_lines = readFile(inputfile)
        dbExecute(sql_lines)
