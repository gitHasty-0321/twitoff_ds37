# Twitter Analysis App: Who tweeted it?

*  This application allows for a client to use a predictive model to determine which user is more likely to have tweeted a given text.
*  Framework development done using Flask-Python.
*  Queries Twitter API (tweepy).
*  Implements word2vect using SpaCy Natural Language Processing model to create embeddings from the soured tweet text.
*  Stores the embedded tweets in a SQLAlchemy Database.
*  Tweet data is fitted to a Scikit-Learn Logistic Regression model to perform predictions.
*  Finally data is then serialized (pickled) to display results for online use.  


# Progress in Motion:

*  Implement BERT Googles Transformer and Run binary classification for current application
*  Enhance visualizations could scale up problem and then use live data feed
*  Incorporating Redis for caching to mitigate performance issues
*  Improve UI using Bootstrap or JQuery
*  Add more fields of interest/diversify model functionality
