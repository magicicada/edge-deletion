import networkx as nx
import pydot
import EdgeDeletion as ed
import graphFunctions as gf
INFINITY = 999999999

# General function used to invoke the algorithm
# Input - graph - the graph of interest for the algorithm
#       - nice_decomposition - a nice tree decomposition of that graph
#       - root - the root of the nice tree decomposition (it might be possible to drop this)
#       - h - maximum size of the compoments
#       - k - maximum number of deleted edges
# Output - a set of delValues for the root of the nice tree decomposition
def apply_algorithm(graph, nice_decomposition, root, h, k):    
    # Get root's children
    children = get_all_neighbours(nice_decomposition, root)

    # We now have a nice tree decomposition.
    # Figure out delValues for the root:
    delValues = get_del_values(graph, nice_decomposition, root, children, h, k)

    return delValues

# Creates a nice tree decomposition from the tree decomposition provided
# Input - decomp - a tree decomposition
#       - root - the node for the root of the tree decomposition (and for the nice one)
# Output - a nice tree decomposition graph
def get_nice_tree_decomp(decomp, root):
    # Remove not needed quotation marks and trailing whitespace
    for node in decomp:
        decomp.node[node]["label"] = decomp.node[node]["label"].replace('"', '').strip()
    root = root.replace('"', '').strip()
    
    children = get_all_neighbours(decomp, root)
    make_it_nice(decomp, root, children)

    # Remove any nodes that are not INTRODUCE, FORGET, JOIN or LEAF (essentially duplicate nodes)
    nodes = decomp.nodes()
    for node in nodes:
        if decomp.node[node]["kind"] == "":
            neighbours = get_all_neighbours(decomp, node)
            if len(neighbours) == 2:
                decomp.add_edge(neighbours[0], neighbours[1])
                decomp.remove_node(node)
            else:
                print "ERROR"
    
    return decomp

# Calculates the delValues of the given node. If the node is a LEAF, the delValues are
# calculated based on the node itself, otherwise the function makes a recursive call to itself.
# Input - graph - the graph of interest for the algorithm
#       - decomp - a nice tree decomposition of that graph
#       - node - the given node
#       - h - maximum size of the compoments
#       - k - maximum number of deleted edges
# Output - a set of delValues for the given node
def get_del_values(graph, decomp, node, children, h, k):
    kind = ""
    try:
        kind = decomp.node[node]["kind"]
    except:
        pass
    bag = decomp.node[node]["label"].strip().split(" ")
    delValues = []
    if kind == "JOIN":
        delValuesChild1 = get_del_values(graph, decomp, children[0], get_all_children(decomp, children[0], node),h,k)
        delValuesChild2 = get_del_values(graph, decomp, children[1], get_all_children(decomp, children[1], node),h,k)
        #print "Getting delValues for", kind, "node", node, "with bag", bag, "and children", children
        delValues = ed.sigOfJoin(None, None, bag, graph, None, None, None, None, delValuesChild1, delValuesChild2, h, k)

    elif kind == "INTRODUCE":
        child_bag = decomp.node[children[0]]["label"].strip().split(" ")
        delValuesChild = get_del_values(graph, decomp, children[0], get_all_children(decomp, children[0], node),h,k)
        #print "Getting delValues for", kind, "node", node, "with bag", bag, "and children", children
        delValues = ed.sigOfIntroduce(None, None, bag, graph, None, child_bag, delValuesChild, h, k)

    elif kind == "FORGET":
        child_bag = decomp.node[children[0]]["label"].strip().split(" ")
        delValuesChild = get_del_values(graph, decomp, children[0], get_all_children(decomp, children[0], node),h,k)
        #print "Getting delValues for", kind, "node", node, "with bag", bag, "and children", children
        delValues = ed.sigOfForget(None, None, bag, graph, None, child_bag, delValuesChild, h, k)

    elif kind == "LEAF":
        #print "Getting delValues for", kind, "node", node, "with bag", bag, "and children", children
        delValues = ed.sigOfLeaf(None, None, bag, graph, h, k)
        #for guy in delValues:
        #    if delValues[guy] != INFINITY:
        #        print str(guy) + " | " + str(delValues[guy])

    # This should not be needed anymore
    else:
        delValues = get_del_values(graph, decomp, children[0], get_all_children(decomp, children[0], node),h,k)
        #print "This one is a duplicate"

    return delValues
                                      
# A recursive function used to create a nice tree decomposition from a tree decomposition.
# Input - graph - the tree decomposition of interest
#       - node - the node currently being "nice-ify-ed" (root at the beginning)
#       - children - a list of the children of the given node
def make_it_nice(graph, node, children):
    bag = graph.node[node]["label"]
    #print "Fixing vertex", node, "with children", children, "and bag", bag
    if len(children) > 1:
        #print "vertex",node," is a JOIN because len(children) = ", len(children)
        graph.node[node]["kind"] = "JOIN"
        # Introduce more Join nodes if there are too many children (or 2 different children)
        # Otherwise continue down the tree
        if len(children) != 2 or (graph.node[node]["label"] != graph.node[children[0]]["label"]
                                  or graph.node[children[0]]["label"] != graph.node[children[1]]["label"]):
            count = 0
            # Remove all children
            for child in children:
                graph.remove_edge(node, child)
            # Create additional nodes. Half would have 1 of the original children as a child and
            # would turn out to be either Intoduce or Forget nodes and the other half would be
            # Join nodes to which the Introduce/Forget nodes would be linked to.
            # Goal is to create a ladder-like structure.
            cursor = node
            start_vertex = graph.number_of_nodes()+1
            for i in range(len(children)-1):
                graph.node[cursor]['kind'] = "JOIN"
                #print "Now is a join node ", cursor
                vertex_num = graph.number_of_nodes()+1
                graph.add_node(vertex_num, label=str(bag).strip())
                #print "adding holder node ", vertex_num, "with bag", bag, "node=", node
                graph.add_edge(cursor, vertex_num)
                graph.add_edge(vertex_num, children[i])
                graph.add_node(vertex_num+1, label=str(bag).strip())
                #print "adding join node ", vertex_num+1, "with bag", bag
                graph.add_edge(cursor, vertex_num+1)
                cursor = vertex_num+1
            graph.add_edge(cursor, children[-1])
            # JOIN nodes now added. Recursively call this function to fix all of the original children,
            # i.e. decide whether is is going to be an introduce or forget node.
            #print "start_vertex = ", start_vertex
            #print "node = ", node
            #print "children = ", get_all_children(graph, start_vertex, node)
            make_it_nice(graph, start_vertex, get_all_children(graph, start_vertex, node))
            for i in range(start_vertex+2, cursor, 2):
                make_it_nice(graph, i, get_all_children(graph, i, i-1))
            if cursor-2 < start_vertex:
                last_parent = node
            else:
                last_parent = cursor - 2
            make_it_nice(graph, cursor, get_all_children(graph, cursor, last_parent))
        # In this case we were lucky and there is indeed a Join node where one was supposed to be. Just carry on.
        else:
            make_it_nice(graph,children[0], get_all_children(graph, children[0], node))
            make_it_nice(graph,children[1], get_all_children(graph, children[1], node))
            return
    # Here we need either Introduce or Forget nodes.
    elif len(children) == 1:
        #print "vertex",node," is a Int/Forget because len(children) = ", len(children)
        # Find out how information in the two bags differs
        child_bag = graph.node[children[0]]['label']
        child_bag = child_bag.strip().split(" ")
        bag = bag.strip().split(" ")
        #print "b=",bag
        #print "c=",child_bag
        forgotten = [vertex for vertex in child_bag if vertex not in bag]
        introduced = [vertex for vertex in bag if vertex not in child_bag]
        # Add Introduce and Forget nodes as necessary
        graph.remove_edge(node,children[0])
        cursor = node
        current_bag = bag
        for vertex in introduced:
            graph.node[cursor]["kind"] = "INTRODUCE"
            vertex_num = graph.number_of_nodes()+1
            current_bag = [item for item in current_bag if item != vertex]
            graph.add_node(vertex_num, label=" ".join(map(str,current_bag)), kind="")
            #print "Node", cursor, "is introduce; with child bag", current_bag, "and child",vertex_num
            graph.add_edge(cursor, vertex_num)
            cursor = vertex_num
        for vertex in forgotten:
            graph.node[cursor]["kind"] = "FORGET"
            vertex_num = graph.number_of_nodes()+1
            current_bag.append(vertex)
            graph.add_node(vertex_num, label=" ".join(map(str,current_bag)), kind="")
            #print "Node", cursor, "is forget; with child bag", current_bag, "and child",vertex_num
            graph.add_edge(cursor, vertex_num)
            cursor = vertex_num
        graph.add_edge(cursor, children[0])
        #print "final child is", children[0], "with bag", graph.node[children[0]]['label']
        make_it_nice(graph, children[0], get_all_children(graph, children[0], cursor))
    # Last possibility is that the node is actually a Leaf Node
    else:
        #print "vertex",node," is a LEAF because len(children) = ", len(children)
        graph.node[node]["kind"] = "LEAF"

# Finds all of the nodes that are connected to the given node by an edge
# Input - graph - the tree (or tree decompostion) to which the node belongs
#       - node - the given node
# Output - a list of all nodes adjacent to the given node
def get_all_neighbours(graph, node):
    neighbours = []
    for edge in graph.edges():
        for i in range(2):
            if edge[i] == node:
                neighbours.append(edge[1-i])
    return neighbours

# Finds all of the children of a given node (assuming only one parent)
# Input - graph - the tree (or tree decompostion) to which the node belongs
#       - node - the given node
#       - parent - the one adjacent node that is not a child
# Output - a list of all children of the given node
def get_all_children(graph, node, parent):
    neighbours = get_all_neighbours(graph, node)
    return [vertex for vertex in neighbours if vertex != parent]

'''
tree = nx.read_dot("test.txt")
root = tree.nodes()[0]
nice_tree = get_nice_tree_decomp(tree, root)
print "MADE NICE"
for node in nice_tree.nodes():
    kind = nice_tree.node[node]["kind"]
    print node, nice_tree.node[node]["label"], kind, get_all_neighbours(nice_tree, node)
    
graph = gf.read_edges_from_file("test2.txt", " ")
print "READ"
#'''
#print get_all_neighbours(nice_tree, nice_tree.node[7])
#delValues = apply_algorithm(graph, tree, root, 3,7)
#print "-------------------------=========="
#for guy in delValues:
#    if delValues[guy] != INFINITY:
#        print guy, " | ", delValues[guy]

