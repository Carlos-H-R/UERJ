import keyboard

from time import sleep
from random import randint
from Treasure import Treasure


class Map():
    # implementa o mapa do jogo 
    # registra a posição dos objetos 
    # registra a posicao dos jogadores
    # registra os acessos as salas

    def __init__(self, lines=25, columns=25, number_of_treasures=15, number_of_rooms=0) -> None:
        self.__size__ = (lines,columns)
        self.__rooms__ = number_of_rooms
        self.__id_track__ = 1
        self.__position__ = dict()
        self.__tresures__ = dict()
        self.__n_treasures__ = number_of_treasures

        self.createMap()
        self.distribute_tresures()
        self.start()


    def start(self) -> None:
        self.__position__['test'] = (1,2)
        position = self.__position__['test']
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
            
            if not self.check_treasure((line,column)) and  not (self.__position__ == (line,column)):
                self.__tresures__[self.__id_track__] = ((line,column), Treasure(value, self.__id_track__))
                self.__id_track__ += 1
                self.__map__[line][column] = 'X'

    def check_treasure(self, position) -> bool:
        for i in self.__tresures__.values():
            if position == i[0]:
                return True
            
        return False

    def update_position(self, id: str, dx: int, dy: int) -> None:
        y,x = self.__position__[id]
        self.__map__[y][x] = ' '

        y = (y+dy)%self.__size__[0]
        x = (x+dx)%self.__size__[1]

        self.__position__[id] = (y,x)
        self.__map__[y][x] = 'P'

        self.check_treasure(self.__position__)

        self.showMap()

    def interact(self):
        pass

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
        formatedMap = str()

        for line in self.__map__:
            formatedMap += str(line) + '\n'

        print(formatedMap)
        return formatedMap
    

class TreasureRoom(Map):
    # extende o mapa para implementar a sala
    # pode ser usada para a sala do tesouro 
    # sala vazia nao pode ser acessada
    # registra posicao dos recursos 
    # geracao aleatoria de tesouros
    # jogador tem 10 segundos para coletar os tesouros
    # se atingido o limite de tempo o jogador é removido da sala
    # semaforo para controlar o acesso de jogadores

    # Semaforo binario garantindo q apenas um jogador por vez acesse a sala
    # jogadores que tentarem acessar uma sala ocupada sera colocado em uma sala de espera
    # a sala de espera e gerenciada pelo servidor
    __empty__ = False

    def start(self) -> None:
        pass

    def is_empty(self) -> bool:
        # checa se a sala esta vazia
        return self.__empty__
    
    def check_empty(self) -> None:
        counter = 0
        for i in self.__tresures__:
            if i[1].is_colected():
                counter += 1

        if counter == self.__n_treasures__:
            self.__empty__ = True


class Main_Map(Map):
    # extende a classe mapa para implementar o mapa principal
    # região crítica
    # concorrecias gerenciada por semáforos
    # o mapa eh dividido em celulas
    # acessos simultaneos a recursos devem ser sincronizados
    # alteração do estado do mapa deve ser uma operação atomica

    # movimentacao dos jogadores eh controlada por semaforos
        # cada celula do mapa pode ter um semaforo individual
        # ou o mapa inteiro possui um semaforo

    # apenas um jogador pode coletar tesouro por vez
    # a posicao deve ser atualizada de forma consistente

    def start(self) -> None:
        self.distribute_treasure_rooms()

    def distribute_treasure_rooms(self) -> None:
        self.treasure_rooms = dict()

        for i in range(self.__rooms__):
            y = randint(0,self.__size__[0])
            x = randint(0,self.__size__[1])
            position = (x,y)

            if not self.check_treasure(position):
                self.treasure_rooms['room_'+str(id)] = (position, TreasureRoom())

            # else:
            #     y = randint(0,self.__size__[0])
            #     x = randint(0,self.__size__[1])
            #     position = (x,y)



if __name__ == "__main__":
    m = Map(lines=10, columns=10, number_of_treasures=3)
    # print(m.showMap())