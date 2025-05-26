import socket

from rpc.serializer import serializer


class rpc_client:
    def __init__(self, ip = '127.0.0.1', port = 8060) -> None:
        # create socket 
        self.serializer = serializer()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.bind((ip, port))

    def connect(self, protocol: bytes, binder_IP: str, binder_PORT: int) -> bool:
        # conect to binder
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as binder_socket:
            # binder_socket.bind(('127.0.0.1',8061))
            binder_socket.connect((binder_IP, binder_PORT))
            binder_socket.send(protocol)

            rec_obj = binder_socket.recv(4096)
            server_address = self.serializer.unserialize(rec_obj)
            print(server_address)

            if not server_address:
                print('Service Unavaliable!')
                return False

            else:
                self.client_socket.connect(server_address)
                print(f"Conected to server {server_address}")
                return True

    def disconect(self) -> None:
        # finish the enlace and close the socket
        pass

    def call(self, method, x, y):
        # send a request and waits for result
        request = self.serializer.send_protocol('LOOKUP', method)
        if self.connect(request, '127.0.0.1', 8080):
            request = {'function': method,
                       'x': x,
                       'y': y
                       }

            procedure = self.serializer.serialize_obj(request)
            self.client_socket.send(procedure)

            result = self.client_socket.recv(8192)
            result = self.serializer.unserialize(result)
            print(result)
        
            return result

        else:
            pass
