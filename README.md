# Who-To-Follow

Who-To-Follow is a recommender for high quality content on Twitter. 

## Motivation

Twitter can either be an amazing learning resource or a cacophonous echo chamber, depending on how you use it. I spent many hours manually searching for the right people to follow in order to make the platform productive for my interests.

Who-To-Follow enables the discovery of high quality content, thereby encouraging people to learn, connect, and share. 

## The Data

## The Model

After trialing many models, an ensemble method of Graph and NLP produced the best results. This algorithm transverses the Twitter graph based on retweets and then uses TD-IDF and cosine similarity to predict interest similarity.

This works well because <b> retweets is a signal of quality content</b>


