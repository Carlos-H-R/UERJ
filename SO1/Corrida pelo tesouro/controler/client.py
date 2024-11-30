import socket


class Client:
    def __init__(self, IP, PORT) -> None:
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((IP,PORT))


if __name__ == "__main__":
    c = Client(123, 8080)
