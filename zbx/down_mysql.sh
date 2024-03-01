GV_VERSION=$(cat ./patch/.version_docker)
VERSION=rocky-${GV_VERSION}
ADDRESS=registry.cn-shanghai.aliyuncs.com/zabbix_docker/zabbix_chinese
for IM in `cat ./patch/.images_mysql`
do
docker pull ${ADDRESS}:${IM}_${VERSION}
docker tag ${ADDRESS}:${IM}_${VERSION} ${IM}:${VERSION}
docker rmi ${ADDRESS}:${IM}_${VERSION}
done
docker pull ${ADDRESS}:rockylinux8
docker tag ${ADDRESS}:rockylinux8 rockylinux8:8
docker rmi ${ADDRESS}:rockylinux8
docker pull ${ADDRESS}:mariadb
docker tag ${ADDRESS}:mariadb mariadb:11.2.3
docker rmi ${ADDRESS}:mariadb
docker pull ${ADDRESS}:grafana_grafana-enterprise
docker tag ${ADDRESS}:grafana_grafana-enterprise grafana/grafana-enterprise:10.0.11
docker rmi ${ADDRESS}:grafana_grafana-enterprise
docker pull ${ADDRESS}:grafana_loki
docker tag ${ADDRESS}:grafana_loki grafana/loki:2.9.4
docker rmi ${ADDRESS}:grafana_loki
docker pull ${ADDRESS}:grafana_promtail
docker tag ${ADDRESS}:grafana_promtail grafana/promtail:2.9.4
docker rmi ${ADDRESS}:grafana_promtail