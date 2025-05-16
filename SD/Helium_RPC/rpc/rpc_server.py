import queue
import pickle
import socket

from threading import Thread


class rpc_server:
    def __init__(self):
        self.server_socker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socker.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def online() -> None:
        # connect the server and distribute ports        
        pass

    def offline() -> None:
        # stop the server
        pass

    
    