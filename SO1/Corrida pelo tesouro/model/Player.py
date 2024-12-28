class Player:
    def __init__(self) -> None:
        # cria o objeto player
        self.__points__ = 0
        
    def updatePoints(self, points):
        # atualiza a contagem de pontos
        self.__points__ = points

    def updatePosition(self, size, line, column):
        # armazena a posicao do jogador
        self.map_size = size
        self.__position__ = [line,column]


if __name__ == "__main__":
    p = Player()
    p.updatePoints()
    print(p.__points__)
