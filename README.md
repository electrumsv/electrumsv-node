[![PyPI version](https://badge.fury.io/py/electrumsv-node.svg)](https://badge.fury.io/py/electrumsv-node) 
[![Build Status](https://dev.azure.com/electrumsv/ElectrumSV/_apis/build/status/electrumsv.electrumsv-node?branchName=master)](https://dev.azure.com/electrumsv/ElectrumSV/_build/latest?definitionId=5&branchName=master)
[![Platforms](https://img.shields.io/badge/platforms-linux%20%7C%20windows%20%7C%20macos-blue)](https://img.shields.io/badge/platforms-linux%20%7C%20windows%20%7C%20macos-blue)
[![Node Version](https://img.shields.io/badge/node_version-v1.0.7-brown)](https://img.shields.io/badge/platforms-linux%20%7C%20windows%20%7C%20macos-blue)

# ElectrumSV-Node

The project is intended to provide Python packages for Linux, MacOS and Windows that include and
help run pre-built Bitcoin SV executables. It should allow the consistently usable and available
ability to run a Bitcoin SV node on any 64-bit platform with the installation of the
`electrumsv-node` package using the standard `pip` package manager for Python.

These packages and the executables within them, are only intended for running nodes for development
as Regtest blockchains. If we had the ability to do so, we would prevent them from running as any
other blockchain. Do not bother us with your questions or problems related to non-Regtest usage.

* You must be using 64-bit Python 3.7 or 3.8.
* You must be using Windows, MacOS or Linux.
* You must have the latest version of the `pip` package.

To update `pip`:

    > python3 -m pip install --upgrade pip

To install `electrumsv-node`:

    > pip3 install electrumsv-node

To use it:

    import logging
    import electrumsv_node
    
    # Set logging level to debug mode to see logging information (Optional)
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s",
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H-%M-%S",
    )
    logger = logging.getLogger("testing")
    
    electrumsv_node.start()
    
    # (Optional keyword arguments)
    # electrumsv_node.start(
    #     data_path=</your/custom/datadir/path>,
    #     rpcuser="rpcuser",
    #     rpcpassword="rpcpassword",
    #     rpcport=18332,
    #     p2p_port=18444,
    #     zmq_port=28332,
    #     network='regtest',
    #     print_to_console=True,  # feeds logging to stdout
    #     extra_params=['-somearg1=var1', '-somearg2=var2']
    # )
    
    result = electrumsv_node.call_any('getinfo')
    logger.debug(result.json())
    electrumsv_node.stop()
    electrumsv_node.reset()


Console output will look something like this (with custom data directory):

    2021-01-03 11-50-29 INFO starting bitcoin node
    2021-01-03 11-50-29 DEBUG polling bitcoin node...
    2021-01-03 11-50-31 DEBUG polling bitcoin node...
    2021-01-03 11-50-32 INFO bitcoin node online
    2021-01-03 11-50-32 DEBUG {'result': {'version': 101000700, 'protocolversion': 70015
    , 'walletversion': 160300, 'balance': 0.0, 'blocks': 0, 'timeoffset': 0, 'connections': 0, 'proxy': '', 'difficulty': 4.656542373906925e-10, 'testnet': False, 'stn': False, 'keypoololdest': 1609627830, 'keypoolsize': 2000, 'paytxfee': 0.0, 'relayfee': 2.5e-06, 'errors': 'This is a pre-release or beta test build - use at your own risk - do not use for mining or merchant applications', 'maxblocksize': 10000000000, 'maxminedblocksize': 128000000, 'maxstackmemoryusagepolicy': 100000000, 'maxstackmemoryusageconsensus': 9223372036854775807}, 'error': None, 'id': 0}
    2021-01-03 11-50-32 DEBUG stopping bitcoin node
    2021-01-03 11-50-32 INFO bitcoin daemon stopped.
    2021-01-03 11-50-32 DEBUG resetting state of RegTest bitcoin daemon...
    2021-01-03 11-50-32 ERROR the bitcoin daemon must be shutdown to reset - retrying in 3 seconds
    2021-01-03 11-50-35 DEBUG removed 'C:\Users\donha\AppData\Local\ElectrumSV-Node' successfully

## The node data directory

By default, the node will be started with a data directory in a standard location. On Windows this
will be within `ElectrumSV-Node` in the computer's `LOCALAPPDATA` directory, which will likely be
`c:\users\<user-name>\AppData\Local`. On MacOS and Linux this will be within `.electrumsv-node` in
the user's home directory, which will likely be something like `/home/<user-name>` on Linux or
`/Users/<user-name>` on MacOS.

## ElectrumSV and ElectrumSV-Node

This is part of a wider effort to provide a first class RegTest development environment
experience with the [ElectrumSV](https://github.com/electrumsv/electrumsv) stack (which includes
ElectrumX). It is expected that for these purposes, the
[ElectrumSV-SDK](https://github.com/electrumsv/electrumsv-sdk) project will be the way that
developers will make use of ElectrumSV-Node.
