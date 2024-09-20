CREATE DATABASE sharkbox_transaction DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'sharkbox_transaction'@'%' IDENTIFIED BY 'sharkbox@pro@888';
GRANT ALL ON sharkbox_transaction.* TO 'sharkbox_transaction'@'%';
FLUSH PRIVILEGES;

CREATE TABLE sharkbox_transaction.global_transaction(
     t_id                    VARCHAR(255)   COMMENT '事务id'
    ,app_name                VARCHAR(255)   COMMENT '事务发起方模块名'
    ,call_info               TEXT           COMMENT '接口参数--json格式'
    ,api_state               INT            COMMENT '监控程序状态,1:挂起,4:执行成功'
    ,main_state              INT            COMMENT '事务发起方-入口程序状态,0:未执行,1:执行失败,2:执行成功'
    ,create_time             DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
    ,modify_time             DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间'
    ,retry_count             INT DEFAULT 0  COMMENT '重试次数'
    ,PRIMARY KEY(t_id)
)COMMENT "全局事务处理表"
ENGINE=INNODB CHARSET=utf8;