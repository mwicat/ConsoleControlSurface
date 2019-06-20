import os
import sys


CONSOLE_PORT = 8484


def spawn_console(namespace):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, BASE_DIR)
    from rfoo.utils import rconsole
    rconsole.spawn_server(namespace=namespace, port=CONSOLE_PORT)
