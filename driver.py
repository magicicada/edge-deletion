import graphFunctions
import searches
import time

# Name of the file containing edges for the graph
FILENAME = "SampleGraph1"

graph = graphFunctions.read_edges_from_file(FILENAME)

# Code to track execution time
start_time = time.time()

# Change search method HERE --v
minEdges = searches.simple_search(graph, 12)

elapsed_time = time.time()-start_time
print "Miminum deletions necessary are: ", minEdges
print "It took: ", elapsed_time, "seconds"
