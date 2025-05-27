class math_service:
    """
    Fornece métodos para operações matemáticas básicas como adição,
    subtração, divisão e multiplicação.
    """
    def __init__(self) -> None:
        """
        Inicializa a classe e mapeia os nomes das operações
        para seus respectivos métodos.

        Atributos:
            services (dict): Um dicionário que armazena os métodos de serviço,
                             onde a chave é o nome da operação (string) e o
                             valor é o método correspondente.
        """
        self.services = {
            'add': self.add,
            'sub': self.sub,
            'divide': self.divide,
            'multiply': self.multiply
        }
    
    def add(self, x: int, y: int) -> int:
        """
        Realiza a adição de dois números inteiros.

        Args:
            x (int): O primeiro operando.
            y (int): O segundo operando.

        Returns:
            int: A soma de `x` e `y`.
        """
        return x+y
    
    def sub(self, x: int, y: int) -> int:
        """
        Realiza a subtração de dois números inteiros.

        Args:
            x (int): O primeiro operando (minuendo).
            y (int): O segundo operando (subtraendo).

        Returns:
            int: A diferença entre `x` e `y`.
        """
        return x-y
    
    def divide(self, x: int, y: int) -> int:
        """
        Realiza a divisão inteira de dois números inteiros.

        Args:
            x (int): O dividendo.
            y (int): O divisor.

        Returns:
            int: O resultado da divisão inteira de `x` por `y`.
                 Retorna 0 se `y` for 0 para evitar ZeroDivisionError,
                 ou levanta uma exceção se um tratamento mais rigoroso for necessário.
                 (Nota: A implementação atual usa //, que levantará ZeroDivisionError se y for 0).
        """
        if y == 0:
            # Em um ambiente de produção, é preferível levantar um erro RPC
            # ou retornar um valor de erro específico.
            print("Erro: Divisão por zero!")
            return 0 # Ou raise ZeroDivisionError("Divisão por zero não permitida")
        return x//y
    
    def multiply(self, x: int, y: int) -> int:
        """
        Realiza a multiplicação de dois números inteiros.

        Args:
            x (int): O primeiro operando.
            y (int): O segundo operando.

        Returns:
            int: O produto de `x` e `y`.
        """
        return x*y

