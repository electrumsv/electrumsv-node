#!/bin/bash

# $1 - path to checkout and build Bitcoin SV in.

brew install automake berkeley-db libtool boost openssl pkg-config libevent
git clone --branch bugfix/cmake-windows-build-1.0.6 --depth=1 https://github.com/electrumsv/bitcoin-sv $1
export MACOSX_DEPLOYMENT_TARGET=10.15
pushd $1
./autogen.sh
# --disable-wallet
./configure --disable-tests --disable-bench --enable-zmq
make
popd
