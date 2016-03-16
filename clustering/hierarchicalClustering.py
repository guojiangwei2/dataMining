#!/usr/bin/env python
# -*- coding:utf-8 -*-

from Queue import PriorityQueue
import math
import numpy


class hClusterer:

    def __init__(self, filename):

        with open(filename, 'r') as f:
            lines = f.readlines()
            header = lines[0].strip().split(',')
            self.cols = len(header)
            self.rows = len(lines) - 1

        rawData = [line.strip().split(',') for line in lines[1:]]
        rawDataT = numpy.array(rawData).T.tolist()
        self.data = [[], ] * self.cols
        for i in range(self.cols):
            if i == 0:
                self.data[i] = rawDataT[i]
            else:
                rawVector = [int(x) for x in rawDataT[i]]
                self.data[i] = self.normalizeColumn(rawVector)

        self.counter = 0
        self.queue = PriorityQueue()
        for i in range(self.rows):
            neighbors = dict([[j, ((i, j), self.distance(i, j))]
                              for j in range(self.rows) if i != j])
            sorted_neighbors = sorted([[neighbors[x][1], neighbors[x][0]] for x in neighbors])
            minDistance = sorted_neighbors[0][0]
            nearestPair = sorted(sorted_neighbors[0][1])

            # minDistance uniqueIdentity obv_label pair distanceDict
            self.queue.put((minDistance, self.counter,
                            [[self.data[0][i]], nearestPair, neighbors]))
            self.counter += 1


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


    def distance(self, i, j):
        sumSquares = 0
        for k in range(1, self.cols):
            sumSquares += (self.data[k][i] - self.data[k][j])**2
        return math.sqrt(sumSquares)


    def cluster(self):

        done = False
        while not done:
            # minDistance uniqueIdentity [obv_label pair distanceDict]
            topOne = self.queue.get()
            nearestPair = sorted(topOne[2][1])
            if not self.queue.empty():
                nextOne = self.queue.get()
                nearPair = sorted(nextOne[2][1])
                # check for the pair of the popped two elements
                # pop another prior one and push the popped back until paired
                tmp = []
                while nearPair != nearestPair:
                    tmp.append((nextOne[0], self.counter, nextOne[2]))
                    self.counter += 1
                    nextOne = self.queue.get()
                    nearPair = sorted(nextOne[2][1])
                # push the unpaired items back in the queue
                for item in tmp:
                    self.queue.put(item)

                # curCluster is, perhaps obviously, the new cluster
                # which combines cluster item1 with cluster item2.
                if len(topOne[2][0]) == 1:
                    item1 = topOne[2][0][0]
                else:
                    item1 = topOne[2][0]
                if len(nextOne[2][0]) == 1:
                   item2 = nextOne[2][0][0]
                else:
                    item2 = nextOne[2][0]
                curCluster = (item1, item2)

                # Now I am doing two things. First, finding the nearest
                # neighbor to this new cluster. Second, building a new
                # neighbors list by merging the neighbors lists of item1
                # and item2. If the distance between item1 and element 23
                # is 2 and the distance betweeen item2 and element 23 is 4
                # the distance between element 23 and the new cluster will
                # be 2 (i.e., the shortest distance).
                minDistance = 99999
                nearestPair = ()
                nearestNeighbor = ''
                merged = {}
                nNeighbors = nextOne[2][2]
                for (key, value) in topOne[2][2].items():
                    if key in nNeighbors:
                        if nNeighbors[key][1] < value[1]:
                            dist =  nNeighbors[key]
                        else:
                            dist = value
                        if dist[1] < minDistance:
                            minDistance =  dist[1]
                            nearestPair = dist[0]
                            nearestNeighbor = key
                        merged[key] = dist

                if merged == {}:
                    return curCluster
                else:
                    self.queue.put((minDistance, self.counter,
                                    [curCluster, nearestPair, merged]))
                    self.counter += 1


def printDendrogram(T, sep=3):
    """Print dendrogram of a binary tree. Each tree node is represented by a
    length-2 tuple. printDendrogram is written and provided by David Eppstein
    2002. Accessed on 14 April 2014:
    http://code.activestate.com/recipes/139422-dendrogram-drawing/ """

    def isPair(T):
        return type(T) == tuple and len(T) == 2

    def maxHeight(T):
        h = max(maxHeight(T[0]), maxHeight(T[1])) if isPair(T) else len(str(T))
        return h + sep

    activeLevels = {}

    def traverse(T, h, isFirst):
        if isPair(T):
            traverse(T[0], h - sep, 1)
            s = [' '] * (h - sep)
            s.append('|')
        else:
            s = list(str(T))
            s.append(' ')

        while len(s) < h:
            s.append('-')

        if (isFirst >= 0):
            s.append('+')
            if isFirst:
                activeLevels[h] = 1
            else:
                del activeLevels[h]

        A = list(activeLevels)
        A.sort()
        for L in A:
            if len(s) < L:
                while len(s) < L:
                    s.append(' ')
                s.append('|')

        print (''.join(s))

        if isPair(T):
            traverse(T[1], h-sep, 0)

    traverse(T, maxHeight(T), -1)


if __name__ == '__main__':
    filename = '/home/ubuntu14/jeffGithub/machine_learning/clustering/dogs.csv'
    hg = hClusterer(filename)
    cluster = hg.cluster()
    printDendrogram(cluster)
