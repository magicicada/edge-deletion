import networkx as nx

# Reads in edges from a file. The edges are stored in
# tuples, one tuple per line. Each tuple holds the numbers
# of the two vertices at the endpoints of the edge that the
# tuple represents.
# Input - the filename of the file holding the data for the edges
# Output - a graph object with all of the vertices and edges.
def read_edges_from_file(filename):
    f = open(filename, "r")
    graph = nx.Graph()
    currentLine = f.readline()
    while(currentLine != ""):
        # Remove unwanted characters and add in the new edge
        cleanedLine = currentLine.strip().split(",")
        firstVertex = cleanedLine[0]
        secondVertex = cleanedLine[1]
        graph.add_edge(firstVertex,secondVertex)
        currentLine = f.readline()
    f.close()
    return graph

# Calculates the maximum size of a component in a graph
# Input - a graph object
# Output - an integer number; the maximum component size
def maximum_component_size(graph):
    maximum = 0
    # Loop over all components to find maximum
    for component in nx.connected_components(graph):
        if len(component) > maximum:
            maximum = len(component)
    return maximum

# Checks whether the maximum component size is less than a given number
# Input - an integer to check against
# Output - a boolean value:
#     True -> the maximum component size is less than or equal to the number
#     False -> the maximum component size is more than the number
def maximum_at_most(graph, number):
    maximum = maximum_component_size(graph)
    return maximum <= number
