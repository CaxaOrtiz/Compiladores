
class CharArrayManager:
    def __init__(self, array: list):
        self.array = array
        self.index = 0

    def getNextChar(self):
        try:
            if self.index < len(self.array):
                char = self.array[self.index]
                self.index += 1
                return char
            return None
        except:
            return None

    def backPosition(self):
        self.index -= 1

    def show_characters(self):
        print(len(self.array))
        for i in range(len(self.array)):
            char = self.array[i]
            special_chars = ""
            if char == '\n':
                special_chars += " salto de linea \\n"
            if char == '\r':
                special_chars += " retorno de carro \\r"
            if char == '\t':
                special_chars += " tabulador \\t"
            print(char + " posicion:" + str(i) + special_chars)

    def hasNext(self):
        return self.index < len(self.array)