## Who-To-Follow

Who-To-Follow is a recommender for high quality content on Twitter. 

### Motivation

Twitter can either be an amazing learning resource or a cacophonous echo chamber, depending on how you use it. I spent many hours manually searching for the right people to make the platform productive for my interests. I was curious what type of Machine Learning algorithm could filter a large amount of data to surface high quality, personalized content.

### Obstacles

* Noise - there are 500 million tweets a day on Twitter and a large part of it is non-content (e.g. conversations, self-promotion)
* Quality - Quality is subjective and highly personal

### The Data and Model

TWeets and social graphs were obtained from Twitter's REST API and stored in a MongoDB database.

The algorithm is an ensemble methods that uses Graph Theory and NLP. Details on the model and the decision to use them are as follows:

* Retweet Graph. Why? In the TwitterSphere, a retweet is a strongest signal of quality and best way to reduce noise.

![Model Step 1](http://i64.tinypic.com/an07zk.jpg)

* Individual tweets as documents. Why?  People have diverse interests and to use all of their texts as one document would be treating them as one homogeneous entity. 

![Model Step 2](http://postimg.org/image/nd2zmxi05/)

* TF-IDF and cosine similarity. Why? To check for interest similarity. Given the brevity of tweets, this method returned fairly good results, though I am curious to test Word2Vec. 

* Custom Scoring. This was necessitated since we used individual tweets and documents. This method produced the best results. 

### Results

The results were quite intuitive and insightful. Here is a sample output from Chris Moody - I enjoyed a Data Science talk he gave recently.

![Sample Output](http://s14.postimg.org/uxr1iyhhd/Sample_output.jpg)

As you can see, his recommendations were closely associated to Data Science. He is only following 1 of the 3 recommendations, Samim. 


