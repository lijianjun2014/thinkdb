#this file using for fabric3
'''
Every func means one tasks.Please refer the Fabric to use.


'''
from fabric.api import *
from fabric.contrib.files import exists
import os



env.hosts = ['192.168.79.128']
env.key_filename = 'E:\\Flask\\test_key\\id_rsa'
env.user = 'root'

def hello():
    print("Hello,Fabric!")

def touchfile():
    open_shell("")

def ping():
    run('whoami')
    local('dir|findstr env', capture=False)
    a = local('dir|findstr test',capture=True)
    print(a)

def stop_mysql():
    run("/data/mysql/bin/mysqladmin -S /tmp/mysql3308.sock shutdown")

def start_mysql():
    run('/data/mysql/bin/mysqld_safe --defaults-file=/data/mysql3308/my.cnf &')

def install_mysql(version,**xargs):
    def check_user():
        is_user = int(run('id mysql|wc -l'))
        if is_user != 1:
            run("useradd mysql -M -s /sbin/nologin")
        is_user = int(run('id mysql|wc -l'))
        return  is_user;
    def check_dir():
        dtime = run("date +%F")
        if not exists(r'/opt/soft/mysql_install_%s' % dtime):
            run("mkdir -p /opt/soft/mysql_install_%s" % dtime)
    #下载MySQL源码并解压
    def download():
        dtime = run("date +%F")
        with cd("/opt/soft/mysql_install_%s" % dtime):
            if version == '5.5':
                if not 'source_url' in locals():
                    run("wget -O mysql.tar.gz %s --no-check-certificate" % 'http://mirrors.sohu.com/mysql/MySQL-5.5/mysql-5.5.55.tar.gz')
                else:
                    run("wget -O mysql.tar.gz %s --no-check-certificate" % xargs['source_url'])
                run("mkdir mysql_code_5.5 && tar -zxf mysql.tar.gz -C mysql_code_5.5 --strip-components=1")
            elif version == "5.6":
                if not 'source_url' in locals():
                    run("wget -O mysql.tar.gz %s --no-check-certificate" % 'http://mirrors.sohu.com/mysql/MySQL-5.6/mysql-5.6.36.tar.gz')
                else:
                    run("wget -O mysql.tar.gz %s --no-check-certificate" % xargs['source_url'])
                    run("mkdir mysql_code_5.6 && tar -zxf mysql.tar.gz -C mysql_code_5.6 --strip-components=1")
    def install():
        dtime = run("date +%F")
        with cd("/opt/soft/mysql_install_%s/mysql_code_%s" % (dtime,version)):
            run('yum install zlib libxml libjpeg freetype libpng gd curl libiconv zlib-devel libxml2-devel libjpeg-devel freetype-devel libpng-devel gd-devel curl-devel curl libxml2 libxml2-devel libmcrypt libmcrypt-devel libxslt* ncurses-devel openssl openssl-devel pcre pcre-devel gcc gcc-c++ dtrace systemtap-sdt-devel make cmake -y')
            if not "install_dest" in locals() and not "install_dest" in globals():
                run("cmake -DCMAKE_INSTALL_PREFIX=/usr/local/mysql -DMYSQL_DATADIR=/usr/local/mysql/data -DWITH_INNOBASE_STORAGE_ENGINE=1 -DWITH_ARCHIVE_STORAGE_ENGINE=1 -DWITH_BLACKHOLE_STORAGE_ENGINE=1 -DWITH_PARTITION_STORAGE_ENGINE=1 -DWITH_PERFSCHEMA_STORAGE_ENGINE=1 -DWITH_FEDERATED_STORAGE_ENGINE=1 -DWITH_MEMORY_STORAGE_ENGINE=1 -DWITH_READLINE=1 -DMYSQL_UNIX_ADDR=${install_path}/data/mysql.sock -DMYSQL_TCP_PORT=3306 -DENABLED_LOCAL_INFILE=1 -DEXTRA_CHARSETS=all -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci")
            else:
                run("cmake -DCMAKE_INSTALL_PREFIX=%s -DMYSQL_DATADIR=%s/data -DWITH_INNOBASE_STORAGE_ENGINE=1 -DWITH_ARCHIVE_STORAGE_ENGINE=1 -DWITH_BLACKHOLE_STORAGE_ENGINE=1 -DWITH_PARTITION_STORAGE_ENGINE=1 -DWITH_PERFSCHEMA_STORAGE_ENGINE=1 -DWITH_FEDERATED_STORAGE_ENGINE=1 -DWITH_MEMORY_STORAGE_ENGINE=1 -DWITH_READLINE=1 -DMYSQL_UNIX_ADDR=${install_path}/data/mysql.sock -DMYSQL_TCP_PORT=3306 -DENABLED_LOCAL_INFILE=1 -DEXTRA_CHARSETS=all -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci" % (xargs['install_dest'],xargs['install_dest']))
            run("make && make install")
    check_user()
    check_dir()
    download()
    install()


