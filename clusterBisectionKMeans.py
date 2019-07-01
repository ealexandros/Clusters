#Clustering algorithm in a the 2 dimensions
import random
import collections  #Only use for the Counter()
import math

import matplotlib.pyplot as plt #Graphical View


#-----------#Random Inputs#-----------#
array = []
for i in range(100):
    array.append([
        random.uniform(0, 50),
        random.uniform(0, 50)
    ])

clusters = 20  #The amount of clusters we cant to produce.


#-----------#Cluster K-Mean Function#-----------#

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

def clusterKMeans(arrayCluster, numberCluster=2):
    """
    This Function takes every point that we give it and the number of Clusters
    we want to make. First of all it takes two random points then it finds the
    distances between all points and lastly it check which point belongs in
    which cluster.

    This Function is inly called in the clusterBiscectingKMeans.

    :param_1, All of the points that we want it to analyze:
    :param_2, The number of clusters we want to make:
    :param_3, Random starting values:
    :param_4, The team of every cluster point:
    :returns, The correct cluster points:
    """

    #cheching if the cluster is (K) == 1
    if(numberCluster <= 1):
        return -1

    #Pick N-Random Clusters..
    K = []    #Taking the global K
    for i in range(0 ,numberCluster):
        xNumber = random.randint(0, len(arrayCluster)-1)
        while(xNumber in K):
            xNumber = random.randint(0, len(arrayCluster)-1)
        K.append(xNumber)

    #Start solving the Cluster
    clusterDistances = []
    for i in K:
        temp = []   #Temporary store the values here
        x1 = arrayCluster[i][0]    #1st coordinate
        y1 = arrayCluster[i][1]    #2nd coordinate
        for j in arrayCluster:
            temp.append(Distance(x1, y1, j[0], j[1]))

        clusterDistances.append(temp)

    #Finding the right value Clusters
    minValues = []
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

    #Adding some more values..
    finalClustersValues.append(minValues)

    return finalClustersValues

###########----Bisecting Kmeans Cluster----###########

#Sum of Squared Errors helps us to find which cluster to Biscect
def sumOfSquaredErrors(answers, globalMinValue, clusters):
    """
    This cluster deletes every extra element from the answers array. It
    it used at the end of the clusterBiscectingKMeans Function.

    :param_1, all of the center points of every cluster:
    :param_2, all of the clusters teams:
    :param_3, the amount of clusters:
    :returns the center point of the necessary cluster:
    """

    counter = 0
    finalArray = []
    finalArrayTemp = []
    for i in range(0, len(answers)):
        temp = collections.Counter(globalMinValue)

        min = 10000
        minName = 10000
        for valueMin in temp:
            if(min <= temp[valueMin]):
                min = temp[valueMin]
                minName = valueMin

        temp = []
        for k,j in enumerate(globalMinValue):
                temp.append(Distance(answers[i][0], answers[i][1], array[k][0], array[k][1]))

        temp1 = []
        for valueGrabber in range(clusters):
            temp1.append([valueGrabber, 0])
            for k,j in enumerate(globalMinValue):
                if(j == valueGrabber):
                    x = temp1[valueGrabber].pop(1) + temp[k]
                    temp1[valueGrabber].append(x)
        finalArrayTemp.append(temp1)


    finalArrayNumbers = []
    for i in range(clusters):
        min = 10000
        minName = 10000
        for k,j in enumerate(finalArrayTemp):
            if(min > j[i][1]):
                min = j[i][1]
                minName = k
        finalArrayNumbers.append(minName)

    for i in finalArrayNumbers:
        finalArray.append(answers[i])

    return finalArray

#The criterion will be the amount of points each cluster will have
def clusterGrabber(minValues, globalMinValueTemp):
    """
    Deciding which cluster to devide. In our case the cluster with the
    most points inside it

    :param_1, The points that the cluster have:
    :param_2, All of the points that the cluster have:
    :returns, The new array that we want to check:
    """
    #Finding which one has the most values
    global array #taking the array with all the points inside.

    temp = collections.Counter(globalMinValueTemp)

    max = -1
    maxName = -1
    for valueMax in temp:
        if(max <= temp[valueMax]):
            max = temp[valueMax]
            maxName = valueMax

    #Assigning the new Array
    newArray = []
    for k,i in enumerate(globalMinValueTemp):
        if(i == maxName):
            newArray.append(array[k])

    #This is modified in order to make a better Graph
    return newArray

def fixGlobalMinValue(minValues, globalMinValueTemp, count):
    """
    Fixing the globalMinValueTemp (The points that every cluster have).

    :param_1, The points that the cluster have:
    :param_2, All of the points that the cluster have:
    :param_3, The amount of clusters we have so far:
    :returns, The new fixed globalMinValueTemp:
    """

    temp = collections.Counter(globalMinValueTemp)

    max = -1
    maxName = -1
    for valueMax in temp:
        if(max <= temp[valueMax]):
            max = temp[valueMax]
            maxName = valueMax

    temp = collections.Counter(minValues)

    min = -1
    minName = -1
    for valueMin in temp:
        if(min <= temp[valueMin]):
            min = temp[valueMin]
            minName = valueMin

    c = 0
    for k,i in enumerate(globalMinValueTemp):
        if(i == maxName):
            if(minName == minValues[c]):
                globalMinValueTemp[k] = count
            c += 1

    return globalMinValueTemp

def clusterBiscectingKMeans(array, clusters):
    """
    This is the main Function, that need to be called by the user. It takes an
    array and the amount of clusters and starts deviding them until it reaches a
    number of cluster that is given.

    :param_1, the points that we want to give:
    :param_2, the number of clusters we want to get at the end:
    :returns the center point of the necessary cluster:
    """

    answer = []   #All the Cluster answers
    count = 2
    for i in range(0, clusters-1):
        #Checking if the it is the first step..
        global globalMinValueTemp
        if(i == 0):
            result = clusterKMeans(array)
            #Adding the two solutions inside the answer variable
            answer.append(result[0])
            answer.append(result[1])

            globalMinValueTemp = result[2]
        else:
            #Picking a Cluster to divide
            array = clusterGrabber(result[2], globalMinValueTemp)

            #Adding the two solutions inside the answer variable
            result = clusterKMeans(array)
            answer.append(result[0])
            answer.append(result[1])

            #Fixing the globalMinValueTemp array
            globalMinValueTemp = fixGlobalMinValue(result[2], globalMinValueTemp, count)
            count += 1
    answer = sumOfSquaredErrors(answer, globalMinValueTemp, clusters)

    return answer

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
        for k,j in enumerate(globalMinValueTemp):
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
globalMinValueTemp = []

#---#Calling the Functions#---#

#The -1 is an error
answer = clusterBiscectingKMeans(array, clusters)
print("Cluster Coordinates: " + str(answer))

graphicalPlot(array, answer, clusters)
