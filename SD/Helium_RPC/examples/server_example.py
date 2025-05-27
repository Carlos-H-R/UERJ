import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from rpc.rpc_server import rpc_server

def main():
    """
    Inicia o servidor RPC.

    Cria uma instância de `rpc_server` e a coloca online,
    registrando os serviços de matemática com o binder.
    """
    rpc_server().online()

if __name__ == "__main__":
    main()

