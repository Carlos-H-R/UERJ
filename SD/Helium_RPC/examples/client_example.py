import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from rpc.rpc_stub_generator import rpc_stub_generator


def main():
    """
    Exemplo de uso do cliente RPC para realizar operações matemáticas remotas.

    Cria um stub para os serviços de matemática e demonstra
    chamadas de adição, multiplicação, subtração e divisão.
    """
    math_stub = rpc_stub_generator()

    print("Resultado de 5 + 3:", math_stub.add(5, 3))
    print("Resultado de 4 * 2:", math_stub.multiply(4, 2))
    print("Resultado de 5 - 3:", math_stub.sub(5, 3))
    print("Resultado de 4 / 2:", math_stub.divide(4, 2))


if __name__ == "__main__":
    main()

