#!/usr/bin/env python
# -*- coding:utf-8 -*-

import math


class Classifier:

    def __init__(self, bucketPrefix, testBucketNumber, dataFormat):

        self.prior = {}
        self.conditional = {}
        self.format = dataFormat.strip().split(',')

        total = 0
        classes = {}
        counts = {}
        # assistant for compute the mean and standard deviation
        totals = {}
        numericValues = {}

        for i in range(1, 11):
            if i != testBucketNumber:
                filename = "%s-%02i" % (bucketPrefix, i)
                with open(filename, 'r') as f:
                    lines = f.readlines()
                for line in lines:
                    fields = line.strip().split('\t')
                    ignore, vector, nums = [], [], []
                    for i in range(len(fields)):
                        if self.format[i] == 'num':
                            nums.append(float(fields[i]))
                        elif self.format[i] == 'attr':
                            vector.append(fields[i])
                        elif self.format[i] == 'comment':
                            ignore.append(fields[i])
                        elif self.format[i] == 'class':
                            category = fields[i]

                    # count total numbers
                    total += 1
                    # count category numbers
                    try:
                        classes[category] += 1
                    except KeyError:
                        classes[category] = 1
                    # count categorical conditional numbers
                    col = 0
                    counts.setdefault(category, {})
                    for columnValue in vector:
                        col += 1
                        counts[category].setdefault(col, {})
                        counts[category][col].setdefault(columnValue, 0)
                        counts[category][col][columnValue] += 1
                    numericValues.setdefault(category, {})
                    # process numeric attributes to compute mean and std.
                    totals.setdefault(category, {})
                    col = 0
                    for columnValue in nums:
                        col += 1
                        totals[category].setdefault(col, 0)
                        totals[category][col] += columnValue
                        numericValues[category].setdefault(col, [])
                        numericValues[category][col].append(columnValue)

        # prior probility
        for (category, count) in classes.items():
            self.prior[category] = 1.0 * count / total

        # conditional probabilities
        for (category, columns) in counts.items():
              self.conditional.setdefault(category, {})
              for (col, valueCounts) in columns.items():
                  self.conditional[category].setdefault(col, {})
                  for (attrValue, count) in valueCounts.items():
                      self.conditional[category][col][attrValue] = (
                          1.0 * count / classes[category])

        # means and standard deviation
        self.means = {}
        self.totals = totals
        for (category, columns) in totals.items():
            self.means.setdefault(category, {})
            for (col, cTotal) in columns.items():
                self.means[category][col] = 1.0 * cTotal / classes[category]
        self.ssd = {}
        for (category, columns) in numericValues.items():
            self.ssd.setdefault(category, {})
            for (col, values) in columns.items():
                SumOfSquareDifferences = 0
                theMean = self.means[category][col]
                for value in values:
                    SumOfSquareDifferences += (value - theMean)**2
                self.ssd[category][col] = math.sqrt(1.0 *\
                    SumOfSquareDifferences / (classes[category]  - 1))


    def classify(self, itemVector, numVector):

        results = []
        sqrt2pi = math.sqrt(2 * math.pi)
        for (category, prior) in self.prior.items():
            prob = prior
            col = 1
            for attrValue in itemVector:
                if not attrValue in self.conditional[category][col]:
                    prob = 0
                else:
                    prob = prob * self.conditional[category][col][attrValue]
                col += 1
            col = 1
            for x in numVector:
                mean = self.means[category][col]
                ssd = self.ssd[category][col]
                ePart = math.pow(math.e, -(x - mean)**2/(2*ssd**2))
                prob = prob * ((1.0 / (sqrt2pi*ssd)) * ePart)
                col += 1
            results.append((prob, category))

        return max(results)[1]


    def testBucket(self, bucketPrefix, bucketNumber):

        filename = "%s-%02i" % (bucketPrefix, bucketNumber)
        with open(filename, 'r') as f:
            lines = f.readlines()
        totals = {}
        loc = 1
        for line in lines:
            loc += 1
            data = line.strip().split('\t')
            vector, numV = [], []
            classInColumn = -1
            for i in range(len(self.format)):
                if self.format[i] == 'num':
                    numV.append(float(data[i]))
                elif self.format[i] == 'attr':
                    vector.append(data[i])
                elif self.format[i] == 'class':
                    classInColumn = i
            theRealClass = data[classInColumn]
            # input: categorial vector and numeric vector
            classifiedAs = self.classify(vector, numV)
            totals.setdefault(theRealClass, {})
            totals[theRealClass].setdefault(classifiedAs, 0)
            totals[theRealClass][classifiedAs] += 1

        return totals
 

def tenfold(bucketPrefix, dataFormat):
    results = {}
    for i in range(1, 11):
        c = Classifier(bucketPrefix, i, dataFormat)
        t = c.testBucket(bucketPrefix, i)
        for (key, value) in t.items():
            results.setdefault(key, {})
            for (ckey, cvalue) in value.items():
                results[key].setdefault(ckey, 0)
                results[key][ckey] += cvalue

    categories = list(results.keys())
    categories.sort()
    print("\n            Classified as: ")
    header = "             "
    subheader = "               +"
    for category in categories:
        header += "% 10s   " % category
        subheader += "-------+"
    print(header)
    print(subheader)
    total = 0.0
    correct = 0.0
    for category in categories:
        row = " %10s    |" % category
        for c2 in categories:
            if c2 in results[category]:
                count = results[category][c2]
            else:
                count = 0
            row += " %5i |" % count
            total += count
            if c2 == category:
                correct += count
        print(row)
    print(subheader)
    print("\n%5.3f percent correct" %((correct * 100) / total))
    print("total of %i instances" % total)


def pdf(mean, ssd, x):

    ePart = math.pow(math.e, -(x-mean)**2/(2*ssd**2))
    print (ePart)
    return (1.0 / (math.sqrt(2*math.pi)*ssd)) * ePart


if __name__ == '__main__':
    #house_format = 'class,' + ','.join(['attr'] * 16)
    #tenfold("house-votes/hv", house_format)
    pima_format = ','.join(['num'] * 8) + ',class'
    #tenfold("pimaSmall/pimaSmall", pima_format)
    tenfold("pima/pima", pima_format)
