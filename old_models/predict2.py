from sklearn.metrics.pairwise import linear_kernel
import tweepy
from tweepy import OAuthHandler
import cPickle as pickle
from model1 import Model1
import pymongo
import sys

def scrape_info(sn): 

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


	return user_tweets

def process(raw_data):
	data = []

	for tweet in raw_data:
		tweet_text = tweet.get('text').encode('utf8', 'ignore').strip('\n')
		data.append(tweet_text)

	mega_tweet = " ".join(x for x in data)
	mega_tweet1 = unicode(mega_tweet, errors='ignore')

	return mega_tweet1

def predict(data, vect, dict_data, word_counts): 
	vector = vect.transform([data])
	result = linear_kernel(vector, word_counts)
	result_vector = result[0]

	indices = result_vector.argsort()[-11:-1][::-1]
	
	output = []

	for idx in indices:
		output.append(dict_data.items()[idx][0])

	return result, output

if __name__ == '__main__':
	sn = raw_input("Please enter a twitter handle: ")
	raw_data = scrape_info(sn)
	data = process(raw_data)
	with open('data/data_dict.pkl') as f: 
		dict_data = pickle.load(f)
	with open('data/vectorizer.pkl') as f: 
		vect = pickle.load(f)
	with open('data/word_counts.pkl') as f: 
		word_counts = pickle.load(f)
	result, output = predict(data, vect, dict_data, word_counts)
	print output
	