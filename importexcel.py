#!/bin/python
#coding=utf-8

import pymysql
import sys
import xlrd

# 使用方法：
# python3 importdata.py filename
# filename为要导入的文件名称，importdata.py为脚本名称
# 注意：需要 pip3 install pymysql 安装pymsql库 
# Author:qitan


# 请输入的相关信息
host = ""
user = ""
password = "" 
database = ""
table = ""
selectziduan = [] # 请输入要导入的字段列数，例如[1,2,5]表示仅仅导入第一个、第二个和第五个字段的数据；默认为全部字段数据

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
        # print('\n\nSQL语句为：\n\n',sql)
        dbc.execute("desc {};".format(table))
        print("\n数据结构为:\n",dbc.fetchall())
    db.close()

# 读取导入文件的数据
def readFile(excelfile):
    ziduan = getZiduan()
    sql_lines=''
    workbook = xlrd.open_workbook(excelfile)
    sheet = sheet = workbook.sheet_by_index(0)

    # 获取需要转化的数字和日期
    line = sheet.row(1)
    nucol = []
    xlcol = []
    for i in range(len(line)):
        if 'number' in str(line[i]):
            nucol.append(i)
        elif 'xldate' in str(line[i]):
            xlcol.append(i)
        else:
            pass

    # 获取表格中的值
    for i in range(1,sheet.nrows):
        linev = sheet.row_values(i)
        if nucol:
            for j in nucol:
                linev[j] = str(int(linev[j]))
            for k in xlcol:
                d = xlrd.xldate_as_datetime(linev[k],workbook.datemode)
                linev[k] = str(d)

        linev = tuple(linev)
        sql = 'insert into {} ({}) values {};'.format(table,ziduan,linev)
        sql_lines = sql_lines + sql
    return(sql_lines)

if __name__ == '__main__':
    inputfile = sys.argv[1]
    if inputfile[-5:] != '.xlsx':
        print("请使用一个.xlsx的文件")
    else:
        sql_lines = readFile(inputfile)
        dbExecute(sql_lines)
