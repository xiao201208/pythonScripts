#!/usr/bin/env python
#auther:qitan

import sys
import pexpect

tarfile = '/var/log'
#signer = '#' if user=='root' else '$'
signer = '#'

def downTar(host,port,user,password):
	sshprocess = pexpect.spawn('/usr/bin/ssh',[user+'@'+host,'-p',port])
	process = pexpect.spawn('/usr/bin/scp',['-P',port,user+'@'+host+':/tmp/{}.tar.gz'.format(host),'/tmp/'],timeout=3600)
	process.expect('(?i)password')
	process.sendline(password)
	process.expect(pexpect.EOF)
	sshprocess.expect(signer)
	sshprocess.sendline('/usr/bin/rm -f /tmp/{}.tar.gz'.format(host))
	sshprocess.expect(signer)
	print(sshprocess.before)
	sshprocess.sendline('exit')	
		
def tarFile(host,port,user,password):
	sshprocess = pexpect.spawn('/usr/bin/ssh',[user+'@'+host,'-p',port])
	sshprocess.expect(signer)
	sshprocess.sendline('tar -Pczf /tmp/{}.tar.gz'.format(host) +' '+ tarfile)
	sshprocess.expect(signer)
	print(sshprocess.before)
	sshprocess.sendline('exit')
	
def batchtar():
	for l in open('hostlist.txt'):
		l = l.strip('\n')
		host,port,user,password = l.split()
		tarFile(host,port,user,password)
		downTar(host,port,user,password)

if __name__ == '__main__':
	batchtar()
