import logging
import os
import shutil
import time
from pathlib import Path

from electrumsv_node import electrumsv_node
from electrumsv_node.electrumsv_node import call_any, FailedToStopError

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H-%M-%S",
)

logger = logging.getLogger("testing")
MODULE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))


def test_start_stop_reset():
    try:
        electrumsv_node.start()
        electrumsv_node.stop()
        electrumsv_node.start()
        electrumsv_node.stop()
        try:
            electrumsv_node.reset()
        except FailedToStopError as e:
            logger.debug(str(e))
            electrumsv_node.stop()
        electrumsv_node.reset()
        assert True
    except Exception as e:
        raise e


def test_multiple_instances():
    data_path1 = MODULE_DIR.joinpath("datadir1")
    rpcport1 =  20000
    p2p_port1 = 20001

    data_path2 = MODULE_DIR.joinpath("datadir2")
    rpcport2 =  20002
    p2p_port2 = 20003
    try:
        electrumsv_node.start(data_path=data_path1, rpcport=rpcport1, p2p_port=p2p_port1)
        electrumsv_node.start(data_path=data_path2, rpcport=rpcport2, p2p_port=p2p_port2)
        time.sleep(5)
        result1 = call_any("getinfo", rpcport=rpcport1)
        result2 = call_any("getinfo", rpcport=rpcport2)
        result1.json()
        result2.json()
        electrumsv_node.stop(rpcport=rpcport1)
        electrumsv_node.stop(rpcport=rpcport2)
        electrumsv_node.reset(data_path=data_path1, rpcport=rpcport1)
        electrumsv_node.reset(data_path=data_path2, rpcport=rpcport2)
        assert True
    except Exception as e:
        electrumsv_node.stop(rpcport=rpcport1)
        electrumsv_node.stop(rpcport=rpcport2)
        raise e


def test_call_any(method_name='help', *args):
    try:
        electrumsv_node.start()
        time.sleep(5)
        result = call_any(method_name, *args)
        print(result.json()['result'])
        time.sleep(5)
        electrumsv_node.stop()
        assert True
    except Exception as e:
        raise e

# test_call_any("generate", 10)
# test_call_any("help")
# test_start_stop_reset()
