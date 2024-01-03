GV_VERSION=$(cat ./patch/.version_docker)
VERSION=centos-${GV_VERSION}
ADDRESS=registry.cn-shanghai.aliyuncs.com/zabbix_docker/zabbix_chinese
for IM in `cat ./patch/.images_mysql`
do
docker tag ${IM}:${VERSION} ${ADDRESS}:${IM}_${VERSION}
docker push ${ADDRESS}:${IM}_${VERSION}
docker rmi ${ADDRESS}:${IM}_${VERSION}
done
docker tag quay.io/centos/centos:stream8 ${ADDRESS}:centos_stream8
docker push ${ADDRESS}:centos_stream8
docker rmi ${ADDRESS}:centos_stream8
docker tag mariadb:11.1.2 ${ADDRESS}:mariadb
docker push ${ADDRESS}:mariadb
docker rmi ${ADDRESS}:mariadb
docker tag grafana/grafana-enterprise:10.1.0 ${ADDRESS}:grafana_grafana-enterprise
docker push ${ADDRESS}:grafana_grafana-enterprise
docker rmi ${ADDRESS}:grafana_grafana-enterprise
docker tag grafana/loki:2.8.4 ${ADDRESS}:grafana_loki
docker push ${ADDRESS}:grafana_loki
docker rmi ${ADDRESS}:grafana_loki
docker tag grafana/promtail:2.8.4 ${ADDRESS}:grafana_promtail
docker push ${ADDRESS}:grafana_promtail
docker rmi ${ADDRESS}:grafana_promtail