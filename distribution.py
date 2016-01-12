from sklearn.metrics.pairwise import linear_kernel
import tweepy
from tweepy import OAuthHandler
import cPickle as pickle
from tweetdoc_model import Tweetdoc
import pymongo
import sys
import numpy as np
from collections import Counter, defaultdict


class Analysis(object): 
	def __init__(self, user_list, tweet_list, word_counts, vect):
		self.user_raw_data = None 
		self.user_list = user_list
		self.tweet_list = tweet_list
		self.word_counts = word_counts
		self.vect = vect
		self.result_matrix = None
		self.user_tweets = None

	def scrape_info(self, sn): 

		consumer_key = "HXJfoPTVxH6Iqqzv4nY5SlYgO"
		consumer_secret = "7LfAfz2a0LmH4dH46X4mUXSH6RTVmiS9zE1kgcBkw5NPirEkJ1"
		access_token = "34633790-ENRADvdaiEsSEhudIrNRQrxZPrPcb4hMLPupf5seb"
		access_token_secret = "hCKKwx5FyzpspWvnVr1wv4sU7JHlUNwVdJPPFrcL34wT3"

		auth = OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)

		api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
		
		try: 
			raw_data = api.user_timeline(sn, count=50)
		except: 
			print sys.exc_info()


		self.user_raw_data = raw_data

	def process(self):
		user_tweets = []

		for tweet in self.user_raw_data:
			tweet_text = tweet.get('text').encode('utf8', 'ignore')
			user_tweets.append(tweet_text)

		self.user_tweets = user_tweets

	def distribution(self): 
		vector = self.vect.transform(self.user_tweets)
		result_matrix = linear_kernel(vector, self.word_counts)

		self.result_matrix = result_matrix

		# create a dictionary with a unique matrix for each person

		distribution_matrix = defaultdict(list)

		for idx, row in enumerate(result_matrix.T):
			user_name = self.user_list[idx]
			distribution_matrix[user_name] += row

		return distribution_matrix


if __name__ == '__main__':
	with open('data/tweetdoc_user_list.pkl') as f: 
		user_list = pickle.load(f)
	with open('data/tweetdoc_tweet_list.pkl') as f: 
		tweet_list = pickle.load(f)
	with open('data/tweetdoc_word_counts.pkl') as f: 
		word_counts = pickle.load(f)
	with open('data/tweetdoc_vectorizer.pkl') as f: 
		vect = pickle.load(f)
	analysis = Analysis(user_list, tweet_list, word_counts, vect)
	analysis.scrape_info('susiexsun')
	analysis.process()
	analysis.distribution()
