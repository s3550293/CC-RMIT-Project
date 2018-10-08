import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

# Imports the Google Cloud client library
from google.cloud import bigquery

import jinja2
import webapp2

# Instantiates a client
bigquery_client = bigquery.Client()

# The name for the new dataset
dataset_id = 'userData'

# Prepares a reference to the new dataset
dataset_ref = bigquery_client.dataset(dataset_id)
dataset = bigquery.Dataset(dataset_ref)


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
# class Handel(webapp2.RequestHandler):

#     def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
        
# [END guestbook]

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    # ('/update', Handel),
], debug=True)
# [END app]
