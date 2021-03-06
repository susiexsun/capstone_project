from sklearn.metrics.pairwise import linear_kernel
import tweepy
from tweepy import OAuthHandler
import cPickle as pickle
from tweetdoc_model import Tweetdoc
import pymongo
import sys
import numpy as np
from collections import Counter

def scrape_info(sn): 

	consumer_key = "HXJfoPTVxH6Iqqzv4nY5SlYgO"
	consumer_secret = "7LfAfz2a0LmH4dH46X4mUXSH6RTVmiS9zE1kgcBkw5NPirEkJ1"
	access_token = "34633790-ENRADvdaiEsSEhudIrNRQrxZPrPcb4hMLPupf5seb"
	access_token_secret = "hCKKwx5FyzpspWvnVr1wv4sU7JHlUNwVdJPPFrcL34wT3"

	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
	
	try: 
		user_tweets = api.user_timeline(sn, count=50)
	except: 
		print sys.exc_info()


	return user_tweets

def process(raw_data):
	data = []

	for tweet in raw_data:
		tweet_text = tweet.get('text').encode('utf8', 'ignore')
		data.append(tweet_text)

	return data

def predict(data, vect, user_list, word_counts, sn): 
	vector = vect.transform(data)
	result_matrix = linear_kernel(vector, word_counts)
	
	tweet_list = []

	# For each tweet by the client, find the 30 most similar tweets
	# This list may include tweets by the client
	for row in result_matrix: 
		indices = row.argsort()[-51:-1][::-1]
		tweet_list.append(indices)

	# Find the 50 tweets that showed up the most number of times in the tweet list
	# Now you have a list of the tweets that showed up the most number of times as 
	# being similar to your other tweets
	tweet_indexes = Counter([idx for sublist in tweet_list for idx in sublist])

	print tweet_indexes.most_common(50)

	top_indexes = [tup[0] for tup in tweet_indexes.most_common(50)]

	#find the users that wrote the tweets 
	user_array = np.array(user_list)

	people = user_array[top_indexes]

	print people

	# remove for duplicate people
	unique_people = set(people)

	print unique_people

	return [x for x in unique_people if x != sn]

if __name__ == '__main__':
	sn = raw_input("Please enter a twitter handle: ")
	raw_data = scrape_info(sn)
	data = process(raw_data)
	with open('data/tweetdoc_user_list.pkl') as f: 
		user_list = pickle.load(f)
	with open('data/tweetdoc_vectorizer.pkl') as f: 
		vect = pickle.load(f)
	with open('data/tweetdoc_word_counts.pkl') as f: 
		word_counts = pickle.load(f)
	output = predict(data, vect, user_list, word_counts, sn)
	print output
	