from math import *
# adjMatrix structure:
#i,j -> cost = cost from i to j.

def distanceKM(arrOfCoords, i,j):
    R = 6371 #Earth's radius in km
    lat1 = arrOfCoords[i][0]
    long1 = arrOfCoords[i][1]
    lat2 = arrOfCoords[j][0]
    long2 = arrOfCoords[j][1]
    deltaLat = radians(lat2-lat1)
    deltaLong = radians(long2-long1)
    #Haversine Formula
    dist = sin(deltaLat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(deltaLong/2)**2
    dist = 2* atan2 (sqrt(dist), sqrt(1-dist))
    dist = R * dist
    return dist

def graphGeneration(arrOfCoords, arrOfEdges):
    #returns an adjacency matrix that represents the cost from i to j.
    adjMatrix =[]
    for i in range(len(arrOfCoords)):
        tempMat = []
        for j in range(len(arrOfCoords)):
            tempMat.append(100000)
        adjMatrix.append(tempMat) 

    for edge in arrOfEdges:
        adjMatrix[edge[0]][edge[1]] = distanceKM(arrOfCoords,edge[0],edge[1])
        adjMatrix[edge[1]][edge[0]] = distanceKM(arrOfCoords,edge[1],edge[0])

    return adjMatrix

def findMinNode(arr,openSet):
    #returns index of minimum value/cost
    iMin = openSet[0]
    for i in openSet:
        if arr[iMin] > arr[i]:
            iMin = i
    return iMin

def heuristicCost(i,goal,arrOfCoords):
    return distanceKM(arrOfCoords,i,goal)

def pathReconstruction(cameFrom,curr,cost):
    result = [curr]
    while cameFrom[curr] != None:
        curr = cameFrom[curr]
        result.insert(0,curr)
    result.append(cost)
    return result

def findNeighbors(adjMatrix,curr):
    neighbors = []
    for i in range(len(adjMatrix)):
        if(adjMatrix[curr][i] != 100000):
            neighbors.append(i)
    return neighbors

def Astar(start,goal,arrOfCoords,adjMatrix):
    #returns array of integer, which represents the vertices that has to be visited.
    #adjMatrix : represents the graph
    openSet = [start] #ready to evaluate.
    closedSet = [] #already evaluated.
    fScore = [100000] * len(arrOfCoords) #total cost from start to goal, passing by i = fScore[i]
    gScore = [100000] * len(arrOfCoords) #cost from start to i = gScore[i]
    fScore[start] = heuristicCost(start,goal,arrOfCoords)
    gScore[start] = 0
    cameFrom = [None] * len(arrOfCoords) # cameFrom[i] : simpul i telah ditelusuri dari simpul cameFrom[i]
    

    while openSet: #selama openSet masih ada isinya
        curr = findMinNode(fScore,openSet)
        if curr == goal:
            return pathReconstruction(cameFrom,curr,gScore[curr])
        else:
            openSet.remove(curr)
            closedSet.insert(0,curr)

            #curr bertetangga dengan siapa saja?
            neighborCurr = findNeighbors (adjMatrix, curr)
 
            for neighbor in neighborCurr:
                if not (neighbor in closedSet):
                    if not (neighbor in openSet):
                        openSet.append(neighbor)
                    temp_gScore = gScore[curr] + adjMatrix[curr][neighbor]

                    if temp_gScore < gScore[neighbor]:
                        cameFrom[neighbor] = curr
                        gScore[neighbor] = temp_gScore
                        fScore[neighbor] = gScore[neighbor] + heuristicCost(neighbor,goal,arrOfCoords)

    #if not successful
    return None