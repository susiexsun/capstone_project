## Who-To-Follow

Who-To-Follow is a recommender for high quality content on Twitter. 

![Webapp Overview](http://s9.postimg.org/5emdyfd4f/overview.jpg)

Working web app at http://susiexsun.com/whotofollow.html

### Motivation

Twitter can either be an amazing learning resource or a cacophonous echo chamber, depending on how you use it. I spent many hours manually searching for the right people to make the platform productive for my interests. I was curious what type of Machine Learning algorithm could filter a large amount of data to surface high quality, personalized content.

Who-To-Follow is a webapp where you input a Twitter handle and receive a list of people recommendations. 


### The Model

The algorithm is an ensemble methods that uses Graph Theory and NLP. Details on the model and the decision to use them are as follows:

* Retweet Graph. Why? In the TwitterSphere, a retweet is a strongest signal of quality and best way to reduce noise.

![Model Step 1](http://i64.tinypic.com/an07zk.jpg)

* Individual tweets as documents. Why?  People have diverse interests and to use all of their texts as one document would be treating them as one homogeneous entity. 

![Model Step 2](http://s10.postimg.org/5n1b1w4fd/Image_Step_2.jpg)

* TF-IDF and cosine similarity. Why? To check for interest similarity. Given the brevity of tweets, this method returned fairly good results, though I am curious to test Word2Vec. 

* Custom Scoring. This was necessitated since we used individual tweets and documents. This method produced the best results. 

### Results

Here is a sample output from Chris Moody - I enjoyed a Data Science talk he gave recently.

![Sample Output](http://s14.postimg.org/uxr1iyhhd/Sample_output.jpg)

As you can see, his recommendations were closely associated to Data Science. He is only following 1 of the 3 recommendations, Samim. 

From some preliminary user testing, <b>83% of people found Who To Follow to be preferable to Triadic Closure</b>. 100% of people found it to be better than random. 

## Conclusions

This custom built algorithm is able to make intuitive and insightful recommendations. The secret sauce here is the retweet Graph structure and an elegant way to cut through the noise on the Twitter Platform. 

### Possibilities for further work

* More extensive user testing
* Refining the model: adding a Page-Rank like component for retweets 
* Broader applications: Apply the algorithm to other taste-driven products with discovery problems, such as music, TV shows, podcasts. Given the complexity of these products, a Social Graph + Content Analysis machine learning algorithm may produce great recommendations.

## Repo Structure

* retweet_model.py - creates the retweet graph
* retweet_predict.py - runs cosine similarity and the custom scoring method
* retweet_vect.py - creates the TF-IDF model

#### Data
* scrape_with_graph.py - Pulling Graph and Tweets from Twitter's User Timeline and Friend Ids using Tweepy
* twitter_streaming.py - Pulling Data from Twitter's streaming API using Tweepy's StreamListener
* twitter_user.py - Collecting user timelines using IDs seeded from Twitter Streaming
* specific_user.py - Used for QA and troubleshooting. Scrapes and confirms specific people are in the database. 

#### Old Models
Legacy code on the various models that were tested during the course of experimentation.

#### Web_App
* web_app.py - Runs the web_app using Flask and Jinga
* Static - HTML pages that run the homepage and recommendations page
* Templates - Templates from Bootstrap.






