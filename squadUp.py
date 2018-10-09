import os
import urllib
import logging

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2
import MySQLdb

# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

def connect_to_cloudsql():

    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD)

    else:
        db = MySQLdb.connect(host='35.197.191.91', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

    return db

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):

    def get(self):
        fHandle = ""
        email = ""
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

            email = user.email()

            db = connect_to_cloudsql()
            cursor = db.cursor()

            cursor.execute('USE squadUp;')
            cursor.execute('Select FortniteHandle from squadusers where email like "'+ email +'";')
            myresult = cursor.fetchall()

            logging.critical(myresult)

            for x in myresult:
                fHandle = x

            cursor.close()
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'fHandle': fHandle,
            'email': email,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

# [START Handel]
class ProfileUpdate(webapp2.RequestHandler):

    def post(self):
        logging.critical('Save Fortnite Handle')

        user = users.get_current_user()
        email = ''

        if user:
            email = user.email()
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'

        fortnitehandle = self.request.get('fortnitehandle')

        logging.critical('Fortnite Handle: ' + fortnitehandle)

        db = connect_to_cloudsql()
        cursor = db.cursor()
        cursor.execute('USE squadUp;')
        sql = "INSERT INTO squadusers (Email, FortniteHandle, AccountId, Solo, Duo, Squad) VALUES ('%s', '%s', '%s', %d, %d, %d);" % (email, fortnitehandle, 'hello', 0, 0, 0)
        cursor.execute(sql)
        cursor.close()

        template_values = {
            'user': user,
            'fHandle': fortnitehandle,
            'email': email,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END Handel]

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/update', ProfileUpdate),
], debug=True)
# [END app]
