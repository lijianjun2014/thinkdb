/*
Navicat MySQL Data Transfer

Source Server         : 本机
Source Server Version : 50554
Source Host           : localhost:3306
Source Database       : fthinkdb

Target Server Type    : MYSQL
Target Server Version : 50554
File Encoding         : 65001

Date: 2018-05-15 17:15:05
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for admin_log
-- ----------------------------
DROP TABLE IF EXISTS `admin_log`;
CREATE TABLE `admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '操作日志ID',
  `username` varchar(32) NOT NULL DEFAULT '' COMMENT '操作人用户名',
  `event` varchar(128) NOT NULL DEFAULT '' COMMENT '操作事件',
  `add_time` datetime DEFAULT NULL COMMENT '添加时间',
  `last_modify_time` datetime DEFAULT NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_admin_log_add_time` (`add_time`),
  KEY `ix_admin_log_username` (`username`),
  KEY `ix_admin_log_last_modify_time` (`last_modify_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for data_center
-- ----------------------------
DROP TABLE IF EXISTS `data_center`;
CREATE TABLE `data_center` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '数据中心ID',
  `name` varchar(32) NOT NULL DEFAULT '' COMMENT '数据中心名称',
  `introduction` varchar(64) NOT NULL DEFAULT '' COMMENT '数据中心简介',
  `add_time` datetime DEFAULT NULL COMMENT '添加时间',
  `last_modify_time` datetime DEFAULT NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for db_cluster
-- ----------------------------
DROP TABLE IF EXISTS `db_cluster`;
CREATE TABLE `db_cluster` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '集群主键ID',
  `name` varchar(64) NOT NULL DEFAULT '' COMMENT '名称',
  `status` varchar(6) NOT NULL DEFAULT 'online' COMMENT '状态',
  `introduction` varchar(256) NOT NULL DEFAULT '' COMMENT '简介',
  `applicant` varchar(16) NOT NULL DEFAULT '' COMMENT 'who applicate this cluster',
  `add_time` datetime DEFAULT NULL COMMENT '添加时间',
  `last_modify_time` datetime DEFAULT NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_db_cluster_name` (`name`),
  KEY `ix_db_cluster_applicant` (`applicant`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for messages
-- ----------------------------
DROP TABLE IF EXISTS `messages`;
CREATE TABLE `messages` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID主键',
  `title` varchar(32) NOT NULL DEFAULT '' COMMENT '标题',
  `content` varchar(256) NOT NULL DEFAULT '' COMMENT '内容',
  `sender` varchar(32) NOT NULL DEFAULT '' COMMENT '发件人',
  `recipient` varchar(32) NOT NULL DEFAULT '' COMMENT '收件人',
  `is_read` smallint(6) NOT NULL DEFAULT '0' COMMENT '消息是否已读，1：是，0：否',
  `add_time` datetime DEFAULT NULL COMMENT '消息发送时间',
  `last_modify_time` datetime DEFAULT NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_messages_sender` (`sender`),
  KEY `ix_messages_recipient` (`recipient`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for mysql_databases
-- ----------------------------
DROP TABLE IF EXISTS `mysql_databases`;
CREATE TABLE `mysql_databases` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '数据库ID',
  `name` varchar(32) NOT NULL DEFAULT '' COMMENT '名称(标识)',
  `cluster_id` int(11) DEFAULT NULL COMMENT '集群ID',
  `datacenter_id` int(11) DEFAULT NULL COMMENT '所属数据库中心',
  `version` varchar(16) NOT NULL DEFAULT '' COMMENT '版本号',
  `ip` varchar(16) NOT NULL DEFAULT '' COMMENT 'IP地址',
  `port` int(11) NOT NULL DEFAULT '0' COMMENT '端口',
  `db_user` varchar(32) NOT NULL DEFAULT '' COMMENT '数据库连接用户',
  `db_password` varchar(32) NOT NULL DEFAULT '' COMMENT '数据库连接密码',
  `is_master` smallint(6) NOT NULL DEFAULT '0' COMMENT '是否主库,0否1是',
  `is_slave` smallint(6) NOT NULL DEFAULT '0' COMMENT '是否从库,0否1是',
  `is_monitor` smallint(6) NOT NULL DEFAULT '0' COMMENT '是否监控,0否1是',
  `status` varchar(10) NOT NULL DEFAULT 'unknown' COMMENT 'active:正常,inactive：出错,unknown:未知状态',
  `applicant` varchar(16) NOT NULL DEFAULT '' COMMENT '申请人',
  `introduction` varchar(8) NOT NULL DEFAULT '' COMMENT '说明简介',
  `add_time` datetime DEFAULT NULL COMMENT '添加时间',
  `last_modify_time` datetime DEFAULT NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_mysql_databases_name` (`name`),
  KEY `cluster_id` (`cluster_id`),
  KEY `datacenter_id` (`datacenter_id`),
  KEY `ix_mysql_databases_ip` (`ip`),
  CONSTRAINT `mysql_databases_ibfk_1` FOREIGN KEY (`cluster_id`) REFERENCES `db_cluster` (`id`),
  CONSTRAINT `mysql_databases_ibfk_2` FOREIGN KEY (`datacenter_id`) REFERENCES `data_center` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for mysql_replication
-- ----------------------------
DROP TABLE IF EXISTS `mysql_replication`;
CREATE TABLE `mysql_replication` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '复制ID',
  `db_name` varchar(32) NOT NULL DEFAULT '' COMMENT '名称(标识)',
  `ip` varchar(16) NOT NULL DEFAULT '' COMMENT 'IP地址',
  `port` int(11) NOT NULL DEFAULT '0' COMMENT '端口',
  `read_only` varchar(4) NOT NULL DEFAULT '' COMMENT '只读',
  `gtid_mode` varchar(4) NOT NULL DEFAULT '' COMMENT 'GTID模式',
  `master_host` varchar(16) NOT NULL DEFAULT '' COMMENT '主库IP',
  `master_port` int(11) NOT NULL DEFAULT '0' COMMENT '主库端口',
  `slave_io_run` varchar(16) NOT NULL DEFAULT '' COMMENT '从库IO线程',
  `slave_sql_run` varchar(16) NOT NULL DEFAULT '' COMMENT '从库SQL线程',
  `delay` int(11) NOT NULL DEFAULT '0' COMMENT '从库延迟',
  `master_log_file` varchar(32) NOT NULL DEFAULT '' COMMENT '当前Master二进制文件名',
  `read_master_log_pos` varchar(32) NOT NULL DEFAULT '' COMMENT 'IO线程读取的当前Maste文件偏移量',
  `relay_master_log_file` varchar(32) NOT NULL DEFAULT '' COMMENT 'SQL线程执行到当前的Master日志的文件名',
  `exec_master_log_pos` varchar(32) NOT NULL DEFAULT '' COMMENT 'SQL线程执行到当前的Master日志偏移量',
  `add_time` datetime DEFAULT NULL COMMENT '添加时间',
  `last_modify_time` datetime DEFAULT NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_mysql_replication_db_name` (`db_name`),
  KEY `ix_mysql_replication_master_host` (`master_host`),
  KEY `ix_mysql_replication_ip` (`ip`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for mysql_replication_history
-- ----------------------------
DROP TABLE IF EXISTS `mysql_replication_history`;
CREATE TABLE `mysql_replication_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `mysql_replication_id` int(11) DEFAULT NULL COMMENT '主从复制表的ID',
  `db_name` varchar(32) NOT NULL COMMENT '名称(标识)',
  `ip` varchar(16) NOT NULL COMMENT 'IP地址',
  `port` int(11) NOT NULL COMMENT '端口',
  `read_only` varchar(4) NOT NULL DEFAULT '' COMMENT '只读',
  `gtid_mode` varchar(4) NOT NULL DEFAULT '' COMMENT 'GTID模式',
  `master_host` varchar(16) NOT NULL DEFAULT '' COMMENT '主库IP',
  `master_port` int(11) NOT NULL DEFAULT '0' COMMENT '主库端口',
  `slave_io_run` varchar(16) NOT NULL DEFAULT '' COMMENT '从库IO线程',
  `slave_sql_run` varchar(16) NOT NULL DEFAULT '' COMMENT '从库SQL线程',
  `delay` int(11) NOT NULL DEFAULT '0' COMMENT '从库延迟',
  `master_log_file` varchar(32) NOT NULL DEFAULT '' COMMENT '当前Master二进制文件名',
  `read_master_log_pos` varchar(32) NOT NULL DEFAULT '' COMMENT 'IO线程读取的当前Maste文件偏移量',
  `relay_master_log_file` varchar(32) NOT NULL DEFAULT '' COMMENT 'SQL线程执行到当前的Master日志的文件名',
  `exec_master_log_pos` varchar(32) NOT NULL DEFAULT '' COMMENT 'SQL线程执行到当前的Master日志偏移量',
  `add_time` datetime DEFAULT NULL COMMENT '添加时间',
  `last_modify_time` datetime DEFAULT NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_mysql_replication_history_master_host` (`master_host`),
  KEY `ix_mysql_replication_history_ip` (`ip`),
  KEY `ix_mysql_replication_history_db_name` (`db_name`),
  KEY `ix_mysql_replication_history_mysql_replication_id` (`mysql_replication_id`)
) ENGINE=InnoDB AUTO_INCREMENT=652 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for mysql_slow_query_review
-- ----------------------------
DROP TABLE IF EXISTS `mysql_slow_query_review`;
CREATE TABLE `mysql_slow_query_review` (
  `checksum` bigint(20) unsigned NOT NULL,
  `fingerprint` text NOT NULL,
  `sample` text NOT NULL,
  `first_seen` datetime DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL,
  `reviewed_by` varchar(20) DEFAULT NULL,
  `reviewed_on` datetime DEFAULT NULL,
  `comments` text,
  PRIMARY KEY (`checksum`),
  KEY `idx_checksum` (`checksum`) USING BTREE,
  KEY `idx_last_seen` (`last_seen`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for mysql_slow_query_review_history
-- ----------------------------
DROP TABLE IF EXISTS `mysql_slow_query_review_history`;
CREATE TABLE `mysql_slow_query_review_history` (
  `serverid_max` smallint(4) NOT NULL DEFAULT '0',
  `db_max` varchar(100) DEFAULT NULL,
  `user_max` varchar(100) DEFAULT NULL,
  `checksum` bigint(20) unsigned NOT NULL,
  `sample` text NOT NULL,
  `ts_min` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `ts_max` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `ts_cnt` float DEFAULT NULL,
  `Query_time_sum` float DEFAULT NULL,
  `Query_time_min` float DEFAULT NULL,
  `Query_time_max` float DEFAULT NULL,
  `Query_time_pct_95` float DEFAULT NULL,
  `Query_time_stddev` float DEFAULT NULL,
  `Query_time_median` float DEFAULT NULL,
  `Lock_time_sum` float DEFAULT NULL,
  `Lock_time_min` float DEFAULT NULL,
  `Lock_time_max` float DEFAULT NULL,
  `Lock_time_pct_95` float DEFAULT NULL,
  `Lock_time_stddev` float DEFAULT NULL,
  `Lock_time_median` float DEFAULT NULL,
  `Rows_sent_sum` float DEFAULT NULL,
  `Rows_sent_min` float DEFAULT NULL,
  `Rows_sent_max` float DEFAULT NULL,
  `Rows_sent_pct_95` float DEFAULT NULL,
  `Rows_sent_stddev` float DEFAULT NULL,
  `Rows_sent_median` float DEFAULT NULL,
  `Rows_examined_sum` float DEFAULT NULL,
  `Rows_examined_min` float DEFAULT NULL,
  `Rows_examined_max` float DEFAULT NULL,
  `Rows_examined_pct_95` float DEFAULT NULL,
  `Rows_examined_stddev` float DEFAULT NULL,
  `Rows_examined_median` float DEFAULT NULL,
  `Rows_affected_sum` float DEFAULT NULL,
  `Rows_affected_min` float DEFAULT NULL,
  `Rows_affected_max` float DEFAULT NULL,
  `Rows_affected_pct_95` float DEFAULT NULL,
  `Rows_affected_stddev` float DEFAULT NULL,
  `Rows_affected_median` float DEFAULT NULL,
  `Rows_read_sum` float DEFAULT NULL,
  `Rows_read_min` float DEFAULT NULL,
  `Rows_read_max` float DEFAULT NULL,
  `Rows_read_pct_95` float DEFAULT NULL,
  `Rows_read_stddev` float DEFAULT NULL,
  `Rows_read_median` float DEFAULT NULL,
  `Merge_passes_sum` float DEFAULT NULL,
  `Merge_passes_min` float DEFAULT NULL,
  `Merge_passes_max` float DEFAULT NULL,
  `Merge_passes_pct_95` float DEFAULT NULL,
  `Merge_passes_stddev` float DEFAULT NULL,
  `Merge_passes_median` float DEFAULT NULL,
  `InnoDB_IO_r_ops_min` float DEFAULT NULL,
  `InnoDB_IO_r_ops_max` float DEFAULT NULL,
  `InnoDB_IO_r_ops_pct_95` float DEFAULT NULL,
  `InnoDB_IO_r_ops_stddev` float DEFAULT NULL,
  `InnoDB_IO_r_ops_median` float DEFAULT NULL,
  `InnoDB_IO_r_bytes_min` float DEFAULT NULL,
  `InnoDB_IO_r_bytes_max` float DEFAULT NULL,
  `InnoDB_IO_r_bytes_pct_95` float DEFAULT NULL,
  `InnoDB_IO_r_bytes_stddev` float DEFAULT NULL,
  `InnoDB_IO_r_bytes_median` float DEFAULT NULL,
  `InnoDB_IO_r_wait_min` float DEFAULT NULL,
  `InnoDB_IO_r_wait_max` float DEFAULT NULL,
  `InnoDB_IO_r_wait_pct_95` float DEFAULT NULL,
  `InnoDB_IO_r_wait_stddev` float DEFAULT NULL,
  `InnoDB_IO_r_wait_median` float DEFAULT NULL,
  `InnoDB_rec_lock_wait_min` float DEFAULT NULL,
  `InnoDB_rec_lock_wait_max` float DEFAULT NULL,
  `InnoDB_rec_lock_wait_pct_95` float DEFAULT NULL,
  `InnoDB_rec_lock_wait_stddev` float DEFAULT NULL,
  `InnoDB_rec_lock_wait_median` float DEFAULT NULL,
  `InnoDB_queue_wait_min` float DEFAULT NULL,
  `InnoDB_queue_wait_max` float DEFAULT NULL,
  `InnoDB_queue_wait_pct_95` float DEFAULT NULL,
  `InnoDB_queue_wait_stddev` float DEFAULT NULL,
  `InnoDB_queue_wait_median` float DEFAULT NULL,
  `InnoDB_pages_distinct_min` float DEFAULT NULL,
  `InnoDB_pages_distinct_max` float DEFAULT NULL,
  `InnoDB_pages_distinct_pct_95` float DEFAULT NULL,
  `InnoDB_pages_distinct_stddev` float DEFAULT NULL,
  `InnoDB_pages_distinct_median` float DEFAULT NULL,
  `QC_Hit_cnt` float DEFAULT NULL,
  `QC_Hit_sum` float DEFAULT NULL,
  `Full_scan_cnt` float DEFAULT NULL,
  `Full_scan_sum` float DEFAULT NULL,
  `Full_join_cnt` float DEFAULT NULL,
  `Full_join_sum` float DEFAULT NULL,
  `Tmp_table_cnt` float DEFAULT NULL,
  `Tmp_table_sum` float DEFAULT NULL,
  `Tmp_table_on_disk_cnt` float DEFAULT NULL,
  `Tmp_table_on_disk_sum` float DEFAULT NULL,
  `Filesort_cnt` float DEFAULT NULL,
  `Filesort_sum` float DEFAULT NULL,
  `Filesort_on_disk_cnt` float DEFAULT NULL,
  `Filesort_on_disk_sum` float DEFAULT NULL,
  `last_modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`checksum`,`ts_min`,`ts_max`),
  KEY `idx_serverid_max` (`serverid_max`) USING BTREE,
  KEY `idx_checksum` (`checksum`) USING BTREE,
  KEY `idx_query_time_max` (`Query_time_max`) USING BTREE,
  KEY `idx_last_modify` (`last_modify_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for mysql_status
-- ----------------------------
DROP TABLE IF EXISTS `mysql_status`;
CREATE TABLE `mysql_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `db_name` varchar(32) NOT NULL DEFAULT '' COMMENT '名称(标识)',
  `ip` varchar(16) NOT NULL DEFAULT '' COMMENT 'IP地址',
  `port` int(11) NOT NULL DEFAULT '0' COMMENT '端口',
  `db_cluster_name` varchar(32) NOT NULL DEFAULT '' COMMENT '所属集群名称',
  `data_center_name` varchar(32) NOT NULL DEFAULT '' COMMENT '所属数据中心名称',
  `is_master` smallint(6) NOT NULL DEFAULT '0' COMMENT '是否主库,0否1是',
  `is_slave` smallint(6) NOT NULL DEFAULT '0' COMMENT '是否从库,0否1是',
  `uptime` int(11) NOT NULL DEFAULT '1' COMMENT '在线时长',
  `version` varchar(16) NOT NULL DEFAULT '' COMMENT '版本号',
  `max_connection` int(11) NOT NULL DEFAULT '1' COMMENT '最大连接数',
  `max_connect_errors` int(11) NOT NULL DEFAULT '1' COMMENT '最大连接数',
  `open_files_limit` int(11) NOT NULL DEFAULT '1' COMMENT '最大打开文件数',
  `open_files` int(11) NOT NULL DEFAULT '1' COMMENT '当前打开文件数',
  `table_open_cache` int(11) NOT NULL DEFAULT '1' COMMENT '表缓存数',
  `open_tables` int(11) NOT NULL DEFAULT '1' COMMENT '当前打开表数',
  `opened_tables` int(11) NOT NULL DEFAULT '1' COMMENT '当前打开表数',
  `max_tmp_tables` int(11) NOT NULL DEFAULT '1' COMMENT '临时表限制',
  `max_heap_table_size` int(11) NOT NULL DEFAULT '1' COMMENT '内存临时表限制',
  `max_allowed_packet` int(11) NOT NULL DEFAULT '1' COMMENT 'Packet大小',
  `threads_connected` int(11) NOT NULL DEFAULT '1' COMMENT '当前打开线程数',
  `threads_running` int(11) NOT NULL DEFAULT '1' COMMENT '当前活动线程数',
  `threads_created` int(11) NOT NULL DEFAULT '1' COMMENT '创建的线程数量',
  `threads_cached` int(11) NOT NULL DEFAULT '1' COMMENT '线程缓存数量',
  `connections` int(11) NOT NULL DEFAULT '1' COMMENT '连接数',
  `aborted_clients` int(11) NOT NULL DEFAULT '1' COMMENT '断开客户端数量',
  `aborted_connects` int(11) NOT NULL DEFAULT '1' COMMENT '断开的连接数',
  `created_tmp_tables` smallint(6) NOT NULL DEFAULT '1' COMMENT '创建的临时表数量',
  `created_tmp_disk_tables` smallint(6) NOT NULL DEFAULT '1' COMMENT '创建的磁盘临时表数量',
  `connections_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒连接数',
  `bytes_received_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒接收字节数',
  `bytes_sent_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒发送字节数',
  `com_select_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒查询量',
  `com_insert_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒写入量',
  `com_update_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒更新量',
  `com_delete_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒删除量',
  `com_commit_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒提交数',
  `com_rollback_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒回滚',
  `questions_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒处理的客户端发送的请求数',
  `queries_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒处理的请求数包括存储过程，事件等',
  `transaction_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒事务数',
  `created_tmp_tables_persecond` smallint(6) NOT NULL DEFAULT '1' COMMENT '每秒创建的临时表',
  `created_tmp_disk_tables_persecond` smallint(6) NOT NULL DEFAULT '1' COMMENT '每秒创建的磁盘临时表',
  `created_tmp_files_persecond` smallint(6) NOT NULL DEFAULT '1' COMMENT '每秒创建的临时文件数',
  `table_locks_immediate_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒获得锁数量',
  `table_locks_waited_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒的锁等待',
  `innodb_buffer_pool_pages_total` int(11) NOT NULL DEFAULT '1' COMMENT 'InnoDB总页数',
  `innodb_buffer_pool_pages_data` smallint(6) NOT NULL DEFAULT '1' COMMENT 'InnoDB使用中的页数量',
  `innodb_buffer_pool_pages_dirty` smallint(6) NOT NULL DEFAULT '1' COMMENT 'InnoDB脏数据的页数量',
  `innodb_buffer_pool_pages_flushed` smallint(6) NOT NULL DEFAULT '1' COMMENT '缓冲池请求刷新的页数量',
  `innodb_buffer_pool_pages_free` int(11) NOT NULL DEFAULT '1' COMMENT '空闲页数量',
  `innodb_buffer_pool_reads` int(11) NOT NULL DEFAULT '1' COMMENT 'Innodb从磁盘读取数',
  `innodb_buffer_pool_read_requests` int(11) NOT NULL DEFAULT '1' COMMENT 'Innodb从缓冲读取数',
  `innodb_row_lock_current_waits` int(11) NOT NULL DEFAULT '1' COMMENT 'InnoDB当前锁等待数',
  `innodb_row_lock_time_avg` int(11) NOT NULL DEFAULT '1' COMMENT '平均锁等待时长毫秒',
  `innodb_row_lock_waits` int(11) NOT NULL DEFAULT '1' COMMENT 'Innodb锁等待总量',
  `innodb_row_lock_time_max` int(11) NOT NULL DEFAULT '1' COMMENT 'InnoDB最大锁等待时长毫秒',
  `innodb_rows_inserted_persecond` int(11) NOT NULL DEFAULT '1' COMMENT 'InnoDB每秒新增行数',
  `innodb_rows_deleted_persecond` int(11) NOT NULL DEFAULT '1' COMMENT 'InnoDB每秒删除行数',
  `innodb_rows_updated_persecond` int(11) NOT NULL DEFAULT '1' COMMENT 'InnoDB每秒更新行数',
  `innodb_rows_reads_persecond` int(11) NOT NULL DEFAULT '1' COMMENT 'InnoDB每秒查询行数',
  `add_time` datetime DEFAULT NULL COMMENT '添加时间',
  `last_modify_time` datetime DEFAULT NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_mysql_status_db_name` (`db_name`),
  KEY `ix_mysql_status_db_cluster_name` (`db_cluster_name`),
  KEY `ix_mysql_status_data_center_name` (`data_center_name`),
  KEY `ix_mysql_status_ip` (`ip`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for mysql_status_history
-- ----------------------------
DROP TABLE IF EXISTS `mysql_status_history`;
CREATE TABLE `mysql_status_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `mysql_status_id` int(11) DEFAULT NULL COMMENT 'status表的主键,可以不用要，主要为了简化监控脚本的语句',
  `db_name` varchar(32) NOT NULL DEFAULT '' COMMENT '名称(标识)',
  `ip` varchar(16) NOT NULL DEFAULT '' COMMENT 'IP地址',
  `port` int(11) NOT NULL DEFAULT '0' COMMENT '端口',
  `db_cluster_name` varchar(32) NOT NULL DEFAULT '' COMMENT '所属集群名称',
  `data_center_name` varchar(32) NOT NULL DEFAULT '' COMMENT '所属数据中心名称',
  `is_master` smallint(6) NOT NULL DEFAULT '0' COMMENT '是否主库,0否1是',
  `is_slave` smallint(6) NOT NULL DEFAULT '0' COMMENT '是否从库,0否1是',
  `uptime` int(11) NOT NULL DEFAULT '1' COMMENT '在线时长',
  `version` varchar(16) NOT NULL DEFAULT '' COMMENT '版本号',
  `max_connection` int(11) NOT NULL DEFAULT '1' COMMENT '最大连接数',
  `max_connect_errors` int(11) NOT NULL DEFAULT '1' COMMENT '最大连接数',
  `open_files_limit` int(11) NOT NULL DEFAULT '1' COMMENT '最大打开文件数',
  `open_files` int(11) NOT NULL DEFAULT '1' COMMENT '当前打开文件数',
  `table_open_cache` int(11) NOT NULL DEFAULT '1' COMMENT '表缓存数',
  `open_tables` int(11) NOT NULL DEFAULT '1' COMMENT '当前打开表数',
  `opened_tables` int(11) NOT NULL DEFAULT '1' COMMENT '当前打开表数',
  `max_tmp_tables` int(11) NOT NULL DEFAULT '1' COMMENT '临时表限制',
  `max_heap_table_size` int(11) NOT NULL DEFAULT '1' COMMENT '内存临时表限制',
  `max_allowed_packet` int(11) NOT NULL DEFAULT '1' COMMENT 'Packet大小',
  `threads_connected` int(11) NOT NULL DEFAULT '1' COMMENT '当前打开线程数',
  `threads_running` int(11) NOT NULL DEFAULT '1' COMMENT '当前活动线程数',
  `threads_created` int(11) NOT NULL DEFAULT '1' COMMENT '创建的线程数量',
  `threads_cached` int(11) NOT NULL DEFAULT '1' COMMENT '线程缓存数量',
  `connections` int(11) NOT NULL DEFAULT '1' COMMENT '连接数',
  `aborted_clients` int(11) NOT NULL DEFAULT '1' COMMENT '断开客户端数量',
  `aborted_connects` int(11) NOT NULL DEFAULT '1' COMMENT '断开的连接数',
  `created_tmp_tables` int(11) NOT NULL DEFAULT '1' COMMENT '创建的临时表数量',
  `created_tmp_disk_tables` int(11) NOT NULL DEFAULT '1' COMMENT '创建的磁盘临时表数量',
  `connections_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒连接数',
  `bytes_received_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒接收字节数',
  `bytes_sent_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒发送字节数',
  `com_select_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒查询量',
  `com_insert_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒写入量',
  `com_update_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒更新量',
  `com_delete_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒删除量',
  `com_commit_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒提交数',
  `com_rollback_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒回滚',
  `questions_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒处理的客户端发送的请求数',
  `queries_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒处理的请求数包括存储过程，事件等',
  `transaction_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒事务数',
  `created_tmp_tables_persecond` smallint(6) NOT NULL DEFAULT '1' COMMENT '每秒创建的临时表',
  `created_tmp_disk_tables_persecond` smallint(6) NOT NULL DEFAULT '1' COMMENT '每秒创建的磁盘临时表',
  `created_tmp_files_persecond` smallint(6) NOT NULL DEFAULT '1' COMMENT '每秒创建的临时文件数',
  `table_locks_immediate_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒获得锁数量',
  `table_locks_waited_persecond` int(11) NOT NULL DEFAULT '1' COMMENT '每秒的锁等待',
  `innodb_buffer_pool_pages_total` int(11) NOT NULL DEFAULT '1' COMMENT 'InnoDB总页数',
  `innodb_buffer_pool_pages_data` smallint(6) NOT NULL DEFAULT '1' COMMENT 'InnoDB使用中的页数量',
  `innodb_buffer_pool_pages_dirty` smallint(6) NOT NULL DEFAULT '1' COMMENT 'InnoDB脏数据的页数量',
  `innodb_buffer_pool_pages_flushed` smallint(6) NOT NULL DEFAULT '1' COMMENT '缓冲池请求刷新的页数量',
  `innodb_buffer_pool_pages_free` int(11) NOT NULL DEFAULT '1' COMMENT '空闲页数量',
  `innodb_buffer_pool_reads` int(11) NOT NULL DEFAULT '1' COMMENT 'Innodb从磁盘读取数',
  `innodb_buffer_pool_read_requests` int(11) NOT NULL DEFAULT '1' COMMENT 'Innodb从缓冲读取数',
  `innodb_row_lock_current_waits` int(11) NOT NULL DEFAULT '1' COMMENT 'InnoDB当前锁等待数',
  `innodb_row_lock_time_avg` int(11) NOT NULL DEFAULT '1' COMMENT '平均锁等待时长毫秒',
  `innodb_row_lock_waits` int(11) NOT NULL DEFAULT '1' COMMENT 'Innodb锁等待总量',
  `innodb_row_lock_time_max` int(11) NOT NULL DEFAULT '1' COMMENT 'InnoDB最大锁等待时长毫秒',
  `innodb_rows_inserted_persecond` int(11) NOT NULL DEFAULT '1' COMMENT 'InnoDB每秒新增行数',
  `innodb_rows_deleted_persecond` int(11) NOT NULL DEFAULT '1' COMMENT 'InnoDB每秒删除行数',
  `innodb_rows_updated_persecond` int(11) NOT NULL DEFAULT '1' COMMENT 'InnoDB每秒更新行数',
  `innodb_rows_reads_persecond` int(11) NOT NULL DEFAULT '1' COMMENT 'InnoDB每秒查询行数',
  `add_time` datetime DEFAULT NULL COMMENT '添加时间',
  `last_modify_time` datetime DEFAULT NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`),
  KEY `ix_mysql_status_history_db_cluster_name` (`db_cluster_name`),
  KEY `ix_mysql_status_history_data_center_name` (`data_center_name`),
  KEY `idx_db_name_last_time` (`db_name`,`last_modify_time`)
) ENGINE=InnoDB AUTO_INCREMENT=1472 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for tickets
-- ----------------------------
DROP TABLE IF EXISTS `tickets`;
CREATE TABLE `tickets` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '工单ID',
  `tickets_num` bigint(20) NOT NULL DEFAULT '0' COMMENT '工单编号',
  `applicant` varchar(16) NOT NULL DEFAULT '' COMMENT '提交人',
  `auditor` varchar(16) NOT NULL DEFAULT '' COMMENT '审核人',
  `sqlcontent` text NOT NULL COMMENT '待审核的语句内容',
  `db_id` int(11) DEFAULT NULL,
  `status` varchar(16) NOT NULL DEFAULT '' COMMENT '工单状态',
  `is_execute` smallint(6) NOT NULL DEFAULT '0' COMMENT '工单是否已经执行',
  `is_delete` smallint(6) NOT NULL DEFAULT '0' COMMENT '工单逻辑删除,0:正常，1：删除',
  `audit_advise` text NOT NULL COMMENT '审核意见',
  `introduction` varchar(10) NOT NULL DEFAULT '' COMMENT '工单简介',
  `type` varchar(6) NOT NULL DEFAULT '' COMMENT '工单类型：DML，DDL',
  `add_time` datetime DEFAULT NULL COMMENT '提交时间',
  `last_modify_time` datetime NOT NULL COMMENT '最后变更时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_tickets_tickets_num` (`tickets_num`),
  KEY `db_id` (`db_id`),
  KEY `ix_tickets_add_time` (`add_time`),
  KEY `ix_tickets_applicant` (`applicant`),
  CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`db_id`) REFERENCES `mysql_databases` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(64) NOT NULL DEFAULT '' COMMENT '用户名',
  `password` varchar(128) NOT NULL DEFAULT '' COMMENT '密码',
  `real_name` varchar(16) NOT NULL DEFAULT '' COMMENT '真实姓名',
  `email` varchar(64) NOT NULL DEFAULT '' COMMENT '邮件地址',
  `status` varchar(10) NOT NULL DEFAULT '' COMMENT '状态',
  `group_id` int(11) DEFAULT NULL COMMENT '用户组ID',
  `privileges` varchar(256) NOT NULL DEFAULT '' COMMENT 'url权限',
  `add_time` datetime DEFAULT NULL COMMENT '添加日期',
  `last_modify_time` datetime DEFAULT NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  UNIQUE KEY `ix_users_username` (`username`),
  KEY `group_id` (`group_id`),
  KEY `ix_users_status` (`status`),
  KEY `ix_users_real_name` (`real_name`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `user_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for user_group
-- ----------------------------
DROP TABLE IF EXISTS `user_group`;
CREATE TABLE `user_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户组ID',
  `group_name` varchar(32) NOT NULL DEFAULT '' COMMENT '组名称',
  `introduction` varchar(16) NOT NULL DEFAULT '' COMMENT '用户组简介',
  `add_time` datetime DEFAULT NULL COMMENT '添加时间',
  `last_modify_time` datetime DEFAULT NULL COMMENT '最后更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_name` (`group_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
