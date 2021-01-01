# Dockerfile for building Bitcoin SV
# Adapted from https://github.com/bitcoin-sv/bitcoin-sv/blob/master/contrib/nchain/devops/Dockerfile
# This base image has been pushed to dockerhub at:
# https://hub.docker.com/repository/docker/electrumsvsdk/node-builder-base
FROM centos:7
RUN yum -y install  \
       libboost-all-dev \
       libdb-dev        \
       libdb++-dev      \
       build-essential  \
       libtool          \
       autotools-dev    \
       automake         \
       pkg-config       \
       libssl-dev       \
       libevent-dev     \
       libminiupnpc-dev \
       libzmq3-dev      \
       git              \
       python3          \
       python3-pip      \
       perl             \
       cpanminus        \
       libperlio-gzip-perl \
       libjson-perl     \
       zlib1g-dev       \
       bsdmainutils


RUN pip3 install requests pyzmq rpyc
#RUN cpanm PerlIO::gzip
RUN cpanm JSON
RUN cpanm Term::ReadLine
