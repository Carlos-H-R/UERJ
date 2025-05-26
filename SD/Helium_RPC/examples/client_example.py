from rpc.rpc_stub_generator import rpc_stub_generator


if __name__ == "__main__":
    math_stub = rpc_stub_generator()

    print("Resultado de 5 + 3", math_stub.add(5,3))
    print("Resultado de 4 * 2", math_stub.multiply(4,2))
    print("Resultado de 5 - 3", math_stub.sub(5,3))
    print("Resultado de 4 / 2", math_stub.divide(4,2))
