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

from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

import pusher
import pusher.gae
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
# Pro Key
app.config['SECRET_KEY'] = 'secret' 
db = SQLAlchemy(app)
# [END create_app]

def parent_key(user_key):
    return ndb.Key("OnlineUsers", user_key)

class UserData(db.Model):
    __tablename__ = 'UserData'
    Id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(255), nullable=False)
    EpicUserHandle = db.Column(db.String(255), nullable=False)
    AccountId = db.Column(db.String(255), nullable=False)
    SoloRating = db.Column(db.Integer, nullable=True)
    DuoRating = db.Column(db.Integer, nullable=True)
    SquadRating = db.Column(db.Integer, nullable=True)

    def __init__(self, email, epicuserhandle, accountid, score, mm):
        self.Email = email
        self.EpicUserHandle = epicuserhandle
        self.AccountId = accountid
        self.SoloRating = score
        self.SquadRating = mm

    def __repr__(self):
        return '<Email %r>' % self.email

class UserDataStore(ndb.Model):
    Email = ndb.StringProperty(indexed=False)
    EpicUserHandle = ndb.StringProperty(indexed=False)
    AccountId = ndb.StringProperty(indexed=False)
    SoloRating = ndb.IntegerProperty(indexed=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = users.get_current_user()
        email = user.email()
        global_Email = user.email()
        url = users.create_logout_url('/')
        url_linktext = 'Logout'
        
        fHandle = request.form['fortnitehandle']

        resp = urlfetch.fetch('https://api.fortnitetracker.com/v1/profile/pc/'+fHandle, headers={'TRN-Api-Key' : 'e5d4ace5-28ae-4579-a6d4-fad7b8ad556d'})
        data = json.loads(resp.content)

        accountId = data["accountId"]
        score = data["lifeTimeStats"][6].get('value')
        score = score.replace(',', '')
        rating = data["stats"]["p9"]["trnRating"]["valueInt"]

        currUser = UserData(
            email=email, 
            epicuserhandle=fHandle, 
            accountid=accountId,
            score=int(score),
            mm=rating
        )

        db.session.add(currUser)
        db.session.commit()

        return render_template('index.html', user=user, email=email, fHandle=fHandle, url=url, url_linktext=url_linktext)
    else:
        user = users.get_current_user()
        email = ''
        fHandle = ''
        if user:
            url = users.create_logout_url('/')
            url_linktext = 'Logout'
            email = user.email()
            global_Email = user.email()
            
            squadUser = UserData.query.filter_by(Email=email).first()
            if squadUser:
                logging.critical(squadUser.Email)
                fHandle = squadUser.EpicUserHandle
                
                return render_template('index.html', user=user, email=email, fHandle=fHandle, url=url, url_linktext=url_linktext)
        else:
            
            url = users.create_login_url('/')
            url_linktext = 'Login'

        return render_template('index.html', user=user, email=email, url=url, url_linktext=url_linktext)

@app.route('/profile')
def profile():
    user = users.get_current_user()
    email = user.email()

    squadUser = UserData.query.filter_by(Email=email).first()
    if squadUser:
        fHandle = squadUser.EpicUserHandle
        return render_template('profile.html', email=email, fHandle=fHandle)

    return render_template('profile.html', email=email)

pusher_client = pusher.Pusher(
  app_id='618751',
  key='5abda3965495f71e0f72',
  secret='67964c3ddfb15f99fc04',
  cluster='ap1',
  backend=pusher.gae.GAEBackend
)

@app.route('/search')
def search():
    logging.critical("Adding User to Data Store")
    user = users.get_current_user()
    squadUser = UserData.query.filter_by(Email=user.email()).first()
    parent = parent_key(user.email())
    user_key = ndb.Key(UserDataStore, user.email(), parent=parent)
    fetch = user_key.get()

    if fetch is None:
        logging.critical("User Added")
        dataUser = UserDataStore(key=user_key)
        dataUser.Email = user.email()
        dataUser.EpicUserHandle = squadUser.EpicUserHandle
        dataUser.AccountId = squadUser.AccountId
        dataUser.SoloRating = squadUser.SoloRating

        dataUser.put()
        pusher_client.trigger('public-channel', 'search-event', {'fHandle': squadUser.EpicUserHandle})
    # When complete
    return render_template('search.html', fHandle=squadUser.EpicUserHandle)

@app.route('/cancel')
def cancel():
    logging.critical("Deleting user")
    user = users.get_current_user()
    parent = parent_key(user.email())
    user_key = ndb.Key(UserDataStore, user.email(), parent=parent)
    fetch = user_key.get()

    if fetch is not None:
        fetch.key.delete()

    url = users.create_logout_url('/')
    url_linktext = 'Logout'
    email = user.email()
    squadUser = UserData.query.filter_by(Email=email).first()
    fHandle = squadUser.EpicUserHandle

    return render_template('index.html', user=user, email=email, fHandle=fHandle, url=url, url_linktext=url_linktext)

@app.route("/pusher/auth", methods=['POST'])
def pusher_authentication():

  auth = pusher.authenticate(
    channel=u'private-channel',
    socket_id=request.form['socket_id']
  )
  return json.dumps(auth)



# [END]

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]