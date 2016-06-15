#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function
import os, codecs, math


class bayesText:

    def __init__(self, trainingdir, stopwordlist):
        """This class implements a naive Bayes approach to text
        classification
        trainingdir is the training data. Each subdirectory of
        trainingdir is titled with the name of the classification
        category -- those subdirectories in turn contain the text
        files for that category.
        The stopwordlist is a list of words (one per line) will be
        removed before any counting takes place.
        """
        self.vocabulary = {}
        self.prob = {}
        self.totals = {}

        with codecs.open(stopwordlist, 'r', 'iso8859-1') as f:
            lines = f.readlines()
            self.stopwords = set([x.strip() for x in lines])

        categories = os.listdir(trainingdir)
        # filter out files that are not directories
        self.categories = [filename for filename in categories
                           if os.path.isdir(trainingdir + filename)]
        print("Counting ...")
        for category in self.categories:
            print('    ' + category)
            (self.prob[category], self.totals[category]) =\
            self.train(trainingdir, category)

        # delete the word the appear for less than 3 times
        toDelete = [word for word in self.vocabulary if self.vocabulary[word] < 3]
        for word in toDelete:
            del self.vocabulary[word]

        print("Computing probabilities:")
        vocabLength = len(self.vocabulary)
        for category in self.categories:
            print('    ' + category)
            denominator = self.totals[category] + vocabLength
            for word in self.vocabulary:
                count = self.prob[category].get(word, 0)
                self.prob[category][word] = (float(count + 1)/ denominator)
        print ("DONE TRAINING\n\n")


    def train(self, trainingdir, category):

        currentdir = trainingdir + category
        files = os.listdir(currentdir)
        token_res = []
        for file in files:
            with codecs.open(currentdir + '/' + file, 'r', 'iso8859-1') as f:
                lines = f.readlines()
                tokens = [token.strip('\'".,?:-').lower() for line in lines\
                          for token in line.split()\
                          if token.strip('\'".,?:-').lower() != ''\
                          and not token.strip('\'".,?:-').lower() in self.stopwords]
                token_res.extend(tokens)

        total  = len(token_res)
        counts = dict([[token, token_res.count(token)] for token in set(token_res)])

        for token, cnt in counts.items():
            try:
                self.vocabulary[token] += 1
            except KeyError:
                self.vocabulary[token] = 1

        return(counts, total)


    def classify(self, filename):

        with codecs.open(filename, 'r', 'iso8859-1') as f:
            lines = f.readlines()
            token_lst = [token.strip('\'".,?:-').lower()\
                         for line in lines for token in line.split()\
                         if token.strip('\'".,?:-').lower() in self.vocabulary]

        results = dict([[c, 0] for c in self.categories])
        for token in token_lst:
            for category in self.categories:
                results[category] += math.log(self.prob[category][token])
        results = [[c, results[c]] for c in sorted(results, key=results.get, reverse=True)]

        return results[0][0]


    def testCategory(self, directory, category):
        files = os.listdir(directory)
        total = 0
        correct = 0
        for file in files:
            total += 1
            result = self.classify(directory + file)
            if result == category:
                correct += 1
        return (correct, total)


    def test(self, testdir):
        """Test all files in the test directory
        that directory is organized into subdirectories
        each subdir is a classification category"""
        categories = os.listdir(testdir)
        # filter out files that are not directories
        categories = [filename for filename in categories if
                      os.path.isdir(testdir + filename)]
        correct = 0
        total = 0
        for category in categories:
            print(".", end="")
            new_dir = testdir + category + '/'
            (catCorrect, catTotal) = self.testCategory(new_dir, category)
            correct += catCorrect
            total += catTotal
        print("\n\nAccuracy is  %f%%  (%i test instances)" %
              ((float(correct) / total) * 100, total))


if __name__ == '__main__':
    import os
    curr_path = os.getcwd()
    baseDirectory = curr_path + "/20news-bydate/"
    trainingDir = baseDirectory + "20news-bydate-train/"
    testDir = baseDirectory + "20news-bydate-test/"

    stoplistfile = "/Users/raz/Downloads/20news-bydate/stopwords0.txt"
    print("Reg stoplist 0 ")
    bT = bayesText(trainingDir, baseDirectory + "stopwords0.txt")
    print("Running Test ...")
    bT.test(testDir)

    '''
    print("\n\nReg stoplist 25 ")
    bT = bayesText(trainingDir, baseDirectory + "stopwords25.txt")
    print("Running Test ...")
    bT.test(testDir)

    print("\n\nReg stoplist 174 ")
    bT = bayesText(trainingDir, baseDirectory + "stopwords174.txt")
    print("Running Test ...")
    bT.test(testDir)
    '''
