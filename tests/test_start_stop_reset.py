import logging
import os
import tempfile
import time
from pathlib import Path

import electrumsv_node
from electrumsv_node import call_any

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H-%M-%S",
)

logger = logging.getLogger("testing")
MODULE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))


def test_start_stop_reset():
    temp_path = tempfile.TemporaryDirectory()
    print("test_start_stop_reset", temp_path.name)
    try:
        rpcport1 =  20400
        p2p_port1 = 20401
        zmq_port1 = 20402
        electrumsv_node.start(data_path=temp_path.name, rpcport=rpcport1, p2p_port=p2p_port1,
            zmq_port=zmq_port1)
        electrumsv_node.stop(rpcport=rpcport1)
        electrumsv_node.start(data_path=temp_path.name, rpcport=rpcport1, p2p_port=p2p_port1,
            zmq_port=zmq_port1)
        electrumsv_node.stop(rpcport=rpcport1)
        electrumsv_node.reset(data_path=temp_path.name, rpcport=rpcport1)
        assert True
    except Exception as e:
        electrumsv_node.stop()
        raise e
    finally:
        iterations = 5
        while electrumsv_node.is_running(20400) and iterations:
            time.sleep(1)
            iterations -= 1
        temp_path.cleanup()


def test_multiple_instances():
    td1 = tempfile.TemporaryDirectory()
    data_path1 = td1.name
    td2 = tempfile.TemporaryDirectory()
    data_path2 = td2.name
    print("test_multiple_instances", data_path1, data_path2)

    rpcport1 =  20000
    p2p_port1 = 20001
    zmq_port1 = 20002

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
    finally:
        iterations = 5
        while electrumsv_node.is_running(rpcport2) and iterations:
            time.sleep(1)
            iterations -= 1
        td1.cleanup()
        td2.cleanup()


def test_call_any(method_name='help', *args):
    td = tempfile.TemporaryDirectory()
    data_path = td.name
    try:
        electrumsv_node.start(data_path=data_path, rpcport=23000)
        result = call_any(method_name, *args, rpcport=23000, rpchost="127.0.0.1",
            rpcuser="rpcuser", rpcpassword="rpcpassword")
        logger.debug(result.json()['result'])
        electrumsv_node.stop(rpcport=23000, rpchost="127.0.0.1", rpcuser="rpcuser",
            rpcpassword="rpcpassword")
        assert True
    except Exception as e:
        raise e
    finally:
        iterations = 5
        while electrumsv_node.is_running(23000) and iterations:
            time.sleep(1)
            iterations -= 1
        td.cleanup()


# test_call_any("generate", 10)
# test_call_any("getinfo")
# test_start_stop_reset()
