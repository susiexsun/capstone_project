import numpy as np
from pymongo import MongoClient
from collections import OrderedDict
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
import cPickle as pickle

class Model2(object): 
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
		count_vect = processed_data['count_vect']
		count_vect.insert(text_and_id)


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
				doc_dict[user] += tweet
			else: 
				doc_dict[user] = tweet

		self.dict = doc_dict


	def vectorize(self): 
		matrix = []

		for k, v in self.dict.iteritems(): 
			matrix.append(v)


		vect = CountVectorizer()
		word_counts = vect.fit_transform(np.array(matrix))

		self.matrix = matrix
		self.vect = vect
		self.word_counts = word_counts


if __name__ == '__main__':
	model2 = Model2()
	# model2.create_conn_and_database()
	model2.data_to_docs()
	model2.vectorize()
	with open('data/count_vect_data_dict.pkl', 'w') as f: 
		pickle.dump(model2.dict, f)
	with open('data/count_vectorizer.pkl', 'w') as f: 
		pickle.dump(model2.vect, f)
	with open('data/count_vect_word_counts.pkl', 'w') as f: 
		pickle.dump(model2.word_counts, f)