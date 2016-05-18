
# This is the code I used to retrieve tweets based on queries I mentioned in the design report

import unicodedata
import json
import tweepy
#from tweepy import OAuthHandler


auth = tweepy.OAuthHandler('1DpXmbdT3n1gTMekQ0NzBUWhJ', 'ihfeWTdSV3YNjqymWwciuqS4bcwT6JdSVWG5wwS3dabKydnS6m')
auth.set_access_token('4390387221-sPVsyBQhXkstTGyZKMnSJjUufMOTDIZ6qlmtV3Q', 'PsPlJFEPqOuQynQrlh1DZigwLwn45uFi9ddNmzSD8ih4C')

api = tweepy.API(auth)

public_tweets = api.search('holiday trip OR holiday plan',count=100) 

file = open('tweet_holidays_1.txt','w')

i=0

file.write("Below are the random sample tweets \n\n")

for tweet in public_tweets:
	i+=1
	print "#", 
	print i, 
	print " : "
	tweet = unicodedata.normalize('NFKD', tweet.text).encode('utf-8','ignore')
	print tweet
	file.write('['+str(i)+', ,')
	file.write(json.dumps(tweet))
	file.write(']')
	file.write("\n")
	
file.close()