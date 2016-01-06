from flask import Flask, request, render_template
app = Flask(__name__)
import predict1 as p1
import cPickle as pickle

@app.route('/')
def home_page(): 
    return render_template("index.html")

@app.route('/recommend', methods=['POST'])
def screen_name():
    text = str(request.form['screen_name'])
    raw_data = p1.scrape_info(text)
    data = p1.process(raw_data)
    output = p1.predict(vect, data, dict_data, word_counts)
    sites = ""
    for handle in output: 
        sites +="<a href='https://twitter.com/%s' target='_blank'>%s</a><br><br>" %(handle, handle)

    return sites

if __name__ == '__main__':
    with open('data/ngrams_data_dict.pkl') as f: 
        dict_data = pickle.load(f)
    with open('data/ngrams_vectorizer.pkl') as f: 
        vect = pickle.load(f)
    with open('data/ngrams_word_counts.pkl') as f: 
        word_counts = pickle.load(f)
    app.run(host='0.0.0.0', port=7066, debug=True)