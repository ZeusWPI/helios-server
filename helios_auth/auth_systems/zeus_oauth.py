import httplib2
import json
from django.conf import settings
from django.core.mail import send_mail
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import util
import sys

util.positional_parameters_enforcement = util.POSITIONAL_IGNORE

# some parameters to indicate that status updating is not possible
STATUS_UPDATES = False

# display tweaks
LOGIN_MESSAGE = "Log in with my Zeus Account"

def get_flow(redirect_url=None):
  return OAuth2WebServerFlow(settings.ZEUS_CLIENT_ID,
            client_secret=settings.ZEUS_CLIENT_SECRET,
            redirect_uri=redirect_url,
            auth_uri="https://adams.ugent.be/oauth/oauth2/authorize/",
            token_uri="https://adams.ugent.be/oauth/oauth2/token/",
            scope="read"
            )

def get_auth_url(request, redirect_url):
  flow = get_flow(redirect_url)

  request.session['zeus_oauth-redirect-url'] = redirect_url
  return flow.step1_get_authorize_url()

def get_user_info_after_auth(request):
  flow = get_flow(request.session['zeus_oauth-redirect-url'])

  if not request.GET.has_key('code'):
    return None

  code = request.GET['code']
  credentials = flow.step2_exchange(code)
  http = httplib2.Http(".cache")
  http = credentials.authorize(http)
  (resp_headers, content) = http.request("https://adams.ugent.be/oauth/api/current_user/", "GET")

  response = json.loads(content)
  username = response['username'].strip().lower()
  # This does nothing except verify that the username is ascii
  username.decode('ascii')
  return {'type': 'zeus_oauth', 'user_id': username, 'name': username, 'info': {'email': username + '@zeus.ugent.be'}, 'token':{}}

def do_logout(user):
  return None

def update_status(token, message):
  pass

def send_message(user_id, name, user_info, subject, body):
  send_mail(subject, body, settings.SERVER_EMAIL, ["%s <%s>" % (user_id, user_id + "@zeus.ugent.be")], fail_silently=False)

def check_constraint(constraint, user_info):
  pass

def can_create_election(user_id, user_info):
  return False