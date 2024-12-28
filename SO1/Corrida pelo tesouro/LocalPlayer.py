import keyboard

from time import sleep
from threading import BoundedSemaphore

from model.Player import Player
from controler.client import ClientSocket

class LocalPlayer(Player):
    def start(self) -> None:
        try:
            ip = str(input('Insira o IP: '))
            port = int(input('Insira a porta: '))

            self.__clientConection__ = ClientSocket(ip, port)
            self.__active__ = BoundedSemaphore()

        except ConnectionRefusedError:
            print("\nServidor fechado! ")

    def update_info(self):
        # recebe os pacotes do servidor e atualiza as informações do cliente
        self.__clientConection__.receive()

    def listenig_keyboard(self):
        # observa os eventos de teclado e processa a entrada
        while self.__active__._value:
            keyboard.on_press(self.move)
            sleep(0.2)

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

        self.__clientConection__.send(message.encode())


if __name__ == "__main__":
    l = LocalPlayer().start()