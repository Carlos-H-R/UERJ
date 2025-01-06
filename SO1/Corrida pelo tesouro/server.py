import socket

from time import sleep
from threading import Thread, BoundedSemaphore
from model.Maps import Main_Map

class GameServer:
    """
    Classe GameServer
    Implementa os mecanismos internos do jogo, gerencia o estado do jogo,
    recebe comandos e transmite o estado atualizado aos jogadores.
    """

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind((self.ip, self.port))
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.active = True
        self.max_players = 1
        self.package_buffer = []
        self.players = {}
        self.threads = {}
        self.connections = {}
        self.map = None
        self.update_lock = BoundedSemaphore(1)

    def start(self, max_players):
        self.max_players = max_players
        self.map = Main_Map(10, 10, 10, 7)
        
        Thread(target=self.listening).start()
        Thread(target=self.send_updated_state, daemon=True).start()
        Thread(target=self.update_state, daemon=True).start()

    def listening(self):
        """
        Aceita conexões de novos jogadores e cria threads para gerenciá-los.
        """
        self.socket_server.listen(self.max_players)
        print("Aguardando conexões...")

        while len(self.threads) < self.max_players:
            try:
                client, address = self.socket_server.accept()
                client.send(b'Aguarde o jogo comecar...')
                print(f"Conexão estabelecida com {address}")

                self.players[address] = {"status": True}
                self.connections[address] = client

                thread = Thread(target=self.handle_connection, args=(address,))
                self.threads[address] = thread
                thread.start()
            except Exception as error:
                print(f"Erro ao aceitar conexão: {error}")

    def handle_connection(self, address):
        """
        Gerencia comunicação com um jogador.
        """
        self.new_player(address)
        client = self.connections[address]

        while self.active and self.players[address]["status"]:
            try:
                package = client.recv(1024)
                if package:
                    command = package.decode("utf-8")
                    self.package_buffer.append((address, command))
            except Exception as error:
                print(f"Erro na comunicação com {address}: {error}")
                self.players[address]["status"] = False

    def new_player(self, id):
        """
        Adiciona um novo jogador ao mapa.
        """
        self.map.new_player(id)

    def update_state(self):
        """
        Atualiza o estado do jogo com base nos comandos recebidos.
        """
        while self.active:
            self.update_lock.acquire()
            try:
                if self.package_buffer:
                    id, command = self.package_buffer.pop(0)
                    player_room = self.map.__players__[id].getRoom()

                    if player_room == 0:
                        self.map.move(id, command)
                    else:
                        self.map.treasure_rooms[player_room].move(id, command)

                    sleep(0.1)

            except IndexError:
                pass
            except Exception as error:
                print(f"Erro ao atualizar estado: {error}")
            finally:
                self.update_lock.release()
                sleep(0.1)

    def send_updated_state(self):
        """
        Envia o estado atualizado do jogo para todos os jogadores.
        """
        while self.active:
            self.update_lock.acquire()
            try:
                for id, client in self.connections.items():
                    if id in self.map.__players__:
                        player = self.map.__players__[id]
                        map_data = self.map.showMap() if player.getRoom() == 0 else self.map.treasure_rooms[player.getRoom()].showMap()
                    
                        client.send(map_data.encode("utf-8"))
                
                sleep(0.1)
                        
            except Exception as error:
                print(f"Erro ao enviar estado: {error}")
            finally:
                self.update_lock.release()
                sleep(0.1)

    def quit_game(self):
        """
        Encerra o servidor e desconecta todos os jogadores.
        """
        print("Encerrando o jogo...")
        self.active = False
        for client in self.connections.values():
            client.close()
        self.socket_server.close()

if __name__ == "__main__":
    IP = "192.168.1.47"
    PORT = 8080

    game = GameServer(IP, PORT)
    game.start(2)
