import queue
import socket

from threading import Thread
from interface.math_service import math_service


class rpc_server:
    def __init__(self):
        self.server_socker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socker.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def online(self) -> None:
        # connect the server and register services   
        
        pass

    def offline(self) -> None:
        # stop the server
        pass

    def create_service(self) -> None:
        pass

