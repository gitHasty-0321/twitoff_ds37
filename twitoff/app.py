from flask import Flask, render_template, request
from .models import DB
import os
from .models import User
from .models import Tweet
from .twitter import add_or_update_user
from .predict import User 
from .predict import predict_user


def create_app():
    """
    Summary: Is the main app function for twitoff.
            Ties whole package together.

    """
    # __name__ is the name of the current path module
    app = Flask(__name__, instance_relative_config=True)
    
       
    # Tell app where to find database
    ## configuring by registering database with the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

    # Finally CONNECT
    DB.init_app(app)

    @app.route('/')
    def root():
        """Route to our Homepage"""
        return render_template('base.html',
                               title='Home',
                               users=User.query.all())

    @app.route('/update')
    def update():
        """Update all users"""
        users = User.query.all()
        usernames = [user.username for user in users]
        for username in usernames:
            add_or_update_user(username)

        return render_template('base.html', title='Update Users')

    @app.route('/reset')
    def reset():
        # resetting the database
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset Database')

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        """
        Summary:
            We either take name that was passed in or
            we pull it from our request.values which would be accessed
            through the user submission.

        Parameters
            -name: (str, optional, default=None)
            -message: (str, optional, returns empty string by default)

        """
        name = name or request.values['user_name']
        try:

            if request.method == 'POST':

                add_or_update_user(name)

                message = f'User "{name}" was successfully added.'

            tweets = User.query.filter(User.username == name).one().tweets

        except Exception as e:
            message = f"Error adding {name}: {e}"

            tweets = []

        return render_template('user.html',
                               title=name,
                               tweets=tweets,
                               message=message)

    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted(
                              [request.values['user0'],
                               request.values['user1']])

        if user0 == user1:
            message = 'Cannot compare users to themselves!'

        else:
            prediction = predict_user(user0,
                                      user1,
                                      request.values['tweet_text'])

            message = f"""
                            "{request.values['tweet_text']}"
                               is more likely to be said by
                                 {user1 if prediction else user0}
                                   than
                                     {user0 if prediction else user1}

                       """

        return render_template('prediction.html',
                               title='Prediction',
                               message=message)

    return app
