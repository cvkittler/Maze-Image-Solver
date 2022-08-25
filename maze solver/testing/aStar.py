from copy import deepcopy
import numpy as np
import cv2
from time import sleep
from math import sqrt


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0 #cost to get here
        self.h = 0 #heuristic
        self.f = 0 #total cost estemat 

    def __eq__(self, other):
        
        return self.position[0] == other.position[0] and self.position[1] == other.position[1]

    def calcCosts(self, goal):
        self.g = self.parent.g + 1
        self.h = ((self.position[0] - goal.position[0]) ** 2)+ ((self.position[1] - goal.position[1]) ** 2)
        self.f = self.g + self.h

# DEPRICATED
def getAdj4(map,point):
    returnPoints = []
    size = np.shape(map)
    for x_shift, y_shift in [(0,1),(0,-1),(1,0),(-1,0)]:
        if(point[0]+x_shift >= 0 and point[1]+y_shift >= 0):
            if(point[0]+x_shift < size[0] and point[1]+y_shift < size[1]):
                # white it 255
                # black is 0
                curPoint = map[point[0]+x_shift][point[1]+y_shift]
                if(curPoint == 0):
                    returnPoints.append((point[0]+x_shift,point[1]+y_shift))
    return returnPoints

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

def aStar(image,start,end):
    avalableNodes = []
    seenNodes = []
    path = []

    startNode = Node(None,start)
    avalableNodes.append(startNode)
    endNode = Node(None,end)
        
        
    blankMap = [[[255 for k in range(3)] for i in range(len(image[0]))] for j in range(len(image))]
    for i in range(len(image)):
        for j in range(len(image[0])):
            if image[i][j] == 0:
                blankMap[i][j][0]= 0
                blankMap[i][j][1]= 0
                blankMap[i][j][2]= 0
    cv2.imshow("Map", np.uint8(blankMap))
    curNode = startNode
    done = False
    counter = 0
    while len(avalableNodes) > 0 and not done:
        curNode = avalableNodes[0]
        currentIndex = 0
        for index, node in enumerate(avalableNodes):
            if node.f < curNode.f:
                curNode = node
                currentIndex = index

        # if counter == 10:
        #     debugMap = deepcopy(blankMap)
        #     for a in avalableNodes:
        #         debugMap[a.position[0]][a.position[1]][1] = 0

        #     for a in seenNodes:
        #         debugMap[a.position[0]][a.position[1]][0] = 0
        #     debugMap[curNode.position[0]][curNode.position[1]][2] = 0

        #     scale = 3
        #     cv2.imshow("Image", cv2.resize(np.uint8(debugMap), (len(image[0])*scale,len(image)*scale)))
        #     cv2.waitKey(1)
        #     counter = 0
        # else:
        #     counter += 1
            
        avalableNodes.pop(currentIndex)
        seenNodes.append(curNode)
        # print(f"\tCurrent Node: {curNode.position} Target {endNode.position}")
        if curNode == endNode:
            print("yay path found")
            pathNode = curNode
            while not pathNode == startNode:
                path.append(pathNode.position)
                pathNode = pathNode.parent
                done = True

        for nodePose in getAdj8(image,curNode.position):
            append = True
            newNode = Node(curNode,nodePose)
            for seenNode in seenNodes:
                if newNode == seenNode:
                    append = False
            newNode.calcCosts(endNode)
            for index,avalableNode in enumerate(avalableNodes):
                if newNode == avalableNode and newNode.g > avalableNode.g:
                    append = False
            if append:
                avalableNodes.append(newNode)
    if len(path) == 0:
        for node in seenNodes:
            path.append(node.position)
    return path
        


if __name__ == "__main__":
    map =  np.array([[255,0,255,255,255],
                     [255,0,255,0,255],
                     [255,255,255,0,255],
                     [0,0,0,0,255],
                     [255,255,255,255,255]])

    print(aStar(map,(0,0),(4,4)))