# Gerador de Stubs Dinamico

from rpc.rpc_client import rpc_client

class rpc_stub_generator:
    def  __init__(self) -> None:
        self._client = rpc_client()

    def __getattr__(self, _name: str):
        """Metodo do Stub_Generator que gera novos metodos"""

        def remote_call(x: int, y: int):
            return self._client.call(_name, x, y)
        
        return remote_call
    