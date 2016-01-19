## Who-To-Follow

Who-To-Follow is a recommender for high quality content on Twitter. 

### Motivation

Twitter can either be an amazing learning resource or a cacophonous echo chamber, depending on how you use it. I spent many hours manually searching for the right people to follow in order to make the platform productive for my interests.

Who-To-Follow enables the discovery of high quality content, thereby encouraging people to learn, connect, and share. 

### The Data and Model

TWeets and social graphs were obtained from Twitter's REST API and stored in a MongoDB database.

The algorithm is an ensemble methods that uses Graph Theory and NLP. It transverses the Twitter graph based on retweets and then uses TD-IDF and cosine similarity on individual tweets to predict interest similarity. This model produced the best results of 5 different models. The reasons for this are as follows: 

* Retweet Graph - in the TwitterSphere, a retweet is a strongest signal of quality
* Individual tweets as documents - People have diverse interests and there are more interesting and direct matches 

This works well because <b> retweets is a signal of quality content</b>


