# [START app]
import os
import urllib
import logging

# [START imports]
from google.appengine.api import users
from google.appengine.ext import ndb

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# [END imports]

# [DATABASE info]

CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
CLOUDSQL_DATABASE = os.environ.get('CLOUDSQL_DATABASE')

LIVE_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@3306/{database}'
    '?unix_socket=/cloudsql/{connection_name}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)

if os.environ.get('GAE_INSTANCE'):
    SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI

# [END DATABASE info]


# [START create_app]
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = LIVE_SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
# [END create_app]

class SquadUser(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(255), nullable=True)
    EpicUserHandle = db.Column(db.String(255), nullable=True)
    AccountId = db.Column(db.String(255), nullable=True)
    SoloRating = db.Column(db.Integer, nullable=True)
    DuoRating = db.Column(db.Integer, nullable=True)
    SquadRating = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Email %r>' % self.email

@app.route('/')
def index():
    user = users.get_current_user()
    email = ''
    fhandle = ''
    if user:
        url = users.create_logout_url('/')
        url_linktext = 'Logout'
        email = user.email()
        
        logging.critical(SquadUser.query.all())
    else:
        url = users.create_login_url('/')
        url_linktext = 'Login'

    return render_template('index.html', user=user, email=email, url=url, url_linktext=url_linktext)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

# [END app]




# import jinja2

# import MySQLdb

# # These environment variables are configured in app.yaml.
# CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
# CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
# CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

# def connect_to_cloudsql():
#     if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
#         cloudsql_unix_socket = os.path.join(
#             '/cloudsql', CLOUDSQL_CONNECTION_NAME)

#         db = MySQLdb.connect(
#             unix_socket=cloudsql_unix_socket,
#             user=CLOUDSQL_USER,
#             passwd=CLOUDSQL_PASSWORD)

#         logging.critical('We have connnected to squadup sql')
#     else:
#         db = MySQLdb.connect(host='35.197.191.91', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

#     return db

# JINJA_ENVIRONMENT = jinja2.Environment(
#     loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
#     extensions=['jinja2.ext.autoescape'],
#     autoescape=True)

# class MainPage(webapp2.RequestHandler):

#     def get(self):
#         fHandle = ""
#         email = ""
#         user = users.get_current_user()
#         if user:
#             url = users.create_logout_url(self.request.uri)
#             url_linktext = 'Logout'

#             email = user.email()

#             dbc = connect_to_cloudsql()
#             cursor = dbc.cursor()

#             cursor.execute('USE squadUp;')
#             cursor.execute('Select FortniteHandle from squadusers where email like "'+ email +'";')
#             myresult = cursor.fetchall()

#             for x in myresult:
#                 fHandle = x

#             logging.critical(fHandle)
#             cursor.close()
#             dbc.close()
#             logging.critical('We have closed the connection')
#         else:
#             url = users.create_login_url(self.request.uri)
#             url_linktext = 'Login'

#         template_values = {
#             'user': user,
#             'fHandle': fHandle,
#             'email': email,
#             'url': url,
#             'url_linktext': url_linktext,
#         }

#         template = JINJA_ENVIRONMENT.get_template('index.html')
#         self.response.write(template.render(template_values))

# # [START profileUpdate]
# class ProfileUpdate(webapp2.RequestHandler):

#     def post(self):
#         logging.critical('Save Fortnite Handle')

#         user = users.get_current_user()
#         email = ''

#         if user:
#             email = user.email()
#             url = users.create_logout_url(self.request.uri)
#             url_linktext = 'Logout'

#         fortnitehandle = self.request.get('fortnitehandle')

#         logging.critical('Fortnite Handle: ' + fortnitehandle)

#         dbc = connect_to_cloudsql()
#         cursor = dbc.cursor()
#         cursor.execute('USE squadUp;')
#         sql = "INSERT INTO squadusers (Email, FortniteHandle, AccountId, Solo, Duo, Squad) VALUES ('%s', '%s', '%s', %d, %d, %d);" % (email, fortnitehandle, 'hello', 0, 0, 0)
#         cursor.execute(sql)
#         cursor.close()
#         dbc.close()

#         logging.critical('We have closed the connection')

#         template_values = {
#             'user': user,
#             'fHandle': fortnitehandle,
#             'email': email,
#             'url': url,
#             'url_linktext': url_linktext,
#         }

#         template = JINJA_ENVIRONMENT.get_template('index.html')
#         self.response.write(template.render(template_values))
# # [END Handel]

# [START app]
# app = webapp2.WSGIApplication([
#     ('/', MainPage),
#     ('/update', ProfileUpdate),
# ], debug=True)
# [END app]
