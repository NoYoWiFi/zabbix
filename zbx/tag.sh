VERSION=centos-${1}
NEW_VERSION=centos-${2}
for IM in `cat ./patch/.images`
do
docker tag ${IM}:${VERSION} ${IM}:${NEW_VERSION}
docker rmi ${IM}:${VERSION}
done
