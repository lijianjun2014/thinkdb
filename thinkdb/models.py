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
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,comment="用户ID")
    username = db.Column(db.String(64),nullable=False,default='',server_default='',unique=True,index=True,comment="用户名")
    password = db.Column(db.String(128),nullable=False,default='',server_default='',comment="密码")
    real_name = db.Column(db.String(16),nullable=False,default='',server_default='',index=True,comment="真实姓名")
    email = db.Column(db.String(64),nullable=False,default='',server_default='',unique=True,index=True,comment="邮件地址")
    status = db.Column(db.String(10),index=True,nullable=False,default='',server_default='',comment="状态")
    group_id = db.Column(db.Integer, db.ForeignKey('user_group.id'),comment="用户组ID")
    privileges = db.Column(db.String(256),nullable=False,default='',server_default='',comment="url权限")
    add_time = db.Column(db.DateTime,default=datetime.now,comment="添加日期")
    last_modify_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now,comment="最后更新时间")
    def __repr__(self):
        return '<User %r>' % (self.username)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
#用户组
class User_Group(db.Model):
    __tablename__ = 'user_group'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,comment="用户组ID")
    group_name = db.Column(db.String(32),nullable=False,default='',server_default='',unique=True,comment="组名称")
    users = db.relationship('User',backref='group')
    introduction = db.Column(db.String(16),nullable=False,default='',server_default='',comment="用户组简介")
    add_time = db.Column(db.DateTime,default=datetime.now,comment="添加时间")
    last_modify_time  = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now,comment="最后更新时间")
    def __repr__(self):
        return '<User_Group %r>' % (self.group_name)


############################数据库相关表##############################
#MySQL数据库信息表
class MySQL_Databases(db.Model):
    __tablename__ = 'mysql_databases'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,comment="数据库ID")
    name = db.Column(db.String(32),nullable=False,default='',server_default='',index=True,unique=True,comment="名称(标识)")
    cluster_id = db.Column(db.Integer, db.ForeignKey('db_cluster.id'),comment="集群ID")
    datacenter_id = db.Column(db.Integer,db.ForeignKey('data_center.id'),comment="所属数据库中心")
    version = db.Column(db.String(16),nullable=False,default='',server_default='',comment="版本号")
    ip = db.Column(db.String(16),nullable=False,default='',server_default='',index=True,comment="IP地址")
    port = db.Column(db.Integer,nullable=False,default=0,server_default='0',comment="端口")
    db_user = db.Column(db.String(32),nullable=False,default='',server_default='',comment="数据库连接用户")
    db_password = db.Column(db.String(32),nullable=False,default='',server_default='',comment="数据库连接密码")
    is_master = db.Column(db.SmallInteger,nullable=False,default=0,server_default='0',comment="是否主库,0否1是")
    is_slave = db.Column(db.SmallInteger, nullable=False, default=0,server_default='0', comment="是否从库,0否1是")
    is_monitor = db.Column(db.SmallInteger, nullable=False, default=0, server_default='0', comment="是否监控,0否1是")
    status = db.Column(db.String(10),nullable=False,default='unknown',server_default='unknown',comment="active:正常,inactive：出错,unknown:未知状态")
    applicant = db.Column(db.String(16),nullable=False,default='',server_default='',comment="申请人")
    introduction = db.Column(db.String(8),nullable=False,default='',server_default='',comment="说明简介")
    add_time = db.Column(db.DateTime,default=datetime.now,comment="添加时间")
    last_modify_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now,comment="最后更新时间")
    tickets = db.relationship('Tickets',backref='mysql_databases')
    def __repr__(self):
        return '<Databases %r>' % (self.name)

#MySQL_Status 数据库状态信息表
class MySQL_Status(db.Model):
    __tablename__ = 'mysql_status'
    id = db.Column(db.BigInteger,primary_key=True,autoincrement=True,comment="自增主键")
    db_name = db.Column(db.String(32),nullable=False,default='',server_default='',index=True,unique=True,comment="名称(标识)")
    ip = db.Column(db.String(16),nullable=False,default='',server_default='',index=True,comment="IP地址")
    port = db.Column(db.BigInteger,nullable=False,default=0,server_default='0',comment="端口")
    db_cluster_name = db.Column(db.String(32),nullable=False,default='',server_default='',index=True,comment="所属集群名称")
    data_center_name = db.Column(db.String(32),nullable=False,default='',server_default='',index=True,comment="所属数据中心名称")
    is_master = db.Column(db.Integer, nullable=False, default=0, server_default='0', comment="是否主库,0否1是")
    is_slave = db.Column(db.Integer, nullable=False, default=0, server_default='0', comment="是否从库,0否1是")
    uptime = db.Column(db.BigInteger,nullable=False,default=1, server_default='1',comment="在线时长")
    version = db.Column(db.String(16), nullable=False, default='', server_default='', comment="版本号")
    max_connection = db.Column(db.BigInteger,nullable=False,default=1,server_default='1',comment="最大连接数")
    max_connect_errors = db.Column(db.BigInteger,nullable=False,default=1,server_default='1',comment="最大连接数")
    open_files_limit = db.Column(db.BigInteger,nullable=False,default=1,server_default='1',comment="最大打开文件数")
    open_files = db.Column(db.BigInteger,nullable=False,default=1,server_default='1',comment="当前打开文件数")
    table_open_cache = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="表缓存数")
    open_tables = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="当前打开表数")
    opened_tables = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="当前打开表数")
    max_tmp_tables = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="临时表限制")
    max_heap_table_size = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="内存临时表限制")
    max_allowed_packet = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="Packet大小")
    threads_connected = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="当前打开线程数")
    threads_running = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="当前活动线程数")
    threads_created = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="创建的线程数量")
    threads_cached = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="线程缓存数量")
    connections = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="连接数")
    aborted_clients = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="断开客户端数量")
    aborted_connects = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="断开的连接数")
    created_tmp_tables = db.Column(db.Integer, nullable=False, default=1, server_default='1',comment="创建的临时表数量")
    created_tmp_disk_tables = db.Column(db.Integer, nullable=False, default=1, server_default='1',comment="创建的磁盘临时表数量")
    connections_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒连接数")
    bytes_received_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒接收字节数")
    bytes_sent_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒发送字节数")
    com_select_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒查询量")
    com_insert_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒写入量")
    com_update_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒更新量")
    com_delete_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒删除量")
    com_commit_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒提交数")
    com_rollback_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒回滚")
    questions_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒处理的客户端发送的请求数")
    queries_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒处理的请求数包括存储过程，事件等")
    transaction_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒事务数")
    created_tmp_tables_persecond = db.Column(db.Integer, nullable=False, default=1, server_default='1', comment="每秒创建的临时表")
    created_tmp_disk_tables_persecond = db.Column(db.Integer, nullable=False, default=1, server_default='1', comment="每秒创建的磁盘临时表")
    created_tmp_files_persecond = db.Column(db.Integer, nullable=False, default=1, server_default='1', comment="每秒创建的临时文件数")
    table_locks_immediate_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒获得锁数量")
    table_locks_waited_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒的锁等待")
    #InnoDB
    innodb_buffer_pool_pages_total = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="InnoDB总页数")
    innodb_buffer_pool_pages_data = db.Column(db.Integer, nullable=False, default=1, server_default='1',comment="InnoDB使用中的页数量")
    innodb_buffer_pool_pages_dirty = db.Column(db.Integer, nullable=False, default=1, server_default='1',comment="InnoDB脏数据的页数量")
    innodb_buffer_pool_pages_flushed = db.Column(db.Integer, nullable=False, default=1, server_default='1',comment="缓冲池请求刷新的页数量")
    innodb_buffer_pool_pages_free = db.Column(db.BigInteger, nullable=False, default=1, server_default='1',comment="空闲页数量")
    innodb_buffer_pool_reads = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="Innodb从磁盘读取数")
    innodb_buffer_pool_read_requests = db.Column(db.BigInteger, nullable=False, default=1, server_default='1',comment="Innodb从缓冲读取数")
    innodb_row_lock_current_waits = db.Column(db.BigInteger, nullable=False, default=1, server_default='1',comment="InnoDB当前锁等待数")
    innodb_row_lock_time_avg = db.Column(db.BigInteger, nullable=False, default=1, server_default='1',comment="平均锁等待时长毫秒")
    innodb_row_lock_waits = db.Column(db.BigInteger, nullable=False, default=1, server_default='1',comment="Innodb锁等待总量")
    innodb_row_lock_time_max = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="InnoDB最大锁等待时长毫秒")
    innodb_rows_inserted_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1',comment="InnoDB每秒新增行数")
    innodb_rows_deleted_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="InnoDB每秒删除行数")
    innodb_rows_updated_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="InnoDB每秒更新行数")
    innodb_rows_reads_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1',comment="InnoDB每秒查询行数")
    add_time = db.Column(db.DateTime,default=datetime.now,comment="添加时间")
    last_modify_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now,comment="最后更新时间")
    def __repr__(self):
        return '<MySQL_Status %r>' % (self.db_name)

class MySQL_Status_History(db.Model):
    __tablename__ = 'mysql_status_history'
    id = db.Column(db.BigInteger,primary_key=True,autoincrement=True,comment="自增主键")
    mysql_status_id = db.Column(db.BigInteger,comment="status表的主键,可以不用要，主要为了简化监控脚本的语句")
    db_name = db.Column(db.String(32),nullable=False,default='',server_default='',comment="名称(标识)")
    ip = db.Column(db.String(16),nullable=False,default='',server_default='',comment="IP地址")
    port = db.Column(db.BigInteger,nullable=False,default=0,server_default='0',comment="端口")
    db_cluster_name = db.Column(db.String(32),nullable=False,default='',server_default='',index=True,comment="所属集群名称")
    data_center_name = db.Column(db.String(32),nullable=False,default='',server_default='',index=True,comment="所属数据中心名称")
    is_master = db.Column(db.Integer, nullable=False, default=0, server_default='0', comment="是否主库,0否1是")
    is_slave = db.Column(db.Integer, nullable=False, default=0, server_default='0', comment="是否从库,0否1是")
    uptime = db.Column(db.BigInteger,nullable=False,default=1, server_default='1',comment="在线时长")
    version = db.Column(db.String(16), nullable=False, default='', server_default='', comment="版本号")
    max_connection = db.Column(db.BigInteger,nullable=False,default=1,server_default='1',comment="最大连接数")
    max_connect_errors = db.Column(db.BigInteger,nullable=False,default=1,server_default='1',comment="最大连接数")
    open_files_limit = db.Column(db.BigInteger,nullable=False,default=1,server_default='1',comment="最大打开文件数")
    open_files = db.Column(db.BigInteger,nullable=False,default=1,server_default='1',comment="当前打开文件数")
    table_open_cache = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="表缓存数")
    open_tables = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="当前打开表数")
    opened_tables = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="当前打开表数")
    max_tmp_tables = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="临时表限制")
    max_heap_table_size = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="内存临时表限制")
    max_allowed_packet = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="Packet大小")
    threads_connected = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="当前打开线程数")
    threads_running = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="当前活动线程数")
    threads_created = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="创建的线程数量")
    threads_cached = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="线程缓存数量")
    connections = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="连接数")
    aborted_clients = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="断开客户端数量")
    aborted_connects = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="断开的连接数")
    created_tmp_tables = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="创建的临时表数量")
    created_tmp_disk_tables = db.Column(db.BigInteger, nullable=False, default=1, server_default='1',comment="创建的磁盘临时表数量")
    connections_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒连接数")
    bytes_received_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒接收字节数")
    bytes_sent_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒发送字节数")
    com_select_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒查询量")
    com_insert_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒写入量")
    com_update_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒更新量")
    com_delete_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒删除量")
    com_commit_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒提交数")
    com_rollback_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒回滚")
    questions_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒处理的客户端发送的请求数")
    queries_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒处理的请求数包括存储过程，事件等")
    transaction_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒事务数")
    created_tmp_tables_persecond = db.Column(db.Integer, nullable=False, default=1, server_default='1', comment="每秒创建的临时表")
    created_tmp_disk_tables_persecond = db.Column(db.Integer, nullable=False, default=1, server_default='1', comment="每秒创建的磁盘临时表")
    created_tmp_files_persecond = db.Column(db.Integer, nullable=False, default=1, server_default='1', comment="每秒创建的临时文件数")
    table_locks_immediate_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒获得锁数量")
    table_locks_waited_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="每秒的锁等待")
    #InnoDB
    innodb_buffer_pool_pages_total = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="InnoDB总页数")
    innodb_buffer_pool_pages_data = db.Column(db.Integer, nullable=False, default=1, server_default='1',comment="InnoDB使用中的页数量")
    innodb_buffer_pool_pages_dirty = db.Column(db.Integer, nullable=False, default=1, server_default='1',comment="InnoDB脏数据的页数量")
    innodb_buffer_pool_pages_flushed = db.Column(db.Integer, nullable=False, default=1, server_default='1',comment="缓冲池请求刷新的页数量")
    innodb_buffer_pool_pages_free = db.Column(db.BigInteger, nullable=False, default=1, server_default='1',comment="空闲页数量")
    innodb_buffer_pool_reads = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="Innodb从磁盘读取数")
    innodb_buffer_pool_read_requests = db.Column(db.BigInteger, nullable=False, default=1, server_default='1',comment="Innodb从缓冲读取数")
    innodb_row_lock_current_waits = db.Column(db.BigInteger, nullable=False, default=1, server_default='1',comment="InnoDB当前锁等待数")
    innodb_row_lock_time_avg = db.Column(db.BigInteger, nullable=False, default=1, server_default='1',comment="平均锁等待时长毫秒")
    innodb_row_lock_waits = db.Column(db.BigInteger, nullable=False, default=1, server_default='1',comment="Innodb锁等待总量")
    innodb_row_lock_time_max = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="InnoDB最大锁等待时长毫秒")
    innodb_rows_inserted_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1',comment="InnoDB每秒新增行数")
    innodb_rows_deleted_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="InnoDB每秒删除行数")
    innodb_rows_updated_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1', comment="InnoDB每秒更新行数")
    innodb_rows_reads_persecond = db.Column(db.BigInteger, nullable=False, default=1, server_default='1',comment="InnoDB每秒查询行数")
    add_time = db.Column(db.DateTime,default=datetime.now,comment="添加时间")
    last_modify_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now,comment="最后更新时间")
    __table_args__ = (db.Index('idx_db_name_last_time','db_name','last_modify_time'),)
    def __repr__(self):
        return '<MySQL_Status_History %r>' % (self.db_name)

#MySQL主从复制表
class MySQL_Replication(db.Model):
    __tablename__ = 'mysql_replication'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,comment="复制ID")
    db_name = db.Column(db.String(32),nullable=False,default='',server_default='',index=True,unique=True,comment="名称(标识)")
    ip = db.Column(db.String(16),nullable=False,default='',server_default='',index=True,comment="IP地址")
    port = db.Column(db.Integer,nullable=False,default=0,server_default='0',comment="端口")
    read_only = db.Column(db.String(4),nullable=False,default='',server_default='',comment="只读")
    gtid_mode = db.Column(db.String(4),nullable=False,default='',server_default='',comment="GTID模式")
    master_host = db.Column(db.String(16),nullable=False,default='',server_default='',index=True,comment="主库IP")
    master_port = db.Column(db.Integer,nullable=False,default=0,server_default='0',comment="主库端口")
    slave_io_run = db.Column(db.String(16),nullable=False,default='',server_default='',comment="从库IO线程")
    slave_sql_run = db.Column(db.String(16),nullable=False,default='',server_default='',comment="从库SQL线程")
    delay = db.Column(db.Integer,nullable=False,default=0,server_default='0',comment="从库延迟")
    master_log_file = db.Column(db.String(32),nullable=False,default='',server_default='',comment="当前Master二进制文件名")
    read_master_log_pos = db.Column(db.String(32), nullable=False, default='',server_default='', comment="IO线程读取的当前Maste文件偏移量")
    relay_master_log_file = db.Column(db.String(32), nullable=False, default='',server_default='', comment="SQL线程执行到当前的Master日志的文件名")
    exec_master_log_pos = db.Column(db.String(32), nullable=False, default='',server_default='', comment="SQL线程执行到当前的Master日志偏移量")
    add_time = db.Column(db.DateTime,default=datetime.now,comment="添加时间")
    last_modify_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now,comment="最后更新时间")
    def __repr__(self):
        return '<MySQL_Replication %r>' % (self.db_name)
#MySQL主从信息历史表
class MySQL_Replication_History(db.Model):
    __tablename__ = 'mysql_replication_history'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,comment="主键ID")
    mysql_replication_id = db.Column(db.Integer,index=True,comment="主从复制表的ID")
    db_name = db.Column(db.String(32),nullable=False,index=True,comment="名称(标识)")
    ip = db.Column(db.String(16),nullable=False,index=True,comment="IP地址")
    port = db.Column(db.Integer,nullable=False,comment="端口")
    read_only = db.Column(db.String(4),nullable=False,default='',server_default='',comment="只读")
    gtid_mode = db.Column(db.String(4),nullable=False,default='',server_default='',comment="GTID模式")
    master_host = db.Column(db.String(16),nullable=False,default='',server_default='',index=True,comment="主库IP")
    master_port = db.Column(db.Integer,nullable=False,default=0,server_default='0',comment="主库端口")
    slave_io_run = db.Column(db.String(16),nullable=False,default='',server_default='',comment="从库IO线程")
    slave_sql_run = db.Column(db.String(16),nullable=False,default='',server_default='',comment="从库SQL线程")
    delay = db.Column(db.Integer,nullable=False,default=0,server_default='0',comment="从库延迟")
    master_log_file = db.Column(db.String(32), nullable=False, default='', server_default='', comment="当前Master二进制文件名")
    read_master_log_pos = db.Column(db.String(32), nullable=False, default='', server_default='',comment="IO线程读取的当前Maste文件偏移量")
    relay_master_log_file = db.Column(db.String(32), nullable=False, default='', server_default='',comment="SQL线程执行到当前的Master日志的文件名")
    exec_master_log_pos = db.Column(db.String(32), nullable=False, default='', server_default='',comment="SQL线程执行到当前的Master日志偏移量")
    add_time = db.Column(db.DateTime,default=datetime.now,comment="添加时间")
    last_modify_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now,comment="最后更新时间")
    def __repr__(self):
        return '<MySQL_Replication_History %r>' % (self.db_name)
#数据中心
class Data_Center(db.Model):
    __tablename__ = "data_center"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,comment="数据中心ID")
    name = db.Column(db.String(32),unique=True,nullable=False,default='',server_default='',comment="数据中心名称")
    introduction = db.Column(db.String(64),nullable=False,default='',server_default='',comment="数据中心简介")
    add_time = db.Column(db.DateTime,default=datetime.now,comment="添加时间")
    last_modify_time  = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now,comment="最后更新时间")
    databases = db.relationship('MySQL_Databases',backref='data_center')
    def __repr__(self):
        return  '<Data_Center %r>' % (self.name)
#数据库集群信息
class Db_Cluster(db.Model):
    __tablename__ = "db_cluster"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,comment="集群主键ID")
    name = db.Column(db.String(64),nullable=False,default='',server_default='',index=True,unique=True,comment="名称")
    status = db.Column(db.String(6),nullable=False,default="online",server_default="online",comment="状态")
    introduction = db.Column(db.String(256),nullable=False,default='',server_default='',comment="简介")
    applicant = db.Column(db.String(16),nullable=False,default='',server_default='',index=True,comment="who applicate this cluster")
    add_time = db.Column(db.DateTime,default=datetime.now,comment="添加时间")
    last_modify_time  = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now,comment="最后更新时间")
    databases = db.relationship('MySQL_Databases', backref='cluster')
    def __repr__(self):
        return  '<Db_Cluster %r>' % (self.name)

###############################工单##################################
#工单
class Tickets(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,comment="工单ID")
    tickets_num = db.Column(db.BigInteger,nullable=False,default=0,server_default='0',index=True,comment="工单编号",unique=True)
    applicant = db.Column(db.String(16),nullable=False,default='',server_default='',index=True,comment="提交人")
    auditor = db.Column(db.String(16),nullable=False,default='',server_default='',comment="审核人")
    sqlcontent = db.Column(db.Text,nullable=False,default='',server_default='',comment="待审核的语句内容")
    db_id = db.Column(db.Integer, db.ForeignKey('mysql_databases.id'))
    status = db.Column(db.String(16),nullable=False,server_default='',default='',comment="工单状态")
    is_execute = db.Column(db.SmallInteger,nullable=False,default=0,server_default='0',comment="工单是否已经执行")
    is_delete = db.Column(db.SmallInteger,nullable=False,default=0,server_default='0',comment="工单逻辑删除,0:正常，1：删除")
    audit_advise = db.Column(db.Text,nullable=False,default='',server_default='',comment='审核意见')
    introduction = db.Column(db.String(10),nullable=False,default='',server_default='',comment="工单简介")
    type = db.Column(db.String(6),nullable=False,default='',server_default='',comment="工单类型：DML，DDL")
    add_time = db.Column(db.DateTime, default=datetime.now, comment="提交时间", index=True)
    last_modify_time = db.Column(db.DateTime,nullable=False,default=datetime.now,onupdate=datetime.now,comment="最后变更时间")
    def __repr__(self):
        return '<Tickets %r >' % (self.id)

##############################消息##################################
###########################  Message ##########################
#Message
class Messages(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,comment="ID主键")
    title = db.Column(db.String(32),nullable=False,default='',server_default='',comment="标题")
    content = db.Column(db.String(256),nullable=False,default='',server_default='',comment="内容")
    sender = db.Column(db.String(32),nullable=False,default='',server_default='',index=True,comment="发件人")
    recipient = db.Column(db.String(32),nullable=False,default='',server_default='',index=True,comment="收件人")
    is_read = db.Column(db.SmallInteger(),nullable=False,default=0,server_default='0',comment="消息是否已读，1：是，0：否")
    add_time = db.Column(db.DateTime,default=datetime.now,comment="消息发送时间")
    last_modify_time = db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now,comment="最后更新时间")
    def __repr__(self):
        return '<Message %r>' % (self.title)



#操作日志
class Admin_Log(db.Model):
    __tablename__ = 'admin_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,comment="操作日志ID")
    username = db.Column(db.String(32),nullable=False,default='',server_default='',index=True,comment="操作人用户名")
    event = db.Column(db.String(128),nullable=False,default='',server_default='',comment="操作事件")
    add_time = db.Column(db.DateTime,default=datetime.now,index=True,comment="添加时间")
    last_modify_time = db.Column(db.DateTime,default=datetime.now,onupdate=True,index=True,comment="最后更新时间")
    def __repr__(self):
        return '<Admin_Log %r>' % (self.username)
#全局配置
class Options(db.Model):
    __tablename__ = "options"
    id = db.Column(db.SmallInteger,primary_key=True,autoincrement=True,comment="配置主键ID")
    site_name = db.Column(db.String(32),nullable=False,default='',server_default='',comment="站点名称")
    site_url = db.Column(db.String(32),nullable=False,default='',server_default='',comment="站点url")
    monitor_frequency = db.Column(db.SmallInteger,nullable=False,default='1',server_default='1',comment="监控频率分钟")
    email_on = db.Column(db.SmallInteger,nullable=False,default='1',server_default='1',comment="是否开启邮件报警")
    email_times = db.Column(db.SmallInteger,nullable=False,default='3',server_default='3',comment="邮件发送次数")
    email_sleep = db.Column(db.SmallInteger,nullable=False,default='30',server_default='30',comment="邮件报警达到次数后，休眠时间")
    receiver = db.Column(db.String(256),nullable=False,default='',server_default='',comment="邮件报警收件人地址;分号分割")
    smtp_host = db.Column(db.String(20),nullable=False,default='',server_default='',comment="SMTP主机")
    smtp_port = db.Column(db.String(20), nullable=False, default='', server_default='', comment="SMTP主机端口")
    smtp_user = db.Column(db.String(20), nullable=False, default='', server_default='', comment="SMTP账户")
    smtp_password = db.Column(db.String(32), nullable=False, default='', server_default='', comment="SMTP密码")
    add_time = db.Column(db.DateTime, default=datetime.now, index=True, comment="添加时间")
    last_modify_time = db.Column(db.DateTime, default=datetime.now, onupdate=True, index=True, comment="最后更新时间")
    def __repr__(self):
        return '<Option %r>' % (self.site_name)

if __name__ == '__main__':
    db.create_all()




