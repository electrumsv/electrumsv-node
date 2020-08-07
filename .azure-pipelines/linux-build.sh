#!/bin/bash
sudo apt-get install build-essential libtool autotools-dev automake pkg-config libssl-dev libevent-dev bsdmainutils
sudo apt-get install libboost-system-dev libboost-filesystem-dev libboost-chrono-dev libboost-program-options-dev libboost-test-dev libboost-thread-dev
sudo apt-get install g++-mingw-w64-x86-64
sudo update-alternatives --config x86_64-w64-mingw32-g++
git clone --branch v1.0.4 --depth=1 https://github.com/bitcoin-sv/bitcoin-sv.git
pushd bitcoin-sv

pushd depends
make build-win64
popd

./autogen.sh
CONFIG_SITE=$PWD/depends/x86_64-w64-mingw32/share/config.site  ./configure --disable-wallet --disable-tests --disable-bench --prefix=/
make
popd

# sudo apt-get install build-essential libtool autotools-dev automake pkg-config libssl-dev libevent-dev bsdmainutils
# sudo apt-get install libboost-system-dev libboost-filesystem-dev libboost-chrono-dev libboost-program-options-dev libboost-test-dev libboost-thread-dev
# git clone --branch v1.0.4 --depth=1 https://github.com/bitcoin-sv/bitcoin-sv.git
# pushd bitcoin-sv
# ./autogen.sh
# ./configure --disable-wallet --disable-tests --disable-bench
# make
# popd
