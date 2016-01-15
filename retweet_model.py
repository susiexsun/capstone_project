from pymongo import MongoClient
from collections import Counter
from collections import defaultdict

client = MongoClient()
twitter = client['twitter']
new = twitter['new']

class Graph():
	def __init__(self):
		self.first_gen = None
		self.second_gen = None
		self.third_gen = None

	def run_model(self, sn): 
		# 5 ids. returns list of ids for the most retweeted of friends of target
		docs = new.find({'user.screen_name': sn})

		for doc in docs: 
			an_id = doc.get('user').get('id')

		first_gen = self.most_retweets(an_id)
		self.first_gen = first_gen

		# 25 ids. list with top five retweeted of each from generation 1.
		second_dict = defaultdict(list)

		for item in first_gen:  
			second_dict[item].append(self.most_retweets(item))

		self.second_gen = second_dict

		# 125 ids. list with top five retweeted of each from generation 2. 
		second_gen_list = [x for x in second_dict.values()]
		third_dict = defaultdict(list)

		for item in second_gen_list: 
				third_dict[item].append(self.most_retweets(item))

		return self.first_gen, self.second_gen, self.third_gen


	def most_retweets(self, an_id): 
		docs = new.find({'user.id': an_id})
		
		my_counter = Counter()

		for doc in docs:
			if doc.get('retweeted') == True: 
				retweeted_handle = doc.get('retweeted_status').get('user').get('id')
				my_counter[retweeted_handle] += 1


		top_10 = [tup[0] for tup in my_counter.most_common(10)]

		return top_10

if __name__ == '__main__':
	graph = Graph()
	graph.run_model('susiexsun')
