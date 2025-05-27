import pickle


class serializer:
    """
    Fornece métodos para converter objetos Python em bytes e vice-versa,
    além de gerenciar um formato de protocolo de comunicação.
    Utiliza o módulo `pickle` para serialização e desserialização.
    """
    def __init__(self) -> None:
        """
        Construtor da classe Serializer.
        (Atualmente sem inicialização específica).
        """
        pass

    def serialize_obj(self, obj: object) -> bytes:
        """
        Serializa um objeto Python em uma sequência de bytes.

        Args:
            obj (object): O objeto a ser serializado.

        Returns:
            bytes: A representação em bytes do objeto.
        """
        bytes_obj = pickle.dumps(obj)
        return bytes_obj

    def serialize(self, *args) -> bytes:
        """
        Serializa múltiplos argumentos em uma lista de bytes.

        Args:
            *args: Argumentos variáveis a serem serializados.

        Returns:
            bytes: A representação em bytes da lista de argumentos.
        """
        message = list(args)
        return pickle.dumps(message)

    def unserialize(self, message_bytes: bytes):
        """
        Desserializa uma sequência de bytes de volta para um objeto Python.

        Args:
            message_bytes (bytes): A sequência de bytes a ser desserializada.

        Returns:
            Any: O objeto Python desserializado.
        """
        arguments = pickle.loads(message_bytes)
        return arguments

    def send_protocol(self, 
                      command: str, 
                      service_name: str, 
                      ip: str | None = None, 
                      port: str | int | None = None
                      ) -> bytes:
        """
        Constrói um protocolo de comunicação baseado em comando, nome do serviço,
        IP e porta (opcionalmente). O protocolo é uma string formatada
        ('COMMAND|SERVICE_NAME|IP|PORT' ou 'COMMAND|SERVICE_NAME') e serializada.

        Args:
            command (str): O comando do protocolo (ex: 'REGISTER', 'LOOKUP', 'END').
            service_name (str): O nome do serviço.
            ip (str | None, optional): O endereço IP (para registro). Padrão para None.
            port (str | int | None, optional): A porta (para registro). Padrão para None.

        Returns:
            bytes: O protocolo serializado.
        """
        
        if (ip is None) or (port is None):
            protocol = '|'.join([command, service_name])
            return pickle.dumps(protocol)

        else:
            protocol = '|'.join([command, service_name, ip, str(port)]) # type: ignore
            return pickle.dumps(protocol)

    def received_protocol(self, b_protocol: bytes) -> list:
        """
        Desserializa um protocolo de bytes e o divide em uma lista de strings.

        Args:
            b_protocol (bytes): O protocolo em formato de bytes.

        Returns:
            list: Uma lista de strings representando as partes do protocolo.
        """
        protocol: str = pickle.loads(b_protocol)
        return protocol.split('|')

