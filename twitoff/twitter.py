import tweepy
import spacy
from os import getenv
from .models import DB
from .models import Tweet
from .models import User

# Getting our environment variables
# API KEYS
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_KEY_SECRET')

# Making the connection to the Twitter API
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)


def add_or_update_user(username):

    try:

        # Get the user information
        twitter_user = TWITTER.get_user(screen_name=username)

        # If there is no user in the database then create one
        # If there IS a user in the database, let's have that be our db_user
        db_user = (User.query.get(twitter_user.id)
                   or User(id=twitter_user.id,
                   username=username))

        # Add User to the DataBase if they didn't already exist
        DB.session.add(db_user)

        # Get all the tweets of added user
        tweets = twitter_user.timeline(count=200,
                                       exclude_replies=True,
                                       include_rts=False,
                                       tweet_mode='extended',
                                       since_id=db_user.newest_tweet_id)

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # Add all the tweets to the DataBase session
        for tweet in tweets:

            tweet_vector = vectorize_tweet(tweet.full_text)

            db_tweet = Tweet(id=tweet.id,
                             text=tweet.full_text[:300],
                             vect=tweet_vector)

            db_user.tweets.append(db_tweet)

            DB.session.add(db_tweet)

    except Exception as error:
        print(f"Error Processing {username}: {error}")
        raise error

    else:
        # Save (possibly New User) and/or tweets to the database
        DB.session.commit()


nlp = spacy.load('C:\\Users\\steve\\tweepy\\TweetyPy\\my_model')


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector
