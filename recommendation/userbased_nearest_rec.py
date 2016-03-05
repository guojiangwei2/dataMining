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
                 "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0,
                      "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        }


def computeDistance(rating1, rating2, r=2):
    # r=1: manhattan distance, r=2: euclidean distance
    distance = 0
    commonItems = set(rating1.keys()) & set(rating2.keys())
    for item in commonItems:
        distance += pow(abs(rating1[item] - rating2[item]), r)
    return pow(distance, 1.0 / r) if commonItems else 0


def computeNearestNeighbor(username, users):

    distances = [[computeDistance(users[x], users[username], r=3), x]\
        for x in users if x != username]
    distances.sort()
    return distances


def recommend(username, users):

    recommendations = []

    nearest = computeNearestNeighbor(username, users)[0][1]
    neighborRatings = users[nearest]
    userRatings = users[username]
    recommendations = [[x, neighborRatings[x]] for x in neighborRatings if x not in userRatings]

    return sorted(recommendations, key=lambda artistTuple: artistTuple[1], reverse=True)


if __name__ == '__main__':
    print(recommend('Hailey', users))
