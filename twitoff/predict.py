from .models import User
import numpy as np
from sklearn.linear_model import LogisticRegression
from .twitter import vectorize_tweet


def predict_user(user0_name, user1_name, hypo_tweet_text):
    """predict_user() summary:
        Determine and return which user is more likely to say a given tweet.

    Parameters
    ----------
    user0_name : str, valid Twitter username

        If the string that is passed is not a valid Twitter
        username the function will return an error. 'user1_name'
        has parallel use-cases and applications, i.e. parameter definitions
        are interchangeable.

    user1_name : str, valid Twitter username

        If the string that is passed is not a valid Twitter
        username the function will return an error. 'user0_name'
        has parallel use-cases and applications, i.e. parameter definitions
        are interchangeable.

    hypo_tweet_text : str, tweet-like object

        Any valid string is acceptable. The string should
        emulate the likeness of a twitter post from one of the
        given users.

    Example: predict_user("elonmusk", "jackblack", "Tesla cars go vroom")
    Returns: 0 (user0_name: "elonmusk") or a 1 (user1_name: "jackblack")
    """
    # Query Database for Users
    # Desired Users MUST be in Database
    user0 = User.query.filter(User.username == user0_name).one()
    user1 = User.query.filter(User.username == user1_name).one()

    # 2-Dimensional Arrays
    # Getting tweet vectors from each tweet for each user
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # Vertically stack tweet_vects to get one numpy array
    # X-matrix for training the logistic regression
    vects = np.vstack([user0_vects, user1_vects])

    # 1-Dimensional Arrays
    zeros = np.zeros(len(user0.tweets))
    ones = np.ones(len(user1.tweets))

    # y-vector (target) for training the logistic regression
    labels = np.concatenate([zeros, ones])

    # instantiate our logistic regression model
    log_reg = LogisticRegression()

    # fit our logistic regression model to the data
    # (X_vects, y_labels)
    log_reg.fit(vects, labels)

    # vectorize (get the word embeddings) for
    # our hypothetical tweet to pass into .predict()
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    # get prediction for which user is more likely
    # to say the hypo_tweet_text
    prediction = log_reg.predict(hypo_tweet_vect.reshape(1, -1))

    return prediction[0]
