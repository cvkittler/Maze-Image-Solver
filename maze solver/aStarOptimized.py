from copy import deepcopy
import numpy as np
from heapq import heappop, heappush
import cv2
from time import sleep

def getAdj8(map,point):
    returnPoints = []
    size = np.shape(map)
    for x_shift, y_shift in [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]:
        if(point[0]+x_shift >= 0 and point[1]+y_shift >= 0):
            if(point[0]+x_shift < size[0] and point[1]+y_shift < size[1]):
                # white it 255
                # black is 0
                curPoint = map[point[0]+x_shift][point[1]+y_shift]
                if(curPoint == 255):
                    returnPoints.append((point[0]+x_shift,point[1]+y_shift))
    return returnPoints

def calcCost(end, dist, curr):
    g = dist
    h = ((curr[0] - end[0]) ** 2) + ((curr[1] - end[1]) ** 2)
    f = g + h
    return f

def aStar(image, start, end):
    return aStarOptimized(image, start, end)

def aStarOptimized(image, start, end):
    openNodes = [] # this is the fronteir or nodes that can be visited
    heappush(openNodes, (0,tuple(start),0))

    cameFrom = {}
    cameFrom[tuple(start)] = "START"

    costSoFar = {}
    costSoFar[tuple(start)] = 0

    while openNodes:
        currNode = heappop(openNodes)

        if currNode[1] == tuple(end):
            path = []
            currStep = tuple(currNode[1])
            while not currStep == tuple(start):
                path.append(currStep)
                currStep = cameFrom[currStep]
            return path, list(cameFrom.keys())

        for adjNode in getAdj8(image,currNode[1]):
            newCost = calcCost(end,currNode[2]+1,adjNode)
            if not adjNode in costSoFar or newCost < costSoFar[adjNode]:
                costSoFar[adjNode] = newCost
                heappush(openNodes,(newCost,adjNode,currNode[2]+1))
                cameFrom[adjNode] = currNode[1]

    return None

def aStarQueue(image, start, end):
    end = tuple(end)
    start = tuple(start)

    openNodes = []
    closedNodes = {} # Dictary where key -> value is the path 

    path = []
    # how the heap objects are orginzied
    # total cost - for sorting the heap into a priority queue
    # (cords,total_cost,to get here) - the object stored
    #       cords - cords of the node
    #       total_cost - same as before
    #       to_get_here - cost from start to this node
    #(total_cost (cords,total_cost,to get here))
    heappush(openNodes, (0,(start,0,0))) #put all nodes adjacent to start in queue
    curNode = (0,("START",0,0))

    while openNodes: #while there are still nodes to explore
        #get the lowest cost node
        newNode = heappop(openNodes)
        #get a new node till its not a closed node
        lookingForNode = True
        while lookingForNode:
            if newNode[1][0] in closedNodes: #if the node has already been visited
                if newNode[0] < closedNodes[newNode[1][0]]["cost"]:#check if the cost to get there is cheaper
                    print("poke")
                newNode = heappop(openNodes)
            else:
                lookingForNode = False
        #add that node to the closed nodes by setting the parent
        closedNodes[newNode[1][0]] = { "node": curNode[1][0], "cost": curNode[0]}
        curNode = newNode
        #check to see if the current Node is the end c
        if curNode[1][0] == end:
            #recreate the path taken to get to the end
            curStep = curNode[1][0]
            while not curStep == "START":
                path.append(curStep)
                curStep = closedNodes[curStep]["node"]
            return path, list(closedNodes.keys()) #<---------- EXIT
        #get nodes that can move to next
        for adjNode in getAdj8(image,curNode[1][0]):
            #if the node has not been closed
            if not adjNode in closedNodes:
                pass
                #add this node to the openNodes
            g = curNode[1][2] + 1
            h = ((adjNode[0] - end[0]) ** 2) + ((adjNode[1] - end[1]) ** 2)
            f = g + h
            heappush(openNodes,(f, (adjNode,f,g)))

    return "No Path", None
    
def aStarWithImage(image, start, end):
    end = tuple(end)
    start = tuple(start)

    openNodes = []
    closedNodes = {}

    path = []

    displayImage = deepcopy(image)

    #(total_cost (cords,total_cost,to get here))
    heappush(openNodes, (0,(start,0,0)))
    curNode = (None,("START",None))

    while openNodes: #while there are still nodes to explore
        cv2.imshow("Image", np.uint8(displayImage))
        cv2.waitKey(1)
        #get the lowest cost node
        newNode = heappop(openNodes)
        #get a new node till its not a closed node
        while newNode[1][0] in closedNodes:
            newNode = heappop(openNodes)
        #add that node to the closed nodes by setting the parent
        closedNodes[newNode[1][0]] = curNode[1][0]
        curNode = newNode
        displayImage[newNode[1][0][0]][newNode[1][0][1]] = 100
        #check to see if the current Node is the end
        if curNode[1][0] == end:
            #recreate the path taken to get to the end
            curStep = curNode[1][0]
            while not curStep == "START":
                path.append(curStep)
                curStep = closedNodes[curStep]
            return path
        #get nodes that can move to next
        for adjNode in getAdj8(image,curNode[1][0]):
            #if the node has not been closed
            if not adjNode in closedNodes:
                #add this node to the openNodes
                g = curNode[1][2] + 1
                h = ((adjNode[0] - end[0]) ** 2) + ((adjNode[1] - end[1]) ** 2)
                f = g + h
                heappush(openNodes,(f, (adjNode,f,g)))