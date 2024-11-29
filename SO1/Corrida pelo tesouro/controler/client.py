import socket


class client:
    def __init__(self, IP, PORT) -> None:
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((IP,PORT))


#
