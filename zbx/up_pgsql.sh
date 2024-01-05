GV_VERSION=$(cat ./patch/.version_docker)
VERSION=rocky-${GV_VERSION}
ADDRESS=registry.cn-shanghai.aliyuncs.com/zabbix_docker/zabbix_pgsql
for IM in `cat ./patch/.images_pgsql`
do
docker tag ${IM}:${VERSION} ${ADDRESS}:${IM}_${VERSION}
docker push ${ADDRESS}:${IM}_${VERSION}
docker rmi ${ADDRESS}:${IM}_${VERSION}
done
docker tag rockylinux:8 ${ADDRESS}:rockylinux8
docker push ${ADDRESS}:rockylinux8
docker rmi ${ADDRESS}:rockylinux8
docker tag timescale/timescaledb:2.13.0-pg15 ${ADDRESS}:2.13.0-pg15
docker push ${ADDRESS}:2.13.0-pg15
docker rmi ${ADDRESS}:2.13.0-pg15
docker tag grafana/grafana-enterprise:10.1.0 ${ADDRESS}:grafana_grafana-enterprise
docker push ${ADDRESS}:grafana_grafana-enterprise
docker rmi ${ADDRESS}:grafana_grafana-enterprise
docker tag grafana/loki:2.8.4 ${ADDRESS}:grafana_loki
docker push ${ADDRESS}:grafana_loki
docker rmi ${ADDRESS}:grafana_loki
docker tag grafana/promtail:2.8.4 ${ADDRESS}:grafana_promtail
docker push ${ADDRESS}:grafana_promtail
docker rmi ${ADDRESS}:grafana_promtail