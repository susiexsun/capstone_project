import numpy as np
from pymongo import MongoClient
from collections import OrderedDict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import cPickle as pickle

class Model1(object): 
	def __init__(self): 
		self.user_list = None
		self.tweet_list = None
		self.vect = None
		self.word_counts = None

	def create_conn_and_database(self): 
		''' Connects to MongoDB database and pulls data for model. 
		This only needs to be run once per model.'''

		client = MongoClient()
		twitter = client['twitter']
		new = twitter['new']
		text_and_id = new.find({}, {'user.id':1, 'user.screen_name':1, 'text':1, '_id':0})


		processed_data = client['processed_data']
		graph_model = processed_data['graph_model']
		graph_model.insert(text_and_id)


	def run_model(self):
		''' Turns data into a usable format for the TfidfVectorizer 
		
		INPUT: MongoDB data with 1 Mongo Document per tweet
		
		OUTPUT: Updates self.dict with OrderedDict. OrderedDict has 1 
		key per person, and the text is 1 long string with all of the tweets.
		'''

		client = MongoClient()
		processed_data = client['processed_data']
		graph_model = processed_data['graph_model']

		docs = graph_model.find({})
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
	model = Model1()
	model.create_conn_and_database()
	model.run_model()
	with open('data/retweet_user_list.pkl', 'w') as f: 
		pickle.dump(model.user_list, f)
	with open('data/retweet_tweet_list.pkl', 'w') as f: 
		pickle.dump(model.tweet_list, f)
	with open('data/retweet_vectorizer.pkl', 'w') as f: 
		pickle.dump(model.vect, f)
	with open('data/retweet_word_counts.pkl', 'w') as f: 
		pickle.dump(model.word_counts, f)
	