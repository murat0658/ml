I have implemented decision tree in this homework in the Car database. 1/3 testing, 2/3 training data. I also implemented all pruning levels so that we can see if there is an overfit.
I copied the data file from remote db to my local and to the same directory as code file. This is enough to see the results. Output format is like this: 

Firstly, the time after training and calculating gain ratios is given.
The pruning level is given. If the pruning level is 1, this means that the height of decision tree is 1. This was repeated until all possible pruning levels are achieved. From height 1 to 6 is the order of output.
Time is given. The differences between given times are training (tree construction) + testing times.
Constructed tree is given. Nodes in the same level are represented with tree. Node and its children are represented with dictionary.
Accuracy of constructed decision tree against test data was given.

I implemented the code as if it shuffles dataset and takes 2/3 for training and 1/3 for testing. Then, it calculates the gain ratios. Next, random variables(=features, columns) were ordered according to their gain ratios. Afterwards, training and testing with several pruning levels were implemented.
If we first look at the decision tree with no pruning, its accuracy result was between 88% and 90%. To see if there is overfit, we apply pruning to the tree one level. Generally, the result is between 76-78%. This means we do not have overfitting. After some pruning, the accuracy does not change. The reason is that ‘unacc’ class dominates (~70%) the classes and I choose the dominating class one level up while pruning. I can take this observed stable accuracy(67-71%) as base case for that reason. Also, if we assume that data split is uniform, we can expect that base case ~70% as well. The reason is that if the ‘unacc’ is predicted for all values without any training, this gets ~70% accuracy under uniformness assumption. According to our results, our data gets (88,90) - (67-71) = 17-23 % accuracy gain after training -in the no pruning case. In addition, we can see that training and testing times increase as the time decision tree height increases. 

As a result, our decision tree without pruning do not overfit the data and gets ~90% accuracy over test data. 
