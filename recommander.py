# Code file for the book Programmer's Guide to Data Mining
# http://guidetodatamining.com
# Ron Zacharski
# Modified by Jeffrey

import codecs
from math import sqrt


class recommender(object):

    def __init__(self, k=1, metric='pearson', n=5):
        """ initialize recommender
        currently, if data is dictionary the recommender is initialized to it.
        For all other data types of data, no initialization occurs
        k is the k value for k nearest neighbor
        metric is which distance formula to use
        n is the maximum number of recommendations to make"""
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
        """loads the BX book dataset. Path is where the BX files are located"""

        # First load book ratings into self.data
        # user, book, rating
        f = codecs.open(path + "BX-Book-Ratings.csv", 'r', 'utf8')
        for line in f:
            # separate line into fields
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

        # Now load books into self.productid2name
        # Books contains isbn, title, and author among other fields
        f = codecs.open(path + "BX-Books.csv", 'r', 'utf8')
        for line in f:
            #separate line into fields
            fields = line.split(';')
            isbn = fields[0].strip('"')
            title = fields[1].strip('"')
            author = fields[2].strip().strip('"')
            title = title + ' by ' + author
            self.productid2name[isbn] = title
        f.close()

        #  Now load user info into both self.userid2name and
        #  self.username2id
        f = codecs.open(path + "BX-Users.csv", 'r', 'utf8')
        for line in f:
            #print(line)
            #separate line into fields
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
        """Given product id number return product name"""
        return self.productid2name[id] if id in self.productid2name else id


    def pearson(self, rating1, rating2):

        sum_xy, sum_x, sum_y, sum_x2, sum_y2 = [0] * 5
        n = 0
        for key in rating1:
            if key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            return 0
        # now compute denominator
        denominator = (sqrt(sum_x2 - pow(sum_x, 2) / n)
                       * sqrt(sum_y2 - pow(sum_y, 2) / n))
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator


    def computeNearestNeighbor(self, username):
        """creates a sorted list of users based on their distance to username"""
        distances = [[x, self.fn(self.data[username], self.data[x])]
                     for x in self.data if x != username]
        # sort based on distance -- closest first
        distances.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        return distances


    def recommend(self, user):
       """Give list of recommendations"""
       recommendations = {}
       # first get list of users ordered by nearness
       nearest = self.computeNearestNeighbor(user)
       # now get the ratings for the user
       userRatings = self.data[user]
       # determine the total distance
       #totalDistance = sum([nearest[i][1] for i in range(self.k)])
       totalDistance = 0
       for i in range(self.k):
           totalDistance += nearest[i][1]
       # now iterate through the k nearest neighbors
       # accumulating their ratings
       for i in range(self.k):
          # compute slice of pie 
          weight = nearest[i][1] / totalDistance
          # get the name of the person
          name = nearest[i][0]
          # get the ratings for this person
          neighborRatings = self.data[name]
          # get the name of the person
          # now find bands neighbor rated that user didn't
          for artist in neighborRatings:
             if not artist in userRatings:
                if artist not in recommendations:
                   recommendations[artist] = (neighborRatings[artist]
                                              * weight)
                else:
                   recommendations[artist] = (recommendations[artist]
                                              + neighborRatings[artist]
                                              * weight)
       # now make list from dictionary
       recommendations = list(recommendations.items())
       recommendations = [(self.convertProductID2name(k), v)
                          for (k, v) in recommendations]
       # finally sort and return
       recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse = True)
       # Return the first n items
       return recommendations[:self.n]


if __name__ == '__main__':
    recommender = recommender()
    path='/home/ubuntu14/jeffGithub/learnpython/learnDataMining/chapter2/chapter2_data/BX-Dump/'
    recommender.loadBookDB(path)
    print recommender.recommend('230650')
    #print recommender.recommend('276747')
