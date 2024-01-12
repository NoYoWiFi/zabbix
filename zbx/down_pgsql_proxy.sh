GV_VERSION=$(cat ./patch/.version_docker)
VERSION=rocky-${GV_VERSION}
ADDRESS=registry.cn-shanghai.aliyuncs.com/zabbix_docker/zabbix_pgsql
for IM in `cat ./patch/.images_pgsql_proxy`
do
docker pull ${ADDRESS}:${IM}_${VERSION}
docker tag ${ADDRESS}:${IM}_${VERSION} ${IM}:${VERSION}
docker rmi ${ADDRESS}:${IM}_${VERSION}
done
docker pull ${ADDRESS}:2.13.0-pg15
docker tag ${ADDRESS}:2.13.0-pg15 timescale/timescaledb:2.13.0-pg15
docker rmi ${ADDRESS}:2.13.0-pg15