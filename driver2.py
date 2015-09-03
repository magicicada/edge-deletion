import graphFunctions as gf
import networkx as nx
import treeDecomposition as td
import time
# E-mail stuff
import smtplib
INFINITY = 999999999

for i in range(6):
    # Name of the file containing edges for the graph
    GRAPHNAME = "sampleGraphs/links2012.edges-"+ str(i) +".anonGraph"
    TREENAME = "TreeDecomplinks2012.edges-" + str(i) + ".anonGraph.dgf.txt"
    #content = GRAPHNAME + "\n" + TREENAME + "\n\n"
    print "GraphName =", GRAPHNAME
    print "DecompName =", TREENAME

    treeDecomp = nx.read_dot(TREENAME)
    graph = gf.read_edges_from_file(GRAPHNAME, " ")
    root = treeDecomp.nodes()[0]
    niceTreeDecomp = td.get_nice_tree_decomp(treeDecomp, root)
    
    for j in range(graph.number_of_nodes()/8, graph.number_of_nodes()/2):
        for k in range(1, len(graph.edges())):
            print "Working on a graph with", graph.number_of_nodes(), "vertices"
            #msg = "Working on a graph with " + str(graph.number_of_nodes()) + " vertices\n"

            print "Looking for at most", k, "edges to delete, so as to"
            print "separate the graph into components of size at most", j, "nodes"
            #msg = msg + "Looking for at most " + str(k) + " edges to delete, so as to\n"
            #msg = msg + "separate the graph into components of size at most " + str(j) + " nodes\n"
            # Code to track execution time
            print "Starting search..."
            print "Calling td.apply_algorithm(graph, treeDecomp, ",j,",",k,")"
            start_time = time.time()

            # Change search method HERE --v
            delValues = td.apply_algorithm(graph, niceTreeDecomp, root, j,k)

            elapsed_time = time.time()-start_time
            solved = False
            for guy in delValues:
                if delValues[guy] != INFINITY:
                    print guy, " | ", delValues[guy]
                    solved = True
                    break
            print "It took:", elapsed_time, "seconds\n"
            #msg = msg + "\nIt took: " + str(elapsed_time) + " seconds\n\n"
            if solved == True:
                print "It's possible!\n---------------------------------------------------------"
                #msg = msg + "It's possible!\n---------------------------------------------------------\n"
                #content = content + msg
                break
            else:
                print "It's NOT possible."
                #msg = msg + "It's NOT possible."
                #content = content + msg

    #content = content + "Algorithm ran on graphs from 2010"

    #mail = smtplib.SMTP("smtp.gmail.com", 587)
    #mail.ehlo()
    #mail.starttls()
    #mail.login("mai1", "password")
    #mail.sendmail("mai1", "mail2", content)
    #mail.close()
