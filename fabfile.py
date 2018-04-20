#this file using for fabric3
'''
Every func means one tasks.Please refer the Fabric to use.


'''
from fabric.api import *

env.hosts = ['192.168.79.128']
env.user = 'root'

def hello():
    print("Hello,Fabric!")

