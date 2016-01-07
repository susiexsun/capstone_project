import tweepy
from tweepy import OAuthHandler
from pymongo import MongoClient
import time
import os
import json
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
test = twitter['test']
cursor = twitter.test.find(no_cursor_timeout=True)

scraped = []

for document in cursor: 
	try: 
		sn = document.get('user').get('screen_name').encode('ascii')

		if sn in scraped: 
			continue

		scraped.append(sn)
		users = twitter['users']
	
		try: 
			user_tweets = api.user_timeline(sn, count=50)
			users.insert(user_tweets)
		except: 
			time.sleep(300)
	
	except: 
		continue

cursor.close()


