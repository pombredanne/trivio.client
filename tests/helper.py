from triv.io.client.api import Client
from httpretty import HTTPretty, httprettified


def auth_input():
  return 'user', 'password'

def client(cookie_path):
  return Client(
    "test.triv.io", 
    auth_input=auth_input,
    cookie_path=cookie_path + '/cookies.txt'
  )
  
# useful httppretty helpers
def github_login_flow():
  """
  Mock out triv.io api as if it exsits at test.triv.io
  """ 
  
  HTTPretty.register_uri(HTTPretty.GET,
    "http://test.triv.io/",
    body=(
      '<html><head><title>Triv.io Beta</title></head>'
      '<body>'
      '<a href="https://github.com/login/oauth/authorize"/>'
      '</body>'
      '</html>'
    ),
    status = 401,
    content_type="text/html"
  )
  
  
  HTTPretty.register_uri(HTTPretty.GET,
    "https://github.com/login/oauth/authorize",
    body="redirecting",
    status=302,
    location="http://test.triv.io/integrated"
  )
  
  # todo, create a real api-end point for logins
  HTTPretty.register_uri(HTTPretty.GET,
    "http://test.triv.io/integrated",
    body="you made it",
  )
  