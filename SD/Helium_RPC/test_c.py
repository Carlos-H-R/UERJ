from rpc.rpc_stub_generator import rpc_stub_generator 

math_stub = rpc_stub_generator()

result = math_stub.add(15,4)
print(f"O resultado é {result}")
