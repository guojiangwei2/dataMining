#!/usr/bin/env python
# -*- coding:utf-8 -*-

import math
import random 
import numpy


class kClusterer:

    def __init__(self, filename, k):
        """ k is the number of clusters to make
        This init method:
           1. reads the data from the file named filename
           2. stores that data by column in self.data
           3. normalizes the data using Modified Standard Score
           4. randomly selects the initial centroids
           5. assigns points to clusters associated with those centroids
        """
        self.k = k
        self.iterationNumber = 0
        self.pointsChanged = 0
        self.sse = 0

        with open(filename, 'r') as f:
            lines = f.readlines()
            header = lines[0].strip().split(',')
            self.cols = len(header)
            self.obvs = len(lines) - 1

        rawData = [line.strip().split(',') for line in lines[1:]]
        rawDataT = numpy.array(rawData).T.tolist()
        self.data = [[], ] * self.cols
        for i in range(self.cols):
            if i == 0:
                self.data[i] = rawDataT[i]
            else:
                rawVector = [int(x) for x in rawDataT[i]]
                self.data[i] = self.normalizeColumn(rawVector)

        # represent the cluster that each point belongs to
        self.memberOf = [-1, ] * self.obvs

        # select the random centroids
        random.seed()
        self.selectInitialCentroids()
        self.assignPointsToCluster()


    def getMedian(self, lst):
        sorted_lst = sorted(lst)
        length = len(lst)
        is_odd = length % 2 == 1
        idx = int((length - 1) / 2) if is_odd else int(length / 2 - 1)
        median = sorted_lst[idx] if is_odd else sum(sorted_lst[idx: idx + 2]) / 2.0
        return median


    def normalizeColumn(self, vector):
        median = self.getMedian(vector)
        asd = sum([abs(x - median) for x in vector]) * 1.0 / len(vector)
        result = [(x - median) * 1.0 / asd for x in vector]
        return result


    def eDistance(self, i, j):
        # compute distance of point i and centroid j
        # centroid j is point of data
        sumSquares = 0
        for k in range(1, self.cols):
            sumSquares += (self.data[k][i] - self.data[k][j])**2
        return math.sqrt(sumSquares)


    def distanceToClosestCentroid(self, point, centroidList):
        result = 999999
        for centroid in centroidList:
            distance = self.eDistance(point, centroid)
            if distance < result:
                result = distance
        return result


    def selectInitialCentroids(self):
        # implement the k-means++ method of selecting
        # the set of initial centroids
        centroids = []
        current = random.choice(range(self.obvs))
        centroids.append(current)
        for i in range(0, self.k - 1):
            weights = [self.distanceToClosestCentroid(x, centroids) 
                       for x in range(self.obvs)]
            total = sum(weights)
            weights = [x / total for x in weights]

            # the roulette wheel simulation
            num = random.random()
            total = 0
            x = -1
            while total < num:
                x += 1
                total += weights[x]
            centroids.append(x)

        self.centroids = [[self.data[i][r]  for i in range(1, self.cols)]
                            for r in centroids]


    def updateCentroids(self):
        # Using the points in the clusters, determine the centroid
        # (mean point) of each cluster
        members = [self.memberOf.count(i) for i in range(len(self.centroids))]
        # self.centroids is a list of vectors represent the centroid point
        self.centroids = [[sum([self.data[k][i]
                            for i in range(self.obvs)
                            if self.memberOf[i] == centroid])/members[centroid]
                           for k in range(1, self.cols)]
                          for centroid in range(len(self.centroids))]


    def euclideanDistance(self, i, j):
        # compute distance of point i and centroid j
        # centroid j is an independent vector
        sumSquares = 0
        for k in range(1, self.cols):
            sumSquares += (self.data[k][i] - self.centroids[j][k-1])**2
        return math.sqrt(sumSquares)


    def assignPointToCluster(self, i):
        # assign point to cluster based on distance from centroids
        min = 999999
        clusterNum = -1
        for centroid in range(self.k):
            dist = self.euclideanDistance(i, centroid)
            if dist < min:
                min = dist
                clusterNum = centroid
        # keep track of changing points
        if clusterNum != self.memberOf[i]:
            self.pointsChanged += 1
        # add square of distance to running sum of squared error
        self.sse += min**2
        return clusterNum


    def assignPointsToCluster(self):
        # assign each data point to a cluster
        self.pointsChanged = 0
        self.sse = 0
        self.memberOf = [self.assignPointToCluster(i) for i in range(self.obvs)]


    def kCluster(self):
        # updates the centroids by computing the mean point of each cluster
        # re-assign the points to clusters based on these new centroids
        # until the number of points that change cluster membership is less than 1%.
        done = False
        while not done:
            self.iterationNumber += 1
            self.updateCentroids()
            self.assignPointsToCluster()
            if float(self.pointsChanged) / len(self.memberOf) <  0.01:
                done = True

        print("Final SSE: %f" % self.sse)


    def showMembers(self):
        # display the cluster res
        for centroid in range(len(self.centroids)):
             print ("\n\nClass %i\n========" % centroid)
             for name in [self.data[0][i] for i in range(self.obvs)
                          if self.memberOf[i] == centroid]:
                 print(name)


if __name__ == '__main__':
    km = kClusterer('/home/ubuntu14/jeffGithub/machine_learning/clustering/dogs.csv', 3)
    km.kCluster()
    km.showMembers()
