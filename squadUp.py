import os
import urllib

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
        db = MySQLdb.connect(host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD, database='squadUp')

    return db


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

# [START Handel]
class Handel(webapp2.RequestHandler):

    def post(self):
        print 'hello World'
        if users.get_current_user():
                    email = users.get_current_user().email()
        handelName = self.request.get('handel')
        cursor = connect_to_cloudsql().cursor()
        sql = "INSERT INTO customers (Email, EpicUserHandle, AccountId, SoloRating, DuoRating, SquadRating) VALUES (%s, %s,%s, %d,%d, %d)"
        val = (email, handelName,"",0,0,0)
        cursor.execute(sql, val)

        # 
        # rows_to_insert = [
        #     ('handelName','','','','',email)
        # ]
        # errors = bigquery_client.insert_rows(table, rows_to_insert)
# [END Handel]

class Search(webapp2.RequestHandler):

    def post(self):
        print 'hello'

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/update', Handel),
    ('/matchmake', Search)
], debug=True)
# [END app]
