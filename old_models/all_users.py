import numpy as np
from pymongo import MongoClient


client = MongoClient()
twitter = client['twitter']
tweets = twitter['users']

# names = tweets.distinct('user.screen_name')
# ids = tweets.distinct('user.id')

# data = []
# for num in xrange(len(names)):
# 	temp_dict = {} 
# 	temp_dict['screen_name'] =  names[num]
# 	temp_dict['id'] = ids[num]
# 	data.append(temp_dict)

# print data[1]

all_users = twitter['all_users']

# for d in data: 
# 	all_users.save(d)



test = all_users.find_one({'screen_name': 'MichaeIBotlon'})
test_id = test.get('id')
