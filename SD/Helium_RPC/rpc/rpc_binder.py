import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))


import socket

from threading import Thread
from rpc.serializer import serializer


class binder:
    """
    O 'binder' é o componente central do sistema RPC que gerencia o registro
    e a localização de serviços.
    """
    def __init__(self, ip: str = '127.0.0.1', port: int = 8080):
        """
        Inicializa o 'binder', configurando seu socket e instanciando o serializador.

        Args:
            ip (str, optional): O endereço IP do 'binder'. Padrão para '127.0.0.1'.
            port (int, optional): A porta do 'binder'. Padrão para 8080.
        """
        # create the class and it's initial attributes
        self.binder_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.binder_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.binder_socket.bind((ip,port))

        self.serializer = serializer()
        self.services = dict()
        self.alive = False  # Estado para controlar o ciclo de vida do binder

    def binder_handler(self, connection: socket.socket):
        """
        Lida com as requisições de um cliente ou servidor conectado ao 'binder'.

        Processa comandos `REGISTER` (para servidores) e `LOOKUP` (para clientes).

        Args:
            connection (socket.socket): O objeto de conexão do cliente/servidor.
        """
        handling = True
        while handling:
            try:
                request_protocol = connection.recv(4096)
                if not request_protocol: # Conexão fechada pelo cliente
                    break
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
                    print(f"LOOKUP request for service: {service_name}")

                    try:
                        service_address = self.services[service_name]
                        connection.send(self.serializer.serialize_obj(service_address))
                        print(f"Service {service_name} found at {service_address}")

                    except KeyError:
                        # serviço não disponivel
                        print(f"Service {service_name} not found.")
                        connection.send(self.serializer.serialize_obj(0))

                    handling = False # Após um LOOKUP, a conexão pode ser fechada
                                     # ou manter-se aberta dependendo do protocolo
                                     # Aqui, é fechada.

                elif protocol[0] == 'END':
                    connection.close()
                    handling = False
                    print('--> Connection ended by client.')

                else:
                    connection.send(b'Unknown Protocol!')
                    print(f"Unknown protocol received: {protocol[0]}")

            except ConnectionResetError:
                print("Client disconnected unexpectedly.")
                handling = False
            except Exception as e:
                print(f"Error in binder_handler: {e}")
                handling = False
        connection.close()


    def start_binder(self) -> None:
        """
        Inicializa o 'binder', colocando-o em modo de escuta por conexões.

        Cada nova conexão é tratada em uma thread separada.
        """
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
                print("\nKeyboardInterrupt detected. Shutting down binder...")
                self.alive = False
            except socket.timeout:
                continue
            except Exception as e:
                print(f"An unexpected error occurred in start_binder: {e}")
                self.alive = False # Pode ser uma boa ideia parar em caso de erro crítico

        print('Binder Offline ... ')
        self.binder_socket.close()

if __name__ == "__main__":
    binder().start_binder()

