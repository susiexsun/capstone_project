## Who-To-Follow

Who-To-Follow is a recommender for high quality content on Twitter. 

### Motivation

Twitter can either be an amazing learning resource or a cacophonous echo chamber, depending on how you use it. I spent many hours manually searching for the right people to make the platform productive for my interests. I was curious what type of Machine Learning algorithm could filter a large amount of data to surface high quality, personalized content. Hence Who-To-Follow was created.

Who-To-Follow enables the discovery of high quality content, encouraging people to learn, connect, and share. 

### The Data and Model

TWeets and social graphs were obtained from Twitter's REST API and stored in a MongoDB database.

The algorithm is an ensemble methods that uses Graph Theory and NLP. It transverses the Twitter graph based on retweets and then uses TD-IDF and cosine similarity on individual tweets to predict interest similarity. This model produced the best results of 5 different models. Details on the model and the decision to use them are as follows:  

* Retweet Graph - in the TwitterSphere, a retweet is a strongest signal of quality. This is a way to reduce noise.

![Model Step 1](http://postimg.org/image/4x6y3wubn/)

* Individual tweets as documents. Why?  People have diverse interests and to use all of their texts as one document would be treating them as one homogeneous entity. 



