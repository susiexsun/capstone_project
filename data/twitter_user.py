import tweepy
from tweepy import OAuthHandler
from pymongo import MongoClient
import time
import os
import json
import time

consumer_key = XXXX
consumer_secret = XXXX
access_token = XXXX
access_token_secret = XXXX

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


