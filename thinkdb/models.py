#import
import sys
sys.path.append('E:\\Flask')
from thinkdb import db,login_manager
from datetime import datetime
from flask_login import UserMixin
import pymysql
#用户表
class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,comment="主键ID")
    username = db.Column(db.String(64),unique=True,nullable=False,index=True,comment="用户名")
    password = db.Column(db.String(128),nullable=False,comment="密码")
    real_name = db.Column(db.String(16),nullable=False,default='',index=True,comment="真实姓名")
    email = db.Column(db.String(64),nullable=False,unique=True,index=True,comment="邮件地址")
    status = db.Column(db.String(10),index=True,nullable=False,comment="状态")
    group_id = db.Column(db.Integer, db.ForeignKey('user_group.id'),comment="用户组ID")
    privileges = db.Column(db.String(256),nullable=False,default='',comment="url权限")
    add_time = db.Column(db.DateTime,default=datetime.now(),comment="添加日期")
    last_modify_time = db.Column(db.DateTime,default=datetime.now(),onupdate=datetime.now(),comment="最后更新时间")
    def __repr__(self):
        return '<User %r>' % (self.username)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
#用户组
class User_Group(db.Model):
    __tablename__ = 'user_group'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    group_name = db.Column(db.String(32),unique=True)
    users = db.relationship('User',backref='group')
    introduction = db.Column(db.String(16),comment="用户组简介")
    add_time = db.Column(db.DateTime,default=datetime.now())
    last_modify_time  = db.Column(db.DateTime,default=datetime.now(),onupdate=datetime.now())
    def __repr__(self):
        return '<User_Group %r>' % (self.group_name)


############################数据库相关表##############################
#MySQL数据库信息表
class MySQL_Databases(db.Model):
    __tablename__ = 'mysql_databases'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,comment="主键ID")
    name = db.Column(db.String(32),index=True,unique=True,comment="名称(标识)")
    cluster_id = db.Column(db.Integer, db.ForeignKey('db_cluster.id'),comment="集群ID")
    datacenter_id = db.Column(db.Integer,db.ForeignKey('data_center.id'),comment="所属数据库中心")
    version = db.Column(db.String(16),nullable=False,default='',comment="版本号")
    ip = db.Column(db.String(16),nullable=False,index=True,comment="IP地址")
    port = db.Column(db.Integer,nullable=False,comment="端口")
    is_master = db.Column(db.SmallInteger,nullable=False,default=0,comment="是否主库,0否1是")
    is_slave = db.Column(db.SmallInteger, nullable=False, default=0, comment="是否从库,0否1是")
    status = db.Column(db.String(10),nullable=False,default='unknown',comment="active:正常,inactive：出错,unknown:未知状态")
    applicant = db.Column(db.String(16),nullable=False,comment="申请人")
    introduction = db.Column(db.String(8),comment="说明简介")
    add_time = db.Column(db.DateTime,default=datetime.now())
    last_modify_time = db.Column(db.DateTime,default=datetime.now(),onupdate=datetime.now())
    tickets = db.relationship('Tickets',backref='mysql_databases')
    def __repr__(self):
        return '<Databases %r>' % (self.name)
#MySQL主从复制表
class MySQL_Replication(db.Model):
    __tablename__ = 'mysql_replication'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,comment="主键ID")
    db_name = db.Column(db.String(32),index=True,unique=True,comment="名称(标识)")
    ip = db.Column(db.String(16),nullable=False,index=True,comment="IP地址")
    port = db.Column(db.Integer,nullable=False,comment="端口")
    read_only = db.Column(db.String(4),nullable=False,default='',comment="只读")
    gtid_mode = db.Column(db.String(4),nullable=False,default='',comment="GTID模式")
    master_host = db.Column(db.String(16),nullable=False,default='',index=True,comment="主库IP")
    master_port = db.Column(db.Integer,nullable=False,default=0,comment="主库端口")
    slave_io_run = db.Column(db.String(16),nullable=False,default='',comment="从库IO线程")
    slave_sql_run = db.Column(db.String(16),nullable=False,default='',comment="从库SQL线程")
    delay = db.Column(db.Integer,nullable=False,default=0,comment="从库延迟")
    relay_log_file = db.Column(db.String(32),nullable=False,default='',comment="RELAY日志")
    relay_log_pos = db.Column(db.String(32), nullable=False, default='', comment="RELAY日志偏移量")
    master_log_file = db.Column(db.String(32), nullable=False, default='', comment="Master二进制文件名")
    master_log_pos = db.Column(db.String(32), nullable=False, default='', comment="Master二进制日志偏移量")
    add_time = db.Column(db.DateTime,default=datetime.now())
    last_modify_time = db.Column(db.DateTime,default=datetime.now(),onupdate=datetime.now())
    def __repr__(self):
        return '<MySQL_Replication %r>' % (self.db_name)
#MySQL主从信息历史表
class MySQL_Replication_History(db.Model):
    __tablename__ = 'mysql_replication_history'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,comment="主键ID")
    db_name = db.Column(db.String(32),index=True,unique=True,comment="名称(标识)")
    ip = db.Column(db.String(16),nullable=False,index=True,comment="IP地址")
    port = db.Column(db.Integer,nullable=False,comment="端口")
    read_only = db.Column(db.String(4),nullable=False,default='',comment="只读")
    gtid_mode = db.Column(db.String(4),nullable=False,default='',comment="GTID模式")
    master_host = db.Column(db.String(16),nullable=False,default='',index=True,comment="主库IP")
    master_port = db.Column(db.Integer,nullable=False,default=0,comment="主库端口")
    slave_io_run = db.Column(db.String(16),nullable=False,default='',comment="从库IO线程")
    slave_sql_run = db.Column(db.String(16),nullable=False,default='',comment="从库SQL线程")
    delay = db.Column(db.Integer,nullable=False,default=0,comment="从库延迟")
    relay_log_file = db.Column(db.String(32),nullable=False,default='',comment="RELAY日志")
    relay_log_pos = db.Column(db.String(32), nullable=False, default='', comment="RELAY日志偏移量")
    master_log_file = db.Column(db.String(32), nullable=False, default='', comment="Master二进制文件名")
    master_log_pos = db.Column(db.String(32), nullable=False, default='', comment="Master二进制日志偏移量")
    add_time = db.Column(db.DateTime,default=datetime.now())
    last_modify_time = db.Column(db.DateTime,default=datetime.now(),onupdate=datetime.now())
    def __repr__(self):
        return '<MySQL_Replication_History %r>' % (self.db_name)
#数据库分类
class Data_Center(db.Model):
    __tablename__ = "data_center"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(32),unique=True)
    introduction = db.Column(db.String(64))
    add_time = db.Column(db.DateTime,default=datetime.now())
    last_modify_time  = db.Column(db.DateTime,default=datetime.now(),onupdate=datetime.now())
    databases = db.relationship('MySQL_Databases',backref='data_center')
    def __repr__(self):
        return  '<Data_Center %r>' % (self.name)
#数据库集群信息
class Db_Cluster(db.Model):
    __tablename__ = "db_cluster"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(64),nullable=False,index=True,unique=True)
    status = db.Column(db.String(6),nullable=False,default="online",server_default="online")
    introduction = db.Column(db.String(256),comment="集群简介")
    applicant = db.Column(db.String(16),nullable=False,index=True,comment="who applicate this cluster")
    add_time = db.Column(db.DateTime,default=datetime.now())
    last_modify_time  = db.Column(db.DateTime,default=datetime.now(),onupdate=datetime.now())
    databases = db.relationship('MySQL_Databases', backref='cluster')
    def __repr__(self):
        return  '<Db_Cluster %r>' % (self.name)

###############################工单##################################
#工单
class Tickets(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,comment="ID")
    tickets_num = db.Column(db.BigInteger,nullable=False,index=True,comment="工单编号",unique=True)
    applicant = db.Column(db.String(16),nullable=False,index=True,comment="提交人")
    auditor = db.Column(db.String(16),nullable=False,comment="审核人")
    sqlcontent = db.Column(db.Text,nullable=False,comment="待审核的语句内容")
    db_id = db.Column(db.Integer, db.ForeignKey('mysql_databases.id'))
    status = db.Column(db.String(16),nullable=False,server_default='',default='',comment="工单状态")
    is_execute = db.Column(db.SmallInteger,nullable=False,default=0,comment="工单是否已经执行")
    is_delete = db.Column(db.SmallInteger,nullable=False,default=0,comment="工单逻辑删除,0:正常，1：删除")
    audit_advise = db.Column(db.Text,nullable=False,default='',comment='审核意见')
    introduction = db.Column(db.String(10),nullable=False,default='',comment="工单简介")
    type = db.Column(db.String(6),nullable=False,default='',comment="工单类型：DML，DDL")
    add_time = db.Column(db.DateTime, default=datetime.now(), comment="提交时间", index=True)
    last_modify_time = db.Column(db.DateTime,nullable=False,default=datetime.now(),onupdate=datetime.now(),comment="最后变更时间")
    def __repr__(self):
        return '<Tickets %r >' % (self.id)

##############################消息##################################
###########################  Message ##########################
#Message
class Messages(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,comment="ID主键")
    title = db.Column(db.String(32),nullable=False,comment="标题")
    content = db.Column(db.String(256),nullable=False,comment="内容")
    sender = db.Column(db.String(32),nullable=False,index=True,comment="发件人")
    recipient = db.Column(db.String(32),nullable=False,index=True,comment="收件人")
    is_read = db.Column(db.SmallInteger(),nullable=False,default=0,comment="消息是否已读，1：是，0：否")
    add_time = db.Column(db.DateTime,default=datetime.now(),comment="消息发送时间")
    last_modify_time = db.Column(db.DateTime,default=datetime.now(),onupdate=datetime.now(),comment="最后更新时间")
    def __repr__(self):
        return '<Message %r>' % (self.title)



#操作日志
class Admin_Log(db.Model):
    __tablename__ = 'admin_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32),nullable=False,index=True,default='')
    event = db.Column(db.String(128))
    add_time = db.Column(db.DateTime,default=datetime.now(),index=True)
    last_modify_time = db.Column(db.DateTime,default=datetime.now(),onupdate=True,index=True)
    def __repr__(self):
        return '<Admin_Log %r>' % (self.username)
if __name__ == '__main__':
    db.create_all()




