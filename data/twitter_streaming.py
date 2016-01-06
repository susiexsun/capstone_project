from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient
import os
import json

consumer_key = "HXJfoPTVxH6Iqqzv4nY5SlYgO"
consumer_secret = "7LfAfz2a0LmH4dH46X4mUXSH6RTVmiS9zE1kgcBkw5NPirEkJ1"
access_token = "34633790-ENRADvdaiEsSEhudIrNRQrxZPrPcb4hMLPupf5seb"
access_token_secret = "hCKKwx5FyzpspWvnVr1wv4sU7JHlUNwVdJPPFrcL34wT3"


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

