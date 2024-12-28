class Treasure:
    def __init__(self, value, id) -> None:
        self.__id__ = id # cada tesouro tem um id diferente
        self.__value__ = value
        self.__colected__ = False
        
    def __colect__(self, id):
        self.__colected__ = True
        self.__playerID__ = id

    def is_colected(self) -> bool:
        return self.__colected__
    