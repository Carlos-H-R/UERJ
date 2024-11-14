import socket
import math

from threading import Thread

class Server_Socket:
    
    def __init__(self, IP: str, PORT: int) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((IP,PORT))
        
    def active(self):
        self.server_socket.listen(5)

        print('Servidor ativo! Aguardando Conexões... ')

        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                
                print(f"Conexão estabelecida com {client_address}")
                Thread(target=self.process_data, args=(client_socket,))


            except:
                print("\n\nErro!\n\n")

    def process_data(self, client: socket.socket):
        try:
            messenge = client.recv(1024)
            messenge = messenge.decode('UTF-8')

            result = self.calculator(messenge)

            client.send(result)
        
        except:
            print("\nTimeout!\n")

    def calculator(self, expression):
        expression:list = expression.split()
        comand = str(expression.pop(0)).lower()
        expression = list(map(int, expression))
        
        if comand == 'soma':
            result = sum(expression)
            print(result)
            return f"A soma eh: {result}"

        else:
            return f"O comando {comand} nao eh reconhecido"


if __name__ == "__main__":
    ip = '10.10.1.61'
    port = 8080

    server = Server_Socket(ip, port)
    server.active()
                
