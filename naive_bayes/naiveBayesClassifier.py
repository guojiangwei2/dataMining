#!/usr/bin/env python
# -*- coding:utf-8 -*-


class Classifier:

    def __init__(self, bucketPrefix, testBucketNumber, dataFormat):
        self.prior = {}
        self.conditional = {}
        self.format = dataFormat.strip().split(',')

        total = 0
        classes = {}
        counts = {}
        for i in range(1, 11):
            if i != testBucketNumber:
                filename = "%s-%02i" % (bucketPrefix, i)
                with open(filename, 'r') as f:
                    lines = f.readlines()
                for line in lines:
                    fields = line.strip().split('\t')
                    ignore, vector = [], []
                    for i in range(len(fields)):
                        if self.format[i] == 'num':
                            vector.append(float(fields[i]))
                        elif self.format[i] == 'attr':
                            vector.append(fields[i])
                        elif self.format[i] == 'comment':
                            ignore.append(fields[i])
                        elif self.format[i] == 'class':
                            category = fields[i]

                    total += 1
                    try:
                        classes[category] += 1
                    except KeyError:
                        classes[category] = 1
                    counts.setdefault(category, {})
                    col = 0
                    for columnValue in vector:
                        col += 1
                        counts[category].setdefault(col, {})
                        counts[category][col].setdefault(columnValue, 0)
                        counts[category][col][columnValue] += 1

        # prior probilities
        for (category, count) in classes.items():
            self.prior[category] = 1.0 * count / total
        # conditional probabilities p(D|h)
        for (category, columns) in counts.items():
              self.conditional.setdefault(category, {})
              for (col, valueCounts) in columns.items():
                  self.conditional[category].setdefault(col, {})
                  for (attrValue, count) in valueCounts.items():
                      self.conditional[category][col][attrValue] =\
                          (1.0 * count / classes[category])


    def classify(self, itemVector):

        results = []
        for (category, prior) in self.prior.items():
            prob = prior
            col = 0
            for attrValue in itemVector:
                col += 1
                if not attrValue in self.conditional[category][col]:
                    prob = 0
                else:
                    prob = prob * self.conditional[category][col][attrValue]
            results.append((prob, category))
        return max(results)[1]


    def testBucket(self, bucketPrefix, bucketNumber):

        filename = "%s-%02i" % (bucketPrefix, bucketNumber)
        with open(filename, 'r') as f:
            lines = f.readlines()
        loc = 1
        totals = {}
        for line in lines:
            loc += 1
            data = line.strip().split('\t')
            vector = []
            classInColumn = -1
            for i in range(len(self.format)):
                if self.format[i] == 'num':
                    vector.append(float(data[i]))
                elif self.format[i] == 'attr':
                    vector.append(data[i])
                elif self.format[i] == 'class':
                    classInColumn = i
            theRealClass = data[classInColumn]
            classifiedAs = self.classify(vector)
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


if __name__ == '__main__':
    house_format = 'class,' + ','.join(['attr'] * 16)
    tenfold('house-votes/hv', house_format)
    #c = Classifier("iHealth/i", 10, "attr,attr,attr,attr,class")
    #print(c.classify(['health', 'moderate', 'moderate', 'yes']))
