
from pymongo import MongoClient
from collections import Counter


client = MongoClient()
twitter = client['twitter']
english = twitter['english']

def most_retweets(sn): 
	docs = english.find({'user.screen_name': sn})
	print 'hi'
	
	my_counter = Counter()

	for doc in docs:
		if doc.get('retweeted') == True: 
			retweeted_handle = doc.get('retweeted_status').get('user').get('screen_name')
			print retweeted_handle
			my_counter[retweeted_handle] += 1


	top_5 = [tup[0] for tup in my_counter.most_common(5)]

	return top_5

if __name__ == '__main__':
	top_5 = most_retweets('susiexsun')
	my_dict = {}
	for person in top_5: 
		temp = most_retweets(person)
		my_dict[person] = temp

	print my_dict

