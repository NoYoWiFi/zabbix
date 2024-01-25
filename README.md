==持续更新最新版本...==
# 全自动安装方法
1. 下载一键安装脚本
[一键安装脚本](https://gitcode.net/1284524409/zabbix/-/archive/centos_7_zabbix_5.0.x_mysql/zabbix-centos_7_zabbix_5.0.x_mysql.tar.gz)
2. 执行命令全自动安装zabbix-server
```
tar -zxvf zabbix-centos_7_zabbix_5.0.x_mysql.tar.gz
cd zabbix-centos_7_zabbix_5.0.x_mysql
sh autosetup.sh install
```
3. 执行命令全自动安装zabbix-proxy
```
tar -zxvf zabbix-centos_7_zabbix_5.0.x_mysql.tar.gz
cd zabbix-rocky_8_zabbix_6.0.x_mysql
sh autosetup.sh proxy
```


**打开网页输入服务器IP地址访问zabbix**
http://IP:8080 或 https://IP:8443
用户名: Admin
密码: zabbix

**打开网页输入服务器IP地址访问grafana**
https://IP:3000
用户名: admin
密码: admin

**将grafana界面设置成中文**
![](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/vx_images/2cc17fdd154217656975030bc6636523.png)

**启用zabbix插件
![](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/vx_images/844a584f0789fc28205b2b5a8302938c.png)

**连接zabbix数据库插件**
![](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/vx_images/c87b39af3050dac2ecb62c7365bc7a7b.png)

**新建zabbix数据库连接**
`https://zabbix-web-nginx-mysql:8443/api_jsonrpc.php`

![](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/vx_images/c68d9dbf98134214aa759dd25bbfbb2e.png)

**输入正确的用户名密码**
`Admin/zabbix`

![](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/vx_images/aa5fd658ee04a9dd7687e459b3064dbe.png)


**zabbix-server服务器同时优化成了rsyslog日志服务器，rsyslog日志端口为514**
日志存储路径为 /var/log/loki/

**grafana优化集成了zabbix与Loki插件**
请将任意.log后缀日志存入 /var/log/loki/即可连接到loki
URL为http://IP:3100
![在这里插入图片描述](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/vx_images/c469826e35f6d0735418cbb9ca008b22.png)


`交流群`  
  
| zabbix-答疑群                                                                                                | zabbix-汉化群                                                                                                  |  
|-----------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|  
| ![微信打赏](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/vx_images/zabbix-dayi.png) | ![微信打赏](https://gitcode.net/1284524409/zabbix/-/raw/rocky_8_zabbix_6.0.x_mysql/vx_images/zabbix-hanhua.png) |  
  
  
**全文完结**