from TipoToken import TipoToken
from Token import Token
import traceback

class Analizador():
    def __init__(self, tokens):
        self.tokens = tokens
        self.currentToken: Token = tokens[0]
        self.debugger_mode = False

    def analisis(self):
        try:
            self.program()
            self.match(TipoToken.EOF)
            print("Programa válido")
            return "Programa válido"
        except Exception as e:
            print("Programa no válido")
            if self.debugger_mode:
                traceback.print_exc()
            print(e)
            return "Programa no válido"

    def program(self):
        self.declaration()

    def declaration(self):
        if self.currentToken.get_tipo() == TipoToken.CLASS:
            self.class_decl()
            self.declaration()
        elif self.currentToken.get_tipo() == TipoToken.FUNCTION:
            self.fun_decl()
            self.declaration()
        elif self.currentToken.get_tipo() == TipoToken.VAR:
            self.var_decl()
            self.declaration()
        elif self.currentToken.get_tipo() in [TipoToken.FOR, TipoToken.IF, TipoToken.PRINT, TipoToken.RETURN, TipoToken.WHILE, TipoToken.LLAVE_IZQUIERDA, TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL, TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO, TipoToken.IDENTIFICADOR, TipoToken.NEGACION, TipoToken.RESTA]:
            self.statement()
            self.declaration()
        else:
            # Asumimos épsilon
            pass

    def class_decl(self):
        self.match(TipoToken.CLASS)
        self.match(TipoToken.IDENTIFICADOR)
        self.class_inher()
        self.match(TipoToken.LLAVE_IZQUIERDA)
        self.functions()
        self.match(TipoToken.LLAVE_DERECHA)

    def class_inher(self):
        if self.currentToken.get_tipo() == TipoToken.MENOR_QUE:
            self.match(TipoToken.MENOR_QUE)
            self.match(TipoToken.IDENTIFICADOR)
        # si no es MENOR_QUE, asumimos épsilon

    def functions(self):
        if self.currentToken.get_tipo() == TipoToken.IDENTIFICADOR:
            self.function()
            self.functions()
        # si no es IDENTIFICADOR, asumimos épsilon
    def function(self):
        self.match(TipoToken.IDENTIFICADOR)
        self.match(TipoToken.PARENTESIS_IZQUIERDO)
        self.parameters_opc()
        self.match(TipoToken.PARENTESIS_DERECHO)
        self.block()

    def parameters_opc(self):
        if self.currentToken.get_tipo() == TipoToken.IDENTIFICADOR:
            self.parameters()
        # si no es IDENTIFICADOR, asumimos épsilon

    def parameters(self):
        self.match(TipoToken.IDENTIFICADOR)
        self.parameters_2()

    def parameters_2(self):
        if self.currentToken.get_tipo() == TipoToken.COMA:
            self.match(TipoToken.COMA)
            self.match(TipoToken.IDENTIFICADOR)
            self.parameters_2()
        # si no es COMA, asumimos épsilon

    def fun_decl(self):
        self.match(TipoToken.FUNCTION)
        self.function()

    def var_decl(self):
        self.match(TipoToken.VAR)
        self.match(TipoToken.IDENTIFICADOR)
        self.var_init()
        self.match(TipoToken.PUNTO_Y_COMA)

    def var_init(self):
        if self.currentToken.get_tipo() == TipoToken.ASIGNAR:
            self.match(TipoToken.ASIGNAR)
            self.expression()
        # si no es ASIGNAR, asumimos épsilon
    def statement(self):
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                      TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                      TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            self.expr_stmt()
        elif self.currentToken.get_tipo() == TipoToken.FOR:
            self.for_stmt()
        elif self.currentToken.get_tipo() == TipoToken.IF:
            self.if_stmt()
        elif self.currentToken.get_tipo() == TipoToken.PRINT:
            self.print_stmt()
        elif self.currentToken.get_tipo() == TipoToken.RETURN:
            self.return_stmt()
        elif self.currentToken.get_tipo() == TipoToken.WHILE:
            self.while_stmt()
        elif self.currentToken.get_tipo() == TipoToken.LLAVE_IZQUIERDA:
            self.block()
        else:
            raise Exception("Error en la línea " + str(self.currentToken.linea) + ". Se esperaba el inicio de una declaración o sentencia pero se encontró un " + str(self.currentToken.get_tipo()))

    def expr_stmt(self):
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                      TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                      TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            self.expression()
            self.match(TipoToken.PUNTO_Y_COMA)
        else:
            raise Exception("Error en la línea " + str(self.currentToken.linea) + ". Se esperaba una expresión válida " + str(self.currentToken.get_tipo()))

    def for_stmt(self):
        self.match(TipoToken.FOR)
        self.match(TipoToken.PARENTESIS_IZQUIERDO)
        self.for_stmt_1()
        self.for_stmt_2()
        self.for_stmt_3()
        self.match(TipoToken.PARENTESIS_DERECHO)
        self.statement()

    def for_stmt_1(self):
        if self.currentToken.get_tipo() == TipoToken.VAR:
            self.var_decl()
        elif self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE,
                                        TipoToken.NULL, TipoToken.NUMERO, TipoToken.CADENA,
                                        TipoToken.PARENTESIS_IZQUIERDO, TipoToken.IDENTIFICADOR,
                                        TipoToken.DIFERENTE, TipoToken.RESTA]:
            self.expr_stmt()
        elif self.currentToken.get_tipo() == TipoToken.PUNTO_Y_COMA:
            self.match(TipoToken.PUNTO_Y_COMA)
        else:
            raise Exception("Error en la línea " + str(self.currentToken.linea) + ". Se esperaba una expresión válida " + str(self.currentToken.get_tipo()))

    def for_stmt_2(self):
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                      TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                      TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            self.expression()
            self.match(TipoToken.PUNTO_Y_COMA)
        elif self.currentToken.get_tipo() == TipoToken.PUNTO_Y_COMA:
            self.match(TipoToken.PUNTO_Y_COMA)
        else:
            raise Exception("Error en la línea " + str(self.currentToken.linea) + ". Se esperaba una expresión válida " + str(self.currentToken.get_tipo()))

    def for_stmt_3(self):
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                      TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                      TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            self.expression()
        else:
            pass  # Asumimos épsilon

    def if_stmt(self):
        self.match(TipoToken.IF)
        self.match(TipoToken.PARENTESIS_IZQUIERDO)
        self.expression()
        self.match(TipoToken.PARENTESIS_DERECHO)
        self.statement()
        self.else_statement()

    def else_statement(self):
        if self.currentToken.get_tipo() == TipoToken.ELSE:
            self.match(TipoToken.ELSE)
            self.statement()
        else:
            pass  # Asumimos épsilon
    def print_stmt(self):
        self.match(TipoToken.PRINT)
        self.expression()
        self.match(TipoToken.PUNTO_Y_COMA)

    def return_stmt(self):
        self.match(TipoToken.RETURN)
        self.return_exp_opc()
        self.match(TipoToken.PUNTO_Y_COMA)

    def return_exp_opc(self):
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                      TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                      TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            self.expression()
        else:
            pass  # Asumimos épsilon

    def while_stmt(self):
        self.match(TipoToken.WHILE)
        self.match(TipoToken.PARENTESIS_IZQUIERDO)
        self.expression()
        self.match(TipoToken.PARENTESIS_DERECHO)
        self.statement()

    def block(self):
        self.match(TipoToken.LLAVE_IZQUIERDA)
        self.block_decl()
        self.match(TipoToken.LLAVE_DERECHA)

    def block_decl(self):
        if self.currentToken.get_tipo() in [TipoToken.CLASS, TipoToken.FUNCTION, TipoToken.VAR, TipoToken.FOR, TipoToken.IF,
                                      TipoToken.PRINT, TipoToken.RETURN, TipoToken.WHILE, TipoToken.LLAVE_IZQUIERDA,
                                      TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE,
                                      TipoToken.NULL, TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                      TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            self.declaration()
            self.block_decl()
        else:
            pass  # Asumimos épsilon

    def expression(self):
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                      TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                      TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            self.assignment()
        else:
            raise Exception("Error en la línea " + str(self.currentToken.get_linea()) + ". Se esperaba una expresion valida" + str(self.currentToken.get_tipo()))

    def assignment(self):
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                      TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                      TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            self.logic_or()
            self.assignment_opc()
        else:
            raise Exception("Error en la línea " + str(self.currentToken.get_linea()) + ". Se esperaba una expresion valida" + str(self.currentToken.get_tipo()))

    def assignment_opc(self):
        if self.currentToken.get_tipo() == TipoToken.ASIGNAR:
            self.match(TipoToken.ASIGNAR)
            self.expression()
        else:
            pass  # Asumimos épsilon
    def logic_or(self):
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                      TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                      TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            self.logic_and()
            self.logic_or_2()
        else:
            raise Exception("Error en la línea " + str(self.currentToken.get_linea()) + ". Se esperaba una expresion valida" + str(self.currentToken.get_tipo()))

    def logic_or_2(self):
        if self.currentToken.get_tipo() == TipoToken.OR:
            self.match(TipoToken.OR)
            self.logic_and()
            self.logic_or_2()
        else:
            pass  # Asumimos épsilon

    def logic_and(self):
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                      TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                      TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            self.equality()
            self.logic_and_2()
        else:
            raise Exception("Error en la línea " + str(self.currentToken.get_linea()) + ". Se esperaba una expresion valida" + str(self.currentToken.get_tipo()))

    def logic_and_2(self):
        if self.currentToken.get_tipo() == TipoToken.AND:
            self.match(TipoToken.AND)
            self.equality()
            self.logic_and_2()
        else:
            pass  # Asumimos épsilon

    def equality(self):
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                      TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                      TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            self.comparison()
            self.equality_2()
        else:
            raise Exception("Error en la línea " + str(self.currentToken.get_linea()) + ". Se esperaba una expresion valida" + str(self.currentToken.get_tipo()))

    def equality_2(self):
        if self.currentToken.get_tipo() == TipoToken.DIFERENTE:
            self.match(TipoToken.DIFERENTE)
            self.comparison()
            self.equality_2()
        elif self.currentToken.get_tipo() == TipoToken.IGUAL_A:
            self.match(TipoToken.IGUAL_A)
            self.comparison()
            self.equality_2()
        else:
            pass  # Asumimos épsilon

    def comparison(self):
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                      TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                      TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            self.term()
            self.comparison_2()
        else:
            raise Exception("Error en la línea " + str(self.currentToken.get_linea()) + ". Se esperaba una expresion valida" + str(self.currentToken.get_tipo()))

    def comparison_2(self):
        if self.currentToken.get_tipo() == TipoToken.MAYOR_QUE:
            self.match(TipoToken.MAYOR_QUE)
            self.term()
            self.comparison_2()
        elif self.currentToken.get_tipo() == TipoToken.MAYOR_O_IGUAL:
            self.match(TipoToken.MAYOR_O_IGUAL)
            self.term()
            self.comparison_2()
        elif self.currentToken.get_tipo() == TipoToken.MENOR_QUE:
            self.match(TipoToken.MENOR_QUE)
            self.term()
            self.comparison_2()
        elif self.currentToken.get_tipo() == TipoToken.MENOR_O_IGUAL:
            self.match(TipoToken.MENOR_O_IGUAL)
            self.term()
            self.comparison_2()
        else:
            pass  # Asumimos épsilon

    def term(self):
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                      TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                      TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            self.factor()
            self.term_2()
        else:
            raise Exception("Error en la línea " + str(self.currentToken.get_linea()) + ". Se esperaba una expresion valida" + str(self.currentToken.get_tipo()))


    def term_2(self):
        if self.currentToken.get_tipo() == TipoToken.RESTA:
            self.match(TipoToken.RESTA)
            self.factor()
            self.term_2()
        elif self.currentToken.get_tipo() == TipoToken.SUMA:
            self.match(TipoToken.SUMA)
            self.factor()
            self.term_2()
        else:
            pass  # Asumimos épsilon

    def factor(self):
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                      TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                      TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            self.unary()
            self.factor_2()
        else:
            raise Exception("Error en la línea " + str(self.currentToken.get_linea()) + ". Se esperaba una expresion valida" + str(self.currentToken.get_tipo()))

    def factor_2(self):
        if self.currentToken.get_tipo() == TipoToken.DIVISION:
            self.match(TipoToken.DIVISION)
            self.unary()
            self.factor_2()
        elif self.currentToken.get_tipo() == TipoToken.MULTIPLICACION:
            self.match(TipoToken.MULTIPLICACION)
            self.unary()
            self.factor_2()
        else:
            pass  # Asumimos épsilon

    def unary(self):
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                      TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                      TipoToken.IDENTIFICADOR]:
            self.call()
        elif self.currentToken.get_tipo() == TipoToken.DIFERENTE:
            self.match(TipoToken.DIFERENTE)
            self.unary()
        elif self.currentToken.get_tipo() == TipoToken.RESTA:
            self.match(TipoToken.RESTA)
            self.unary()
        else:
            raise Exception("Error en la línea " + str(self.currentToken.get_linea()) + ". Se esperaba una expresion valida" + str(self.currentToken.get_tipo()))

    def call(self):
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                      TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                      TipoToken.IDENTIFICADOR]:
            self.primary()
            self.call_2()
        else:
            raise Exception("Error en la línea " + str(self.currentToken.get_linea()) + ". Se esperaba una expresion valida" + str(self.currentToken.get_tipo()))

    def call_2(self):
        if self.currentToken.get_tipo() == TipoToken.PARENTESIS_IZQUIERDO:
            self.match(TipoToken.PARENTESIS_IZQUIERDO)
            self.arguments_opc()
            self.match(TipoToken.PARENTESIS_DERECHO)
            self.call_2()
        elif self.currentToken.get_tipo() == TipoToken.PUNTO:
            self.match(TipoToken.PUNTO)
            self.match(TipoToken.IDENTIFICADOR)
            self.call_2()
        else:
            pass  # Asumimos épsilon

    def call_opc(self):
        # TODO: Implementar según la gramática
        pass

    def primary(self):
        if self.currentToken.get_tipo() == TipoToken.THIS:
            self.match(TipoToken.THIS)
        elif self.currentToken.get_tipo() == TipoToken.SUPER:
            self.match(TipoToken.SUPER)
            self.match(TipoToken.PUNTO)
            self.match(TipoToken.IDENTIFICADOR)
        elif self.currentToken.get_tipo() == TipoToken.FALSE:
            self.match(TipoToken.FALSE)
        elif self.currentToken.get_tipo() == TipoToken.TRUE:
            self.match(TipoToken.TRUE)
        elif self.currentToken.get_tipo() == TipoToken.NULL:
            self.match(TipoToken.NULL)
        elif self.currentToken.get_tipo() == TipoToken.NUMERO:
            self.match(TipoToken.NUMERO)
        elif self.currentToken.get_tipo() == TipoToken.CADENA:
            self.match(TipoToken.CADENA)
        elif self.currentToken.get_tipo() == TipoToken.PARENTESIS_IZQUIERDO:
            self.match(TipoToken.PARENTESIS_IZQUIERDO)
            self.expression()
            self.match(TipoToken.PARENTESIS_DERECHO)
        elif self.currentToken.get_tipo() == TipoToken.IDENTIFICADOR:
            self.match(TipoToken.IDENTIFICADOR)
        else:
            raise Exception("Error en la línea " + str(self.currentToken.get_linea()) + ". Se esperaba una expresion valida" + str(self.currentToken.get_tipo()))

    def arguments_opc(self):
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                      TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                      TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            self.arguments()
        else:
            pass  # Asumimos épsilon

    def arguments(self):
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                      TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                      TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            self.expression()
            self.arguments_2()
        else:
            raise Exception("Error en la línea " + str(self.currentToken.get_linea()) + ". Se esperaba una expresion valida" + str(self.currentToken.get_tipo()))
    def arguments_2(self):
        if self.currentToken.get_tipo() == TipoToken.COMA:
            self.match(TipoToken.COMA)
            self.expression()
            self.arguments_2()
        else:
            pass  # Asumimos épsilon

    def match(self, type):
        if self.currentToken.get_tipo() == type:
            if self.currentToken.get_tipo() != TipoToken.EOF:
                self.avanzar()
        else:
            error_message = "Error en la línea " + str(self.currentToken.get_linea()) + ". Se esperaba un " + str(type) + " pero se encontró un " + str(self.currentToken.get_tipo())
            raise Exception(error_message)

    def avanzar(self):
        try:
            self.currentToken = self.tokens[self.tokens.index(self.currentToken) + 1]
        except IndexError:
            raise Exception("Se llegó al final de los tokens sin encontrar EOF.")