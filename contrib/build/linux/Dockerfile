# Dockerfile for building Bitcoin SV
# Adapted from https://github.com/bitcoin-sv/bitcoin-sv/blob/master/contrib/nchain/devops/Dockerfile
# This base image has been pushed to dockerhub at:
# https://hub.docker.com/repository/docker/electrumsvsdk/node-builder-base
FROM nchain/buildtools:build-sv-centos7.6

RUN yum install -y dos2unix
COPY install_system_requirements.sh /
RUN dos2unix /install_system_requirements.sh
RUN /install_system_requirements.sh
