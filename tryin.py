import time
import tweepy
from tweepy import OAuthHandler
from pymongo import MongoClient
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

# Access Twitter API
consumer_key = "HXJfoPTVxH6Iqqzv4nY5SlYgO"
consumer_secret = "7LfAfz2a0LmH4dH46X4mUXSH6RTVmiS9zE1kgcBkw5NPirEkJ1"
access_token = "34633790-ENRADvdaiEsSEhudIrNRQrxZPrPcb4hMLPupf5seb"
access_token_secret = "hCKKwx5FyzpspWvnVr1wv4sU7JHlUNwVdJPPFrcL34wT3"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Initialize Mongo Connection
client = MongoClient()
twitter = client['twitter']
users = twitter['users']

def get_ids(sn): 
	ids = []
	for page in tweepy.Cursor(api.followers_ids, screen_name=sn).pages():
	    try: 
	    	ids.extend(page)
	    except: 
	    	print sys.exc_info()
	return ids

def get_data(sn): 
	record = users.find_one({'user.screen_name': sn})
	a_dict = {'abc': 123}

	if type(record) != type(a_dict):
		try: 
			user_tweets = api.user_timeline(sn, count=20)
			users.insert(user_tweets)
		except: 
			print sys.exc_info()
		
		X_docs = []

		for tweet in user_tweets:
			tweet_text = tweet.text
			X_docs.append(tweet_text)
	else: 
		docs = users.find({'user.screen_name': sn})
		
		X_docs = []

		for doc in docs: 
			tweet = doc.get('text').encode('utf8', 'ignore')
			X_docs.append(tweet)

	return X_docs

def scrape_new_users(ids): 
	tweet_list = []
	user_ids = []
	user_handles = []

	for one_id in ids: 
		record = users.find_one({'user.id': one_id})
		a_dict = {'abc': 123}
		if type(record) != type(a_dict):
			try: 
				user_tweets = api.user_timeline(one_id, count=20)
				users.insert(user_tweets)
				for doc in user_tweets: 
					tweet = doc.text
					user_id = doc.user.id
					user_handle = doc.user.screen_name
					tweet_list.append(tweet)
					user_ids.append(user_id)
					user_handles.append(user_handle)
			except: 
				print sys.exc_info()
		else: 
			docs = users.find({'user.id': one_id})
			for doc in docs: 
				tweet = doc.get('text').encode('utf8', 'ignore')
				user_handle = doc.get('user').get('screen_name')
				user_id = doc.get('user').get('id')
				tweet_list.append(tweet)
				user_ids.append(user_id)
				user_handles.append(user_handle)

	return tweet_list, user_ids, user_handles

def run_model(tweet_list): 
	vect = TfidfVectorizer()
	word_counts = vect.fit_transform(tweet_list)

	return vect, word_counts

def predict(data, vect, user_handles, tweet_list, word_counts): 
	vector = vect.transform(data)
	result_matrix = linear_kernel(vector, word_counts)

	indices_of_tweets = []

	# For each tweet by the client, find the 30 most similar tweets
	# This list may include tweets by the client
	for row in result_matrix: 
		indices = row.argsort()[:][::-1]
		indices_of_tweets.append(indices[2:51])


	# Return the person that tweeted each of the 50 most similar tweets
	#user_ids_array = np.array(user_ids)
	user_handles_array = np.array(user_handles)
	ids_per_tweet = []
	handles_per_tweet = []

	for row in indices_of_tweets: 
		ids_per_tweet.append(user_ids_array[row])
		handles_per_tweet.append(user_handles_array[row])

	# Count up how many times each person shows up. 
	# Same weighting is given to people who have many tweets similar to one client tweet
	# and a tweet that matches a high number of client tweets.s
	persons_counter = Counter()

	for row in handles_per_tweet: 
		persons_counter.update(row)

	# return the top 10 people in this list
	top_people_and_count = persons_counter.most_common(10)

	top_people = [tup[0] for tup in top_people_and_count]

	return top_people


if __name__ == '__main__':
	sn = 'susiexsun'
	ids = get_ids(sn)
	X_docs = get_data(sn)
	tweet_list, user_ids, user_handles = scrape_new_users(ids)
	#vect, word_counts = run_model(tweet_list)
	#top_people = predict(data, vect, user_handles, tweet_list, word_counts)data