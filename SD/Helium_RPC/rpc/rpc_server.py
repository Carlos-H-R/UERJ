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

        self.service_provider = dict()
        self.serializer = serializer()
        self.calculator = math_service()
    
    def online(self, binder_ip = '127.0.0.1', binder_port = 8080) -> None:
        # connect the server and register services   
        
        try:    
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as binder_socket:
                # binder_socket.bind(('127.0.0.1',8071))
                binder_socket.connect((binder_ip,binder_port))
                
                for service in self.calculator.services:
                    service_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    service_socket.bind((self.IP,0))
                    
                    address = service_socket.getsockname()
                    
                    t = Thread(target=self.service, args=(service_socket, )).start()
                    self.service_provider[service] = t

                    request = self.serializer.send_protocol('REGISTER', service, address[0], (address[1]).__str__())
                    binder_socket.send(request)

                    reply = binder_socket.recv(4096)
                    reply = self.serializer.unserialize(reply)
                    print(reply)

                request = self.serializer.send_protocol('END','END')
                binder_socket.send(request)
                binder_socket.close()

            self.queue = Queue()
            print("\n>> Server Online!\n")

        except OSError:
            self.online()

    def service(self, service_socket: socket.socket) -> None:
        try:                 
                service_socket.listen(5)

                connetion, address = service_socket.accept()

                print(f"Service request from {address}")
                Thread(target=self.processing, args=(connetion, address)).start()

        except:
            pass

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
    