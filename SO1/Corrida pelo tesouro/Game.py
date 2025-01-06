import socket

from time import sleep
from threading import Thread
from threading import BoundedSemaphore
from multiprocessing import Pipe

from model.Maps import Main_Map
from model.Player import Player



class GameServer():
    """
    # Classe GameServer

    A classe GameServer implementa os mecanismos internos do jogo. 
    Também responsável pelo controle de concorrência, regiões críticas, sincronização e comunicações

    -> Gerencia o estado do jogo\n
    -> Implementa o Mapa\n
    -> Recebe os comandos dos jogadores\n
    -> Transimite o estado do jogo aos jogadores

    """
    __active__: BoundedSemaphore
    __max_players__ = 1
    __status__ = dict()
    __threads__ = dict()
    __connections__ = dict()
    package_buffer = []

    def __init__(self, IP, PORT) -> None:
        self.ip = IP
        self.port = PORT

        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind((self.ip, self.port))
        
        self.__active__ = BoundedSemaphore(1)

    def start(self, max_players):
        self.__updating__ = BoundedSemaphore(1)

        self.__max_players__ = max_players
        self.__map__ = Main_Map(30, 30, 50, 9)
        
        self.listening()
        Thread(target=self.send_updated_state).start()
        Thread(target=self.update_state).start()

    def listening(self) -> None:
        """ 
        Faz com que o Servidor esteja pronto para receber novas conexões\n
        Cada nova conexão é atribuida a uma Thread
        """
        
        self.socket_server.listen(10)
        print("Aguardando conexões... \n")

        while self.__threads__.__len__() < self.__max_players__:
            try:
                client, address = self.socket_server.accept()
                client.send(b'Aguarde o Jogo comecar ... ')

                print(f"Conexão estabelecida com {address}")
                self.__status__[address] = BoundedSemaphore(1)
                self.__threads__[address] = Thread(target=self.new_connection, args=(address,))
                self.__connections__[address] = client

            except BaseException as error:
                print(error)

        for id in self.__threads__.keys():
            self.__threads__[id].start()

    def update_state(self):
        """
        Checa o buffer e atualiza o estado do jogo
        """

        while self.__active__._value:
            self.__updating__.acquire()

            try:
                id, command = self.package_buffer.pop(0)
                room = self.__map__.__players__[id].getRoom()

                if room == 0:
                    self.__map__.move(id, command)

                else:
                    self.__map__.treasure_rooms[room].move(id, command)

            except IndexError:
                sleep(0.3)

            self.__updating__.release()

    def send_updated_state(self) -> None:
        """
        Verifica o estado do jogo e envia as informações para os jogadores
        """

        while self.__active__._value:
            self.__updating__.acquire()

            for id in self.__connections__.keys():
                player: Player = self.__map__.__players__[id]

                player_points = player.getPoints()
                player_room = player.getRoom()
                player_position = player.getPosition()

                if player_room == 0:
                    player_map = self.__map__.showMap()

                else:
                    player_map = self.__map__.treasure_rooms[player_room].showMap()

                package = str((player_points,player_room,player_position,player_map)).encode('utf-8')
                self.__connections__[id].send(package)

            self.__updating__.release()
            sleep(0.1)

    def new_connection(self, address) -> None:
        self.new_player(address)
        
        while self.__active__._value and self.__status__[address]:
            try:
                print('try')
                package = self.__connections__[address].recv(1024)
                print('recieved')
                print(package.decode())
                self.package_buffer.append((address,package))

            except BaseException as error:
                print(error)

    def new_player(self, id) -> None:
        self.__map__.new_player(id)

    def quit_game(self):
        print("Fechando o Jogo! ... ")
        self.__active__.acquire()


if __name__ == "__main__":
    IP = '192.168.1.47'
    PORT = 8080
    
    game = GameServer(IP, PORT)
    game.start(1)
