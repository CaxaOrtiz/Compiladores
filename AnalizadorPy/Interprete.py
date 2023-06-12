import sys
from typing import List
from Escaner import Escaner
from Token import Token
from Analizador import Analizador

existenErrores = False

def main(args: List[str]) -> None:
    if len(args) > 1:
        print("Uso correcto: interprete [script]")
        sys.exit(64)
    elif len(args) == 1:
        print("Ejecutanto Archivo..")
        ejecutarArchivo(args[0])
    else:
        ejecutarPrompt()

def ejecutarArchivo(path: str) -> None:
    with open(path, "r") as archivo:
        source = archivo.read()
        ejecutar(source)

    if existenErrores:
        sys.exit(65)

def ejecutarPrompt() -> None:
    print("Ingresa los comandos a validar:")
    while True:
        linea = input(">>> ")
        if not linea:
            break

        ejecutar(linea)
        global existenErrores
        existenErrores = False

def ejecutar(source: str) -> str:
    scanner = Escaner(source)
    tokens = scanner.scan_tokens()

   

    analiza = Analizador(tokens)
    return analiza.analisis()

def error(linea: int, mensaje: str) -> None:
    reportar(linea, "", mensaje)

def reportar(linea: int, donde: str, mensaje: str) -> None:
    print(f"[linea {linea}] Error {donde}: {mensaje}", file=sys.stderr)
    global existenErrores
    existenErrores = True

if __name__ == "__main__":
    main(sys.argv[1:])
