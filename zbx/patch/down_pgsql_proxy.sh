GV_ENV_SHELL="./patch/.env_shell"
source ./patch/getEnv.sh
GV_VERSION=${GV_ARR_ENV[GV_ZABBIX_POSTFIX]}
VERSION=rocky-${GV_VERSION}
ADDRESS=registry.cn-shanghai.aliyuncs.com/zabbix_docker/zabbix_pgsql
for IM in `cat ./patch/.images_pgsql_proxy`
do
docker pull ${ADDRESS}:${IM}_${VERSION}
docker tag ${ADDRESS}:${IM}_${VERSION} ${IM}:${VERSION}
docker rmi ${ADDRESS}:${IM}_${VERSION}
done
docker pull ${ADDRESS}:${GV_ARR_ENV[GV_POSTGRESQL_VERSION]}
docker tag ${ADDRESS}:${GV_ARR_ENV[GV_POSTGRESQL_VERSION]} timescale/timescaledb:${GV_ARR_ENV[GV_POSTGRESQL_VERSION]}
docker rmi ${ADDRESS}:${GV_ARR_ENV[GV_POSTGRESQL_VERSION]}