from typing import Optional
from AdmCaracteres import CharArrayManager
from TipoToken import TipoToken

class Identificador():
    def __init__(self, manager: CharArrayManager):
        self.manager = manager

    def get_lexema(self) -> Optional[str]:
        lexema = ""
        continuar = True
        while self.manager.hasNext() and continuar:
            next_char = self.manager.getNextChar()
            if next_char.isalpha() or next_char.isdigit():
                lexema += next_char
            else:
                continuar = False
                self.manager.backPosition()
        
        if len(lexema) == 0:
            return None
        
        return lexema

    def get_tipo_token(self) -> TipoToken:
        return TipoToken.IDENTIFICADOR

    def get_literal(self):
        return None