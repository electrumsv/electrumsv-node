import logging
import time

from electrumsv_node import electrumsv_node
from electrumsv_node.electrumsv_node import call_any

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H-%M-%S",
)

def test_start_stop_reset():
    try:
        electrumsv_node.start()
        time.sleep(5)
        electrumsv_node.stop()
        time.sleep(5)
        electrumsv_node.reset()
        assert True
    except Exception as e:
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
