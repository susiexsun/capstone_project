import numpy as np
from pymongo import MongoClient
from collections import OrderedDict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import cPickle as pickle

class Model1(object): 
	def __init__(self): 
		self.dict = None
		self.vect = None
		self.word_counts = None
		self.list_of_tweets = None

	def create_conn_and_database(self): 
		''' Connects to MongoDB database and pulls data for model. 
		This only needs to be run once per model.'''

		client = MongoClient()
		twitter = client['twitter']
		tweets = twitter['users']
		text_and_id = tweets.find({}, {'user.id':1, 'user.screen_name':1, 'text':1, '_id':0})


		processed_data = client['processed_data']
		tfidf = processed_data['tfidf']
		tfidf.insert(text_and_id)


	def data_to_docs(self):
		''' Turns data into a usable format for the TfidfVectorizer 
		
		INPUT: MongoDB data with 1 Mongo Document per tweet
		
		OUTPUT: Updates self.dict with OrderedDict. OrderedDict has 1 
		key per person, and the text is 1 long string with all of the tweets.
		'''

		client = MongoClient()
		processed_data = client['processed_data']
		count_vect = processed_data['count_vect']

		docs = count_vect.find({})
		doc_dict = OrderedDict()

		for doc in docs:
			tweet = doc.get('text').encode('utf8', 'ignore')
			user = doc.get('user').get('screen_name')
			if user in doc_dict: 
				doc_dict[user] += " " + tweet
			else: 
				doc_dict[user] = tweet

		print doc_dict.items()[1]

		self.dict = doc_dict


	def tfidf(self): 
		list_of_tweets = []

		for k, v in self.dict.iteritems(): 
			list_of_tweets.append(v)

		vect = TfidfVectorizer()
		word_counts = vect.fit_transform(list_of_tweets)

		self.list_of_tweets = list_of_tweets
		self.vect = vect
		self.word_counts = word_counts

		print word_counts[1]


if __name__ == '__main__':
	model = Model1()
	#model.create_conn_and_database()
	model.data_to_docs()
	model.tfidf()
	# with open('data/ngrams_data_dict.pkl', 'w') as f: 
	# 	pickle.dump(model.dict, f)
	# with open('data/ngrams_vectorizer.pkl', 'w') as f: 
	# 	pickle.dump(model.vect, f)
	# with open('data/ngrams_word_counts.pkl', 'w') as f: 
	# 	pickle.dump(model.word_counts, f)
	