#!/bin/bash

# $1 - path to checkout and build Bitcoin SV in.
# $2 - git clone URI.
# $3 - git clone branch name.

brew install automake berkeley-db libtool boost openssl pkg-config libevent
git clone --branch $3 --depth=1 $2 $1
export MACOSX_DEPLOYMENT_TARGET=10.15
pushd $1
./autogen.sh
./configure --disable-wallet --disable-tests --disable-bench
make
popd
