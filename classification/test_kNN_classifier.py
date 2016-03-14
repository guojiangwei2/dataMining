#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
sys.path.append('/home/ubuntu14/jeffGithub/machine_learning/classification/')
from kNN_classifier import Classifier


def tenfold(bucketPrefix, dataFormat, k):
    results = {}
    for i in range(1, 11):
        c = Classifier(bucketPrefix, i, dataFormat, k)
        t = c.testBucket()
        for (key, value) in t.items():
            results.setdefault(key, {})
            for (ckey, cvalue) in value.items():
                results[key].setdefault(ckey, 0)
                results[key][ckey] += cvalue

    categories = list(results.keys())
    categories.sort()
    print("\n       Classified as: ")
    header = "        "
    subheader = "      +"
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
    print("SMALL DATA SET")
    tenfold("pimaSmall/pimaSmall",
            "num,num,num,num,num,num,num,num,class", 3)

    #print("\n\nLARGE DATA SET")
    #tenfold("pima/pima",
    #    "num    num num num num num num num class", 3)
