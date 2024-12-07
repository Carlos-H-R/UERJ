class Player:
    def __init__(self) -> None:
        self.points = 0

        # configura e inicia a conexao

    def getMap(self):
        # get the current map from the server and update if necessary
        pass
        
    def getPoints(self):
        # comunicate with the server and update the number of points
        points = 10
        self.points = points

    def getPosition(self):
        # checa a posição do jogador no mapa
        pass

    def move(self, dx, dy):
        # envia para o servidor o input de movimento
        vector = (dx,dy)
        return vector
    
    def interact(self):
        # envia para o servidor comando para interagir com a celula atual
        pass