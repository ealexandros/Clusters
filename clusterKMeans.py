#Clustering algorithm in a the 2 dimensions
import random
import math

import matplotlib.pyplot as plt #Graphical View


#-----------#Random Inputs#-----------#
array = []  #array is the param_1 in the first function
for i in range(200):
    array.append([
        random.uniform(0, 50),
        random.uniform(0, 50)
    ])

clusters = 20  #The amount of clusters we cant to produce.

#-----------#Clusters#-----------#

#Euclidean Distance_Func
def Distance(x1, y1, x2, y2):
    """
    This class is used inside the clusterKMeans in order to find the
    distances between to points. (We use the Euclidean methid in this case)

    :param_1_2, The x and y position of the first point:
    :param_3_4, The x and y position of the second point:
    :returns, The distance between two points:
    """
    first = (x1 - x2)**2
    second = (y1 - y2)**2
    return round(math.sqrt(first + second),1)

#Cluster K-Mean Function

def clusterKMeans(arrayCluster, numberCluster):
    """
    This Function takes every point that we give it and the number of Clusters
    we want to make. First of all it takes two random points (if we want 2 clusters, for 3 Clusters
    3 point etc) then it finds the distances between all points and lastly it check which point
    belongs in which cluster.

    :param_1, All of the points that we want it to analyze:
    :param_2, The number of clusters we want to make:
    :returns, The correct cluster points:
    """
    #cheching if the cluster is (K) == 1
    if(numberCluster <= 1):
        return -1

    #Pick N-Random Clusters..
    K = []
    for i in range(0 ,numberCluster):
        xNumber = random.randint(0,len(arrayCluster)-1)
        while(xNumber in K):
            xNumber = random.randint(0,len(arrayCluster)-1)
        K.append(xNumber)

    #Start solving the Cluster
    clusterDistances = []
    for i in K:
        temp = []   #Temporary store the values here
        x1 = arrayCluster[i][0]    #1st coordinate
        y1 = arrayCluster[i][1]    #2nd coordinate
        for j in array:
            temp.append(Distance(x1, y1, j[0], j[1]))

        clusterDistances.append(temp)

    #Finding the right value Clusters
    global minValues
    for i in range(0, len(arrayCluster)):
        min = 10000
        minName = 10000
        for k,j in enumerate(clusterDistances):
            if(min > j[i]):
                min = j[i]
                minName = k

        minValues.append(minName)

    #Last step is to sum the values and divede them..
    finalClustersValues = []
    for i in range(0, numberCluster):
        sum1 = 0
        sum2 = 0
        counter = 0
        for k,j in enumerate(minValues):
            if(i == j):
                sum1 += arrayCluster[k][0]
                sum2 += arrayCluster[k][1]
                counter += 1

        finalClustersValues.append([round(sum1/counter, 1), round(sum2/counter, 1)])

    return finalClustersValues


######-------Graphical View-------######

def graphicalPlot(arrayCluster, answers, clusters):
    """
    This function plots our the given points.
    The "Green Squere" are the correct cluster points.
    All of the different colored circles are the clusters teams.

    :param_1, All of the points:
    :param_2, The correct cluster points:
    :param_#, The number of clusters we want to make:
    """

    #Finding the right cluster team
    firstArrayVol1 = []
    firstArrayVol2 = []
    for i in range(clusters):
        firstArrayVolTemp1 = []
        firstArrayVolTemp2 = []
        for k,j in enumerate(minValues):
            if(j == i):
                firstArrayVolTemp1.append(arrayCluster[k][0])
                firstArrayVolTemp2.append(arrayCluster[k][1])
        firstArrayVol1.append(firstArrayVolTemp1)
        firstArrayVol2.append(firstArrayVolTemp2)

    thirdArray = []
    fourthArray = []
    for i in answers:
        thirdArray.append(i[0])
        fourthArray.append(i[1])

    #Making some Labels to the x,y axis
    plt.xlabel("x axis")
    plt.ylabel("y axis")

    #Adding the points
    fig, ax = plt.subplots()

    for i in range(len(firstArrayVol1)):
        plt.plot(firstArrayVol1[i], firstArrayVol2[i], "o")

    plt.plot(thirdArray, fourthArray, "gs")

    ax.set_aspect("equal", 'datalim')
    plt.show()


#We need this values to be Global in order to draw a better Graph
minValues = []  #the team of every cluster point

#The -1 is an error
answer = clusterKMeans(array, clusters)
print("Cluster Coordinates: " + str(answer))

#Calling the plot.
graphicalPlot(array, answer, clusters)
