import numpy as np
from pymongo import MongoClient
import tweepy
from tweepy import OAuthHandler
import time


## REMOVE RT

## % of tweets being retweets

## Reading level



## DEALING WITH LINKS
#### % Links
#### % Links 

## Filter out those with a bad following to followers ratio

## Remove publications & Organizations

consumer_key = "HXJfoPTVxH6Iqqzv4nY5SlYgO"
consumer_secret = "7LfAfz2a0LmH4dH46X4mUXSH6RTVmiS9zE1kgcBkw5NPirEkJ1"
access_token = "34633790-ENRADvdaiEsSEhudIrNRQrxZPrPcb4hMLPupf5seb"
access_token_secret = "hCKKwx5FyzpspWvnVr1wv4sU7JHlUNwVdJPPFrcL34wT3"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

client = MongoClient()
twitter = client['twitter']
curated_users = twitter['curated_users']
list_of_users = curated_users.find()

curated_tweets = twitter['curated_tweets']

for user in list_of_users: 
	username = user.get('screen_name')
	print username
	try: 
			user_tweets = api.user_timeline(username, count=50)
			curated_tweets.insert(user_tweets)
	except:
			time.sleep(10)