import os
# =============================
# 📋 ClickHouse 表注册（和 MySQL 一样使用）
# =============================

# 1. 日志主表
ROOT_PATH = os.getenv("ROOT_PATH", "/monitor")

register_clickhouse_table(
    sql="""
    CREATE TABLE IF NOT EXISTS logs_with_pri
    (
        `uid` String DEFAULT concat(toString(toUnixTimestamp(timestamp)), leftPad(toString(sipHash64(timestamp, host, message) % 1000000000), 9, '0')),
        `timestamp` DateTime,
        `host` String,
        `ip` String,
        `severity` String,
        `message` String,
        `tags` Array(String),
        `file` String,
        `pri` String,
        `facility` String,
        INDEX idx_uid uid TYPE bloom_filter GRANULARITY 1
    )
    ENGINE = MergeTree
    PARTITION BY toYYYYMMDD(timestamp)
    ORDER BY (timestamp,
    ip,
    severity)
    TTL timestamp + toIntervalDay(90)
    SETTINGS index_granularity = 8192;
    """,
    table_name="logs_with_pri"
)

register_clickhouse_table(
    sql="""
    CREATE TABLE IF NOT EXISTS logs_no_pri
    (
        `uid` String DEFAULT concat(toString(toUnixTimestamp(timestamp)), leftPad(toString(sipHash64(timestamp, host, message) % 1000000000), 9, '0')),
        `timestamp` DateTime,
        `host` String,
        `ip` String,
        `severity` String,
        `message` String,
        `tags` Array(String),
        `file` String,
        `pri` String,
        `facility` String,
        INDEX idx_uid uid TYPE bloom_filter GRANULARITY 1
    )
    ENGINE = MergeTree
    PARTITION BY toYYYYMMDD(timestamp)
    ORDER BY (timestamp,
    ip,
    severity)
    TTL timestamp + toIntervalDay(90)
    SETTINGS index_granularity = 8192;
    """,
    table_name="logs_no_pri"
)

register_clickhouse_table(
    sql="""
    CREATE TABLE IF NOT EXISTS logs_with_pri_zabbix
    (
        `uid` String DEFAULT concat(toString(toUnixTimestamp(timestamp)), leftPad(toString(sipHash64(timestamp, host, message) % 1000000000), 9, '0')),
        `timestamp` DateTime,
        `host` String,
        `ip` String,
        `severity` String,
        `message` String,
        `tags` Array(String),
        `file` String,
        `pri` String,
        `facility` String,
        INDEX idx_uid uid TYPE bloom_filter GRANULARITY 1
    )
    ENGINE = MergeTree
    PARTITION BY toYYYYMMDD(timestamp)
    ORDER BY (timestamp,
    ip,
    severity)
    TTL timestamp + toIntervalDay(90)
    SETTINGS index_granularity = 8192;
    """,
    table_name="logs_with_pri_zabbix"
)

register_clickhouse_table(
    sql="""
    CREATE TABLE IF NOT EXISTS logs_no_pri_zabbix
    (
        `uid` String DEFAULT concat(toString(toUnixTimestamp(timestamp)), leftPad(toString(sipHash64(timestamp, host, message) % 1000000000), 9, '0')),
        `timestamp` DateTime,
        `host` String,
        `ip` String,
        `severity` String,
        `message` String,
        `tags` Array(String),
        `file` String,
        `pri` String,
        `facility` String,
        INDEX idx_uid uid TYPE bloom_filter GRANULARITY 1
    )
    ENGINE = MergeTree
    PARTITION BY toYYYYMMDD(timestamp)
    ORDER BY (timestamp,
    ip,
    severity)
    TTL timestamp + toIntervalDay(90)
    SETTINGS index_granularity = 8192;
    """,
    table_name="logs_no_pri_zabbix"
)

# =============================
# 📋 系统配置表注册
# =============================

# 1. 筛选收藏表
register_system_table(
    sql="""
    CREATE TABLE IF NOT EXISTS `filter_favorites` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `table_name` varchar(255) NOT NULL COMMENT '表名',
        `name` varchar(100) NOT NULL COMMENT '标签名称',
        `filter_expr` text COMMENT '筛选表达式',
        `sort_field` varchar(100) DEFAULT NULL COMMENT '排序字段',
        `sort_order` varchar(10) DEFAULT 'DESC' COMMENT '排序方向',
        `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`),
        KEY `idx_table_name` (`table_name`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='筛选收藏表';
    """,
    table_name="filter_favorites"  #  如果 SQL 解析失败，手动指定表名
)

# 2. 任务管理表（如果需要）
register_system_table(
    sql="""
    CREATE TABLE IF NOT EXISTS `pipeline_tasks` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `task_id` varchar(100) NOT NULL COMMENT '任务ID',
        `task_name` varchar(255) DEFAULT NULL COMMENT '任务名称',
        `status` varchar(20) DEFAULT 'pending' COMMENT '状态',
        `progress` int(11) DEFAULT 0 COMMENT '进度',
        `result` text COMMENT '执行结果',
        `error` text COMMENT '错误信息',
        `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
        `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`),
        UNIQUE KEY `uk_task_id` (`task_id`),
        KEY `idx_status` (`status`),
        KEY `idx_created_at` (`created_at`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Pipeline任务表';
    """,
    table_name="pipeline_tasks"  #  如果 SQL 解析失败，手动指定表名
)

# 3. 终端执行历史表（作为系统表）
register_system_table(
    sql="""
    CREATE TABLE IF NOT EXISTS `terminal_executions` (
        `id` int AUTO_INCREMENT PRIMARY KEY,
        `task_id` varchar(100) NOT NULL COMMENT '任务ID',
        `table_name` varchar(100) NOT NULL COMMENT '关联的表名/视图名',
        `command` text COMMENT '执行的命令',
        `status` varchar(20) DEFAULT 'pending' COMMENT '执行状态',
        `stdout` longtext COMMENT '标准输出',
        `stderr` longtext COMMENT '错误输出',
        `exit_code` int DEFAULT NULL COMMENT '退出码',
        `execution_time` float DEFAULT 0 COMMENT '执行耗时(秒)',
        `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
        INDEX `idx_task_id` (`task_id`),
        INDEX `idx_table_name` (`table_name`),
        INDEX `idx_status` (`status`),
        INDEX `idx_created_at` (`created_at`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='终端执行历史记录';
    """,
    table_name="terminal_executions",
)

# 4. 用户配置表（示例）
register_system_table(
    sql="""
    CREATE TABLE IF NOT EXISTS `user_preferences` (
        `id` int AUTO_INCREMENT PRIMARY KEY,
        `user_id` varchar(100) NOT NULL COMMENT '用户标识',
        `pref_key` varchar(100) NOT NULL COMMENT '配置键',
        `pref_value` text COMMENT '配置值',
        `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
        `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY `uk_user_key` (`user_id`, `pref_key`),
        INDEX `idx_user_id` (`user_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户配置表';
    """,
    table_name="user_preferences",
)

register_system_table(
    sql="""
    CREATE TABLE IF NOT EXISTS `pipeline_executions` (
        `id` int AUTO_INCREMENT PRIMARY KEY,
        `task_id` varchar(100) NOT NULL COMMENT '任务ID',
        `table_name` varchar(100) DEFAULT NULL COMMENT '关联的表名',
        `updated_tables` varchar(500) DEFAULT NULL COMMENT '所有被更新的表名(逗号分隔)',
        `virtual_table_name` varchar(100) DEFAULT NULL COMMENT '虚拟表名',
        `status` varchar(20) DEFAULT 'pending' COMMENT '执行状态',
        `progress` int DEFAULT 0 COMMENT '进度',
        `current_step` varchar(50) DEFAULT '' COMMENT '当前步骤',
        `message` text COMMENT '状态消息',
        `excel_file` varchar(500) DEFAULT NULL COMMENT 'Excel文件路径',
        `import_result` text COMMENT '导入结果JSON',
        `stdout` longtext COMMENT '标准输出',
        `stderr` longtext COMMENT '错误输出',
        `logs` longtext COMMENT '执行日志',
        `exit_code` int DEFAULT NULL COMMENT '退出码',
        `execution_time` float DEFAULT 0 COMMENT '执行耗时(秒)',
        `error` text COMMENT '错误信息',
        `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
        `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
        INDEX `idx_task_id` (`task_id`),
        INDEX `idx_table_name` (`table_name`),
        INDEX `idx_status` (`status`),
        INDEX `idx_created_at` (`created_at`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Pipeline任务执行历史记录';
    """,
    table_name="pipeline_executions",
)

# 父菜单图标映射
MENU_GROUP_ICONS = {
    "积压监控": "📦",
    "超时监控": "⏰",
    "磁盘监控": "💾",
    "进程监控": "🌐",
    "IPMI监控": "📈",
    "Zabbix监控": "/icons/zabbix.svg",
    "终端工具": "🖥️",
    "自定义监控": "⚙️",
    "趋势分析": "📈",  #  添加趋势分析分组
}

# 父菜单图标映射
MENU_GROUP_ICONS = {
    "积压监控": f"{ROOT_PATH}/static/icons/目录积压监控.svg",
    "超时监控": f"{ROOT_PATH}/static/icons/目录超时监控.svg",
    "磁盘监控": f"{ROOT_PATH}/static/icons/Linux磁盘监控.svg",
    "进程监控": f"{ROOT_PATH}/static/icons/Linux进程监控.svg",
    "IPMI监控": f"{ROOT_PATH}/static/icons/IPMI监控.svg",
    "Zabbix监控": f"{ROOT_PATH}/static/icons/zabbix.svg",
    "终端工具": f"{ROOT_PATH}/static/icons/终端工具.svg",
    "自定义监控": f"{ROOT_PATH}/static/icons/自定义监控.svg",
    "趋势分析": f"{ROOT_PATH}/static/icons/数据趋势图.svg",
}

# app/models/table_configs.py

# =============================
# 🎨 UI 图标配置
# =============================

UI_ICONS = {
    "欢迎": f"{ROOT_PATH}/static/icons/欢迎.svg",
    "太极": f"{ROOT_PATH}/static/icons/太极.ico",
    "快捷筛选": f"{ROOT_PATH}/static/icons/快捷筛选.svg",
    "聚合方式": f"{ROOT_PATH}/static/icons/聚合方式.svg",
    "数值字段": f"{ROOT_PATH}/static/icons/数值字段.svg",
    "数据源": f"{ROOT_PATH}/static/icons/数据源.svg",
    "分组": f"{ROOT_PATH}/static/icons/分组.svg",
    "数据点数": f"{ROOT_PATH}/static/icons/数据点数.svg",
    "最大值": f"{ROOT_PATH}/static/icons/最大值.svg",
    "最小值": f"{ROOT_PATH}/static/icons/最小值.svg",
    "平均值": f"{ROOT_PATH}/static/icons/平均值.svg",
    "当前显示": f"{ROOT_PATH}/static/icons/当前显示.svg",
    "数据表格": f"{ROOT_PATH}/static/icons/数据表格.svg",
    "历史记录": f"{ROOT_PATH}/static/icons/历史记录.svg",
    "趋势图": f"{ROOT_PATH}/static/icons/趋势图.svg",
    "刷新": f"{ROOT_PATH}/static/icons/刷新.svg",
    "等待": f"{ROOT_PATH}/static/icons/等待.svg",
    "刷新中": f"{ROOT_PATH}/static/icons/刷新中.svg",
    "帮助": f"{ROOT_PATH}/static/icons/帮助.svg",
    "停止": f"{ROOT_PATH}/static/icons/停止.svg",
    "暂停": f"{ROOT_PATH}/static/icons/暂停.svg",
    "执行": f"{ROOT_PATH}/static/icons/执行.svg",
    "完成": f"{ROOT_PATH}/static/icons/完成.svg",
    "失败": f"{ROOT_PATH}/static/icons/失败.svg",
    "时钟": f"{ROOT_PATH}/static/icons/时钟.svg",
    "日历": f"{ROOT_PATH}/static/icons/日历.svg",
    "字典": f"{ROOT_PATH}/static/icons/字典.svg",
    "操作符": f"{ROOT_PATH}/static/icons/操作符.svg",
    "连接符": f"{ROOT_PATH}/static/icons/连接符.svg",
    "示例": f"{ROOT_PATH}/static/icons/示例.svg",
    "结果": f"{ROOT_PATH}/static/icons/结果.svg",
    "垃圾桶": f"{ROOT_PATH}/static/icons/垃圾桶.svg",
    "警告": f"{ROOT_PATH}/static/icons/警告.svg",
    "复制": f"{ROOT_PATH}/static/icons/复制.svg",
    "下载": f"{ROOT_PATH}/static/icons/下载.svg",
    "详情": f"{ROOT_PATH}/static/icons/详情.svg",
    "日志": f"{ROOT_PATH}/static/icons/日志.svg",
    "查找": f"{ROOT_PATH}/static/icons/查找.svg",
    "日志查询": f"{ROOT_PATH}/static/icons/日志查询.svg",
}

#  合并成一个
ICONS = {**MENU_GROUP_ICONS, **UI_ICONS}

#====================
# 📋 使用 SQL 语句注册表
# =============================
# 新增日志查询菜单
# 新增日志查询菜单
UI_CONFIGS["log_search_with_pri"] = TableUIConfig(
    view_type=ViewType.LOG,
    display_name="syslog日志查询",
    description="ClickHouse 日志检索与分析",
    menu_group="日志分析",
    menu_icon=f"{ROOT_PATH}/static/icons/日志查询.svg",
    menu_order=1,
    physical_table_name="logs_with_pri",  # 不同的表
    # =============================================
    #字段映射：显示名 → 实际字段名
    # =============================================
    computed_field_mapping={
        "时间": "timestamp",
        "主机": "host",
        "严重级别": "severity",
        "优先级": "pri",
        "设施": "facility",
        "文件": "file",
        "消息": "message",
    },
    # =============================================
    #包含字段：白名单
    # =============================================
    include_fields={
        "t1": [
            "uid",
            "severity",
			"ip",
            "message",
            "file",
        ]
    },
    # 添加截断配置
#    truncate_fields={
#        "message": 200,   # 消息内容截断为 200 字符
#        "file": 100,      # 文件路径截断为 100 字符
#        "uid": 20,        # UID 截断为 20 字符
#    },    
    # =============================================
    #排除字段：黑名单（优先级高于 include_fields）
    # =============================================
    # exclude_fields={
    #     "t1": [
    #         "tags",      # 标签（暂不显示）
    #     ]
    # },
    # =============================================
    #可搜索字段（高级筛选自动补全）
    # =============================================
    # searchable_fields=[
    #     "timestamp",
    #     "host",
    #     "severity",
    #     "pri",
    #     "facility",
    #     "file",
    #     "message",
    # ],
    #默认排序
    default_sort_field="timestamp",
    default_sort_order="DESC",
    #时间配置（复用 trend_config）
    trend_config=TrendConfig(
        time_field="timestamp",
        default_days=1,
        max_days=30,
    )
)

UI_CONFIGS["log_search_no_pri"] = TableUIConfig(
    view_type=ViewType.LOG,
    display_name="syslog入库失败查询",
    description="ClickHouse 日志检索与分析",
    menu_group="日志分析",
    menu_icon=f"{ROOT_PATH}/static/icons/日志查询.svg",
    menu_order=1,
    physical_table_name="logs_no_pri",  # 不同的表
    # =============================================
    #字段映射：显示名 → 实际字段名
    # =============================================
    computed_field_mapping={
        "时间": "timestamp",
        "主机": "host",
        "严重级别": "severity",
        "优先级": "pri",
        "设施": "facility",
        "日志文件": "file",
        "消息": "message",
    },
    # =============================================
    #包含字段：白名单
    # =============================================
    include_fields={
        "t1": [
            "uid",
            "severity",
			"ip",
            "message",
        ]
    },
    # 添加截断配置
#    truncate_fields={
#        "message": 200,   # 消息内容截断为 200 字符
#        "file": 100,      # 文件路径截断为 100 字符
#        "uid": 20,        # UID 截断为 20 字符
#    },    
    # =============================================
    #排除字段：黑名单（优先级高于 include_fields）
    # =============================================
    # exclude_fields={
    #     "t1": [
    #         "tags",      # 标签（暂不显示）
    #     ]
    # },
    # =============================================
    #可搜索字段（高级筛选自动补全）
    # =============================================
    # searchable_fields=[
    #     "timestamp",
    #     "host",
    #     "severity",
    #     "pri",
    #     "facility",
    #     "file",
    #     "message",
    # ],
    #默认排序
    default_sort_field="timestamp",
    default_sort_order="DESC",
    #时间配置（复用 trend_config）
    trend_config=TrendConfig(
        time_field="timestamp",
        default_days=1,
        max_days=30,
    )
)

UI_CONFIGS["log_search_with_pri_zabbix"] = TableUIConfig(
    view_type=ViewType.LOG,
    display_name="zabbix日志查询",
    description="ClickHouse 日志检索与分析",
    menu_group="日志分析",
    menu_icon=f"{ROOT_PATH}/static/icons/日志查询.svg",
    menu_order=1,
    physical_table_name="logs_with_pri_zabbix",  # 不同的表
    # =============================================
    #字段映射：显示名 → 实际字段名
    # =============================================
    computed_field_mapping={
        "时间": "timestamp",
        "主机": "host",
        "严重级别": "severity",
        "优先级": "pri",
        "设施": "facility",
        "文件": "file",
        "消息": "message",
    },
    # =============================================
    #包含字段：白名单
    # =============================================
    include_fields={
        "t1": [
            "uid",
            "severity",
            "message",
			"ip",
            "file",
        ]
    },
    # 添加截断配置
#    truncate_fields={
#        "message": 200,   # 消息内容截断为 200 字符
#        "file": 100,      # 文件路径截断为 100 字符
#        "uid": 20,        # UID 截断为 20 字符
#    },    
    # =============================================
    #排除字段：黑名单（优先级高于 include_fields）
    # =============================================
    # exclude_fields={
    #     "t1": [
    #         "tags",      # 标签（暂不显示）
    #     ]
    # },
    # =============================================
    #可搜索字段（高级筛选自动补全）
    # =============================================
    # searchable_fields=[
    #     "timestamp",
    #     "host",
    #     "severity",
    #     "pri",
    #     "facility",
    #     "file",
    #     "message",
    # ],
    #默认排序
    default_sort_field="timestamp",
    default_sort_order="DESC",
    #时间配置（复用 trend_config）
    trend_config=TrendConfig(
        time_field="timestamp",
        default_days=1,
        max_days=30,
    )
)

UI_CONFIGS["log_search_no_pri_zabbix"] = TableUIConfig(
    view_type=ViewType.LOG,
    display_name="zabbix入库失败查询",
    description="ClickHouse 日志检索与分析",
    menu_group="日志分析",
    menu_icon=f"{ROOT_PATH}/static/icons/日志查询.svg",
    menu_order=1,
    physical_table_name="logs_no_pri_zabbix",  # 不同的表
    # =============================================
    #字段映射：显示名 → 实际字段名
    # =============================================
    computed_field_mapping={
        "时间": "timestamp",
        "主机": "host",
        "严重级别": "severity",
        "优先级": "pri",
        "设施": "facility",
        "日志文件": "file",
        "消息": "message",
    },
    # =============================================
    #包含字段：白名单
    # =============================================
    include_fields={
        "t1": [
            "uid",
            "severity",
			"ip",
            "message",
        ]
    },
    # 添加截断配置
#    truncate_fields={
#        "message": 200,   # 消息内容截断为 200 字符
#        "file": 100,      # 文件路径截断为 100 字符
#        "uid": 20,        # UID 截断为 20 字符
#    },    
    # =============================================
    #排除字段：黑名单（优先级高于 include_fields）
    # =============================================
    # exclude_fields={
    #     "t1": [
    #         "tags",      # 标签（暂不显示）
    #     ]
    # },
    # =============================================
    #可搜索字段（高级筛选自动补全）
    # =============================================
    # searchable_fields=[
    #     "timestamp",
    #     "host",
    #     "severity",
    #     "pri",
    #     "facility",
    #     "file",
    #     "message",
    # ],
    #默认排序
    default_sort_field="timestamp",
    default_sort_order="DESC",
    #时间配置（复用 trend_config）
    trend_config=TrendConfig(
        time_field="timestamp",
        default_days=1,
        max_days=30,
    )
)