import socket

from threading import Thread


class ServerSocket:
    def __init__(self, IP, PORT) -> None:
        self.ip = IP
        self.port = PORT

        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        # Verifica dados persistidos
        # Realiza checagens 
        # Inicia scrypts relacionado a logica do jogo
        # Inicia a conexão
        # Delega funcoes

        self.socket_server.bind((self.ip, self.port))
        self.listening()

    def save(self):
        # armazena o estado do jogo
        pass

    def stop(self):
        # Finaliza as Threads 
        # Encerra as conexões 
        # Persiste o q for necessario
        # Realiza verificação do servidor
        # Encerra o socket
        # Libera recursos restantes

        self.socket_server.close()

    def listening(self):
        # Passa a esperar novas conexões e atribui uma thread a essa conexão
        self.socket_server.listen(10)
        client, address = self.socket_server.accept()
        print(address)

        m = client.recv(1024).decode()
        print(m)


if __name__ == "__main__":
    IP = '192.168.1.47'
    PORT = 8080

    s = ServerSocket(IP, PORT)
    s.start()
