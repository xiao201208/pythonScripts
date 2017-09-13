#!/usr/bin/env python
# -*- coding: utf-8 -*-  

###############################
##使用方法
##安装paramko
###pip install cryptography
###pip install paramiko
##将ip、端口、用户名、密码写入到hostlist.txt中放到与此脚本同级的目录下
##############################


import sys,os
import paramiko
import traceback
home_dir = os.environ["HOME"]
id_rsa_pub = '{}/.ssh/id_rsa.pub'.format(home_dir)

def checkPubFile():
    if not os.path.isfile(id_rsa_pub):
        print('id_rsa.pub Does not exist! Please use ssh-keygen to creat one.')
        sys.exit(0)

def up_key(host,port,user,passwd):
    try:
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host,int(port), user, passwd)
        t = paramiko.Transport((host, port))
        t.connect(username=user, password=passwd)
        sftp =paramiko.SFTPClient.from_transport(t)
        print('create Host:{} .ssh dir......'.format(host))
        stdin,stdout,stderr=s.exec_command('mkdir ~/.ssh/')
        print('upload id_rsa.pub to Host:{}......',format(host))
        sftp.put(id_rsa_pub, "/tmp/temp_key")
        stdin,stdout,stderr=s.exec_command('cat /tmp/temp_key >> ~/.ssh/authorized_keys && rm -rf /tmp/temp_key')
        print('{}@{}  success!\n'.format(user,host))
        s.close()
        t.close()
    #获取异常信息
    except Exception as e:
        traceback.print_exc()
        try:
            s.close()
            t.close()
        except:
            pass

def run():
    checkPubFile()
    for line in open('hostlist.txt'):
        line = line.strip('\n')
        host,port,user,passwd = line.split()
        up_key(host, int(port), user, passwd)
if __name__ == '__main__':
    run()