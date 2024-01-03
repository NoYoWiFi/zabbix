GV_VERSION=$(cat ./patch/.version_docker)
VERSION=centos-${GV_VERSION}
ADDRESS=registry.cn-shanghai.aliyuncs.com/zabbix_docker/zabbix_pgsql
for IM in `cat ./patch/.images_pgsql`
do
docker pull ${ADDRESS}:${IM}_${VERSION}
docker tag ${ADDRESS}:${IM}_${VERSION} ${IM}:${VERSION}
docker rmi ${ADDRESS}:${IM}_${VERSION}
done
docker pull ${ADDRESS}:centos_stream8
docker tag ${ADDRESS}:centos_stream8 quay.io/centos/centos:stream8
docker rmi ${ADDRESS}:centos_stream8
docker pull ${ADDRESS}:pg15-latest
docker tag ${ADDRESS}:pg15-latest timescale/timescaledb-ha:pg15-latest
docker rmi ${ADDRESS}:pg15-latest