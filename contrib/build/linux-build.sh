#!/bin/bash

# $1 - path to checkout and build Bitcoin SV in.

# ---

# try various methods, in order of preference, to detect distro
# store result in variable '$distro'
if type lsb_release >/dev/null 2>&1 ; then
   d_name=$(lsb_release -i -s)
   d_version=$(lsb_release -r -s)
elif [ -e /etc/os-release ] ; then
   d_name=$(awk -F= '$1 == "ID" {gsub(/"/, "", $2); print  $2}' /etc/os-release)
   d_version=$(awk -F= '$1 == "VERSION_ID" {gsub(/"/, "", $2); print  $2}' /etc/os-release)
else
   echo "unknown distribution: no method of identification"
   exit 1
fi

# convert to lowercase
d_name=$(printf '%s\n' "$d_name" | LC_ALL=C tr '[:upper:]' '[:lower:]')

# now do different things depending on distro
case "$d_name" in
   centos*)  echo "valid distribution: '$d_name'" ;;
#    debian*)  commands-for-debian ;;
#    ubuntu*)  echo "valid distribution: '$d_name'" ;;
#    mint*)    commands-for-mint ;;
   *)        echo "unsupported distribution: '$d_name'" ; exit 1 ;;
esac

if [[ ! $d_version =~ ^7.*$ ]]; then
    echo "unsupported distribution version: '$d_version'"
    exit 1
fi

echo "supported distribution version: '$d_version'"

# ---

yum install -y epel-release
yum install -y gcc-c++ libtool make autoconf automake openssl-devel libevent-devel libdb-devel libdb-cxx-devel
yum install centos-release-scl -y
yum install devtoolset-8-gcc* -y
source /opt/rh/devtoolset-8/enable

# boost-devel for centos 7 is 1.5 something and is lower than the minimum, need to compile..
# python-devel is 3.6, boost will find 3.7 without devel support, so tell boost below.
yum install -y python3-devel libicu-devel bzip2-devel wget

mkdir boost
cd boost
wget --no-verbose https://dl.bintray.com/boostorg/release/1.70.0/source/boost_1_70_0.tar.gz
tar -xzf boost_1_70_0.tar.gz
cd boost_1_70_0
./bootstrap.sh --with-python=/usr/bin/python3.6 --with-python-version=3.6 --with-python-root=/usr/lib/python3.6
./b2 include="/usr/include/python3.6m" install --prefix=/opt/boost_1_70
echo "/opt/boost_1_70/lib" > /etc/ld.so.conf.d/boost_1_70.conf
ldconfig
cd ../../

mkdir libevent
cd libevent
wget --no-verbose https://github.com/libevent/libevent/releases/download/release-2.1.12-stable/libevent-2.1.12-stable.tar.gz
tar -xzf libevent-2.1.12-stable.tar.gz
cd libevent-2.1.12-stable
./configure --prefix=/opt/libevent_2_1 --disable-shared
make install
libtool --finish /opt/libevent_2_1
ldconfig
cd ../../

git clone --branch v1.0.6 --depth=1 https://github.com/bitcoin-sv/bitcoin-sv.git $1
pushd $1
ACLOCAL_PATH=/usr/share/aclocal ./autogen.sh
# --disable-wallet
./configure --disable-tests --disable-bench --with-boost=/opt/boost_1_70
make
popd
