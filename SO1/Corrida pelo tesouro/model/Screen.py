from os import system
from sys import stdout
from time import sleep

class Screen:
    # Classe responsavel por exibir informacoes para o jogador
    # Mapa, pontuacao e avisos

    def __init__(self) -> None:
        # inicia o atributo que guarda o tamanho da saída
        self.output_size: int = 0

    def clear(self, timeout=0):
        sleep(timeout)
        system('cls')

    def output(self, content: str):
        try:
            # Formata as informacoes e exibe na saida padrao
            self.clear()
            self.output_size = stdout.write(content)
            stdout.flush()
            sleep(0.02)

        except BaseException as error:
            print(error)


if __name__ == "__main__":
    s = Screen()
    
    s.output('Vamos \ntestar... ')
    sleep(2)

    s.output('Serasse funciona? ')
    sleep(2)

    s.output('oi')
    sleep(2)

    s.output('Finalizando o Teste! ...')
    sleep(3)

    s.clear()

        