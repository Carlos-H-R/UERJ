import socket
import keyboard

from time import sleep
from threading import Thread, Event
from multiprocessing import Pipe
from model.Screen import Screen
from model.Player import Player

class LocalPlayer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.active = Event()
        self.active.set()

        try:
            self.socket_client.connect((self.ip, self.port))
            print("Conexão com o servidor estabelecida com sucesso!\n")
        except (ConnectionError, socket.error) as error:
            print(f"Erro ao conectar ao servidor: {error}")
            self.active.clear()

    def start(self):
        if not self.active.is_set():
            return

        self.entry, self.receive_pipe = Pipe()
        self.send_pipe, self.out = Pipe()

        self.screen = Screen()

        welcome_message = self.socket_client.recv(1024).decode("utf-8")
        self.screen.output(welcome_message)

        Thread(target=self.listen_to_server, daemon=True).start()
        Thread(target=self.process_messages, daemon=True).start()
        Thread(target=self.listen_to_keyboard, daemon=True).start()
        Thread(target=self.send_to_server, daemon=True).start()

    def listen_to_server(self):
        """Recebe mensagens do servidor e as envia para processamento."""
        while self.active.is_set():
            try:
                package = self.socket_client.recv(2048)
                if package:
                    self.receive_pipe.send(package.decode("utf-8"))

            except (ConnectionResetError, ConnectionAbortedError, socket.error) as error:
                print(f"Erro ao receber dados do servidor: {error}")
                self.active.clear()

    def send_to_server(self):
        """Envia mensagens do cliente para o servidor."""
        while self.active.is_set():
            try:
                if self.out.poll():
                    message = self.out.recv()
                    self.socket_client.send(message.encode("utf-8"))
            except (BrokenPipeError, EOFError, socket.error) as error:
                print(f"Erro ao enviar dados para o servidor: {error}")
                self.active.clear()

    def listen_to_keyboard(self):
        """Observa eventos de teclado e processa comandos do jogador."""
        keyboard.on_press(self.handle_key_event)
        while self.active.is_set():
            sleep(0.4)

    def process_messages(self):
        """Processa mensagens recebidas do servidor."""
        while self.active.is_set():
            try:
                if self.entry.poll():
                    map_data = self.entry.recv()

                    self.screen.clear()
                    self.screen.output(map_data)
                    sleep(0.8)

            except EOFError:
                sleep(0.4)

    def handle_key_event(self, event: keyboard.KeyboardEvent):
        """Converte eventos de teclado em comandos para o servidor."""
        key = event.name.lower()

        commands = {
            'p': 'quit',
            'w': 'up',
            's': 'down',
            'a': 'left',
            'd': 'right',
        }

        message = commands.get(key, '')
        if message:
            self.send_pipe.send(message)

    def stop(self):
        """Encerra todas as conexões e threads."""
        print("Encerrando o jogo...")
        self.active.clear()
        self.socket_client.close()

if __name__ == "__main__":
    ip = "192.168.1.47"
    port = 8080

    player = LocalPlayer(ip, port)
    try:
        player.start()
        while player.active.is_set():
            sleep(0.1)
    except KeyboardInterrupt:
        print("Finalizando o cliente...")
    finally:
        player.stop()
