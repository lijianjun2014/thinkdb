# coding: utf-8

from multiprocessing import Process
import multiprocessing
import time,pymysql,psutil,os,datetime

# 数据库连接信息
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'thinkdb',
    'password': '123456',
    'db': 'fthinkdb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
    }

count = 0
while True:
    os.system('venv\\Scripts\\activate')
    print("第%s次监控！" % (count))
    start_time =  datetime.datetime.now()
    print("开始时间：%s" % start_time)
    os.system('python monitor\\monitor.py')
    end_time = datetime.datetime.now()
    print("结束时间：%s" % end_time)
    print("耗时：%s" % (end_time-start_time))
    count = count + 1
    time.sleep(60)




