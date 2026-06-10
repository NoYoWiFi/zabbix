declare -x LD_LIBRARY_PATH="/usr/local/src/perl5-5.26.3:/usr/local/lib:/usr/local/lib64"
declare -x JAVA_HOME=/usr/local/lib/jvm/jdk1.8.0_202
declare -x JRE_HOME=${JAVA_HOME}/jre  
declare -x CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
declare -x JAVA_PATH=${JAVA_HOME}/bin:${JRE_HOME}/bin
declare -x PATH="${JAVA_PATH}:/usr/local/opt/venv_37_centos7/bin:/usr/local/opt/go/bin:/usr/local/opt/glibc/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin"
