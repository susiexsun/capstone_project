import pymongo
from pymongo import MongoClient
from sqlalchemy import create_engine
import sys
import pandas as pd

client = MongoClient()
twitter = client['twitter']
tweets = twitter['english']

engine = create_engine("postgresql://susiesun@localhost/twitter")

docs = tweets.find({}, {'id': 1, 'user.id':1, 'text':1,'entities.urls': 1, 'created_at': 1, 'user.screen_name':1,  'user.followers_count': 1,\
											 'user.friends_count': 1, 'user.description':1})


output = []

for doc in docs: 
	temp = pull_data(doc)
	output.append(temp)


def pull_data(doc): 
	mylist = []

	mylist.append(doc.get('id'))
	mylist.append(doc.get('user').get('id'))
	mylist.append(doc.get('text'))
	mylist.append(doc.get('entities').get('urls'))
	mylist.append(doc.get('created_at'))
	mylist.append(doc.get('user').get('screen_name'))
	mylist.append(doc.get('user').get('followers_count'))
	mylist.append(doc.get('user').get('friends_count'))
	mylist.append(doc.get('user').get('description'))