# [START app]
import os
import urllib
import logging
import json
# import requests
# import requests_toolbelt.adapters.appengine

# [START imports]
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# requests_toolbelt.adapters.appengine.monkeypatch()
# [END imports]

# [DATABASE info]
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
CLOUDSQL_DATABASE = os.environ.get('CLOUDSQL_DATABASE')

LIVE_SQLALCHEMY_DATABASE_URI = (
    'mysql+mysqldb://{user}:{password}@/{database}'
    '?unix_socket=/cloudsql/{connection_name}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)

if os.environ.get('GAE_INSTANCE'):
    SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
# [END DATABASE info]


# [START create_app]
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = LIVE_SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
# [END create_app]

class UserData(db.Model):
    __tablename__ = 'UserData'
    Id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(255), nullable=False)
    EpicUserHandle = db.Column(db.String(255), nullable=False)
    AccountId = db.Column(db.String(255), nullable=False)
    SoloRating = db.Column(db.Integer, nullable=True)
    DuoRating = db.Column(db.Integer, nullable=True)
    SquadRating = db.Column(db.Integer, nullable=True)

    def __init__(self, email, epicuserhandle, accountid):
        self.Email = email
        self.EpicUserHandle = epicuserhandle
        self.AccountId = accountid

    def __repr__(self):
        return '<Email %r>' % self.email

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = users.get_current_user()
        email = user.email()
        url = users.create_logout_url('/')
        url_linktext = 'Logout'
        fHandle = request.form['fortnitehandle']

        resp = urlfetch.fetch('https://api.fortnitetracker.com/v1/profile/pc/'+fHandle, headers={'TRN-Api-Key' : 'e5d4ace5-28ae-4579-a6d4-fad7b8ad556d'})
        logging.info(resp.content)
        data = json.loads(resp.content)

        accountId = data["accountId"]

        currUser = UserData(
            email=email, 
            epicuserhandle=fHandle, 
            accountid=accountId
        )

        db.session.add(currUser)
        db.session.commit()

        squ = UserData.query.filter_by(Email=email)
        logging.info(squ)

        return render_template('index.html', user=user, email=email, fHandle=fHandle, url=url, url_linktext=url_linktext)
    else:
        user = users.get_current_user()
        email = ''
        fHandle = ''
        if user:
            url = users.create_logout_url('/')
            url_linktext = 'Logout'
            email = user.email()
            
            squ = UserData.query.filter_by(Email=email)

            logging.info(squ)
        else:
            url = users.create_login_url('/')
            url_linktext = 'Login'

        return render_template('index.html', user=user, email=email, url=url, url_linktext=url_linktext)

@app.route('/profile')
def profile():
    user = users.get_current_user()
    email = user.email()
    return render_template('profile.html', email=email)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

# [END app]