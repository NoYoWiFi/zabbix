GV_VERSION=$(cat ./patch/.version_docker)
VERSION=centos-${GV_VERSION}
for IM in `cat ./patch/.images_mysql_save`
do
docker save -o ${IM}.tar.gz  ${IM}:${VERSION}
done
docker save -o centos.tar.gz quay.io/centos/centos:stream8
docker save -o mariadb.tar.gz mariadb:11.2.3
