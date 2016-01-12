from flask import Flask, request, render_template
app = Flask(__name__)
import tweetdoc_predict2 as td_p2
import cPickle as pickle

@app.route('/')
def home_page(): 
    return render_template("index.html")

@app.route('/recommend', methods=['POST'])
def screen_name():
    text = str(request.form['screen_name'])
    raw_data = td_p2.scrape_info(text)
    data = td_p2.process(raw_data)
    output = td_p2.predict(data, vect, user_list, tweet_list, word_counts, text)
    sites = ""
    for handle in output: 
        sites +="<a href='https://twitter.com/%s' target='_blank'>%s</a><br>" %(handle, handle)

    return sites

if __name__ == '__main__':
    with open('data/tweetdoc_user_list.pkl') as f: 
        user_list = pickle.load(f)
    with open('data/tweetdoc_tweet_list.pkl') as f: 
        tweet_list = pickle.load(f)
    with open('data/tweetdoc_vectorizer.pkl') as f: 
        vect = pickle.load(f)
    with open('data/tweetdoc_word_counts.pkl') as f: 
        word_counts = pickle.load(f)
    app.run(host='0.0.0.0', port=7066, debug=True)