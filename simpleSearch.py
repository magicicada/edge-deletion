import networkx as nx
import graphFunctions

# A naive and simple search that loops over all possible sets of edges
# Input: graph - a graph object containing the graph of interest
#        maxSize - an integer signifying the maximum component size
# Output: an integer; the minimum number of edges to be removed
def simple_search(graph, maxSize):
    minRemovals = len(graph.edges())
    # Create the powerset of all possible edge combinations
    for edges in powerset(graph.edges()):
        # test if it is a solution
        if graphFunctions.is_edge_set_disconnecting(graph, maxSize, edges):
            # record the minimun number of edges needed
            if minRemovals > len(edges):
                minRemovals = len(edges)
    return minRemovals

def A_star_search(graph, maxSize):
    

# A function to compute the powerset of a given set
# Input - a set of items (any collection should work)
# Output - a generator that gives all of the items
# in the powerset of the initial set.
def powerset(items):
    # Terminating case
    if len(items) <= 1:
        yield []
        yield items
    else:
        # Recursively divide the set into sections of decreasing length
        for item in powerset(items[1:]):
            yield item
            yield [items[0]] + item
