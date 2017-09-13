#coding=utf8

import os
import sys

if os.getuid() == 0:
	pass
else:
	print('您不是root用户，请使用root用户运行该脚本')
	sys.exit(1)

version = raw_input('请输入您需要的python版本:')
if version == '2.7':
	url = 'https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tar.xz'
elif version == '3.6':
	url = 'https://www.python.org/ftp/python/3.6.2/Python-3.6.2.tar.xz'
else:
	print('您输入的版本号有误,请输入2.7或者w3.6')
	sys.exit(1)

cmd = 'wget ' + url
res = os.system(cmd)

if res != 0:
	print('下载源码包失败，请检测网络情况')
	sys.exit(1)
if version == '2.7':
	package_name = 'Python-2.7.13'
else:
	package_name = 'Python-3.6.2'

cmd = 'tar -xvJf ' +package_name+'.tar.xz'
res = os.system(cmd)

if res != 0:
	os.system('rm -f '+package_name+'.tar.xz')
	print('解压缩失败，请重新运行这个脚本')
	sys.exit(1)
cmd = 'cd '+package_name+' && ./configure --prefix=/usr/local/python && make &&make install'
res=os.system(cmd)

if res != 0:
	print('编译python源码失败，请检测依赖包')
	sys.exit(1)


