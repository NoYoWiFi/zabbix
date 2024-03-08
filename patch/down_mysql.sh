GV_ENV_SHELL="./.env_shell"
source ./getEnv.sh
GV_VERSION=${GV_ARR_ENV[GV_ZABBIX_POSTFIX]}
VERSION=rocky-${GV_VERSION}
ADDRESS=registry.cn-shanghai.aliyuncs.com/zabbix_docker/zabbix_chinese
for IM in `cat ./patch/.images_mysql`
do
docker pull ${ADDRESS}:${IM}_${VERSION}
docker tag ${ADDRESS}:${IM}_${VERSION} ${IM}:${VERSION}
docker rmi ${ADDRESS}:${IM}_${VERSION}
done
docker pull ${ADDRESS}:${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE_TAG]}
docker tag ${ADDRESS}:${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE_TAG]} ${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE]}
docker rmi ${ADDRESS}:${GV_ARR_ENV[GV_ROCKY_LINUX_RELEASE_TAG]}
docker pull ${ADDRESS}:mariadb
docker tag ${ADDRESS}:mariadb mariadb:${GV_ARR_ENV[GV_MARIADB_VERSION]}
docker rmi ${ADDRESS}:mariadb
docker pull ${ADDRESS}:grafana_grafana-enterprise
docker tag ${ADDRESS}:grafana_grafana-enterprise grafana/grafana-enterprise:${GV_ARR_ENV[GV_GRAFANA_VERSION]}
docker rmi ${ADDRESS}:grafana_grafana-enterprise
docker pull ${ADDRESS}:grafana_loki
docker tag ${ADDRESS}:grafana_loki grafana/loki:${GV_ARR_ENV[GV_LOKI_VERSION]}
docker rmi ${ADDRESS}:grafana_loki
docker pull ${ADDRESS}:grafana_promtail
docker tag ${ADDRESS}:grafana_promtail grafana/promtail:${GV_ARR_ENV[GV_PROMTAIL_VERSION]}
docker rmi ${ADDRESS}:grafana_promtail