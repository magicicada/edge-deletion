#!/usr/bin/env python

import sys
import copy
import networkx as nx
from collections import Counter
INFINITY = 999999999

def noBigSteps(candidate):
    sortV =sorted(candidate)
    # A check to make sure no duplicates are allowed
    if 1 not in candidate:
        return False
    for i in range(0, len(sortV) - 1):
        if sortV[i+1] - sortV[i] > 1:
            # print "" 
            # print "=========================="
            # print "candidate failing!"
            # print candidate
            # print "=========================="
            # print "" 
            return False
    return True

def nextPartition(current, maxH, size):
    # first do sanity check for done
    #last = True
    # print "considering current "
    # print current
    #for i in range(0, len(current)-1):
    #    if current[i+1] != current[i]+1:
            # print "not found to be the last"
    #        last = False
    # print "the last check value is " + str(last)
    # print "the first val check value is " + str(current[0] == 1)
    #if last and current[0] == 1:
    #    return "DONE"
    
    newPartition = []
    canDo = False
    for guy in current:
        newPartition.append(guy)
    if current[len(current)-1] < size:
       newPartition[len(newPartition)-1] = newPartition[len(newPartition)-1] + 1
    else:
#         the below should maybe be: (len(newPartition)-2, -1, -1): 
        for i in range(len(newPartition)-2, -1, -1):
            if newPartition[i] < size:
                canDo = True
                newPartition[i] = newPartition[i] + 1
                for j in range(i+1, len(newPartition)):
                    newPartition[j] = 1
                break
        if not canDo: ##
            newPartition = "DONE"
    # print newPartition
    return newPartition

# generate all partitions of guys in bag such that
# no partition is larger than maxH
# currently returns integer list encoding.  Is that adequate?
def getAllPartitions(bag, maxH):
    size = len(bag)
    partitions = []
    # now we want all numbers up to 1,2,3,4,... using only the digits 1 to size
    #  and really, we don't want more than maxH of any single digit
    # never use a digit that?s more than 1 larger than any other digit in the encoding
    firstPartition = [1] * size
    currentPartition = firstPartition
    while currentPartition != "DONE":
        partitions.append(currentPartition)
        currentPartition = nextPartition(currentPartition, maxH, size)
    # print "partitions= ",partitions
    goodPartitions = []
    for guy in partitions:
        # print ">", guy
        #guy = sorted(guy)
        if guy not in goodPartitions and max(Counter(guy).values())<= maxH:
            # print "=>", guy
            if noBigSteps(guy):
                goodPartitions.append(guy)
                # print guy
    return goodPartitions

# print getAllPartitions([1,2,3,4],3)

# changes numerical partition encodings into actual bags
# I'm not checking to see if the partitions are valid, yet
# will return a list of lists of lists    #added a weak validity check
def bagEm(partitionList, bag):
    partitioned = []
    for guy in partitionList:
        dictOfParts = {}
        for i in range(0, len(guy)):
            if guy[i] not in dictOfParts:
                dictOfParts[guy[i]] = []
            dictOfParts[guy[i]].append(bag[i])
        if sorted(dictOfParts.values()) not in partitioned:
            partitioned.append(sorted(map(sorted,dictOfParts.values())))
    return partitioned

# print bagEm(getAllPartitions([1, 2, 3, 4], 4), [1, 2, 3, 4])

# A weak validity check for unbagged partition lists
# Should prevent double counting.
def partition_not_repeating(partitionList):
    pass

def nextFunction(current, maxVal):
    newPartition = []
    canDo = False
    for guy in current:
        newPartition.append(guy)
    if current[len(current)-1] < maxVal:
       newPartition[len(newPartition)-1] = newPartition[len(newPartition)-1] + 1
    else:
#         the below should maybe be: (len(newPartition)-2, -1, -1): 
        for i in range(len(newPartition)-2, -1, -1):
            if newPartition[i] < maxVal:
                canDo = True
                newPartition[i] = newPartition[i] + 1
                for j in range(i+1, len(newPartition)):
                    newPartition[j] = 1
                break
        if not canDo:
            newPartition = "DONE"
    # print newPartition
    return newPartition


# will give functions as dictionaries, in a list
def getAllFunctions(partition, maxH):
    # print "generating functions for: "
    allFunctions = []
    guy = partition
    # for guy in partitions:
    # print "Now working on partition "
    # print guy
    # print "who has length " + str(len(guy))
    firstFunction = [1] * len(guy)

    # print "first function is " + str(firstFunction)
    currentFunction = firstFunction
    while currentFunction != "DONE":
        
        if currentFunction != "DONE":
            #print "check validity of " + str(currentFunction) + " for " + str(guy)
            isValid = True
            for i in range(0, len(currentFunction)):
                # print "comparing " + str(currentFunction[i]) + " to " + str(len(guy[i]))
                if currentFunction[i] < len(partition[i]):
                    isValid = False
            if isValid:
                #print "ADDED!!"
                dictThis = {}
                for i in range(0, len(currentFunction)):
                    dictThis[tuple(partition[i])] = currentFunction[i]
                allFunctions.append(dictThis)
            currentFunction = nextFunction(currentFunction, maxH)    
           
        #print " a possible function " + str(currentFunction)
    #print "done generating functions"
    return allFunctions 

# print getAllFunctions([[1,2],[3,4]], 3)

def generateAllStates(t, treeDecomp, bag, graph, h):
    states = []
    allPartitions  = bagEm(getAllPartitions(bag, h), bag)
    # print allPartitions
    # allPartitions = [[allPartitions[3]]]
    for p in allPartitions:
        # print "p=", p, "h=", h
        allFunctions = getAllFunctions(p, h)
        # print "all functions is"
        # print allFunctions
        for c in allFunctions:
             states.append((p, c))
    return states

# print generateAllStates(None, None, [1,2,3,4], None, 3)

def inSamePart(partition, u, v):
    for guy in partition:
        if u in guy and v in guy:
            return True
    #print "checking partition spans, found " + str(u)+ "-" + str(v) + " are not in the same part of " + str(partition)
    return False

# Number of things not contained in any one given partition
def countSpans(graph, bag, partition):
    subgraph = graph.subgraph(bag)
    count = 0
    for (u, v) in subgraph.edges():
        if not inSamePart(partition, u, v):
            count = count + 1
    return count

# The number of edges adjacent to v that do not connect v to nodes in the same partition
def countSpansSingle(graph, bag, partition, v):
    subgraph = graph.subgraph(bag)
    count = 0
    for u in subgraph.neighbors(v):
        if not inSamePart(partition, u, v):
            count = count + 1
    return count

def sorted_dictionary_to_string(dictionary):
    keys = sorted(dictionary.keys())
    string = ""
    for key in keys:
        string = string + str(sorted(key)) + ": " + str(dictionary[key]) + ", "
    return "{" + string[:-2] + "}"
    
def sigOfLeaf(t, treeDecomp, bag, graph, h, k):
    delValues = {}
    #print "Generating states"
    allStates = generateAllStates(t, treeDecomp, bag, graph, h)
    #print "considering each state" # Here
    for (p, c) in allStates:
        subgraph = graph.subgraph(bag) # Move this
        #print "-counting spanning edges within " + str(bag)
        #print " for parition " + str(p)
        #print " and for func " + str(c)
        countEdges = countSpans(graph, bag, p) # Pass only subgraph
        #print " count is " + str (countEdges)
        if countEdges <= k:
            delValues[(str(p), sorted_dictionary_to_string(c))] = countEdges
        else:
            delValues[(str(p), sorted_dictionary_to_string(c))] = INFINITY
    return delValues
# G = nx.Graph()
# G.add_edge(1,2)
# G.add_edge(3,2)
# G.add_edge(3,4)
# print sigOfLeaf(None, None, [1,2,3,4], G, 3, 2)

def generateAllRefinements(part, v, h):
    #print "in generateAllRef, we've received " + str(part)
    if part == [v]:
        return [[]]
    toPartition = [x for x in part if x != v]
    #print "in generateAllRef, we need to partition " + str(toPartition)
    return bagEm(getAllPartitions(toPartition, h), toPartition)

#print generateAllRefinements([1,2,3,4],3,3)

def sigOfIntroduce(t, treeDecomp, bag, graph, childT, childBag, delValuesChild, h, k):
    # Safety check:
    if len(bag) - len(childBag) != 1:
        print "ERROR, this is not an Introduce node"
        exit
    
    delValues  = {}
    #print "doing the introduce node"
    #print "calculating v"
    v = list(set(bag) - set(childBag))[0]
    #print "calculating all states"
    allStates = generateAllStates(t, treeDecomp, bag, graph, h)
    #print "for each guy in allStates"
    for (p, c) in allStates:
        # generating the inherited states
        #print "==========considering " + str((p, c)) + " from allStates========"
        inherited = []
        Xr = []
        #print "looking for Xr"
        for dude in p:
            if v in dude:
                Xr  = dude
        #print "Xr is " + str(Xr)
        if Xr == []:
            print "problem: cannot find a partition containing v in introduce procedure"
        # Generate refinements
        remainderP = copy.deepcopy(p)
        remainderP.remove(Xr)
        #print "remainderP is " + str(remainderP)
        #print "Generating refinements"
        refinements  =  generateAllRefinements(Xr, v, h)
        #print "for each refinement of " + str(refinements)
        for refinedPart in refinements: # for refinement in refinements?
            #print "for refinedPart " + str(refinedPart)
            pPrime = remainderP + refinedPart # P'
            allRefinedFunctions = getAllFunctions(sorted(pPrime), h)
            #print "all refined functions is "+ str (allRefinedFunctions)
            for guy in allRefinedFunctions: # This is no longer in pseudocode, on purpose?
                #print "now to check the sum condition in " + str(guy)
                # check sum condition: error in pseudocode here?TODO
                sumOf = 0
                okay = False
                for entry in refinedPart:
                    #print "adding in the function for " + str(entry) + " which is " + str(guy[tuple(entry)])
                    sumOf = sumOf + guy[tuple(entry)]
                #print "total sum is " + str(sumOf)
                #print "which we will compare to " + str(c[tuple(Xr)]-1)
                if sumOf == c[tuple(Xr)]-1:
                    okay = True
                for entry in remainderP:
                    if c[tuple(entry)] != guy[tuple(entry)]:
                        okay = False
                if okay:                    
                    inherited.append((sorted(pPrime), guy))
        #print "for state " + str((p, c)) + " the inherited list is "
        #print str(inherited)
        minValue = INFINITY
        for (pPrime, cPrime) in inherited: # t' no longer used?
            #print "looking at " + str((pPrime, cPrime)) + " in inherited"
            #print "the del values are"
            #print delValuesChild[(str(pPrime), str(cPrime))]           #################################
            value = delValuesChild[(str(sorted(map(sorted,pPrime))), sorted_dictionary_to_string(cPrime))] + countSpansSingle(graph, bag, p, v)
            if value < minValue:
                minValue = value

        if minValue <= k:
            delValues[(str(sorted(map(sorted,p))), sorted_dictionary_to_string(c))] = minValue
        else:
            delValues[(str(sorted(map(sorted,p))), sorted_dictionary_to_string(c))] = INFINITY
        
    return delValues

def is_function_valid(c):
    valid = True
    for Xr in c:
        if c[Xr] < len(Xr):
            valid = False
    return valid

def sigOfForget(t, treeDecomp, bag, graph, childT, childBag, delValuesChild, h, k):
    # Safety check:
    if len(bag) - len(childBag) != -1:
        print "ERROR, this is not a Forget node"
        exit

    delValues  = {}
    v = list(set(childBag) - set(bag))[0]
    allStates = generateAllStates(t, treeDecomp, bag, graph, h)
    #print "Allstates = ", allStates
    inheritedSets = []
    for (p, c) in allStates:
#     generating the inherited sigma set
        inheritedPartitions = []
        # make a bunch of copies, one for v being added to each part
        for part in p:
            if len(part) < h:
                newPart = []
                for secondPart in p:
                    if secondPart != part:
                        newPart.append(copy.deepcopy(secondPart))
                    else:
                        newPart.append(copy.deepcopy(secondPart) + [v])
                inheritedPartitions.append(map(sorted,newPart))
        # add it in its own part
        temp = copy.deepcopy(p)
        temp.append([v])
        inheritedPartitions.append(map(sorted,temp))

        #print "inherited = ", inheritedPartitions        
        for pPrime in inheritedPartitions:
            #print "pprime=", pPrime
            allCPrime = []
            cPrime = {}
            vSingleton = False
            for part in pPrime:
                if part != [v]:
                    #print "part= ", copy.deepcopy(part)
                    #print "v= ", v
                    partWithoutV = copy.deepcopy(part)
                    if v in partWithoutV:
                        #print "v in partwithoutV"
                        partWithoutV.remove(v)
                    #print "partwithoutV= ",partWithoutV
                    #print "cc=", c
                    #print "c=",c[tuple(partWithoutV)]
                    cPrime[tuple(part)] = c[tuple(partWithoutV)] #it is possible to get incorrect fnc here?
                    #print "cp=", cPrime
                else:
                    vSingleton = True
            if not vSingleton:
                allCPrime.append(cPrime)
            else:
                for i in range(h+1):
                    if i <= h and i >= 1:
                        newCPrime = copy.deepcopy(cPrime)
                        newCPrime[tuple([v])] = i
                        allCPrime.append(newCPrime)
            
            for cPrime in allCPrime:
                #print "cprime", cPrime
                if is_function_valid(cPrime):
                    inheritedSets.append((pPrime,cPrime))
                #else:
                    #print "State not valid: ", pPrime, cPrime

        minValue = INFINITY
        setOfInterest = {}
        for (pPrime, cPrime) in inheritedSets:
            #print "pPrime", pPrime, "cPrime", cPrime
            value = delValuesChild[(str(sorted(map(sorted,pPrime))),sorted_dictionary_to_string(cPrime))]
            if value < minValue:
                minValue = value
                setOfInterest = (pPrime, cPrime)

        #print "setOfInterest ", setOfInterest, "for state: ", (p, c)

        if minValue <= k:
            delValues[str(sorted(map(sorted,p))),sorted_dictionary_to_string(c)] = minValue
        else:
            delValues[str(sorted(map(sorted,p))),sorted_dictionary_to_string(c)] = INFINITY

    return delValues
            
#             MAYBE COMPLETED


def sigOfJoin(t, treeDecomp, bag, graph, childT1, childT2, childBag1, childBag2, delValuesChild1, delValuesChild2, h, k):

    delValues = {} # None, None, bag, graph, None, None, childBag1, childBag2, delValuesChild1, delValuesChild2, h
    allStates = generateAllStates(t, treeDecomp, bag, graph, h)

    for (p,c) in allStates:
        # generating the inherited join states
        inheritedStates = []
        p1 = copy.deepcopy(p)
        p2 = copy.deepcopy(p)
        # generate all function pairs
        allFunctionPairs = []
        allRefinedFunctions = getAllFunctions(p1, h)
        for c1 in allRefinedFunctions:
            for c2 in allRefinedFunctions:
                for blockX in p:
                    if c[tuple(blockX)] == c1[tuple(blockX)] + c2[tuple(blockX)] - len(blockX):
                        allFunctionPairs.append((c1,c2))
        
        # add state to inherited states
        for (c1, c2) in allFunctionPairs:
            inheritedStates.append(((p1,c1),(p2,c2)))

        minValue = INFINITY
        for ((p1,c1),(p2,c2)) in inheritedStates:
            #print "1 del1=", delValuesChild1[str(p1), sorted_dictionary_to_string(c1)]
            #print "2 del2=", delValuesChild2[str(p2),sorted_dictionary_to_string(c2)]
            value = delValuesChild1[str(sorted(map(sorted,p1))), sorted_dictionary_to_string(c1)] + delValuesChild2[str(sorted(map(sorted,p2))),sorted_dictionary_to_string(c2)] - countSpans(graph, bag, p)
            if value < minValue:
                minValue = value

        if minValue <= k:
            delValues[(str(sorted(map(sorted,p))),sorted_dictionary_to_string(c))] = minValue
        else:
            delValues[(str(sorted(map(sorted,p))),sorted_dictionary_to_string(c))] = INFINITY
            
    return delValues




#graph  = nx.path_graph(25)
# print(generateAllStates(1, 2, [1, 2, 3, 4], graph, 3))
#h = 4
#k = 6
#NONSENSE = "nonsense"
#delValuesLeaf = sigOfLeaf(NONSENSE, NONSENSE, [1,2,3], graph, h, k)
#delValuesLeaf2 = sigOfLeaf(NONSENSE, NONSENSE, [1,2,3], graph, h, k)
#print "+++++++FOR LEAF++++++++"
#for guy in delValuesLeaf:
#    print str(guy) + " | " + str(delValuesLeaf[guy])
#delValuesIntr = sigOfIntroduce(NONSENSE, NONSENSE, [1,2,3,4], graph, NONSENSE, [1,2,3], delValuesLeaf, h, k)
#print "+++++++Introduce++++++++"
#for guy in delValuesIntr:
#    if delValuesIntr[guy] != INFINITY:
#        print str(guy) + " | " + str(delValuesIntr[guy])
#delValuesForget = sigOfForget(NONSENSE, NONSENSE, [1,3], graph, NONSENSE, [1,2,3], delValuesLeaf, h, k)
#print "+++++++Forget++++++++"
#for guy in delValuesForget:
#    if delValuesForget[guy] != INFINITY:
#        print str(guy) + " | " + str(delValuesForget[guy])
#delValuesJoin = sigOfJoin(NONSENSE, NONSENSE, [1,2,3,4], graph, NONSENSE, NONSENSE, NONSENSE, NONSENSE, delValuesIntr, delValuesLeaf2, h, k)
#print "+++++++Join++++++++"
#for guy in delValuesJoin:
#    if delValuesJoin[guy] != INFINITY:
#        print str(guy) + " | " + str(delValuesJoin[guy])

