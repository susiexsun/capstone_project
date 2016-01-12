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

def predict(data, vect, user_list, tweet_list, word_counts, sn): 
	vector = vect.transform(data)
	result_matrix = linear_kernel(vector, word_counts)
	
	indices_of_tweets = []

	# For each tweet by the client, find the 30 most similar tweets
	# This list may include tweets by the client
	for row in result_matrix: 
		indices = row.argsort()[:][::-1]
		indices_of_tweets.append(indices[2:51])

	print indices_of_tweets

	tweet_array = np.array(tweet_list)
	tweets = tweet_array[indices_of_tweets]

	print zip(data, tweets)


	# Return the person that tweeted each of the 50 most similar tweets
	user_array = np.array(user_list)
	persons_per_tweet = []

	for row in indices_of_tweets: 
		persons_per_tweet.append(user_array[row])

	print persons_per_tweet

	# Count up how many times each person shows up. 
	# Same weighting is given to people who have many tweets similar to one client tweet
	# and a tweet that matches a high number of client tweets.
	persons_counter = Counter()

	for row in persons_per_tweet: 
		persons_counter.update(row)

	print persons_counter

	# return the top 25 people in this list
	top_people_and_count = persons_counter.most_common(25)

	print top_people_and_count

	top_people = [tup[0] for tup in top_people_and_count]

	return top_people

if __name__ == '__main__':
	sn = raw_input("Please enter a twitter handle: ")
	raw_data = scrape_info(sn)
	data = process(raw_data)
	with open('data/tweetdoc_user_list.pkl') as f: 
		user_list = pickle.load(f)
	with open('data/tweetdoc_tweet_list.pkl') as f: 
		tweet_list = pickle.load(f)
	with open('data/tweetdoc_vectorizer.pkl') as f: 
		vect = pickle.load(f)
	with open('data/tweetdoc_word_counts.pkl') as f: 
		word_counts = pickle.load(f)
	output = predict(data, vect, user_list, tweet_list, word_counts, sn)
	#print output