from gensim import corpora, models, similarities
import numpy as np
from pymongo import MongoClient
from collections import OrderedDict, defaultdict
import cPickle as pickle

class Model1(object): 
	def __init__(self): 
		self.handle_tweet_dict = None
		self.id_handle_dict = None
		self.dictionary = None
		self.corpus = None
		self.model = None

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
		handle_tweet_dict = defaultdict(list)
		id_handle_dict = defaultdict(list)

		for doc in docs: 
			tweet = doc.get('text').encode('utf8', 'ignore')
			user_id = doc.get('user').get('id')
			handle = doc.get('user').get('screen_name').encode('utf8', 'ignore')
			handle_tweet_dict[handle].append(tweet)
			id_handle_dict[user_id] = handle

		self.handle_tweet_dict = handle_tweet_dict
		self.id_handle_dict = id_handle_dict

		dictionary_input = [x for sublist in handle_tweet_dict.values() for x in sublist]

		# vect = TfidfVectorizer()
		# word_counts = vect.fit_transform(model_input)

		dictionary = corpora.Dictionary(dictionary_input)
		corpus = [dictionary.doc2bow(text) for text in dictionary]
		self.corpus = corpus

		lsi = models.LsiModel(corpus)
		self.model = lsi
		



if __name__ == '__main__':
	model = Model1()
	#model.create_conn_and_database()
	model.run_model()
	with open('data/retweet_word2vec_handle_tweet_dict.pkl', 'w') as f: 
		pickle.dump(model.handle_tweet_dict, f)
	with open('data/retweet_word2vec_id_handle_dict.pkl', 'w') as f: 
		pickle.dump(model.id_handle_dict, f)
	with open('data/retweet_word2vec_dictionary.pkl', 'w') as f: 
		pickle.dump(model.dictionary, f)
	with open('data/retweet_word2vec_lsi.pkl', 'w') as f: 
		pickle.dump(model.lsi, f)


	