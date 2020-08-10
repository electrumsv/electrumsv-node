# ElectrumSV-Node

The project is intended to provide Python packages for Linux, MacOS and Windows that include and
help run pre-built Bitcoin SV executables. It should allow the consistently usable and available
ability to run a Bitcoin SV node on any 64-bit platform with the installation of the
`electrumsv-node` package using the standard `pip` package manager for Python.

These packages and the executables within them, are only intended for running nodes for development
as Regtest blockchains. If we had the ability to do so, we would prevent them from running as any
other blockchain. Do not bother us with your questions or problems related to non-Regtest usage.

To install:

    > pip install electrumsv-node

To use it:

    from electrumsv_node import electrumsv_node

    # Set logging level to debug mode to see logging information (Optional)
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s",
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H-%M-%S",
    )

    electrumsv_node.start()
    time.sleep(5)
    electrumsv_node.stop()
    time.sleep(5)
    electrumsv_node.reset()

Console output will look something like this (with directory in site-packages):

    2020-07-03 19-35-57 DEBUG starting RegTest bitcoin daemon...
    2020-07-03 19-36-02 DEBUG stopping RegTest bitcoin daemon...
    2020-07-03 19-36-02 DEBUG bitcoin daemon stopped.
    2020-07-03 19-36-07 DEBUG resetting state of RegTest bitcoin daemon...
    2020-07-03 19-36-09 DEBUG removed G:\electrumsv-node\electrumsv_node\data successfully
    2020-07-03 19-36-09 DEBUG created G:\electrumsv-node\electrumsv_node\data successfully

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
