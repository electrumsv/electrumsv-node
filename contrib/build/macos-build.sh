#!/bin/bash

# $1 - path to checkout and build Bitcoin SV in.

# Fix for:
#   `configure: error: libdb_cxx missing, Bitcoin SV requires this library for wallet`
#   `functionality (--disable-wallet to disable wallet functionality)`
brew install berkeley-db4
brew link berkeley-db4 --force

brew install automake libtool boost openssl pkg-config libevent
brew install zeromq  # needed for --enable-zmq to work
git clone --branch bugfix/cmake-macos-build-1.0.13 --depth=1 https://github.com/electrumsv/bitcoin-sv $1
export MACOSX_DEPLOYMENT_TARGET=10.15
pushd $1
./autogen.sh
# --disable-wallet
./configure --disable-tests --disable-bench --enable-zmq
make
popd
