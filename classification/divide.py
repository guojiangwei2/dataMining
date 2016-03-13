#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import json


def buckets(filename, bucketName, separator, classColumn):

    data = {}
    with open(filename, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if separator != '\t':
            line = line.replace(separator, '\t')
        category = line.split()[classColumn]
        try:
            data[category].append(line)
        except KeyError:
            data[category] = [line, ]

    numberOfBuckets = 10
    buckets = [[]] * numberOfBuckets
    for k in data.keys():
        random.shuffle(data[k])
        bNum = 0
        for item in data[k]:
            buckets[bNum].append(item)
            bNum = (bNum + 1) % numberOfBuckets

    for bNum in range(numberOfBuckets):
        with open('%s-%02d' % (bucketName, bNum + 1), 'wb') as f:
            json.dump(bucketes[bNum], f)


if __name__ == '__main__':
    buckets("pimaSmall.txt", 'pimaSmall','\t',8)
