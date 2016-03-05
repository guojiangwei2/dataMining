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
