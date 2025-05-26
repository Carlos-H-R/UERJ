from threading import Thread

from rpc.rpc_server import rpc_server
from rpc.rpc_binder import binder


def proxy_binder():
    _binder = binder()
    _binder.start_binder()


if __name__ == "__main__":
    binder = binder()