from unittest import TestCase
from nose.tools import eq_

from triv.io import client as cmd
from triv.io.client.api import Client
from httpretty import HTTPretty, httprettified

from tempfile import mkdtemp
import os
import shutil


class TestCommandLine(TestCase):
  
  def setUp(self):
    self.cookie_dir = mkdtemp()
    self.cookie_path = os.path.join(self.cookie_dir, "cookies.txt")
    
  def tearDown(self):
    shutil.rmtree(self.cookie_dir)
    HTTPretty.disable()
  
  def auth_input(self):
    return 'user', 'password'
      
  def test_success(self):
    return None
    


  def test_projects(self):
    HTTPretty.enable()
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
    
