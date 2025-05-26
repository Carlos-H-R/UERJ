import socket
import time

from rpc.serializer import serializer


class rpc_client:
    def __init__(self, ip = '127.0.0.1', port = 8060) -> None:
        # create socket 
        self.serializer = serializer()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.bind((ip, port))

    def connect_to_binder(self, protocol: bytes, binder_IP: str, binder_PORT: int) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as binder_socket:
                # binder_socket.bind(('127.0.0.1',8061))
                binder_socket.connect((binder_IP, binder_PORT))
                binder_socket.sendall(protocol)

                rec_obj = binder_socket.recv(4096)
                server_address = self.serializer.unserialize(rec_obj)
                return server_address
                
        except ConnectionRefusedError:
            print(f"The binder has refused connection at {binder_IP}:{binder_PORT}")
            return None
        
        except Exception as error:
            print(f"Error when connecting to the binder: {error}")
            return None

    def call(self, method, x, y):
        # send a request and waits for result
        lookup_request = self.serializer.send_protocol('LOOKUP', method)

        server_address = self.connect_to_binder(lookup_request, '127.0.0.1', 8080)

        if not server_address or not isinstance(server_address, tuple):
            print("Service Unavailable or Wrong Address!")
            return None

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as service_socket:
                service_socket.connect(server_address)
                
                request = {
                    'function': method,
                    'x': x,
                    'y': y
                }
                
                procedure = self.serializer.serialize_obj(request)
                service_socket.sendall(procedure)

                result = service_socket.recv(8192)
                if not result:
                    return None

                result = self.serializer.unserialize(result)
                return result
        
        except ConnectionRefusedError:
            print(f"Conexão recusada pelo servidor {server_address}")
            return None
        
        except Exception as error:
            print(f"Erro durante chamada {method} no servidor {server_address}")
            return None

    def disconect(self) -> None:
        # finish the enlace and close the socket
        pass
