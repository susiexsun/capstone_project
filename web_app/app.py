from flask import Flask, request, render_template
app = Flask(__name__)
import retweet_predict as rp
import cPickle as pickle
from pymongo import MongoClient
from collections import defaultdict

@app.route('/')
def home_page(): 
    return render_template("index.html")

@app.route('/recommend', methods=['POST'])
def screen_name():
    text = str(request.form['screen_name'])
    data = rp.get_data(text)
    output = rp.predict(data, vect, text)

    client = MongoClient()
    twitter = client['twitter']
    new = twitter['new']

    tweet_output = []
    handle_output = {}

    for screen_name in output:
        docs = new.find({'user.screen_name': screen_name}).limit(3)
        for doc in docs: 
            the_id = doc.get('id')
            the_handle = doc.get('user').get('screen_name')
            tweet_output.append("https://twitter.com/jack/status/%s" % the_id)
            handle_output[the_handle] = "https://twitter.com/%s" %the_handle
    

    return render_template('results.html', tweet_output=tweet_output, handle_output=handle_output)


if __name__ == '__main__':
    with open('data/retweet_vectorizer.pkl') as f: 
        vect = pickle.load(f)
    app.run(host='0.0.0.0', port=7066, debug=True)