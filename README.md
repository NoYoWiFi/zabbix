### 项目地址

|标题|链接  |
|--|--|
| centos_7_zabbix_5.0.x_mysql | [centos_7_zabbix_5.0.x_mysql](https://gitcode.com/fantasywith/zabbix/tree/centos_7_zabbix_5.0.x_mysql) |
| centos_7_zabbix_7.0.x_mysql | [centos_7_zabbix_7.0.x_mysql](https://gitcode.com/fantasywith/zabbix/tree/centos_7_zabbix_7.0.x_mysql) |
| centos_7_zabbix_7.0.x_pgsql | [centos_7_zabbix_7.0.x_pgsql](https://gitcode.com/fantasywith/zabbix/tree/centos_7_zabbix_7.0.x_pgsql) |
| rocky_8_zabbix_6.0.x_mysql | [rocky_8_zabbix_6.0.x_mysql](https://gitcode.com/fantasywith/zabbix/tree/rocky_8_zabbix_6.0.x_mysql) |
| rocky_8_zabbix_6.0.x_pgsql | [rocky_8_zabbix_6.0.x_pgsql](https://gitcode.com/fantasywith/zabbix/tree/rocky_8_zabbix_6.0.x_pgsql) |
| rocky_8_zabbix_7.0.x_mysql | [rocky_8_zabbix_7.0.x_mysql](https://gitcode.com/fantasywith/zabbix/tree/rocky_8_zabbix_7.0.x_mysql) |
| rocky_8_zabbix_7.0.x_pgsql | [rocky_8_zabbix_7.0.x_pgsql](https://gitcode.com/fantasywith/zabbix/tree/rocky_8_zabbix_7.0.x_pgsql) |
| rocky_9_zabbix_7.0.x_pgsql | [rocky_9_zabbix_7.0.x_pgsql](https://gitcode.com/fantasywith/zabbix/tree/rocky_9_zabbix_7.0.x_pgsql) |
| kylin_v10_zabbix_7.0.x_mysql | [kylin_v10_zabbix_7.0.x_mysql](https://gitcode.com/fantasywith/zabbix/tree/kylin_v10_zabbix_7.0.x_mysql) |
| kylin_v10_zabbix_7.0.x_pgsql | [kylin_v10_zabbix_7.0.x_pgsql](https://gitcode.com/fantasywith/zabbix/tree/kylin_v10_zabbix_7.0.x_pgsql) |
| zabbix_6.0.x_docker | [zabbix_6.0.x_docker](https://gitcode.com/fantasywith/zabbix/tree/zabbix_6.0.x_docker) |
| zabbix_6.0.x_dockerfile | [zabbix_6.0.x_dockerfile](https://gitcode.com/fantasywith/zabbix/tree/zabbix_6.0.x_dockerfile) |
| zabbix_7.0.x_docker | [zabbix_7.0.x_docker](https://gitcode.com/fantasywith/zabbix/tree/zabbix_7.0.x_docker) |
| zabbix_7.0.x_dockerfile | [zabbix_7.0.x_dockerfile](https://gitcode.com/fantasywith/zabbix/tree/zabbix_7.0.x_dockerfile) |
| zabbix_api | [zabbix_api](https://gitcode.com/fantasywith/zabbix/tree/zabbix_api) |
| zabbix_7.0.x_build | [zabbix_7.0.x_build](https://gitcode.com/fantasywith/zabbix/tree/zabbix_7.0.x_build) |


### 克隆项目文件
```
# **执行如下命令克隆 NoYoWiFi 编排好的 zabbix 项目**
ZBX_SOURCES=https://'public':'EnSy68rd-72hN-Lnn_zYVpFQ'@gitcode.com/fantasywith/zabbix.git
ZBX_BRANCH=zabbix_7.0.x_build
ZBX_TODIR=/opt/${ZBX_BRANCH}
cd ${ZBX_TODIR}
git -c advice.detachedHead=false clone ${ZBX_SOURCES} --branch ${ZBX_BRANCH} --depth 1 --single-branch ${ZBX_TODIR}/
chmod 755 -R ${ZBX_TODIR}/
cd ${ZBX_TODIR}/
```

### <center><font color=#ff0000> 警告！警告！警告！</font></center>

<font color=#ff0000> ！！！重要的事情说三遍！！！</font>
`千万不要将 /usr/local/lib 和 /usr/local/lib64 添加到 /etc/ld.so.conf 文件或 /etc/ld.so.conf.d 目录`
`千万不要将 /usr/local/lib 和 /usr/local/lib64 添加到 /etc/ld.so.conf 文件或 /etc/ld.so.conf.d 目录`
`千万不要将 /usr/local/lib 和 /usr/local/lib64 添加到 /etc/ld.so.conf 文件或 /etc/ld.so.conf.d 目录`
<font color=#ff0000> ！！！重要的事情说三遍！！！</font>

```
# 完全编译完成后磁盘使用情况
[root@localhost ~]# du -sh /usr/local/
28G	/usr/local/
[root@localhost ~]# 
```
-------------------------------------------------------------------------------------------------------

## yum 安装编译工具及依赖 
```
yum -y install gcc-c++ glibc-devel m4 libtool unzip python-devel rpm-build policycoreutils-devel xz-devel 

libtool --finish /usr/local/lib
libtool --finish /usr/local/lib64
libtool --finish /usr/local/opt/glibc/lib
go env -w GO111MODULE=on && \
go env -w GOPROXY=https://goproxy.cn,direct && \
go env -w GOBIN=/usr/local/opt/go/bin
declare -x ACLOCAL_PATH="/usr/local/share/aclocal/"
declare -x LD_LIBRARY_PATH="/usr/local/src/perl5-5.26.3:/usr/local/lib:/usr/local/lib64"
declare -x JAVA_HOME=/usr/local/lib/jvm/jdk1.8.0_202
declare -x JRE_HOME=${JAVA_HOME}/jre  
declare -x CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
declare -x JAVA_PATH=${JAVA_HOME}/bin:${JRE_HOME}/bin
declare -x PATH="${JAVA_PATH}:/usr/local/opt/venv_37_centos7/bin:/usr/local/opt/go/bin:/usr/local/opt/glibc/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin"
declare -x PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:/usr/local/lib64/pkgconfig"
# 如果想启用yum打开下面的LD_PRELOAD变量，关闭使用unset LD_PRELOAD
# export LD_PRELOAD="/usr/lib64/liblzma.so.5:/usr/local/lib64/libcrypto.so.1.1:/usr/local/lib64/libssl.so.1.1"

pkg-config --cflags --libs libffi
pkg-config --cflags --libs libreadline
pkg-config --modversion nettle
pkg-config --modversion libreadline

# yum -y install install python-devel bzip2 unixODBC unixODBC-devel device-mapper rpm libaio* rpm-build libxml2-devel bzip2-devel libpng-devel libjpeg-devel freetype-devel readline-devel libxslt-devel elfutils-libelf-devel
```

### <center>编译安装make</center>

### 编译安装make ^make
<span id="make"></span>

 \[[[#^make-error\|依赖 make-error]]\]
 [依赖 make-error](#make-error)

```
https://ftp.gnu.org/gnu/make/make-4.2.1.tar.gz
tar -zxvf /opt/make-4.2.1.tar.gz -C /usr/local/src
cd /usr/local/src/make-4.2.1
mkdir build
cd build
../configure --prefix=/usr/local/
make -j4 && make install
ln -sf /usr/local/bin/make /usr/local/bin/gmake
```

-------------------------------------------------------------------------------------------------------

## <center>编译安装gcc</center>

### 编译安装gmp ^gmp
<span id="gmp"></span>

```
https://gmplib.org/download/gmp/gmp-6.1.2.tar.xz
tar -xvf /opt/gmp-6.1.2.tar.xz -C /usr/local/src
cd /usr/local/src/gmp-6.1.2
mkdir build
cd build
../configure --prefix=/usr/local
make -j4 && make install
```

### 编译安装mpfr ^mpfr
<span id="mpfr"></span>

 \[[[#^gmp\|依赖 gmp]]\]
 [依赖 gmp](#gmp)


1. 下载安装包
```
https://www.cnblogs.com/zhiminyu/p/18267733
http://www.multiprecision.org/downloads/mpfr-3.1.6.tar.gz
tar -zxvf /opt/mpfr-3.1.6.tar.gz -C /usr/local/src
cd /usr/local/src/mpfr-3.1.6
mkdir build
cd build
../configure --prefix=/usr/local --with-gmp=/usr/local
make -j4 && make install
```

### 编译安装mpc ^mpc

<span id="mpc"></span>

\[[[#^mpfr\|依赖 mpfr]]\] |  \[[[#^gmp\|依赖 gmp]]\]
[依赖 mpfr](#mpfr) | [依赖 gmp](#gmp)

1. 下载安装包
```
https://www.cnblogs.com/zhiminyu/p/18267733
http://www.multiprecision.org/downloads/mpc-0.9.tar.gz
tar -zxvf /opt/mpc-0.9.tar.gz -C /usr/local/src
cd /usr/local/src/mpc-0.9
mkdir build
cd build
../configure --prefix=/usr/local --with-gmp=/usr/local --with-mpfr=/usr/local
make -j4 && make install
```

### 编译安装isl ^isl
<span id="isl"></span>

 \[[[#^gmp\|依赖 gmp]]\]
[依赖 gmp](#gmp)

1. 下载安装包
```
https://libisl.sourceforge.io/isl-0.16.1.tar.gz
tar -zxvf /opt/isl-0.16.1.tar.gz -C /usr/local/src
cd /usr/local/src/isl-0.16.1
mkdir build
cd build
../configure --prefix=/usr/local --with-gmp-prefix=/usr/local
make -j4 && make install
```

### 编译安装gcc ^gcc
<span id="gcc"></span>

 \[[[#^mpc\|依赖 mpc]]\] |  \[[[#^gmp\|依赖 gmp]]\] |  \[[[#^mpfr\|依赖 mpfr]]\] |  \[[[#^isl\|依赖 isl]]\]
[依赖 mpc](#mpc) | [依赖 gmp](#gmp) | [依赖 mpfr](#mpfr) | [依赖 gmp](#gmp) | [依赖 isl](#isl)
1. 下载安装包
```
https://ftp.gnu.org/gnu/gcc/gcc-8.5.0/gcc-8.5.0.tar.gz
tar -zxvf /opt/gcc-8.5.0.tar.gz -C /usr/local/src
cd /usr/local/src/gcc-8.5.0
mkdir build
cd build
../configure --prefix=/usr/local --enable-checking=release --enable-languages=c,c++ --disable-multilib --enable-linker-build-id --with-gmp=/usr/local --with-gmp-include=/usr/local/include --with-gmp-lib=/usr/local/lib --with-mpfr=/usr/local --with-mpfr-include=/usr/local/include --with-mpfr-lib=/usr/local/lib --with-mpc=/usr/local --with-mpc-include=/usr/local/include --with-mpc-lib=/usr/local/lib -with-isl=/usr/local --with-isl-lib=/usr/local/lib --with-isl-include=/usr/local/include
make -j4
make -j4 install
ln -sf /usr/local/bin/gcc /usr/local/bin/cc
```

```
----------------------------------------------------------------------
Libraries have been installed in:
   /usr/local/gcc-8.5.0/gcc/lib/../lib64

If you ever happen to want to link against installed libraries
in a given directory, LIBDIR, you must either use libtool, and
specify the full pathname of the library, or use the `-LLIBDIR'
flag during linking and do at least one of the following:
   - add LIBDIR to the `LD_LIBRARY_PATH' environment variable
     during execution
   - add LIBDIR to the `LD_RUN_PATH' environment variable
     during linking
   - use the `-Wl,-rpath -Wl,LIBDIR' linker flag
   - have your system administrator add LIBDIR to `/etc/ld.so.conf'

See any operating system documentation about shared libraries for
more information, such as the ld(1) and ld.so(8) manual pages.
----------------------------------------------------------------------
```

### 编译安装 m4 ^m4
<span id="m4"></span>

```
https://ftp.gnu.org/gnu/m4/m4-1.4.18.tar.gz
tar -zxvf /opt/m4-1.4.18.tar.gz -C /usr/local/src
cd /usr/local/src/m4-1.4.18
# sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
# echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h
mkdir build
cd build
../configure --prefix=/usr/local
make -j4
make -j4 install
```

### 编译安装 automake ^automake
<span id="automake"></span>

\[[[#^m4\|依赖 m4]]\]
[依赖 m4](#m4)

```
https://ftp.gnu.org/gnu/automake/automake-1.16.1.tar.gz
tar -zxvf /opt/automake-1.16.1.tar.gz -C /usr/local/src
cd /usr/local/src/automake-1.16.1
mkdir build
cd build
../configure --prefix=/usr/local
make -j4
make -j4 install
```

### 编译安装 autoconf ^autoconf
<span id="autoconf"></span>

\[[[#^automake\|依赖 automake]]\]
[依赖 automake](#automake)

```
http://mirrors.kernel.org/gnu/autoconf/autoconf-2.69.tar.gz
tar -zxvf /opt/autoconf-2.69.tar.gz -C /usr/local/src
cd /usr/local/src/autoconf-2.69
mkdir build
cd build
declare -x M4=/usr/local/bin/m4
../configure --prefix=/usr/local
make -j4
make -j4 install
```

### 编译安装libtool ^libtool
<span id="libtool"></span>

```
https://mirrors.sjtug.sjtu.edu.cn/gnu/libtool/libtool-2.4.6.tar.gz
tar -zxvf /opt/libtool-2.4.6.tar.gz -C /usr/local/src
cd /usr/local/src/libtool-2.4.6
mkdir build
cd build/
# ../configure --prefix=/usr/local/libtool-2.4.6/libtool
../configure --prefix=/usr/local
make -j4 && make install
```

### 编译安装bzip2 ^bzip2
<span id="bzip2"></span>

```
https://sourceware.org/pub/bzip2/bzip2-1.0.7.tar.gz
tar -zxvf /opt/bzip2-1.0.7.tar.gz -C /usr/local/src
cd /usr/local/src/bzip2-1.0.7
make -j4
make -j4 install PREFIX=/usr/local
make clean
make -j4 -f Makefile-libbz2_so
make -j4 install PREFIX=/usr/local
\cp libbz2.so.1.0* /usr/local/lib/
```

### 编译安装pkgconf ^pkgconf
<span id="pkgconf"></span>

```
https://codeload.github.com/pkgconf/pkgconf/tar.gz/refs/tags/pkgconf-1.4.2
tar -zxvf /opt/pkgconf-pkgconf-1.4.2.tar.gz -C /usr/local/src
cd /usr/local/src/pkgconf-pkgconf-1.4.2
autoreconf -vifs
mkdir build
cd build
../configure --prefix=/usr/local --enable-shared
make -j4
make -j4 install
ln -sf /usr/local/bin/pkgconf /usr/local/bin/pkg-config
```
-------------------------------------------------------------------------------------------------------

## <center>编译安装glibc</center>

### 编译perl ^perl
<span id="perl"></span>

```
https://codeload.github.com/Perl/perl5/tar.gz/refs/tags/v5.26.3
tar -xvf /opt/perl5-5.26.3.tar.gz -C /usr/local/src
cd /usr/local/src/perl5-5.26.3/
./Configure -des -Dprefix=/usr/local -Duseshrplib  -Dusethreads -Uversiononly
make -j4
make -j4 install
```

### 编译bison ^bison
<span id="bison"></span>

 \[[[#^perl\|依赖 perl]]\]
[依赖 perl](#perl)

```
http://ftp.gnu.org/gnu/bison/bison-3.0.4.tar.xz
tar -xvf /opt/bison-3.0.4.tar.xz -C /usr/local/src
cd /usr/local/src/bison-3.0.4
# sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
# echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h
mkdir build
cd build
../configure --prefix=/usr/local
make -j4
make  -j4 install
```

### 编译安装glibc ^glibc
<span id="glibc"></span>

 \[[[#^bison\|依赖 bison]]\] 
[依赖 bison](#bison)

1. 下载安装包
```
https://ftp.gnu.org/gnu/glibc/glibc-2.28.tar.gz
tar -zxvf /opt/glibc-2.28.tar.gz -C /usr/local/src
cd /usr/local/src/glibc-2.28
mkdir build
cd build
mkdir -p /usr/local/opt
../configure --prefix=/usr/local/opt/glibc  --enable-shared --bindir=/usr/local
make -j4 && make install
```

-------------------------------------------------------------------------------------------------------

## <center>cmake编译安装</center>

### 编译安装openssl ^openssl
<span id="openssl"></span>

```
https://openssl-library.org/source/old/1.1.1/index.html
tar -zxvf /opt/openssl-1.1.1w.tar.gz -C /usr/local/src
cd /usr/local/src/openssl-1.1.1w
mkdir build
cd build
../config --shared enable-ssl3 enable-ssl3-method enable-mdc2 enable-md2 --prefix=/usr/local 
make -j4 && make install
```

### 编译zlib ^zlib
<span id="zlib"></span>

```
https://zlib.net/fossils/zlib-1.2.11.tar.gz
tar -zxvf /opt/zlib-1.2.11.tar.gz -C /usr/local/src
cd /usr/local/src/zlib-1.2.11
mkdir build
cd build
../configure --prefix=/usr/local
make -j4 && make install
```

### 编译安装pam ^pam
<span id="pam"></span>
```
https://codeload.github.com/linux-pam/linux-pam/tar.gz/refs/tags/v1.3.1
tar -xvf /opt/Linux-PAM-1.3.1.tar.xz -C /usr/local/src
cd /usr/local/src/Linux-PAM-1.3.1
mkdir build
cd build
../configure --prefix=/usr/local
make -j4 && make install
mkdir -p /usr/local/include/security
mv -vf /usr/local/include/pam* /usr/local/include/security
mv -vf /usr/local/include/_pam_* /usr/local/include/security
```


### 编译安装openssh ^openssh
<span id="openssh"></span>

 \[[[#^openssl\|依赖 openssl]]\] |  \[[[#^pam\|依赖 pam]]\] |  \[[[#^zlib\|依赖 zlib]]\]
[依赖 openssl](#openssl) | [依赖 pam](#pam) | [依赖 zlib](#zlib)

```
https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-8.0p1.tar.gz
tar -zxvf /opt/openssh-8.0p1.tar.gz -C /usr/local/src
cd /usr/local/src/openssh-8.0p1
mkdir build
cd build

../configure --prefix=/usr/local  --with-ssl-dir=/usr/local --with-zlib=/usr/local --with-md5-passwords --with-pam

make -j4
make install
```

### 编译安装cmake ^cmake
<span id="cmake"></span>

 \[[[#^openssl\|依赖 openssl]]\] |  \[[[#^gcc\|依赖 gcc]]\]
 [依赖 openssl](#openssl) | [依赖 gcc](#gcc)

```
https://cmake.org/files/v3.16/cmake-3.16.8.tar.gz
tar -zxvf /opt/cmake-3.16.8.tar.gz -C /usr/local/src
cd /usr/local/src/cmake-3.16.8
mkdir build
cd build
../bootstrap --prefix=/usr/local
gmake -j4 && gmake install
```

-------------------------------------------------------------------------------------------------------

## <center>python3.7编译安装</center>

### 编译libffi ^libffi
<span id="libffi"></span>

```
https://codeload.github.com/libffi/libffi/tar.gz/refs/tags/v3.4.4
tar -zxvf /opt/libffi-3.4.4.tar.gz -C /usr/local/src
cd /usr/local/src/libffi-3.4.4
mkdir build
cd build
../configure --prefix=/usr/local
make -j4
make -j4 install
ln -sf /usr/local/lib64/libffi.so /usr/local/lib/libffi.so
```

### 编译python3.7 ^python37
<span id="python37"></span>

\[[[#^zlib\|依赖 zlib]]\] | \[[[#^libffi\|依赖 libffi]]\] | \[[[#^openssl\|依赖 openssl]]\]
 [依赖 zlib](#zlib) | [依赖 libffi](#libffi) | [依赖 openssl](#openssl)
 
```
https://mirrors.huaweicloud.com/python/3.7.0/
tar -xvf /opt/Python-3.7.0.tar.xz -C /usr/local/src
cd /usr/local/src/Python-3.7.0
mkdir build
cd build

../configure --prefix=/usr/local --with-openssl=/usr/local --enable-shared
make -j4
make install
```

### 编译pycurl ^pycurl
<span id="pycurl"></span>

\[[[#^openssl\|依赖 openssl]]\]
[依赖 openssl](#openssl)

```
# 解决yum无法使用问题
https://pypi.org/project/pycurl/7.43.0.3/#files
tar -zxvf /opt/pycurl-7.43.0.3.tar.gz -C /usr/local/src
cd /usr/local/src/pycurl-7.43.0.3/

# 报错略过
python3 setup.py  --with-openssl install
python2 setup.py  --with-openssl install

```

-------------------------------------------------------------------------------------------------------

## <center>git编译安装</center>

### 编译pcre2 ^pcre2
<span id="pcre2"></span>

```
https://github.com/PCRE2Project/pcre2/releases?page=2
tar -xvf /opt/pcre2-10.32.tar.gz -C /usr/local/src
cd /usr/local/src/pcre2-10.32/
mkdir build
cd build
../configure --prefix=/usr/local --enable-pcre2grep-libz
make -j4
make -j4 install
```

### 编译安装libssh2 ^libssh2
<span id="libssh2"></span>

\[[[#^openssl\|依赖 openssl]]\] | \[[[#^zlib\|依赖 zlib]]\]
 [依赖 zlib](#zlib) | [依赖 openssl](#openssl)
 
1. 下载安装包
```
https://libssh2.org/download/libssh2-1.11.1.tar.xz
tar -xvf /opt/libssh2-1.11.1.tar.xz -C /usr/local/src
cd /usr/local/src/libssh2-1.11.1
mkdir cmake-build
cd cmake-build/
cmake -D OPENSSL_ROOT_DIR="/usr/local" -D CMAKE_INSTALL_PREFIX=/usr/local -D OPENSSL_CRYPTO_LIBRARY="/usr/local/lib64/libcrypto.so" -D OPENSSL_SSL_LIBRARY="/usr/local/lib64/libssl.so" -D ZLIB_INCLUDE_DIR="/usr/local/include" -D ZLIB_LIBRARY="/usr/local/lib/libz.so" ..

gmake -j4 && gmake install
```

### 编译安装berkeley-db ^berkeley-db
<span id="berkeley-db"></span>

\[[[#^libtool\|依赖 libtool]]\]
[依赖 libtool](#libtool) 
 
```
http://download.oracle.com/berkeley-db/db-5.1.29.tar.gz
tar -zxvf /opt/db-5.1.29.tar.gz -C /usr/local/src
cd /usr/local/src/db-5.1.29
mkdir build
cd build/
../dist/configure --prefix=/usr/local
make -j4 && make install
```

### 编译安装openldap ^openldap
<span id="openldap"></span>

\[[[#^berkeley-db\|依赖 berkeley-db]]\]
[依赖 berkeley-db](#berkeley-db) 

1. 下载安装包
```
https://www.openldap.org/software/download/OpenLDAP/openldap-release/openldap-2.4.46.tgz
tar -zxvf /opt/openldap-2.4.46.tgz -C /usr/local/src
yum install libtool-ltdl-devel -y

cd /usr/local/src/openldap-2.4.46
mkdir build
cd build/

../configure --prefix=/usr/local
make depend
make -j4 && make install
```
--------------------------------------------------111111111111111111111
### 编译curl ^curl
<span id="curl"></span>

\[[[#^openssl\|依赖 openssl]]\] | \[[[#^zlib\|依赖 zlib]]\] | \[[[#^libssh2\|依赖 libssh2]]\] | \[[[#^openldap\|依赖 openldap]]\]
[依赖 openssl](#openssl) | [依赖 zlib](#zlib) | [依赖 libssh2](#libssh2) | [依赖 openldap](#openldap) 

```
https://curl.se/download/curl-7.61.1.tar.gz
tar -zxvf /opt/curl-7.61.1.tar.gz -C /usr/local/src
cd /usr/local/src/curl-7.61.1/
mkdir build
cd build

../configure --prefix=/usr/local --with-zlib=/usr/local --with-libssh2=/usr/local --with-ssl=/usr/local --without-nss --with-ldap-lib=ldap

make -j4
make install
```

### 编译expat ^expat
<span id="expat"></span>

```
https://github.com/libexpat/libexpat/releases/tag/R_2_2_5
tar -jxvf /opt/expat-2.2.5.tar.bz2 -C /usr/local/src
cd /usr/local/src/expat-2.2.5/
mkdir build
cd build
../configure --prefix=/usr/local
make -j4 
make -j4 install
```

### 编译libiconv ^libiconv
<span id="libiconv"></span>

```
https://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.16.tar.gz
tar -zxvf /opt/libiconv-1.16.tar.gz -C /usr/local/src
cd /usr/local/src/libiconv-1.16/
mkdir build
cd build
../configure --prefix=/usr/local
make -j4 
make -j4 install
```

###  <font color=#008000> 编译git</font> ^git
<span id="git"></span>

\[[[#^pcre2\|依赖 pcre2]]\] | \[[[#^openssl\|依赖 openssl]]\] | \[[[#^libpcre2\|依赖 libpcre2]]\] | \[[[#^perl\|依赖 perl]]\] | \[[[#^zlib\|依赖 zlib]]\] | \[[[#^curl\|依赖 curl]]\] | \[[[#^expat\|依赖 expat]]\] | \[[[#^iconv\|依赖 iconv]]\]
[依赖 pcre2](#pcre2) | [依赖 openssl](#openssl) | [依赖 libpcre2](#libpcre2) | [依赖 perl](#perl) | [依赖 zlib](#zlib) | [依赖 curl](#curl) | [依赖 expat](#expat) | [依赖 iconv](#iconv) 

```
https://www.kernel.org/pub/software/scm/git/git-2.43.0.tar.gz
tar -zxvf /opt/git-2.43.0.tar.gz -C /usr/local/src
cd /usr/local/src/git-2.43.0/
./configure --prefix=/usr/local --with-openssl --with-libpcre2 --with-perl=/usr/local/bin/perl --with-zlib=/usr/local --with-curl --with-expat --with-iconv=/usr/local
make -j4
make -j4 install
```

-------------------------------------------------------------------------------------------------------

## <center>MariaDB-server编译安装</center>

### 编译fmt ^fmt
<span id="fmt"></span>

```
https://github.com/fmtlib/fmt/releases/download/11.0.2/fmt-11.0.2.zip
unzip /opt/fmt-11.0.2.zip -d /usr/local/src/
cd /usr/local/src/fmt-11.0.2
mkdir cmake-build
cd cmake-build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local
gmake -j4
gmake -j4 install
```


### 编译zstd ^zstd
<span id="zstd"></span>

 
```
https://github.com/facebook/zstd/releases/tag/v1.4.1
tar -zxvf /opt/zstd-1.4.1.tar.gz -C /usr/local/src
cd /usr/local/src/zstd-1.4.1/build/cmake/
mkdir cmake-build
cd cmake-build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local
make -j4
make -j4 install
```

### 编译icu ^icu
<span id="icu"></span>

```
https://github.com/unicode-org/icu/releases/tag/release-60-3
tar -zxvf /opt/icu4c-60_3-src.tgz -C /usr/local/src
cd /usr/local/src/icu
mkdir build 
cd build
../source/configure --prefix=/usr/local
make -j4
make install
```

### 编译boost ^boost
<span id="boost"></span>

\[[[#^icu\|依赖 icu]]\]
 [依赖 icu](#icu) 
 
```
https://archives.boost.io/release/1.81.0/source/boost_1_81_0.tar.gz
tar -zxvf /opt/boost_1_81_0.tar.gz -C /usr/local/src
cd /usr/local/src/boost_1_81_0
./bootstrap.sh --prefix=/usr/local --with-icu=/usr/local
./b2 install
```

### 编译libmd ^libmd
<span id="libmd"></span>

```
https://archive.hadrons.org/software/libmd/libmd-1.1.0.tar.xz
tar -xvf /opt/libmd-1.1.0.tar.xz -C /usr/local/src
cd /usr/local/src/libmd-1.1.0/
mkdir build
cd build
../configure --prefix=/usr/local
make -j4
make -j4 install
```

### 编译gettext ^gettext
<span id="gettext"></span>

```
https://ftp.gnu.org/pub/gnu/gettext/gettext-0.19.8.tar.gz
tar -zxvf /opt/gettext-0.19.8.tar.gz -C /usr/local/src
cd /usr/local/src/gettext-0.19.8/
mkdir build
cd build
../configure --prefix=/usr/local
make -j4 
make -j4 install
```

### 编译ncurses ^ncurses
<span id="ncurses"></span>

```
http://ftp.gnu.org/pub/gnu/ncurses/ncurses-6.1.tar.gz
tar -zxvf /opt/ncurses-6.1.tar.gz -C /usr/local/src
cd /usr/local/src/ncurses-6.1/
mkdir build
cd build
../configure --prefix=/usr/local --with-shared --with-gpm --with-libtool --with-normal --with-debug --enable-overwrite --enable-pc-files
make -j4 
make -j4 install
```

### 编译nettle ^nettle
<span id="nettle"></span>

\[[[#^gmp\|依赖 gmp]]\]
 [依赖 gmp](#gmp) 
 
```
https://ftp.gnu.org/gnu/nettle/nettle-3.4.1.tar.gz
tar -zxvf /opt/nettle-3.4.1.tar.gz -C /usr/local/src
cd /usr/local/src/nettle-3.4.1/
mkdir build
cd build
../configure --prefix=/usr/local
make -j4
make -j4 install
chmod +x /usr/local/lib64/libnettle*
```

### 编译libtasn1 ^libtasn1
<span id="libtasn1"></span>

```
https://ftp.gnu.org/gnu/libtasn1/libtasn1-4.13.tar.gz
tar -zxvf /opt/libtasn1-4.13.tar.gz -C /usr/local/src
cd /usr/local/src/libtasn1-4.13/
mkdir build
cd build
../configure --prefix=/usr/local
make -j4 
make -j4 install
```

### 编译libunistring ^libunistring
<span id="libunistring"></span>

```
https://ftp.gnu.org/gnu/libunistring/libunistring-0.9.9.tar.gz
tar -zxvf /opt/libunistring-0.9.9.tar.gz -C /usr/local/src
cd /usr/local/src/libunistring-0.9.9/
# sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
# echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h
mkdir build
cd build
../configure --prefix=/usr/local
make -j4 
make -j4 install
```

### 编译libidn2 ^libidn2
<span id="libidn2"></span>

```
https://ftp.gnu.org/gnu/libidn/libidn2-2.2.0.tar.gz
tar -zxvf /opt/libidn2-2.2.0.tar.gz -C /usr/local/src
cd /usr/local/src/libidn2-2.2.0/
mkdir build
cd build
../configure --prefix=/usr/local
make -j4 
make -j4 install
```

### 编译unbound ^unbound
<span id="unbound"></span>

\[[[#^openssl\|依赖 openssl]]\] | \[[[#^expat\|依赖 expat]]\]
 [依赖 openssl](#openssl) |  [依赖 expat](#expat) 
 
```
https://codeload.github.com/NLnetLabs/unbound/tar.gz/refs/tags/release-1.16.2
tar -zxvf /opt/unbound-release-1.16.2.tar.gz -C /usr/local/src
cd /usr/local/src/unbound-release-1.16.2/
./configure --prefix=/usr/local --with-ssl=/usr/local --with-libexpat=/usr/local
make -j4 
make -j4 install
```

### 编译p11-kit ^p11-kit
<span id="p11-kit"></span>

\[[[#^libtasn1\|依赖 libtasn1]]\] | \[[[#^libffi\|依赖 libffi]]\]
 [依赖 libtasn1](#libtasn1) |  [依赖 libffi](#libffi) 

```
https://github.com/p11-glue/p11-kit/releases/tag/0.23.22
tar -xvf /opt/p11-kit-0.23.22.tar.xz -C /usr/local/src
cd /usr/local/src/p11-kit-0.23.22/
mkdir build
cd build
../configure --prefix=/usr/local
make -j4 
make -j4 install
```

### 编译gnutls ^gnutls
<span id="gnutls"></span>

\[[[#^gmp\|依赖 gmp]]\] | \[[[#^libunistring\|依赖 libunistring]]\] | \[[[#^unbound\|依赖 unbound]]\] | \[[[#^libtasn1\|依赖 libtasn1]]\] | \[[[#^nettle\|依赖 nettle]]\] | \[[[#^p11-kit\|依赖 p11-kit]]\] | \[[[#^libidn2\|依赖 libidn2]]\]
[依赖 gmp](#gmp) | [依赖 libunistring](#libunistring) | [依赖 unbound](#unbound) | [依赖 libtasn1](#libtasn1) | [依赖 nettle](#nettle) | [依赖 p11-kit](#p11-kit) | [依赖 libidn2](#libidn2)

```
http://www.ring.gr.jp/pub/net/gnupg/gnutls/v3.6/gnutls-3.6.16.tar.xz
tar -xvf /opt/gnutls-3.6.16.tar.xz -C /usr/local/src
cd /usr/local/src/gnutls-3.6.16/
mkdir build
cd build
mkdir /etc/unbound
/usr/local/sbin/unbound-anchor -a /etc/unbound/root.key
../configure --prefix=/usr/local
make -j4 
make -j4 install
```

### 安装java ^java
<span id="java"></span>

```
https://repo.huaweicloud.com/java/jdk/8u202-b08/
mkdir -p /usr/local/lib/jvm
tar -zxvf /opt/jdk-8u202-linux-x64.tar.gz -C /usr/local/lib/jvm
java -version
ln -sf /usr/local/lib/jvm/jdk1.8.0_202/include/linux/jni_md.h /usr/local/lib/jvm/jdk1.8.0_202/include/jni_md.h
ln -sf /usr/local/lib/jvm/jdk1.8.0_202/include/linux/jawt_md.h /usr/local/lib/jvm/jdk1.8.0_202/include/jawt_md.h
```

### 编译安装libenvent ^libenvent
<span id="libenvent"></span>

```
https://github.com/libevent/libevent/releases/download/release-2.1.8-stable/libevent-2.1.8-stable.tar.gz
tar -zxvf /opt/libevent-2.1.8-stable.tar.gz -C /usr/local/src
cd /usr/local/src/libevent-2.1.8-stable

./configure --prefix=/usr/local
make -j4
make -j4 install
```

### 编译安装mongo-c-driver ^mongo-c-driver
<span id="mongo-c-driver"></span>

```
https://github.com/mongodb/mongo-c-driver/releases/tag/1.29.1
tar -zxvf /opt/mongo-c-driver-1.29.1.tar.gz -C /usr/local/src
cd /usr/local/src/mongo-c-driver-1.29.1/
mkdir cmake-build
cd cmake-build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local/ -D OPENSSL_ROOT_DIR=/usr/local
make -j4
make -j4 install
mv -vf /usr/local/include/libbson-1.0/* /usr/local/include
```

### 编译安装 libxml2 ^libxml2
<span id="libxml2"></span>

```
http://xmlsoft.org/sources/libxml2-2.9.7.tar.gz
tar -zxvf /opt/libxml2-2.9.7.tar.gz -C /usr/local/src
cd /usr/local/src/libxml2-2.9.7
mkdir build
cd build
../configure --prefix=/usr/local
make -j4
make -j4 install
ln -sf /usr/local/include/libxml2/libxml /usr/local/include/libxml
```

### 编译安装 judy ^judy
<span id="judy"></span>

```
https://jaist.dl.sourceforge.net/project/judy/judy/Judy-1.0.5/Judy-1.0.5.tar.gz?viasf=1
tar -zxvf /opt/Judy-1.0.5.tar.gz -C /usr/local/src
cd /usr/local/src/judy-1.0.5
./configure --prefix=/usr/local
# make 报错再执行一次make即可
make -j4 && make install
```

### 编译安装 lz4 ^lz4
<span id="lz4"></span>

```
https://github.com/lz4/lz4/releases
tar -zxvf /opt/lz4-1.10.0.tar.gz -C /usr/local/src
cd /usr/local/src/lz4-1.10.0/build/cmake/
mkdir cmake-build
cd cmake-build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local
make -j4 && make -j4 install

```

### 编译安装 xz ^xz
<span id="xz"></span>

```
https://jaist.dl.sourceforge.net/project/lzmautils/xz-5.2.4.tar.gz?viasf=1
tar -zxvf /opt/xz-5.2.4.tar.gz -C /usr/local/src
cd /usr/local/src/xz-5.2.4/
mkdir build
cd build
../configure --prefix=/usr/local --enable-shared
make -j4
make -j4 install

```

### 编译安装 lzo ^lzo
<span id="lzo"></span>

```
http://www.oberhumer.com/opensource/lzo/download/lzo-2.08.tar.gz
tar -zxvf /opt/lzo-2.08.tar.gz -C /usr/local/src
cd /usr/local/src/lzo-2.08
mkdir build
cd build
../configure --prefix=/usr/local --enable-shared
make -j4 && make -j4 install

```

### 编译安装 krb5 ^krb5
<span id="krb5"></span>

```
https://kerberos.org/dist/krb5/1.18/krb5-1.18.2.tar.gz
tar -zxvf /opt/krb5-1.18.2.tar.gz -C /usr/local/src
cd /usr/local/src/krb5-1.18.2/src
mkdir build
cd build
../configure --prefix=/usr/local
make -j4
make -j4 install

```

### 编译安装 gssapi ^gssapi
<span id="gssapi"></span>

\[[[#^krb5\|依赖 krb5]]\]
[依赖 krb5](#krb5)

```
https://files.pythonhosted.org/packages/f7/17/1a316f0c6a1b802a9b4d6253068b4a3756cfef19fbd43d9747839d98ff30/gssapi-1.5.1.tar.gz
tar -zxvf /opt/gssapi-1.5.1.tar.gz -C /usr/local/src
cd /usr/local/src/gssapi-1.5.1

python3 -m venv /usr/local/opt/venv_37_centos7
source /usr/local/opt/venv_37_centos7/bin/activate

pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
pip3 install --upgrade setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple

pip3 install .
deactivate
```

### 编译安装 swig ^swig
<span id="swig"></span>

```
https://jaist.dl.sourceforge.net/project/swig/swig/swig-4.3.0/swig-4.3.0.tar.gz?viasf=1
tar -zxvf /opt/swig-4.3.0.tar.gz -C /usr/local/src
cd /usr/local/src/swig-4.3.0
mkdir build
cd build
../configure --prefix=/usr/local --with-pcre2-prefix=/usr/local
make -j4
make -j4 install

```

### 编译安装 kytea ^kytea
<span id="kytea"></span>

\[[[#^autoconf\|依赖 autoconf]]\]
[依赖 autoconf](#autoconf)

```
https://codeload.github.com/neubig/kytea/zip/refs/heads/master
unzip /opt/kytea-master.zip -d /usr/local/src
cd /usr/local/src/kytea-master
mkdir m4
autoreconf -vifs
mkdir build
cd build
../configure --prefix=/usr/local
make -j4
# 报错的话再执行一次
make -j4 install

```

### 编译安装 kytea-python ^kytea-python
<span id="kytea-python"></span>

\[[[#^swig\|依赖 swig]]\]
[依赖 swig](#swig)

```
https://files.pythonhosted.org/packages/bd/92/3a987ebc15180fdc8f69bf774ea9007e8f063949b229a432524e5aeed019/kytea-0.1.9.tar.gz
tar -zxvf /opt/kytea-0.1.9.tar.gz -C /usr/local/src
cd /usr/local/src/kytea-0.1.9

python3 -m venv /usr/local/opt/venv_37_centos7
source /usr/local/opt/venv_37_centos7/bin/activate

pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
pip3 install --upgrade setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple

swig -c++ -python -I/usr/local/include /usr/local/src/kytea-0.1.9/lib/kytea/mykytea.i

pip3 install .
deactivate
```

### 编译安装 snappy ^snappy
<span id="snappy"></span>

```
https://codeload.github.com/google/snappy/tar.gz/refs/tags/1.1.8
tar -zxvf /opt/snappy-1.1.8.tar.gz -C /usr/local/src
cd /usr/local/src/snappy-1.1.8/
mkdir cmake-build
cd cmake-build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local -DBUILD_SHARED_LIBS=1
gmake -j4
gmake -j4 install

```

### 编译安装 pyopenssl ^pyopenssl
<span id="pyopenssl"></span>

```
source /usr/local/opt/venv_37_centos7/bin/activate
pip3 install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
pip3 install pyopenssl msgpack-python
deactivate
```

### 编译安装 unixODBC ^unixODBC
<span id="unixODBC"></span>

```
https://www.unixodbc.org/unixODBC-2.3.7.tar.gz
tar -zxvf /opt/unixODBC-2.3.7.tar.gz -C /usr/local/src
cd /usr/local/src/unixODBC-2.3.7
mkdir build
cd build
../configure --prefix=/usr/local
make -j4
make -j4 install

```

### 编译安装 zeromq ^zeromq
<span id="zeromq"></span>

```
https://github.com/zeromq/libzmq/releases/tag/v4.3.5
tar -zxvf /opt/zeromq-4.3.5.tar.gz -C /usr/local/src
cd /usr/local/src/zeromq-4.3.5
mkdir build
cd build
../configure --prefix=/usr/local
make -j4
make -j4 install

```

### 编译安装 readline ^readline
<span id="readline"></span>

```
ftp://ftp.gnu.org/gnu/readline/
tar -zxvf /opt/readline-6.2.tar.gz -C /usr/local/src
cd /usr/local/src/readline-6.2
mkdir build
cd build
../configure --prefix=/usr/local --enable-shared --with-curses
# 该选项强制 Readline 链接该`libncurses`库
make -j4 SHLIB_LIBS="-lncurses"
make -j4 SHLIB_LIBS="-lncurses" install
rm -rf /usr/local/lib/libreadline.*.old
```

### 编译MariaDB-server ^MariaDB-server
<span id="MariaDB-server"></span>

\[[[#^fmt\|依赖 fmt]]\] | \[[[#^openssl\|依赖 openssl]]\] | \[[[#^boost\|依赖 boost]]\] | \[[[#^ncurses\|依赖 ncurses]]\] | \[[[#^curl\|依赖 curl]]\] | \[[[#^zstd\|依赖 zstd]]\] | \[[[#^gnutls\|依赖 gnutls]]\] | \[[[#^pcre2\|依赖 pcre2]]\] | \[[[#^bzip2\|依赖 bzip2]]\] | \[[[#^nettle\|依赖 nettle]]\] | | \[[[#^libenvent\|依赖 libenvent]]\] | \[[[#^pam\|依赖 pam]]\] | \[[[#^java\|依赖 java]]\] | \[[[#^zlib\|依赖 zlib]]\] | \[[[#^mongo-c-driver\|依赖 mongo-c-driver]]\] | \[[[#^libxml2\|依赖 libxml2]]\] | \[[[#^judy\|依赖 judy]]\] | \[[[#^lz4\|依赖 lz4]]\] | \[[[#^xz\|依赖 xz]]\] | \[[[#^lzo\|依赖 lzo]]\] | \[[[#^snappy\|依赖 snappy]]\] | \[[[#^pyopenssl\|依赖 pyopenssl]]\] | \[[[#^unixODBC\|依赖 unixODBC]]\] | \[[[#^kytea\|依赖 kytea]]\] | \[[[#^zeromq\|依赖 zeromq]]\] | \[[[#^readline\|依赖 readline]]\]

[依赖 fmt](#fmt) | [依赖 openssl](#openssl) | [依赖 boost](#boost) | [依赖 ncurses](#ncurses) | [依赖 curl](#curl) | [依赖 zstd](#zstd) | [依赖 gnutls](#gnutls)|[依赖 pcre2](#pcre2) | [依赖 bzip2](#bzip2) | [依赖 nettle](#nettle) | [依赖 libenvent](#libenvent) | [依赖 pam](#pam) | [依赖 java](#java) | [依赖 zlib](#zlib)|[依赖 mongo-c-driver](#mongo-c-driver) | [依赖 libxml2](#libxml2) | [依赖 judy](#judy) | [依赖 lz4](#lz4) | [依赖 xz](#xz) | [依赖 lzo](#lzo) | [依赖 snappy](#snappy)|[依赖 pyopenssl](#pyopenssl) | [依赖 unixODBC](#unixODBC) | [依赖 kytea](#kytea) | [依赖 zeromq](#zeromq) | [依赖 readline](#readline)
```
https://mirrors.tuna.tsinghua.edu.cn/mariadb/mariadb-10.11.11/source/mariadb-10.11.11.tar.gz
tar -zxvf /opt/mariadb-10.11.11.tar.gz -C /usr/local/src
cd /usr/local/src/mariadb-10.11.11
mkdir cmake-build
cd cmake-build

# 注释掉bcon.h，根据bson.h的使用规范只有bson/bson.h能被直接引用
vi /usr/local/src/mariadb-10.11.11/storage/connect/cmgoconn.h
      8 #include <bson/bson.h>
      9 /*#include <bson/bcon.h>*/

# 改成下面的样子避免类型错误
vi /usr/local/src/mariadb-10.11.11/storage/connect/cmgoconn.cpp
# 909-923
                        case BSON_TYPE_UTF8:
                                  value->SetValue_psz((PSZ)bson_iter_utf8(&Desc, NULL));
                                  break;
                        case BSON_TYPE_INT32:
                                  value->SetValue(static_cast<long long>(bson_iter_int32(&Desc)));
                                  break;
                        case BSON_TYPE_INT64:
                                  value->SetValue(static_cast<long long>(bson_iter_int64(&Desc)));
                                  break;
                        case BSON_TYPE_DOUBLE:
                                  value->SetValue(static_cast<long long>(bson_iter_double(&Desc)));
                                  break;
                        case BSON_TYPE_DATE_TIME:
                                  value->SetValue(static_cast<long long>(bson_iter_date_time(&Desc) / 1000));
                                  break;


cmake .. \
-DLIBFMT_INCLUDE_DIR=/usr/local/include \
-DCMAKE_INSTALL_PREFIX=/usr/local \
-DMYSQL_DATADIR=/var/lib/mysql \
-DSYSCONFDIR=/usr/local/etc \
-DWITHOUT_TOKUDB=1 \
-DMYSQL_UNIX_ADDR=/var/lib/mysql/mysql.sock \
-DDEFAULT_CHARSET=utf8 \
-DDEFAULT_COLLATION=utf8_general_ci \
-DBoost_INCLUDE_DIR=/usr/local/include \
-DCURSES_CURSES_LIBRARY=/usr/local/lib/libncurses.so \
-DCURSES_INCLUDE_PATH=/usr/local/include \
-DCURL_INCLUDE_DIR=/usr/local/include \
-DCURL_LIBRARY=/usr/local/lib/libcurl.so \
-DZSTD_INCLUDE_DIRS=/usr/local/include \
-DZSTD_LIBRARIES=/usr/local/lib64/libzstd.so \
-DGNUTLS_INCLUDE_DIR=/usr/local/include \
-DGNUTLS_LIBRARY=/usr/local/lib/libgnutls.so \
-DBZIP2_INCLUDE_DIR=/usr/local/include \
-DBZIP2_LIBRARIES=/usr/local/lib/libbz2.so.1.0 \
-DNETTLE_LIBRARY=/usr/local/lib64 \
-DNETTLE_INCLUDE_DIR=/usr/local/include \
-DHOGWEED_LIBRARY=/usr/local/lib64/ \
-DBoost_DIR=/usr/local \
-DEVENT_LIBRARY=/usr/local/lib/libevent.so \
-DJAVA_AWT_INCLUDE_PATH=/usr/local/lib/jvm/jdk1.8.0_202/include \
-DJAVA_AWT_LIBRARY=/usr/local/lib/jvm/jdk1.8.0_202/jre/lib/amd64/libawt.so \
-DJAVA_INCLUDE_PATH=/usr/local/lib/jvm/jdk1.8.0_202/include \
-DJAVA_JVM_LIBRARY=/usr/local/lib/jvm/jdk1.8.0_202/jre/lib/amd64/server/libjvm.so \
-DJava_JAR_EXECUTABLE=/usr/local/lib/jvm/jdk1.8.0_202/bin/jar \
-DJava_IDLJ_EXECUTABLE=/usr/local/lib/jvm/jdk1.8.0_202/bin/idlj \
-DJava_JARSIGNER_EXECUTABLE=/usr/local/lib/jvm/jdk1.8.0_202/bin/jarsigner \
-DJava_JAVAC_EXECUTABLE=/usr/local/lib/jvm/jdk1.8.0_202/bin/javac \
-DJava_JAVADOC_EXECUTABLE=/usr/local/lib/jvm/jdk1.8.0_202/bin/javadoc \
-DJava_JAVAH_EXECUTABLE=/usr/local/lib/jvm/jdk1.8.0_202/bin/javah \
-DJava_JAVA_EXECUTABLE=/usr/local/lib/jvm/jdk1.8.0_202/bin/java  \
-DOPENSSL_INCLUDE_DIR=/usr/local/include \
-DOPENSSL_CRYPTO_LIBRARY=/usr/local/lib64/libcrypto.so \
-DOPENSSL_SSL_LIBRARY=/usr/local/lib64/libssl.so \
-DPAM_LIBRARY=/usr/local/lib/libpam.so \
-DZLIB_INCLUDE_DIR=/usr/local/include \
-DZLIB_LIBRARY_RELEASE=/usr/local/lib/libz.so \
-Dlibmongoc-1.0_DIR=/usr/local/lib64 \
-DLIBXML2_INCLUDE_DIR=/usr/local/include/libxml2 \
-DLIBXML2_LIBRARY=/usr/local/lib/libxml2.so \
-DJudy_INCLUDE_DIRS=/usr/local/include \
-DKRB5_CONFIG=/usr/local/bin/krb5-config \
-DJudy_LIBRARIES=/usr/local/lib/libJudy.so \
-DLZ4_INCLUDE_DIRS=/usr/local/include \
-DLZ4_LIBRARIES=/usr/local/lib64/liblz4.so \
-DLIBLZMA_INCLUDE_DIR=/usr/local/include \
-DLIBLZMA_LIBRARY_RELEASE=/usr/local/lib/liblzma.so \
-DLZO_INCLUDE_DIRS=/usr/local/include \
-DLZO_LIBRARIES=/usr/local/lib/liblzo2.so \
-DSNAPPY_INCLUDE_DIRS=/usr/local/include \
-DSNAPPY_LIBRARIES=/usr/local/lib64/libsnappy.so \
-DODBC_INCLUDES=/usr/local/include \
-DODBC_LIBRARY=/usr/local/lib/libodbc.so \
-DPCRE_libpcre2-8_INCLUDEDIR=/usr/local/include \
-DPCRE_libpcre2-8_LIBDIR=/usr/local/lib \
-DREADLINE_INCLUDE_DIR=/usr/local/include \
-DREADLINE_LIBRARY=/usr/local/lib/libreadline.so

\cp /opt/fmt-11.0.2.zip /usr/local/src/mariadb-10.11.11/cmake-build/extra/libfmt/src/fmt-11.0.2.zip
# 删掉 /usr/local/mariadb-10.11.11/plugin/auth_pam/mapper/pam_user_map.c 56行的 static
gmake -j4 && gmake install

/bak/src/mariadb-10.11.11/cmake-build/scripts D:\00_development\pycharm\kylin_v10_zabbix_7.0.x_mysql\usr\local\share\mariadb-10.11.11
```

### 配置 mariadb 系统服务 ^mariadb-service
<span id="mariadb-service"></span>

1. 创建mysql用户组和用户：
```
groupadd -r mysql
useradd -g mysql -r -s /sbin/nologin mysql -d /usr/lib/mysql
# 归其为mysql用户
mkdir -p /var/lib/mysql
chown mysql:mysql /var/lib/mysql
chmod 755 /var/lib/mysql
```

2. 更改 libexec 权限
```
chmod +x /usr/libexec/mysql*
mkdir -p /var/log/mariadb
chmod +x /usr/local/bin/mysql_install_db
chmod +x /usr/local/bin/mariadb-install-db
systemctl daemon-reload
```
-------------------------------------------------------------------------------------------------------

## <center>pgsql-server编译安装</center>

### 编译安装 libxslt ^libxslt
<span id="libxslt"></span>

```
https://codeload.github.com/GNOME/libxslt/tar.gz/refs/tags/v1.1.32
tar -zxvf /opt/libxslt-1.1.32.tar.gz -C /usr/local/src
cd /usr/local/src/libxslt-1.1.32
mkdir m4
export ACLOCAL_PATH="/usr/local/share/aclocal"
autoreconf -vifs
mkdir build
cd build
../configure --prefix=/usr/local --enable-shared
make -j4
make -j4 install

```

### 编译安装pgsql ^pgsql
<span id="pgsql"></span>

\[[[#^perl\|依赖 perl]]\] | \[[[#^python37\|依赖 python37]]\] | \[[[#^readline\|依赖 readline]]\]
[依赖 perl](#perl) | [依赖 python37](#python37) | [依赖 readline](#readline) 

```
https://ftp.postgresql.org/pub/source/v16.2/postgresql-16.2.tar.gz
tar -zxvf /opt/postgresql-16.2.tar.gz -C /usr/local/src
cd /usr/local/src/postgresql-16.2
mkdir build
cd build

../configure \
--prefix=/usr/local/ \
--with-pgport=5432 \
--with-segsize=16 \
--with-blocksize=32 \
--with-wal-blocksize=64 \
--with-libedit-preferred \
--with-perl \
--with-openssl \
--with-libxml \
--with-python \
--with-libxslt \
--enable-thread-safety \
--enable-nls=en_US.UTF-8 \
--without-icu \
--with-libraries=/usr/local/lib/ \
--with-includes=/usr/local/include/ \
--libdir=/usr/local/lib \
--with-zstd \
--with-lz4 \
--with-libxml \
--with-ldap \
--with-pam \
--with-gssapi \
--with-perl
make -j4 && make install
```

### 编译安装timescale ^timescale
<span id="timescale"></span>

```
https://codeload.github.com/timescale/timescaledb/tar.gz/refs/tags/2.13.1
tar -zxvf /opt/timescaledb-2.13.1.tar.gz -C /usr/local/src
cd /usr/local/src/timescaledb-2.13.1
mkdir build
cd build
echo y | ../bootstrap
cd ./build && make -j4
make -j4 install
```

### 配置与启动 pgsql ^conf-pgsql
<span id="conf-pgsql"></span>

1. 创建mysql用户组和用户：
```
groupadd -r postgres
useradd -g postgres -r -s /bin/bash postgres -d /var/lib/pgsql
echo 123.com | passwd --stdin postgres
# 归其为mysql用户
mkdir -p /var/lib/pgsql
chown postgres:postgres /var/lib/pgsql
chmod 755 /var/lib/pgsql
chmod +x /usr/libexec/postgresql-check-db-dir
chmod +x /usr/local/bin/postgresql-setup
chmod +x  /usr/local/share/postgresql-setup/library.sh
/usr/local/bin/postgresql-16-setup initdb
timescaledb-tune --pg-config=/usr/local/bin/pg_config -yes
timescaledb-tune --pg-config=/usr/local/bin/pg_config -conf-path=/var/lib/pgsql/data/postgresql.conf -yes

systemctl start postgresql
systemctl status postgresql

[root@localhost ~]# cat /var/lib/pgsql/.bashrc 
export LD_LIBRARY_PATH="/usr/local/src/perl5-5.26.3:/usr/local/lib:/usr/local/lib64"
declare -x JAVA_HOME=/usr/local/lib/jvm/jdk1.8.0_202
declare -x JRE_HOME=${JAVA_HOME}/jre  
declare -x CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
declare -x JAVA_PATH=${JAVA_HOME}/bin:${JRE_HOME}/bin
export PATH="${JAVA_PATH}:/usr/local/opt/venv_37_centos7/bin:/usr/local/opt/go/bin:/usr/local/opt/glibc/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin"
[root@localhost ~]# 
sudo -u postgres bash -c '. /var/lib/pgsql/.bashrc; /usr/local/bin/psql -c "grant all on database \"zabbix\" to zabbix;"'
```
-------------------------------------------------------------------------------------------------------

## <center>centos7 构建zabbix7.0 rpm 安装包</center>

### 编译安装net-snmp ^net-snmp
<span id="net-snmp"></span>

\[[[#^perl\|依赖 perl]]\]
[依赖 perl](#perl) 

```
https://codeload.github.com/net-snmp/net-snmp/tar.gz/refs/tags/v5.8
tar -zxvf /opt/net-snmp-5.8.tar.gz -C /usr/local/src
cd /usr/local/src/net-snmp-5.8
mkdir build
./configure --prefix=/usr/local --enable-embedded-perl --enable-shared --with-perl-modules --with-openssl=/usr/local
# 一路回车
make -j4
make -j4 install
```

### 编译安装 popt ^popt
<span id="popt"></span>

1. 下载安装包
```
https://ftp.osuosl.org/pub/rpm/popt/releases/popt-1.x/popt-1.18.tar.gz
tar -zxvf /opt/popt-1.18.tar.gz -C /usr/local/src
cd /usr/local/src/popt-1.18
mkdir build
cd build/
../configure --prefix=/usr/local --enable-shared
make -j4
make -j4 install

```

### 编译安装OpenIPMI ^OpenIPMI
<span id="OpenIPMI"></span>

\[[[#^popt\|依赖 popt]]\] | \[[[#^net-snmp\|依赖 net-snmp]]\] | \[[[#^openssl\|依赖 openssl]]\] | \[[[#^readline\|依赖 readline]]\]
[依赖 popt](#popt) | [依赖 net-snmp](#net-snmp) | [依赖 openssl](#openssl) | [依赖 readline](#readline) 

```
https://jaist.dl.sourceforge.net/project/openipmi/OpenIPMI%202.0%20Library/OpenIPMI-2.0.31.tar.gz?viasf=1
tar -zxvf /opt/OpenIPMI-2.0.36.tar.gz -C /usr/local/src
cd /usr/local/src/OpenIPMI-2.0.36
mkdir build
cd build/
../configure --prefix=/usr/local --enable-shared --with-openssl=/usr/local --with-snmplibs="-L/usr/local -lnetsnmp"
make -j4
make -j4 install

```

### 安装fping ^fping
<span id="fping"></span>

```
https://github.com/schweikert/fping/releases/tag/v5.2
tar -zxvf /opt/fping-5.2.tar.gz -C /usr/local/src
cd /usr/local/src/fping-5.2
mkdir build
cd build/
../configure --prefix=/usr/local
make -j4
make -j4 install
```

### 安装go ^go
<span id="go"></span>

```
https://golang.google.cn/dl/
# cat /opt/go1.22.4.linux-amd64.tar.gz_0* > /opt/go1.22.4.linux-amd64.tar.gz
tar -zxvf /opt/go1.22.4.linux-amd64.tar.gz -C /usr/local/opt
go env -w GO111MODULE=on && \
go env -w GOPROXY=https://goproxy.cn,direct && \
go env -w GOBIN=/usr/local/opt/go/bin
```

### 编译 libmagic ^libmagic
<span id="libmagic"></span>

```
https://codeload.github.com/file/file/tar.gz/refs/tags/FILE5_33
tar -zxvf /opt/file-FILE5_33.tar.gz -C /usr/local/src
cd /usr/local/src/file-FILE5_33
autoreconf -vifs
mkdir build
cd build
../configure --prefix=/usr/local --enable-shared
make -j4 
make -j4 install
```

### 编译 libarchive ^libarchive
<span id="libarchive"></span>

```
https://github.com/libarchive/libarchive/releases?page=2
tar -zxvf /opt/libarchive-3.3.3.tar.gz -C /usr/local/src
cd /usr/local/src/libarchive-3.3.3
mkdir build
cd build
../configure --prefix=/usr/local --enable-shared
make -j4 
make -j4 install
```

### <font color=#ff0000> 编译 lua ^lua</font>
<span id="lua"></span>

`这个无需安装`

```
https://www.lua.org/ftp/lua-5.3.4.tar.gz
tar -zxvf /opt/lua-5.3.4.tar.gz -C /usr/local/src
cd /usr/local/src/lua-5.3.4
sed -i -e "/^\TO_LIB/s/=.*/= liblua.a liblua.so/" /usr/local/src/lua-5.3.4/Makefile
sed -i -e "/^\CFLAGS/s/=.*/= -O2 -Wall -Wextra -DLUA_COMPAT_5_2 \$(SYSCFLAGS) \$(MYCFLAGS) -fPIC/"  /usr/local/src/lua-5.3.4/src/Makefile
sed -i -e "/^LUA_SO/d" /usr/local/src/lua-5.3.4/src/Makefile
sed -i -e "/^LUA_A/a\LUA_SO= liblua.so" /usr/local/src/lua-5.3.4/src/Makefile
sed -i -e "/^\ALL_T/s/=.*/= \$(LUA_A) \$(LUA_T) \$(LUAC_T) \$(LUA_SO)/"  /usr/local/src/lua-5.3.4/src/Makefile
sed -i -e "/^\$(LUA_T)/i\$(LUA_SO): \$(CORE_O) \$(LIB_O)\n\t\$(CC) -o \$@ -shared \$? -ldl -lm" /usr/local/src/lua-5.3.4/src/Makefile
make -j4 linux
make -j4 linux install

cat > /usr/local/lib/pkgconfig/lua.pc << EOF
prefix=/usr/local
exec_prefix=\${prefix}
libdir=\${exec_prefix}/lib
sharedlibdir=\${libdir}
includedir=\${prefix}/include

Name: lua
Description: lua
Version: 5.3.4

Requires:
Libs: -L\${libdir} -L\${sharedlibdir} -lz
Cflags: -I\${includedir}
EOF

chmod +x /usr/local/lib/liblua.so
```

### 编译 libelf ^libelf
<span id="libelf"></span>

```
https://sourceware.org/elfutils/ftp/0.190/elfutils-0.190.tar.bz2
tar -jxvf /opt/elfutils-0.190.tar.bz2 -C /usr/local/src
cd /usr/local/src/elfutils-0.190
mkdir build
cd build
../configure --prefix=/usr/local --disable-debuginfod --enable-install-elfh --enable-libdebuginfod=dummy
make -j4 
make -j4 -C libelf install
install -vm644 config/libelf.pc /usr/local/lib/pkgconfig/libelf.pc
```

### 编译 rpm ^rpm
<span id="rpm"></span>

\[[[#^openssl\|依赖 openssl]]\] | \[[[#^libmagic\|依赖 libmagic]]\] | \[[[#^libarchive\|依赖 libarchive]]\] | \[[[#^libelf\|依赖 libelf]]\]
[依赖 openssl](#openssl) | [依赖 libmagic](#libmagic) | [依赖 libarchive](#libarchive) | [依赖 libelf](#libelf)

```
https://ftp.osuosl.org/pub/rpm/releases/rpm-4.14.x/rpm-4.14.3.tar.bz2
tar -jxvf /opt/rpm-4.14.3.tar.bz2 -C /usr/local/src
cd /usr/local/src/rpm-4.14.3
sh autogen.sh --prefix=/usr/local --enable-shared --with-crypto=openssl --without-lua
make -j4 
make -j4 install
```

### 生成rpm ^make-rpm
<span id="make-rpm"></span>

\[[[#^net-snmp\|依赖 net-snmp]]\] | \[[[#^OpenIPMI\|依赖 OpenIPMI]]\]  | \[[[#^fping\|依赖 fping]]\]  | \[[[#^go\|依赖 go]]\]  | \[[[#^rpm\|依赖 rpm]]\] 
[依赖 net-snmp](#net-snmp) | [依赖 OpenIPMI](#OpenIPMI) | [依赖 fping](#fping) | [依赖 go](#go) | [依赖 rpm](#rpm)

```
https://cdn.zabbix.com/zabbix/sources/stable/7.0/zabbix-7.0.6.tar.gz

# 因非yum或rpm安装，所以需要注释掉校验
     97 # BuildRequires:        make
    114 # %if 0%{?rhel} >= 7 || %{amzn} >= 2023
    115 # BuildRequires:        pcre2-devel
    116 # %else
    117 # BuildRequires:        pcre-devel
    118 # %endif
    119 # %if 0%{?rhel} >= 6 || %{amzn} >= 2023
    120 # BuildRequires:        openssl-devel >= 1.0.1
    121 # %endif
    122 # %if 0%{?rhel} >= 7 || %{amzn} >= 2023
    123 # BuildRequires:        systemd
    124 # %endif
    125 # %if 0%{?build_selinux_policy}
    126 # BuildRequires: policycoreutils-devel
    127 # %if 0%{rhel} >= 9 || %{amzn} >= 2023
    128 # BuildRequires: selinux-policy-devel
    129 # %endif
    130 # %endif
	997 # %{_datadir}/zabbix-sql-scripts/sqlite3/proxy.sql

        --with-ssh2=/usr/local
        --with-postgresql=/usr/local/bin/pg_config
        --with-mysql=/usr/local/bin/mysql_config
        --with-net-snmp=/usr/local/bin/net-snmp-config
        --with-openipmi=/usr/local
        --with-ldap=/usr/local
        --with-libevent=/usr/local
        --with-libevent-include=/usr/local/include
        --with-libevent-lib=/usr/local/lib
        --with-openssl=/usr/local

https://repo.zabbix.com/zabbix/7.0/rhel/7/SRPMS/
 rpm -ivhU --force --nodeps /opt/zabbix-7.0.7-release1.el7.src.rpm

--define "dist .ky10" \

cd /root/rpmbuild/SPECS/ &&
rpmbuild \
--define "dist .el7" \
--define "rhel 7" \
--define "_bindir /usr/bin" \
--define "_datadir /usr/share" \
--define "_docdir /usr/share/doc" \
--define "_localstatedir /var" \
--define "_mandir /usr/share/man" \
--define "_sbindir /usr/sbin" \
--define "_sysconfdir /etc" \
--define "zabbix_script_dir /usr/bin" \
--define "_tmpfilesdir /usr/lib/tmpfiles.d" \
--define "_unitdir /usr/lib/systemd/system" \
--define "zabbix_script_dir /usr/bin" \
--define "build_selinux_policy 1" \
--define "build_agent 1" \
--define "build_agent2 1" \
--define "build_web_service 1" \
--define "build_server 1" \
--define "build_proxy 1" \
--define "build_frontend 1" \
--define "build_java_gateway 1" \
--define "build_with_mysql 1" \
--define "build_with_pgsql 1" \
--define "build_with_sqlite 0" \
-bb zabbix.spec
```


-------------------------------------------------------------------------------------------------------

## <center>centos7 编译安装 zabbix 7.0</center>

### 编译安装nginx ^nginx
<span id="nginx"></span>

1. 创建 nginx 用户组和用户：
```
groupadd -r nginx
useradd -g nginx -r -s /sbin/nologin nginx -d /usr/share/zabbix
```
2. 编译安装nginx
```
https://nginx.org/download/nginx-1.24.0.tar.gz
tar -zxvf /opt/nginx-1.24.0.tar.gz -C /usr/local/src
cd /usr/local/src/nginx-1.24.0
./configure --prefix=/usr/local --user=nginx --group=nginx --error-log-path=/var/log/nginx/nginx.log --http-log-path=/var/log/nginx/access.log --conf-path=/etc/nginx/nginx.conf --pid-path=/var/run/nginx.pid --with-http_stub_status_module --with-http_ssl_module --with-http_gzip_static_module
make -j4 
make -j4 install
systemctl daemon-reload
systemctl start nginx
systemctl status nginx
```

### 编译 libpng ^libpng
<span id="libpng"></span>

```
https://jaist.dl.sourceforge.net/project/libpng/libpng16/1.6.44/libpng-1.6.44.tar.gz?viasf=1
tar -zxvf /opt/libpng-1.6.44.tar.gz -C /usr/local/src
cd /usr/local/src/libpng-1.6.44
mkdir build
cd build
../configure --prefix=/usr/local
make -j4 
make -j4 install
```

### 编译 libjpeg ^libjpeg
<span id="libjpeg"></span>

```
http://www.ijg.org/files/jpegsrc.v9f.tar.gz
tar -zxvf /opt/jpegsrc.v9f.tar.gz -C /usr/local/src
cd /usr/local/src/jpeg-9f
mkdir build
cd build
../configure --prefix=/usr/local
make -j4 
make -j4 install
```

### 编译 freetype ^freetype
<span id="freetype"></span>

```
https://download.savannah.gnu.org/releases/freetype/freetype-2.9.tar.bz2
tar -zxvf /opt/freetype-2.9.1.tar.gz -C /usr/local/src
cd /usr/local/src/freetype-2.9.1
mkdir build
cd build
../configure --prefix=/usr/local
make -j4 
make -j4 install
```

### 编译 oniguruma ^oniguruma
<span id="oniguruma"></span>

```
https://github.com/kkos/oniguruma/releases
tar -zxvf /opt/onig-6.9.10.tar.gz -C /usr/local/src
cd /usr/local/src/onig-6.9.10
mkdir build
cd build
../configure --prefix=/usr/local
make -j4 
make -j4 install
```

### 编译安装 php ^php
<span id="php"></span>

\[[[#^libpng\|依赖 libpng]]\] | \[[[#^libjpeg\|依赖 libjpeg]]\] | \[[[#^freetype\|依赖 freetype]]\] | \[[[#^oniguruma\|依赖 oniguruma]]\] 
[依赖 libpng](#libpng) | [依赖 libjpeg](#libjpeg) | [依赖 freetype](#freetype) | [依赖 oniguruma](#oniguruma)

1. 创建 nginx 用户组和用户：
```
groupadd -r nginx
useradd -g nginx -r -s /sbin/nologin nginx -d /usr/share/zabbix
```
2. 编译安装php
```
https://www.php.net/distributions/php-8.3.3.tar.gz
tar -zxvf /opt/php-8.3.3.tar.gz -C /usr/local/src
cd /usr/local/src/php-8.3.3
cd build
../configure --prefix=/usr/local --with-config-file-path=/etc --with-pdo-mysql=/usr/local --with-mysql-sock=/var/lib/mysql/mysql.sock --with-pgsql=/usr/local/bin --with-pdo-pgsql=/usr/local --enable-gd --enable-bcmath --with-jpeg --with-freetype --enable-ctype --enable-xml --enable-session --enable-sockets --enable-mbstring=shared --with-gettext --with-ldap --with-openssl --without-pdo-sqlite --without-sqlite3 --enable-fpm --with-iconv=/usr/local/bin -with-fpm-acl --with-fpm-user=nginx --with-fpm-group=nginx --with-curl --with-mysqli
make -j4 
make -j4 install
mkdir -p /var/log/loki
chmod 777 -R /var/log/loki
chown nginx:nginx /var/log/loki/zabbix_php-fpm_slow.log
touch /usr/local/var/log/php-fpm.log
chown nginx:nginx /usr/local/var/log/php-fpm.log
/usr/local/bin/php -r 'phpinfo();' | grep 'php.ini'
\cp /usr/local/src/php-8.3.3/php.ini-production /etc/php.ini
	# 修改/etc/php.ini配置文件
    920 extension=/usr/local/lib/php/extensions/no-debug-non-zts-20230831/mbstring.so
systemctl daemon-reload
systemctl start php-fpm
systemctl status php-fpm
```
-------------------------------------------------------------------------------------------------------

## 安装 zabbix 7.0 - mysql 版 ^zabbix-70-mysql
<span id="zabbix-70-mysql"></span>

```
libtool --finish /usr/local/lib
libtool --finish /usr/local/lib64
libtool --finish /usr/local/opt/glibc/lib
declare -x ACLOCAL_PATH="/usr/local/share/aclocal/"
declare -x LD_LIBRARY_PATH="/usr/local/src/perl5-5.26.3:/usr/local/lib:/usr/local/lib64"
declare -x JAVA_HOME=/usr/local/lib/jvm/jdk1.8.0_202
declare -x JRE_HOME=${JAVA_HOME}/jre  
declare -x CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
declare -x JAVA_PATH=${JAVA_HOME}/bin:${JRE_HOME}/bin
declare -x PATH="${JAVA_PATH}:/usr/local/opt/venv_37_centos7/bin:/usr/local/opt/go/bin:/usr/local/opt/glibc/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin"
declare -x PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:/usr/local/lib64/pkgconfig"
# 如果想启用yum打开下面的LD_PRELOAD变量，关闭使用unset LD_PRELOAD
# export LD_PRELOAD="/usr/lib64/liblzma.so.5:/usr/local/lib64/libcrypto.so.1.1:/usr/local/lib64/libssl.so.1.1"

rpm -ivhU --force --nodeps zabbix-agent2-7.0.7-release1.x86_64.rpm zabbix-get-7.0.7-release1.x86_64.rpm zabbix-java-gateway-7.0.7-release1.x86_64.rpm zabbix-js-7.0.7-release1.x86_64.rpm zabbix-sender-7.0.7-release1.x86_64.rpm zabbix-server-mysql-7.0.7-release1.x86_64.rpm zabbix-web-service-7.0.7-release1.x86_64.rpm

rpm -ivhU --force --nodeps zabbix-nginx-conf-7.0.7-release1.noarch.rpm zabbix-sql-scripts-7.0.7-release1.noarch.rpm zabbix-web-7.0.7-release1.noarch.rpm zabbix-web-deps-7.0.7-release1.noarch.rpm zabbix-web-mysql-7.0.7-release1.noarch.rpm 
```

### <center>注意</center>

### 注意 ^zhuyi
<span id="zhuyi"></span>

1. gcc重新编译要执行，如果更改了系统环境变量也需要执行
```
# make clean
# make distclean
find ./ -name config.cache | xargs rm -f
```
2. 查看二进制文件 build ID 命令，编译 gcc 时需要添加 "--enable-linker-build-id"
```
eu-readelf -n /root/rpmbuild/BUILDROOT/zabbix-7.0.4-release1.el7.x86_64/usr/sbin/zabbix_agent2
eu-readelf -n /root/rpmbuild/BUILDROOT/zabbix-7.0.7-release1.el7.x86_64/usr/sbin/zabbix_web_service
```
3. LD_LIBRARY_PATH、LIBRARY_PATH用于告知ld命令查找库位置
`多个位置用 : 隔开`
```
declare -x LIBRARY_PATH="/usr/local/openssl-1.1.1w/openssl/lib:/usr/local/libssh2-1.11.1/libssh2/lib64:/usr/local/mpc-0.9/mpc/lib:/usr/local/gcc-8.5.0/gcc/lib64/:/usr/local/Linux-PAM-1.3.1/pam/lib:/usr/local/OpenIPMI-2.0.36/OpenIPMI/lib:/usr/local/openldap-2.4.46/openldap/lib:/usr/local/libevent-2.1.8-stable/libevent/lib/"

declare -x LD_LIBRARY_PATH="/usr/local/openssl-1.1.1w/openssl/lib:/usr/local/libssh2-1.11.1/libssh2/lib64:/usr/local/mpc-0.9/mpc/lib:/usr/local/gcc-8.5.0/gcc/lib64/:/usr/local/Linux-PAM-1.3.1/pam/lib:/usr/local/OpenIPMI-2.0.36/OpenIPMI/lib:/usr/local/openldap-2.4.46/openldap/lib:/usr/local/libevent-2.1.8-stable/libevent/lib/"
```
4. 编译安装的make阶段报错Failed to build these modules:\_ctypes
`尝试设置您的 PKG_CONFIG_PATH 变量以包含 libffi.pc 的安装路径，即declare -x PKG_CONFIG_PATH="/usr/local/libffi-3.4.4/libffi/lib/pkgconfig"`
```
/usr/bin/install -c python-config.py /users/mskoenz/.pyenv/versions/3.7.0/lib/python3.7/config-3.7m-x86_64-linux-gnu/python-config.py
/usr/bin/install -c python-config /users/mskoenz/.pyenv/versions/3.7.0/bin/python3.7m-config
./python -E ./setup.py install \
   	--prefix=/users/mskoenz/.pyenv/versions/3.7.0 \
	--install-scripts=/users/mskoenz/.pyenv/versions/3.7.0/bin \
	--install-platlib=/users/mskoenz/.pyenv/versions/3.7.0/lib/python3.7/lib-dynload \
	--root=/
running install
running build
running build_ext
INFO: Could not locate ffi libs and/or headers

The following modules found by detect_modules() in setup.py, have been
built by the Makefile instead, as configured by the Setup files:
_abc                  atexit                pwd
time


Failed to build these modules:
_ctypes
```
5. cmake  OPENSSL_ROOT_DIR (missing: OPENSSL_CRYPTO_LIBRARY OPENSSL_INCLUDE_DIR)
```
# OPENSSL_ROOT_DIR (missing: OPENSSL_CRYPTO_LIBRARY OPENSSL_INCLUDE_DIR)
set(OPENSSL_ROOT_DIR "/usr/local/openssl-1.1.1w/openssl")
```

6. cmake 编译安装可以通过grep查看确实的文件
```
[root@localhost build]# grep "NOTFOUND" CMakeCache.txt 
Boost_DIR:PATH=Boost_DIR-NOTFOUND
CHECKMODULE:FILEPATH=CHECKMODULE-NOTFOUND
CMAKE_DLLTOOL:FILEPATH=CMAKE_DLLTOOL-NOTFOUND
CURSES_CURSES_LIBRARY:FILEPATH=CURSES_CURSES_LIBRARY-NOTFOUND
CURSES_FORM_LIBRARY:FILEPATH=CURSES_FORM_LIBRARY-NOTFOUND
CURSES_NCURSES_LIBRARY:FILEPATH=CURSES_NCURSES_LIBRARY-NOTFOUND
DTRACE:FILEPATH=DTRACE-NOTFOUND
EVENT_LIBRARY:FILEPATH=EVENT_LIBRARY-NOTFOUND
GRN_MECAB_CONFIG_ABSOLUTE_PATH:FILEPATH=GRN_MECAB_CONFIG_ABSOLUTE_PATH-NOTFOUND
JAVA_AWT_INCLUDE_PATH:PATH=JAVA_AWT_INCLUDE_PATH-NOTFOUND
JAVA_AWT_LIBRARY:FILEPATH=JAVA_AWT_LIBRARY-NOTFOUND
JAVA_INCLUDE_PATH:PATH=JAVA_INCLUDE_PATH-NOTFOUND
JAVA_INCLUDE_PATH2:PATH=JAVA_INCLUDE_PATH2-NOTFOUND
JAVA_JVM_LIBRARY:FILEPATH=JAVA_JVM_LIBRARY-NOTFOUND
Java_IDLJ_EXECUTABLE:FILEPATH=Java_IDLJ_EXECUTABLE-NOTFOUND
Java_JARSIGNER_EXECUTABLE:FILEPATH=Java_JARSIGNER_EXECUTABLE-NOTFOUND
Java_JAR_EXECUTABLE:FILEPATH=Java_JAR_EXECUTABLE-NOTFOUND
Java_JAVAC_EXECUTABLE:FILEPATH=Java_JAVAC_EXECUTABLE-NOTFOUND
Java_JAVADOC_EXECUTABLE:FILEPATH=Java_JAVADOC_EXECUTABLE-NOTFOUND
Java_JAVAH_EXECUTABLE:FILEPATH=Java_JAVAH_EXECUTABLE-NOTFOUND
Java_JAVA_EXECUTABLE:FILEPATH=Java_JAVA_EXECUTABLE-NOTFOUND
Judy_INCLUDE_DIRS:PATH=Judy_INCLUDE_DIRS-NOTFOUND
Judy_LIBRARIES:FILEPATH=Judy_LIBRARIES-NOTFOUND
KRB5_CONFIG:FILEPATH=KRB5_CONFIG-NOTFOUND
LIBAIO_INCLUDE_DIRS:PATH=LIBAIO_INCLUDE_DIRS-NOTFOUND
LIBAIO_LIBRARIES:FILEPATH=LIBAIO_LIBRARIES-NOTFOUND
LIBEDIT_INCLUDE_DIR:PATH=LIBEDIT_INCLUDE_DIR-NOTFOUND
LIBEDIT_LIBRARY:FILEPATH=LIBEDIT_LIBRARY-NOTFOUND
LIBLZMA_INCLUDE_DIR:PATH=LIBLZMA_INCLUDE_DIR-NOTFOUND
LIBLZMA_LIBRARY_DEBUG:FILEPATH=LIBLZMA_LIBRARY_DEBUG-NOTFOUND
LIBLZMA_LIBRARY_RELEASE:FILEPATH=LIBLZMA_LIBRARY_RELEASE-NOTFOUND
LIBXML2_INCLUDE_DIR:PATH=LIBXML2_INCLUDE_DIR-NOTFOUND
LIBXML2_LIBRARY:FILEPATH=LIBXML2_LIBRARY-NOTFOUND
LZ4_INCLUDE_DIRS:PATH=LZ4_INCLUDE_DIRS-NOTFOUND
LZ4_LIBRARIES:FILEPATH=LZ4_LIBRARIES-NOTFOUND
LZO_INCLUDE_DIRS:PATH=LZO_INCLUDE_DIRS-NOTFOUND
LZO_LIBRARIES:FILEPATH=LZO_LIBRARIES-NOTFOUND
ODBC_INCLUDES:FILEPATH=ODBC_INCLUDES-NOTFOUND
ODBC_LIBRARY:FILEPATH=ODBC_LIBRARY-NOTFOUND
OPENSSL_CRYPTO_LIBRARY:FILEPATH=OPENSSL_CRYPTO_LIBRARY-NOTFOUND
OPENSSL_SSL_LIBRARY:FILEPATH=OPENSSL_SSL_LIBRARY-NOTFOUND
PAM_LIBRARY:FILEPATH=PAM_LIBRARY-NOTFOUND
READLINE_INCLUDE_DIR:PATH=READLINE_INCLUDE_DIR-NOTFOUND
READLINE_LIBRARY:FILEPATH=READLINE_LIBRARY-NOTFOUND
SEMODULE_PACKAGE:FILEPATH=SEMODULE_PACKAGE-NOTFOUND
SNAPPY_INCLUDE_DIRS:PATH=SNAPPY_INCLUDE_DIRS-NOTFOUND
SNAPPY_LIBRARIES:FILEPATH=SNAPPY_LIBRARIES-NOTFOUND
URING_INCLUDE_DIRS:PATH=URING_INCLUDE_DIRS-NOTFOUND
URING_LIBRARIES:FILEPATH=URING_LIBRARIES-NOTFOUND
ZLIB_INCLUDE_DIR:PATH=ZLIB_INCLUDE_DIR-NOTFOUND
ZLIB_LIBRARY_DEBUG:FILEPATH=ZLIB_LIBRARY_DEBUG-NOTFOUND
ZLIB_LIBRARY_RELEASE:FILEPATH=ZLIB_LIBRARY_RELEASE-NOTFOUND
libmongoc-1.0_DIR:PATH=libmongoc-1.0_DIR-NOTFOUND
[root@localhost build]# 
```

7. 处理yum无法使用的问题
通过设置预加载环境变量
```
export LD_PRELOAD="/usr/local/lib64/libcrypto.so.1.1:/usr/local/lib64/libssl.so.1.1:/usr/lib64/liblzma.so.5"
```

8. 关于无法生成libperl.so的说明
```
# 需要添加参数
./Configure -des -Dprefix=/usr/local -Duseshrplib  -Dusethreads -Uversiononly
# 需要设置环境变量
declare -x LD_LIBRARY_PATH="/usr/local/src/perl5-5.26.3​:/usr/local/lib:/usr/local/lib64"
```

9. 关于ldd无法使用的说明
```
# 老版本的使用全路径
/bin/ldd xxx.so
# 新版本的直接ldd
ldd xxx.so

```

9. 关于readline报错
`checking for rl_initialize in -lreadline... no`
`configure: error: libreadline is required!`
```
# 干掉编译安装生成的备份
rm -rf /usr/local/lib/libreadline.*.old
```

10. 关于error: Couldn't exec /usr/local/lib/rpm/elfdeps: No such file or directory

\[[[#^libelf\|依赖 libelf]]\]
[依赖 libelf](#libelf) 

[需要编译安装 libelf](https://www.linuxfromscratch.org/lfs/view/12.1/chapter08/libelf.html
)

11. 关于mysql/mariadb启动程序
启动服务调用的mysql来自
/usr/local/src/mariadb-10.11.11/cmake-build/support-files/mysql.server
也就是说将mysql.server重命名为了mysqld放到了/usr/libexec路径下
```
\cp /usr/local/src/mariadb-10.11.11/cmake-build/support-files/mysql.server /usr/libexec/mysqld
```

11. 关于报错 php8.3 编译报错

PHP 8.3.0 build fails on centos 8 with the error:

```
/usr/bin/ld: dynamic STT_GNU_IFUNC symbol `mb_utf16be_to_wchar' with pointer equality in `ext/mbstring/libmbfl/filters/mbfilter_utf16.o' can not be used when making an executable; recompile with -fPIE and relink with -pie
collect2: error: ld returned 1 exit status
```

解决办法：

```
Workaround if you don't want to install gcc-toolset-* : configure with --enable-mbstring=shared  
this issue occured only if mbstring is not compiled as a shared extension (you also need to add extension=mbstring.so to your php.ini)
```
-------------------------------------------------------------------------------------------------------
12. 关于缺少 liblber-2.4.so.2
解决办法：
需要openldap [依赖 openldap](#openldap) \[[[#^openldap\|依赖 openldap]]\]

13. 麒麟v10 make报错 ^make-error
<span id="make-error"></span>
```
more undefined references to `__alloca' follow

解决方法： 

进入glob/glob.c文件，在第211和232注释掉。

输入指令 vi glob/glob.c

添加

#define __alloca         alloca

#define __stat             stat

```

13. 麒麟v10 m4报错
```
问题：
freadahead.c: In function 'freadahead':
freadahead.c:91:3: error: #error "Please port gnulib freadahead.c to your platform! Look at the definition of fflush, fread, ungetc on your system, then report this to bug-gnulib."
   91 |  #error "Please port gnulib freadahead.c to your platform! Look at the definition of fflush, fread, ungetc on your system, then report this to bug-gnulib."
      |   ^~~~~
make[7]: *** [Makefile:1837: freadahead.o] Error 1
make[7]: Leaving directory '/opt/p2/openwrt/build_dir/host/m4-1.4.17/lib'

解决：
cd /usr/local/src/m4-1.4.18/
sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h
```


14. 麒麟v10 bison报错
```
问题：
lib/fseterr.c: In function 'fseterr':
lib/fseterr.c:77:3: error: #error "Please port gnulib fseterr.c to your platform! Look at the definitions of ferror and clearerr on your system, then report this to bug-gnulib."
   77 |  #error "Please port gnulib fseterr.c to your platform! Look at the definitions of ferror and clearerr on your system, then report this to bug-gnulib."
      |   ^~~~~
make[6]: *** [Makefile:3461: lib/fseterr.o] Error 1
make[6]: Leaving directory '/opt/p2/openwrt/build_dir/host/bison-3.0.4'

解决：
cd /usr/local/src/bison-3.0.4
sed -i 's/IO_ftrylockfile/IO_EOF_SEEN/' lib/*.c
echo "#define _IO_IN_BACKUP 0x100" >> lib/stdio-impl.h
```
## <center>参考</center> ^cankao
<span id="cankao"></span>

### [Zabbix 7.0编译部署教程](https://forum.lwops.cn/article/547)

### [# 8.3.0 build fails](https://github.com/php/php-src/issues/12774)
-------------------------------------------------------------------------------------------------------
