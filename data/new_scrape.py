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

def scrape_info(list_of_ids): 
	my_dict = defaultdict(list)

	for one_id in list_of_ids: 
		print one_id
		try: 
				user_tweets = api.user_timeline(one_id, count=50)
				try: 
					new.insert(user_tweets)
				except: 
					continue
		except:
				time.sleep(300)

		new_list = get_following(one_id)
		for item in new_list:
			print item
			my_dict[one_id].append(item)

	print my_dict

	return [x for x in my_dict.values()]

def get_following(one_id):
	list_of_ids = []
	try: 
		for page in tweepy.Cursor(api.friends_ids, user_id = one_id).pages():
			temp = page.get('ids')
			list_of_ids.extend(temp)
	except: 
		time.sleep(300)

	return list_of_ids

if __name__ == '__main__':
	docs = new.find(no_cursor_timeout=True)
	# a_set = set()
	# for doc in docs: 
	# 	a_set.add(doc.get('user').get('id'))
	# a_list = list(a_set)
	a_list = get_following([34633790])
	gen_1 = scrape_info(a_list)
	print "gen_1 done"
	print
	gen_2 = []
	for item in gen_1: 
		gen_2.extend(scrape_info(item))
	print "gen_2 done"
	print
	gen_3 = []
	for item in gen_2: 
		gen_3.extend(scrape_info(item))
	# print "gen_3 done"
	# print
	# gen_4 = []
	# for item in gen_3: 
	# 	gen_3.extend(scrape_info(item))
	# print "gen_4 done"



