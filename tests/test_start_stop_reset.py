import logging
import time

from electrumsv_node import electrumsv_node

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

test_start_stop_reset()
