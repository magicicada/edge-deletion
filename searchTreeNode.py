class Node:

    def __init__(self, parent, edges):
        self.parent = parent
        self.edges = edges
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def get_childen(self):
        return self.children

    def get_parent(self):
        return self.parent

    def __str__(self):
        return ', '.join(map(str,self.edges)) + "\n" + ', '.join(map(str,self.children))
    
