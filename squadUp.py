import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

# Imports the Google Cloud client library
# from google.cloud import bigquery

# Instantiates a client
# bigquery_client = bigquery.Client()

# # The name for the new dataset
# dataset_id = 'userData'
# table_id = 'users'  # replace with your table ID
# table_ref = bigquery_client.dataset(dataset_id).table(table_id)
# table = bigquery_client.get_table(table_ref)  # API request
# # Prepares a reference to the new dataset
# dataset_ref = bigquery_client.dataset(dataset_id)
# dataset = bigquery.Dataset(dataset_ref)

import jinja2
import webapp2



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

        # [START guestbook]

class Handel(webapp2.RequestHandler):

    def post(self):
        if users.get_current_user():
                    email = users.get_current_user().email()
        # handelName = self.request.get('handel')
        # rows_to_insert = [
        #     ('handelName','','','','',email)
        # ]
        # errors = bigquery_client.insert_rows(table, rows_to_insert)
        
# [END guestbook]

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/update', Handel),
], debug=True)
# [END app]
