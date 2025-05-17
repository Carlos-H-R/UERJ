import socket

from serializer import serializer


class binder:
    def __init__(self, ip = 'http://localhost', port = 8080):
        # create the class and it's initial attributes
        self.binder_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.binder_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.binder_socket.bind((ip,port))

        self.serializer = serializer()

        self.services = dict()

    def start_binder(self):
        # inicialize the binder
        self.binder_socket.listen(5)

        while True:
            connection, address = self.binder_socket.accept()
            print(f"Request received from {address}")

            request_protocol = connection.recv(1024)

            protocol = self.serializer.received_protocol(request_protocol)

            if protocol[0] == 'REGISTER':
               service_name: str = protocol[1]
               ip: str = protocol[2]
               port: int = protocol[3]

               self.services[service_name] = (ip, port)

               connection.send(b'Sucessfully registered!')

           
            elif protocol[0] == 'LOOKUP':
                service_name = protocol[1]

                try:
                    service_address = self.services[service_name]
                    
                    connection.send(self.serializer.serialize_obj(service_address))


                except KeyError:
                    # serviço não disponivel
                    connection.send(b'Service Unavaliable!')


            else:
                connection.send(b'Unknown Protocol!')

            connection.close()
    