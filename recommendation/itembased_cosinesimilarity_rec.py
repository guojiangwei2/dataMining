#!/usr/bin/env python
# -*- coding:utf-8 -*-

from math import sqrt

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0,
                      "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0,
                 "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0,
                  "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0,
                 "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0,
                    "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0,
                     "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0,
                 "Slightly Stoopid": 4.0, "The Strokes": 5.0}
        }

new_user = {"Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0}}


class recommender():

    def __init__(self, data):

        self.data = data
        self.itemSimilarity = {}


    def computeSimilarity(self):

        self.items = set()
        user_avg = {}
        for user, ratings in self.data.items():
            user_avg[user] = float(sum(ratings.values())) / len(ratings.values())
            user_item = list(ratings.keys())
            self.items |= set(user_item)

        self.itemSimilarity = dict([[x, dict([[x, 0] for x in self.items])] for x in self.items])
        for item1 in self.items:
            for item2 in self.items:
                num, dem1, dem2 = (0, 0, 0)
                for user, ratings in self.data.items():
                    if item1 in ratings and item2 in ratings:
                        avg = user_avg[user]
                        num += (ratings[item1] - avg) * (ratings[item2] - avg)
                        dem1 += pow((ratings[item1] - avg), 2)
                        dem2 += pow((ratings[item2] - avg), 2)
                if dem1 * dem2 != 0:
                    self.itemSimilarity[item1][item2] = num / (sqrt(dem1) * sqrt(dem2))


    def predictScore(self, userRatings, item):

        similarities = self.itemSimilarity[item]
        num, dem = (0, 0)
        for item, rating in userRatings.items():
            if item in similarities:
                nr = rating * 1.0 / 2 - 1.5
                num += nr * similarities[item]
                dem += abs(similarities[item])

        return round(2 * (float(num) / dem) + 3, 1) if dem != 0 else None


    def cosineSimilarityRecommender(self, userRatings):

        recommendations = [[x, self.predictScore(userRatings, x)]
                           for x in self.items if self.predictScore(userRatings, x)]
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse = True)

        return recommendations[:5]


if __name__ == '__main__':
    r = recommender(users)
    r.computeSimilarity()
    #print r.itemSimilarity
    Veronica = new_user['Veronica']
    #print r.predictScore(Veronica, 'The Strokes')
    print r.cosineSimilarityRecommender(Veronica)
