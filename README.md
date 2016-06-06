# Recommendation-Systems-of-Tourist-Spots-based-on-Twitter-data
The Project recommends the best relevant ads to the twitter users who express their interest in taking a memorable vacation

The training data set is placed in training_tweets.txt which contains 1000 training tweets.

The testing data set is placed in testing_tweets.txt which contains 200 testing tweets.

Two classifiers are implemented: Support Vector Machine and Logistic Regression. Logistic Regression is found to give a little more accuracy than Support Vector Machine. So, we used Logistic Regression. SVM.py contains the implementation of Support Vector Machine. LR.py contains both the implementation of both Logistic Regression and Pearson correlation similarity function.

Running the LR.py file will create the recommendations.txt file which contains the recommendations for each predicted positive tweet.

The accuracy of the built recommendation system is around 70%. The accuracy is expected to increase by adding more datasets to the training data. 
