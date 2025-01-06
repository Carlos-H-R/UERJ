import socket

u = 'utf-8'

class Client_Socket:
    
    def __init__(self, IP, PORT) -> None:
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((IP,PORT))

    def send_messenge(self):
        self.messenge = str(input('Insira a mensagem: '))
        self.messenge = self.messenge.encode('UTF-8')
        self.socket_client.send(self.messenge)

        print('\nMensagem Enviada!')
        self.receive_messenge()

    def receive_messenge(self):
        answer = self.socket_client.recv(1024).decode(u)
        print(f"\nResposta >> {answer} \n")

    def end_connection(self):
        end = b'kill'
        self.socket_client.send(end)
        self.socket_client.close()


if __name__ == "__main__":
    # ip = '10.10.1.106'
    # ip = '10.10.1.61'
    ip = '192.168.1.47'
    port = 8080
    client = Client_Socket(ip, port)

    lock = True
    while lock:
        print("1 - enviar mensagem \n0 - encerrar")
        entry = input('\n>> ')

        try:
            entry = int(entry)
            if entry == 1:
                client.send_messenge()

            elif entry == 0:
                print("\n\nEncerrando...")
                client.end_connection()
                lock = False

            else:
                print('\n\nComando não reconhecido! \n\n')

        except:
            print('\n\nO comando deve ser um numero! \n\n')

