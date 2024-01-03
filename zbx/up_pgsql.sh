GV_VERSION=$(cat ./patch/.version_docker)
VERSION=centos-${GV_VERSION}
ADDRESS=registry.cn-shanghai.aliyuncs.com/zabbix_docker/zabbix_pgsql
for IM in `cat ./patch/.images_pgsql`
do
docker tag ${IM}:${VERSION} ${ADDRESS}:${IM}_${VERSION}
docker push ${ADDRESS}:${IM}_${VERSION}
docker rmi ${ADDRESS}:${IM}_${VERSION}
done
docker tag quay.io/centos/centos:stream8 ${ADDRESS}:centos_stream8
docker push ${ADDRESS}:centos_stream8
docker rmi ${ADDRESS}:centos_stream8
docker tag timescale/timescaledb:2.13.0-pg15 ${ADDRESS}:2.13.0-pg15
docker push ${ADDRESS}:2.13.0-pg15
docker rmi ${ADDRESS}:2.13.0-pg15