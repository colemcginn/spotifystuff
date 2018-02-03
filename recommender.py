#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scipy.stats as scistats
import pickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

# This helpful method will print the jokes for you
def print_jokes(p, n_jokes):
    for i in range(N_clusters):
        print '\n------------------------------'
        print '     cluster ' + str(i) + '   '
        print '------------------------------'
        for j in idx[p == i][:n_jokes]:
            print jokes[j] + '\n'

data = pickle.load(open('jester_train_test.p'))
# rows are users, columns are jokes
data_test = data['data_test']
data_train = data['data_train']

# Here are the joke texts, idx is used to index in print_jokes
jokes = pickle.load(open('jokes.pck', 'rb'))
idx = np.arange(len(jokes))

# Here we compute the similarity matrix. Refer to slides
# to see how to use the calculated numbers
d_user_user = np.zeros([data_test.shape[0],data_train.shape[0]])
d_item_item = np.zeros([data_train.shape[1],data_train.shape[1]])

# These calculations take a while, so you might want to save the matrices
# and load them each time instead of computing from scratch.
for i in range(data_test.shape[0]):
	ri = data_test[i]
	for j in range(data_train.shape[0]):
		rj = data_train[j]
		# use elements for which both users have given ratings
		inds = np.logical_and(ri != 0, rj != 0)
		# some users gave the same rating to all jokes :(
		if np.std(ri[inds])==0 or np.std(rj[inds])==0:
			continue
		d_user_user[i,j] = scistats.pearsonr(ri[inds],rj[inds])[0]

for i in range(data_train.shape[1]):
	ri = data_train[:,i]
	d_item_item[i,i] = 1
	for j in range(i+1, data_train.shape[1]):
		rj = data_train[:,j]
		# consider only those users who have given ratings
		inds = np.logical_and(ri != 0, rj != 0)
		d_item_item[i,j] = scistats.pearsonr(ri[inds],rj[inds])[0]
		d_item_item[j,i] = d_item_item[i,j]

# If the rating is 0, then the user has not rated that item
# You can use this mask to select for rated or unrated jokes
d_mask = (data_test == 0)

# ------------------- user user --------------------- #
sumUU = 0
count = 0
rating = 0
prediction = 0
predictions = [[-1,-1,-1]]
predict_test = np.zeros([data_test.shape[0],data_test.shape[1]])
print "\n*******User User similarity*******"

max = 0
jokeID = 0
rmse = 0
for u in range(data_test.shape[0]):
	for column in range(len(data_test[0])):
		rating = data_test[u][column]
		if rating==0:
			for x in range(len(data_train[:,column])):
				prediction += data_train[:,column][x]*d_user_user[u][x]
				sumUU += d_user_user[u][x]
			predictions.append([u,column,prediction/sumUU])
			prediction=0
			sumUU=0
		else:
			for x in range(len(data_train[:,column])):
				prediction += data_train[:,column][x]*d_user_user[u][x]
				sumUU += d_user_user[u][x]
			predict_test[u][column] = prediction/sumUU
			prediction = 0
			sumUU = 0
	for row in predictions:
		if row[0]==u:
			if row[2] > max:
				max=row[2]
				jokeID = row[1]

	joke_rec = jokeID #Replace this with the index of your recommended joke from those jokes with **zero** ratings
	jokeID = 0
	max = 0
	print "Test instance "+str(u)+" Recommend joke: "+str(joke_rec)
sum=0
count=0
for u in range(data_test.shape[0]):
	for i in range(len(data_test[0])):
		if data_test[u][i]!=0:
			sum += (data_test[u][i]-predict_test[u][i])**2
			count+=1
rmse = (sum/count)**0.5
print "RMSE for all predictions: " + str(rmse)

# ------------------ item item ----------------------- #
print "\n*******Item Item similarity*******"
sumUU = 0
count = 0
rating = 0
prediction = 0
predictions = [[-1,-1,-1]]
jokeID = 0
max = 0
rmse = 0
predict_test = np.zeros([data_test.shape[0],data_test.shape[1]])
for u in range(data_test.shape[0]):
	for column in range(len(data_test[0])):
		rating = data_test[u][column]
		if rating==0:
			for x in range(len(data_train[0])):
				prediction += data_train[u][x]*d_item_item[column][x]
				sumUU += d_item_item[column][x]
			predictions.append([u,column,prediction/sumUU])
			prediction=0
			sumUU=0
		else:
			for x in range(len(data_train[0])):
				prediction += data_train[u][x]*d_item_item[column][x]
				sumUU += d_item_item[column][x]
			predict_test[u][column] = prediction/sumUU
			prediction=0
			sumUU=0
	for row in predictions:
		if row[0]==u:
			if row[2] > max:
				max=row[2]
				jokeID = row[1]
	joke_rec = jokeID #Replace this with the index of your recommended joke from those jokes with **zero** ratings
	jokeID = 0
	max = 0
	print "Test instance "+str(u)+" Recommend joke: "+str(joke_rec)
sum=0
count=0
for u in range(data_test.shape[0]):
	for i in range(len(data_test[0])):
		if data_test[u][i]!=0:
			sum += (data_test[u][i]-predict_test[u][i])**2
			count+=1
rmse = (sum/count)**0.5
print "RMSE for all predictions: " + str(rmse)


# ------- Clustering question  -------- #
N_clusters = 10
# ------- jokes clustering based on user votes  -------- #
print "\n*******Clustering based on user votes*******"

####################################
# put your code here
####################################
# Here you should apply KMeans clustering to the ratings in the
# *TRAINING DATA* <--- very important!
# You should *not* use the test data for this question at all.
# Replace jokes_cluster with the output of your clustering.
# Below is a random clustering that ignores the joke text
# so the code still works.
####################################
jokes_cluster = np.random.randint(low=N_clusters,size=data_train.shape[1])
print_jokes(jokes_cluster, 3)
print jokes_cluster

# ------ jokes clustering based on text similariy ------#
print "\n*******Clustering based on text similarity*******"
# Use the following vectorizer to turn the text of the jokes
# into vectors that can be clustered
vectorizer = CountVectorizer(stop_words='english',
							max_df=0.95,
                            min_df=0.05,
                        	analyzer='char',
                            ngram_range = [2,5], binary=True)
####################################
# put your code here
####################################
# Here you should apply the vectorizer to the text of the jokes
# and then use the vector representation as input to KMeans clustering.
# Replace jokes_cluster with the output of your clustering.
# Below is a random clustering that ignores the joke text
# so the code still works.
jokes_cluster = np.random.randint(low=N_clusters,size=data_train.shape[1])
print_jokes(jokes_cluster, 3)
print jokes_cluster