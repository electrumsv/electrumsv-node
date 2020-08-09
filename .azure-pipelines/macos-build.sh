#!/bin/bash

brew install automake berkeley-db libtool boost openssl pkg-config libevent
git clone --branch bugfix/cmake-windows-build --depth=1 https://github.com/electrumsv/bitcoin-sv
pushd bitcoin-sv
./autogen.sh
./configure --disable-wallet --disable-tests --disable-bench
make
popd

cp bitcoin-sv/src/bitcoind $ESV_NODE_ARTIFACTS_PATH/
cp bitcoin-sv/src/bitcoin-tx $ESV_NODE_ARTIFACTS_PATH/
cp bitcoin-sv/src/bitcoin-miner $ESV_NODE_ARTIFACTS_PATH/
cp bitcoin-sv/src/bitcoin-seeder $ESV_NODE_ARTIFACTS_PATH/
cp bitcoin-sv/src/bitcoin-cli $ESV_NODE_ARTIFACTS_PATH/
