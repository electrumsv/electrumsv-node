import logging
import electrumsv_node

# Set logging level to debug mode to see logging information (Optional)
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H-%M-%S",
)
logger = logging.getLogger("testing")

def test_simple_start_call_stop():
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
