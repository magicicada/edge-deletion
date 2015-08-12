import graphFunctions
import searchTree
import searchTreeNode as nd
import time
# E-mail stuff
import smtplib

for i in range(6):
    # Name of the file containing edges for the graph
    FILENAME = "sampleGraphs/links2010.edges-" + str(i) + ".anonGraph"
    content = FILENAME + "\n"

    graph = graphFunctions.read_edges_from_file(FILENAME, " ")

    for j in range(graph.number_of_nodes()/8, graph.number_of_nodes()/2):
        for k in range(1, len(graph.edges())/12):
            tree = searchTree.SearchTree()
            print "Working on a graph with", graph.number_of_nodes(), "vertices"
            msg = "Working on a graph with " + str(graph.number_of_nodes()) + " vertices\n"
            tree.set_root(nd.Node(graph.edges(),0))

            print "Looking for at most", k, "edges to delete, so as to"
            print "separate the graph into components of size at most", j, "nodes"
            msg = msg + "Looking for at most " + k + " edges to delete, so as to\n"
            msg = msg + "separate the graph into components of size at most " + j + " nodes\n"
            # Code to track execution time
            print "Starting search..."
            start_time = time.time()

            # Change search method HERE --v
            minEdges = tree.breadth_first_search(15,3)

            elapsed_time = time.time()-start_time
            print "Miminum deletions necessary are: ", minEdges
            msg = msg + "Miminum deletions necessary are: " + str(minEdges)
            #print "That is ", len(minEdges), "edges"
            print "It took: ", elapsed_time, "seconds"
            msg = msg + "\nIt took: " + str(elapsed_time) + "seconds\n\n"
            content = content + msg

    content = content + "Algorithm ran on " + (len(graph.edges())/12)*(graph.number_of_nodes()/2 - graph.number_of_nodes()/8 +1) + " different possibilities."

    mail = smtplib.SMTP("smtp.gmail.com", 587)
    mail.ehlo()
    mail.starttls()
    mail.login("mai1", "password")
    mail.sendmail("mai1", "mail2", content)
    mail.close()

