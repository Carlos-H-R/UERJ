import socket
import time

from rpc.serializer import serializer


class rpc_client:
    """
    Gerencia a conexão com o 'binder' para descobrir serviços e a comunicação
    com os servidores de serviço para executar chamadas de procedimento remoto.
    """
    def __init__(self, ip: str = '127.0.0.1', port: int = 8060) -> None:
        """
        Inicializa o cliente RPC, configurando o socket e instanciando o serializador.

        Args:
            ip (str, optional): O endereço IP do cliente. Padrão para '127.0.0.1'.
            port (int, optional): A porta do cliente. Padrão para 8060.
        """
        self.serializer = serializer()

        # O cliente não precisa de bind a menos que precise de uma porta específica
        # para comunicação de retorno ou para ser identificado pelo binder.
        # Para chamadas de saída, geralmente um bind automático é suficiente.
        # Se for para um cenário onde o binder precisa se conectar de volta ao cliente,
        # então o bind é necessário. Por simplicidade, vou manter como estava.
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.bind((ip, port))


    def connect_to_binder(self, protocol: bytes, binder_IP: str, binder_PORT: int) -> tuple | None:
        """
        Conecta-se ao 'binder' para enviar um protocolo (geralmente uma requisição de LOOKUP)
        e recebe a resposta do 'binder'.

        Args:
            protocol (bytes): O protocolo serializado a ser enviado ao 'binder'.
            binder_IP (str): O endereço IP do 'binder'.
            binder_PORT (int): A porta do 'binder'.

        Returns:
            tuple | None: O endereço do servidor de serviço (tupla IP, Porta) se a conexão
                          for bem-sucedida e o serviço for encontrado, `None` caso contrário.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as binder_socket:
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

    def call(self, method: str, x: int, y: int) -> int | None:
        """
        Realiza uma chamada de procedimento remoto para um método específico com os argumentos `x` e `y`.

        Primeiro, solicita o endereço do serviço ao 'binder' e, em seguida,
        envia a requisição para o servidor de serviço.

        Args:
            method (str): O nome do método a ser chamado remotamente.
            x (int): O primeiro argumento para o método remoto.
            y (int): O segundo argumento para o método remoto.

        Returns:
            int | None: O resultado da chamada RPC ou `None` se o serviço não estiver
                        disponível ou ocorrer um erro.
        """
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

                result_bytes = service_socket.recv(8192)
                if not result_bytes:
                    print(f"No data received from service server {server_address}")
                    return None

                result = self.serializer.unserialize(result_bytes)
                return result
        
        except ConnectionRefusedError:
            print(f"Conexão recusada pelo servidor {server_address}")
            return None
        
        except Exception as error:
            print(f"Erro durante chamada {method} no servidor {server_address}: {error}")
            return None

    def disconect(self) -> None:
        """
        Finaliza o enlace e fecha o socket.
        (Atualmente sem implementação detalhada, apenas um placeholder.)
        """
        print("Client disconnected.")
        # self.client_socket.close() # Implementação real de desconexão

