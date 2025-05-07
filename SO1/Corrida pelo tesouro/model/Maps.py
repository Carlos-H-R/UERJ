from random import randint
from model.Player import Player
from model.Treasure import Treasure


class Map():
    """
    # Classe Map

    -> Implementa o mapa do jogo 
    -> Registra a posição dos objetos 
    -> Registra a posicao dos jogadores
    """

    def __init__(self, lines=25, columns=25, number_of_treasures=15, number_of_rooms=0) -> None:
        self.__size__ = (lines,columns)
        self.__n_rooms__ = number_of_rooms
        self.__n_treasures__ = number_of_treasures

        self.__id_track__ = 1
        self.__players__ = dict()
        self.__tresures__ = dict()

        self.createMap()
        self.distribute_tresures()
        self.start()


    def start(self) -> None:
        self.__players__['test'] = Player()
        self.__players__['test'].updatePosition(self.__size__, 1, 2)
        position = self.__players__['test'].getPosition()
        self.__map__[position[0]][position[1]] = 'P'

        self.showMap()
        self.update()


    def createMap(self) -> None:
        self.__map__ = []
        
        for i in range(self.__size__[0]):
            self.__map__.append([' '] * self.__size__[1])

    def distribute_tresures(self) -> None:
        while self.__id_track__ <= self.__n_treasures__:
            value = randint(1,15) * 100
            column = randint(0,self.__size__[1] - 1)
            line = randint(0,self.__size__[0] - 1)
            
            if not self.check_treasure((line,column)):
                self.__tresures__[self.__id_track__] = Treasure(value, (line,column))
                self.__id_track__ += 1
                self.__map__[line][column] = 'X'

    def check_treasure(self, position: tuple) -> bool:
        """ Retorna True se ha tesouro na posicao informada """

        for i in self.__tresures__.values():
            if position == i.getPosition() and not i.is_colected():
                return True
            
        return False
    
    def get_treasure(self, position) -> int:
        """ Retorna o Valor do tesouro naquela posição """

        for i in self.__tresures__.keys():
            if position == self.__tresures__[i].getPosition():
                return self.__tresures__[i].getValue()
            
        return 0

    def update_position(self, id: str, dx: int, dy: int) -> None:
        y,x = self.__players__[id].getPosition()

        yy = (y+dy)%self.__size__[0]
        xx = (x+dx)%self.__size__[1]

        if self.check_treasure((yy,xx)):
            treasure_value = self.get_treasure((yy,xx))

            self.__players__[id].updatePoints(treasure_value)
            self.__players__[id].updatePosition(0, (yy,xx))
            self.__map__[y][x] = ' '
            self.__map__[yy][xx] = 'P'

        else:
            self.__players__[id].updatePosition(0, (yy,xx))
            self.__map__[y][x] = ' '
            self.__map__[yy][xx] = 'P'

        self.showMap()

    def move(self, id, input) -> None:
        if input == 'up':
            self.update_position(id,  0,-1)

        elif input == 'down':
            self.update_position(id,  0, 1)

        elif input == 'left':
            self.update_position(id, -1, 0)

        elif input == 'right':
            self.update_position(id,  1, 0)

    def update(self):
        while True:
            # keyboard.on_press(callback=self.keyboard)
            key = str(input())
            self.move('test', key.lower())
        
    def showMap(self) -> str:
        # top_size = (2 * self.__size__[1]) + 1
        # top = ' ' * top_size
        formatedMap = str()

        # formatedMap += '\033[4m' + top + '\n'

        for line in self.__map__:
            # formatedMap += '|' + '|'.join(line) + '|' + '\n'
            formatedMap += ' '.join(line) + '\n'

        # formatedMap += '\033[0m'
        
        # print(formatedMap)
        return formatedMap
    

class TreasureRoom(Map):
    # Extende a class Map para implementar a sala
    # usada como a sala do tesouro 
    # sala vazia nao pode ser acessada
    # registra posicao dos recursos 
    # geracao aleatoria de tesouros
    # acesso e tempo disponível é controlado esxternamente
    # semaforo para controlar o acesso de jogadores

    # Semaforo binario garantindo q apenas um jogador por vez acesse a sala
    # jogadores que tentarem acessar uma sala ocupada sera colocado em uma sala de espera
    # a sala de espera e gerenciada pelo servidor
    __empty__ = False

    def start(self) -> None:
        pass

    def enter(self, player_id):
        self.__players__[player_id] = Player()

    def is_empty(self) -> bool:
        # checa se a sala esta vazia
        return self.__empty__
    
    def check_empty(self) -> None:
        counter = 0
        for i in self.__tresures__:
            if i[1].is_colected():
                counter += 1

        if counter >= self.__n_treasures__:
            self.__empty__ = True

    def set_entry_position(self, position) -> None:
        self.__entry_position__ = position

    def get_entry_position(self) -> tuple:
        return self.__entry_position__
    
    def new_player(self, name: str):
        self.__players__[name] = Player()

        x = randint(0,self.__size__[1] - 1)
        y = randint(0,self.__size__[0] - 1)

        position = [(y,x)]

        while position.__len__():
            p = position.pop(0)

            if not self.check_treasure(p) and not self.check_room(p) and not self.check_player('', p):
                self.__players__[name].updatePosition(0, p)
                self.__map__[p[0]][p[1]] = 'P'

            else:
                x = randint(0,self.__size__[1] - 1)
                y = randint(0,self.__size__[0] - 1)

                position.append((y,x))


class Main_Map(Map):
    """
    # Classe Main_Map
    
    ### Extende a classe mapa para implementar o mapa principal
    
    É uma egião crítica e as concorrências são tratadas pelo servidor
    
    O mapa é dividido em celulas nas quais são distribuidos os recursos
    Acessos simultaneos a recursos são tratados 
    Alteração do estado do mapa eh uma operação atomica e controlada por semaforos

    A movimentacao dos jogadores é controlada por semaforos
        -> O mapa inteiro possui um semaforo que permite
    """

    # apenas um jogador pode coletar tesouro por vez
    # a posicao deve ser atualizada de forma consistente

    def start(self) -> None:
        self.distribute_treasure_rooms()

        # # wait for players
        # self.__players__['test'] = Player()
        # self.__players__['test'].updatePosition(0, self.__size__, 1, 2)
        # position = self.__players__['test'].getPosition()
        # self.__map__[position[0]][position[1]] = 'P'

        # self.showMap()
        # self.update()

    def distribute_treasure_rooms(self) -> None:
        self.treasure_rooms = dict()
        id_track = 1

        positions = []

        for i in range(self.__n_rooms__):
            y = randint(0,self.__size__[0] - 1)
            x = randint(0,self.__size__[1] - 1)
            positions.append((x,y))

        while positions.__len__():
            position = positions.pop(0)

            if not self.check_treasure(position) and not self.check_room(position):
                self.treasure_rooms[id_track] = TreasureRoom(lines=15, columns=15, number_of_rooms=0, number_of_treasures=15)
                self.treasure_rooms[id_track].set_entry_position(position)
                self.__map__[position[1]][position[0]] = 'S'

                id_track += 1

            else:
                y = randint(0, self.__size__[0])
                x = randint(0, self.__size__[1])
                positions.append((x,y))

    def get_room(self, position):
        """ Retorna o id da Sala de tesouro na posição informada """
        
        for room in self.treasure_rooms.keys():
            if position == self.treasure_rooms[room].get_entry_position():
                return room
            
        return 0

    def check_room(self, position) -> bool:
        """ Retorna True quando há Sala de tesouro na posição informada"""

        for room in self.treasure_rooms.values():
            if position == room.get_entry_position():
                return True
            
        return False
    
    def check_player(self, id, position) -> bool:
        """ Retorna True quando há um jogador com id diferente na posição informada """

        for key in self.__players__.keys():
            player = self.__players__[key]
            if id != key and position == player.getPosition() and not player.getRoom():
                return True
            
        return False

    def new_player(self, name: str):
        self.__players__[name] = Player()

        x = randint(0,self.__size__[1] - 1)
        y = randint(0,self.__size__[0] - 1)

        position = [(y,x)]

        while position.__len__():
            p = position.pop(0)

            if not self.check_treasure(p) and not self.check_room(p) and not self.check_player('', p):
                self.__players__[name].updatePosition(0, p)
                self.__map__[p[0]][p[1]] = 'P'

            else:
                x = randint(0,self.__size__[1] - 1)
                y = randint(0,self.__size__[0] - 1)

                position.append((y,x))

    def update_position(self, id: str, dx: int, dy: int) -> None:
        y,x = self.__players__[id].getPosition()

        yy = (y+dy)%self.__size__[0]
        xx = (x+dx)%self.__size__[1]

        if self.check_treasure((yy,xx)):
            treasure_value = self.get_treasure((yy,xx))

            self.__players__[id].updatePoints(treasure_value)
            self.__players__[id].updatePosition(0,(yy,xx))
            self.__map__[y][x] = ' '
            self.__map__[yy][xx] = 'P'

        elif self.check_room((yy,xx)):
            room = self.get_room((yy,xx))
            self.__players__[id].updatePosition(room, (0,0))

            self.treasure_rooms[room].new_player(id)

        elif self.check_player(id, (yy,xx)):
            pass

        else:
            self.__players__[id].updatePosition(0, (yy,xx))
            self.__map__[y][x] = ' '
            self.__map__[yy][xx] = 'P'



if __name__ == "__main__":
    # m = Map(lines=10, columns=10, number_of_treasures=3)
    # print(m.showMap())

    main = Main_Map(lines=15, columns=15, number_of_treasures=10, number_of_rooms=9)
