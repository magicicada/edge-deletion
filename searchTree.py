import searchTreeNode as nd
import graphFunctions as gf
import Queue

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
    def spawn_children(node, number):
        if len(node.get_edges()) >= number:
            for index in range(node.get_rightmost_deleted(),len(node.edges)):
                child_node = nd.Node(node,node.edges[:index]+node.edges[index+1:],index)
                node.add_child(child_node)
                SearchTree.spawn_children(child_node, number)

    def fill(self, edges, number):
        if self.is_empty():
            root = self.set_root(nd.Node(None, edges, 0))
            SearchTree.spawn_children(root, number)

    def __str__(self):
        return self.root

    def breadth_first_search(self, number):
        all_edges = self.root.get_edges()
        queue = Queue.Queue()
        queue.put(self.root)
        while not queue.empty():
            current_node = queue.get()
            current_node_edges = current_node.get_edges()
            if gf.is_edge_set_disconnected(number, current_node_edges):
                deleted_edges = []
                for edge in all_edges:
                    if edge not in current_node_edges:
                        deleted_edges.append(edge)
                return deleted_edges
            children = current_node.get_children()
            for child in children:
                queue.put(child)
        return "Impossible"

tree = SearchTree()
tree.fill([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],10)
print tree.root
