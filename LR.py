from sklearn.linear_model import LogisticRegression
from sklearn import svm
import pylab as pl
import numpy as np
import scipy as sp
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV
import json
import unicodedata

stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

tweets = []
for line in open('training_tweets.txt').readlines():
	tweets.append(json.loads(line))

# Extract the vocabulary of keywords
vocab = dict()
for id, class_label, text in tweets:
	for term in text.split():
		term = term.lower()
		term = "".join(c for c in term if c not in ('!','.',':','#',"'",","))
		if len(term) > 2 and term not in stopwords:
		#if len(term) > 2:
			if vocab.has_key(term):
				vocab[term] = vocab[term] + 1
			else:
				vocab[term] = 1

# Remove terms whose frequencies are less than a threshold (e.g., 20)
vocab = {term: freq for term, freq in vocab.items() if freq > 20}
# Generate an id (starting from 0) for each term in vocab
vocab = {term: idx for idx, (term, freq) in enumerate(vocab.items())}
print 'The list of keywords that are considered: '
print vocab

# Generate X and y
X = []
y = []
for tweet_id, class_label, tweet_text in tweets:
	x = [0] * len(vocab)
	terms = [term for term in tweet_text.split() if len(term) > 2]
	for term in terms:
		term = "".join(c for c in term if c not in ('!','.',':','#',"'",","))
		if vocab.has_key(term):
			x[vocab[term]] += 1
	y.append(class_label)
	X.append(x)

# 10 folder cross validation to estimate the best w and b
clf = LogisticRegression()
clf.fit(X, y)

# predict the class labels of new tweets
tweets = []
for line in open('testing_tweets.txt').readlines():
	tweets.append(json.loads(line))

# Generate X for testing tweets
X = []
class_labels = []
for tweet_id, class_label, tweet_text in tweets:
	x = [0] * len(vocab)
	terms = [term for term in tweet_text.split() if len(term) > 2]
	for term in terms:
		term = "".join(c for c in term if c not in ('!','.',':','#',"'",","))
		if vocab.has_key(term):
			x[vocab[term]] += 1
	X.append(x)
	class_labels.append(class_label)
y = clf.predict(X)
ypercent = clf.predict_proba(X)

#print len(ypercent)

#lr.predict_proba(X) will return you the predict probabilities

#print y[0]
#print class_labels[0]
#
#print ypercent
#print y

j = 0
for i in range(0,len(y)):
	if(y[i] == class_labels[i]):
		j = j + 1

print j
#print len(y)
#print j/len(y)		
#print 'The achieved accuracy is '+str(((j/len(y))*100))+'%'

fp = open('positive_predictions.txt', 'w')
fn = open('negative_predictions.txt', 'w')
fa = open('ad_predictions.txt', 'w')
X_positive_pred = []
X_negative_pred = []
X_ad_pred = []
pos_tweets = []
neg_tweets = []
ad_tweets = []
for idx, [tweet_id, class_label, tweet_text] in enumerate(tweets):
	if(y[idx] == 0):
		fn.write(json.dumps([tweet_text, y[idx], str(max(ypercent[idx])*100)+'%']) + '\r\n')
		X_negative_pred.append(X[idx])
		neg_tweets.append(tweet_text)
	elif(y[idx] == 1):
		fp.write(json.dumps([tweet_text, y[idx], str(max(ypercent[idx])*100)+'%']) + '\r\n')
		X_positive_pred.append(X[idx])
		pos_tweets.append(tweet_text)
	else:
		fa.write(json.dumps([tweet_text, y[idx], str(max(ypercent[idx])*100)+'%']) + '\r\n')
		X_ad_pred.append(X[idx])
		ad_tweets.append(tweet_text)
fp.close()
fn.close()
fa.close()

#print len(pos_tweets)
#print len(X_positive_pred)

fr = open('recommendations.txt','w')
for k in range(0, len(X_positive_pred)):
	rec_tweets = []
	for i in range(0, len(X_ad_pred)):
		pearson = sp.stats.pearsonr(X_positive_pred[k], X_ad_pred[i])
		if(pearson[0] > 0.4):
			rec_tweets.append(ad_tweets[i])
	fr.write("Tweet :"+str(unicodedata.normalize('NFKD', pos_tweets[k]).encode('utf-8','ignore'))+"\n")
	fr.write("Recommended ads"+"\n")
	fr.write(json.dumps(rec_tweets))
	fr.write("\n")
	fr.write("\n")
	
fr.close()

print '\r\nAmong the total {1} tweets, {0} tweets are predicted as positive.'.format(sum(y==1), len(y))
print '\r\nAmong the total {1} tweets, {0} tweets are predicted as negative.'.format(sum(y==0), len(y))
print '\r\nAmong the total {1} tweets, {0} tweets are predicted as advertisements.'.format(sum(y==2), len(y))
