### syntax=docker/dockerfile:1
FROM rockylinux:8
ADD repos.tar.gz /etc/yum.repos.d/
RUN set -eux && \
yum makecache
