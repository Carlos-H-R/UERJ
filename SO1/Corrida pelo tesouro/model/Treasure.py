class Treasure:
    def __init__(self, value, position) -> None:
        self.__value__ = value
        self.__colected__ = False
        self.__position__ = position
        
    def __colect__(self) -> None:
        self.__colected__ = True

    def is_colected(self) -> bool:
        return self.__colected__
    
    def getValue(self) -> int:
        return self.__value__
    
    def getPosition(self) -> tuple:
        return self.__position__