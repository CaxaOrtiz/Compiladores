
from AFDGeneral import AFDManager
from Comentarios import Comentarios
from AFD import TipoAFD
from enum import Enum
from TipoToken import TipoToken
from Token import Token
from AdmCaracteres import CharArrayManager


class TipoAFD(Enum):
    IDENTIFICADOR = 0
    CADENA = 1
    NUMEROS = 2
    SIMBOLO_SIMPLE = 3
    COMENTARIOS_Y_SLASH = 4
    OPERADOR_RELACIONAL = 5
    NINGUNO = 6


class Escaner:

    def __init__(self, source):
        palabras_reservadas = {
            "and": TipoToken.AND,
            "class": TipoToken.CLASS,
            "else": TipoToken.ELSE,
            "false": TipoToken.FALSE,
            "for": TipoToken.FOR,
            "fun": TipoToken.FUNCTION,
            "if": TipoToken.IF,
            "null": TipoToken.NULL,
            "or": TipoToken.OR,
            "print": TipoToken.PRINT,
            "return": TipoToken.RETURN,
            "super": TipoToken.SUPER,
            "this": TipoToken.THIS,
            "true": TipoToken.TRUE,
            "var": TipoToken.VAR,
            "while": TipoToken.WHILE
        }
        self.source = source
        self.tokens = []
        self.manager = CharArrayManager(list(source))
        self.AUTOMATAS = AFDManager(self.manager)
        self.palabrasReservadas = palabras_reservadas



    def scan_tokens(self):
        print("Escaneando tokens")
        linea = 1
        char_manager = self.manager  # Crear una instancia de la clase CharArrayManager

        while True:
            try:
                nextChar = char_manager.getNextChar()
                if nextChar:
                    type = self.AUTOMATAS.checkType(nextChar)
                    automata = self.AUTOMATAS.getAFD(type)

                    if automata:
                        char_manager.backPosition()
                        lexema = automata.get_lexema()
                        if lexema:
                            if lexema in self.palabrasReservadas:
                                self.tokens.append(Token(self.palabrasReservadas[lexema], lexema, automata.get_literal(), linea))
                            else:
                                if automata.get_tipo_token() != TipoToken.COMENTARIOS:
                                    self.tokens.append(Token(automata.get_tipo_token(), lexema, automata.get_literal(), linea))
                                else:
                                    comentarios = automata
                                    linea += comentarios.get_aumento()
                        else:
                            from Interprete import error
                            mensaje = ""
                            if automata.get_tipo_token() == TipoToken.CADENA:
                                mensaje = "Cadena mal introducida"
                            elif automata.get_tipo_token() == TipoToken.NUMERO:
                                mensaje = "Numero mal introducido"
                            elif automata.get_tipo_token() == TipoToken.COMENTARIOS:
                                mensaje = "Comentario mal escrito"
                            else:
                                raise ValueError("Unexpected value: " + automata.get_tipo_token() + ",linea:" + str(linea) + ",mensaje:" + mensaje)
                            error(linea, mensaje);
                    if nextChar == '\n':
                        linea += 1
                else:
                    break
            except:
                break

        self.tokens.append(Token(TipoToken.EOF, "", None, linea))
        return self.tokens
