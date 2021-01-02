#!/bin/bash
yum -y install wget git which file python3 python3-devel libtool make autoconf automake \
    openssl-devel libevent-devel libdb-devel libdb-cxx-devel bzip2-devel libicu-devel

yum install -y epel-release
yum install -y gcc-c++ libtool make autoconf automake openssl-devel libevent-devel libdb-devel libdb-cxx-devel
yum install centos-release-scl -y
yum install devtoolset-8-gcc* -y
scl enable devtoolset-8 bash
source /opt/rh/devtoolset-8/enable
yum install -y python3-devel libicu-devel bzip2-devel wget patch lbzip2

# Make and install boost 1.7
mkdir boost
cd boost
wget --no-verbose https://dl.bintray.com/boostorg/release/1.70.0/source/boost_1_70_0.tar.gz
tar -xzf boost_1_70_0.tar.gz
rm boost_1_70_0.tar.gz
cd boost_1_70_0
./bootstrap.sh --with-python=/usr/bin/python3.6 --with-python-version=3.6 --with-python-root=/usr/lib/python3.6
./b2 include="/usr/include/python3.6m" install --prefix=/opt/boost_1_70
echo "/opt/boost_1_70/lib" > /etc/ld.so.conf.d/boost_1_70.conf
ldconfig
cd ../../
