from AdmCaracteres import CharArrayManager
from TipoToken import TipoToken

class Simbolos:
    def __init__(self, manager):
        self.manager = manager
        self.simbolo = ''
        self.simbolos = {
            '+': TipoToken.SUMA,
            '-': TipoToken.RESTA,
            '*': TipoToken.MULTIPLICACION,
            '{': TipoToken.LLAVE_IZQUIERDA,
            '}': TipoToken.LLAVE_DERECHA,
            '[': TipoToken.CORCHETE_IZQUIERDO,
            ']': TipoToken.CORCHETE_DERECHO,
            '(': TipoToken.PARENTESIS_IZQUIERDO,
            ')': TipoToken.PARENTESIS_DERECHO,
            ',': TipoToken.COMA,
            '.': TipoToken.PUNTO,
            ';': TipoToken.PUNTO_Y_COMA
        }

    def get_lexema(self):
        self.simbolo = self.manager.getNextChar()
        return self.simbolo

    def get_tipo_token(self):
        return self.simbolos.get(self.simbolo)

    def get_literal(self):
        return None