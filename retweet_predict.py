from sklearn.metrics.pairwise import linear_kernel
import tweepy
from pymongo import MongoClient
import sys
import numpy as np
from collections import Counter
import tweepy
from tweepy import OAuthHandler

def get_data(sn): 

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

	data = []

	for tweet in user_tweets:
		tweet_text = tweet.get('text').encode('utf8', 'ignore')
		data.append(tweet_text)

	return data


def predict(data, vect, user_list, tweet_list, word_counts): 
	vector = vect.transform(data)
	result_matrix = linear_kernel(vector, word_counts)
	
	indices_of_tweets = []

	# For each tweet by the client, find the 30 most similar tweets
	# This list may include tweets by the client
	for row in result_matrix: 
		indices = row.argsort()[:][::-1]
		indices_of_tweets.append(indices[2:51])


	# Return the person that tweeted each of the 50 most similar tweets
	user_array = np.array(user_list)
	persons_per_tweet = []

	for row in indices_of_tweets: 
		persons_per_tweet.append(user_array[row])

	# Count up how many times each person shows up. 
	# Same weighting is given to people who have many tweets similar to one client tweet
	# and a tweet that matches a high number of client tweets.
	persons_counter = Counter()

	for row in persons_per_tweet: 
		persons_counter.update(row)

	# return the top 25 people in this list
	top_people_and_count = persons_counter.most_common(25)

	top_people = [tup[0] for tup in top_people_and_count]

	return top_people

if __name__ == '__main__':
	raw_data = get_data(sn)
	with open('data/retweet_user_list.pkl') as f: 
		user_list = pickle.load(f)
	with open('data/retweet_tweet_list.pkl') as f: 
		tweet_list = pickle.load(f)
	with open('data/retweet_vectorizer.pkl') as f: 
		vect = pickle.load(f)
	with open('data/retweet_word_counts.pkl') as f: 
		word_counts = pickle.load(f)
	output = predict(data, vect, user_list, tweet_list, word_counts)
	print output