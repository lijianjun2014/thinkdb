README
====
Thinkdb现在处于开发中是一个雏形，很多功能暂未实现，当然也暂时未实现脚本自动化安装与部署。<br>
如果您需要试用可以参照以下步骤来完成安装与上线。具体由于服务器平台与版本不一致，可能会有差异！<br>
****

# ThinkDB安装流程
## ThinkDB程序下载
    1. git clone https://github.com/lijianjun2014/thinkdb.git
    2. cd thinkdb && mkdir /usr/local/thinkdb && cp -r {config.py,main.py,requirement,monitor/,uwsgi_conf/，thinkdb/} /usr/local/thinkdb/
    3. views.py中Inception的连接配置块根据实际情况填写IP,端口，用户，密码等信息。
    4. 监控脚本monitor/monitor.py文件里面，需要根据实际情况更改监控历史数据存放信息

  
## Nginx安装
    1. 下载nginx安装包：wget http://nginx.org/download/nginx-1.10.3.tar.gz
    2. 解压:   tar -zxf nginx-1.10.3.tar.gz
    3. 编译:   cd nginx-1.10.3 && ./configure --prefix=/usr/local/nginx
    4. 安装：  make && make install

## Python升级
    1. 下载并解压好Python3.6,进入目录
    2. 编译:   ./configure --prefix=/usr/local/python3.6
    3. 安装:   make && make install
    4. 移动服务器自带的python版本：  mv /usr/bin/python /usr/bin/python_old
    5. 添加软链:    ln -s /usr/local/python3.6/bin/python3.6 /usr/bin/python
    6. 编辑/etc/profile：    echo "PATH=$PATH:/usr/local/python3.6/bin" >>/etc/profile  && source /etc/profile
    7. 修改yum文件，防止python升级导致Yum 命令失效：
       vim /usr/bin/yum
```diff
- #!/usr/bin/python
+ #!/usr/bin/python_old
```
    8. 如果是Centos7使用firewall-cmd 则还需要修改：
    vim /usr/bin/firewall-cmd
```diff
- #!/usr/bin/python
+ #!/usr/bin/python_old
```
## 安装虚拟环境和依赖包
    1. 安装virtualenv:        /usr/local/python3.6/bin/pip3.6 install virtualenv
    2. 创建Thinkdb虚拟环境：      /usr/local/python3.6/bin/virtualenv /usr/local/thinkdb/venv
    3. 激活thinkdb虚拟环境:   source /usr/local/thinkdb/venv/bin/activate
    4. 安装thinkdb所需依赖：  pip install -r /usr/local/thinkdb/requirement

## 运行nginx
    1. 从thinkdb包下面的nginx_conf文件夹拷贝nginx.conf到/usr/local/nginx/conf/nginx.conf
    2. /usr/local/nginx/sbin/nginx    如报错请百度解决nginx报错
    3. 启动uwsgi:   /usr/local/thinkdb/venv/bin/uwsgi --ini /usr/local/thinkdb/uwsgi_conf/uwsgi.conf &
## 导入数据与表结构：
    1.登录数据库，创建thinkdb数据库，导入thinkdb中sql文件夹下的数据。
    2.修改config.py和 thinkdb/views.py中的数据库连接信息
    3.现在用admin/admin888 来查看效果吧。

## Python3使用Inception需要修改的地方：
  1、如果按照正确格式书写后还是报错：2576, 'Must start as begin statement。解决方案：<br>
    修改pymysql的cursor.py,找到"if not self._defer_warnings"，大概在338行将self._show_warnings()这一句注释掉，也可以直接删除，换成pass。
```diff
- if not self._defer_warnings:
-     self._show_warnings()
+ if not self._defer_warnings:
+     pass
```  
  2、修改pymysql的connections.py里面的_request_authentication() 增加2行如下：
```diff
- if int(self.server_version.split('.', 1)[0]) >= 5:
-    self.client_flag |= CLIENT.MULTI_RESULTS
+ if self.server_version.split('.', 1)[0] == "Inception2":
+    self.client_flag |= CLIENT.MULTI_RESULTS
+ elif int(self.server_version.split('.', 1)[0]) >= 5:
+    self.client_flag |= CLIENT.MULTI_RESULTS
```
