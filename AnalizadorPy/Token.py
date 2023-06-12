class Token:
    def __init__(self, tipo, lexema, literal, linea):
        self.tipo = tipo
        self.lexema = lexema
        self.literal = literal
        self.linea = linea

    def __str__(self):
        return f"{self.tipo} {self.lexema} {'' if self.literal is None else str(self.literal)}"

    def get_tipo(self):
        return self.tipo

    def get_lexema(self):
        return self.lexema

    def get_literal(self):
        return self.literal

    def get_linea(self):
        return self.linea