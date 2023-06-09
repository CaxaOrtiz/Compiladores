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
        # Comprueba el tipo de token actual
        if self.currentToken.get_tipo() == TipoToken.CLASS:
            # Si es un token de tipo CLASS, llama a la función class_decl() para procesar la declaración de clase
            self.class_decl()
            # Después de procesar una declaración de clase, llama a sí misma nuevamente para procesar la siguiente declaración
            self.declaration()
        elif self.currentToken.get_tipo() == TipoToken.FUNCTION:
            # Si es un token de tipo FUNCTION, llama a la función fun_decl() para procesar la declaración de función
            self.fun_decl()
            # Después de procesar una declaración de función, llama a sí misma nuevamente para procesar la siguiente declaración
            self.declaration()
        elif self.currentToken.get_tipo() == TipoToken.VAR:
            # Si es un token de tipo VAR, llama a la función var_decl() para procesar la declaración de variable
            self.var_decl()
            # Después de procesar una declaración de variable, llama a sí misma nuevamente para procesar la siguiente declaración
            self.declaration()
        elif self.currentToken.get_tipo() in [TipoToken.FOR, TipoToken.IF, TipoToken.PRINT, TipoToken.RETURN, TipoToken.WHILE, TipoToken.LLAVE_IZQUIERDA, TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL, TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO, TipoToken.IDENTIFICADOR, TipoToken.NEGACION, TipoToken.RESTA]:
            # Si el tipo de token actual se encuentra en la lista de tipos de tokens que representan sentencias,
            # llama a la función statement() para procesar la sentencia
            self.statement()
            # Después de procesar una sentencia, llama a sí misma nuevamente para procesar la siguiente declaración
            self.declaration()
        else:
            # Si no se cumple ninguna de las condiciones anteriores, se asume que es épsilon (un caso base o fin de la recursión)
            pass
        
    def class_decl(self):
        # Coincide con el token de tipo CLASS
        self.match(TipoToken.CLASS)
        # Coincide con el token de tipo IDENTIFICADOR (nombre de la clase)
        self.match(TipoToken.IDENTIFICADOR)
        # Verifica si hay herencia de clase
        self.class_inher()
        # Coincide con el token de apertura de llave {
        self.match(TipoToken.LLAVE_IZQUIERDA)
        # Procesa las funciones dentro de la clase
        self.functions()
        # Coincide con el token de cierre de llave }
        self.match(TipoToken.LLAVE_DERECHA)

    def class_inher(self):
        # Verifica si hay un token de tipo MENOR_QUE (indicador de herencia de clase)
        if self.currentToken.get_tipo() == TipoToken.MENOR_QUE:
            # Coincide con el token MENOR_QUE
            self.match(TipoToken.MENOR_QUE)
            # Coincide con el token de tipo IDENTIFICADOR (nombre de la clase de la que hereda)
            self.match(TipoToken.IDENTIFICADOR)
        # Si no hay token MENOR_QUE, asumimos épsilon (no hay herencia)

    def functions(self):
        # Verifica si el token actual es de tipo IDENTIFICADOR (nombre de función)
        if self.currentToken.get_tipo() == TipoToken.IDENTIFICADOR:
            # Procesa la función actual
            self.function()
            # Procesa las funciones restantes en la clase
            self.functions()
        # Si no hay token IDENTIFICADOR, asumimos épsilon (no hay más funciones)

    def function(self):
        # Coincide con el token de tipo IDENTIFICADOR (nombre de función)
        self.match(TipoToken.IDENTIFICADOR)
        # Coincide con el token de apertura de paréntesis (
        self.match(TipoToken.PARENTESIS_IZQUIERDO)
        # Procesa los parámetros opcionales de la función
        self.parameters_opc()
        # Coincide con el token de cierre de paréntesis )
        self.match(TipoToken.PARENTESIS_DERECHO)
        # Procesa el bloque de código de la función
        self.block()
    
    def parameters_opc(self):
    # Verifica si el token actual es de tipo IDENTIFICADOR (nombre de parámetro)
        if self.currentToken.get_tipo() == TipoToken.IDENTIFICADOR:
        # Procesa los parámetros
            self.parameters()
    # Si no es un token IDENTIFICADOR, asumimos épsilon (no hay parámetros)

    def parameters(self):
    # Coincide con el token de tipo IDENTIFICADOR (nombre de parámetro)
        self.match(TipoToken.IDENTIFICADOR)
    # Procesa los parámetros adicionales
        self.parameters_2()

    def parameters_2(self):
        # Verifica si el token actual es de tipo COMA (separador de parámetros)
        if self.currentToken.get_tipo() == TipoToken.COMA:
            # Coincide con el token COMA
            self.match(TipoToken.COMA)
            # Coincide con el token de tipo IDENTIFICADOR (nombre de parámetro)
            self.match(TipoToken.IDENTIFICADOR)
            # Procesa los parámetros adicionales
            self.parameters_2()
        # Si no hay un token COMA, asumimos épsilon (no hay más parámetros)

    def fun_decl(self):
        # Coincide con el token de tipo FUNCTION
        self.match(TipoToken.FUNCTION)
        # Procesa la declaración de la función
        self.function()

    def var_decl(self):
    # Coincide con el token de tipo VAR
        self.match(TipoToken.VAR)
    # Coincide con el token de tipo IDENTIFICADOR (nombre de la variable)
        self.match(TipoToken.IDENTIFICADOR)
    # Inicializa la variable (asignación opcional)
        self.var_init()
    # Coincide con el token de tipo PUNTO_Y_COMA (finalización de la declaración)
        self.match(TipoToken.PUNTO_Y_COMA)

    def var_init(self):
        # Verifica si el token actual es de tipo ASIGNAR (operador de asignación)
        if self.currentToken.get_tipo() == TipoToken.ASIGNAR:
            # Coincide con el token ASIGNAR
            self.match(TipoToken.ASIGNAR)
            # Analiza la expresión a asignar
            self.expression()
        # Si no hay un token ASIGNAR, asumimos épsilon (no hay asignación)

    def statement(self):
        # Verifica el tipo del token actual para determinar qué tipo de sentencia o declaración se espera
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                    TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                    TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            # La sentencia es una expresión, por lo que se llama a expr_stmt() para analizarla
            self.expr_stmt()
        elif self.currentToken.get_tipo() == TipoToken.FOR:
            # La sentencia es un bucle FOR, por lo que se llama a for_stmt() para analizarlo
            self.for_stmt()
        elif self.currentToken.get_tipo() == TipoToken.IF:
            # La sentencia es una estructura IF, por lo que se llama a if_stmt() para analizarlo
            self.if_stmt()
        elif self.currentToken.get_tipo() == TipoToken.PRINT:
            # La sentencia es una instrucción PRINT, por lo que se llama a print_stmt() para analizarlo
            self.print_stmt()
        elif self.currentToken.get_tipo() == TipoToken.RETURN:
            # La sentencia es una instrucción RETURN, por lo que se llama a return_stmt() para analizarlo
            self.return_stmt()
        elif self.currentToken.get_tipo() == TipoToken.WHILE:
            # La sentencia es un bucle WHILE, por lo que se llama a while_stmt() para analizarlo
            self.while_stmt()
        elif self.currentToken.get_tipo() == TipoToken.LLAVE_IZQUIERDA:
            # La sentencia es un bloque de código, por lo que se llama a block() para analizarlo
            self.block()
        else:
            # Si no se reconoce el tipo de sentencia, se lanza una excepción
            raise Exception("Error en la línea " + str(self.currentToken.linea) + ". Se esperaba el inicio de una declaración o sentencia pero se encontró un " + str(self.currentToken.get_tipo()))

    def expr_stmt(self):
    # Verifica si el token actual es uno de los tipos de token que pueden comenzar una expresión
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                    TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                    TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            # Analiza la expresión llamando al método expression()
            self.expression()
            # Coincide con el token de tipo PUNTO_Y_COMA (finalización de la expresión)
            self.match(TipoToken.PUNTO_Y_COMA)
        else:
            # Si el tipo del token actual no coincide con los tipos de token esperados, se lanza una excepción
            raise Exception("Error en la línea " + str(self.currentToken.linea) + ". Se esperaba una expresión válida " + str(self.currentToken.get_tipo()))

    def for_stmt(self):
        # Coincide con el token FOR
        self.match(TipoToken.FOR)
        # Coincide con el token PARENTESIS_IZQUIERDO
        self.match(TipoToken.PARENTESIS_IZQUIERDO)
        # Analiza la primera parte del bucle FOR llamando al método for_stmt_1()
        self.for_stmt_1()
        # Analiza la segunda parte del bucle FOR llamando al método for_stmt_2()
        self.for_stmt_2()
        # Analiza la tercera parte del bucle FOR llamando al método for_stmt_3()
        self.for_stmt_3()
        # Coincide con el token PARENTESIS_DERECHO
        self.match(TipoToken.PARENTESIS_DERECHO)
        # Analiza la sentencia dentro del bucle FOR llamando al método statement()
        self.statement()

    def for_stmt_1(self):
        # Verifica el tipo del token actual para determinar qué tipo de expresión o declaración se espera
        if self.currentToken.get_tipo() == TipoToken.VAR:
            # La primera parte del bucle FOR es una declaración de variable, por lo que llama a var_decl() para analizarlo
            self.var_decl()
        elif self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE,
                                        TipoToken.NULL, TipoToken.NUMERO, TipoToken.CADENA,
                                        TipoToken.PARENTESIS_IZQUIERDO, TipoToken.IDENTIFICADOR,
                                        TipoToken.DIFERENTE, TipoToken.RESTA]:
            # La primera parte del bucle FOR es una expresión, por lo que llama a expr_stmt() para analizarlo
            self.expr_stmt()
        elif self.currentToken.get_tipo() == TipoToken.PUNTO_Y_COMA:
            # La primera parte del bucle FOR es un punto y coma (épsilon), lo que significa que no hay una expresión o declaración en esta parte
            self.match(TipoToken.PUNTO_Y_COMA)
        else:
            # Si el tipo del token actual no coincide con los tipos de token esperados, se lanza una excepción
            raise Exception("Error en la línea " + str(self.currentToken.linea) + ". Se esperaba una expresión válida " + str(self.currentToken.get_tipo()))
    
    def for_stmt_2(self):
    # Verifica si el token actual es uno de los tipos de token que pueden comenzar una expresión
        if self.currentToken.get_tipo() in [TipoToken.THIS, TipoToken.SUPER, TipoToken.FALSE, TipoToken.TRUE, TipoToken.NULL,
                                    TipoToken.NUMERO, TipoToken.CADENA, TipoToken.PARENTESIS_IZQUIERDO,
                                    TipoToken.IDENTIFICADOR, TipoToken.DIFERENTE, TipoToken.RESTA]:
            # Analiza la expresión llamando al método expression()
            self.expression()
            # Coincide con el token de tipo PUNTO_Y_COMA (finalización de la expresión)
            self.match(TipoToken.PUNTO_Y_COMA)
        elif self.currentToken.get_tipo() == TipoToken.PUNTO_Y_COMA:
            # Si el tipo del token actual es PUNTO_Y_COMA, significa que esta parte del bucle FOR es un punto y coma (épsilon), no se requiere una expresión
            self.match(TipoToken.PUNTO_Y_COMA)
        else:
            # Si el tipo del token actual no coincide con los tipos de token esperados, se lanza una excepción
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