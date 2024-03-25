GV_ENV_SHELL="./patch/.env_shell"
source ./patch/getEnv.sh
GV_VERSION=${GV_ARR_ENV[GV_ZABBIX_POSTFIX]}
VERSION=rocky-${GV_VERSION}
ADDRESS=registry.cn-shanghai.aliyuncs.com/zabbix_docker/zabbix_chinese
for IM in `cat ./patch/.images_mysql_proxy`
do
docker pull ${ADDRESS}:${IM}_${VERSION}
docker tag ${ADDRESS}:${IM}_${VERSION} ${IM}:${VERSION}
docker rmi ${ADDRESS}:${IM}_${VERSION}
done
docker pull ${ADDRESS}:mariadb
docker tag ${ADDRESS}:mariadb mariadb:${GV_ARR_ENV[GV_MARIADB_VERSION]}
docker rmi ${ADDRESS}:mariadb