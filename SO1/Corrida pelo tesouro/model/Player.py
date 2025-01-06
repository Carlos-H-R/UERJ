class Player:
    def __init__(self) -> None:
        # cria o objeto player
        self.__points__ = 0
        self.__position__ = None
        self.__room__ = None

    def getRoom(self) -> int:
        return self.__room__

    def getPoints(self) -> int:
        return self.__points__
    
    def getPosition(self) -> list:
        return self.__position__
    
    def setRoom(self, room) -> None:
        self.__room__ = room
    
    def setPoints(self, points: int) -> None:
        self.__points__ = points
        
    def updatePoints(self, points):
        # atualiza a contagem de pontos
        self.__points__ += points

    def updatePosition(self, room, position):
        # armazena a posicao do jogador
        line = position[0]
        column = position[1]
        self.__room__ = room
        self.__position__ = [line,column]


if __name__ == "__main__":
    p = Player()
    # p.updatePoints()
    print(p.__points__)
