#Clustering algorithm in a the 2 dimensions
import random
import collections  #Only use for the Counter()
import math

import matplotlib.pyplot as plt #Graphical View


class ClusterKMeans():
    def __init__(self, arrayCluster, numberCluster=2):
        self.arrayCluster = arrayCluster
        self.numberCluster = numberCluster

        #We need those for better graphs
        self.K = []
        self.minValues = [] #We will need that in the Bisecting KMeans clustering

    #Euclidean Distance_Func
    def Distance(self, x1, y1, x2, y2):
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

    def clusterKMeans(self):
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
        if(self.numberCluster <= 1):
            return -1

        #Pick N-Random Clusters..
        K = []
        for i in range(0, self.numberCluster):
            xNumber = random.randint(0,len(self.arrayCluster)-1)
            while(xNumber in K):
                xNumber = random.randint(0,len(self.arrayCluster)-1)
            K.append(xNumber)

        #Start solving the Cluster
        clusterDistances = []
        for i in K:
            temp = []   #Temporary store the values here
            x1 = self.arrayCluster[i][0]    #1st coordinate
            y1 = self.arrayCluster[i][1]    #2nd coordinate
            for j in self.arrayCluster:
                temp.append(self.Distance(x1, y1, j[0], j[1]))

            clusterDistances.append(temp)

        #Finding the right value Clusters
        for i in range(0, len(self.arrayCluster)):
            min = 10000
            minName = 10000
            for k,j in enumerate(clusterDistances):
                if(min > j[i]):
                    min = j[i]
                    minName = k

            self.minValues.append(minName)

        #Last step is to sum the values and divede them..
        finalClustersValues = []
        for i in range(0, self.numberCluster):
            sum1 = 0
            sum2 = 0
            counter = 0
            for k,j in enumerate(self.minValues):
                if(i == j):
                    sum1 += self.arrayCluster[k][0]
                    sum2 += self.arrayCluster[k][1]
                    counter += 1

            finalClustersValues.append([round(sum1/counter, 1), round(sum2/counter, 1)])

        return finalClustersValues

class Clusters(ClusterKMeans):
    def __init__(self, array, clusters):
        super().__init__(array) #initialize the KMeans constractor..

        #__init__ the variables
        self.array = array
        self.arrayCluster = self.array
        self.clusters = clusters
        self.answer = [] #All of the answers points
        globalMinValueTemp = []

    #override the method because the clusters are always set to 2(defualt)
    def clusterKMeans(self):
        self.numberCluster = self.clusters
        self.answer = super().clusterKMeans()
        self.globalMinValueTemp = self.minValues  #For the graph
        return self.answer

    #Sum of Squared Errors helps us to find which cluster to Biscect
    def sumOfSquaredErrors(self):
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
        for i in range(0, len(self.answer)):
            temp = collections.Counter(self.globalMinValueTemp)

            min = 10000
            minName = 10000
            for valueMin in temp:
                if(min <= temp[valueMin]):
                    min = temp[valueMin]
                    minName = valueMin

            temp = []
            for k,j in enumerate(self.globalMinValueTemp):
                    temp.append(self.Distance(self.answer[i][0], self.answer[i][1], self.array[k][0], self.array[k][1]))

            temp1 = []
            for valueGrabber in range(self.clusters):
                temp1.append([valueGrabber, 0])
                for k,j in enumerate(self.globalMinValueTemp):
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
            finalArray.append(self.answer[i])

        return finalArray


    #The criterion will be the amount of points each cluster will have
    def clusterGrabber(self):
        """
        Deciding which cluster to devide. In our case the cluster with the
        most points inside it

        :param_1, The points that the cluster have:
        :param_2, All of the points that the cluster have:
        :returns, The new array that we want to check:
        """
        #Finding which one has the most values

        temp = collections.Counter(self.globalMinValueTemp)

        max = -1
        maxName = -1
        for valueMax in temp:
            if(max <= temp[valueMax]):
                max = temp[valueMax]
                maxName = valueMax

        #Assigning the new Array
        newArray = []
        for k,i in enumerate(self.globalMinValueTemp):
            if(i == maxName):
                newArray.append(self.array[k])

        #This is modified in order to make a better Graph
        return newArray

    def fixGlobalMinValue(self, count):
        """
        Fixing the globalMinValueTemp (The points that every cluster have).

        :param_1, The points that the cluster have:
        :param_2, All of the points that the cluster have:
        :param_3, The amount of clusters we have so far:
        :returns, The new fixed globalMinValueTemp:
        """

        temp = collections.Counter(self.globalMinValueTemp)

        max = -1
        maxName = -1
        for valueMax in temp:
            if(max <= temp[valueMax]):
                max = temp[valueMax]
                maxName = valueMax

        temp = collections.Counter(self.minValues)

        min = -1
        minName = -1
        for valueMin in temp:
            if(min <= temp[valueMin]):
                min = temp[valueMin]
                minName = valueMin

        c = 0
        for k,i in enumerate(self.globalMinValueTemp):
            if(i == maxName):
                if(minName == self.minValues[c]):
                    self.globalMinValueTemp[k] = count
                c += 1

        return self.globalMinValueTemp

    def clusterBiscectingKMeans(self):
        """
        This is the main Function, that need to be called by the user. It takes an
        array and the amount of clusters and starts deviding them until it reaches a
        number of cluster that is given.

        :param_1, the points that we want to give:
        :param_2, the number of clusters we want to get at the end:
        :returns the center point of the necessary cluster:
        """

        count = 2
        for i in range(0, self.clusters-1):
            #Checking if the it is the first step..
            if(i == 0):
                result = super().clusterKMeans()
                #Adding the two solutions inside the answer variable
                self.answer.append(result[0])
                self.answer.append(result[1])

                self.globalMinValueTemp = self.minValues
            else:
                #Picking a Cluster to divide
                self.arrayCluster = self.clusterGrabber()

                #Adding the two solutions inside the answer variable
                self.minValues = []  #We need to reset that value
                result = super().clusterKMeans()

                self.answer.append(result[0])
                self.answer.append(result[1])

                #Fixing the globalMinValueTemp array
                self.globalMinValueTemp = self.fixGlobalMinValue(count)
                count += 1

        self.answer = self.sumOfSquaredErrors()

        return self.answer

    def plot(self):
        plt = GraphicalPlot(self.array, self.answer, self.clusters, self.globalMinValueTemp)
        plt.graphicalPlot()

class GraphicalPlot:
    def __init__(self, arrayCluster, answers, clusters, minValues):
        self.arrayCluster = arrayCluster
        self.answers = answers
        self.clusters = clusters
        self.minValues = minValues

    def graphicalPlot(self):
        
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
        for i in range(self.clusters):
            firstArrayVolTemp1 = []
            firstArrayVolTemp2 = []
            for k,j in enumerate(self.minValues):
                if(j == i):
                    firstArrayVolTemp1.append(self.arrayCluster[k][0])
                    firstArrayVolTemp2.append(self.arrayCluster[k][1])
            firstArrayVol1.append(firstArrayVolTemp1)
            firstArrayVol2.append(firstArrayVolTemp2)

        thirdArray = []
        fourthArray = []
        for i in self.answers:
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


array = []  #array is the param_1 in the first function
for i in range(10):
    array.append([
        random.uniform(0, 5),
        random.uniform(0, 5)
    ])

clusters = 5  #The amount of clusters we cant to produce.
cluster = Clusters(array, clusters)
print(cluster.clusterKMeans())

cluster.plot()
