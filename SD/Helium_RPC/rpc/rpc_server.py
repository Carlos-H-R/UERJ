import socket
import time

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

        # self.alive = True
        self.service_provider = dict()
        self.serializer = serializer()
        self.calculator = math_service()
    
    def online(self, binder_ip = '127.0.0.1', binder_port = 8080) -> None:
        # connect the server and register services   
        
        try:    
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as binder_socket:
                # binder_socket.bind(('127.0.0.1',8071))
                binder_socket.connect((binder_ip,binder_port))
                
                for service_name in self.calculator.services:
                    service_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    service_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    service_socket.bind((self.IP,0))
                    
                    address = service_socket.getsockname()
                    
                    Thread(target=self.service, args=(service_socket, )).start()
                    
                    # Armazena o socket de serviço, não a thread. Isso pode ser útil para gerenciamento futuro.
                    self.service_provider[service_name] = service_socket

                    request = self.serializer.send_protocol('REGISTER', service_name, address[0], str(address[1]))
                    binder_socket.sendall(request)

                    reply = binder_socket.recv(4096)
                    reply = self.serializer.unserialize(reply)
                    print(reply)

                request = self.serializer.send_protocol('END','END')
                binder_socket.sendall(request)
                binder_socket.close()

            self.queue = Queue()
            print("\n>> Server Online!\n")

        except OSError as error:
            print(f"Erro ao iniciar o servidor ou conectar ao binder: {error}")
            raise

    def service(self, service_socket: socket.socket) -> None:
        try:                 
            service_socket.listen(5)
            
            while True: 
                service_socket.settimeout(5)
                try:
                    connection, address = service_socket.accept()
                    Thread(target=self.processing, args=(connection, address)).start()
                    print(f"Requisição de serviço de {address} na porta {service_socket.getsockname()[1]}")

                except socket.timeout:
                    continue
            
        except Exception as e: 
            print(f"Erro na thread de escuta do serviço: {e}")
            # Depois tratar mecanismo de parada para as threads

        finally:
            service_socket.close()

    def processing(self, connection: socket.socket, address):
        try:
            # Recebe a requisição do cliente
            request_bytes: bytes = connection.recv(8192) 
            if not request_bytes: # Se a conexão foi fechada ou nenhum dado foi recebido
                print(f"Cliente {address} desconectou ou enviou dados vazios.")
                connection.close()
                return None

            request_dict: dict = self.serializer.unserialize(request_bytes)

            func_name = request_dict['function']
            x = request_dict['x']
            y = request_dict['y']

            method = self.calculator.services[func_name]
            result = method(x,y) # Calcula o resultado

            response_bytes = self.serializer.serialize_obj(result)
            connection.sendall(response_bytes) 

            connection.close() # Fecha a conexão após enviar a resposta

        except KeyError as e:
            print(f"Erro: Função '{e}' não encontrada para o cliente {address}.")
            error_message = self.serializer.serialize_obj(f"Erro no servidor: Função '{e}' não encontrada.")
            connection.sendall(error_message)
            connection.close()

        except Exception as e: # Captura todas as outras exceções durante o processamento da RPC
            print(f"Erro durante o processamento RPC para o cliente {address}: {e}")
            error_message = self.serializer.serialize_obj(f"Erro interno do servidor: {e}")
            connection.sendall(error_message)
            connection.close()

    def offline(self) -> None:
        # stop the server
        self.queue.put(False)
    