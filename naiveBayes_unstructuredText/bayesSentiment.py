#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
import os, codecs, math


class bayesText:

    def __init__(self, trainingdir, stopwordlist, ignoreBucket):

        self.vocabulary = {}
        self.totals = {}
        self.prob = {}

        with open(stopwordlist, 'r') as f:
            lines = f.readlines()
            self.stopwords = set([x.strip() for x in lines])

        categories = os.listdir(trainingdir)
        # filter out files that are not directories
        self.categories = [filename for filename in categories
                           if os.path.isdir(trainingdir + filename)]
        for category in self.categories:
            (self.prob[category], self.totals[category]) =\
            self.train(trainingdir, category, ignoreBucket)

        toDelete = [x for x in self.vocabulary if self.vocabulary[x] < 3]
        for word in toDelete:
            del self.vocabulary[word]

        # now compute probabilities
        vocabLength = len(self.vocabulary)
        for category in self.categories:
            denominator = self.totals[category] + vocabLength
            for word in self.vocabulary:
                count = self.prob[category].get(word, 0)
                self.prob[category][word] = (float(count + 1) / denominator)


    def train(self, trainingdir, category, bucketNumberToIgnore):

        ignore = "%i" % bucketNumberToIgnore
        currentdir = trainingdir + category
        directories = os.listdir(currentdir)
        counts = {}
        total = 0
        for directory in directories:
            if directory != ignore:
                currentBucket = trainingdir + category + "/" + directory
                files = os.listdir(currentBucket)
                for file in files:
                    f = codecs.open(currentBucket + '/' + file, 'r', 'iso8859-1')
                    for line in f:
                        tokens = line.split()
                        for token in tokens:
                            token = token.strip('\'".,?:-')
                            token = token.lower()
                            if token != '' and not token in self.stopwords:
                                self.vocabulary.setdefault(token, 0)
                                self.vocabulary[token] += 1
                                counts.setdefault(token, 0)
                                counts[token] += 1
                                total += 1
                    f.close()

        return (counts, total)


    def classify(self, filename):

        results = dict([[c, 0] for c in self.categories])
        f = codecs.open(filename, 'r', 'iso8859-1')
        for line in f:
            tokens = line.split()
            for token in tokens:
                token = token.strip('\'".,?:-').lower()
                if token in self.vocabulary:
                    for category in self.categories:
                        results[category] += math.log(self.prob[category][token])
        f.close()
        results = [[token, results[token]] for token in\
                   sorted(results, key=results.get, reverse=True)]

        return results[0][0]


    def testCategory(self, direc, category, bucketNumber):

        results = {}
        directory = direc + ("%i/" % bucketNumber)
        files = os.listdir(directory)
        for file in files:
            result = self.classify(directory + file)
            results.setdefault(result, 0)
            results[result] += 1

        return results


    def test(self, testdir, bucketNumber):
        """Test all files in the test directory--that directory is
        organized into subdirectories--each subdir is a classification
        category"""
        results = {}
        categories = os.listdir(testdir)
        # filter out files that are not directories
        categories = [filename for filename in categories if
                      os.path.isdir(testdir + filename)]
        correct = 0
        total = 0
        for category in categories:
            results[category] = self.testCategory(
                testdir + category + '/', category, bucketNumber)

        return results


def tenfold(dataPrefix, stoplist):
    results = {}
    for i in range(0,10):
        print('computing the %i bucket' % i)
        bT = bayesText(dataPrefix, stoplist, i)
        r = bT.test(theDir, i)
        for (key, value) in r.items():
            results.setdefault(key, {})
            for (ckey, cvalue) in value.items():
                results[key].setdefault(ckey, 0)
                results[key][ckey] += cvalue
                categories = list(results.keys())
    categories.sort()
    print("\n       Classified as: ")
    header = "          "
    subheader = "        +"
    for category in categories:
        header += "% 2s   " % category
        subheader += "-----+"
    print(header)
    print(subheader)
    total = 0.0
    correct = 0.0
    for category in categories:
        row = " %s    |" % category 
        for c2 in categories:
            if c2 in results[category]:
                count = results[category][c2]
            else:
                count = 0
            row += " %3i |" % count
            total += count
            if c2 == category:
                correct += count
        print(row)
    print(subheader)
    print("\n%5.3f percent correct" %((correct * 100) / total))
    print("total of %i instances" % total)


if __name__ == '__main__':
    import os
    curr_path = os.getcwd()
    prefixPath = curr_path + "/review_polarity_buckets/"
    theDir = prefixPath + "/txt_sentoken/"
    stoplistfile = prefixPath + "stopwords25.txt"
    tenfold(theDir, stoplistfile)
