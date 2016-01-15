from flask import Flask, request, render_template
app = Flask(__name__)
import retweet_predict as rp
import cPickle as pickle

@app.route('/')
def home_page(): 
    return render_template("index.html")

@app.route('/recommend', methods=['POST'])
def screen_name():
    text = str(request.form['screen_name'])
    data = rp.get_data(text)
    output = rp.predict(data, vect, user_list, tweet_list, word_counts)
    sites = ""
    for handle in output: 
        sites +="<a href='https://twitter.com/%s' target='_blank'>%s</a><br>" %(handle, handle)

    return sites

if __name__ == '__main__':
    with open('data/retweet_user_list.pkl') as f: 
        user_list = pickle.load(f)
    with open('data/retweet_tweet_list.pkl') as f: 
        tweet_list = pickle.load(f)
    with open('data/retweet_vectorizer.pkl') as f: 
        vect = pickle.load(f)
    with open('data/retweet_word_counts.pkl') as f: 
        word_counts = pickle.load(f)
    app.run(host='0.0.0.0', port=7066, debug=True)