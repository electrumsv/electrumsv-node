Python packages
===============

The original reason that these packages are created containing standalone installs of the
node software, is that ElectrumSV is written in Python and uses the Python packaging system
to acquire it's dependencies. The Python package repository enforces strict compatibility
rules on uploaded binary packages like our node packages, and this ensures that those packages
will run on as wide a range of computers that use the architectures we support.

As of `electrumsv-node` version 0.0.23 we support the following platforms:

* 64 bit Linux.
* 64 bit MacOS (OS X 10.9 and above).
* 64 bit Windows.

For the following versions of Python:

* Python 3.7
* Python 3.8
* Python 3.9

Installing the package
----------------------

Different platforms have different ways of installing Python. If you are using Windows or MacOS,
you can go to the official `Python web site`__ and download a version. If you are using Linux
you will need to work out how to install Python for whatever Linux distribution, we cannot help
you with that.

__ https://www.python.org/downloads/

Windows
~~~~~~~

Ensure you have Python 3.7 or later, you can do so with the following command at a DOS prompt::

    > py --version
    3.9.5

Ensure your `pip` package installation command is associated with the given version of Python,
which in this case is 3.9::

    > pip --version
    pip 21.1.1 from c:\...\python\python39\lib\site-packages\pip (python 3.9)

If your `py` command does not find a version of Python that is supported by `electrumsv-node`,
try the commands `py --help` and `py --list` to see what your options are.

Now that you know what Python version you are installing the package for, you can go ahead and
install it (remember to add any additional arguments you need to `py`)::

    > pip install -U electrumsv-node

This should complete successfully, given that you are using 64-bit Windows and a compatible
version of Python.

MacOS or Linux
~~~~~~~~~~~~~~

Ensure you have Python 3.7 or later, you can do so with the following command in a terminal::

    $ python3 --version
    Python 3.9.1

Ensure that your ``pip3`` command is associated with the version of Python that you are using.
Check the following command prints a message that ends with something like ``(Python 3.8)``
that matches your Python version::

    pip3 --version

Now you should be able to install the `electrumsv-node` package::

    pip3 install -U electrumsv-node

This should complete successfully, given that you are using a 64-bit processor and a compatible
version of Python.

Running the node
----------------

Each Python package contains a Python module and the node binaries for the given platform. The
module is just a simple wrapper that starts and stops running the node, and allows the user to
differentiate the parameters so that they can if necessary run multiple nodes at the same
time. As Python packages are just zip archives, it is possible for a user to download a package
file and extract the included node binaries if they wish.

Running one node instance
~~~~~~~~~~~~~~~~~~~~~~~~~

This package is primarily intended to be used to run local regtest nodes. This example will show
how to run one regtest node, and how to generate blocks and obtain regtest coins using it. The
shown commands will be for Windows, but will work for all supported operating systems.

Starting the node::

    >>> import electrumsv_node
    >>> electrumsv_node.start()
    26400

The value returned is the process id, which in this case is ``26400``. While it is possible to
specify that the node runs against testnet or other blockchains, by default as shown here it runs
against the regtest blockchain. We will now call an RPC method on the running node, check that
we get a response and that our local regtest blockchain is a blank slate with no mined blocks.

Calling the ``getinfo`` RPC method::

    >>> result = electrumsv_node.call_any("getinfo")
    >>> data = result.json()
    >>> data
    {'result': {'version': 101000600, 'protocolversion': 70015, 'walletversion': 160300, 'balance': 0.0, 'blocks': 0, 'timeoffset': 0, 'connections': 0, 'proxy': '', 'difficulty': 4.656542373906925e-10, 'testnet': False, 'stn': False, 'keypoololdest': 1622424022, 'keypoolsize': 2000, 'paytxfee': 0.0, 'relayfee': 2.5e-06, 'errors': 'This is a pre-release or beta test build - use at your own risk - do not use for mining or merchant applications', 'maxblocksize': 10000000000, 'maxminedblocksize': 128000000, 'maxstackmemoryusagepolicy': 100000000, 'maxstackmemoryusageconsensus': 9223372036854775807}, 'error': None, 'id': 0}
    >>> data["result"]["blocks"]
    >>> 0

The response indicates that the node is running, that the wallet is compiled into it, and that
the no blocks have been mined yet. We will now mine one block to an arbitrary regtest address.

Mining a block::

    >>> result = electrumsv_node.call_any("generatetoaddress", 1, "mfs8Y8gAwC2vJHCeSXkHs6LF5nu5PA7nxc")
    >>> result.json()
    {'result': ['1e6b5730e742e7d26338384056563bee8a9b0b06f70b279efe899117e2003366'], 'error': None, 'id': 0}

The response indicates that one block with the given hash was mined. At this point we know how to
start a node and call RPC methods, including generating a block to send coins to one of our
addresses. It is not intended that this documentation illustrate how to use the node RPC methods,
but just to show they can be called in useful ways.

One of the biggest advantages of running a regtest node is that it is your own test blockchain,
and you can reset it any time you want, starting again from a fresh blockchain. First let's
confirm that the local regtest blockchain has a mined block.

    >>> result = electrumsv_node.call_any("getinfo")
    >>> result.json()["result"]["blocks"]
    1

Let's reset the blockchain, so that it is a blank slate we can use to do fresh tests against.

Resetting the node::

    >>> electrumsv_node.reset()

With the node reset, we can start it again and confirm that it has been properly reset.

.. code-block:: python

    >>> electrumsv_node.start()
    8208
    >>> electrumsv_node.call_any("getinfo").json()["result"]["blocks"]
    0

Running multiple node instances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There's a few things that happen when you run one node instance that make it a lot easier to do
without worrying about the details. This includes using the default values to:

* Specify a unique directory for the node to put blockchain data in.
* Specify which port the node should use for RPC.
* Specify which port the node should use for ZMQ.
* Specify which port the node should use for P2P.

If you are going to run multiple node instances you need to pass unique values for each of these
as parameters when calling methods on the ``electrum_node`` Python module.

Start the two nodes::

    >>> import os, tempfile
    >>> base_temp_path = tempfile.gettempdir()
    >>> temp_path1 = os.path.join(base_temp_path, "node1")
    >>> P2P_PORT1=8001
    >>> ZMQ_PORT1=8011
    >>> RPC_PORT1=8021
    >>> temp_path2 = os.path.join(base_temp_path, "node2")
    >>> P2P_PORT2=8002
    >>> ZMQ_PORT2=8012
    >>> RPC_PORT2=8022
    >>> electrumsv_node.start(rpcport=RPC_PORT1, p2p_port=P2P_PORT1, zmq_port=ZMQ_PORT1, data_path=temp_path1)
    27792
    >>> electrumsv_node.start(rpcport=RPC_PORT2, p2p_port=P2P_PORT2, zmq_port=ZMQ_PORT2, data_path=temp_path2)
    27608

At this stage, both nodes lack any knowledge of any other node. They have no way to know about other nodes
they can establish P2P connections to, to share transactions and blocks with.

Tell the first node about the second node::

    >>> result = electrumsv_node.call_any("addnode", f"127.0.0.1:{P2P_PORT2}", "add", rpcport=RPC_PORT1)
    >>> result.json()
    {'result': None, 'error': None, 'id': 0}

The first node will now establish an outgoing P2P connection to the second node. You may need to wait a
a little bit for it to happen.

Generate a block on the second node::

    >>> result = electrumsv_node.call_any("generatetoaddress", 1, "mfs8Y8gAwC2vJHCeSXkHs6LF5nu5PA7nxc", rpcport=RPC_PORT2)
    >>> result.json()
    {'result': ['7d8c4bd2d396e0f4144560b27579f91045e04fdc61359f94f261276237c9280e'], 'error': None, 'id': 0}

Whether your two nodes are connected yet, or are in the process of connecting still, the second node
will share this block with the first node shortly after the connection is established.

Check the status of the first node::

   >>> electrumsv_node.call_any("getinfo", rpcport=RPC_PORT1).json()["result"]["blocks"]
   1

You can now see that the first node has received the block you had the second node mine. Your local network
of nodes is working. A good next step might be to work out how to cause a reorg in one node, by mining
a forked longer chain in the other.