#!/bin/bash

# $1 - path to checkout and build Bitcoin SV in.

brew install automake berkeley-db libtool boost openssl pkg-config libevent
git clone --branch bugfix/cmake-windows-build --depth=1 https://github.com/electrumsv/bitcoin-sv $1
export MACOSX_DEPLOYMENT_TARGET=10.15
pushd $1
./autogen.sh
./configure --disable-wallet --disable-tests --disable-bench
make
popd