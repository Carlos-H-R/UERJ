import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))


import socket

from threading import Thread
from rpc.serializer import serializer


class binder:
    def __init__(self, ip = '127.0.0.1', port = 8080):
        # create the class and it's initial attributes
        self.binder_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.binder_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.binder_socket.bind((ip,port))

        self.serializer = serializer()
        self.services = dict()

    def binder_handler(self, connection: socket.socket):
        handling = True
        while handling:
            try:
                request_protocol = connection.recv(4096)
                protocol = self.serializer.received_protocol(request_protocol)
            
                if protocol[0] == 'REGISTER':
                    service_name: str = protocol[1]
                    ip: str = protocol[2]
                    port: int = int(protocol[3])

                    self.services[service_name] = (ip, port)
                    print(service_name, self.services[service_name])
                    reply = self.serializer.serialize_obj('Sucessfully registered!')

                    connection.send(reply)
                    print('--> New service registered!')
            
                elif protocol[0] == 'LOOKUP':
                    service_name = protocol[1]
                    print(service_name)

                    try:
                        service_address = self.services[service_name]
                        # connection.send(self.serializer.serialize_obj('|'.join(service_address)))
                        connection.send(self.serializer.serialize_obj(service_address))

                    except KeyError:
                        # serviço não disponivel
                        connection.send(self.serializer.serialize_obj(0))

                    handling = False

                elif protocol[0] == 'END':
                    connection.close() # Ainda a definir se o socket sera encerrado
                    handling = False

                else:
                    connection.send(b'Unknown Protocol!')

            except:
                pass

    def start_binder(self) -> None:
        # inicialize the binder
        self.binder_socket.settimeout(5)
        self.binder_socket.listen(5)
        self.alive = True

        print('Binder Online ... ')

        while self.alive:
            try:
                connection, address = self.binder_socket.accept()
                print(f"\nRequest received from {address}")

                Thread(target=self.binder_handler, args=(connection,)).start()

            except KeyboardInterrupt:
                self.binder_socket.close()
                self.alive = False

            except socket.timeout:
                continue

        print('Binder Offline ... ')
        self.binder_socket.close()

if __name__ == "__main__":
    binder().start_binder()
    