from AdmCaracteres import CharArrayManager
from TipoToken import TipoToken
from typing import Optional

class Comentarios():
    def __init__(self, manager: CharArrayManager):
        self.manager = manager
        self.aumento = 0
        self.set_aumento = False
        self.tipo_token = None

    def get_lexema(self) -> Optional[str]:
        lexema = ""
        wraper = None
        status = 0
        continuar = True
        while self.manager.hasNext() and continuar:
            next_char = self.manager.getNextChar()
            if status == 0:
                if next_char == '/':
                    lexema += next_char
                    status = 1
            elif status == 1:
                if next_char == '/':
                    lexema += next_char
                    status = 2
                elif next_char == '*':
                    lexema += next_char
                    status = 3
                else:
                    status = 5
            elif status == 2:
                self.tipo_token = TipoToken.COMENTARIOS
                if next_char != '\n':
                    lexema += next_char
                    status = 2
                else:
                    status = 6
            elif status == 3:
                self.tipo_token = TipoToken.COMENTARIOS
                if next_char == '*':
                    lexema += next_char
                    status = 4
                elif next_char == '\n':
                    self.aumento += 1
                else:
                    lexema += next_char
            elif status == 4:
                if next_char == '/':
                    lexema += next_char
                    status = 7
                elif next_char == '*':
                    lexema += next_char
                    status = 4
                else:
                    lexema += next_char
                    status = 3

            if status == 5:
                continuar = False
                self.manager.backPosition()
                self.tipo_token = TipoToken.DIVISION
                wraper = lexema
            elif status == 6:
                continuar = False
                self.manager.backPosition()
                self.tipo_token = TipoToken.COMENTARIOS
                wraper = lexema
            elif status == 7:
                self.set_aumento = True
                continuar = False
                self.tipo_token = TipoToken.COMENTARIOS
                wraper = lexema
            elif not self.manager.hasNext() and status == 2:
                continuar = False
                self.tipo_token = TipoToken.COMENTARIOS
                wraper = lexema
            elif not self.manager.hasNext() and status == 3:
                continuar = False
                self.tipo_token = TipoToken.COMENTARIOS
                wraper = None

        return wraper

    def get_tipo_token(self) -> TipoToken:
        return self.tipo_token

    def get_literal(self):
        return None

    def get_aumento(self):
        aux = self.aumento
        aux_aumento = self.set_aumento
        self.set_aumento = False
        self.aumento = 0
        return aux if aux_aumento else 0