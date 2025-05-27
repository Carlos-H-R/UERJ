import socket
import time

from queue import Queue
from threading import Thread

from rpc.serializer import serializer
from interface.math_service import math_service


class rpc_server:
    """
    Gerencia a comunicação do servidor RPC, registra serviços com um "binder"
    e processa requisições de clientes.
    """
    def __init__(self, ip: str = '127.0.0.1', port: int = 8070):
        """
        Inicializa o servidor RPC, configurando o socket e instanciando
        o serializador e o serviço de calculadora.

        Args:
            ip (str, optional): O endereço IP do servidor. Padrão para '127.0.0.1'.
            port (int, optional): A porta do servidor. Padrão para 8070.
        """
        self.IP = ip
        self.PORT = port

        self.server_socker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socker.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socker.bind((ip,port))        

        self.service_provider = dict()
        self.serializer = serializer()
        self.calculator = math_service()
    
    def online(self, binder_ip: str = '127.0.0.1', binder_port: int = 8080) -> None:
        """
        Conecta o servidor ao "binder" (serviço de registro) e registra
        todos os serviços disponíveis (`math_service`). Cada serviço é executado
        em uma thread separada para lidar com as requisições.

        Args:
            binder_ip (str, optional): Endereço IP do "binder". Padrão para '127.0.0.1'.
            binder_port (int, optional): Porta do "binder". Padrão para 8080.

        Raises:
            OSError: Levantada se houver um erro ao iniciar o servidor ou conectar ao "binder".
        """
        
        try:    
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as binder_socket:
                binder_socket.connect((binder_ip,binder_port))
                
                for service_name in self.calculator.services:
                    # Cria um socket para cada serviço e o bind a uma porta dinâmica (0)
                    service_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    service_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    service_socket.bind((self.IP,0)) # Porta 0 para que o SO escolha uma porta livre
                    
                    address = service_socket.getsockname()
                    
                    # Inicia uma thread para cada serviço escutar conexões
                    Thread(target=self.service, args=(service_socket, )).start()
                    
                    # Armazena o socket de serviço. Isso pode ser útil para gerenciamento futuro.
                    self.service_provider[service_name] = service_socket

                    # Envia a requisição de registro para o binder
                    request = self.serializer.send_protocol('REGISTER', service_name, address[0], str(address[1]))
                    binder_socket.sendall(request)

                    # Recebe a resposta do binder
                    reply = binder_socket.recv(4096)
                    reply = self.serializer.unserialize(reply)
                    print(reply)

                # Envia um comando 'END' para o binder para indicar que o registro terminou
                request = self.serializer.send_protocol('END','END')
                binder_socket.sendall(request)
                binder_socket.close()

            self.queue = Queue() # Usado para sinalização de parada (ainda a ser totalmente implementado)
            print("\n>> Server Online!\n")

        except OSError as error:
            print(f"Erro ao iniciar o servidor ou conectar ao binder: {error}")
            raise

    def service(self, service_socket: socket.socket) -> None:
        """
        Método que executa em uma thread separada para cada serviço.

        Ele escuta por conexões de clientes no socket de serviço e inicia
        uma nova thread para processar cada requisição recebida.

        Args:
            service_socket (socket.socket): O socket específico para este serviço.
        """
        try:                 
            service_socket.listen(5) # Habilita o socket a aceitar conexões
            
            while True: 
                service_socket.settimeout(5) # Define um timeout para accept
                try:
                    connection, address = service_socket.accept()
                    # Inicia uma nova thread para processar a requisição do cliente
                    Thread(target=self.processing, args=(connection, address)).start()
                    print(f"Requisição de serviço de {address} na porta {service_socket.getsockname()[1]}")

                except socket.timeout:
                    # Continua o loop se não houver conexões no tempo limite
                    continue
                except Exception as e:
                    print(f"Erro ao aceitar conexão ou iniciar thread de processamento: {e}")
                    break # Quebra o loop em caso de erro grave
            
        except Exception as e: 
            print(f"Erro na thread de escuta do serviço: {e}")
            # TODO: Adicionar mecanismo de parada para as threads de serviço
        finally:
            service_socket.close() # Garante que o socket seja fechado ao sair

    def processing(self, connection: socket.socket, address: tuple):
        """
        Processa uma requisição RPC recebida de um cliente.

        Deserializa a requisição, chama o método apropriado da `math_service`
        e envia o resultado de volta ao cliente.

        Args:
            connection (socket.socket): O objeto de conexão do cliente.
            address (tuple): O endereço do cliente (IP, Porta).
        """
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
        """
        Sinaliza para o servidor parar.
        (Mecanismo de parada ainda a ser totalmente implementado para todas as threads.)
        """
        self.queue.put(False) # Usa uma fila para sinalizar a parada.
        print("Server signaled to go offline.")

