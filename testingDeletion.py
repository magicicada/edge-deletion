#!/usr/bin/env python

import EdgeDeletion as ed
import networkx as nx

# created October 5, 2015 by JEnright
# This will be a workspace for debugging and understanding the edge deletion code
# The plan: start with a simple nice tree decomposition, test some of the methods 


treeBags = {}
treeBags['a'] = [2, 3]
treeBags['b'] = [1, 2, 3]
treeBags['c'] = [1, 2]
treeBags['d'] = [1]
treeBags['e'] = [2,22]
decompEdges = [('a', 'b'), ('b', 'c'), ('c', 'd'), ('c', 'e')]
decomp = nx.Graph()
decomp.add_edges_from(decompEdges)

edges = [(1, 2), (2, 3), (2,22)]
graph = nx.Graph()
graph.add_edges_from(edges)
print graph.nodes()

h=2
k=1

sigs = ed.sigOfLeaf(graph, decomp, treeBags['e'], graph, h, k)
print "leaf signature"
for guy in sigs:
    print ed.printSignatureNicely(guy) + " Value " + str(sigs[guy])


#graph  = nx.path_graph(25)
# print(generateAllStates(1, 2, [1, 2, 3, 4], graph, 3))
#h = 4
#k = 6
#NONSENSE = "nonsense"
#delValuesLeaf = sigOfLeaf(NONSENSE, NONSENSE, [1,2,3,4], graph, h, k)
#delValuesLeaf2 = sigOfLeaf(NONSENSE, NONSENSE, [1,2,3,4], graph, h, k)
#print "+++++++FOR LEAF++++++++"
#for guy in delValuesLeaf:
#    print str(guy) + " | " + str(delValuesLeaf[guy])
#delValuesIntr = sigOfIntroduce(NONSENSE, NONSENSE, [1,2,3,4], graph, NONSENSE, [1,2,3], delValuesLeaf, h, k)
#print "+++++++Introduce++++++++"
#for guy in delValuesIntr:
#    if delValuesIntr[guy] != INFINITY:
#        print str(guy) + " | " + str(delValuesIntr[guy])
#delValuesForget = sigOfForget(NONSENSE, NONSENSE, [1,3,4], graph, NONSENSE, [1,2,3,4], delValuesLeaf, h, k)
#print "+++++++Forget++++++++"
#for guy in delValuesForget:
#    if delValuesForget[guy] != INFINITY:
#        print str(guy) + " | " + str(delValuesForget[guy])
#delValuesJoin = sigOfJoin(NONSENSE, NONSENSE, [1,2,3,4], graph, NONSENSE, NONSENSE, NONSENSE, NONSENSE, delValuesIntr, delValuesLeaf2, h, k)
#print "+++++++Join++++++++"
#for guy in delValuesJoin:
#    if delValuesJoin[guy] != INFINITY:
#        print str(guy) + " | " + str(delValuesJoin[guy])
