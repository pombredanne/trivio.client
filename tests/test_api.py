from unittest import TestCase
from nose.tools import eq_

from triv.io import client as cmd
from triv.io.client.api import Client
from httpretty import HTTPretty, httprettified

from tempfile import mkdtemp
import os
import shutil


class TestApi(TestCase):
  """
  Test verifying proper interpetation of the triv.io api.
  """
  
  def setUp(self):
    self.cookie_dir = mkdtemp()
    self.cookie_path = os.path.join(self.cookie_dir, "cookies.txt")
    
  def tearDown(self):
    shutil.rmtree(self.cookie_dir)
  
  def auth_input(self):
    return 'user', 'password'
      
  def test_success(self):
    return None
    
  @httprettified
  def test_unathorized(self):
    def request_callback(method, uri, headers):
      headers['content_type'] = "text/html"
      headers['status'] = 401
      return (
        '<html><head><title>Triv.io Beta</title></head>'
        '<body>'
        '<a href="https://github.com/login/oauth/authorize"/>'
        '</body>'
        '</html>'
      )
    
    HTTPretty.register_uri(HTTPretty.GET,
      "http://test.triv.io/",
      body=request_callback
    )
    
    HTTPretty.register_uri(HTTPretty.GET,
      "http://test.triv.io/workspaces/",
      responses=[
        HTTPretty.Response(
          body="access denied",
          status=401
        ),
        HTTPretty.Response(
          body='[]',
          content_type="application_json"
        )
        
      ]
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
           
    conn = Client(
      "test.triv.io", 
      auth_input=self.auth_input,
      cookie_path=self.cookie_path
    )
    conn.projects()
    

  @httprettified
  def test_projects(self):
    HTTPretty.register_uri(HTTPretty.GET, 
      "http://test.triv.io/",
      body="redirect",
      location="http://test.triv.io/integrated",
      status=302
    )
    
    HTTPretty.register_uri(HTTPretty.GET, 
      "http://test.triv.io/integrated",
      body=""
    )
        
    
    conn = Client(
      "test.triv.io", 
      auth_input=self.auth_input,
      cookie_path=self.cookie_path
    )
    
    HTTPretty.register_uri(HTTPretty.GET, 
      "http://test.triv.io/workspaces/",
      body='[{"title": "foo", "tables":{}}]'
    )
    
    eq_(len(conn.projects()), 1)
    
