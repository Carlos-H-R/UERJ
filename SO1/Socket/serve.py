import socket
import math

from time import sleep
from threading import Thread

class Server_Socket:
    
    def __init__(self, IP: str, PORT: int) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((IP,PORT))
        
        self.threads = dict()
        self.buffer = list()
        
    def active(self):
        self.server_socket.listen(5)

        print('Servidor ativo! Aguardando Conexões... ')

        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                
                print(f"Conexão estabelecida com {client_address}")
                t = Thread(target=self.process_data, args=(client_socket,))
                t.start()
                self.threads[t.getName()] = t


            except BaseException as error:
                print(error)

    def process_data(self, client: socket.socket):
        # lock = 10
        lock = 3
        
        while lock:
            try:
                messenge = client.recv(1024)
                messenge = messenge.decode('UTF-8')

                if messenge == 'kill':
                    lock = 0

                else:
                    result = self.calculator(messenge)
                    self.buffer.append(result)

                    client.send(result.encode('UTF-8'))
            
            except:
                # print("\nTimeout!\n")
                sleep(5)
                lock -= 1

    def calculator(self, expression):
        expression:list = expression.split()
        comand = str(expression.pop(0)).lower()
        expression = list(map(int, expression))
        
        if comand == 'soma':
            result = sum(expression)
            print(result)
            return str(f"A soma eh: {result}")
        
        elif comand == 'kill':
            self.kill()

        else:
            return str(f"O comando {comand} nao eh reconhecido")

    def close_server(self):
        for t in self.threads:
            if self.threads[t].is_alive():
                self.threads[t].join()

    def kill(self):
        for t in self.threads:
            self.threads[t].terminate()


if __name__ == "__main__":
    # ip = '10.10.1.61'
    ip = '192.168.1.47'
    port = 8080

    server = Server_Socket(ip, port)
    server.active()

    print(server.buffer)     
