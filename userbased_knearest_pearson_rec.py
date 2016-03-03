#!/usr/bin/env python
# -*- coding:utf-8 -*-

import codecs
from math import sqrt


class recommender():

    def __init__(self, k=2, metric='pearson', n=5):

        self.k = k
        self.n = n
        self.username2id = {}
        self.userid2name = {}
        self.productid2name = {}
        self.data = {}
        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson


    def loadBookDB(self, path=''):

        # user, book, rating
        f = codecs.open(path + "BX-Book-Ratings.csv", 'r', 'utf8')
        for line in f:
            fields = line.split(';')
            user = fields[0].strip('"')
            book = fields[1].strip('"')
            rating = int(fields[2].strip().strip('"'))
            try:
                self.data[user][book] = rating
            except KeyError:
                self.data[user] = {}
                self.data[user][book] = rating
        f.close()

        # Books contains isbn, title, and author among other fields
        f = codecs.open(path + "BX-Books.csv", 'r', 'utf8')
        for line in f:
            fields = line.split(';')
            isbn = fields[0].strip('"')
            title = fields[1].strip('"')
            author = fields[2].strip().strip('"')
            title = title + ' by ' + author
            self.productid2name[isbn] = title
        f.close()

        f = codecs.open(path + "BX-Users.csv", 'r', 'utf8')
        for line in f:
            fields = line.split(';')
            userid = fields[0].strip('"')
            location = fields[1].strip('"')
            if len(fields) > 3:
                age = fields[2].strip().strip('"')
            else:
                age = 'NULL'
            if age != 'NULL':
                value = location + '  (age: ' + age + ')'
            else:
                value = location
            self.userid2name[userid] = value
            self.username2id[location] = userid
        f.close()


    def convertProductID2name(self, id):

        return self.productid2name[id] if id in self.productid2name else id


    def pearson(self, rating1, rating2):

        commonItems = set(rating1.keys()) & set(rating2.keys())
        n = len(commonItems)

        if n == 0:
            return 0

        x, y = rating1, rating2
        sum_x = sum([x[i] for i in commonItems])
        sum_y = sum([y[i] for i in commonItems])
        sum_x2 = sum([pow(x[i], 2) for i in commonItems])
        sum_y2 = sum([pow(y[i], 2) for i in commonItems])
        sum_xy = sum([x[i] * y[i] for i in commonItems])

        denominator = (sqrt(sum_x2 - pow(sum_x, 2) / n) *
                       sqrt(sum_y2 - pow(sum_y, 2) / n))
        numerator = sum_xy - (sum_x * sum_y) / n

        return numerator / denominator if denominator != 0 else 0


    def computeNearestNeighbor(self, username):

        distances = [[x, self.fn(self.data[username], self.data[x])]
                     for x in self.data if x != username]

        distances.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        return distances


    def recommend(self, user):

        recommendations = {}

        userRatings = self.data[user]
        nearest = self.computeNearestNeighbor(user)
        totalDistance = sum([nearest[i][1] for i in range(self.k)])

        if totalDistance == 0:
            return []

        for i in range(self.k):
            weight = nearest[i][1] / totalDistance
            name = nearest[i][0]
            neighborRatings = self.data[name]
            notRatings = set(neighborRatings.keys()) - set(userRatings.keys())
            for artist in notRatings:
                add_item = neighborRatings[artist] * weight
                try:
                    recommendations[artist] += add_item
                except KeyError:
                    recommendations[artist] = add_item

        recommendations = list(recommendations.items())
        recommendations = [(self.convertProductID2name(k), v)
                          for (k, v) in recommendations]

        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse = True)

        return recommendations[:self.n]


if __name__ == '__main__':
    r = recommender()
    path='/home/ubuntu14/jeffGithub/machine_learning/BX-Dump/'
    r.loadBookDB(path)
    #print r.recommend('230650')
    print r.recommend('276747')
