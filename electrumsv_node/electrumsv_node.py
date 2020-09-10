import json
import logging
import os
import shutil
import signal
import subprocess
import sys
from typing import Optional, Union

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


def is_running() -> bool:
    try:
        payload = json.dumps({"jsonrpc": "2.0", "method": "getinfo", "params": [], "id": 0})
        result = requests.post("http://rpcuser:rpcpassword@127.0.0.1:18332", data=payload)
        result.raise_for_status()
        # print(result.json())
        return True
    except Exception:
        return False


# https://stackoverflow.com/questions/1196074/how-to-start-a-background-process-in-python
def _start(config_path: Optional[str]=None, data_path: Optional[str]=None) -> int:
    global DEFAULT_DATA_PATH
    if config_path is None:
        config_path = os.path.join(FILE_PATH, "bitcoin.conf")
    if data_path is None:
        data_path = DEFAULT_DATA_PATH
    os.makedirs(data_path, exist_ok=True)
    args = [ BITCOIND_PATH, f"-conf={config_path}", f"-datadir={data_path}",
        "-rpcuser=rpcuser", "-rpcpassword=rpcpassword" ]
    proc: subprocess.Popen
    if sys.platform == "win32":
        args[0] = f"\"{args[0]}\""
        proc = subprocess.Popen(" ".join(args), creationflags=subprocess.DETACHED_PROCESS)
    elif sys.platform in ("darwin", "linux"):
        proc = subprocess.Popen(args)
    else:
        raise UnknownPlatformError(sys.platform)
    return proc.pid


def is_node_running():
    for timeout in (3, 3, 3):
        logger.debug("polling bitcoin node...")
        if is_running():
            return True
        time.sleep(timeout)


def start(config_path: Optional[str] = None, data_path: Optional[str] = None) -> int:
    logger.debug("starting bitcoin node")
    pid = _start()
    if is_node_running():
        return pid

    # sometimes the node is still shutting down from a previous run
    logger.debug("starting the bitcoin node failed - retrying...")
    pid = _start()
    if is_node_running():
        return pid
    raise FailedToStartError("failed to start bitcoin node")


def stop(first_attempt: bool=True):
    try:
        logger.debug("stopping bitcoin node")
        assert is_running(), "bitcoin daemon is not running."
        payload = json.dumps({"jsonrpc": "2.0", "method": "stop", "params": [], "id": 0})
        result = requests.post("http://rpcuser:rpcpassword@127.0.0.1:18332", data=payload)
        result.raise_for_status()
        logger.debug("bitcoin daemon stopped.")
        return result
    except Exception as e:
        if first_attempt:
            logger.error(str(e) + " Retrying after 1 second in case it is still waking up...")
            time.sleep(1)
            stop(first_attempt=False)
        else:
            logger.error(str(e))


def is_node_stopped():
    for timeout in (3, 3, 3):
        if is_running():
            logger.error("the bitcoin daemon must be shutdown to reset - retrying in 3 seconds")
            time.sleep(timeout)
        else:
            return True
    return False


def reset(data_path: Optional[str]=None):
    if data_path is None:
        data_path = DEFAULT_DATA_PATH
    try:
        logger.debug("resetting state of RegTest bitcoin daemon...")
        if not is_node_stopped():
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


def call_any(method_name: str, *args):
    result = None
    try:
        if not args:
            params = []
        else:
            params = [*args]
        payload = json.dumps({"jsonrpc": "2.0", "method": f"{method_name}", "params": params,
            "id": 0})
        result = requests.post("http://rpcuser:rpcpassword@127.0.0.1:18332", data=payload)
        result.raise_for_status()
        return result
    except requests.exceptions.HTTPError as e:
        if result is not None:
            logger.error(result.json()['error']['message'])
        raise e


__all__ = [ "start", "stop", "is_running", "reset", "call_any", "BITCOIND_PATH",
    "DEFAULT_DATA_PATH" ]

