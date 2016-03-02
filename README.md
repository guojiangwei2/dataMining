# machine_learning
learning classical machine learning methods with python

### recommand system
* nearest neighbor recommandation
* k-nearest neighbors recommandation
* some way to measure distances: manhattan distance, euclidean distance, pearson
* user-based recommandation has this 2 shortness: scalability, sparsity
* item-based(model-based) filtering:
 * cosine similarity to compute the item's distance and then compute each other item's predict score
 * item-based filtering is a way to use all information that users give to item i and others to predict i
 * slop one: compute deviations between pair of items and then use deviations to make perdictions
 * slop one is a way to simulate every items' ratings and weight slop one is to get a predictions that
 * will maximize keep the system's stability (every pair items has the similarity distances)
