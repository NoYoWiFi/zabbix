### syntax=docker/dockerfile:1
FROM rockylinux:9-minimal
ADD repos.tar.gz /etc/yum.repos.d/
RUN set -eux && \
mkdir -p /etc/yum.repos.d/bak && \
mv /etc/yum.repos.d/rocky* /etc/yum.repos.d/bak && \
microdnf makecache
