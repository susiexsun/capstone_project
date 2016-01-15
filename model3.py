import tryin as tr

class Model3(object): 
	def __init__(self): 

	def round_one(sn):
		ids = tr.get_ids(sn)
		data = tr.get_data(sn)
		tweet_list, user_list = tr.scrape_new_users(ids)
		vect, word_counts = tr.run_model(tweet_list, user_list)
		top_people = tr.predict(data, vect, user_list, tweet_list, word_counts)

		return top_people


