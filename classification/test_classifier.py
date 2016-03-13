#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
sys.path.append('/home/ubuntu14/jeffGithub/machine_learning/classification/')

from nearest_neighbor_classifier import Classifier


def test(training_filename, test_filename):

    classifier = Classifier(training_filename, r=2)
    #classifier = Classifier(training_filename, fn='normalize', r=2)
    #classifier = Classifier(training_filename, fn='range', r=2)

    with open(test_filename, 'r') as f:
        lines = f.readlines()
    numCorrect = 0.0
    for line in lines:
        data = line.strip().split()
        vector = []
        classInColumn = -1
        for i in range(len(classifier.format)):
              if classifier.format[i] == 'num':
                  vector.append(float(data[i]))
              elif classifier.format[i] == 'class':
                  classInColumn = i
        theClass= classifier.classify(vector)
        prefix = '-'
        if theClass == data[classInColumn]:
            numCorrect += 1
            prefix = '+'
        print("%s  %12s  %s" % (prefix, theClass, line))

    print("%4.2f%% correct" % (numCorrect * 100/ len(lines)))


if __name__ == '__main__':
    #test('athletesTrainingSet.data', 'athletesTestSet.data')
    #test("irisTrainingSet.data", "irisTestSet.data")
    test("mpgTrainingSet.data", "mpgTestSet.data")
