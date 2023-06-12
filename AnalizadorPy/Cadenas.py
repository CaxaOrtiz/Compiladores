from AdmCaracteres import CharArrayManager
from  TipoToken import TipoToken
from  typing import Optional

class Cadenas():
    def __init__(self, manager: CharArrayManager):
        self.manager:CharArrayManager = manager
        self.literal = None

    def get_lexema(self) -> Optional[str]:
        lexema = ""
        continuar = False
        next_char = self.manager.getNextChar()
        if next_char == '"':
                    continuar = not continuar
        if next_char == '\n':
                self.manager.backPosition()
        lexema += next_char
        
        while self.manager.hasNext and continuar:
            next_char = self.manager.getNextChar()
            if next_char == '"':
                    continuar = not continuar
            if next_char == '\n':
                self.manager.backPosition()
                break
            lexema += next_char
        
        if not (lexema[0] == '"' and lexema[-1] == '"'):
            return None
        
        self.literal = lexema[1:-1]
        return lexema

    def get_tipo_token(self) -> TipoToken:
        return TipoToken.CADENA

    def get_literal(self):
        return self.literal