
class Buffer:
    def load_buffer(self):
        ruta=input("Ingresa la ruta del archivo para analizar \n")
        a = open(ruta, 'r')
        text = a.readline()

        buffer = []
        cont = 1

        while text != "":
            buffer.append(text)
            text = a.readline()
            cont += 1

            if cont == 10 or text == '':
                buf = ''.join(buffer)
                cont = 1
                yield buf
                buffer = []

        a.close()

class Token:

    nombre_token =""
    valor_token=""
    fila = 0
    columna = 0

    def setAtributos(self, nombre_token, valor_token, fila, columna):
        self.nombre_token = nombre_token
        self.valor_token = valor_token
        self.fila = fila
        self.columna = columna

    def __str__(self):
        print("Token: {"+self.nombre_token+"} \n Valor: {"+self.valor_token+"} \n Fila: {"+str(self.fila)+"} \n Columna: {"+str(self.columna)+"}\n\n")

import re

class AnalizadorLexico:
    lin_num = 1

    def tokenize(self, code):
        reglas = [
            ('Main', r'main'),          # main
            ('Void', r'void'),          # void
            ('Int', r'int'),            # int
            ('Float', r'float'),        # float
            ('Char', r'char'),          # char
            ('If', r'if'),              # if
            ('Else', r'else'),          # else
            ('While', r'while'),        # while
            ('For', r'for'),            # for
            ('Struct', r'struct'),      # struct
            ('Include', r'#include'),   # include
            ('Read', r'read'),          # read
            ('Print', r'print'),        # print
            ('Parentesis_de_apertura', r'\('),        # (
            ('Parentesis_de_cierre', r'\)'),        # )
            ('Corchete_de_apertura', r'\['),        # (
            ('Corchete_de_cierre', r'\]'),        # )
            ('Llave_de_apertura', r'\{'),          # {
            ('Llave_de_cierre', r'\}'),          # }
            ('Coma', r','),            # ,
            ('Punto_y_coma', r';'),           # ;
            ('Igual', r'=='),              # ==
            ('Noigual', r'!='),              # !=
            ('Mayorigual', r'<='),              # <=
            ('Menorigual', r'>='),              # >=
            ('Or', r'\|\|'),            # ||
            ('And', r'&&'),             # &&
            ('Attr', r'\='),            # =
            ('INCLUDE_CONST',r'\<[a-zA-Z]\w*\.[c-h]\>'), #INCLUDE
            ('Mayor', r'<'),               # <
            ('Menor', r'>'),               # >
            ('Mas', r'\+'),            # +
            ('Menos', r'-'),            # -
            ('Mult', r'\*'),            # *
            ('Div', r'\/'),             # /
            ('Id', r'[a-zA-Z]\w*'),     # IDENTIFICADORES
            ('FLOAT_CONST', r'\d(\d)*\.\d(\d)*'),   # FLOAT
            ('INTEGER_CONST', r'\d(\d)*'),          # INT
            ('CHAR_CONST', r'\'[a-zA-Z]\''),        #CHAR
            ('NEWLINE', r'\n'),         # SALTO DE LINEA
            ('SKIP', r'[ \t]+'),        # ESPACIO and TABULADOR
            ('MISMATCH', r'°'),         # CUALQUIER OTRO CARACTER
        ]

        tokens_join = '|'.join('(?P<%s>%s)' % x for x in reglas)
        lin_start = 0
        token = Token()

        for m in re.finditer(tokens_join, code):
            token_tipo = m.lastgroup
            token_lexema = m.group(token_tipo)
            if token_tipo == 'NEWLINE':
                lin_start = m.end()
                self.lin_num += 1
            elif token_tipo == 'SKIP':
                continue
            else:
                    col = m.start() - lin_start
                    token.setAtributos(token_tipo,token_lexema,self.lin_num,col)
                    token.__str__()

        return token

if __name__ == '__main__':
    Buffer = Buffer()
    Analizador = AnalizadorLexico()
    for i in Buffer.load_buffer():
        Analizador.tokenize(i)