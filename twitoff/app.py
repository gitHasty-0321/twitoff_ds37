from flask import Flask, render_template
from .models import DB, User, Tweet
from .twitter import add_or_update_user

def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        
        users = User.query.all()
        
        return render_template('base.html', title='Home', users=users)

    @app.route('/populate')
    def populate():
        add_or_update_user('ryanallred')
        add_or_update_user('nasa')
        return render_template('base.html', title='Populate')

    @app.route('/update')
    def update():
        users = User.query.all()
        usernames = [user.username for user in users]
        for username in usernames:
            add_or_update_user(username)

        return render_template('base.html', title='Update')

    @app.route('/reset')
    def reset():

        # resetting the database
        DB.drop_all()
        DB.create_all()

        return render_template('base.html', title='Reset')

    return app