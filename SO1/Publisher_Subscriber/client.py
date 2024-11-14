import socket

class Client_Socket:
    
    def __init__(self, IP, PORT) -> None:
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((IP,PORT))

    def enviar(self):
        self.messenge = str(input('Insira a mensagem: '))
        self.messenge = self.messenge.encode('UTF-8')
        self.socket_client.send(self.messenge)

        print('\nMensagem Enviada!')


if __name__ == "__main__":
    # ip = '10.10.1.106'
    ip = '10.10.1.61'
    port = 8080
    client = Client_Socket(ip, port)

    lock = True
    while lock:
        print("1 - enviar mensagem \n0 - encerrar")
        entry = input('\n>> ')

        try:
            entry = int(entry)
            if entry == 1:
                client.enviar()

            elif entry == 0:
                print('\n\nComando não reconhecido! \n\n')
                lock = False

        except:
            print('\n\nO comando deve ser um numero! \n\n')

