import socket


class ClientSocket:
    def __init__(self, IP, PORT) -> None:
        self.ip = IP
        self.port = PORT
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((IP,PORT))

    def set_address(self, IP, PORT):
        self.socket_client.close()
        self.ip = IP
        self.port = PORT
        self.socket_client.connect()

    def reconect(self):
        # check conection
        # check ping
        self.socket_client.connect((self.ip,self.port))

    def disconect(self):
        self.socket_client.close()

    


if __name__ == "__main__":
    IP = '192.168.1.47'
    PORT = 8080

    c = ClientSocket(IP, PORT)
