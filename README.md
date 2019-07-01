# Clusters

In this repository so far there are two clusters. The first one is the K-Means Cluster and the second one is the
Bisecting K-Means Cluster.

Clusters or clustering is the task of grouping a set of objects in such a way that objects in the same group (called a cluster) 
are more similar (in some sense) to each other than to those in other groups (clusters)

-->K-Means Cluster

In this algorithm we give the K-Mean Cluster an array of points and the amount of clusters we want to make.
This algorithm will take n-amount of random points inside the array (n is the number of clusters we want to have) and will
divede it in n clusters. The clusters are devided based on the distance between the random points and the points in the array.


The result will be the center position of every cluster. (For example answer = [ [x1, y1], [x2, y2], [x3, y3] ])


-->Bisecting K-Means Cluster

The Bisecting K-Means-Cluster works like the the K-Means-Cluster but with a twist.


This are the steps that it does:


1)Pick a cluster to split. (In our case the cluster with the most points inside it)

2)Find 2 sub-clusters using the basic k-Means algorithm (Bisecting step)

3)Repeat step 2, the bisecting step, for ITER times and take the split that produces the clustering with the highest overall similarity.

4)Repeat steps 1, 2 and 3 until the desired number of clusters is reached.


-->Some links that might be useful:

http://minethedata.blogspot.com/2012/08/bisecting-k-means.html

https://en.wikipedia.org/wiki/Cluster_analysis


#Auther Alehandro
