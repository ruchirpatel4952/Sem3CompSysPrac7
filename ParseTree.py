# class ParseException(Exception):
#     """
#     Raised when tokens provided don't match the expected grammar
#     Use this with `raise ParseException("My error message")`
#     """
#     pass


# class ParseTree():

#     def __init__(self, node_type, value):
#         """
#         A node in a Parse Tree data structure
#         @param node_type The type of node (see element types).
#         @param value The node's value. Should only be used on terminal nodes/leaves, and empty otherwise.
#         """
#         self.node_type = node_type
#         self.value = value
#         self.children = []
    

#     def addChild(self,child):
#         """
#         Adds a ParseTree as a child of this ParseTree
#         @param child The ParseTree to add
#         """
#         self.children.append(child)
    

#     def getChildren(self):
#         """
#         Get a list of child nodes in the order they were added.
#         @return A LinkedList of ParseTrees
#         """
#         return self.children
    

#     def getType(self):
#         """
#         Get the type of this ParseTree Node
#         @return The type of node (see element types).
#         """
#         return self.node_type
    

#     def getValue(self):
#         """
#         Get the value of this ParseTree Node
#         @return The node's value. Should only be used on terminal nodes/leaves, and empty otherwise.
#         """
#         return self.value
    

#     def __str__(self,depth=0):
#         """
#         Generate a string from this ParseTree
#         @return A printable representation of this ParseTree with indentation
#         """        
#         # Set indentation
#         indent = ""
#         for i in range(0,depth):
#             indent += "  \u2502 "
        
#         # Generate output
#         output = ""
#         if(len(self.children)>0):
#             # Output if the node has children
#             output += self.node_type + "\n"
#             for child in children:
#                 output += indent + "  \u2514 " + child.__str__(depth+1)
            
#             output += indent + "\n"
#         else :
#             # Output if the node is a leaf/terminal
#             output += self.node_type + " " + self.value + "\n"
        
#         return output

    

# class Token(ParseTree):

#     """
#     Token for parsing. Can be used as a terminal node in a ParseTree
#     """
#     pass
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

    def match(self, expected_list):
        if self.type != expected_list[0]:
            return False
        expected_list.pop(0)
        for child in self.children:
            if isinstance(child, ParseTree):
                if not child.match(expected_list):
                    return False
            else:
                if child != expected_list.pop(0):
                    return False
        return True

    def __repr__(self):
        return f"ParseTree({self.type}, {self.value}, {self.children})"

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def getType(self):
        return self.type

    def getValue(self):
        return self.value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"
