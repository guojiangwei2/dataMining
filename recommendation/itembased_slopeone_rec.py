#!/usr/bin/env python
# -*- coding:utf-8 -*-

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
        self.frequencies = {}
        self.deviations = {}
        if type(data).__name__ == 'dict':
            self.data = data


    def computeDeviations(self):
        for ratings in self.data.values():
            for (item, rating) in ratings.items():
                self.frequencies.setdefault(item, {})
                self.deviations.setdefault(item, {})
                for (item2, rating2) in ratings.items():
                    if item != item2:
                        try:
                            self.frequencies[item][item2] += 1
                            self.deviations[item][item2] += rating - rating2
                        except KeyError:
                            self.frequencies[item][item2] = 0
                            self.deviations[item][item2] = 0.0

        for (item, ratings) in self.deviations.items():
            for item2 in ratings:
                ratings[item2] /= self.frequencies[item][item2]


    def slopeOneRecommendations(self, userRatings):
        recommendations = {}
        frequencies = {}
        # for every item and rating in the user's recommendations
        for (userItem, userRating) in userRatings.items():
            # for every item in our dataset that the user didn't rate
            for (diffItem, diffRatings) in self.deviations.items():
                if diffItem not in userRatings and userItem in self.deviations[diffItem]:
                    freq = self.frequencies[diffItem][userItem]
                    recommendations.setdefault(diffItem, 0.0)
                    frequencies.setdefault(diffItem, 0)
                    # add to the running sum representing the numerator of the formula
                    recommendations[diffItem] += (diffRatings[userItem] + userRating) * freq
                    # keep a running sum of the frequency of diffitem
                    frequencies[diffItem] += freq
        recommendations =  [(k, round(v / frequencies[k], 1)) for (k, v) in recommendations.items()]
        # finally sort and return
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse = True)
        # I am only going to return the first 5 recommendations
        return recommendations[:5]


if __name__ == '__main__':
    r = recommender(users)
    r.computeDeviations()
    Veronica = new_user['Veronica']
    print r.slopeOneRecommendations(Veronica)
