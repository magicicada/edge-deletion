import searchTreeNode as nd

class SearchTree:

    def __init__(self):
        self.root = None

    def root(self):
        return self.root

    def set_root(self, node):
        self.root = node
        return node

    def is_empty(self):
        return self.root == None

    @staticmethod
    def spawn_children(node):
        if len(node.edges)>1:
            for index in range(len(node.edges)):
                child_node = nd.Node(node,node.edges[:index]+node.edges[index+1:])
                node.add_child(child_node)
                SearchTree.spawn_children(child_node)

    def fill(self, edges):
        if self.is_empty():
            root = self.set_root(nd.Node(None, edges))
            SearchTree.spawn_children(root)

    def __str__(self):
        return self.root


