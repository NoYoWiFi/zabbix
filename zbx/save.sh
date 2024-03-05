GV_ENV_SHELL="./patch/.env_shell"
source ./patch/getEnv.sh
GV_VERSION=${GV_ARR_ENV[GV_ZABBIX_POSTFIX]}
VERSION=rocky-${GV_VERSION}
for IM in `cat ./patch/.images_mysql_save`
do
docker save -o ${IM}.tar.gz  ${IM}:${VERSION}
done
docker save -o centos.tar.gz quay.io/centos/centos:stream8
docker save -o mariadb.tar.gz mariadb:${GV_ARR_ENV[GV_MARIADB_VERSION]}
