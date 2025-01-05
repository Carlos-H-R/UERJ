import socket


class ClientSocket:
    def __init__(self, IP, PORT) -> None:
        self.ip = IP
        self.port = PORT
        self.__socket_client__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket_client__.connect((IP,PORT))

    def set_address(self, IP, PORT):
        # altera o endereço IP e a porta
        self.__socket_client__.close()
        self.ip = IP
        self.port = PORT
        self.__socket_client__.connect()

    def reconect(self):
        # check conection
        # check ping
        self.__socket_client__.connect((self.ip,self.port))

    def disconect(self):
        # global self.__active__
        self.__socket_client__.close()

    def listening(self):
        # monitora a chegada de pacotes decodifica e armazena em buffer
        self.__active__ = True
        self.__message_buffer__ = []

        while self.__active__:
            try: 
                package = self.__socket_client__.recv(1024)
                self.__message_buffer__.append(package.decode('utf-8'))
                
            except:
                print('Tratar exceção')

    def send(self, message: str):
        # metodo que envia para o servidor os comandos processados pelo cliente
        self.package = message.encode('utf-8')
        self.__socket_client__.send(self.package)
        print('sent')

    def receive(self) -> str:
        # metodo que retorna dados decodificado no buffer 
        try:
            data = self.__message_buffer__.pop(0)
            return data
        
        except IndexError:
            print("\nEmpty buffer... ")
    

if __name__ == "__main__":
    IP = '192.168.1.47'
    PORT = 8080

    c = ClientSocket(IP, PORT)

    c.send('Oi')
