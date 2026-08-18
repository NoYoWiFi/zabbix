# 察数系统上线部署手册

## 一、系统概述

| 项目 | 说明 |
| ---- | ---- |
| 系统名称 | 察数系统（监控数据平台） |
| 技术栈 | Python 3.11 + FastAPI + Vue 3 + ClickHouse + MySQL + Redis |

---

## 二、服务器环境要求

| 组件 | 版本要求 | 用途 |
| ---- | ---- | ---- |
| ClickHouse | 22+ | 日志数据存储 |
| MySQL | 5.7+ / 8.0+ | 业务数据存储 |
| Redis | 6+ | 任务队列/缓存 |
| Nginx | 1.20+ | 反向代理（可选） |
| 操作系统 | Rocklinux 8 | 服务器系统 |

---
## 三、准备必要的启动文件
```SH
#!/bin/bash

# ============================================
# 察数系统部署脚本
# ============================================

set -e

PROJECT_DIR="/usr/share/zabbix/monitor"
BACKEND_DIR="${PROJECT_DIR}/backend"
FRONTEND_DIR="${PROJECT_DIR}"

echo "📦 开始部署察数系统..."

# 2. 复制后端二进制
echo "📦 复制后端二进制..."
\cp patch/monitor-api ${BACKEND_DIR}/
chmod +x ${BACKEND_DIR}/monitor-api

# 3. 复制前端静态文件
echo "📦 复制前端静态文件..."
\cp -vrf patch/dist/* ${FRONTEND_DIR}/

# 4. 复制配置文件
echo "📦 复制配置文件..."
\cp patch/.env ${BACKEND_DIR}/
\cp patch/monitor_config.py ${BACKEND_DIR}/

# 7. 复制 Service 文件
echo "📋 复制 Service 文件..."
if [ -f "patch/monitor-api.service" ]; then
    \cp patch/monitor-api.service /etc/systemd/system/
    chmod 644 /etc/systemd/system/monitor-api.service
    echo "  ✅ Service 文件已复制"
else
    echo "  ⚠️  monitor-api.service 不存在，创建默认配置..."
	exit 1
fi

# 7. 重启服务
echo "🔄 重启服务..."
systemctl daemon-reload
systemctl enable monitor-api
systemctl restart monitor-api
systemctl status monitor-api --no-pager
journalctl -u monitor-api -f

echo "✅ 部署完成！"
```

## 四、部署步骤

### Redis

```bash
# CentOS/RHEL
yum install -y redis

sed -i 's/^daemonize yes/daemonize no/' /etc/redis/redis.conf
sed -i 's/^supervised no/supervised systemd/' /etc/redis/redis.conf
sed -i 's|^pidfile .*|pidfile /var/run/redis/redis.pid|' /etc/redis/redis.conf
sed -i 's|^logfile .*|logfile /var/log/redis/redis.log|' /etc/redis/redis.conf
sed -i 's|^dir .*|dir /var/lib/redis|' /etc/redis/redis.conf
sed -i -e "{/^bind 127.0.0.1/s/bind 127.0.0.1/bind 0.0.0.0/}" /etc/redis/redis.conf
sed -i -e "{/^\# requirepass foobared/s/\# requirepass foobared/requirepass Admin@zabbix.com/}" /etc/redis/redis.conf

```
#### 启动 Redis

```bash
# CentOS/RHEL
systemctl enable redis
systemctl start redis
systemctl status redis

# Ubuntu/Debian
systemctl enable redis-server
systemctl start redis-server
systemctl status redis-server
```

#### 验证 Redis

```bash
# 连接测试
redis-cli -h 127.0.0.1 -p 6379 -a Admin@zabbix.com ping
# 预期: PONG

# 查看状态
redis-cli -h 127.0.0.1 -p 6379 -a Admin@zabbix.com info stats
```

---

## 五、Nginx 配置

```nginx

#!/bin/bash

# ============================================
# Nginx 部署脚本 - 察数系统
# ============================================

set -e

NGINX_CONF="/etc/nginx/conf.d/zabbix.conf"
NGINX_MAIN_CONF="/etc/nginx/nginx.conf"
PROJECT_DIR="/usr/share/zabbix/monitor"
FRONTEND_DIR="${PROJECT_DIR}/"
BACKEND_STATIC_DIR="${PROJECT_DIR}/backend/"
DOMAIN_NAME=$(hostname)

echo "============================================"
echo "📦 Nginx 部署 - 察数系统"
echo "============================================"

# 1. 检查 Nginx 是否安装
echo ""
echo "🔍 检查 Nginx..."
if ! command -v nginx &> /dev/null; then
    echo "❌ Nginx 未安装，正在安装..."
    yum install -y nginx || apt-get install -y nginx
fi
echo "  ✅ Nginx 已安装: $(nginx -v 2>&1)"

# 2. 创建必要的目录
echo ""
echo "📁 创建目录..."
mkdir -p ${PROJECT_DIR}/
mkdir -p ${PROJECT_DIR}/backend/static
mkdir -p /etc/pki/nginx
mkdir -p /var/log/nginx

# 3. 检查 SSL 证书
echo ""
echo "🔐 检查 SSL 证书..."
if [ ! -f "/etc/pki/nginx/server.pem" ]; then
    echo "  ⚠️  SSL 证书不存在，生成自签名证书..."
     \cp patch/server.pem /etc/pki/nginx/server.pem
    chmod 600 /etc/pki/nginx/server.pem
    echo "  ✅ 自签名证书已生成"
else
    echo "  ✅ SSL 证书已存在"
fi

# 4. 创建 Nginx 配置文件
echo ""
echo "📝 创建 Nginx 配置..."
\cp patch/zabbix.conf ${NGINX_CONF}
\cp -vrf patch/static ${BACKEND_STATIC_DIR}
echo "  ✅ Nginx 配置已创建: ${NGINX_CONF}"

# 5. 配置 Nginx 主配置文件（确保包含 conf.d）
echo ""
echo "🔧 检查 Nginx 主配置..."
if ! grep -q "include /etc/nginx/conf.d/\*.conf" ${NGINX_MAIN_CONF} 2>/dev/null; then
    echo "  ⚠️  添加 conf.d 包含配置..."
    sed -i '/http {/a \    include /etc/nginx/conf.d/*.conf;' ${NGINX_MAIN_CONF}
fi
echo "  ✅ Nginx 主配置正常"

# 6. 测试 Nginx 配置
echo ""
echo "🔍 测试 Nginx 配置..."
nginx -t 2>&1
if [ $? -eq 0 ]; then
    echo "  ✅ Nginx 配置测试通过"
else
    echo "  ❌ Nginx 配置测试失败"
    exit 1
fi

# 7. 重启 Nginx
echo ""
echo "🔄 重启 Nginx..."
systemctl daemon-reload
systemctl enable nginx
systemctl restart nginx
systemctl enable nginx

# 8. 检查 Nginx 状态
echo ""
echo "📊 Nginx 状态:"
systemctl status nginx --no-pager | head -10

# 9. 检查端口监听
echo ""
echo "🔌 端口监听:"
netstat -tlnp | grep -E "8080|8443" || ss -tlnp | grep -E "8080|8443"

echo ""
echo "============================================"
echo "✅ Nginx 部署完成！"
echo ""
echo "📍 访问地址:"
echo "   HTTP:  http://${DOMAIN_NAME}:8080/monitor/"
echo "   HTTPS: https://${DOMAIN_NAME}:8443/monitor/"
echo ""
echo "🔧 常用命令:"
echo "   systemctl status nginx     # 查看状态"
echo "   systemctl restart nginx    # 重启服务"
echo "   nginx -t                   # 测试配置"
echo "   tail -f /var/log/nginx/error.log  # 查看错误日志"
echo "============================================"
```

---

## 六、数据库初始化

### 6.1 mariadb

启动后端时会自动创建表，也可手动执行：

```sql
DPassword='Admin@zabbix.com'
# 1. 检查并创建数据库（如果不存在）
mariadb -e "CREATE DATABASE IF NOT EXISTS monitor CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;"
# 2. 创建 zabbix 用户（如果不存在）
mariadb -e "CREATE USER IF NOT EXISTS 'zabbix'@'localhost' IDENTIFIED BY '$DPassword';"
mariadb -e "CREATE USER IF NOT EXISTS 'zabbix'@'%' IDENTIFIED BY '$DPassword';"
# 4. 授予权限
mariadb -e "GRANT ALL PRIVILEGES ON monitor.* TO 'zabbix'@'localhost';"
mariadb -e "GRANT ALL PRIVILEGES ON monitor.* TO 'zabbix'@'%';"
# 5. 授予 SET USER 权限给 zabbix 用户
mariadb -e "GRANT SET USER ON *.* TO 'zabbix'@'localhost';"
mariadb -e "GRANT SET USER ON *.* TO 'zabbix'@'%';"
# 6. 设置字符集
mariadb -e "SET GLOBAL character_set_server = utf8mb4;"
mariadb -e "SET GLOBAL collation_server = utf8mb4_bin;"
# 7. 刷新权限
# 授予 zabbix 用户对 monitor 数据库的权限

# 刷新权限
mariadb -e "FLUSH PRIVILEGES;"

echo "数据库和权限设置完成！"

```

### 6.2 ClickHouse

### 安装帮助
```sql

clickhouse-client --host 127.0.0.1 --port 8123 --user default --password Admin@zabbix.com

-- 创建一个名为 'newuser' 的用户，密码为 'securepassword123'
CREATE USER IF NOT EXISTS zabbix IDENTIFIED BY 'Admin@zabbix.com';
-- 修改现有用户密码
-- ALTER USER zabbix IDENTIFIED BY 'Admin@zabbix.com';
-- 授予该用户对默认数据库 'default' 的 SELECT 权限（可选）
GRANT SELECT ON monitor.* TO zabbix;

-- 若需要更广泛权限（如创建表、插入数据），可使用：
GRANT ALL PRIVILEGES ON monitor.* TO zabbix;

CREATE DATABASE IF NOT EXISTS monitor;

sed -i 's|<!-- <listen_host>0.0.0.0</listen_host> -->|<listen_host>0.0.0.0</listen_host>|' /etc/clickhouse-server/config.xml
systemctl restart clickhouse-server
CREATE DATABASE IF NOT EXISTS monitor;
```

### 部署
```SQL
#!/bin/bash

\cp patch/clickhouse.repo /etc/yum.repos.d/
yum install clickhouse-client clickhouse-common-static clickhouse-common-static-dbg clickhouse-server -y

CH_USER="zabbix"
CH_PASSWORD="Admin@zabbix.com"
CH_DATABASE="monitor"

# ============================================
# ClickHouse 初始化脚本（非交互）
# ============================================

echo "🔧 配置 ClickHouse..."

# 1. 启用远程访问（允许非本地连接）
echo "📝 启用远程访问..."
sed -i 's|<!-- <listen_host>0.0.0.0</listen_host> -->|<listen_host>0.0.0.0</listen_host>|' /etc/clickhouse-server/config.xml

# 2. 重启 ClickHouse
echo "🔄 重启 ClickHouse..."
systemctl restart clickhouse-server
sleep 3

# 3. 创建用户（非交互）
echo "👤 创建 ClickHouse 用户..."
clickhouse-client --query "CREATE USER IF NOT EXISTS ${CH_USER} IDENTIFIED BY '${CH_PASSWORD}';" 2>/dev/null || true

# 4. 创建数据库
echo "📁 创建数据库..."
clickhouse-client --query "CREATE DATABASE IF NOT EXISTS ${CH_DATABASE};" 2>/dev/null || true

# 5. 授予权限
echo "🔐 授予权限..."
clickhouse-client --query "GRANT ALL PRIVILEGES ON ${CH_DATABASE}.* TO ${CH_USER};" 2>/dev/null || true

# 6. 验证
echo "✅ 验证连接..."
clickhouse-client --user ${CH_USER} --password ${CH_PASSWORD} --query "SHOW DATABASES;" 2>/dev/null | grep -q ${CH_DATABASE} && echo "  ✅ 连接成功"

echo "✅ ClickHouse 初始化完成！"
```
---
## 七 rsyslog
```SH
#!/bin/bash

# ============================================
# rsyslog 日志采集部署脚本
# ============================================

set -e

echo "============================================"
echo "📦 rsyslog + Loki 日志采集部署"
echo "============================================"

# 1. 安装 rsyslog
echo ""
echo "🔧 安装 rsyslog..."
if ! command -v rsyslogd &> /dev/null; then
    yum install -y rsyslog
fi
echo "  ✅ rsyslog 已安装: $(rsyslogd -v | head -1)"

# 2. 创建日志目录
echo ""
echo "📁 创建日志目录..."
mkdir -p /var/log/loki
mkdir -p /var/log/rsyslog
chmod 755 /var/log/loki

# 4. 创建 rsyslog 配置
echo ""
echo "📝 创建 rsyslog 配置..."

# 4a. 主配置文件 /etc/rsyslog.conf
\cp patch/loki.conf /etc/rsyslog.d/

# 4c. 创建日志轮转配置
\cp patch/loki /etc/logrotate.d/loki

logrotate -d /etc/logrotate.d/loki
logrotate -f /etc/logrotate.d/loki

ln -s /log /var/log/loki

echo "  ✅ rsyslog 配置已创建"

# 5. 设置日志目录权限
echo ""
echo "🔐 设置权限..."
chown -R root:root /var/log/loki
chmod 755 /var/log/loki
chmod 666 /var/log/loki/*.log 2>/dev/null || true

# 7. 重启 rsyslog
echo ""
echo "🔄 重启 rsyslog..."
systemctl daemon-reload
systemctl restart rsyslog
systemctl enable rsyslog

# 8. 检查状态
echo ""
echo "📊 rsyslog 状态:"
systemctl status rsyslog --no-pager | head -10

# 9. 检查端口监听
echo ""
echo "🔌 端口监听:"
netstat -tlnp | grep -E ":514" || ss -tlnp | grep -E ":514"

#![解除打开文件数限制]
\cp ./patch/limits.conf /etc/security/
\cp ./patch/sysctl.conf /etc/
sed -i -e "/^DefaultLimitCORE=/s/=.*/=infinity/" /etc/systemd/system.conf
sed -i -e "/^#DefaultLimitNOFILE=/s/=.*/=100000/" /etc/systemd/system.conf
sed -i -e "/^#DefaultLimitNPROC=/s/=.*/=100000/" /etc/systemd/system.conf
# sed -i -e "/^LimitNOFILE=/s/=.*/=655350/" /usr/lib/systemd/system/mariadb.service
sed -i -e "/^\#DefaultLimitNOFILE=/s/^#//" /etc/systemd/system.conf
sed -i -e "/^\#DefaultLimitNPROC=/s/^#//" /etc/systemd/system.conf
sed -i -e "/^#DefaultLimitCORE=/s/=.*/=infinity/" /etc/systemd/user.conf
sed -i -e "/^#DefaultLimitNOFILE=/s/=.*/=100000/" /etc/systemd/user.conf
sed -i -e "/^#DefaultLimitNPROC=/s/=.*/=100000/" /etc/systemd/user.conf
sed -i -e "/^\#DefaultLimitCORE=/s/^#//" /etc/systemd/user.conf
sed -i -e "/^\#DefaultLimitNOFILE=/s/^#//" /etc/systemd/user.conf
sed -i -e "/^\#DefaultLimitNPROC=/s/^#//" /etc/systemd/user.conf


echo ""
echo "============================================"
echo "✅ rsyslog 部署完成！"
echo ""
echo "📁 日志目录: /var/log/loki/"
echo "📄 自定义配置: /etc/rsyslog.d/loki.conf"
echo "🔄 日志轮转: /etc/logrotate.d/loki"
echo ""
echo "🔧 常用命令:"
echo "   systemctl status rsyslog     # 查看状态"
echo "   systemctl restart rsyslog    # 重启服务"
echo "   tail -f /var/log/loki/xxx.log  # 查看日志"
echo "   rsyslogd -N1 -f /etc/rsyslog.conf  # 测试配置"
echo ""
echo "📊 查看生成的日志文件:"
echo "   ls -la /var/log/loki/"
echo "============================================"
```

---

## 八、vector
```sh
# 下载
curl -O https://packages.timber.io/vector/latest/vector-x86_64-unknown-linux-gnu.tar.gz

# 解压
tar -xzf vector-x86_64-unknown-linux-gnu.tar.gz

# 安装
cp vector-x86_64-unknown-linux-gnu/bin/vector /usr/local/bin/
chmod +x /usr/local/bin/vector
# 创建用户
groupadd -r vector
useradd -r -g vector -s /sbin/nologin -d /var/lib/vector -c "Vector observability data router" vector

# 创建目录
mkdir -p /var/lib/vector /etc/vector
\cp patch/vector.yaml /etc/vector/
vector validate --config-yaml /etc/vector/vector.yaml
chown -R vector:vector /var/lib/vector /etc/vector

\cp patch/vector.service /etc/systemd/system/vector.service
systemctl daemon-reload
systemctl enable vector
systemctl start vector
systemctl status vector
journalctl -u vector -f
```

## 九、常见问题排查

| 问题             | 排查方法                                    |
| -------------- | --------------------------------------- |
| 后端启动失败         | 查看日志 `journalctl -u monitor-api -f` |
| 数据库连接失败        | 检查 `.env` 配置和网络连通性                      |
| ClickHouse 查询慢 | 检查分区和索引                                 |
| 前端页面空白         | 查看浏览器控制台错误                              |
| API 404        | 检查 `ROOT_PATH` 和 `API_PREFIX` 配置        |

---
