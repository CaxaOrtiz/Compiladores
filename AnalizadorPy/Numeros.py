from typing import Optional
from AdmCaracteres import CharArrayManager
from TipoToken import TipoToken

class Numeros():
    def __init__(self, manager: CharArrayManager):
        self.manager = manager
        self.literal = None

    def get_lexema(self) -> Optional[str]:
        lexema = ""
        wraper = None
        continuar = True
        status = 0
        while self.manager.hasNext() and continuar:
            next_char = self.manager.getNextChar()
            if status == 0:
                if next_char.isdigit():
                    lexema += next_char
                    status = 1
            elif status == 1:
                if next_char.isdigit():
                    lexema += next_char
                    status = 1
                elif next_char == '.':
                    lexema += next_char
                    status = 2
                else:
                    status = 7
            elif status == 2:
                if next_char.isdigit():
                    lexema += next_char
                    status = 3
                else:
                    status = 8
            elif status == 3:
                if next_char.isdigit():
                    lexema += next_char
                    status = 3
                elif next_char == 'E':
                    lexema += next_char
                    status = 4
                else:
                    status = 7
            elif status == 4:
                if next_char == '+' or next_char == '-':
                    lexema += next_char
                    status = 5
                elif next_char.isdigit():
                    lexema += next_char
                    status = 6
                else:
                    status = 8
            elif status == 5:
                if next_char.isdigit():
                    lexema += next_char
                    status = 6
                else:
                    status = 8
            elif status == 6:
                if next_char.isdigit():
                    lexema += next_char
                    status = 6
                else:
                    status = 7

            if status == 7:
                continuar = False
                wraper = lexema
                self.manager.backPosition()

            if status == 8:
                continuar = False
                self.manager.backPosition()

            if (not self.manager.hasNext() and status == 3) or (not self.manager.hasNext() and status == 1) or (not self.manager.hasNext() and status == 6):
                continuar = False
                wraper = lexema

        self.literal = lexema
        return wraper

    def get_tipo_token(self) -> TipoToken:
        return TipoToken.NUMERO

    def get_literal(self):
        return float(self.literal)