import graphFunctions
import searchTree
import searchTreeNode as nd
import time
# E-mail stuff
import smtplib

# Name of the file containing edges for the graph
FILENAME = "SampleGraph1"
msg = FILENAME + "\n"

graph = graphFunctions.read_edges_from_file(FILENAME)
tree = searchTree.SearchTree()
print "Working on a graph with", graph.number_of_nodes(), "vertices"
msg = msg + "Working on a graph with" + str(graph.number_of_nodes()) + "vertices\n"
tree.set_root(nd.Node(graph.edges(),0))

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
msg = msg + "\nIt took: " + str(elapsed_time) + "seconds\n"

mail = smtplib.SMTP("smtp.gmail.com", 587)
mail.ehlo()
mail.starttls()
mail.login("mai1", "password")
mail.sendmail("mai1", "mail2", msg)
mail.close()

