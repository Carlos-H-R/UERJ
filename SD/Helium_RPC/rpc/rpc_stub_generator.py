# Gerador de Stubs Dinamico

from rpc.rpc_client import rpc_client

class rpc_stub_generator:
    """
    Classe que atua como um gerador de stubs dinâmico para chamadas RPC.

    Permite que clientes façam chamadas a métodos remotos de forma transparente,
    como se estivessem chamando métodos locais. Ele intercepta chamadas de método
    e as roteia para o `rpc_client`.
    """
    def __init__(self) -> None:
        """
        Inicializa o gerador de stubs, criando uma instância de `rpc_client`.
        """
        self._client = rpc_client()

    def __getattr__(self, _name: str):
        """
        Método mágico invocado quando um atributo (método) não é encontrado no objeto.

        Ele dinamicamente gera uma função `remote_call` que, por sua vez, usa o
        `rpc_client` para chamar o método remoto com o nome `_name`.

        Args:
            _name (str): O nome do método remoto que foi acessado.

        Returns:
            Callable: Uma função (`remote_call`) que encapsula a chamada RPC para o método remoto.
        """

        def remote_call(x: int, y: int):
            """
            Função interna gerada para realizar a chamada remota.

            Args:
                x (int): O primeiro argumento para o método remoto.
                y (int): O segundo argumento para o método remoto.

            Returns:
                Any: O resultado da chamada RPC.
            """
            return self._client.call(_name, x, y)
        
        return remote_call

