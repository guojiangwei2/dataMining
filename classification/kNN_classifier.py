#!/usr/bin/env python
# -*- coding:utf-8 -*-

import heapq
import random

#file_path = '/home/ubuntu14/jeffGithub/machine_learning/classification/pimaSmall/'


class Classifier:

    def __init__(self, bucketPrefix, testBucketNumber, dataFormat, k=10, fn='standardize', r=2):
        # transform the rawfile to the normdata
        # compute the normBase and deviation
        # k stand for the kNN's k nearest neighbor
        # fn stand for the normalization method, default for standardize
        # r stand for the way to compute instance distance,
        # default for euclidean distance
        self.bucketPrefix = bucketPrefix
        self.testBucketNumber = testBucketNumber
        self.k = k
        self.fn = fn
        self.r = r
        self.normbaseAndDeviation = []
        self.format = dataFormat.strip().split(',')
        self.data = []
        for i in range(1, 11):
            if i != self.testBucketNumber:
                filename = "%s-%02i" % (self.bucketPrefix, i)
                with open(filename, 'r') as f:
                    lines = f.readlines()
                for line in lines[1:]:
                    fields = line.strip().split('\t')
                    ignore = []
                    vector = []
                    for i in range(len(fields)):
                        if self.format[i] == 'num':
                            vector.append(float(fields[i]))
                        elif self.format[i] == 'comment':
                            ignore.append(fields[i])
                        elif self.format[i] == 'class':
                            classification = fields[i]
                    self.data.append((classification, vector, ignore))
        self.rawData = list(self.data)
        self.vlen = len(self.data[0][1])
        for i in range(self.vlen):
            self.normalizeColumn(i)

    def getNormbase(self, lst):
        if self.fn == 'standardize':
            # get median
            sorted_lst = sorted(lst)
            length = len(lst)
            is_odd = length % 2 == 1
            idx = int((length - 1) / 2) if is_odd else int(length / 2 - 1)
            normbase = sorted_lst[idx] if is_odd else sum(sorted_lst[idx: idx + 2]) / 2.0
        elif self.fn == 'normalize':
            # get mean
            normbase = sum(lst) / len(lst)
        elif self.fn == 'range':
            # get minimum value
            normbase = min(lst)
        return normbase if lst else None

    def getDeviation(self, lst, normbase):
        if self.fn == 'standardize':
            # get absolute standard deviation
            deviation = sum([abs(x - normbase) for x in lst]) / len(lst)
        elif self.fn == 'normalize':
            # get standard deviation
            num = sum([pow(x - normbase, 2) for x in lst])
            deviation = num / (len(lst) - 1) if len(lst) > 1 else None
        elif self.fn == 'range':
            # get range
            deviation = max(lst) - min(lst)
        return deviation if lst else None

    def normalizeColumn(self, columnNumber):
        col = [v[1][columnNumber] for v in self.data]
        normbase = self.getNormbase(col)
        deviation = self.getDeviation(col, normbase)
        self.normbaseAndDeviation.append((normbase, deviation))
        for v in self.data:
            v[1][columnNumber] = (v[1][columnNumber] - normbase) / deviation

    def normalizeVector(self, v):
        vector = list(v)
        for i in range(len(vector)):
            (normbase, deviation) = self.normbaseAndDeviation[i]
            vector[i] = (vector[i] - normbase) / deviation
        return vector

    def computeDistance(self, vector1, vector2):
        # r=1: manhattan distance, r=2: euclidean distance
        distance = 0
        vlen = len(vector1)
        for i in range(vlen):
            distance += pow(abs(vector1[i] - vector2[i]), self.r)
        return pow(distance, 1.0 / self.r) if vlen else 0

    def knn(self, itemVector):
        # input: classifier and testItemVector
        # output: kNN predict class
        neighbors = heapq.nsmallest(self.k, [(self.computeDistance(itemVector, item[1]), item)
                                    for item in self.data])
        results = {}
        for neighbor in neighbors:
            theClass = neighbor[1][0]
            results.setdefault(theClass, 0)
            results[theClass] += 1
        resultList = sorted([(i[1], i[0]) for i in results.items()], reverse=True)
        maxVotes = resultList[0][0]
        possibleAnswers = [i[1] for i in resultList if i[0] == maxVotes]
        answer = random.choice(possibleAnswers)
        return answer

    def classify(self, itemVector):
        return self.knn(self.normalizeVector(itemVector))

    def testBucket(self):
        # input: test data, output: confusion matrix
        filename = "%s-%02d" % (self.bucketPrefix, self.testBucketNumber)
        with open(filename, 'r') as f:
            lines = f.readlines()
        totals = {}
        for line in lines:
            data = line.strip().split('\t')
            vector = []
            classInColumn = -1
            for i in range(len(self.format)):
                if self.format[i] == 'num':
                    vector.append(float(data[i]))
                elif self.format[i] == 'class':
                    classInColumn = i
            theRealClass = data[classInColumn]
            classifiedAs = self.classify(vector)
            totals.setdefault(theRealClass, {})
            totals[theRealClass].setdefault(classifiedAs, 0)
            totals[theRealClass][classifiedAs] += 1
        return totals
