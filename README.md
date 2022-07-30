# Twitter Analysis App: Who tweeted it?

*  This application allows for a client to us a predictive model to determine which user is more likely to have tweeted a given text.
*  Framework development done using Flask-Python.
*  Queries Twitter API (tweepy).
*  Implements word2vect using SpaCy Natural Language Processing model to create embeddings from the soured tweet text.
*  Stores the embedded tweets in a SQLAlchemy Database.
*  Tweet data is fitted to a Scikit-Learn Logistic Regression model to perform predictions.
*  Finally data is then serialized (pickled) to display results for online use.  
