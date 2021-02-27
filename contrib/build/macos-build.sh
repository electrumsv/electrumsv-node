#!/bin/bash

# https://github.com/bitcoin-sv/bitcoin-sv/issues/18

# $1 - path to checkout and build Bitcoin SV in.

brew install automake libtool boost openssl pkg-config libevent
brew install zeromq  # needed for --enable-zmq to work
brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/master/Formula/berkeley-db.rb --without-java
brew link berkeley-db4 --force
export PATH="/usr/local/opt/berkeley-db@4/bin:$PATH"
export LDFLAGS="-L/usr/local/opt/berkeley-db@4/lib"
export CPPFLAGS="-I/usr/local/opt/berkeley-db@4/include"

git clone --branch bugfix/cmake-windows-build-1.0.7 --depth=1 https://github.com/electrumsv/bitcoin-sv $1
export MACOSX_DEPLOYMENT_TARGET=10.15

pushd $1
./autogen.sh
# --disable-wallet
./configure --disable-tests --disable-bench --enable-zmq
make
popd
