import logging
import time

from electrumsv_node import electrumsv_node

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
