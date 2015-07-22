import searchTreeNode as nd
import networkx as nx
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

    def __str__(self):
        return self.root

    def breadth_first_search(self, comp_size_limit, max_deletions):
        all_edges = self.root.get_edges()
        min_remaining = len(all_edges) - max_deletions

        graph = nx.Graph()
        for edge in all_edges:
            graph.add_edge(edge[0],edge[1])
        number_vertices = nx.number_of_nodes(graph)
        
        queue = Queue.Queue()
        queue.put(self.root)
        while not queue.empty():
            current_node = queue.get()
            if current_node.enough_deletions_allowed(comp_size_limit, min_remaining, number_vertices):
                current_node_edges = current_node.get_edges()
                if gf.is_edge_set_disconnected(comp_size_limit, current_node_edges):
                    deleted_edges = []
                    for edge in all_edges:
                        if edge not in current_node_edges:
                            deleted_edges.append(edge)
                    return deleted_edges
                children = current_node.spawn_children(min_remaining)
                for child in children:
                    queue.put(child)
        return "Impossible"

#tree = SearchTree()
#edges = [[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[10,12],[9,10],[10,11],[11,12],[12,13],[13,14],[14,15],[15,16],[16,17],[17,18],[18,19],[19,20]]
#tree.set_root(nd.Node(edges, 0))
#print tree.breadth_first_search(10,2)

