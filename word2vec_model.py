from gensim import corpora, models, similarities
import numpy as np
import tweepy
from tweepy import OAuthHandler
from pymongo import MongoClient
from collections import OrderedDict, defaultdict


# the corpus should be represented as a dictionary? 
# input questions into word2vec as a list of tokenized words ['graph', 'minors', 'trees']

class Word2Vec_Model(object): 
	def __init__(self): 
		self.dict = None
		self.list_of_tweets = None
		self.input = None
		self.corpus = None
		self.dictionary = None
		self.result = None

	def scrape_target(self, sn): 
		""" 
		INPUT: The screen name of the target person.
		OUTPUT: A list of tweets 

		"""

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
				data.extend(tweet_text.lower().split())

		self.input = data
		return data

	def process_data_for_corpus(self):
			''' Creates a corpus
			
			INPUT: MongoDB data with 1 Mongo Document per tweet
			
			OUTPUT: Updates self.dict with OrderedDict. Updates 
			self.list_of_tweets with tweets
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

			self.dict = doc_dict

			list_of_tweets = []
			for v in self.dict.values(): 
				list_of_tweets.append(v.lower().split())

			self.list_of_tweets = list_of_tweets


	def create_corpus(self): 

			dictionary = corpora.Dictionary(self.list_of_tweets)
			self.dictionary = dictionary
			corpus = [dictionary.doc2bow(text) for text in self.list_of_tweets]

			self.corpus = corpus

			return corpus

	def transform_tfidf(self):
		tfidf = models.TfidfModel(self.corpus)
		corpus_tfidf = tfidf[self.corpus]

		return corpus_tfidf

	def run_model(self):
		lsi = models.LsiModel(self.corpus)
		dictionary=self.dictionary
		doc = self.input
		vec_bow = dictionary.doc2bow(doc)
		vec_lsi = lsi[vec_bow]

		self.result = vec_lsi

		return vec_lsi

	def score_model(self): 
		ranked_result = sorted(self.result, key=lambda x: x[1], reverse=True)
		ranked_indices = [x[0] for x in ranked_result]

		username_array = np.array(self.dict.keys())

		output = username_array[ranked_indices]	

		return output[:10]



if __name__ == '__main__':
	model = Word2Vec_Model()
	data = model.scrape_target('susiexsun')
	#model.create_conn_and_database()
	dictionary = model.process_data_for_corpus()
	corpus = model.create_corpus()
	vec_lsi = model.run_model()
	output = model.score_model()
	print output
