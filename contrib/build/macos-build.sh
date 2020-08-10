#!/bin/bash

brew install automake berkeley-db libtool boost openssl pkg-config libevent
git clone --branch bugfix/cmake-windows-build --depth=1 https://github.com/electrumsv/bitcoin-sv
pushd bitcoin-sv
./autogen.sh
./configure --disable-wallet --disable-tests --disable-bench
make
popd
