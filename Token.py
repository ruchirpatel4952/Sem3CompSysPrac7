class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def getType(self):
        return self.type

    def getValue(self):
        return self.value

    def __str__(self):
        return f'Token(type={self.type}, value={self.value})'
