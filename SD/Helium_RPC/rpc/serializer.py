import pickle


class serializer:
    def __init__(self) -> None:
        pass

    def serialize_obj(self, object) -> bytes:
        bytes_obj = pickle.dumps(object)
        return bytes_obj

    def serialize(self, *args) -> bytes:
        message = list(args)
        return pickle.dumps(message)

    def unserialize(self, message: bytes):
        arguments = pickle.loads(message)
        return arguments

    def send_protocol(self, 
                      command: str, 
                      sercive_name: str, 
                      ip: str = None, 
                      port: int = None
                      ) -> bytes:
        
        if (ip == None) or (port == None):
            protocol = '|'.join([command, sercive_name])
            return pickle.dumps(protocol)

        else:
            protocol = '|'.join([command, sercive_name, ip, port])
            return pickle.dumps(protocol)

    def received_protocol(self, b_protocol: bytes) -> list:
        protocol: str = pickle.loads(b_protocol)
        return protocol.split('|')
