import numpy as np
from pymongo import MongoClient
from collections import OrderedDict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import cPickle as pickle

class Tweetdoc(object): 
	def __init__(self): 
		self.vect = None
		self.word_counts = None
		self.tweet_list = None
		self.user_list = None

	def create_conn_and_database(self): 
		''' Connects to MongoDB database and pulls data for model. 
		This only needs to be run once per model.'''

		client = MongoClient()
		twitter = client['twitter']
		tweets = twitter['users']
		text_and_id = tweets.find({}, {'user.screen_name':1, 'text':1})


		processed_data = client['processed_data']
		tweetdoc = processed_data['tweetdoc']
		tweetdoc.insert(text_and_id)


	# def data_to_docs(self):
	# 	''' Turns data into a usable format for the TfidfVectorizer 
		
	# 	INPUT: MongoDB data with 1 Mongo Document per tweet
	# 	OUTPUT: Updates self.dict with OrderedDict in useable format
	# 	'''

	# 	client = MongoClient()
	# 	processed_data = client['processed_data']
	# 	tweetdoc = processed_data['tweetdoc']

	# 	docs = tweetdoc.find({})
	# 	doc_dict = OrderedDict()

	# 	for doc in docs:
	# 		tweet = doc.get('text').encode('utf8', 'ignore')
	# 		user = doc.get('user').get('screen_name')
	# 		if user in doc_dict: 
	# 			doc_dict[user] += tweet
	# 		else: 
	# 			doc_dict[user] = tweet

	# 	self.dict = doc_dict


	def tfidf(self): 
		client = MongoClient()
		processed_data = client['processed_data']
		tweetdoc = processed_data['tweetdoc']

		docs = tweetdoc.find({})
		
		tweet_list = []
		user_list = []

		for doc in docs: 
			tweet = doc.get('text').encode('utf8', 'ignore')
			user = doc.get('user').get('screen_name')
			tweet_list.append(tweet)
			user_list.append(user)
			

		vect = TfidfVectorizer()
		word_counts = vect.fit_transform(tweet_list)


		self.vect = vect
		self.word_counts = word_counts
		self.tweet_list = tweet_list
		self.user_list= user_list


if __name__ == '__main__':
	model = Tweetdoc()
	#model.create_conn_and_database()
	model.tfidf()
	with open('data/tweetdoc_user_list.pkl', 'w') as f: 
		pickle.dump(model.user_list, f)
	with open('data/tweetdoc_vectorizer.pkl', 'w') as f: 
		pickle.dump(model.vect, f)
	with open('data/tweetdoc_word_counts.pkl', 'w') as f: 
		pickle.dump(model.word_counts, f)
	