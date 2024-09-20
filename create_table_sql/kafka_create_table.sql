-- topic_name = "center"
-- group_name = "center_to_wms"
-- log_table = "kafka_center_to_wms"
-- alter table kafka_log.kafka_center_to_wms modify exec_step VARCHAR(1000) comment '执行记录';
-- alter table kafka_log.kafka_center_to_oms modify exec_step VARCHAR(1000) comment '执行记录';
-- alter table kafka_log.kafka_oms_to_wms modify exec_step VARCHAR(1000) comment '执行记录';


CREATE DATABASE kafka_log DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

drop table if exists kafka_log.kafka_center_to_wms;
CREATE TABLE kafka_log.kafka_center_to_wms(
     topic                      VARCHAR(255)   COMMENT 'kafka主题'
    ,table_id                   VARCHAR(255)   COMMENT '业务table'
    ,kafka_partition            INT            COMMENT 'kafka分区'
    ,kafka_offset               INT            COMMENT 'kafka-offset值'
    ,kafka_timestamp            BIGINT         COMMENT 'kafka-时间戳'
    ,serialized_value_size      INT            COMMENT 'kafka-序列化value的大小'
    ,kafka_value                TEXT           COMMENT 'value-json'
    ,exec_step                  VARCHAR(1000)  COMMENT '执行记录'
    ,exec_code                  INT            COMMENT '接口执行code信息'
    ,exec_status                VARCHAR(255)   COMMENT '接口执行返回信息'
    ,exec_time                  VARCHAR(255)   COMMENT '执行时间戳'
    ,create_time                DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
    ,modify_time                DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间'
    ,retry_count                INT DEFAULT 0  COMMENT '重试次数'
    ,PRIMARY KEY(kafka_offset)
)COMMENT "kafka的center队列数据推送wms"
ENGINE=INNODB CHARSET=utf8;

drop table if exists kafka_log.kafka_center_to_oms;
CREATE TABLE kafka_log.kafka_center_to_oms(
     topic                      VARCHAR(255)   COMMENT 'kafka主题'
    ,table_id                   VARCHAR(255)   COMMENT '业务table'
    ,kafka_partition            INT            COMMENT 'kafka分区'
    ,kafka_offset               INT            COMMENT 'kafka-offset值'
    ,kafka_timestamp            BIGINT         COMMENT 'kafka-时间戳'
    ,serialized_value_size      INT            COMMENT 'kafka-序列化value的大小'
    ,kafka_value                TEXT           COMMENT 'value-json'
    ,exec_step                  VARCHAR(1000)  COMMENT '执行记录'
    ,exec_code                  INT            COMMENT '接口执行code信息'
    ,exec_status                VARCHAR(255)   COMMENT '接口执行返回信息'
    ,exec_time                  VARCHAR(255)   COMMENT '执行时间戳'
    ,create_time                DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
    ,modify_time                DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间'
    ,retry_count                INT DEFAULT 0  COMMENT '重试次数'
    ,PRIMARY KEY(kafka_offset)
)COMMENT "kafka的center队列数据推送oms"
ENGINE=INNODB CHARSET=utf8;

drop table if exists kafka_log.kafka_oms_to_wms;
CREATE TABLE if not exists kafka_log.kafka_oms_to_wms(
     topic                      VARCHAR(255)   COMMENT 'kafka主题'
    ,table_id                   VARCHAR(255)   COMMENT '业务table'
    ,kafka_partition            INT            COMMENT 'kafka分区'
    ,kafka_offset               INT            COMMENT 'kafka-offset值'
    ,kafka_timestamp            BIGINT         COMMENT 'kafka-时间戳'
    ,serialized_value_size      INT            COMMENT 'kafka-序列化value的大小'
    ,kafka_value                TEXT           COMMENT 'value-json'
    ,exec_step                  VARCHAR(1000)  COMMENT '执行记录'
    ,exec_code                  INT            COMMENT '接口执行code信息'
    ,exec_status                VARCHAR(255)   COMMENT '接口执行返回信息'
    ,exec_time                  VARCHAR(255)   COMMENT '执行时间戳'
    ,create_time                DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
    ,modify_time                DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间'
    ,retry_count                INT DEFAULT 0  COMMENT '重试次数'
    ,PRIMARY KEY(kafka_offset)
)COMMENT "kafka的oms队列数据推送wms"
ENGINE=INNODB CHARSET=utf8;