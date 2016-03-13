# Machine Learning
* a study not of A Programmer's Guide to Data Mining
* the original lectures, data and python codes is avaliable in `http://guidetodatamining.com/`
* the github website: `https://github.com/zacharski/pg2dm-python`

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
* Naïve Bayes and Probability Density Functions
 * eager learners(try to build a internal model) VS. lazy learners(just remember and goes through the entire traning data set)
  * give both probabilistic prediction
  * more faster than nearest classification
 * prior probility VS. posteriod probility(conditional probility), p(h|D) = p(D|h) * p(h) / p(D)
 * compute probility of each hypothesis and select the hypothesis with maximum probility. maximum posteroiri hypethesis
 * hMAP = argmax(p(h|D)) = argmax(p(D|h) * p(h) / p(D)) = argmax(p(D|h) * p(h))
 * estimating of probilities: p(x|y) = p(x & y) / p(y)
  * p(x|y) is the estimates of the true probility, so if the true value is very small, sometimes the estimates will be 0
  * the adjust value may be p(x|y) = nc / n ≈ (nc + m * p) / (n + m), where n is the num of sample, nc is the num of target sample, m is a constant called equivalant of sample size, for example as num of the attribute value, p the prior estimate of probility. there are many methods to determine the m, and often we suppose uniform distrubution of the prior probolity.
 * numberical data
  * making categories
  * Gaussian distrubition and probability density function(mean and sample standard diviation)
 * navie means that the events the probilities represent is independend, and we can multiple the probilities together for the joint probilities. we just naviely assuming indenpendence even though we know it is not.
 * advantages and disadvantages
  * navie bayes needs less training data set, simple to implement and has a good performance
  * disadvantage is that navie bayes can't learn interactions between features
  * comparable, kNN is simple to implement, doesn't assumpe any particular structure of the data
  * disadvantage of kNN is that it needs more trainning data sets and more memory to store the data and poor compute performance
  * kNN is extremely versatile and used in large fields such as recommendation systems, proteomics and image classification, it's a good choice if have large training data sets
