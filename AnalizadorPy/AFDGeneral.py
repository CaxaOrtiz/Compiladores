from Identificador import Identificador
from Cadenas import Cadenas
from Numeros import Numeros
from Simbolos import Simbolos
from Comentarios import Comentarios
from Operadores import Operadores
from AFD import TipoAFD


class AFDManager:
    LETRAS = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    NUMEROS = "0123456789"
    SIMBOLOS_SIMPLES = "+-*()[]{};.,"
    OPERADORES = "><=!"
    
    def __init__(self, manager):
        self.identificador = Identificador(manager)
        self.cadenas = Cadenas(manager)
        self.numeros = Numeros(manager)
        self.simbolos = Simbolos(manager)
        self.comentarios = Comentarios(manager)
        self.operadores = Operadores(manager)
    
    def getAFD(self, type):
        if type == TipoAFD.IDENTIFICADOR:
            return self.identificador
        elif type == TipoAFD.CADENA:
            return self.cadenas
        elif type == TipoAFD.NUMEROS:
            return self.numeros
        elif type == TipoAFD.SIMBOLO_SIMPLE:
            return self.simbolos
        elif type == TipoAFD.COMENTARIOS_Y_SLASH:
            return self.comentarios
        elif type == TipoAFD.OPERADOR_RELACIONAL:
            return self.operadores
        else:
            return None
    
    def checkType(self, c):
        if c in self.LETRAS:
            return TipoAFD.IDENTIFICADOR
        elif c == '"':
            return TipoAFD.CADENA
        elif c in self.NUMEROS:
            return TipoAFD.NUMEROS
        elif c in self.SIMBOLOS_SIMPLES:
            return TipoAFD.SIMBOLO_SIMPLE
        elif c == '/':
            return TipoAFD.COMENTARIOS_Y_SLASH
        elif c in self.OPERADORES:
            return TipoAFD.OPERADOR_RELACIONAL
        else:
            return TipoAFD.NINGUNO
