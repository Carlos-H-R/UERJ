import socket

from serializer import serializer


class rpc_stub_generator():
    def __init__(self, ip, port) -> None:
        # create socket 
        self.serializer = serializer()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.bind(ip, port)

    def conect(self, protocol: bytes, binder_IP: str, binder_PORT: int) -> None:
        # conect to binder
        self.client_socket.connect((binder_IP, binder_PORT))
        self.client_socket.send(protocol)

        rec_obj = self.client_socket.recv(1024)
        server_address = self.serializer.unserialize(rec_obj)

        self.client_socket.connect(server_address)

    def disconect(self) -> None:
        # finish the enlace and close the socket
        pass

    def call(self, method, arg1, arg2):
        # send a request and waits for result
        request = self.serializer.send_protocol('LOOKUP', method)
        self.conect(request, 'http://localhost', 8080)

        procedure = self.serializer.serialize(method,arg1,arg2)
        
        self.client_socket.send(procedure)

        result = self.client_socket.recv(1024)
        result = self.serializer.unserialize(result)
        
        return result
    
    def add(self, x: int, y: int):
        return self.call('add', x, y)
    
    def sub(self, x: int, y: int):
        return self.call('sub', x, y)
    
    def divide(self, x: int, y: int):
        return self.call('divide', x, y)
    
    def multiply(self, x: int, y: int):
        return self.call('multiply', x, y)
