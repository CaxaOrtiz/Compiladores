from AdmCaracteres import CharArrayManager
from TipoToken import TipoToken
import AFDGeneral as AFDMana

class Operadores:
    operadores = {
        "<": TipoToken.MENOR_QUE,
        ">": TipoToken.MAYOR_QUE,
        "=": TipoToken.ASIGNAR,
        "!": TipoToken.NEGACION,
        "<=": TipoToken.MENOR_O_IGUAL,
        ">=": TipoToken.MAYOR_O_IGUAL,
        "!=": TipoToken.DIFERENTE,
        "==": TipoToken.IGUAL_A,
    }

    def __init__(self, manager):
        self.manager = manager
        self.lexema = ""

    def get_lexema(self):
        lexema = ""
        continuar = True
        status = 0
        while self.manager.hasNext() and continuar:
            next_char = self.manager.getNextChar()
            if status == 0:
                if next_char in AFDMana.AFDManager.OPERADORES:
                    lexema += next_char
                    status = 1
            elif status == 1:
                if next_char == "=":
                    lexema += next_char
                    status = 2
                else:
                    status = 3
            if status == 2:
                continuar = False
                self.lexema = lexema
                return self.lexema
            if status == 3:
                continuar = False
                self.manager.backPosition()
                self.lexema=lexema
                return self.lexema
            if status == 1 and not self.manager.hasNext():
                self.lexema=lexema
                return self.lexema

    def get_tipo_token(self):
        return Operadores.operadores.get(self.lexema)

    def get_literal(self):
        return None

