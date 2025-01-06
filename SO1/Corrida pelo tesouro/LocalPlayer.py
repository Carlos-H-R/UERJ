import socket
import keyboard

from time import sleep
from threading import Thread
from threading import BoundedSemaphore
from multiprocessing import Pipe

from model.Screen import Screen
from model.Player import Player

class LocalPlayer():
    def __init__(self, IP, PORT) -> None:
        self.ip = IP
        self.port = PORT

        self.__socket_client__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__active__ = BoundedSemaphore(1)

        try:
            self.__socket_client__.connect((IP,PORT))
            print("Conexão com o servidor estabelecida com sucesso!\n")

        except BaseException as error:
            print(error)

    def start(self) -> None:
        # self.f = open('local_log.txt', 'w')
        entry, recieve = Pipe()
        out, send = Pipe()
        
        self.__player__ = Player()
        self.__screen__ = Screen()
        self.entry = entry
        self.out = out
        self.send = send

        message = self.__socket_client__.recv(1024)
        self.__screen__.output(message.decode('utf-8'))

        Thread(target=self.listening, args=(recieve,)).start()
        Thread(target=self.process).start()
        Thread(target=self.listening_keyboard).start()
        Thread(target=self.sending).start()

    def listening(self, recieve):

        while self.__active__._value:
            try: 
                package = self.__socket_client__.recv(1024).decode('utf-8')
                recieve.send(package)
                
            except BaseException as error:
                print(error)
    
    def sending(self):
        while self.__active__._value:
            try: 
                message = self.out.recv()
                self.__socket_client__.send(message.encode('utf-8'))
                
            except EOFError:
                sleep(0.3)
 
    def update_info(self):
        # recebe os pacotes do servidor e atualiza as informações do cliente
        self.__clientConection__.receive()

    def listening_keyboard(self):
        # observa os eventos de teclado e processa a entrada
        while self.__active__._value:
            keyboard.on_press(self.move)
            sleep(0.2)
    
    def process(self) -> None:
        """ Metodo que processa dados decodificado no buffer """
        while self.__active__._value:
            try:
                data = self.entry.recv()
                self.__screen__.output(data)
            
            except IndexError:
                # print("\nEmpty buffer... ", file=self.f)
                sleep(0.4)

    def move(self, event: keyboard.KeyboardEvent):
        # ao receber um evento de teclado processa e define a mensagem a ser enviada ao servidor
        key = event.scan_code

        if keyboard.key_to_scan_codes('p') == key or keyboard.key_to_scan_codes('P') == key:
            message = 'quit'

        elif keyboard.key_to_scan_codes('w') == key or keyboard.key_to_scan_codes('W') == key:
            message = 'up'

        elif keyboard.key_to_scan_codes('s') == key or keyboard.key_to_scan_codes('S') == key:
            message = 'down'

        elif keyboard.key_to_scan_codes('a') == key or keyboard.key_to_scan_codes('A') == key:
            message = 'left'

        elif keyboard.key_to_scan_codes('d') == key or keyboard.key_to_scan_codes('D') == key:
            message = 'right'

        else:
            message = ''

        self.send.send(message)


if __name__ == "__main__":
    # ip = str(input('Insira o IP: '))
    # port = int(input('Insira a porta: '))

    ip = '192.168.1.47'
    port = 8080

    l = LocalPlayer(ip, port)
    l.start()
