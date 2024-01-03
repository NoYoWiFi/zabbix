GV_VERSION=$(cat ./patch/.version_docker)
VERSION=centos-${GV_VERSION}
ADDRESS=registry.cn-shanghai.aliyuncs.com/zabbix_docker/zabbix_pgsql
for IM in `cat ./patch/.images_pgsql`
do
echo "docker pull ${IM}_${VERSION}"
docker pull ${ADDRESS}:${IM}_${VERSION}
docker tag ${ADDRESS}:${IM}_${VERSION} ${IM}:${VERSION}
docker rmi ${ADDRESS}:${IM}_${VERSION}
done
echo "docker pull centos_stream8"
docker pull ${ADDRESS}:centos_stream8
docker tag ${ADDRESS}:centos_stream8 quay.io/centos/centos:stream8
docker rmi ${ADDRESS}:centos_stream8
echo "docker pull pg15-latest"
docker pull ${ADDRESS}:2.13.0-pg15
docker tag ${ADDRESS}:2.13.0-pg15 timescale/timescaledb:2.13.0-pg15
docker rmi ${ADDRESS}:2.13.0-pg15