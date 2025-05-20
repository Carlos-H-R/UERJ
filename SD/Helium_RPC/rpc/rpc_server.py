import socket

from queue import Queue
from threading import Thread

from rpc.serializer import serializer
from interface.math_service import math_service


class rpc_server:
    def __init__(self, ip = '127.0.0.1', port = 8070):
        self.IP = ip
        self.PORT = port

        self.server_socker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socker.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socker.bind((ip,port))

        self.serializer = serializer()
        self.calculator = math_service()
    
    def online(self, binder_ip = '127.0.0.1', binder_port = 8080) -> None:
        # connect the server and register services   
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as binder_socket:
            binder_socket.bind(('127.0.0.1',8071))
            binder_socket.connect((binder_ip,binder_port))

            request = self.serializer.send_protocol('REGISTER', 'remote_calculator', self.IP, self.PORT.__str__())

            binder_socket.send(request)
            reply = binder_socket.recv(4096)
            reply = self.serializer.unserialize(reply)
            print(reply)

            binder_socket.close()

        self.queue = Queue()

    def running(self) -> None:
        print("\nServer Online!\n")
        alive = True

        while alive:
            if self.queue.empty():
                try:
                    self.server_socker.listen(5)
                    connection, address = self.server_socker.accept()
                    print(f"New connection {address}")

                    Thread(target=self.processing, args=(connection, address, ))

                except KeyboardInterrupt:
                    self.queue.put(False)

            else:
                alive = self.queue.get()

    def offline(self) -> None:
        # stop the server
        self.queue.put(False)

    def processing(self, connection: socket.socket, address):
        try:
            request: bytes = connection.recv(4096)
            request: dict = self.serializer.unserialize(request)

            func_name = request['function']
            x = request['x']
            y = request['y']

            method = self.calculator.services[func_name]
            return method(x,y)

        except KeyError:
            pass

        except:
            pass
    