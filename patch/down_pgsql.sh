GV_VERSION=$(cat ./patch/.version_docker)
VERSION=rocky-${GV_VERSION}
ADDRESS=registry.cn-shanghai.aliyuncs.com/zabbix_docker/zabbix_pgsql
for IM in `cat ./patch/.images_pgsql`
do
docker pull ${ADDRESS}:${IM}_${VERSION}
docker tag ${ADDRESS}:${IM}_${VERSION} ${IM}:${VERSION}
docker rmi ${ADDRESS}:${IM}_${VERSION}
done
docker pull ${ADDRESS}:rockylinux8
docker tag ${ADDRESS}:rockylinux8 rockylinux8:8
docker rmi ${ADDRESS}:rockylinux8
docker pull ${ADDRESS}:2.13.0-pg15
docker tag ${ADDRESS}:2.13.0-pg15 timescale/timescaledb:2.13.0-pg15
docker rmi ${ADDRESS}:2.13.0-pg15
docker pull ${ADDRESS}:grafana_grafana-enterprise
docker tag ${ADDRESS}:grafana_grafana-enterprise grafana/grafana-enterprise:10.1.0
docker rmi ${ADDRESS}:grafana_grafana-enterprise
docker pull ${ADDRESS}:grafana_loki
docker tag ${ADDRESS}:grafana_loki grafana/loki:2.8.4
docker rmi ${ADDRESS}:grafana_loki
docker pull ${ADDRESS}:grafana_promtail
docker tag ${ADDRESS}:grafana_promtail grafana/promtail:2.8.4
docker rmi ${ADDRESS}:grafana_promtail