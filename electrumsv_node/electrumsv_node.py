import json
import logging
import os
import shutil
from pathlib import Path
import subprocess
from typing import Tuple

import requests
import time

logger = logging.getLogger("download_bitcoind")
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
path_to_bitcoind = Path(MODULE_DIR).joinpath("bin").joinpath("bitcoind")
path_to_data_dir = Path(MODULE_DIR).joinpath("data")
path_to_config = Path(MODULE_DIR).joinpath("bitcoin.conf")

def _create_if_not_exist(path):
    path = Path(path)
    root = Path(path.parts[0])  # Root
    cur_dir = Path(root)
    for part in path.parts:
        if Path(part) != root:
            cur_dir = cur_dir.joinpath(part)
        if cur_dir.exists():
            continue
        else:
            os.mkdir(cur_dir)
            logger.debug(f"created '{cur_dir}' successfully")

def _is_bitcoind_running() -> bool:
    try:
        payload = json.dumps({"jsonrpc": "2.0", "method": "getinfo", "params": [], "id": 0})
        result = requests.post("http://rpcuser:rpcpassword@127.0.0.1:18332", data=payload)
        result.raise_for_status()
        # print(result.json())
        return True
    except Exception as e:
        return False

def start():
    logger.debug("starting RegTest bitcoin daemon...")
    _create_if_not_exist(path_to_data_dir)
    subprocess.Popen(
        f"start cmd /C {path_to_bitcoind} -conf={path_to_config} -datadir={path_to_data_dir} "
        f"-rpcuser=rpcuser -rpcpassword=rpcpassword", shell=True)


def stop(first_attempt=True):
    try:
        logger.debug("stopping RegTest bitcoin daemon...")
        assert _is_bitcoind_running(), "bitcoin daemon is not running."
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

def reset():
    try:
        logger.debug("resetting state of RegTest bitcoin daemon...")
        assert not _is_bitcoind_running(), "the bitcoin daemon must be shutdown to reset"
        shutil.rmtree(path_to_data_dir)
        logger.debug(f"removed '{path_to_data_dir}' successfully")
        _create_if_not_exist(path_to_data_dir)
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
        # print(f"calling method: {method_name}")
        payload = json.dumps({"jsonrpc": "2.0", "method": f"{method_name}", "params": params,
            "id": 0})
        result = requests.post("http://rpcuser:rpcpassword@127.0.0.1:18332", data=payload)
        result.raise_for_status()
        return result
    except requests.exceptions.HTTPError as e:
        if result is not None:
            logger.error(result.json()['error']['message'])
        raise e
