# Machine Learning

### collabrative filting recommand system
* nearest neighbor recommandation
* k-nearest neighbors recommandation
* some way to measure distances: manhattan distance, euclidean distance, pearson(cosine similarity)
* user-based recommandation: memory based recommendation
* item-based recommandation: model based recommendation
* imformations
 * explicit ratings: lazy ratings, lie or partial imformation, lazy to update ratings
 * implicit ratings: how to recognize the peoples' behavior and build a profile of a person
 * however the implicit and explict information both values
* item-based(model-based) filtering:
 * cosine similarity to compute the item's distance and then compute each other item's predict score
 * item-based filtering is a way to use all information that users give to both item i and others to predict i
 * slop one: compute deviations between pair of items and then use deviations to make perdictions
 * slop one is a way to simulate every items' ratings and weight slop one is to get a predictions that
 * will maximize keep the system's stability (every pair items has the similarity distances)
* shortness
 * sparsity and scalability
 * tend to recommend already popular items, bias toward popularity

### item based filtering
* find the appropriate values of the items
* normalization the variables, as pay attention to scale of diff. attribute
 * (x - min) / range, give a value of 0 to 1
 * (x - e[x]) / std., this value is infulence by outlier much
 * (x - median) / asd, where abslute standard deviation is (∑|x - median| / n)
 * nomarlization is not necessary, it costs times and sometimes reduce the accuracy
* compute the nearest neighbors

### classfication
* a classifier is a program that uses an object's attribute to determine what class or group it belongs to.
 * first try to find a most nearest thing from some labeled objects;
 * predict the unlabeled one as the class of the nearest one's class
* convert the scale of the attribute with some functions
 * compare the standarization, normalization, convert with range value
 * normalize: (x - mean) / std
 * standarize: (x - median) / asd, where asd represents absolute standard deviation
 * convert with range: (x - min) / range, where range equals to (max - min)
* evaluate the classifier: train sets and test sets
 * people never test with the data they used to build the classifier: overly optimistic
 * devide the data set to training and test sets: the result depends on how we devide the data sets, especially when some types are sparse
 * 10-fold cross validation: random devide; iterate 10 times; sum up results
 * level-one-out:
  * adavntege: use the larget possible info. and deterministic
  * disadvantege: computational expense and stratification
 * two way to evaluate the classifier:
  * percent accuracy
  * confusion matrix
 * kappa value = (p(c) - p(r)) / (1 - p(r))
  * < 0: less than chance performance, 0.01-0.2: slightly good, 0.21-0.4: fair performance
  * 0.41-0.6: morderate performance, 0.61-0.8:substantially good performance, 0.81-1.0: near perfact performance
* kNN - k nearest neighbors
 * duck-like classifier, voting method
 * discrete class, avoid the misclassification influenced by the outlier
 * predict numeric value with distance-weighted value:
  * 3 closest instances, with (distance, value) as (d1, v1), (d2, v2) and (d3, v3)
  * transfrom distance as f(d) = 1 / d, weight of each value as f(di) / sum(d1, d2, d3)
  * predict value = ∑(d * weight)
* algorithms or more data
  * better algorithm may have a significant improvment of the perfomance, but more data may be more practice and more improvement
* kNN's application
 * recommending items at amazone
 * assessing cousumer credit risks
 * classifying land cover using image analysis
 * faces recognication
 * recognize the gender of people in images
 * recommending web
 * recommending vacation packages
