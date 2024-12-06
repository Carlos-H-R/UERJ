import Map

class Room(Map):
    # extende o mapa para implementar a sala
    # pode ser usada para a sala do tesouro 
    # pode ser usada como uma sala de espera
    # sala vazia nao pode ser acessada
    # registra posicao dos recursos 
    # geracao aleatoria de tesouros
    # jogador tem 10 segundos para coletar os tesouros
    # se atingido o limite de tempo o jogador é removido da sala
    # semaforo para controlar o acesso de jogadores

    # Semaforo binario garantindo q apenas um jogador por vez acesse a sala
    # jogadores que tentarem acessar uma sala ocupada sera colocado em uma sala de espera
    # a sala de espera e gerenciada pelo servidor

    def __init__(self) -> None:
        pass

    def is_empty(self) -> bool:
        # checa se a sala esta vazia
        return True
    
