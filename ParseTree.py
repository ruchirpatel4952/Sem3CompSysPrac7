class ParseTree:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        self.children = []

    def addChild(self, child):
        self.children.append(child)

    def getType(self):
        return self.type

    def getValue(self):
        return self.value

    def __repr__(self):
        return f"ParseTree(type={self.type}, value={self.value}, children={self.children})"
