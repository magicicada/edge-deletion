#!/usr/bin/env python

import sys
import copy
import networkx as nx
from collections import Counter
INFINITY = 999999999

def noBigSteps(candidate):
    sortV =sorted(candidate)
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
    last = True
    # print "considering current "
    # print current
    for i in range(0, len(current)-1):
        if current[i+1] != current[i]+1:
            # print "not found to be the last"
            last = False
    # print "the last check value is " + str(last)
    # print "the first val check value is " + str(current[0] == 1)
    if last and current[0] == 1:
        return "DONE"
    
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
        if not canDo:
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
    # print partitions
    goodPartitions = []
    for guy in partitions:
        guy = sorted(guy)
        if guy not in goodPartitions and max(Counter(guy).values())<= maxH:
            if noBigSteps(guy):
                goodPartitions.append(guy)
                # print guy
    return goodPartitions
        
# changes numerical partition encodings into actual bags
# I'm not checking to see if the partitions are valid, yet
# will return a list of lists of lists
def bagEm(partitionList, bag):
    partitioned = []
    for guy in partitionList:
        dictOfParts = {}
        for i in range(0, len(guy)):
            if guy[i] not in dictOfParts:
                dictOfParts[guy[i]] = []
            dictOfParts[guy[i]].append(bag[i])
        partitioned.append(dictOfParts.values())
    return partitioned

# print bagEm(getAllPartitions([1, 2, 3, 4], 3), [1, 2, 3, 4])

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
            # print "check validity of " + str(currentFunction) + " for " + str(guy)
            isValid = True
            for i in range(0, len(currentFunction)):
                # print "comparing " + str(currentFunction[i]) + " to " + str(len(guy[i]))
                if currentFunction[i] > len(partition[i]):
                    isValid = False
            if isValid:
                # print "ADDED!!"
                dictThis = {}
                for i in range(0, len(currentFunction)):
                    dictThis[tuple(partition[i])] = currentFunction[i]
                allFunctions.append(dictThis)
            currentFunction = nextFunction(currentFunction, maxH)    
    return allFunctions        
        # print " a possible function " + str(currentFunction)
    # print "done generating functions"
    


def generateAllStates(t, treeDecomp, bag, graph, h):
    states = []
    allPartitions  = bagEm(getAllPartitions(bag, h), bag)
    # print allPartitions
    # allPartitions = [[allPartitions[3]]]
    for p in allPartitions:
        allFunctions = getAllFunctions(p, h)
        # print "all functions is"
        # print allFunctions
        for c in allFunctions:
             states.append((p, c))
    return states

def inSamePart(partition, u, v):
    for guy in partition:
        if u in guy and v in guy:
            return True
    print "checking partition spans, found " + str(u) + str(v) + " are not in the same part of " + str(partition)
    return False

def countSpans(graph, bag, partition):
    subgraph = graph.subgraph(bag)
    count = 0
    for (u, v) in subgraph.edges():
        if not inSamePart(partition, u, v):
            count = count + 1
    return count
def countSpansSingle(graph, bag, partition, v):
    subgraph = graph.subgraph(bag)
    count = 0
    for u in subgraph.neighbors(v):
        if not inSamePart(partition, u, v):
            count = count + 1
    return count
    

def sigOfLeaf(t, treeDecomp, bag, graph, h, k):
    delValues = {}
    print "Generating states"
    allStates = generateAllStates(t, treeDecomp, bag, graph, h)
    print "considering each state"
    for (p, c) in allStates:
        subgraph = graph.subgraph(bag)
        print "counting spanning edges within " + str(bag)
        print " for parition " + str(p)
        countEdges = countSpans(graph, bag, p)
        print "count is " + str (countEdges)
        if countEdges <= k:
            delValues[(str(p), str(c))] = countEdges
        else:
            delValues[(str(p), str(c))] = INFINITY
    return delValues

def generateAllRefinements(part, v, h):
    print "in generateAllRef, we've received " + str(part)
    if part == [v]:
        return []
    toPartition = [x for x in part if x != v]
    print "in generateAllRef, we need to partition " + str(toPartition)
    return bagEm(getAllPartitions(toPartition, h), toPartition)

def sigOfIntroduce(t, treeDecomp, bag, graph, childT, childBag, delValuesChild, h, k):
    delValues  = {}
    print "doing the introduce node"
    print "calculating v"
    v = list(set(bag) - set(childBag))[0]
    print "calculating all states"
    allStates = generateAllStates(t, treeDecomp, bag, graph, h)
    print "for each guy in allStates"
    for (p, c) in allStates:
        # genearating the inherited states
        print "==========considering " + str((p, c)) + " from allStates========"
        inherited = []
        Xr = []
        print "looking for Xr"
        for dude in p:
            if v in dude:
                Xr  = dude
        print "Xr is " + str(Xr)
        if Xr == []:
            print "problem: cannot find a partition containing v in introduce proceedure"
        remainderP = copy.deepcopy(p)
        remainderP.remove(Xr)
        print "remainderP is " + str(remainderP)
        print "Generating refinements"
        refinements  =  generateAllRefinements(Xr, v, h)
        print "for each refinement of "
        print refinements
        for refinedPart in refinements:
            print "for refinedPart " + str(refinedPart)
            pPrime = remainderP + refinedPart
            allRefinedFunctions = getAllFunctions(pPrime, h)
            print "all refined functions is "+ str (allRefinedFunctions)
            for guy in allRefinedFunctions:
                print "now to check the sum condition in " + str(guy)
                # check sum condition: error in pseudocode here?TODO
                sumOf = 0
                for entry in refinedPart:
                    print "adding in the function for " + str(entry) + " which is " + str(guy[tuple(entry)])
                    sumOf = sumOf + guy[tuple(entry)]
                print "total sum is " + str(sumOf)
                print "which we will compare to " + str(c[tuple(Xr)]-1)
                if sumOf == c[tuple(Xr)]-1:
                    inherited.append((pPrime, guy))
        print "for state " + str((p, c)) + " the inherited list is "
        print str(inherited)
        minValue = INFINITY
        for (pPrime, cPrime) in inherited:
            print "looking at " + str((pPrime, cPrime)) + " in inherited"
            print "the del values are"
            print delValuesChild[(str(pPrime), str(cPrime))]
            value = delValuesChild[(str(pPrime), str(cPrime))] + countSpansSingle(graph, bag, pPrime, v)
            if value < minValue:
                minValue = value
        if minValue <= k:
            delValues[(str(p), str(c))] = minValue
        else:
            delValues[(str(p), str(c))] = INFINITY
        
    return delValues       
     

def sigOfForget(t, treeDecomp, bag, graph, childT, childBag, delValuesChild, h):
    delValues  = {}
    v = list(set(childBag) - set(bag))[0]
    allStates = generateAllStates(t, treeDecomp, bag, graph, h)
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
                inheritedPartitions.append(newPart)
        # add it in its own part
        inheritedPartitions.append(copy.deepcopy(p).append([v]))

        
        for pPrime in inheritedPartitions:
            allCPrime = []
            cPrime = {}
            vSingleton = False
            for part in pPrime:
                if pPrime != [v]:
                    partWithoutV = copy.deepcopy(part) - [v]
                    cPrime[part] = c[partWithoutV]
                else:
                    vSingleton = True
            if not vSingleton:
                allCPrime.append(cPrime)
            else:
                for i in range(h+1):
                    if i <= h and i >= 1:
                        newCPrime = copy.deepcopy(cPrime)
                        newCPrime[[v]] = i
                        allCPrime.append(newCPrime)
            
            for c in allCPrime:
                inheritedSets
            
#             NOT COMPLETED


def sigOfJoin(t, treeDecomp, bag, graph, childT, childBag, delValuesChild, h):
    delValues = {}
        
    return delValues




graph  = nx.path_graph(25)
# print(generateAllStates(1, 2, [1, 2, 3, 4], graph, 3))
h = 4
k = 6
NONSENSE = "nonsense"
delValuesLeaf = sigOfLeaf(NONSENSE, NONSENSE, [1,2,3,4], graph, h, k)
print "+++++++FOR LEAF++++++++"
for guy in delValuesLeaf:
    print str(guy) + " | " + str(delValuesLeaf[guy])
delValuesIntr = sigOfIntroduce(NONSENSE, NONSENSE, [1,2,3,4,5], graph, NONSENSE, [1,2,3,4], delValuesLeaf, h, k)
print "+++++++Introduce++++++++"
for guy in delValuesIntr:
    if delValuesIntr[guy] != INFINITY:
        print str(guy) + " | " + str(delValuesIntr[guy])