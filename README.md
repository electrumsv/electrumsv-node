# ElectrumSV-Node
A convenient basic wrapper of a (currently unofficial) compiled windows binary
for bitcoin-sv-1.0.2-x86-64.

This is purely for RegTest use on windows.

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

The idea of this repo is to provide a convenient method for getting a RegTest node running on
windows as part of a wider effort to provide a first class RegTest development environment
experience with the ElectrumSV stack (which includes ElectrumX).
