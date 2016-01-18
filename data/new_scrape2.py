import tweepy
from tweepy import OAuthHandler
from pymongo import MongoClient
from collections import defaultdict
import sys
import time 

consumer_key = "HXJfoPTVxH6Iqqzv4nY5SlYgO"
consumer_secret = "7LfAfz2a0LmH4dH46X4mUXSH6RTVmiS9zE1kgcBkw5NPirEkJ1"
access_token = "34633790-ENRADvdaiEsSEhudIrNRQrxZPrPcb4hMLPupf5seb"
access_token_secret = "hCKKwx5FyzpspWvnVr1wv4sU7JHlUNwVdJPPFrcL34wT3"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

client = MongoClient()
twitter = client['twitter']
new = twitter['new']

# to_scrape_list = [14800270, 15179486, 5988062, 1571270053, 5943622, 3423735975L, 2991813065L, 484837706, 35820849, 1410584018, 86975611, 2529971, 423769635, 312266530, 100250921, 15446531, 2735591, 236518540, 20929486, 1236101, 13418072, 15008449, 7179142, 1769191]

list_2 = [967159538, 15379361, 15446531, 349821958, 2195241, 20652930, 2786220516L, 21245351, 197869772, 20508720]

def scrape_info(list_of_ids): 
	my_dict = defaultdict(list)

	for one_id in list_of_ids: 
		if new.find_one({'user.id': one_id}) is None: 
			print "scraping: ", one_id
			try: 
					user_tweets = api.user_timeline(one_id, count=50)
					try: 
						new.insert(user_tweets)
					except: 
						continue
			except:
					time.sleep(300)
		else: 
			print "already existing in database: ", one_id


if __name__ == '__main__': 
	scrape_info(list_2)

