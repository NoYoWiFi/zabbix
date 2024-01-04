GV_VERSION=$(cat ./patch/.version_docker)
VERSION=rocky-${GV_VERSION}
ADDRESS=registry.cn-shanghai.aliyuncs.com/zabbix_docker/zabbix_chinese
for IM in `cat ./patch/.images_mysql_proxy`
do
docker pull ${ADDRESS}:${IM}_${VERSION}
docker tag ${ADDRESS}:${IM}_${VERSION} ${IM}:${VERSION}
docker rmi ${ADDRESS}:${IM}_${VERSION}
done
docker pull ${ADDRESS}:mariadb
docker tag ${ADDRESS}:mariadb mariadb:10.11.2
docker rmi ${ADDRESS}:mariadb