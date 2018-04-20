#this file using for fabric3
'''
Every func means one tasks.Please refer the Fabric to use.


'''
from fabric.api import *
import hashlib
b = hashlib.md5().update()
a= "123456"
a.encode()
env.hosts = ['192.168.79.128']
env.key_filename = 'E:\\Flask\\test_key\\id_rsa'
env.user = 'root'

def hello():
    print("Hello,Fabric!")

def touchfile():
    run('touch /tmp/www.txt')

def ping():
    run('whoami')