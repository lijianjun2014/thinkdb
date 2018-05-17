#! /bin/evn python
#coding:utf8

import datetime
import time
import pymysql
import contextlib
import logging
from multiprocessing import Process

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'thinkdb',
    'password': '123456',
    'db': 'thinkdb',
    'charset': 'utf8mb4',
    #'cursorclass': pymysql.cursors.DictCursor,
    }

@contextlib.contextmanager
def mysql(ip="127.0.0.1",port=3306,username="thinkdb",password="123456",db_name="information_schema"):
    conn = pymysql.connect(host=ip,port=int(port),user=username,password=password,connect_timeout=10,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    if db_name != '':
        conn.select_db(db_name)
    else:
        conn.select_db("information_schema")
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()

def mysql_query(ip,port,username,password,db_name,sql_content,paras):
    with mysql(ip,port,username,password,db_name) as cursor:
        if paras != '':
            row_count = cursor.execute(sql_content,paras)
        else:
            row_count = cursor.execute(sql_content)
        if row_count == 0:
            result = 0
        else:
            result = cursor.fetchall()
        return result

def thinkdb_update(sql_content,paras):
    with mysql(db_name="thinkdb") as cursor:
        if paras != '':
            cursor.execute(sql_content,paras)
        else:
            cursor.execute(sql_content)
#监控数据存放库的查询
def thinkdb_query(sql_content,paras):
    with mysql(db_name="thinkdb") as cursor:
        if paras != '':
            row_count = cursor.execute(sql_content,paras)
        else:
            row_count = cursor.execute(sql_content)
        if row_count == 0:
            return 0
        else:
            return cursor.fetchall()

def print_sql(ip,port,username,password):
    print(ip,port,username,password)
#获取需要监控的服务器信息

#获取服务器状态信息
def get_mysql_status(ip,port,username,password):
    mysql_status={}
    status = mysql_query(ip,port,username,password,'information_schema',"show global status;",'')
    for i in status:
        mysql_status[i['Variable_name']]=i['Value']
    return mysql_status

#获取服务器参数信息
def get_mysql_variables(ip,port,username,password):
    mysql_variables={}
    variables = mysql_query(ip,port,username,password,'information_schema',"show global variables;",'')
    for i in variables:
        mysql_variables[i['Variable_name']]=i['Value']
    return mysql_variables

#主从判断
def is_master(ip,port,username,password):
    sql_content = "show slave hosts;"
    is_master = mysql_query(ip,port,username,password,'information_schema',sql_content,'')
    if is_master == 0:
        return 0
    else:
        return 1

def is_slave(ip,port,username,password):
    sql_content = "show slave status;"
    slave_info = mysql_query(ip,port,username,password,'information_schema',sql_content,'')
    if slave_info == 0:
        return 0
    else:
        return slave_info

def check_mysql(name,ip,port,username,password,monitor_start_time):
    mysql_status = get_mysql_status(ip,port,username,password)
    mysql_variables = get_mysql_variables(ip,port,username,password)
    master_info = is_master(ip,port,username,password)
    slave_info = is_slave(ip,port,username,password)
    exists_in_replication = thinkdb_query("select id from mysql_replication where db_name = %s",(name))
    time.sleep(5)
    mysql_status2 = get_mysql_status(ip, port, username, password)
    def perseconds(para):
        result = (int(mysql_status2[para]) - int(mysql_status[para]))/5
        return result

    #获取mysql参数值
    version = mysql_variables['version']
    max_connection = mysql_variables['max_connections']
    max_connect_errors = mysql_variables['max_connect_errors']
    open_files_limit = mysql_variables['open_files_limit']
    table_open_cache = mysql_variables['table_open_cache']
    max_tmp_tables = mysql_variables['max_tmp_tables']
    max_heap_table_size = mysql_variables['max_heap_table_size']
    max_allowed_packet = mysql_variables['max_allowed_packet']
    read_only = mysql_variables['read_only']
    if float(version[0:3]) < 5.6:
        gtid_mode = "不支持"
    else:
        gtid_mode = mysql_variables['gtid_mode']
    #获取MySQL状态值
    uptime = mysql_status["Uptime"]
    open_files = mysql_status['Open_files']
    open_tables = mysql_status['Open_tables']
    opened_tables = mysql_status['Opened_tables']
    threads_connected = mysql_status['Threads_connected']
    threads_running = mysql_status['Threads_running']
    threads_created = mysql_status['Threads_created']
    threads_cached = mysql_status['Threads_cached']
    connections = mysql_status['Connections']
    aborted_clients = mysql_status['Aborted_clients']
    aborted_connects = mysql_status['Aborted_connects']
    created_tmp_tables = mysql_status['Created_tmp_tables']
    created_tmp_disk_tables = mysql_status['Created_tmp_disk_tables']
    innodb_buffer_pool_pages_total = mysql_status["Innodb_buffer_pool_pages_total"]
    innodb_buffer_pool_pages_data = mysql_status["Innodb_buffer_pool_pages_data"]
    innodb_buffer_pool_pages_dirty = mysql_status["Innodb_buffer_pool_pages_dirty"]
    innodb_buffer_pool_pages_flushed = mysql_status["Innodb_buffer_pool_pages_flushed"]
    innodb_buffer_pool_pages_free = mysql_status["Innodb_buffer_pool_pages_free"]
    innodb_buffer_pool_reads = mysql_status["Innodb_buffer_pool_reads"]
    innodb_buffer_pool_read_requests = mysql_status["Innodb_buffer_pool_read_requests"]
    innodb_row_lock_current_waits = mysql_status["Innodb_row_lock_current_waits"]
    innodb_row_lock_time_avg = mysql_status["Innodb_row_lock_time_avg"]
    innodb_row_lock_waits = mysql_status["Innodb_row_lock_waits"]
    innodb_row_lock_time_max = mysql_status["Innodb_row_lock_time_max"]
    #获取每秒增量
    connections_persecond = perseconds("Connections")
    bytes_received_persecond =perseconds("Bytes_received")
    bytes_sent_persecond = perseconds("Bytes_sent")
    com_select_persecond = perseconds("Com_select")
    com_insert_persecond = perseconds("Com_insert")
    com_update_persecond = perseconds("Com_update")
    com_delete_persecond = perseconds("Com_delete")
    com_commit_persecond = perseconds("Com_commit")
    com_rollback_persecond = perseconds("Com_rollback")
    questions_persecond = perseconds("Questions")
    queries_persecond = perseconds("Queries")
    transaction_persecond = com_commit_persecond + com_rollback_persecond
    created_tmp_tables_persecond = perseconds("Created_tmp_tables")
    created_tmp_disk_tables_persecond = perseconds("Created_tmp_disk_tables")
    created_tmp_files_persecond = perseconds("Created_tmp_files")
    table_locks_immediate_persecond = perseconds("Table_locks_immediate")
    table_locks_waited_persecond = perseconds("Table_locks_waited")
    innodb_rows_inserted_persecond = perseconds("Innodb_rows_inserted")
    innodb_rows_deleted_persecond = perseconds("Innodb_rows_deleted")
    innodb_rows_updated_persecond = perseconds("Innodb_rows_updated")
    innodb_rows_reads_persecond = perseconds("Innodb_rows_read")
    #获取主从复制信息
    if slave_info != 0:
        master_host = slave_info[0]['Master_Host']
        master_port = slave_info[0]['Master_Port']
        slave_io_run = slave_info[0]['Slave_IO_Running']
        slave_sql_run = slave_info[0]['Slave_SQL_Running']
        delay = int(slave_info[0]['Seconds_Behind_Master'])
        master_log_file = slave_info[0]['Master_Log_File']
        relay_master_log_file = slave_info[0]['Relay_Master_Log_File']
        read_master_log_pos = slave_info[0]['Read_Master_Log_Pos']
        exec_master_log_pos = slave_info[0]['Exec_Master_Log_Pos']
        #处理MySQL_Replication表
        if exists_in_replication == 0:
            sql_content = "insert into mysql_replication select '',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"
            paras = (name,ip,port,read_only,gtid_mode,master_host,master_port,slave_io_run,slave_sql_run,delay,master_log_file,read_master_log_pos,relay_master_log_file,exec_master_log_pos,monitor_start_time,monitor_start_time)
            thinkdb_update(sql_content,paras)
        else:
            sql_content = "update mysql_replication set master_host=%s,master_port = %s,read_only=%s,gtid_mode=%s,slave_io_run=%s,slave_sql_run=%s,delay=%s,master_log_file=%s,relay_master_log_file=%s,read_master_log_pos=%s,exec_master_log_pos=%s,last_modify_time=%s where db_name = %s"
            paras = (master_host, master_port, read_only, gtid_mode, slave_io_run, slave_sql_run, delay,
                     master_log_file, relay_master_log_file, read_master_log_pos, exec_master_log_pos,monitor_start_time,name)
            thinkdb_update(sql_content, paras)


    #写入监控表结果
    sql_content = "update mysql_status set version=%s,max_connection=%s,max_connect_errors=%s,open_files_limit=%s,table_open_cache=%s,max_tmp_tables=%s,max_heap_table_size=%s,max_allowed_packet=%s,uptime=%s,open_files=%s,open_tables=%s,opened_tables=%s,threads_connected=%s,threads_running=%s,threads_created=%s,threads_cached=%s,connections=%s,aborted_clients=%s,aborted_connects=%s,innodb_buffer_pool_pages_total=%s,innodb_buffer_pool_pages_data=%s,innodb_buffer_pool_pages_dirty=%s,innodb_buffer_pool_pages_flushed=%s,innodb_buffer_pool_pages_free=%s,innodb_buffer_pool_reads=%s,innodb_buffer_pool_read_requests=%s,innodb_row_lock_current_waits=%s,innodb_row_lock_time_avg=%s,innodb_row_lock_waits=%s,innodb_row_lock_time_max=%s,connections_persecond=%s,bytes_received_persecond=%s,bytes_sent_persecond=%s,com_select_persecond=%s,com_insert_persecond=%s,com_update_persecond=%s,com_delete_persecond=%s,com_commit_persecond=%s,com_rollback_persecond=%s,questions_persecond=%s,queries_persecond=%s,transaction_persecond=%s,created_tmp_tables_persecond=%s,created_tmp_disk_tables_persecond=%s,created_tmp_files_persecond=%s,table_locks_immediate_persecond=%s,table_locks_waited_persecond=%s,innodb_rows_inserted_persecond=%s,innodb_rows_deleted_persecond=%s,innodb_rows_updated_persecond=%s,innodb_rows_reads_persecond=%s,last_modify_time=%s,created_tmp_disk_tables=%s,created_tmp_tables=%s where db_name = %s;"
    paras = (version,max_connection,max_connect_errors,open_files_limit,table_open_cache,max_tmp_tables,max_heap_table_size,max_allowed_packet,uptime,open_files,open_tables,opened_tables,threads_connected,threads_running,threads_created,threads_cached,connections,aborted_clients,aborted_connects,innodb_buffer_pool_pages_total,innodb_buffer_pool_pages_data,innodb_buffer_pool_pages_dirty,innodb_buffer_pool_pages_flushed,innodb_buffer_pool_pages_free,innodb_buffer_pool_reads,innodb_buffer_pool_read_requests,innodb_row_lock_current_waits,innodb_row_lock_time_avg,innodb_row_lock_waits,innodb_row_lock_time_max,connections_persecond,bytes_received_persecond,bytes_sent_persecond,com_select_persecond,com_insert_persecond,com_update_persecond,com_delete_persecond,com_commit_persecond,com_rollback_persecond,questions_persecond,queries_persecond,transaction_persecond,created_tmp_tables_persecond,created_tmp_disk_tables_persecond,created_tmp_files_persecond,table_locks_immediate_persecond,table_locks_waited_persecond,innodb_rows_inserted_persecond,innodb_rows_deleted_persecond,innodb_rows_updated_persecond,innodb_rows_reads_persecond,monitor_start_time,created_tmp_disk_tables,created_tmp_tables,name)
    thinkdb_update(sql_content,paras)
    #更新mysql_databases表的主从信息字段

    if master_info == 0:
        if slave_info == 0:
            sql_content = "update mysql_databases A join mysql_status B on A.name = B.db_name set A.status='active',B.is_master =0,B.is_slave=0,A.is_master =0,A.is_slave=0 where A.name = %s"
            paras = (name)
            thinkdb_update(sql_content, paras)
        else:
            sql_content = "update mysql_databases A join mysql_status B on A.name = B.db_name set A.status='active',B.is_master =0,B.is_slave=1,A.is_master =0,A.is_slave=1 where A.name = %s"
            paras = (name)
            thinkdb_update(sql_content,paras)
    else:
        if slave_info == 0:
            sql_content = "update mysql_databases A join mysql_status B on A.name = B.db_name set A.status='active',B.is_master =1,B.is_slave=0,A.is_master =1,A.is_slave=0 where A.name = %s"
            paras = (name)
            thinkdb_update(sql_content, paras)
        else:
            sql_content = "update mysql_databases A join mysql_status B on A.name = B.db_name set A.status='active',B.is_master =1,B.is_slave=1,A.is_master =1,A.is_slave=1 where A.name = %s"
            paras = (name)
            thinkdb_update(sql_content, paras)

def insert_status_history_data():
    # 转存status表的数据去历史表
    sql_content = "insert into mysql_status_history select '',A.* from mysql_status A;"
    thinkdb_update(sql_content, '')
    sql_content = "insert into mysql_replication_history select '',A.* from mysql_replication A;"
    thinkdb_update(sql_content,'')
def main():
    servers = mysql_query('127.0.0.1','3306','thinkdb','123456','thinkdb',"select name,ip,port,db_user,db_password from mysql_databases where is_monitor = %s;",1)
    processlist=[]
    monitor_start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if servers:
        for i in servers:
            name = i['name']
            ip = i['ip']
            port = i['port']
            username = i['db_user']
            password = i['db_password']
            process = Process(target=check_mysql,args=(name,ip,port,username,password,monitor_start_time))
            processlist.append(process)
        for x in processlist:
            x.start()
        time.sleep(10)
        for x in processlist:
            x.terminate()
        for x in processlist:
            x.join()
    else:
        logging.warning("check mysql: not found any servers!")


if __name__ == "__main__":
    main()
    insert_status_history_data()