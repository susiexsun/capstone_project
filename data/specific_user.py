import tweepy
from tweepy import OAuthHandler
from pymongo import MongoClient
import sys


def scrape_info(): 
	consumer_key = XXXX
	consumer_secret = XXXX
	access_token = XXXX
	access_token_secret = XXXX

	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

	client = MongoClient()
	twitter = client['twitter']
	new = twitter['new']

	screen_names = ["louiefx"]


	for sn in screen_names: 

		try: 
			user_tweets = api.user_timeline(sn, count=50)
			print "scraping: ", sn
			new.insert(user_tweets)
		except: 
			print sys.exc_info()
			time.sleep(300)

def check(): 

	client = MongoClient()
	twitter = client['twitter']
	users = twitter['users']

	scraped = ["susiexsun", "michaeljancsy", "neiltyson", "sknthla", "SebDery", "Chris_Said", \
								"KevinSimler", "beardigsit", "tylercowen", "NinjaEconomics", "SummerRay", "slobear", \
								"kennethlove", "chrisemoody", "sepeher125", "johngreen", "hankgreen", "ddd", "TimHarford", \
								"robinhanson", "micahtredding", "johnmyleswhite", "fmanjoo", "mattyglesias", "TMFHousel", \
								"pdmsero", "cfchabris", "russpoldrack", "tanayj", "ito", "felixbot", "beaucronin", "toby_n", \
								"Snowden", 'felixsalmon', 'AlSaqqaf', "JPdeRuiter", "bbaskin", "Khanoisseur", "Upstreamism", \
								"EricTopol", "cdixon", "rafat", "ashleymayer", "vijaypande", "bbaskin"]
	
	not_scraped = []
	
	for sn in scraped: 
		record = users.find_one({'user.screen_name': sn})
		print type(record)

		type_record = str(type(record))
		a_dict = {'abc': 123}

		if type(record) != type(a_dict):
			not_scraped.append(sn)

	return not_scraped


if __name__ == '__main__':
	 scrape_info()


