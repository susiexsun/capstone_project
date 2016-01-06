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
		self.matrix = None

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
		OUTPUT: Updates self.dict with OrderedDict in useable format
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
				doc_dict[user] += tweet
			else: 
				doc_dict[user] = tweet

		self.dict = doc_dict


	def tfidf(self): 
		matrix = []

		for k, v in self.dict.iteritems(): 
			matrix.append(v)

		vect = TfidfVectorizer(ngram_range=(1, 2), max_features=10000)
		word_counts = vect.fit_transform(np.array(matrix))

		self.matrix = matrix
		self.vect = vect
		self.word_counts = word_counts


if __name__ == '__main__':
	model = Model1()
	#model.create_conn_and_database()
	model.data_to_docs()
	model.tfidf()
	with open('data/ngrams_data_dict.pkl', 'w') as f: 
		pickle.dump(model.dict, f)
	with open('data/ngrams_vectorizer.pkl', 'w') as f: 
		pickle.dump(model.vect, f)
	with open('data/ngrams_word_counts.pkl', 'w') as f: 
		pickle.dump(model.word_counts, f)
	