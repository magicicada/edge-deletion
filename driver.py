import graphFunctions
import searchTree
import time

# Name of the file containing edges for the graph
FILENAME = "SampleGraph1"

graph = graphFunctions.read_edges_from_file(FILENAME)
tree = searchTree.SearchTree()
print "Working on a graph with", graph.number_of_nodes(), "vertices"
tree.fill(graph.edges())

# Code to track execution time
print "Starting search..."
start_time = time.time()

# Change search method HERE --v
minEdges = tree.breadth_first_search(61)

elapsed_time = time.time()-start_time
print "Miminum deletions necessary are: ", minEdges
#print "That is ", len(minEdges), "edges"
print "It took: ", elapsed_time, "seconds"
