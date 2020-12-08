import json
import logging
import os
import shutil
import signal
import subprocess
import sys
from typing import Iterable, Optional, List
import requests
import time


class FailedToStartError(Exception):
    pass


class FailedToStopError(Exception):
    pass


# https://stackoverflow.com/a/16809886/11881963
if sys.platform in ("linux", "darwin"):
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)


logger = logging.getLogger("electrumsv-node")
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class UnknownPlatformError(Exception):
    pass


FILE_PATH = os.path.dirname(os.path.abspath(__file__))
BITCOIND_PATH = os.path.join(FILE_PATH, "bin", "bitcoind")


def _locate_default_data_path() -> str:
    if sys.platform == "win32":
        return os.path.join(os.environ.get("LOCALAPPDATA"), "ElectrumSV-Node")
    elif sys.platform in ("darwin", "linux"):
        return os.path.join(os.environ["HOME"], ".electrumsv-node")
    raise UnknownPlatformError(sys.platform)

DEFAULT_DATA_PATH = _locate_default_data_path()


def is_running(rpcport: int=18332, rpchost: str="127.0.0.1", rpcuser:
        str="rpcuser", rpcpassword: str="rpcpassword") -> bool:
    try:
        payload = json.dumps({"jsonrpc": "2.0", "method": "getinfo", "params": [], "id": 0})
        result = requests.post(f"http://{rpcuser}:{rpcpassword}@{rpchost}:{rpcport}", data=payload,
            timeout=0.5)
        result.raise_for_status()
        return True
    except Exception:
        return False


def shell_command(config_path: Optional[str] = None, data_path: Optional[str] = None,
        rpcport: int = 18332, rpcuser: str = 'rpcuser',
        rpcpassword: str = 'rpcpassword', network: str = 'regtest',
        p2p_port: int = 18444, zmq_port: int = 28332,
        print_to_console: bool = False, extra_params: Optional[Iterable[str]] = None) -> List:
    """
    Generates the full shell command needed to launch the bitcoin daemon with the desired
    configuration
    """
    global DEFAULT_DATA_PATH
    split_command = [BITCOIND_PATH]
    valid_networks = {'regtest', 'testnet', 'stn', 'main'}
    assert network in valid_networks, f"must select 'network' from {valid_networks}"
    if network != 'main':
        split_command.append(f"-{network}")

    if print_to_console:
        split_command.append(f"-printtoconsole=1")

    if config_path is None:
        config_path = os.path.join(FILE_PATH, "bitcoin.conf")
    if data_path is None:
        data_path = DEFAULT_DATA_PATH
    os.makedirs(data_path, exist_ok=True)
    split_command.extend([
        f"-conf={config_path}",
        f"-datadir={data_path}",
        f"-rpcuser={rpcuser}",
        f"-rpcpassword={rpcpassword}",
        f"-rpcport={rpcport}",
        f"-port={p2p_port}",
        "-rest",
        f"-zmqpubrawtx=tcp://127.0.0.1:{zmq_port}",
        f"-zmqpubrawblock=tcp://127.0.0.1:{zmq_port}",
        f"-zmqpubhashtx=tcp://127.0.0.1:{zmq_port}",
        f"-zmqpubhashblock=tcp://127.0.0.1:{zmq_port}"
    ])
    if extra_params is not None:
        split_command.extend(extra_params)

    proc: subprocess.Popen
    if sys.platform == "win32":
        split_command[0] = f"\"{split_command[0]}\""
        return split_command
    elif sys.platform in ("darwin", "linux"):
        return split_command
    else:
        raise UnknownPlatformError(sys.platform)


# https://stackoverflow.com/questions/1196074/how-to-start-a-background-process-in-python
def _start(config_path: Optional[str]=None, data_path: Optional[str]=None,
           rpcport: int=18332, rpcuser: str='rpcuser',
           rpcpassword: str='rpcpassword', network: str='regtest',
           p2p_port: int=18444, zmq_port: int=28332,
           print_to_console: bool=False, extra_params: Optional[Iterable[str]]=None) -> int:

    split_command = shell_command(config_path, data_path, rpcport, rpcuser, rpcpassword, network,
        p2p_port, zmq_port, print_to_console, extra_params)

    proc: subprocess.Popen
    if sys.platform == "win32":
        proc = subprocess.Popen(" ".join(split_command), creationflags=subprocess.DETACHED_PROCESS)
    elif sys.platform in ("darwin", "linux"):
        proc = subprocess.Popen(split_command)
    else:
        raise UnknownPlatformError(sys.platform)
    return proc.pid


def is_node_running(rpcport: int=18332, rpchost: str="127.0.0.1", rpcuser: str="rpcuser",
        rpcpassword: str="rpcpassword"):
    for timeout in [1] * 5:
        logger.debug("polling bitcoin node...")
        if is_running(rpcport, rpchost, rpcuser, rpcpassword):
            return True
        time.sleep(timeout)


def start(config_path: Optional[str]=None, data_path: Optional[str]=None,
          rpcport: int=18332, rpcuser: str='rpcuser',
          rpcpassword: str='rpcpassword', network: str='regtest',
          p2p_port: int=18444, zmq_port: int=28332,
          print_to_console: bool=False, extra_params: Optional[Iterable[str]]=None) -> int:
    """
    Can only start a node from localhost / the same machine - remote access is only
    supported for RPC commands - namely in the case of dockerization
    """
    logger.debug("starting bitcoin node")
    pid = _start(config_path, data_path, rpcport, rpcuser, rpcpassword, network, p2p_port,
        zmq_port, print_to_console, extra_params)
    if is_node_running(rpcport, "127.0.0.1", rpcuser, rpcpassword):
        time.sleep(1)  # Avoids failure of stop() if called immediately afterwards
        logger.info("bitcoin node online")
        return pid

    # sometimes the node is still shutting down from a previous run
    logger.debug("starting the bitcoin node failed - retrying...")
    pid = _start(config_path, data_path, rpcport, rpcuser, rpcpassword, network, p2p_port,
        zmq_port, print_to_console, extra_params)
    if is_node_running(rpcport, "127.0.0.1", rpcuser, rpcpassword):
        time.sleep(1)  # Avoids failure of stop() if called immediately afterwards
        logger.info("bitcoin node online")
        return pid
    raise FailedToStartError("failed to start bitcoin node")


def stop(first_attempt: bool=True, rpcport: int=18332, rpchost: str="127.0.0.1",
        rpcuser: str="rpcuser", rpcpassword: str="rpcpassword"):
    try:
        logger.debug("stopping bitcoin node")
        assert is_running(rpcport, rpchost, rpcuser, rpcpassword), "bitcoin daemon is not running."
        payload = json.dumps({"jsonrpc": "2.0", "method": "stop", "params": [], "id": 0})
        result = requests.post(f"http://{rpcuser}:{rpcpassword}@{rpchost}:{rpcport}", data=payload,
            timeout=0.5)
        result.raise_for_status()
        logger.debug("bitcoin daemon stopped.")
    except Exception as e:
        if first_attempt:
            logger.error(str(e) + " Retrying after 1 second in case it is still waking up...")
            time.sleep(1)
            stop(first_attempt=False, rpcport=rpcport, rpchost=rpchost, rpcuser=rpcuser,
                rpcpassword=rpcpassword)
        else:
            logger.error(str(e))
            return
        logger.error(str(e))


def is_node_stopped(rpcport: int=18332, rpchost: str="127.0.0.1", rpcuser: str="rpcuser",
        rpcpassword: str="rpcpassword"):
    for timeout in (3, 3, 3):
        if is_running(rpcport, rpchost, rpcuser, rpcpassword):
            logger.error("the bitcoin daemon must be shutdown to reset - retrying in 3 seconds")
            time.sleep(timeout)
        else:
            return True
    return False


def reset(data_path: Optional[str]=None, rpcport: int=18332, rpcuser: str="rpcuser",
        rpcpassword: str="rpcpassword"):
    """can only reset on localhost i.e. the same machine that the node is running on"""
    if data_path is None:
        data_path = DEFAULT_DATA_PATH
    try:
        logger.debug("resetting state of RegTest bitcoin daemon...")
        if not is_node_stopped(rpcport, "127.0.0.1", rpcuser, rpcpassword):
            logger.error("the bitcoin daemon must be shutdown to reset - reached max reattempts")
            raise FailedToStopError("node is not stopped - try stopping the node before "
                "resetting")
        if os.path.exists(data_path):
            shutil.rmtree(data_path)
            logger.debug(f"removed '{data_path}' successfully")
        os.makedirs(data_path, exist_ok=True)
    except FailedToStopError:
        raise
    except Exception as e:
        logger.exception(e)
        raise


def call_any(method_name: str, *args, rpcport: int=18332, rpchost: str="127.0.0.1", rpcuser:
        str="rpcuser", rpcpassword: str="rpcpassword"):
    """Send an RPC request to the specified bitcoin node"""
    result = None
    try:
        if not args:
            params = []
        else:
            params = [*args]
        payload = json.dumps(
            {"jsonrpc": "2.0", "method": f"{method_name}", "params": params, "id": 0})
        result = requests.post(f"http://{rpcuser}:{rpcpassword}@{rpchost}:{rpcport}", data=payload,
                               timeout=10.0)
        result.raise_for_status()
        return result
    except requests.exceptions.HTTPError as e:
        if result is not None:
            logger.error(result.json()['error']['message'])
        raise e


__all__ = [ "start", "stop", "is_running", "reset", "call_any", "BITCOIND_PATH",
    "DEFAULT_DATA_PATH" ]
