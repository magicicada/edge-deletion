import networkx as nx
import pydot
import EdgeDeletion as ed
import graphFunctions as gf
INFINITY = 999999999

def apply_algorithm(graph, nice_decomposition, root, h, k):    
    # Get root's children
    children = get_all_neighbours(nice_decomposition, root)

    # We now have a nice tree decomposition.
    # Figure out delValues for the root:
    delValues = get_del_values(graph, nice_decomposition, root, children, h, k)

    return delValues

def get_nice_tree_decomp(decomp, root):
    children = get_all_neighbours(decomp, root)
    make_it_nice(decomp, root, children)
    return decomp

def get_del_values(graph, decomp, node, children, h, k):
    kind = ""
    try:
        kind = decomp.node[node]["kind"]
    except:
        pass
    bag = decomp.node[node]["label"].replace('"', '').strip().split(" ")
    delValues = []
    if kind == "JOIN":
        delValuesChild1 = get_del_values(graph, decomp, children[0], get_all_children(decomp, children[0], node),h,k)
        delValuesChild2 = get_del_values(graph, decomp, children[1], get_all_children(decomp, children[1], node),h,k)
        #print "Getting delValues for", kind, "node", node, "with bag", bag, "and children", children
        delValues = ed.sigOfJoin(None, None, bag, graph, None, None, None, None, delValuesChild1, delValuesChild2, h, k)

    elif kind == "INTRODUCE":
        child_bag = decomp.node[children[0]]["label"].replace('"', '').strip().split(" ")
        delValuesChild = get_del_values(graph, decomp, children[0], get_all_children(decomp, children[0], node),h,k)
        #print "Getting delValues for", kind, "node", node, "with bag", bag, "and children", children
        delValues = ed.sigOfIntroduce(None, None, bag, graph, None, child_bag, delValuesChild, h, k)

    elif kind == "FORGET":
        child_bag = decomp.node[children[0]]["label"].replace('"', '').strip().split(" ")
        delValuesChild = get_del_values(graph, decomp, children[0], get_all_children(decomp, children[0], node),h,k)
        #print "Getting delValues for", kind, "node", node, "with bag", bag, "and children", children
        delValues = ed.sigOfForget(None, None, bag, graph, None, child_bag, delValuesChild, h, k)

    elif kind == "LEAF":
        #print "Getting delValues for", kind, "node", node, "with bag", bag, "and children", children
        delValues = ed.sigOfLeaf(None, None, bag, graph, h, k)
        #for guy in delValues:
            #if delValues[guy] != INFINITY:
                #print str(guy) + " | " + str(delValues[guy])

    else:
        delValues = get_del_values(graph, decomp, children[0], get_all_children(decomp, children[0], node),h,k)
        #print "This one is a duplicate"

    return delValues
                                      

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
                graph.add_node(vertex_num, label=bag)
                #print "adding holder node ", vertex_num, "with bag", bag, "node=", node
                graph.add_edge(cursor, vertex_num)
                graph.add_edge(vertex_num, children[i])
                graph.add_node(vertex_num+1, label=bag)
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
        child_bag = child_bag.replace('"', '').strip().split(" ")
        bag = bag.replace('"', '').strip().split(" ")
        #print "b=",bag
        #print "c=",child_bag
        introduced = []
        forgotten = []
        for vertex in bag:
            if vertex not in child_bag:
                introduced.append(vertex)
        for vertex in child_bag:
            if vertex not in bag:
                forgotten.append(vertex)
        # Add Introduce and Forget nodes as necessary
        graph.remove_edge(node,children[0])
        cursor = node
        current_bag = bag
        for vertex in introduced:
            graph.node[cursor]["kind"] = "INTRODUCE"
            vertex_num = graph.number_of_nodes()+1
            current_bag = [item for item in current_bag if item != vertex]
            graph.add_node(vertex_num, label=" ".join(map(str,current_bag)))
            #print "Node", cursor, "is introduce; with child bag", current_bag, "and child",vertex_num
            graph.add_edge(cursor, vertex_num)
            cursor = vertex_num
        for vertex in forgotten:
            graph.node[cursor]["kind"] = "FORGET"
            vertex_num = graph.number_of_nodes()+1
            current_bag.append(vertex)
            graph.add_node(vertex_num, label=" ".join(map(str,current_bag)))
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

def get_all_neighbours(graph, node):
    neighbours = []
    for edge in graph.edges():
        for i in range(2):
            if edge[i] == node:
                neighbours.append(edge[1-i])
    return neighbours

def get_all_children(graph, node, parent):
    neighbours = get_all_neighbours(graph, node)
    return [vertex for vertex in neighbours if vertex != parent]
'''
tree = nx.read_dot("TreeDecomplinks2010.edges-5.anonGraph.dgf.txt")
graph = gf.read_edges_from_file("sampleGraphs/links2010.edges-5.anonGraph", " ")
delValues = apply_algorithm(graph, tree, 4,2)
for guy in delValues:
    print guy, " | ", delValues[guy]'''

