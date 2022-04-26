#!/bin/bash

# $1 - path to checkout and build Bitcoin SV in.

brew install automake berkeley-db libtool boost openssl pkg-config libevent
brew install zeromq  # needed for --enable-zmq to work
git clone --branch v1.0.11 --depth=1 https://github.com/bitcoin-sv/bitcoin-sv.git $1
export MACOSX_DEPLOYMENT_TARGET=10.15
pushd $1
./autogen.sh
# --disable-wallet
./configure --disable-tests --disable-bench --enable-zmq
make
popd
