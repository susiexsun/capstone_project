from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient
import os
import json

consumer_key = XXXX
consumer_secret = XXXX
access_token = XXXX
access_token_secret = XXXX


class Listener(StreamListener): 
	def on_data(self, data): 	
		try: 
			client = MongoClient()
			twitter = client['twitter']
			coll = twitter['test']
			tweet = json.loads(data)

			coll.insert(tweet)

		except BaseException, e: 
			print 'failed ondata', str(e)
			time.sleep(5)
			pass

	def on_error(self, status): 
		print status

if __name__ == '__main__': 
	mylistener = Listener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, mylistener)
	stream.filter(track=['the', 'is', 'to', 'of', 'and', 'a', 'be', 'in', 'that', 'have'])

