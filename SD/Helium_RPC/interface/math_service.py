class math_service:
    def __init__(self) -> None:
        self.services = {
            'add': self.add,
            'sub': self.sub,
            'divide': self.divide,
            'multiply': self.multiply
        }
    
    def add(self, x: int, y: int) -> int:
        return x+y
    
    def sub(self, x: int, y: int) -> int:
        return x-y
    
    def divide(self, x: int, y: int) -> int:
        return x//y
    
    def multiply(self, x: int, y: int) -> int:
        return x*y
