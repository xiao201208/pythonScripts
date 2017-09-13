#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: qitan

import os
import sys
import paramiko

home_dir = os.environ['HOME']
key = '{}/.ssh/id_rsa'.format(home_dir)
cmd = sys.argv[1]


def setSshConnect(host,port,user,key,cmd):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host,port,user,key)
	stdin,stdout,stderr = ssh.exec_command(cmd)
	outresult = stdout.read()
	errresult = stderr.read()
	if outresult:
		print('The command is {}'.format(cmd))
		print('The result of host {} is:'.format(host))
		print(outresult.decode())
	else:
		print(cmd)
		print('The Command for {} is error!'.format(host))
		print(errresult)
	ssh.close()


def getInfo():
	for l in open('hostlist.txt'):
		l = l.strip('\n')
		host,port,user = l.split()
		setSshConnect(host,int(port),user,key,cmd)


if __name__ == '__main__':
	getInfo()
