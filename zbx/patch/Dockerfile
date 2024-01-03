# syntax=docker/dockerfile:1
FROM quay.io/centos/centos:stream8
ADD repos.tar.gz /etc/yum.repos.d/
RUN set -eux && \
yum makecache
