GV_ENV_SHELL="./patch/.env_shell"
source ./patch/getEnv.sh
GV_VERSION=${GV_ARR_ENV[GV_ZABBIX_POSTFIX]}
VERSION=rocky-${GV_VERSION}
ADDRESS=registry.cn-shanghai.aliyuncs.com/zabbix_docker/zabbix_chinese
for IM in `cat ./patch/.images_mysql`
do
docker tag ${IM}:${VERSION} ${ADDRESS}:${IM}_${VERSION}
docker push ${ADDRESS}:${IM}_${VERSION}
docker rmi ${ADDRESS}:${IM}_${VERSION}
done
docker tag ${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE]} ${ADDRESS}:${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE_TAG]}
docker push ${ADDRESS}:${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE_TAG]}
docker rmi ${ADDRESS}:${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE_TAG]}
docker tag mariadb:${GV_ARR_ENV[GV_MARIADB_VERSION]} ${ADDRESS}:mariadb
docker push ${ADDRESS}:mariadb
docker rmi ${ADDRESS}:mariadb
docker tag grafana/grafana-enterprise:${GV_ARR_ENV[GV_GRAFANA_VERSION]} ${ADDRESS}:grafana_grafana-enterprise
docker push ${ADDRESS}:grafana_grafana-enterprise
docker rmi ${ADDRESS}:grafana_grafana-enterprise
docker tag grafana/loki:${GV_ARR_ENV[GV_LOKI_VERSION]} ${ADDRESS}:grafana_loki
docker push ${ADDRESS}:grafana_loki
docker rmi ${ADDRESS}:grafana_loki
docker tag grafana/promtail:${GV_ARR_ENV[GV_PROMTAIL_VERSION]} ${ADDRESS}:grafana_promtail
docker push ${ADDRESS}:grafana_promtail
docker rmi ${ADDRESS}:grafana_promtail
