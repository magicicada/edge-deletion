import math

class Node:

    def __init__(self, edges, rightmost_deleted):
#        self.parent = parent
        self.edges = edges
#        self.children = []
        self.rightmost_deleted = rightmost_deleted

#    def add_child(self, node):
#        self.children.append(node)

#    def get_parent(self):
#        return self.parent

    def get_edges(self):
        return self.edges

#    def get_children(self):
#        return self.children

    def get_rightmost_deleted(self):
        return self.rightmost_deleted

    def spawn_children(self, min_num_edges=0):
        children = []
        if len(self.edges) > min_num_edges:
            for index in range(self.rightmost_deleted,len(self.edges)):
                child_node = Node(self.edges[:index]+self.edges[index+1:],index)
                children.append(child_node)
        return children

    def enough_deletions_allowed(self, comp_size_limit, min_remaining, num_vertices):
        num_edges_allowed = math.ceil(float(num_vertices)/comp_size_limit)*(comp_size_limit*(comp_size_limit-1)/2)
        return num_edges_allowed >= min_remaining

    def __str__(self):
        return ', '.join(map(str,self.edges)) + "\n" + ', '.join(map(str,self.children))
    

#node = Node(None,[1,2,3],0)
#print node
#node.spawn_children()
#print node
