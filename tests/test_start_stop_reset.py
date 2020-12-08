import logging
import os
import time
from pathlib import Path

from electrumsv_node import electrumsv_node
from electrumsv_node.electrumsv_node import call_any

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
        electrumsv_node.reset()
        assert True
    except Exception as e:
        electrumsv_node.stop()
        raise e


def test_multiple_instances():
    data_path1 = MODULE_DIR.joinpath("datadir1")
    rpcport1 =  20000
    p2p_port1 = 20001
    zmq_port1 = 20002

    data_path2 = MODULE_DIR.joinpath("datadir2")
    rpcport2 =  22000
    p2p_port2 = 22001
    zmq_port2 = 22003
    try:
        electrumsv_node.start(data_path=data_path1, rpcport=rpcport1, p2p_port=p2p_port1,
            zmq_port=zmq_port1)
        electrumsv_node.start(data_path=data_path2, rpcport=rpcport2, p2p_port=p2p_port2,
            zmq_port=zmq_port2)
        time.sleep(5)
        result1 = call_any("getinfo", rpcport=rpcport1)
        result2 = call_any("getinfo", rpcport=rpcport2)
        result1.json()
        result2.json()
        electrumsv_node.stop(rpcport=rpcport1, rpchost="127.0.0.1", rpcuser="rpcuser",
            rpcpassword="rpcpassword")
        electrumsv_node.stop(rpcport=rpcport2, rpchost="127.0.0.1", rpcuser="rpcuser",
            rpcpassword="rpcpassword")
        electrumsv_node.reset(data_path=data_path1, rpcport=rpcport1, rpcuser="rpcuser",
            rpcpassword="rpcpassword")
        electrumsv_node.reset(data_path=data_path2, rpcport=rpcport2, rpcuser="rpcuser",
            rpcpassword="rpcpassword")
        assert True
    except Exception as e:
        electrumsv_node.stop(rpcport=rpcport1, rpchost="127.0.0.1", rpcuser="rpcuser",
            rpcpassword="rpcpassword")
        electrumsv_node.stop(rpcport=rpcport2, rpchost="127.0.0.1", rpcuser="rpcuser",
            rpcpassword="rpcpassword")
        raise e


def test_call_any(method_name='help', *args):
    try:
        electrumsv_node.start()
        time.sleep(5)
        result = call_any(method_name, *args, rpcport=18332, rpchost="127.0.0.1", rpcuser="rpcuser",
            rpcpassword="rpcpassword")
        print(result.json()['result'])
        time.sleep(5)
        electrumsv_node.stop(rpcport=18332, rpchost="127.0.0.1", rpcuser="rpcuser",
            rpcpassword="rpcpassword")
        assert True
    except Exception as e:
        raise e


# test_call_any("generate", 10)
# test_call_any("help")
# test_start_stop_reset()
