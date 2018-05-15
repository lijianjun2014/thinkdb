README
====
Thinkdb是一款由PYTHON开发的MySQL DBA维护和监控MySQL数据库的软件。
目前完成了语句审核和工单模块，语句审核由去哪儿开源的Inception提供功能。<br>
后期计划陆续添加权限鉴别，数据库实例的上下线，上线自动添加与判断实例，网页端维护等功能。<br>
如果在使用中有遇到任何问题，请与作者联系！同时由于这是一款业也许时间完成的运维平台，难免会有一些小瑕疵，请大家见谅！但我会尽最大努力持续维护。
****

|Author|Li JianJun|
|---|---
|QQ群|　　7273702|
|E-mail|33359848@qq.com


# 使用说明
## 视图模块需要更改的地方
  1、消息组件 需要更改views.py中 dml视图的 收件人group_id 根据实际情况填写DBA团队的ID。<br>
  2、views.py中Inception的连接配置块根据实际情况填写IP,端口，用户，密码等信息。
  3、监控脚本monitor/monitor.py文件里面，需要根据实际情况更改监控历史数据存放信息
  
## 数据库账户权限
  1、监控账户必须要具有process,replication slave,replication client权限


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
# 项目介绍
## 登录
![login](https://github.com/lijianjun2014/thinkdb/blob/master/img/login.png "登录")
## 用户中心
  用户中心包含了用户组和具体的用户，用户组方便权限管理，后期会增加权限管理！
  用户列表支持搜索，搜索由bootstrapJS自带的。
  列表的Action支持用户快捷的 增加 修改 删除操作
![UserCenter](https://github.com/lijianjun2014/thinkdb/blob/master/img/usercenter.png "用户中心")
  新增用户
![AddUser](https://github.com/lijianjun2014/thinkdb/blob/master/img/add_user.png "新增用户")
## 数据库中心
  数据中心包含了数据中心，集群中心，具体的数据库服务器3个维度，能满足大多数的功能需求。
![](https://github.com/lijianjun2014/thinkdb/blob/master/img/dbcenter.png "数据中心")
  更改集群信息，后期陆续会加上集群的自动上下线功能
![](https://github.com/lijianjun2014/thinkdb/blob/master/img/change_cluster.png "数据中心")
## 监控中心
  健康监控
![](https://github.com/lijianjun2014/thinkdb/blob/master/img/health_monitor.png "健康监控")
  复制监控
![](https://github.com/lijianjun2014/thinkdb/blob/master/img/replication_monitor.png "复制监控")
  监控图表
![](https://github.com/lijianjun2014/thinkdb/blob/master/img/echarts1.png "监控图表") 
![](https://github.com/lijianjun2014/thinkdb/blob/master/img/echarts2.png "监控图表") 
![](https://github.com/lijianjun2014/thinkdb/blob/master/img/echarts3.png "监控图表") 
![](https://github.com/lijianjun2014/thinkdb/blob/master/img/echarts4.png "监控图表") 
  慢查询信息
  慢查询是由pt工具生成，这列只做展示用
![](https://github.com/lijianjun2014/thinkdb/blob/master/img/slow_query.png "慢查询")
## 工单模块
  工单模块支持DML，DDL的提交，由DBA审核，后期会加入由直系上级先审核，最后由DBA审核并执行，底层功能是由inception实现
![](https://github.com/lijianjun2014/thinkdb/blob/master/img/tickets.png "工单")
  工单提交，语法错误高亮显示
![](https://github.com/lijianjun2014/thinkdb/blob/master/img/tickets_submit.png "工单")
  工单审核与执行，检测通过了才会出现执行按钮
![](https://github.com/lijianjun2014/thinkdb/blob/master/img/tickets_modify.png "工单")
