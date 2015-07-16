class Node:

    def __init__(self, parent, edges, rightmost_deleted):
        self.parent = parent
        self.edges = edges
        self.children = []
        self.rightmost_deleted = rightmost_deleted

    def add_child(self, node):
        self.children.append(node)

    def get_parent(self):
        return self.parent

    def get_edges(self):
        return self.edges

    def get_children(self):
        return self.children

    def get_rightmost_deleted(self):
        return self.rightmost_deleted

    def __str__(self):
        return ', '.join(map(str,self.edges)) + "\n" + ', '.join(map(str,self.children))
    
